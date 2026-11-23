"""Static contract regression checks; these do not simulate Agent or PR execution."""
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'skills' / 'engineering'


def read(module, path='SKILL.md'):
    return (SKILLS / module / path).read_text()


class TstackIntegrationTests(unittest.TestCase):
    def test_inherited_work_is_reachable_and_read_only_first(self):
        self.assertIn('references/inherited-work.md', read('joy-continue'))
        contract = read('joy-continue', 'references/inherited-work.md')
        for disposition in ('KEEP', 'REWORK', 'SUPERSEDED', 'UNRESOLVED'):
            self.assertIn(disposition, contract)
        for rule in ('只读', '最新纠正', 'git range-diff', 'Co-authored-by', 'squash', '不猜邮箱'):
            self.assertIn(rule, contract)

    def test_review_budget_is_elapsed_not_only_round_count(self):
        self.assertIn('references/review-lifecycle.md', read('joy-loop'))
        contract = read('joy-loop', 'references/review-lifecycle.md')
        for rule in ('单轮', '10 分钟', '总计 30 分钟', '50 分钟', '剩余预算', '终止', '基线', 'diff', 'BLOCKED'):
            self.assertIn(rule, contract)
        self.assertIn('不增加委托或外部模型调用权限', contract)

    def test_observation_cannot_authorize_merge(self):
        self.assertIn('references/pr-delivery.md', read('joy-git'))
        self.assertIn('](pr-observation.md)', read('joy-git', 'references/pr-delivery.md'))
        self.assertTrue((SKILLS / 'joy-git/references/pr-observation.md').is_file())
        observation = read('joy-git', 'references/pr-observation.md')
        for rule in ('单一所有者', 'head', 'base', '完整性', 'UNKNOWN', 'cursor', '不是合并许可', '预算', '停止'):
            self.assertIn(rule, observation)
        self.assertIn('没有实现新的 watcher', observation)

    def test_pr_publication_and_credit_remain_separate_gates(self):
        contract = read('joy-git', 'references/pr-delivery.md')
        for rule in ('Problem', 'Solution', 'Evidence', 'Limits', '原作者', 'squash', 'ready', 'merged', 'resolve', '授权', 'auto-merge'):
            self.assertIn(rule, contract)

    def test_multi_perspective_is_optional_and_evidence_based(self):
        contract = read('joy-review')
        for rule in ('可选多视角', '同一不可变基线', '模型评分', '调用权限'):
            self.assertIn(rule, contract)

    def test_acceptance_catalog_covers_host_neutral_cases(self):
        text = read('joy-stack', 'references/tstack-integration.md')
        for n in range(1, 13):
            self.assertEqual(text.count(f'| TS{n:02d} |'), 1)
        names = {s['name'] for s in json.loads((ROOT / 'catalog.json').read_text())}
        self.assertNotIn('joy-send', names)
        self.assertNotIn('joy-stop', names)
        self.assertIn('非 Agent 行为评测', text)
        self.assertIn('11e37a74d0a6868c121cd0910ab2b3bd9873b92a', text)


if __name__ == '__main__':
    unittest.main()
