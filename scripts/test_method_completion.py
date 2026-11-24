"""Regression guards for method routing/portable docs, not Agent competence tests."""
from pathlib import Path
import shutil
import tempfile
import unittest

from validate import ROOT, validate_skill_bundle


MODULES = ROOT / 'skills/engineering'
BRANCHES = {
    'joy-review': ('review-axes.md',),
    'joy-debug': ('diagnosis-loop.md',),
    'joy-shape': ('domain-modeling.md', 'module-design.md', 'prototypes.md'),
    'joy-understand': ('primary-research.md',),
    'joy-govern': ('architecture-audit.md',),
}


class MethodCompletionTests(unittest.TestCase):
    def read(self, module, filename):
        return (MODULES / module / 'references' / filename).read_text()

    def test_methods_are_linked_at_the_owning_entry_and_portable(self):
        for module, filenames in BRANCHES.items():
            entry = (MODULES / module / 'SKILL.md').read_text()
            for filename in filenames:
                self.assertIn(f'](references/{filename})', entry, module)
            with tempfile.TemporaryDirectory() as temporary:
                target = Path(temporary) / 'isolated' / module
                shutil.copytree(MODULES / module, target,
                                ignore=shutil.ignore_patterns('__pycache__'))
                self.assertEqual(validate_skill_bundle(target), [])

    def test_review_does_not_invent_a_spec_or_mask_an_axis(self):
        text = self.read('joy-review', 'review-axes.md')
        for phrase in ('Standards', 'Spec', '规格缺失', '不能声称 Spec 通过',
                       '无效 ref', '工作区', '不自动启动两个 reviewer', 'Fowler'):
            self.assertIn(phrase, text)
        for name in ('Mysterious Name', 'Duplicated Code', 'Feature Envy',
                     'Data Clumps', 'Primitive Obsession', 'Repeated Switches',
                     'Shotgun Surgery', 'Divergent Change', 'Speculative Generality',
                     'Message Chains', 'Middle Man', 'Refused Bequest'):
            self.assertIn(name, text)

    def test_diagnosis_keeps_red_capable_feedback_and_original_recheck(self):
        text = self.read('joy-debug', 'diagnosis-loop.md')
        for phrase in ('已实际运行', '用户原始症状', '无法建立反馈', '待验证',
                       '原始完整场景', 'seed', '清理', '不因重复失败自动提高预算'):
            self.assertIn(phrase, text)

    def test_domain_decisions_are_not_implementation_or_permission(self):
        text = self.read('joy-shape', 'domain-modeling.md')
        for phrase in ('GLOSSARY-MAP.md', '不写实现细节', '拟议', '不可逆',
                       '真实取舍', '延续项目原目录', '并发', '授权'):
            self.assertIn(phrase, text)

    def test_deepening_does_not_authorize_blind_test_deletion(self):
        text = self.read('joy-shape', 'module-design.md')
        for phrase in ('caller', 'seam', 'adapter', '删除测试', 'joy-test',
                       '进程内', '本地替身', '自有远端', '真正第三方',
                       '项目术语', '不自动并行调用多个模型'):
            self.assertIn(phrase, text)

    def test_prototypes_keep_ui_fidelity_and_are_not_shipping_evidence(self):
        text = self.read('joy-shape', 'prototypes.md')
        for phrase in ('逻辑', 'UI', 'joyally-design', '不套用 Ponytail',
                       '不拦截输入控件', '同一内容', '生产', '不直接晋升',
                       'stub', '用户要求的视觉、交互、状态或动效'):
            self.assertIn(phrase, text)

    def test_research_and_audit_keep_sources_and_authorization(self):
        research = self.read('joy-understand', 'primary-research.md')
        for phrase in ('一手来源', '固定版本', '无命中', '读取失败',
                       '不默认派生后台 Agent', '不自动写入个人记忆'):
            self.assertIn(phrase, research)
        audit = self.read('joy-govern', 'architecture-audit.md')
        for phrase in ('只读', 'before/after', 'joy-shape', 'joyally-image',
                       '无改造价值', '不自动改代码'):
            self.assertIn(phrase, audit)

    def test_completion_record_keeps_attribution_and_historical_limits(self):
        entry = MODULES / 'joy-stack/SKILL.md'
        record = MODULES / 'joy-stack/references/matt-method-completion.md'
        self.assertIn('references/matt-method-completion.md', entry.read_text())
        text = record.read_text()
        for phrase in ('abeeaf95660ba9e8b7c753eb38f441ca707a8823',
                       'Matt Pocock', 'MIT', '独立编写', '真实 Agent',
                       'codebase-design', 'domain-modeling', 'prototype',
                       'research', 'improve-codebase-architecture', 'grill-with-docs'):
            self.assertIn(phrase, text)


if __name__ == '__main__':
    unittest.main()
