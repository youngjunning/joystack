# JoyStack · Git Delivery 收尾事实契约

`joy-git` 独立核验仓库、Git 和交付事实；调用方决定最终标题与排版。

每个实际工作的仓库分别提供：

1. 仓库显示名、可浏览远端主页 URL 与当前分支；没有可浏览远端时提供本地仓库绝对路径，detached HEAD 显示短 SHA 和“未关联分支”。
2. 本任务工作区、commit 和 push 状态。远端提供可浏览的 commit 页面时，用短 commit ID 作为链接文字并指向该提交；无法构造或核验页面时保留纯文本 ID，不编造链接。push 只有在对应远端 ref 回读包含任务 commit 后才能称成功。
3. 采用 PR 流程时提供 PR URL、head/base、required checks、review、mergeability 与 merge 状态；创建 PR、CI 通过和已经合并分别报告。已合并时记录平台 merge/result commit 与 PR 终态，不假定原 head commit 会因 squash/rebase 成为 base 祖先。
4. 创建、认领或续接的 worktree 给出任务、路径、分支、目标、状态、保留原因与清理条件；查询报告覆盖范围和未知用途。清理候选、占用检查、实际删除和 Git/路径回读分别报告；开放 PR、待合回、待验收或唯一恢复入口仍需保留。台账更新不等于 Git 改动。
5. 适用的测试、构建、制品、部署、分发与真实业务验收；未执行或未验证的门槛保持原样。
6. 无关改动只说明它影响了哪个交付决定，不计入本任务成果。

没有本任务仓库改动时不制造空提交；worktree 管理仍报告实际查询、台账与处置结果，Git 交付为 `no-action`。多个仓库分别报告，不把一个仓库的成功推广为全部完成。
