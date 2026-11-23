"""Validate attribution/navigation, not historical causality or Agent execution."""
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
STACK = ROOT / 'skills/engineering/joy-stack'
REFS = STACK / 'references'


class IntegrationSourceRecordsTests(unittest.TestCase):
    def test_every_source_has_its_own_linked_record(self):
        index = (REFS / 'integration-sources.md').read_text()
        for file in ('matt-pocock-integration.md', 'pstack-integration.md',
                     'tstack-integration.md', 'oil-dev-integration.md'):
            self.assertTrue((REFS / file).is_file())
            self.assertIn(f']({file})', index)
            for readme in ('README.md', 'README.en.md'):
                self.assertIn(f'references/{file}', (ROOT / readme).read_text())
        self.assertIn('references/integration-sources.md', (STACK / 'SKILL.md').read_text())
        self.assertIn('](integration-sources.md)', (REFS / 'stack-contract.md').read_text())

    def test_distinct_authors_and_reviewed_snapshots(self):
        matt = (REFS / 'matt-pocock-integration.md').read_text()
        pstack = (REFS / 'pstack-integration.md').read_text()
        tstack = (REFS / 'tstack-integration.md').read_text()
        self.assertIn('Matt Pocock', matt)
        self.assertIn('abeeaf95660ba9e8b7c753eb38f441ca707a8823', matt)
        self.assertIn('Lauren Tan', pstack)
        self.assertIn('7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9', pstack)
        self.assertIn('Theo Browne', tstack)
        self.assertIn('11e37a74d0a6868c121cd0910ab2b3bd9873b92a', tstack)

    def test_old_unknown_provenance_not_fabricated_as_new_execution(self):
        for file in ('matt-pocock-integration.md', 'pstack-integration.md'):
            text = (REFS / file).read_text()
            for phrase in ('最初参考版本', '未整体引入', '验证边界', 'MIT'):
                self.assertIn(phrase, text, file)
            self.assertIn('cce7d148bd716d40d650010c22f0dea69462b61a', text)
            self.assertIn('本次', text)
        oil = (REFS / 'oil-dev-integration.md').read_text()
        self.assertIn('不安装、不调用', oil)
        self.assertIn('不作为可选执行实现或缺失能力的降级依赖', oil)


if __name__ == '__main__':
    unittest.main()
