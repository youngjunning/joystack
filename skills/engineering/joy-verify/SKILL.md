---
name: joy-verify
description: 为工程交付建立相称证据并报告尚未覆盖的边界；用于测试、构建、部署、目标设备或真实业务验收。
metadata:
  author: 杨俊宁
  email: luozhu2021@gmail.com
---

# JoyStack · Verify

从主张反推证据：用户可见行为、关键不变量和最可能回归点各需要什么验证。优先选择能真正观察结果的最小检查，而非只运行方便的命令。

把证据分层记录：静态检查、单元/集成测试、构建、部署、页面/设备、外部服务和真实业务结果。前一层通过不等于后一层已经确认；无法执行时说明缺少的环境、权限或输入，不把它写成成功。

当验证暴露异常，提供复现事实并交给 [`joy-debug`](../joy-debug/SKILL.md)。当验证充分后，可交给 [`joy-review`](../joy-review/SKILL.md) 检查范围遗漏，再依项目规则交付。共享交接标准见[套件契约](../joy-stack/references/stack-contract.md)。
