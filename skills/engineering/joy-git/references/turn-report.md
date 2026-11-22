# JoyStack · Git Delivery 收尾事实契约

`joy-git` 独立核验仓库、Git 和交付事实；调用方决定最终标题与排版。

每个实际工作的仓库分别提供：

1. 仓库显示名、可浏览远端主页 URL 与当前分支；没有可浏览远端时提供本地仓库绝对路径，detached HEAD 显示短 SHA 和“未关联分支”。
2. 本任务工作区、commit 和 push 状态。push 只有在对应远端 ref 回读包含任务 commit 后才能称成功。
3. 采用 PR 流程时提供 PR URL、head/base、required checks、review、mergeability 与 merge 状态；创建 PR、CI 通过和已经合并分别报告。已合并时记录平台 merge/result commit 与 PR 终态，不假定原 head commit 会因 squash/rebase 成为 base 祖先。
4. 本任务创建的临时 worktree 或分支是否已清理；开放 PR 或唯一恢复入口需要保留时，给出路径、分支、原因和恢复条件。
5. 适用的测试、构建、制品、部署、分发与真实业务验收；未执行或未验证的门槛保持原样。
6. 无关改动只说明它影响了哪个交付决定，不计入本任务成果。

没有本任务改动时不制造空提交或仓库事实。多个仓库分别报告，不把一个仓库的成功推广为全部完成。
