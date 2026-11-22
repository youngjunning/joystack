---
name: joy-review
description: 独立检查变更是否符合原目标、系统契约与可维护性要求；用于合入、发布或重要交付前的评审。
metadata:
  author: 杨俊宁
  email: luozhu2021@gmail.com
---

# JoyStack · Review

以任务契约和实际 diff 为共同基线，分别检查两件事：变更是否实现承诺的结果，以及它是否破坏现有边界、错误处理、兼容性、可读性或验证能力。两类结论不互相替代。

只报告可行动的问题：指出受影响位置、触发条件、后果和最低成本的修正方向；不把个人偏好、尚无证据的猜测或范围外重构包装成阻断项。没有问题时说明实际检查过什么，而不是笼统给出“看起来没问题”。

发现未验证的关键主张交给 [`joy-verify`](../joy-verify/SKILL.md)；发现机制不明的缺陷交给 [`joy-debug`](../joy-debug/SKILL.md)。共享交接标准见[套件契约](../joy-stack/references/stack-contract.md)。
