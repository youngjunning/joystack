# 有界评审与当前基线

轮数、等待时间和调用成本分别控制。该协议不增加委托或外部模型调用权限，reviewer 仍只读、无 Git 交付、无再委派权限；模型/effort/usage 只记录宿主实际暴露的值。

## 启动前固定预算与证据

建立本轮 checkpoint：原目标和最新纠正、仓库/commit、scoped 行为 diff（包括 untracked）、范围外事项、现有验证和开放 finding ID。记录 reviewer ID、启动时间、单轮 deadline、Loop 剩余预算与允许的终止方法。

未指定时间时，单轮默认最多 10 分钟，默认 3 轮总计 30 分钟；符合主 Skill 高风险条件延长至 5 轮时，总计上限 50 分钟。预算包含等待、reviewer 重试和作者修正，不因换 reviewer 或中断恢复而重新计数；用户或宿主预算更小则使用更小者。延长范围以本次授权为准，不自创付费额度。调用/费用预算有返回值时记录，无返回值只报告未知，不编造。

## 等待与终止

使用宿主已有的有界 wait/通知方式，不建立第二个 watcher。接近单轮 deadline 时只读检查进展：打印 verdict 但仍在运行，不等于 reviewer 终态；不在其仍审查的 checkout 修改 scoped 文件。

| 观察 | 处理 |
| --- | --- |
| reviewer 正常完成 | 核对完整 findings/APPROVE、checkpoint 与当前 diff；交作者逐项核实 |
| 已输出完整 verdict，仍运行 | 到达 deadline 后使用获准取消并确认终止；只在结果完整、对应固定基线且终止已确认时接受该结果 |
| 超时、失败、缺正文或基线变化 | 保存已知证据，非批准；确认旧 reviewer 终止后才可在剩余预算内重试，重试计入本轮时间与总调用预算 |
| 无取消/终止观察能力，不能确认 reviewer 已停止 | 保持 scoped 文件不变，交接最小恢复条件并结束为 BLOCKED；不强杀其它任务、不制造并行冲突者 |
| 预算耗尽或同一 finding 两次有据回应仍争议 | BLOCKED，保留双方证据、当前状态与可继续条件；无响应、低使用量或高评分均不能替代批准 |

在 deadline 内没有可立即推进的非重叠工作时正常有界等待，不为了“不能闲着”重读 scoped 文件或再启 reviewer。中断恢复先回查原 reviewer 与已耗预算，不让旧任务和新任务同时工作。

## 修正后重新核对当前行为 diff

维护同一原始任务基线与每轮 checkpoint，记录新增行为及开放 finding；可以用相同 `git diff` 与 `git diff --shortstat` 辅助，但行数不是质量门禁。每项新增 lock/cache/helper/guard/兼容分支/测试都需对应任务内的真实问题与验证。范围外建议写明拒绝理由或交后续，不为讨好 reviewer 加复杂度。

安全、数据丢失、并发或兼容风险可能低频但后果重大，不能自动降成 nit。行为变化/有意义冲突解决使旧批准失效；若只改已驳回 nit 的解释或非行为文案，可沿用仍匹配当前行为 diff 的批准。最终 APPROVE 要对应当前 checkpoint、无开放 blocker/should 并有相称验证。
