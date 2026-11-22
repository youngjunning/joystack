---
name: joy-understand
description: 在改动前还原代码、产品行为或历史决策的当前事实；用于不清楚系统如何工作、为何如此或影响范围多大时。
metadata:
  author: 杨俊宁
  email: luozhu2021@gmail.com
---

# JoyStack · Understand

先找到正在发生什么，再决定是否改。阅读与检索按问题收敛：从用户可见现象或目标入口出发，沿调用、数据和状态边界追到能解释结论的位置；必要时核对历史、配置、日志、文档或一手资料。

输出应区分已证实事实、合理推断和未知项，说明来源与影响范围。不要把文件名、相似术语、旧文档或单个测试当成当前行为的证明；也不要在尚未定位问题前直接给修复方案。

当已确认的目标、边界或验收条件仍不清楚时，交给 [`joy-shape`](../joy-shape/SKILL.md)。当事实已经足以安全实施，交给 [`joy-build`](../joy-build/SKILL.md)。共享交接标准见[套件契约](../joy-stack/references/stack-contract.md)。
