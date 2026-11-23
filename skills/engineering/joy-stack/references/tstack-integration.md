# tstack 融合记录与验收边界

来源：[t3dotgg/tstack](https://github.com/t3dotgg/tstack/tree/11e37a74d0a6868c121cd0910ab2b3bd9873b92a)，固定 commit `11e37a74d0a6868c121cd0910ab2b3bd9873b92a`，MIT / Theo Browne。2026-11-23 在完整评估后选择局部吸收；不整体安装、复制 watcher 或绑定模型/运行时。本记录描述 Skill 契约融合，不宣称真实 PR 成功率、多模型质量或成本已经验收。

## 逐项落点

| 上游 | 当前模块及其 reference | 增量与边界 |
| --- | --- | --- |
| modernize、takeover | joy-continue：`references/inherited-work.md`；joy-understand 触发指针 | 只读 semantic refresh，KEEP/REWORK/SUPERSEDED/UNRESOLVED；最新纠正、原目标、源 head 与贡献保留 |
| file-pr、leaving-pr-comments | joy-git：`references/pr-delivery.md` | Problem/Solution/Evidence/Limits、查重、draft 跟项目、原作者/squash、评论回执再按授权 resolve |
| babysit-pr | joy-git：`references/pr-observation.md` | 单所有者、cursor、完整性、head/base、有界等待/退出；不移植 pr-wait，不实现 watcher |
| sol-loop | 已有 joy-loop；新增 `references/review-lifecycle.md` | 保留 3/5 轮，补时间/调用预算、终止确认、checkpoint 和 diff-growth |
| council | joy-review 可选多视角 | 真实路由/授权，不默认三提供商、数字评分或一致意见门禁 |
| full-send、full-stop | joy-git 现有模式与 PR/MR 终点 | 不新增 send/stop；不口令扩权、强制 PR 或擅改 auto-merge/queue |

跨 Skill 按名称发现后解析真实目录；同模块 references 相对自身，不要求兄弟安装。私有/项目适配器可实现等价语义，不把私有 API 或平台数据写进本公开仓库。

## 许可与归属

新增 reference 独立表述方法，保留上述版本与来源，没有复制上游脚本或模型调用。已有 joy-loop 的上游 LICENSE/NOTICE 保留；未来复制或实质改编上游文字/代码仍需保留版权与 MIT 声明，来源/许可不产生模型或平台授权。

## 契约验收案例

| ID | 情景 | 应有处理 |
| --- | --- | --- |
| TS01 | 旧 PR 无冲突但问题已被解决 | SUPERSEDED 建议，不机械重放或自动关闭 |
| TS02 | 目标有效但 API/所有权变化 | REWORK；收敛同目标最小范围，按权限实施 |
| TS03 | 交接与最新纠正不一致，源 head 又前进 | 当前事实/纠正优先，回查来源和责任人 |
| TS04 | 继承 commits 将 squash | 保留核验作者/co-author，新修正分开，不猜邮箱 |
| TS05 | reviewer 输出完整 verdict 后仍运行 | deadline 后取消并确认终止，匹配 checkpoint 才接受 |
| TS06 | 无回复、失败、预算耗尽 | 非批准、BLOCKED；不换 reviewer 重置预算 |
| TS07 | 评审新增范围外 lock/cache/helper | 查必要性，不为评分扩大 diff；低频真实风险保留 |
| TS08 | ready/exit 0 但人工阻断或规则不可读 | UNKNOWN/blocked，父任务核查 gate |
| TS09 | head 变、checks 旧或分页截断 | 旧观察失效，保留版本/完整性未知，不合并 |
| TS10 | 只准备 PR/MR，已有自动合并 | 说明终点冲突，按授权处理设置并回读 |
| TS11 | 重启、游标过期、rate limit、重复监听 | 单所有者、有界恢复，停止时解除自己的观察 |
| TS12 | 无模型路由/通知/平台适配 | 明确缺项，其它基础模块与直接 Git 交付继续 |

`scripts/test_tstack_integration.py` 验证入口、references、关键语义、案例覆盖与来源，属于静态契约检查，非 Agent 行为评测。既有 worktree 脚本测试独立运行；独立评审检查 instruction 一致性，不替代真实 PR/MR、模型等待/取消、race 与恢复验收。

在获准真实任务上比较改前/改后漏接、过期误推进、贡献丢失、scope growth、挂起、假 ready、人工时间及总调用成本。watcher 运行时、多供应商 Council、平台写操作试验仍未实施，不是此次纯 Skill 融合必须自动执行的任务。
