#!/usr/bin/env python3
"""Task-aware worktree inventory and guarded single-worktree closeout."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import uuid

STATES = ("active", "review", "merge", "verify", "paused", "done")
OPERATIONS = ("MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD", "rebase-merge",
              "rebase-apply", "sequencer", "BISECT_LOG")
WORKSPACE = None
GIT_PATH_OVERRIDES = ("GIT_DIR", "GIT_COMMON_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE",
                      "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES")


class Error(Exception):
    pass


class NotRepository(Error):
    pass


def global_home():
    configured = os.environ.get("JOYSTACK_HOME")
    return Path(configured).expanduser() if configured else Path.home() / ".joystack"


def checked_path(path, label="path"):
    resolved = Path(path).expanduser().resolve()
    if WORKSPACE is not None and not resolved.is_relative_to(WORKSPACE):
        raise Error(f"Workspace boundary: {label} resolves outside {WORKSPACE}: {resolved}")
    return resolved


def check_git_paths(repo):
    """Check gitfile/common-dir before invoking Git, not just checkout location."""
    path = checked_path(repo, "Git cwd")
    if WORKSPACE is None:
        return
    for name in GIT_PATH_OVERRIDES:
        if os.environ.get(name):
            raise Error(f"Workspace boundary: inherited {name} redirects Git paths; clear it first")
    for parent in (path, *path.parents):
        if not parent.is_relative_to(WORKSPACE):
            break
        marker = checked_path(parent / ".git", "Git marker")
        if marker.is_file():
            content = marker.read_text().strip()
            if not content.startswith("gitdir: "):
                raise Error("Workspace boundary: invalid .git pointer")
            gitdir = checked_path(parent / content[8:], "Git directory")
        elif marker.is_dir():
            gitdir = checked_path(marker, "Git directory")
        elif (parent / "HEAD").is_file() and ((parent / "objects").is_dir() or (parent / "commondir").is_file()):
            gitdir = checked_path(parent, "Git directory")
        else:
            continue
        common_file = checked_path(gitdir / "commondir", "Git common-dir pointer")
        common = checked_path(gitdir / common_file.read_text().strip(), "Git common-dir") if common_file.is_file() else gitdir
        # These Git paths may themselves be symlinks; inspect before native Git writes.
        for base, names in ((gitdir, ("HEAD", "index", "config.worktree", "logs")),
                            (common, ("config", "objects", "refs", "refs/heads", "logs", "logs/refs/heads", "worktrees"))):
            for name in names:
                checked_path(base / name, "Git metadata " + name)
        return
    raise NotRepository("No Git repository inside the workspace boundary")


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def absolute(path):
    return str(Path(path).expanduser().resolve())


def git(repo, *args, check=True, timeout=30):
    check_git_paths(repo)
    result = subprocess.run(
        ["git", "-C", str(repo), *args], stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, env={**os.environ, "GIT_OPTIONAL_LOCKS": "0", "LC_ALL": "C"},
        timeout=timeout,
    )
    if check and result.returncode:
        raise Error(os.fsdecode(result.stderr).strip() or f"git {args[0]} failed")
    return result


def text(result):
    return os.fsdecode(result.stdout).rstrip("\n")


def revision(repo, ref):
    return text(git(repo, "rev-parse", "--verify", "--end-of-options", ref + "^{commit}"))


def repository(path):
    discovery = git(path, "rev-parse", "--path-format=absolute", "--git-common-dir", check=False)
    if discovery.returncode:
        message = os.fsdecode(discovery.stderr).strip()
        if message.startswith("fatal: not a git repository"):
            raise NotRepository(message)
        raise Error(message or "Unable to discover Git repository")
    common = str(checked_path(text(discovery), "Git common-dir"))
    top = git(path, "rev-parse", "--path-format=absolute", "--show-toplevel", check=False)
    if top.returncode == 0:
        checked_path(text(top), "Git working tree")
    rows = worktrees(common)
    name = Path(rows[0]["path"]).name if rows else Path(common).name
    return {"id": hashlib.sha256(os.fsencode(common)).hexdigest()[:12],
            "common_dir": common, "name": name}


def worktrees(repo):
    # -z preserves spaces, tabs, newlines and non-ASCII path/branch names.
    rows, row = [], {}
    for token in os.fsdecode(git(repo, "worktree", "list", "--porcelain", "-z").stdout).split("\0"):
        if not token:
            if row:
                rows.append(row)
                row = {}
            continue
        key, _, value = token.partition(" ")
        if key == "worktree":
            row["path"] = absolute(value)
        elif key == "HEAD":
            row["head"] = value
        elif key == "branch":
            row["branch"] = value.removeprefix("refs/heads/")
        else:
            row[key] = value or True
    for i, item in enumerate(rows):
        item["primary"] = i == 0
    return rows


def empty_index():
    return {"version": 1, "repositories": {}, "worktrees": {}}


def load_index(path):
    checked_path(path, "task index")
    if not path.exists():
        return empty_index()
    try:
        data = json.loads(path.read_text())
        if (data.get("version") != 1 or not isinstance(data.get("repositories"), dict)
                or not isinstance(data.get("worktrees"), dict)):
            raise ValueError("unsupported index schema")
        for key, repo in data["repositories"].items():
            if (repo["id"] != key or not isinstance(repo["common_dir"], str)
                    or not isinstance(repo["name"], str)):
                raise ValueError("invalid repository entry")
            checked_path(repo["common_dir"], "recorded Git common-dir")
        for key, entry in data["worktrees"].items():
            if (entry["path"] != key or entry["repository_id"] not in data["repositories"]
                    or entry["state"] not in STATES):
                raise ValueError("invalid worktree entry")
            checked_path(key, "recorded worktree")
            for field in ("task", "session", "target", "cleanup_when", "updated_at", "registered_at"):
                if not isinstance(entry[field], str) or not entry[field].strip():
                    raise ValueError(f"invalid worktree {field}")
            if not isinstance(entry.get("keep_reason", ""), str):
                raise ValueError("invalid retention reason")
            if entry.get("reason") is not None and (not isinstance(entry["reason"], str) or not entry["reason"].strip()):
                raise ValueError("invalid isolation reason")
        return data
    except (ValueError, KeyError, TypeError, AttributeError) as exc:
        raise Error(f"Invalid index {path}: {exc}; preserve it and repair explicitly") from exc


@contextmanager
def locked_index(path):
    # All writers serialize read-modify-write; reports never create an index/lock.
    checked_path(path, "task index")
    checked_path(str(path) + ".lock", "task index lock")
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    with open(str(path) + ".lock", "a+b") as lock:
        if os.name == "nt":
            import msvcrt
            lock.seek(0)
            lock.write(b"\0")
            lock.flush()
            lock.seek(0)
            msvcrt.locking(lock.fileno(), msvcrt.LK_LOCK, 1)
        else:
            import fcntl
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        try:
            yield load_index(path)
        finally:
            if os.name == "nt":
                lock.seek(0)
                msvcrt.locking(lock.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


def save_json(path, data):
    checked_path(path, "JSON output")
    fd, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "w") as stream:
            json.dump(data, stream, indent=2, ensure_ascii=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def actual_worktree(path):
    path = str(checked_path(path, "worktree"))
    repo = repository(path)
    row = next((r for r in worktrees(repo["common_dir"]) if r["path"] == path), None)
    if not row or row.get("primary") or row.get("bare"):
        raise Error("Select an exact linked worktree path, not the primary checkout or a subdirectory")
    return repo, row


def remember(data, repo, row, args, created=False):
    old = data["worktrees"].get(row["path"], {})
    if old and old["repository_id"] != repo["id"]:
        raise Error("Path belongs to a different recorded repository; reconcile the old entry first")
    if old and (old["task"] != args.task or old["session"] != args.session):
        raise Error("Task/session ownership changed; use update with an explicit --state for handoff")
    entry = {**old, "id": old.get("id", str(uuid.uuid4())), "repository_id": repo["id"],
             "path": row["path"], "branch": row.get("branch"), "task": args.task,
             "reason": old.get("reason") or args.reason,
             "session": args.session, "target": args.target, "cleanup_when": args.cleanup_when,
             "state": old.get("state", "active") if old.get("branch") == row.get("branch") else "active",
             "keep_reason": old.get("keep_reason", ""), "updated_at": now(),
             "registered_at": old.get("registered_at", now()),
             "created_at": old.get("created_at", now() if created else None),
             "source": old.get("source", "joy-git" if created else "adopted")}
    if args.base:
        entry["base_commit"] = revision(repo["common_dir"], args.base)
    elif "base_commit" not in entry:
        entry["base_commit"] = None
    data["repositories"][repo["id"]] = repo
    data["worktrees"][row["path"]] = entry
    return entry


def slug(value):
    result = re.sub(r"[^\w.-]+", "-", value).strip(".-")[:80]
    if not result:
        raise Error("Task/slug needs a meaningful directory name")
    return result


def create(args, index):
    repo = repository(args.repo)
    base = revision(repo["common_dir"], args.base or args.target)
    revision(repo["common_dir"], args.target)
    # Git expands checkout shorthand such as @{-1}; check/write the same ref.
    args.branch = text(git(repo["common_dir"], "check-ref-format", "--branch", args.branch))
    root = checked_path(args.root, "worktree root")
    path = root / (slug(repo["name"]) + "-" + repo["id"]) / slug(args.slug or args.task)
    path = checked_path(path, "worktree destination")
    if path.is_relative_to(Path(repo["common_dir"])):
        raise Error("Worktree destination must be outside Git's metadata directory")
    if path.exists() or path.is_symlink():
        raise Error(f"Destination already exists: {path}; inspect/adopt instead of retrying")
    for row in worktrees(repo["common_dir"]):
        checkout = Path(row["path"])
        if path.is_relative_to(checkout) and not row.get("bare"):
            ignored = git(checkout, "check-ignore", "-q", "--", str(path), check=False)
            if ignored.returncode:
                raise Error("Project-local worktree destination must already be ignored; no automatic .gitignore edit")
    plan = {"action": "create", "applied": False, "path": str(path), "branch": args.branch,
            "base_commit": base, "target": args.target, "task": args.task,
            "reason": args.reason, "session": args.session}
    if not args.apply:
        return plan
    with locked_index(index) as data:
        if str(path) in data["worktrees"]:
            raise Error("Destination has an existing task record; reconcile it before creation")
        path.parent.mkdir(parents=True, exist_ok=True)
        for relative in ("refs/heads/" + args.branch, "logs/refs/heads/" + args.branch):
            checked_path(Path(repo["common_dir"]) / relative, "new branch metadata")
        creation_error = None
        try:
            git(repo["common_dir"], "worktree", "add", "-b", args.branch, "--", str(path), base)
        except (Error, OSError, subprocess.TimeoutExpired) as exc:
            creation_error = exc
        try:
            observed_repo, row = actual_worktree(path)
        except (Error, OSError, subprocess.TimeoutExpired) as exc:
            raise Error(f"Creation failed or is unconfirmed at {path}: {creation_error or exc}. "
                        "Inspect Git and the destination before retrying; no task registered") from exc
        if (observed_repo["id"] != repo["id"] or row.get("branch") != args.branch
                or row.get("head") != base):
            raise Error(f"Path conflict or creation unconfirmed at {path}: observed repository, branch "
                        "or HEAD does not match this request. Preserve the directory; no task registered")
        if creation_error:
            # Matching coordinates do not prove this failed invocation created it.
            raise Error(f"Git creation/setup failed: {creation_error}. Matching worktree present at {path}, "
                        "but ownership is unconfirmed; not registered. Inspect hooks/setup and explicitly "
                        "register only after confirming ownership; do not recreate") from creation_error
        try:
            # Pin the base actually used, even if a ref moves while creation runs.
            args.base = base
            entry = remember(data, repo, row, args, created=True)
            save_json(index, data)
        except Exception as exc:
            raise Error(f"Worktree created at {path}, but registration failed: {exc}. "
                        "Inspect, then register; do not recreate") from exc
    return {**plan, "applied": True, "record": entry}


def mutate(args, index):
    with locked_index(index) as data:
        path = str(checked_path(args.path, "worktree"))
        if args.command == "forget":
            entry = data["worktrees"].get(path)
            if not entry:
                raise Error("No task record for this path")
            repo = data["repositories"][entry["repository_id"]]
            if (Path(path).exists() or Path(path).is_symlink()
                    or any(r["path"] == path for r in worktrees(repo["common_dir"]))):
                raise Error("Path still exists or Git still registers it; preserve the record")
            del data["worktrees"][path]
            result = {"forgotten": path, "worktree_deleted": False}
        else:
            repo, row = actual_worktree(path)
            if args.command == "register":
                revision(repo["common_dir"], args.target)
                result = remember(data, repo, row, args)
            else:
                result = data["worktrees"].get(path)
                if not result or result["repository_id"] != repo["id"]:
                    raise Error("No matching task record; register it first")
                if result.get("branch") != row.get("branch"):
                    raise Error("Worktree branch changed; inspect and explicitly register its new purpose")
                handoff = any(getattr(args, key, None) not in (None, result[key]) for key in ("task", "session"))
                if handoff and args.state is None:
                    raise Error("Task/session handoff requires an explicit --state; completion is not inherited")
                for key in ("state", "task", "reason", "session", "target", "cleanup_when", "keep_reason"):
                    value = getattr(args, key, None)
                    if value is not None:
                        if key == "target":
                            revision(repo["common_dir"], value)
                        result[key] = value
                result["updated_at"] = now()
        save_json(index, data)
        return result


def snapshot(repo, row, entry, review_days):
    result = {**row, "repository_id": repo["id"], "repository": repo["name"],
              "task": entry.get("task") if entry else None,
              "reason": entry.get("reason") if entry else None,
              "state": entry.get("state") if entry else "unknown",
              "record": entry, "ref_freshness": "local-only", "cleanup_blockers": []}
    blockers = result["cleanup_blockers"]
    try:
        checked_path(row["path"], "listed worktree")
    except Error as exc:
        result["inspection_error"] = str(exc)
        blockers.append("outside-workspace")
        result["cleanup"] = "blocked"
        return result
    if row.get("primary") or row.get("bare"):
        blockers.append("primary-or-bare")
    if not entry:
        blockers.append("purpose-unknown")
    else:
        if entry["state"] != "done":
            blockers.append("task-not-done")
        if entry.get("keep_reason"):
            blockers.append("explicit-retention")
        if entry.get("branch") != row.get("branch"):
            blockers.append("branch-changed")
        try:
            updated = datetime.fromisoformat(entry["updated_at"])
            result["review_due"] = (datetime.now(timezone.utc) - updated).days >= review_days
        except (KeyError, ValueError, TypeError):
            result["review_due"] = None
    if row.get("locked"):
        blockers.append("git-locked")
    if row.get("prunable") or not Path(row["path"]).exists():
        blockers.append("missing-or-prunable")
    if not row.get("bare") and "missing-or-prunable" not in blockers:
        try:
            changes = git(row["path"], "status", "--porcelain=v1", "-z", "--untracked-files=all",
                          "--ignored=matching", "--ignore-submodules=none").stdout.split(b"\0")
            result["dirty"] = any(c and not c.startswith(b"!! ") for c in changes)
            result["ignored_files"] = any(c.startswith(b"!! ") for c in changes)
            if result["dirty"]:
                blockers.append("uncommitted-or-untracked")
            if result["ignored_files"]:
                blockers.append("ignored-files-need-review")
            gitdir = Path(text(git(row["path"], "rev-parse", "--absolute-git-dir")))
            result["operations"] = [name for name in OPERATIONS if (gitdir / name).exists()]
            if result["operations"]:
                blockers.append("git-operation-in-progress")
            result["last_commit_at"] = text(git(row["path"], "log", "-1", "--format=%cI", "HEAD"))
            if entry:
                target = revision(repo["common_dir"], entry["target"])
                result["target_commit"] = target
                adopted = git(repo["common_dir"], "merge-base", "--is-ancestor", row["head"], target, check=False)
                if adopted.returncode == 1:
                    blockers.append("head-not-in-target-history")
                elif adopted.returncode:
                    raise Error("Unable to check target ancestry")
            upstream = git(row["path"], "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}", check=False)
            if upstream.returncode == 0:
                result["upstream"] = text(upstream)
                counts = text(git(row["path"], "rev-list", "--left-right", "--count", "HEAD...@{upstream}")).split()
                result["ahead"], result["behind"] = map(int, counts)
        except (Error, OSError, ValueError, subprocess.TimeoutExpired) as exc:
            result["inspection_error"] = str(exc)
            blockers.append("inspection-failed")
    result["cleanup"] = "needs-occupancy-review" if not blockers else "blocked"
    return result


def inventory(args, index):
    data = load_index(index)
    repos, errors = {}, []
    unresolved_paths = []
    if args.repo:
        for path in args.repo:
            try:
                repo = repository(path)
                repos[repo["id"]] = repo
            except (Error, OSError, subprocess.TimeoutExpired) as exc:
                errors.append({"requested_path": absolute(path), "error": str(exc)})
    else:
        repos.update(data["repositories"])
        root = checked_path(global_home() / "worktrees", "managed worktree root")
        if root.exists():
            try:
                for group in root.iterdir():
                    if not group.is_dir():
                        continue
                    if (group / ".git").exists():
                        continue  # Legacy flat worktree; default discovery only follows grouped layout.
                    if not re.fullmatch(r".+-[0-9a-f]{12}", group.name):
                        unresolved_paths.append(str(checked_path(group, "non-grouped managed directory")))
                        continue
                    candidates = [child for child in group.iterdir() if child.is_dir()]
                    for candidate in candidates:
                        if not (candidate / ".git").exists():
                            unresolved_paths.append(str(checked_path(candidate, "unresolved managed directory")))
                            continue
                        try:
                            repo = repository(candidate)
                            repos[repo["id"]] = repo
                        except (Error, OSError, subprocess.TimeoutExpired) as exc:
                            errors.append({"requested_path": str(candidate), "error": str(exc)})
            except (Error, OSError) as exc:
                errors.append({"requested_path": str(root), "error": str(exc)})
        try:
            repo = repository(Path.cwd())
            repos[repo["id"]] = repo
        except NotRepository:
            pass  # Outside Git: only the explicitly registered repositories.
        except (Error, OSError, subprocess.TimeoutExpired) as exc:
            errors.append({"requested_path": str(Path.cwd()), "error": str(exc)})
    rows = []
    for repo in repos.values():
        try:
            observed = worktrees(repo["common_dir"])
            paths = {row["path"] for row in observed}
            for row in observed:
                entry = data["worktrees"].get(row["path"])
                if entry and entry["repository_id"] != repo["id"]:
                    entry = None
                rows.append(snapshot(repo, row, entry, args.review_days))
            for path, entry in data["worktrees"].items():
                if entry["repository_id"] == repo["id"] and path not in paths:
                    rows.append({"path": path, "repository_id": repo["id"], "repository": repo["name"],
                                 "task": entry["task"], "state": entry["state"], "record": entry,
                                 "cleanup": "blocked", "cleanup_blockers": ["not-registered-in-git"]})
        except (Error, OSError, subprocess.TimeoutExpired) as exc:
            errors.append({"repository_id": repo["id"], "common_dir": repo["common_dir"], "error": str(exc)})
    return {"observed_at": now(), "coverage": "explicit-repositories" if args.repo else "known-repositories-plus-managed-root-and-current-if-git",
            "workspace": str(WORKSPACE) if WORKSPACE else None,
            "index": str(index), "repositories": list(repos.values()), "worktrees": rows,
            "repository_errors": errors, "unresolved_managed_paths": sorted(set(unresolved_paths)),
            "deletion_authorized": False,
            "activity": "Session/process occupancy must be checked separately; commit/record age is not activity."}


def closeout_snapshot(data, path):
    entry = data["worktrees"].get(path)
    if not entry:
        raise Error("No registered task for this exact worktree path")
    repo = data["repositories"][entry["repository_id"]]
    row = next((item for item in worktrees(repo["common_dir"]) if item["path"] == path), None)
    if not row:
        raise Error("Git no longer registers this path; inspect and use forget only after the directory is absent")
    return repo, entry, snapshot(repo, row, entry, review_days=0)


def occupied_cwd(path):
    if not shutil.which("lsof"):
        raise Error("lsof is unavailable; process occupancy cannot be checked automatically")
    result = subprocess.run(["lsof", "-n", "-P", "-d", "cwd", "-F0n"],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20)
    if result.returncode not in (0, 1):
        raise Error("lsof failed; process occupancy remains unknown")
    root = Path(path)
    for field in result.stdout.split(b"\0"):
        if field.startswith(b"n"):
            try:
                if Path(os.fsdecode(field[1:])).resolve().is_relative_to(root):
                    return True
            except (OSError, ValueError):
                raise Error("Unable to resolve a process working directory")
    return False


def closeout(args, index):
    path = str(checked_path(args.path, "worktree"))

    def plan(data):
        repo, entry, row = closeout_snapshot(data, path)
        return repo, entry, row, {"path": path, "branch": row.get("branch"),
                                  "target": entry["target"], "cleanup": row["cleanup"],
                                  "blockers": row["cleanup_blockers"], "applied": False,
                                  "branch_retained": True}

    if not args.apply:
        return plan(load_index(index))[3]
    if not args.sessions_clear:
        raise Error("--sessions-clear is required after checking caller sessions and other process use")
    with locked_index(index) as data:
        repo, entry, row, result = plan(data)
        if row["cleanup"] != "needs-occupancy-review":
            raise Error("Closeout blocked: " + ", ".join(row["cleanup_blockers"]))
        if Path.cwd().resolve().is_relative_to(Path(path)) or occupied_cwd(path):
            raise Error("A process is using this worktree as its working directory")
        # Re-read the target and worktree immediately before the native removal.
        _, _, fresh = closeout_snapshot(data, path)
        if fresh["cleanup"] != "needs-occupancy-review" or fresh["head"] != row["head"] \
                or fresh.get("target_commit") != row.get("target_commit"):
            raise Error("Worktree or target changed during closeout; review again")
        git(repo["common_dir"], "worktree", "remove", path, timeout=300)
        if Path(path).exists() or Path(path).is_symlink() \
                or any(item["path"] == path for item in worktrees(repo["common_dir"])):
            raise Error("Git removal did not fully clear the path; preserve the task record")
        del data["worktrees"][path]
        save_json(index, data)
        return {**result, "cleanup": "closed", "blockers": [], "applied": True,
                "record_forgotten": True}


def parser():
    global WORKSPACE
    scope = argparse.ArgumentParser(add_help=False)
    scope.add_argument("--workspace", default=os.environ.get("JOYSTACK_WORKSPACE"))
    preliminary, _ = scope.parse_known_args()
    WORKSPACE = Path(preliminary.workspace).expanduser().resolve() if preliminary.workspace else None
    home = global_home()
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--workspace", default=preliminary.workspace,
                     help="Platform-approved path boundary; does not change the environment's home directory")
    cli.add_argument("--index", default=str(home / "state/worktrees.json"))
    sub = cli.add_subparsers(dest="command", required=True)
    sub.add_parser("init", help="Initialize the JoyStack global worktrees/state directories; preserves existing records")
    for name in ("list", "cleanup-plan", "scan"):
        command = sub.add_parser(name, help="Inventory worktrees; scan saves a JSON snapshot, never removes anything")
        command.add_argument("--repo", action="append", help="Restrict to these repositories (repeatable); default: known + managed root + current")
        command.add_argument("--json", action="store_true")
        command.add_argument("--review-days", type=int, default=7, help="Record-age review reminder, never a deletion deadline")
        if name == "scan":
            command.add_argument("--output", default=str(home / "state/worktree-inventory.json"),
                                 help="Local JSON snapshot path; task records remain in worktrees.json")
    command = sub.add_parser("close", help="Preview or safely remove one registered, adopted worktree; retain its branch")
    command.add_argument("--path", required=True)
    command.add_argument("--apply", action="store_true")
    command.add_argument("--sessions-clear", action="store_true",
                         help="Caller reviewed task sessions and non-cwd process use; required with --apply")
    for name in ("create", "register"):
        command = sub.add_parser(name)
        command.add_argument("--task", required=True)
        command.add_argument("--reason", required=True, help="Why this task uses a separate worktree")
        command.add_argument("--session", required=True, help="Caller-supplied task/session identity, not inferred")
        command.add_argument("--target", required=True, help="Explicit adoption target ref; local cached refs only")
        command.add_argument("--cleanup-when", required=True)
        command.add_argument("--base", help="Known base ref/commit; unknown for adopted worktrees when omitted")
        if name == "create":
            command.add_argument("--repo", required=True)
            command.add_argument("--branch", required=True)
            command.add_argument("--slug")
            command.add_argument("--root", default=str(home / "worktrees"))
            command.add_argument("--apply", action="store_true", help="Create and register; otherwise only print the plan")
        else:
            command.add_argument("--path", required=True)
    command = sub.add_parser("update", help="Change task metadata, not Git state")
    command.add_argument("--path", required=True)
    command.add_argument("--state", choices=STATES)
    for key in ("task", "reason", "session", "target", "cleanup-when", "keep-reason"):
        command.add_argument("--" + key)
    command = sub.add_parser("forget", help="Remove metadata only after native Git removal and path disappearance")
    command.add_argument("--path", required=True)
    return cli


def main():
    args = parser().parse_args()
    try:
        if WORKSPACE is not None:
            checked_path(Path.cwd(), "current working directory")
        index = checked_path(args.index, "task index")
        checked_path(global_home(), "JoyStack home")
        if args.command == "init":
            home = checked_path(global_home(), "JoyStack home")
            checked_path(home / "worktrees", "worktree root")
            home.mkdir(mode=0o700, parents=True, exist_ok=True)
            with locked_index(index) as data:
                (home / "worktrees").mkdir(mode=0o700, exist_ok=True)
                if not index.exists():
                    save_json(index, data)
            print(json.dumps({"home": str(home), "worktree_root": str(home / "worktrees"),
                              "index": str(index), "records": len(data["worktrees"])}))
            return 0
        for key in ("task", "reason", "session", "target", "cleanup_when"):
            value = getattr(args, key, None)
            if value is not None and not value.strip():
                raise Error(f"--{key.replace('_', '-')} must not be empty")
        if args.command in ("list", "cleanup-plan", "scan"):
            if args.review_days < 0:
                raise Error("--review-days must be non-negative")
            result = inventory(args, index)
            if args.command == "scan":
                output = checked_path(args.output, "inventory snapshot")
                output.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
                save_json(output, {"version": 1, **result})
                result["snapshot_path"] = str(output)
            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=True))
            else:
                print("TASK\tSTATE\tBRANCH\tPATH\tCLEANUP / BLOCKERS")
                for row in result["worktrees"]:
                    values = (row.get("task") or "(unknown)", row["state"], row.get("branch") or "(detached/bare)",
                              row["path"], ", ".join(row["cleanup_blockers"]) or row["cleanup"])
                    print("\t".join(json.dumps(v, ensure_ascii=False)[1:-1] for v in values))
                for error in result["repository_errors"]:
                    print(json.dumps(error), file=sys.stderr)
                for path in result["unresolved_managed_paths"]:
                    print("UNRESOLVED MANAGED PATH: " + path, file=sys.stderr)
                print("Scope: known, managed-root, current, or explicit repositories. Candidates still require session/process and authorization checks.")
            return 1 if result["repository_errors"] else 0
        if args.command == "close":
            result = closeout(args, index)
            print(json.dumps(result, indent=2, ensure_ascii=True))
            return 0
        result = create(args, index) if args.command == "create" else mutate(args, index)
        print(json.dumps(result, indent=2, ensure_ascii=True))
        return 0
    except (Error, OSError, subprocess.TimeoutExpired) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
