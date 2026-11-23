"""Keep method attribution separate from optional upstream execution."""
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
ENTRY = ROOT / 'skills/engineering/joy-stack/SKILL.md'
RECORD = ROOT / 'skills/engineering/joy-stack/references/oil-dev-integration.md'


class OilIntegrationContractTests(unittest.TestCase):
    def test_oil_remains_a_method_source_not_an_execution_dependency(self):
        text = RECORD.read_text()
        self.assertIn('始终由 JoyStack 自身与宿主现有工具完成', text)
        self.assertIn('不安装、不调用', text)
        self.assertIn('不作为可选执行实现或缺失能力的降级依赖', text)
        self.assertNotIn('安装了上游套件时', text)
        self.assertIn('不安装或调用该套件', ENTRY.read_text())

    def test_source_and_license_attribution_are_preserved(self):
        text = RECORD.read_text()
        self.assertIn('https://github.com/oil-oil/oil-dev-skills', text)
        self.assertIn('9bcd9000cfd08ef40546420f403e04a4df1c31f2', text)
        self.assertIn('MIT', text)
        self.assertIn('保留来源、许可与方法归属', text)


if __name__ == '__main__':
    unittest.main()
