"""Integration tests use disposable native Git repositories, never user worktrees."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import worktrees


SCRIPT = Path(__file__).with_name("worktrees.py")


class WorktreeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="joy-git-test-")
        self.root = Path(self.temporary.name).resolve()
        self.repo = self.root / "repo"
        self.index = self.root / "state" / "index.json"
        self.env = {**os.environ, "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
                    "GIT_TERMINAL_PROMPT": "0", "JOYSTACK_HOME": str(self.root / ".joystack")}
        self.init_repo(self.repo)

    def tearDown(self):
        self.temporary.cleanup()

    def init_repo(self, path):
        path.mkdir(parents=True)
        self.run_git(path, "init", "-b", "main")
        self.run_git(path, "config", "user.name", "Test User")
        self.run_git(path, "config", "user.email", "test@example.com")
        self.run_git(path, "config", "commit.gpgsign", "false")
        (path / "file.txt").write_text("base\n")
        (path / ".gitignore").write_text("cache/\n")
        self.run_git(path, "add", "file.txt", ".gitignore")
        self.run_git(path, "commit", "-m", "initial")

    def run_git(self, path, *args):
        return subprocess.run(["git", "-C", str(path), *args], env=self.env,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout.decode().strip()

    def cli(self, *args, ok=True, cwd=None):
        result = subprocess.run([sys.executable, str(SCRIPT), "--index", str(self.index), *map(str, args)],
                                cwd=cwd or self.repo, env=self.env, capture_output=True, text=True)
        if ok:
            self.assertEqual(result.returncode, 0, result.stderr)
            return json.loads(result.stdout)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        return result

    def native(self, name="feature", path=None, detached=False):
        path = path or self.root / name
        args = ("--detach",) if detached else ("-b", name)
        self.run_git(self.repo, "worktree", "add", *args, str(path), "main")
        return path

    def register(self, path, target="main"):
        return self.cli("register", "--path", path, "--task", "Fix search", "--session", "test-session",
                        "--target", target, "--cleanup-when", "adopted and no occupancy")

    def rows(self, *extra):
        return self.cli("list", "--repo", self.repo, "--json", *extra)["worktrees"]

    def row(self, path):
        return next(row for row in self.rows() if row["path"] == str(path))

    def create_args(self, branch="task/search", **overrides):
        values = {"repo": str(self.repo), "root": str(self.root / "managed"), "branch": branch,
                  "task": "Fix search", "session": "test-session", "target": "main",
                  "cleanup-when": "adopted and no occupancy", **overrides}
        return ["create", *[item for key, value in values.items() for item in ("--" + key, value)]]

    def test_list_is_read_only_and_unknown_is_not_idle(self):
        path = self.native()
        before = (self.repo / ".git/index").read_bytes()
        row = self.row(path)
        self.assertEqual(row["state"], "unknown")
        self.assertIn("purpose-unknown", row["cleanup_blockers"])
        self.assertFalse(self.index.parent.exists())
        self.assertEqual(before, (self.repo / ".git/index").read_bytes())

    def test_create_plan_has_no_filesystem_or_git_side_effects(self):
        plan = self.cli(*self.create_args())
        self.assertFalse(plan["applied"])
        self.assertFalse(Path(plan["path"]).parent.exists())
        self.assertFalse(self.index.parent.exists())
        self.assertEqual(len(worktrees.worktrees(self.repo)), 1)
        self.assertIn("Fix-search", plan["path"])

    def test_create_applies_and_registers_exact_base(self):
        plan = self.cli(*self.create_args(), "--apply")
        path = Path(plan["path"])
        self.assertTrue(plan["applied"])
        self.assertEqual(self.run_git(path, "rev-parse", "HEAD"), plan["base_commit"])
        self.assertEqual(plan["record"]["base_commit"], plan["base_commit"])
        self.assertEqual(plan["record"]["source"], "joy-git")
        self.assertIsNotNone(plan["record"]["created_at"])
        self.assertEqual(self.row(path)["task"], "Fix search")
        if os.name != "nt":
            self.assertEqual(self.index.stat().st_mode & 0o777, 0o600)

    def test_adoption_preserves_path_and_unknown_creation_time(self):
        path = self.native(path=self.root / "host-owned" / "odd-directory")
        before = self.run_git(path, "rev-parse", "HEAD")
        record = self.register(path)
        self.assertIsNone(record["created_at"])
        self.assertIsNone(record["base_commit"])
        self.assertEqual(record["source"], "adopted")
        self.assertEqual(before, self.run_git(path, "rev-parse", "HEAD"))
        self.assertTrue(path.exists())

    def test_repeat_register_preserves_retention_and_state(self):
        path = self.native()
        old = self.register(path)
        self.cli("update", "--path", path, "--state", "verify", "--keep-reason", "device validation")
        new = self.register(path)
        self.assertEqual(new["id"], old["id"])
        self.assertEqual(new["state"], "verify")
        self.assertEqual(new["keep_reason"], "device validation")

    def test_primary_and_subdirectory_cannot_be_registered(self):
        path = self.native()
        (path / "sub").mkdir()
        for wrong in (self.repo, path / "sub"):
            result = self.cli("register", "--path", wrong, "--task", "task", "--session", "session",
                              "--target", "main", "--cleanup-when", "done", ok=False)
            self.assertIn("exact linked worktree", result.stderr)

    def test_empty_task_metadata_is_rejected(self):
        result = self.cli(*self.create_args(task="  "), "--apply", ok=False)
        self.assertIn("must not be empty", result.stderr)
        self.assertFalse(self.index.exists())

    def test_done_is_only_an_occupancy_review_candidate(self):
        path = self.native()
        self.register(path)
        self.cli("update", "--path", path, "--state", "done")
        result = self.cli("cleanup-plan", "--repo", self.repo, "--json")
        row = next(row for row in result["worktrees"] if row["path"] == str(path))
        self.assertEqual(row["cleanup"], "needs-occupancy-review")
        self.assertFalse(result["deletion_authorized"])
        self.assertTrue(path.exists())

    def test_clean_active_task_is_not_a_candidate(self):
        path = self.native()
        self.register(path)
        self.assertIn("task-not-done", self.row(path)["cleanup_blockers"])

    def test_pushed_task_branch_is_not_adoption_into_target(self):
        path = self.native()
        self.register(path)
        (path / "file.txt").write_text("feature\n")
        self.run_git(path, "commit", "-am", "feature")
        self.run_git(self.repo, "update-ref", "refs/remotes/origin/feature", self.run_git(path, "rev-parse", "HEAD"))
        self.cli("update", "--path", path, "--state", "done")
        self.assertIn("head-not-in-target-history", self.row(path)["cleanup_blockers"])
        self.run_git(self.repo, "merge", "--ff-only", "feature")
        self.assertEqual(self.row(path)["cleanup"], "needs-occupancy-review")

    def test_uncommitted_untracked_and_ignored_files_block_candidates(self):
        path = self.native()
        self.register(path)
        self.cli("update", "--path", path, "--state", "done")
        (path / "file.txt").write_text("unsaved\n")
        (path / "untracked.txt").write_text("unsaved\n")
        (path / "cache").mkdir()
        (path / "cache/local-state").write_text("valuable\n")
        row = self.row(path)
        self.assertTrue(row["dirty"])
        self.assertTrue(row["ignored_files"])
        self.assertIn("uncommitted-or-untracked", row["cleanup_blockers"])
        self.assertIn("ignored-files-need-review", row["cleanup_blockers"])

    def test_locked_worktree_is_retained(self):
        path = self.native()
        self.register(path)
        self.run_git(self.repo, "worktree", "lock", "--reason", "external drive", str(path))
        self.cli("update", "--path", path, "--state", "done")
        self.assertIn("git-locked", self.row(path)["cleanup_blockers"])

    def test_in_progress_operation_is_retained(self):
        path = self.native()
        self.register(path)
        self.cli("update", "--path", path, "--state", "done")
        gitdir = Path(self.run_git(path, "rev-parse", "--absolute-git-dir"))
        (gitdir / "CHERRY_PICK_HEAD").write_text(self.run_git(path, "rev-parse", "HEAD") + "\n")
        row = self.row(path)
        self.assertIn("git-operation-in-progress", row["cleanup_blockers"])
        self.assertIn("CHERRY_PICK_HEAD", row["operations"])

    def test_old_record_only_requests_review(self):
        path = self.native()
        self.register(path)
        data = json.loads(self.index.read_text())
        data["worktrees"][str(path)]["updated_at"] = (datetime.now(timezone.utc) - timedelta(days=90)).isoformat()
        self.index.write_text(json.dumps(data))
        row = self.row(path)
        self.assertTrue(row["review_due"])
        self.assertEqual(row["cleanup"], "blocked")
        self.assertTrue(path.exists())

    def test_explicit_retention_blocks_done(self):
        path = self.native()
        self.register(path)
        self.cli("update", "--path", path, "--state", "done", "--keep-reason", "keep validation environment")
        self.assertIn("explicit-retention", self.row(path)["cleanup_blockers"])
        self.cli("update", "--path", path, "--keep-reason", "")
        self.assertEqual(self.row(path)["cleanup"], "needs-occupancy-review")

    def test_detached_head_and_newline_paths_remain_exact(self):
        path = self.native(path=self.root / "space\n目录", detached=True)
        record = self.register(path)
        self.assertIsNone(record["branch"])
        row = self.row(path)
        self.assertEqual(row["path"], str(path))
        self.assertTrue(row["detached"])

    def test_branch_change_does_not_inherit_cleanup_permission(self):
        path = self.native()
        self.register(path)
        self.cli("update", "--path", path, "--state", "done")
        self.run_git(path, "checkout", "-b", "another-task")
        self.assertIn("branch-changed", self.row(path)["cleanup_blockers"])
        self.cli("update", "--path", path, "--state", "done", ok=False)
        record = self.register(path)
        self.assertEqual(record["state"], "active")

    def test_missing_target_blocks_cleanup(self):
        path = self.native()
        self.run_git(self.repo, "branch", "adoption-target")
        self.register(path, "adoption-target")
        self.cli("update", "--path", path, "--state", "done")
        self.run_git(self.repo, "branch", "-d", "adoption-target")
        self.assertIn("inspection-failed", self.row(path)["cleanup_blockers"])

    def test_squash_is_conservatively_blocked(self):
        path = self.native()
        self.register(path)
        (path / "file.txt").write_text("feature\n")
        self.run_git(path, "commit", "-am", "feature")
        self.run_git(self.repo, "merge", "--squash", "feature")
        self.run_git(self.repo, "commit", "-m", "squashed feature")
        self.cli("update", "--path", path, "--state", "done")
        self.assertIn("head-not-in-target-history", self.row(path)["cleanup_blockers"])

    def test_forget_requires_both_native_removal_and_path_disappearance(self):
        path = self.native()
        self.register(path)
        self.cli("forget", "--path", path, ok=False)
        self.run_git(self.repo, "worktree", "remove", str(path))
        row = self.row(path)
        self.assertIn("not-registered-in-git", row["cleanup_blockers"])
        result = self.cli("forget", "--path", path)
        self.assertFalse(result["worktree_deleted"])
        self.assertFalse(json.loads(self.index.read_text())["worktrees"])

    def test_missing_but_git_registered_path_is_not_forgotten(self):
        path = self.native()
        self.register(path)
        moved = self.root / "manually-moved"
        path.rename(moved)
        self.assertIn("missing-or-prunable", self.row(path)["cleanup_blockers"])
        self.cli("forget", "--path", path, ok=False)
        self.assertTrue(moved.exists())

    def test_corrupt_index_is_not_replaced(self):
        self.index.parent.mkdir()
        self.index.write_text("corrupt original")
        result = self.cli("list", "--repo", self.repo, "--json", ok=False)
        self.assertIn("preserve it", result.stderr)
        self.assertEqual(self.index.read_text(), "corrupt original")
        self.cli(*self.create_args(), "--apply", ok=False)
        self.assertFalse((self.root / "managed").exists())

    def test_same_named_repositories_have_distinct_destination_roots(self):
        other = self.root / "another" / "repo"
        self.init_repo(other)
        first = self.cli(*self.create_args())
        second = self.cli(*self.create_args(repo=str(other)))
        self.assertNotEqual(Path(first["path"]).parent, Path(second["path"]).parent)

    def test_project_local_root_requires_ignore_rule(self):
        result = self.cli(*self.create_args(root=str(self.repo / "worktrees")), ok=False)
        self.assertIn("must already be ignored", result.stderr)
        (self.repo / ".gitignore").write_text("cache/\nworktrees/\n")
        plan = self.cli(*self.create_args(root=str(self.repo / "worktrees")))
        self.assertFalse(plan["applied"])
        self.assertFalse((self.repo / "worktrees").exists())

    def test_git_metadata_is_not_a_destination(self):
        result = self.cli(*self.create_args(root=str(self.repo / ".git")), ok=False)
        self.assertIn("metadata directory", result.stderr)

    def test_concurrent_registrations_preserve_both_tasks(self):
        paths = [self.native("one"), self.native("two")]
        with ThreadPoolExecutor(max_workers=2) as pool:
            list(pool.map(self.register, paths))
        data = json.loads(self.index.read_text())
        self.assertEqual(set(data["worktrees"]), {str(p) for p in paths})

    def test_known_repository_inventory_works_outside_git(self):
        path = self.native()
        self.register(path)
        result = self.cli("list", "--json", cwd=self.root)
        self.assertEqual(len(result["repositories"]), 1)
        self.assertEqual(len(result["worktrees"]), 2)

    def test_git_creation_survives_index_save_failure(self):
        args = worktrees.parser().parse_args(self.create_args()[0:] + ["--apply"])
        with patch.dict(os.environ, self.env), patch.object(worktrees, "save_index", side_effect=OSError("disk full")):
            with self.assertRaisesRegex(worktrees.Error, "Worktree created.*registration failed"):
                worktrees.create(args, self.index)
        self.assertEqual(len(worktrees.worktrees(self.repo)), 2)
        self.assertFalse(self.index.exists())

    def test_register_cannot_take_over_a_completed_task(self):
        path = self.native()
        self.register(path)
        self.cli("update", "--path", path, "--state", "done")
        before = self.index.read_bytes()
        result = self.cli("register", "--path", path, "--task", "New task", "--session", "new-session",
                          "--target", "main", "--cleanup-when", "done", ok=False)
        self.assertIn("ownership changed", result.stderr)
        self.assertEqual(self.index.read_bytes(), before)

    def test_update_handoff_requires_explicit_state(self):
        path = self.native()
        self.register(path)
        self.cli("update", "--path", path, "--state", "done")
        self.cli("update", "--path", path, "--task", "New task", "--session", "new-session", ok=False)
        record = self.cli("update", "--path", path, "--task", "New task", "--session", "new-session", "--state", "active")
        self.assertEqual(record["state"], "active")
        self.assertIn("task-not-done", self.row(path)["cleanup_blockers"])

    @unittest.skipIf(os.name == "nt", "Executable POSIX Git hook; Windows is not exercised")
    def test_failing_checkout_hook_reports_existing_worktree_without_claiming(self):
        hook = self.repo / ".git/hooks/post-checkout"
        hook.write_text("#!/bin/sh\nprintf hook-ran > hook-marker\nexit 1\n")
        hook.chmod(0o755)
        plan = self.cli(*self.create_args())
        result = self.cli(*self.create_args(), "--apply", ok=False)
        path = Path(plan["path"])
        self.assertIn("Matching worktree present", result.stderr)
        self.assertIn("ownership is unconfirmed; not registered", result.stderr)
        self.assertTrue(path.exists())
        self.assertTrue((path / "hook-marker").exists())
        self.assertFalse(self.index.exists())
        self.assertEqual(len(worktrees.worktrees(self.repo)), 2)

    def test_invalid_current_repository_is_reported_not_empty_success(self):
        path = self.native()
        self.register(path)
        (self.repo / ".git/config").write_text("invalid config line\n")
        result = self.cli("list", "--json", ok=False)
        self.assertEqual(result.returncode, 1)
        data = json.loads(result.stdout)
        self.assertTrue(data["repository_errors"])
        self.assertTrue(any("config" in e["error"] for e in data["repository_errors"]))
        self.assertTrue(path.exists())

    def test_invalid_explicit_repo_keeps_other_repository_results(self):
        path = self.native()
        result = self.cli("list", "--repo", self.repo, "--repo", self.root / "missing", "--json", ok=False)
        self.assertEqual(result.returncode, 1)
        data = json.loads(result.stdout)
        self.assertEqual(len(data["worktrees"]), 2)
        self.assertEqual(len(data["repository_errors"]), 1)
        self.assertTrue(path.exists())

    def test_global_defaults_share_joystack_home(self):
        with patch.dict(os.environ, {"JOYSTACK_HOME": str(self.root / ".joystack"), "XDG_STATE_HOME": str(self.root / "unused")}):
            args = worktrees.parser().parse_args(self.create_args())
        self.assertEqual(Path(args.index), self.root / ".joystack/state/worktrees.json")
        values = self.create_args()
        root_flag = values.index("--root")
        del values[root_flag:root_flag + 2]
        with patch.dict(os.environ, {"JOYSTACK_HOME": str(self.root / ".joystack")}):
            args = worktrees.parser().parse_args(values)
        self.assertEqual(Path(args.root), self.root / ".joystack/worktrees")
        self.assertFalse((self.root / ".joystack").exists())

    def test_init_is_idempotent_and_preserves_existing_records(self):
        path = self.native()
        self.register(path)
        before = self.index.read_bytes()
        first = self.cli("init")
        second = self.cli("init")
        self.assertEqual(first["records"], 1)
        self.assertEqual(second["records"], 1)
        self.assertEqual(self.index.read_bytes(), before)
        self.assertTrue((self.root / ".joystack/worktrees").is_dir())

    def test_init_and_creation_use_global_defaults_without_overrides(self):
        args = self.create_args()
        root_flag = args.index("--root")
        del args[root_flag:root_flag + 2]
        def run(*commands):
            result = subprocess.run([sys.executable, str(SCRIPT), *commands], cwd=self.repo,
                                    env=self.env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            return json.loads(result.stdout)
        home = self.root / ".joystack"
        planned = run(*args)
        self.assertFalse(home.exists())
        initialized = run("init")
        self.assertEqual(initialized["index"], str(home / "state/worktrees.json"))
        created = run(*args, "--apply")
        self.assertTrue(Path(created["path"]).is_relative_to(home / "worktrees"))
        self.assertEqual(len(json.loads((home / "state/worktrees.json").read_text())["worktrees"]), 1)
        self.assertFalse(self.index.exists())

    def test_failed_add_does_not_claim_an_external_worktree_at_destination(self):
        other = self.root / "other-repo"
        self.init_repo(other)
        (other / "file.txt").write_text("different repository\n")
        self.run_git(other, "commit", "-am", "different base")
        self.run_git(self.repo, "checkout", "-b", "alternate-base")
        (self.repo / "file.txt").write_text("different head\n")
        self.run_git(self.repo, "commit", "-am", "alternate base")
        self.run_git(self.repo, "checkout", "main")
        original_git = worktrees.git
        for case in ("repository", "branch", "head"):
            with self.subTest(identity=case):
                args = worktrees.parser().parse_args(self.create_args(branch="task/" + case, slug=case) + ["--apply"])
                destination = []
                def interleaved(repo, *commands, **kwargs):
                    if commands[:2] == ("worktree", "add"):
                        path = commands[-2]
                        external_repo = other if case == "repository" else self.repo
                        branch = args.branch if case == "head" else "external/" + case
                        base = "alternate-base" if case == "head" else "main"
                        self.run_git(external_repo, "worktree", "add", "-b", branch, path, base)
                        destination.append(Path(path))
                    return original_git(repo, *commands, **kwargs)
                with patch.dict(os.environ, self.env), patch.object(worktrees, "git", side_effect=interleaved):
                    with self.assertRaisesRegex(worktrees.Error, "Path conflict or creation unconfirmed.*no task registered"):
                        worktrees.create(args, self.index)
                self.assertFalse(self.index.exists())
                self.assertEqual(len(destination), 1)
                self.assertTrue(destination[0].exists())
                self.assertTrue(self.run_git(destination[0], "branch", "--show-current").startswith(("external/", "task/head")))

    def test_failed_add_with_all_coordinates_matching_still_does_not_claim_ownership(self):
        args = worktrees.parser().parse_args(self.create_args() + ["--apply"])
        original_git = worktrees.git
        destination = []
        def interleaved(repo, *commands, **kwargs):
            if commands[:2] == ("worktree", "add"):
                path, base = commands[-2:]
                self.run_git(self.repo, "worktree", "add", "-b", args.branch, path, base)
                destination.append(Path(path))
            return original_git(repo, *commands, **kwargs)
        with patch.dict(os.environ, self.env), patch.object(worktrees, "git", side_effect=interleaved):
            with self.assertRaisesRegex(worktrees.Error, "Matching worktree present.*ownership is unconfirmed; not registered"):
                worktrees.create(args, self.index)
        self.assertFalse(self.index.exists())
        self.assertTrue(destination[0].exists())
        self.assertEqual(self.run_git(destination[0], "branch", "--show-current"), args.branch)


if __name__ == "__main__":
    unittest.main()
