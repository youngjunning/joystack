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
        boundary = os.environ.get("JOYSTACK_WORKSPACE")
        temporary_root = Path.cwd() if boundary else None
        if boundary and not Path.cwd().resolve().is_relative_to(Path(boundary).expanduser().resolve()):
            raise RuntimeError("Run restricted-platform tests from inside JOYSTACK_WORKSPACE")
        self.temporary = tempfile.TemporaryDirectory(prefix="joy-git-test-", dir=temporary_root)
        self.root = Path(self.temporary.name).resolve()
        self.repo = self.root / "repo"
        self.index = self.root / "state" / "index.json"
        self.env = {**os.environ, "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
                    "GIT_TERMINAL_PROMPT": "0", "JOYSTACK_HOME": str(self.root / ".joystack"),
                    "GIT_CEILING_DIRECTORIES": str(self.root)}
        for name in worktrees.GIT_PATH_OVERRIDES:
            self.env.pop(name, None)
        self.original_workspace = worktrees.WORKSPACE
        worktrees.WORKSPACE = None
        self.init_repo(self.repo)

    def tearDown(self):
        worktrees.WORKSPACE = self.original_workspace
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
        return self.cli("register", "--path", path, "--task", "Fix search",
                        "--reason", "Keep search changes isolated", "--session", "test-session",
                        "--target", target, "--cleanup-when", "adopted and no occupancy")

    def rows(self, *extra):
        return self.cli("list", "--repo", self.repo, "--json", *extra)["worktrees"]

    def row(self, path):
        return next(row for row in self.rows() if row["path"] == str(path))

    def create_args(self, branch="task/search", **overrides):
        values = {"repo": str(self.repo), "root": str(self.root / "managed"), "branch": branch,
                  "task": "Fix search", "reason": "Keep search changes isolated",
                  "session": "test-session", "target": "main",
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

    def test_default_inventory_discovers_grouped_managed_worktrees(self):
        managed = self.root / ".joystack" / "worktrees"
        grouped = self.native(name="grouped", path=managed / ("repo-" + worktrees.repository(self.repo)["id"]) / "grouped-task")
        other = self.root / "other-repo"
        self.init_repo(other)
        other_path = managed / ("other-repo-" + worktrees.repository(other)["id"]) / "other-task"
        self.run_git(other, "worktree", "add", "-b", "other-task", str(other_path), "main")
        flat_repo = self.root / "flat-only-repo"
        self.init_repo(flat_repo)
        flat = managed / "legacy-flat"
        self.run_git(flat_repo, "worktree", "add", "-b", "flat-task", str(flat), "main")
        unresolved = managed / "orphaned"
        unresolved.mkdir(parents=True)
        report = self.cli("list", "--json")
        paths = {row["path"] for row in report["worktrees"]}
        self.assertIn(str(grouped), paths)
        self.assertIn(str(other_path), paths)
        self.assertNotIn(str(flat), paths)
        self.assertEqual(len(report["repositories"]), 2)
        self.assertEqual(self.row(grouped)["state"], "unknown")
        self.assertIn(str(unresolved), report["unresolved_managed_paths"])
        self.assertEqual(report["coverage"], "known-repositories-plus-managed-root-and-current-if-git")
        self.assertFalse(self.index.exists())

    def test_scan_saves_observed_json_without_claiming_unknown_task(self):
        managed = self.root / ".joystack" / "worktrees"
        path = self.native(name="scan-task", path=managed / ("repo-" + worktrees.repository(self.repo)["id"]) / "scan-task")
        report = self.cli("scan", "--json")
        snapshot = Path(report["snapshot_path"])
        saved = json.loads(snapshot.read_text())
        row = next(item for item in saved["worktrees"] if item["path"] == str(path))
        self.assertEqual(saved["version"], 1)
        self.assertEqual(row["state"], "unknown")
        self.assertIn("purpose-unknown", row["cleanup_blockers"])
        self.assertFalse(self.index.exists())
        self.assertEqual(snapshot.stat().st_mode & 0o777, 0o600)

    def test_create_plan_has_no_filesystem_or_git_side_effects(self):
        plan = self.cli(*self.create_args())
        self.assertFalse(plan["applied"])
        self.assertFalse(Path(plan["path"]).parent.exists())
        self.assertFalse(self.index.parent.exists())
        self.assertEqual(len(worktrees.worktrees(self.repo)), 1)
        self.assertIn("Fix-search", plan["path"])
        self.assertEqual(plan["reason"], "Keep search changes isolated")
        self.assertEqual(Path(plan["path"]).parent.name,
                         "repo-" + worktrees.repository(self.repo)["id"])

    def test_create_applies_and_registers_exact_base(self):
        plan = self.cli(*self.create_args(), "--apply")
        path = Path(plan["path"])
        self.assertTrue(plan["applied"])
        self.assertEqual(self.run_git(path, "rev-parse", "HEAD"), plan["base_commit"])
        self.assertEqual(plan["record"]["base_commit"], plan["base_commit"])
        self.assertEqual(plan["record"]["source"], "joy-git")
        self.assertEqual(plan["record"]["reason"], "Keep search changes isolated")
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
        self.assertEqual(record["reason"], "Keep search changes isolated")
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

    def test_adoption_can_record_reviewed_initial_state(self):
        path = self.native()
        stale = self.cli("register", "--path", path, "--task", "Verify release",
                         "--reason", "Keep validation isolated", "--session", "owlet-manual-test",
                         "--target", "main", "--cleanup-when", "After validation",
                         "--expected-head", "0" * 40, ok=False)
        self.assertIn("HEAD changed since", stale.stderr)
        self.assertFalse(self.index.exists())
        record = self.cli("register", "--path", path, "--task", "Verify release",
                          "--reason", "Keep validation isolated", "--session", "owlet-manual-test",
                          "--target", "main", "--cleanup-when", "After validation",
                          "--state", "verify", "--keep-reason", "Awaiting device review",
                          "--expected-head", self.run_git(path, "rev-parse", "HEAD"))
        self.assertEqual(record["state"], "verify")
        self.assertEqual(record["keep_reason"], "Awaiting device review")
        self.assertEqual(self.row(path)["reason"], "Keep validation isolated")

    def test_primary_and_subdirectory_cannot_be_registered(self):
        path = self.native()
        (path / "sub").mkdir()
        for wrong in (self.repo, path / "sub"):
            result = self.cli("register", "--path", wrong, "--task", "task",
                              "--reason", "Isolate task", "--session", "session",
                              "--target", "main", "--cleanup-when", "done", ok=False)
            self.assertIn("exact linked worktree", result.stderr)

    def test_empty_task_metadata_is_rejected(self):
        result = self.cli(*self.create_args(task="  "), "--apply", ok=False)
        self.assertIn("must not be empty", result.stderr)
        self.assertFalse(self.index.exists())

    def test_creation_reason_is_required_and_legacy_records_remain_readable(self):
        result = self.cli(*self.create_args(reason="  "), "--apply", ok=False)
        self.assertIn("--reason must not be empty", result.stderr)
        path = self.native()
        self.register(path)
        data = json.loads(self.index.read_text())
        del data["worktrees"][str(path)]["reason"]
        self.index.write_text(json.dumps(data))
        row = self.row(path)
        self.assertIsNone(row["reason"])
        self.assertEqual(row["task"], "Fix search")

    def test_done_is_only_an_occupancy_review_candidate(self):
        path = self.native()
        self.register(path)
        self.cli("update", "--path", path, "--state", "done")
        result = self.cli("cleanup-plan", "--repo", self.repo, "--json")
        row = next(row for row in result["worktrees"] if row["path"] == str(path))
        self.assertEqual(row["cleanup"], "needs-occupancy-review")
        self.assertFalse(result["deletion_authorized"])
        self.assertTrue(path.exists())

    def test_close_previews_then_removes_only_completed_adopted_worktree(self):
        path = self.native()
        self.register(path)
        self.cli("update", "--path", path, "--state", "done")
        preview = self.cli("close", "--path", path)
        self.assertEqual(preview["cleanup"], "needs-occupancy-review")
        self.assertEqual(preview["task"], "Fix search")
        self.assertEqual(preview["session"], "test-session")
        self.assertFalse(preview["applied"])
        self.assertEqual(preview["head"], self.run_git(path, "rev-parse", "HEAD"))
        self.assertEqual(preview["target_commit"], self.run_git(self.repo, "rev-parse", "main"))
        self.assertTrue(path.exists())
        stale = self.cli("close", "--path", path, "--apply", "--sessions-clear",
                         "--expected-head", "0" * 40, ok=False)
        self.assertIn("changed since the reviewed", stale.stderr)
        self.assertTrue(path.exists())
        wrong_owner = self.cli("close", "--path", path, "--apply", "--sessions-clear",
                               "--expected-task", "Another task", ok=False)
        self.assertIn("changed since the reviewed", wrong_owner.stderr)
        self.assertTrue(path.exists())
        denied = self.cli("close", "--path", path, "--apply", ok=False)
        self.assertIn("--sessions-clear", denied.stderr)
        with patch.object(worktrees, "occupied_cwd", return_value=False):
            result = self.cli("close", "--path", path, "--apply", "--sessions-clear",
                              "--expected-head", preview["head"],
                              "--expected-target-commit", preview["target_commit"],
                              "--expected-task", preview["task"], "--expected-session", preview["session"])
        self.assertTrue(result["applied"])
        self.assertTrue(result["branch_retained"])
        self.assertFalse(path.exists())
        self.assertNotIn(str(path), json.loads(self.index.read_text())["worktrees"])
        self.assertEqual(self.run_git(self.repo, "show-ref", "--verify", "refs/heads/feature") != "", True)

    def test_close_rejects_retention_dirty_and_occupied_worktrees(self):
        path = self.native()
        self.register(path)
        self.cli("update", "--path", path, "--state", "done", "--keep-reason", "pending review")
        denied = self.cli("close", "--path", path, "--apply", "--sessions-clear", ok=False)
        self.assertIn("explicit-retention", denied.stderr)
        self.cli("update", "--path", path, "--keep-reason", "")
        (path / "unsaved.txt").write_text("keep")
        denied = self.cli("close", "--path", path, "--apply", "--sessions-clear", ok=False)
        self.assertIn("uncommitted-or-untracked", denied.stderr)
        (path / "unsaved.txt").unlink()
        with patch.object(worktrees, "occupied_cwd", return_value=True):
            args = worktrees.parser().parse_args(["--index", str(self.index), "close", "--path", str(path),
                                                  "--apply", "--sessions-clear"])
            with self.assertRaisesRegex(worktrees.Error, "A process is using"):
                worktrees.closeout(args, self.index)
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
        nongit = self.root / "not-a-repository"
        nongit.mkdir()
        result = self.cli("list", "--json", cwd=nongit)
        self.assertEqual(len(result["repositories"]), 1)
        self.assertEqual(len(result["worktrees"]), 2)

    def test_git_creation_survives_index_save_failure(self):
        args = worktrees.parser().parse_args(self.create_args()[0:] + ["--apply"])
        with patch.dict(os.environ, self.env), patch.object(worktrees, "save_json", side_effect=OSError("disk full")):
            with self.assertRaisesRegex(worktrees.Error, "Worktree created.*registration failed"):
                worktrees.create(args, self.index)
        self.assertEqual(len(worktrees.worktrees(self.repo)), 2)
        self.assertFalse(self.index.exists())

    def test_register_cannot_take_over_a_completed_task(self):
        path = self.native()
        self.register(path)
        self.cli("update", "--path", path, "--state", "done")
        before = self.index.read_bytes()
        result = self.cli("register", "--path", path, "--task", "New task",
                          "--reason", "Isolate new task", "--session", "new-session",
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

    def restricted(self, *args, ok=True, env=None, cwd=None, index=None):
        environment = {**self.env, "JOYSTACK_WORKSPACE": str(self.root), **(env or {})}
        result = subprocess.run([sys.executable, str(SCRIPT), "--index", str(index or self.index), *map(str, args)],
                                cwd=cwd or self.repo, env=environment, capture_output=True, text=True)
        if ok:
            self.assertEqual(result.returncode, 0, result.stderr)
            return json.loads(result.stdout)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        return result

    def test_home_is_resolved_from_environment_not_workspace(self):
        environment = {**self.env, "HOME": str(self.root / "environment-home"),
                       "JOYSTACK_HOME": "", "JOYSTACK_WORKSPACE": str(self.root)}
        with patch.dict(os.environ, environment), patch.object(sys, "argv", [str(SCRIPT)]):
            args = worktrees.parser().parse_args(["init"])
            self.assertEqual(worktrees.global_home(), self.root / "environment-home/.joystack")
            self.assertEqual(Path(args.index), self.root / "environment-home/.joystack/state/worktrees.json")
            self.assertNotEqual(worktrees.global_home(), self.root / ".joystack")

    def test_restricted_workspace_does_not_silently_relocate_external_home(self):
        result = self.restricted("init", ok=False,
                                 env={"JOYSTACK_HOME": str(self.root.parent / "unapproved-home/.joystack")})
        self.assertIn("JoyStack home resolves outside", result.stderr)
        self.assertFalse(self.index.parent.exists())

    def test_restricted_init_and_create_stay_inside_approved_workspace(self):
        self.restricted("init")
        created = self.restricted(*self.create_args(), "--apply")
        path = Path(created["path"])
        self.assertTrue(path.is_relative_to(self.root))
        rows = self.restricted("list", "--repo", self.repo, "--json")
        self.assertEqual(rows["workspace"], str(self.root))
        self.assertEqual(len(rows["worktrees"]), 2)
        self.assertTrue(self.index.exists())

    def test_restricted_external_index_and_root_rejected_before_write(self):
        outside = self.root.parent / (self.root.name + "-outside")
        result = self.restricted("init", index=outside / "state/index.json", ok=False)
        self.assertIn("task index resolves outside", result.stderr)
        result = self.restricted(*self.create_args(root=str(outside)), "--apply", ok=False)
        self.assertIn("worktree root resolves outside", result.stderr)
        self.assertFalse(outside.exists())
        self.assertFalse(self.index.exists())
        self.assertEqual(len(worktrees.worktrees(self.repo)), 1)

    @unittest.skipIf(os.name == "nt", "POSIX symlinks; Windows is not exercised")
    def test_restricted_symlink_index_lock_root_and_marker_escape_rejected(self):
        # External targets stay in this disposable test fixture, outside the selected boundary.
        scope = self.root / "restricted-scope"
        scope.mkdir()
        env = {"JOYSTACK_WORKSPACE": str(scope), "JOYSTACK_HOME": str(scope / ".joystack")}
        repo = scope / "repo"
        self.init_repo(repo)
        outside = self.root / "outside"
        outside.mkdir()
        index = scope / "state/index.json"
        index.parent.mkdir()
        (outside / "index.json").write_text(json.dumps(worktrees.empty_index()))
        index.symlink_to(outside / "index.json")
        self.restricted("init", cwd=repo, env=env, index=index, ok=False)
        index.unlink()
        lock = Path(str(index) + ".lock")
        (outside / "lock").write_text("preserve")
        lock.symlink_to(outside / "lock")
        self.restricted("init", cwd=repo, env=env, index=index, ok=False)
        self.assertEqual((outside / "lock").read_text(), "preserve")
        lock.unlink()
        root = scope / "escaped-root"
        root.symlink_to(outside, target_is_directory=True)
        result = self.restricted(*self.create_args(repo=str(repo), root=str(root)), "--apply", cwd=repo, env=env, index=index, ok=False)
        self.assertIn("worktree root resolves outside", result.stderr)
        # Entire Git metadata as a symlink must also be rejected before native Git.
        (repo / ".git").rename(outside / "git")
        (repo / ".git").symlink_to(outside / "git", target_is_directory=True)
        before = (outside / "git/index").read_bytes()
        result = self.restricted("list", "--repo", repo, "--json", cwd=repo, env=env, index=index, ok=False)
        self.assertIn("Git marker resolves outside", result.stdout)
        self.assertEqual((outside / "git/index").read_bytes(), before)

    def test_restricted_linked_worktree_with_external_common_dir_rejected(self):
        scope = self.root / "restricted-scope"
        scope.mkdir()
        path = self.native(path=scope / "linked")
        before = (self.repo / ".git/index").read_bytes()
        result = self.restricted("register", "--path", path, "--task", "task",
                                 "--reason", "Isolate task", "--session", "session",
                                 "--target", "main", "--cleanup-when", "done", cwd=path,
                                 env={"JOYSTACK_WORKSPACE": str(scope), "JOYSTACK_HOME": str(scope / ".joystack")},
                                 index=scope / "state/index.json", ok=False)
        self.assertIn("Git directory resolves outside", result.stderr)
        self.assertFalse((scope / "state/index.json").exists())
        self.assertEqual((self.repo / ".git/index").read_bytes(), before)

    def test_restricted_explicit_external_repository_is_an_error(self):
        scope = self.root / "restricted-scope"
        scope.mkdir()
        result = self.restricted("list", "--repo", self.repo, "--json", cwd=scope,
                                 env={"JOYSTACK_WORKSPACE": str(scope), "JOYSTACK_HOME": str(scope / ".joystack")},
                                 index=scope / "state/index.json", ok=False)
        self.assertEqual(result.returncode, 1)
        self.assertTrue(json.loads(result.stdout)["repository_errors"])
        self.assertFalse((scope / "state").exists())

    def test_restricted_git_environment_redirects_rejected(self):
        for name in worktrees.GIT_PATH_OVERRIDES:
            with self.subTest(variable=name):
                result = self.restricted("list", "--repo", self.repo, "--json",
                                         env={name: str(self.root / "other-git-path")}, ok=False)
                self.assertIn("inherited " + name, result.stdout)
                self.assertEqual(result.returncode, 1)

    def test_restricted_external_current_directory_rejected(self):
        scope = self.root / "restricted-scope"
        scope.mkdir()
        result = self.restricted("init", cwd=self.repo,
                                 env={"JOYSTACK_WORKSPACE": str(scope), "JOYSTACK_HOME": str(scope / ".joystack")},
                                 index=scope / "state/index.json", ok=False)
        self.assertIn("current working directory resolves outside", result.stderr)
        self.assertFalse((scope / ".joystack").exists())

    def test_restricted_internal_gitdir_with_external_commondir_rejected(self):
        scope = self.root / "restricted-scope"
        scope.mkdir()
        path = self.native(path=scope / "linked")
        source_gitdir = Path(self.run_git(path, "rev-parse", "--absolute-git-dir"))
        inside_gitdir = scope / "gitdir"
        source_gitdir.rename(inside_gitdir)
        # The gitfile is in scope, but commondir points to the source repo outside it.
        (path / ".git").write_text("gitdir: " + str(inside_gitdir) + "\n")
        (inside_gitdir / "commondir").write_text(str(self.repo / ".git") + "\n")
        result = self.restricted("list", "--repo", path, "--json", cwd=path,
                                 env={"JOYSTACK_WORKSPACE": str(scope), "JOYSTACK_HOME": str(scope / ".joystack")},
                                 index=scope / "state/index.json", ok=False)
        self.assertIn("Git common-dir resolves outside", result.stdout)
        self.assertFalse((scope / "state").exists())

    def test_restricted_external_recorded_paths_are_not_followed(self):
        scope = self.root / "restricted-scope"
        scope.mkdir()
        path = self.native()
        self.register(path)
        index = scope / "index.json"
        index.write_bytes(self.index.read_bytes())
        before = index.read_bytes()
        result = self.restricted("list", "--json", cwd=scope,
                                 env={"JOYSTACK_WORKSPACE": str(scope), "JOYSTACK_HOME": str(scope / ".joystack")},
                                 index=index, ok=False)
        self.assertIn("recorded Git common-dir resolves outside", result.stderr)
        self.assertEqual(index.read_bytes(), before)

    @unittest.skipIf(os.name == "nt", "POSIX symlinks; Windows is not exercised")
    def test_restricted_branch_ref_and_reflog_symlinks_rejected_before_creation(self):
        scope = self.root / "restricted-scope"
        scope.mkdir()
        outside = self.root / "outside"
        outside.mkdir()
        env = {"JOYSTACK_WORKSPACE": str(scope), "JOYSTACK_HOME": str(scope / ".joystack")}
        for number, relative in enumerate(("refs/heads", "logs/refs/heads", "refs/heads/task", "logs/refs/heads/task")):
            with self.subTest(metadata=relative):
                repo = scope / ("repo-" + str(number))
                self.init_repo(repo)
                marker = repo / ".git" / relative
                external = outside / ("metadata-" + str(number))
                if marker.exists():
                    marker.rename(external)
                else:
                    external.mkdir()
                    marker.parent.mkdir(parents=True, exist_ok=True)
                marker.symlink_to(external, target_is_directory=True)
                before = sorted(p.name for p in external.iterdir())
                result = self.restricted(*self.create_args(repo=str(repo), root=str(scope / "managed"), branch="task/new"),
                                         "--apply", cwd=repo, env=env, index=scope / "state/index.json", ok=False)
                self.assertIn("Workspace boundary", result.stderr)
                self.assertEqual(sorted(p.name for p in external.iterdir()), before)
                self.assertFalse((scope / "state/index.json").exists())

    def test_fixture_clears_inherited_git_path_redirects(self):
        (self.repo / "file.txt").write_text("preserve pending data\n")
        before_head = self.run_git(self.repo, "rev-parse", "HEAD")
        before_index = (self.repo / ".git/index").read_bytes()
        before_config = (self.repo / ".git/config").read_bytes()
        cwd = Path.cwd()
        nested = WorktreeTests("runTest")
        initialized = False
        try:
            os.chdir(self.root)
            inherited = {name: str(self.repo / ".git") for name in worktrees.GIT_PATH_OVERRIDES}
            inherited["GIT_WORK_TREE"] = str(self.repo)
            inherited["JOYSTACK_WORKSPACE"] = str(self.root)
            with patch.dict(os.environ, inherited):
                nested.setUp()
                initialized = True
                self.assertTrue(nested.root.is_relative_to(self.root))
                self.assertFalse(any(name in nested.env for name in worktrees.GIT_PATH_OVERRIDES))
        finally:
            if initialized:
                nested.tearDown()
            os.chdir(cwd)
        self.assertEqual(self.run_git(self.repo, "rev-parse", "HEAD"), before_head)
        self.assertEqual((self.repo / ".git/index").read_bytes(), before_index)
        self.assertEqual((self.repo / ".git/config").read_bytes(), before_config)
        self.assertEqual((self.repo / "file.txt").read_text(), "preserve pending data\n")

    def checkout_shorthand(self):
        self.run_git(self.repo, "checkout", "-b", "task/previous")
        self.run_git(self.repo, "checkout", "main")
        self.run_git(self.repo, "branch", "-d", "task/previous")
        self.assertEqual(self.run_git(self.repo, "check-ref-format", "--branch", "@{-1}"), "task/previous")

    def test_checkout_shorthand_uses_normalized_branch_for_plan_and_creation(self):
        self.checkout_shorthand()
        plan = self.cli(*self.create_args(branch="@{-1}"))
        self.assertEqual(plan["branch"], "task/previous")
        created = self.cli(*self.create_args(branch="@{-1}"), "--apply")
        self.assertEqual(created["branch"], "task/previous")
        self.assertEqual(created["record"]["branch"], "task/previous")

    @unittest.skipIf(os.name == "nt", "POSIX symlinks; Windows is not exercised")
    def test_restricted_checkout_shorthand_checks_normalized_ref_path(self):
        scope = self.root / "restricted-scope"
        scope.mkdir()
        repo = scope / "repo"
        self.init_repo(repo)
        self.run_git(repo, "checkout", "-b", "task/previous")
        self.run_git(repo, "checkout", "main")
        self.run_git(repo, "branch", "-d", "task/previous")
        outside = self.root / "external-refs"
        outside.mkdir()
        task_refs = repo / ".git/refs/heads/task"
        task_refs.symlink_to(outside, target_is_directory=True)
        result = self.restricted(*self.create_args(repo=str(repo), root=str(scope / "managed"), branch="@{-1}"),
                                 "--apply", cwd=repo,
                                 env={"JOYSTACK_WORKSPACE": str(scope), "JOYSTACK_HOME": str(scope / ".joystack")},
                                 index=scope / "state/index.json", ok=False)
        self.assertIn("new branch metadata resolves outside", result.stderr)
        self.assertFalse(list(outside.iterdir()))
        self.assertFalse((scope / "state/index.json").exists())


if __name__ == "__main__":
    unittest.main()
