---
name: joy-shape
description: 将模糊需求收敛成可实施、可验收的最小结果与系统边界；用于目标、术语、取舍或成功条件尚未明确时。
metadata:
  author: 杨俊宁
  email: luozhu2021@gmail.com
---

# JoyStack · Shape

把“想做什么”变成一个足够实施的任务契约：目标用户或使用场景、可观察结果、明确不做的范围、已有约束、失败与恢复边界，以及验收证据。

优先使用当前对话、仓库约定和实际代码补全上下文；只在缺失的选择会改变结果、成本、数据兼容性、外部影响或不可逆性时提问。不要把 Agent 提议伪装成用户决定，也不要为了消除所有不确定性而阻塞小改动。

跨模块、权限、付费、数据迁移、外部发布或目标环境验收无法本地证明时，明确它们的所有者和停止条件。契约清楚后交给 [`joy-build`](../joy-build/SKILL.md)；需要验证策略时同时交给 [`joy-verify`](../joy-verify/SKILL.md)。共享交接标准见[套件契约](../joy-stack/references/stack-contract.md)。
