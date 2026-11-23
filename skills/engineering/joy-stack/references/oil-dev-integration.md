# oil dev skills 融合记录

来源为 [oil-oil/oil-dev-skills](https://github.com/oil-oil/oil-dev-skills) 的 `9bcd9000cfd08ef40546420f403e04a4df1c31f2`，核对日期为 2026-11-22，上游许可为 MIT。JoyStack 保留来源与方法归属，以自己的能力边界和文字实现，不复制上游脚本、资产、个人配置或运行时。

| 上游能力 | JoyStack 落点 | 吸收的决策增量 | 不引入的依赖 |
| --- | --- | --- | --- |
| Explore | Understand | 按未知范围分级探索；只读摸底；核对复用基建、仓库约定和真实测试入口 | 仓库扫描脚本、固定模型与并行偏好 |
| Plan | Shape、Build、Verify、Git Delivery | 任务重量分级；事实就绪门；实现范围与快检/门禁契约；结果回验 | 固定模板、强制 worktree 流程、上游合并编排 |
| Delegate | Build、Continue | 宿主中立的委托契约、停止条件与返回结果回验 | 外部 CLI 选择器、会话包装器、`~/.oil-dev` 配置 |
| Code Review | Review | 先查范围漂移，按风险选择轻审或深审，聚焦五类可行动问题 | 上游 review helper 与固定审查运行时 |
| Bug Fix | Debug | 复现优先、根因成立条件、源头修复、系统性扫描与止损 | 固定会诊 runner、自动修改常驻规则 |
| Govern | Govern | 事实采集与语义判断分离；文档单源、测试分层、确定性检查、分支/worktree 看板 | 上游 audit 脚本、固定文档体积阈值、自动删除 |

上述能力始终由 JoyStack 自身与宿主现有工具完成。oil dev skills 仅作为工程方法来源，不安装、不调用，也不作为可选执行实现或缺失能力的降级依赖。保留来源、许可与方法归属；上游后续变化不会自动同步，重新吸收方法前应再次核对来源、许可和行为差异。
