"""Test module discovery, portable references and ownership; not live Agent evals."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from validate import ROOT, validate_skill_bundle


TEST = ROOT / 'skills/engineering/joy-test'


class JoyTestContractTests(unittest.TestCase):
    def test_module_is_registered_and_routed_in_both_readmes(self):
        catalog = json.loads((ROOT / 'catalog.json').read_text())
        entries = [item for item in catalog if item['name'] == 'joy-test']
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]['path'], 'skills/engineering/joy-test')
        for path in ('README.md', 'README.en.md',
                     'skills/engineering/joy-stack/SKILL.md',
                     'skills/engineering/joy-stack/references/stack-contract.md'):
            self.assertIn('joy-test', (ROOT / path).read_text(), path)

    def test_complete_bundle_works_in_an_independent_mount(self):
        self.assertTrue(TEST.is_dir())
        with tempfile.TemporaryDirectory() as directory:
            mount = Path(directory) / 'independent' / 'joy-test'
            shutil.copytree(TEST, mount)
            self.assertEqual(validate_skill_bundle(mount), [])
            for name in ('test-methods.md', 'target-environments.md',
                         'ai-agent-evals.md', 'quality-audit.md', 'affected-tests.md', 'source-review.md'):
                self.assertTrue((mount / 'references' / name).is_file(), name)

    def test_testing_owns_methods_without_taking_delivery_or_loop(self):
        text = (TEST / 'SKILL.md').read_text()
        for phrase in ('name: joy-test', '测试工作的主入口', 'joy-build',
                       'joy-verify', 'joy-debug', 'joy-govern', 'joy-loop',
                       '不启动第二个 Loop', '不把测试通过提升为完整交付通过'):
            self.assertIn(phrase, text)
        for name in ('joy-build', 'joy-verify', 'joy-debug', 'joy-govern'):
            text = (ROOT / f'skills/engineering/{name}/SKILL.md').read_text()
            self.assertIn('joy-test', text, name)

    def test_test_first_and_quality_guards_survive_migration(self):
        text = (TEST / 'SKILL.md').read_text()
        self.assertIn('明确要求 test-first 或 TDD', text)
        methods = (TEST / 'references/test-methods.md').read_text()
        for phrase in ('Red', 'Green', 'Refactor', '最小反例', 'seed',
                       '无覆盖', '超时/崩溃', '疑似等价'):
            self.assertIn(phrase, methods)
        evals = (TEST / 'references/ai-agent-evals.md').read_text()
        for phrase in ('不在看到失败后临时追加重跑', '评测需求本身不构成这种授权'):
            self.assertIn(phrase, evals)
        audit = (TEST / 'references/quality-audit.md').read_text()
        self.assertIn('接口重命名不自动意味着原来的失败场景可以丢失', audit)

    def test_source_attribution_and_single_canonical_identity(self):
        text = (TEST / 'references/source-review.md').read_text()
        for phrase in ('joyally-skills', '64150e7b2a9507a368c4eb72fbf7cc75651c9b0c',
                       'Marcello Curto', 'Apache-2.0', 'CC BY-SA 4.0'):
            self.assertIn(phrase, text)
        for path in TEST.rglob('*.md'):
            self.assertNotIn('name: joyally-test', path.read_text(), path)


if __name__ == '__main__':
    unittest.main()
