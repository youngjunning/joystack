---
name: joy-build
description: 将已澄清的工程目标实现为最小、可反馈的纵向切片；用于功能、重构或已定位修复的实施阶段。
metadata:
  author: 杨俊宁
  email: luozhu2021@gmail.com
---

# JoyStack · Build

在动手前重读任务契约和受影响仓库约定，选择最小能交付用户结果的切片。先让现有接口、数据模型和错误边界保持一致；需要新增边界时，说明旧链路为何不能表达这个结果。

每完成一个切片就取得贴近风险的反馈：类型/静态检查、定向测试、可运行行为或界面回验。测试先行适合能以一个清楚失败表现描述的缺陷或行为；不适合时，仍应先确定可观察的验收信号。避免为“覆盖率”制造只证明实现细节的测试。

实现中发现目标不成立、事实变化或风险超出契约时回到 [`joy-understand`](../joy-understand/SKILL.md) 或 [`joy-shape`](../joy-shape/SKILL.md)，而非继续堆叠补丁。完成后交给 [`joy-verify`](../joy-verify/SKILL.md)，需要独立检查时再交给 [`joy-review`](../joy-review/SKILL.md)。共享交接标准见[套件契约](../joy-stack/references/stack-contract.md)。
