# 变更交付：终点、贡献与平台门禁

适用于 PR/MR 创建、接续、守候或合并；平台命令使用当前可用的专用 Skill/工具及精确 help。不是 GitHub 专用总控，也不替代 Review/Loop/Verify。

## 一次确定交付终点

从当次请求和项目协议确定：留改动、只提交、提交推送、PR/MR ready 未合并、或 merged。未要求合并不默认为合并；已授权直接交付不强制新分支/PR。Full Send/Stop 口令不能自行授权设备控制、共享分支改写、生产发布或平台设置修改。

只准备不合并时，先读实际 auto-merge/merge queue 或等价设置。已有自动合并则说明终点冲突；只有项目规则/明确授权允许时才禁用或退队并回读，不自动移除他人设置。无权限处理时保留状态并报告阻塞，不声称 ready。

## 创建/更新与贡献

先核对该 source/head 与目标 base 是否已有 PR/MR，复用同一任务身份；只读查重失败不能当不存在并重建。draft、标题样式、reviewer 和平台要求按项目规则。

描述用 Problem → Solution → Evidence → Limits：原问题与用户影响、最小解法、实际验证和未覆盖边界。性能/成本数字必须有测量依据，不用实现清单或模型自评冒充收益。提交前检查正文、引用和附件受众；Agent 发言身份/样式按项目要求，模型身份未暴露时不猜。

接手继承变更时，按名称发现 `joy-continue` 并执行其 `references/inherited-work.md`：保留原作者、共同作者和源 PR/MR；新修正分开追溯。squash 前核验贡献信息能否保留在平台允许的合并提交中，不用接手者或模型替代人类贡献，不从用户名推断邮箱，也不为保留署名强改受保护历史。

## 评论与反馈闭环

对照当前代码和对应 head 核实每项 finding，修复、反证或范围外拒绝都有证据。跟随 `joy-loop` 更新开放 ID 与新行为 diff，必要低频风险不自动降级。

确有授权需评论时，核对仓库、PR/MR、thread/comment 与作者；成功回读 ID/URL 或内容回执后再考虑 resolve，且仅在该平台协议和授权允许时执行。评论已发不等于修复，resolve 不等于删除；不确定写入先回查同一对象，不盲目重发。不创建只为刷状态的评论。

## 观察与最终合并

等待任务读取[平台观察协议](pr-observation.md)。通知、green、机器人 done、观察器 exit 0 或 ready 都不是合并许可。每次 push/head/base 变化后，旧结果只作历史证据。

已获合并授权时，本模块回查完整当前门禁：仓库/变更身份、head/base、冲突和目标分支状态、项目 required checks/reviews、阻断意见、签名/队列等配置、允许的合并方式与本次 diff 的独立验证。保护规则不可读、列表截断、旧 head 结果、人工 requests-changes 或必需门禁缺失均不能通过。保留工具返回的 freshness/completeness；没返回则记未知，使用已获准的其它权威读取补齐，无法补齐则等待/交接。

动作前重新读 head；支持 expected-head/lease 的工具绑定已观察 head，不支持则紧贴动作回查并说明竞态窗口，不声称消除竞态。队列/auto-merge 受理不等于 merged；回读平台终态、merge/result commit 与目标成果后才完成。平台拒绝、lease 失配或权限不足时保留现场并更新证据，不 bypass、改写共享历史或改投其它分支。
