"""Verify resource portability using separate, non-adjacent Skill mounts."""
import os
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import validate as validator
from validate import ROOT, validate_skill_bundle


class IndependentMountTests(unittest.TestCase):
    def setUp(self):
        workspace = os.environ.get('JOYSTACK_WORKSPACE')
        if workspace and not Path.cwd().resolve().is_relative_to(Path(workspace).expanduser().resolve()):
            raise RuntimeError('Run restricted-platform tests inside JOYSTACK_WORKSPACE')
        self.temporary = tempfile.TemporaryDirectory(prefix='joystack-mount-test-', dir=Path.cwd() if workspace else None)
        self.root = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def fixture(self):
        skill = self.root / 'standalone' / 'skill'
        skill.mkdir(parents=True)
        return skill

    def test_every_skill_retains_local_resources_without_sibling_mounts(self):
        originals = sorted((ROOT / 'skills/engineering').glob('*/SKILL.md'))
        self.assertTrue(originals)
        for number, original in enumerate(originals):
            with self.subTest(skill=original.parent.name):
                mounted = self.root / f'host-slot-{number}' / 'independent-mount' / 'active-skill'
                shutil.copytree(original.parent, mounted, ignore=shutil.ignore_patterns('__pycache__'))
                self.assertFalse((mounted.parent / 'joy-stack').exists())
                self.assertFalse((mounted.parent / 'joy-git').exists())
                self.assertEqual(validate_skill_bundle(mounted), [])

    def test_existing_sibling_resource_still_violates_mount_boundary(self):
        skill = self.fixture()
        sibling = skill.parent / 'other-skill'
        sibling.mkdir()
        (sibling / 'SKILL.md').write_text('# Another skill\n')
        (skill / 'SKILL.md').write_text('[invoke](../other-skill/SKILL.md)\n')
        self.assertTrue(any('cross-Skill' in e for e in validate_skill_bundle(skill)))

    def test_internal_reference_to_script_is_portable(self):
        skill = self.fixture()
        (skill / 'references').mkdir()
        (skill / 'scripts').mkdir()
        (skill / 'scripts/tool.py').write_text('print("local")\n')
        (skill / 'SKILL.md').write_text('[guide](references/guide.md)\n')
        (skill / 'references/guide.md').write_text('[tool](../scripts/tool.py)\n')
        self.assertEqual(validate_skill_bundle(skill), [])

    def test_missing_file_in_deep_reference_is_reported(self):
        skill = self.fixture()
        (skill / 'references').mkdir()
        (skill / 'SKILL.md').write_text('[guide](references/guide.md)\n')
        (skill / 'references/guide.md').write_text('[missing](../scripts/missing.py)\n')
        self.assertTrue(any('missing bundled resource' in e for e in validate_skill_bundle(skill)))

    def test_encoded_parent_escape_is_rejected(self):
        skill = self.fixture()
        (skill / 'SKILL.md').write_text('[escape](%2E%2E/outside.md)\n')
        self.assertTrue(any('cross-Skill' in e for e in validate_skill_bundle(skill)))

    @unittest.skipIf(os.name == 'nt', 'POSIX symlink test')
    def test_symlinked_resource_outside_mount_is_rejected(self):
        skill = self.fixture()
        outside = self.root / 'outside.md'
        outside.write_text('# Outside mount\n')
        (skill / 'guide.md').symlink_to(outside)
        (skill / 'SKILL.md').write_text('[guide](guide.md)\n')
        self.assertTrue(any('cross-Skill' in e for e in validate_skill_bundle(skill)))

    @unittest.skipIf(os.name == 'nt', 'POSIX symlink test')
    def test_external_document_is_not_read_during_validation(self):
        skill = self.fixture()
        outside = self.root / 'external-document.md'
        outside.write_bytes(b'\xff\xfe')  # UTF-8 read would fail if followed.
        (skill / 'external.md').symlink_to(outside)
        (skill / 'SKILL.md').write_text('# Standalone skill\n')
        self.assertTrue(any('outside bundled document' in e for e in validate_skill_bundle(skill)))

    def test_source_urls_and_local_anchors_are_not_runtime_dependencies(self):
        skill = self.fixture()
        (skill / 'SKILL.md').write_text('[source](https://example.com/source) [heading](#heading)\n')
        self.assertEqual(validate_skill_bundle(skill), [])

    def test_reference_style_sibling_resource_is_rejected(self):
        skill = self.fixture()
        (skill / 'SKILL.md').write_text('[invoke][other]\n\n[other]: ../other-skill/SKILL.md\n')
        self.assertTrue(any('cross-Skill' in e for e in validate_skill_bundle(skill)))

    def test_reference_style_missing_resource_is_reported(self):
        skill = self.fixture()
        (skill / 'SKILL.md').write_text('[guide][missing]\n\n[missing]: <references/not-there.md> "Guide"\n')
        self.assertTrue(any('missing bundled resource' in e for e in validate_skill_bundle(skill)))

    def test_reference_style_local_resource_is_portable(self):
        skill = self.fixture()
        (skill / 'guide.md').write_text('# Guide\n')
        (skill / 'SKILL.md').write_text('[guide][local]\n\n[local]: guide.md\n')
        self.assertEqual(validate_skill_bundle(skill), [])

    @unittest.skipIf(os.name == 'nt', 'POSIX symlink test')
    def test_full_validation_does_not_reread_rejected_external_document(self):
        repository = self.root / 'fake-repository'
        module_path = 'skills/engineering/joy-test'
        skill = repository / module_path
        skill.mkdir(parents=True)
        (repository / 'catalog.json').write_text(json.dumps([{'name': 'joy-test', 'category': 'engineering', 'path': module_path}]))
        (repository / 'README.md').write_text('[skill](' + module_path + '/SKILL.md)\n')
        (skill / 'SKILL.md').write_text('---\nname: joy-test\ndescription: Test only\nmetadata:\n  author: 杨俊宁\n  email: luozhu2021@gmail.com\n---\n# Test\n')
        outside = self.root / 'external-document.md'
        outside.write_bytes(b'\xff\xfe')
        external = skill / 'external.md'
        external.symlink_to(outside)
        original_read = Path.read_text
        reads = []
        def observed_read(path, *args, **kwargs):
            reads.append(path)
            if path == external or path == outside:
                raise AssertionError('Full validation must not read rejected external documents')
            return original_read(path, *args, **kwargs)
        with patch.object(validator, 'ROOT', repository), patch.object(Path, 'read_text', observed_read):
            errors = validator.validate()
        self.assertTrue(any('outside bundled document' in e for e in errors))
        self.assertNotIn(external, reads)
        self.assertNotIn(outside, reads)


if __name__ == '__main__':
    unittest.main()
