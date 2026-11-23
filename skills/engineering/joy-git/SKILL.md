---
name: joy-git
description: 安全完成 Git 提交、推送、PR 与合并交付；管理 worktree 的位置、任务用途、状态、续接和清理。用户查询、创建、认领或清理 worktree 时也使用；普通代码评审与无关只读问答不触发。
metadata:
  author: 杨俊宁
  email: luozhu2021@gmail.com
---

# JoyStack · Git Delivery & Worktrees

负责 Git 交付与任务 worktree 的生命周期。产生仓库改动时，按项目规则与用户当次要求选择直接提交推送或任务分支 + PR；安全门通过后推进到获准终点。需要隔离或管理已有 worktree 时，让位置、用途、状态、成果去向和清理条件可查。它不替代实现、测试、评审、发布或合并冲突处理，不依赖第三方 worktree 管理器。

## 何时进入与交接

Git 交付在 [`joy-verify`](../joy-verify/SKILL.md) 已给出相称证据、需要的 [`joy-loop`](../joy-loop/SKILL.md) 已通过，或用户明确要求 commit、push、PR、merge、Git 收尾时进入。输入是任务边界、项目协议、验证结果与当前仓库状态；输出是 Git 交付结果、提交/远端/PR 证据和保留事项。

准备创建隔离 worktree，或用户问目录用途、查 worktree 总览、认领、续接或清理时，直接进入 [worktree 生命周期](references/worktrees.md)，不必等实现完成。管理只读查询和本机台账不制造提交；没有本任务仓库改动时，Git 交付结果为 `no-action`，但仍完成所请求的管理工作。

平台执行权限是上限；项目 `AGENTS.md`、发布协议和用户当次要求在该上限内优先于本模块。它们决定作者身份、默认交付方式、目标分支、PR/merge 门禁，以及 push 或 merge 是否具有发布副作用；本模块不猜测规则，不把安装当授权，也不把 Git 操作当发布或业务验收。受限平台在执行前按 [全局目录与平台适配](../joy-stack/references/global-home.md) 校验实际路径与 Git common-dir。

## 建立安全边界

在编辑前和提交前分别核对仓库根目录、分支或 HEAD、远端/upstream、目标分支、作者身份，以及 staged、unstaged 和 untracked 状态。多个仓库、submodule 或 worktree 分别判断。

把文件分为本任务改动、已有并行改动，以及缓存/凭据/日志等不应提交的文件。只可显式暂存已确认属于本任务的文件。仅有可分离的 unstaged/untracked 改动时，可在当前 checkout 显式暂存任务文件；若 index 已含无关 staged 内容、分支已分叉、HEAD detached 或当前历史会夹带其他工作，则保留原现场并转入隔离交付。任务改动与并行改动无法可靠拆分时，说明语义依赖并请求决定。

## 隔离交付

交付模式和目标 ref 唯一时，脏工作区或分叉是隔离条件，不是默认停止理由：

1. 获取目标远端的最新状态，按 [worktree 生命周期](references/worktrees.md) 从目标 ref 的确切 commit 创建任务专用分支与目录，立即登记任务、会话、基线、目标和清理条件。
2. 只带入本任务文件或可审查补丁，不复制整个脏目录，也不 stash、reset、rebase 或改写原 checkout。
3. 在隔离环境复验、显式暂存并检查 staged diff；无法脱离未提交依赖独立通过时再请求决定。
4. 推送前再次获取目标 ref；远端前进且无语义冲突时，在未共享任务分支上重放任务提交并复验。
5. 直接交付时以普通 fast-forward push 写入明确目标；PR 交付时推送任务分支并创建或更新指向明确 base 的 PR。按 worktree 生命周期更新状态，核对成果采用、保留原因和会话/进程占用后执行获准清理；待评审、待合回或待验收时报告路径与退出条件。

隔离不新增发布或合并权限，也不授权 force push、共享历史改写、admin bypass 或远端分支删除。预先存在的 worktree、分支和并行改动默认只读保留；用户明确要求认领或清理的对象，按生命周期协议核对，不扩大到其他任务。

## 选择交付模式

- **直接交付：** 项目允许向目标分支普通推送，目标 ref 与发布副作用明确时，提交任务文件并 fast-forward push；不为形式统一额外创建 PR。
- **分支与 PR：** 项目要求、用户指定，或分支保护阻止直接推送时，从最新 base 建立任务分支，推送后创建或更新 PR。记录 head/base、PR URL、required checks、review 与 mergeability；新的代码问题回到 [`joy-loop`](../joy-loop/SKILL.md) 修正和复验。
- **自动门禁守候：** 已获合并授权且只剩可观察的自动 required checks 时，使用宿主的 wait/monitoring 机制在当前交付任务的有界执行预算内持续回读。成功后继续合并；失败后把具体 finding 交回 [`joy-loop`](../joy-loop/SKILL.md) 修正、复验并更新 PR。只有需要人工 review 或其他外部动作、平台不可观测，或等待预算耗尽时，才以开放 PR 交接。
- **合并：** 只有项目规则或用户已授权合并，且 required checks、required review、冲突和分支保护全部通过时才执行允许的 merge 方式。合并后按平台报告的 merge/result commit 与 PR 终态回读 base 已包含合并结果，兼容 merge、squash 与 rebase；再按规则清理任务资源。

## 决策与执行

先确认验证与项目规则相称，再选择一个结果：

| 结果 | 适用条件 | 动作 |
| --- | --- | --- |
| `commit-and-push` | 任务改动、验证、作者、目标 ref 和普通 push 的安全门都明确 | 只提交任务文件，普通推送并回读远端 ref |
| `pr-opened` | 项目或用户选择 PR 流程，任务分支与 base 明确；仍需人工/外部动作、平台不可观测，或自动门禁在有界等待后仍未结束 | 提交并推送任务分支，创建或更新 PR，报告 URL、当前门禁和继续条件 |
| `pr-merged` | PR 流程已获合并授权，全部 merge gate 通过 | 使用允许的 merge 方式合并，按平台 merge/result commit 和 PR 终态回读 base 的合并结果，再清理已采用且可安全删除的任务资源 |
| `commit-only` | 本地提交安全，但 push 会触发未获授权的发布、迁移或其他高影响动作 | 创建本地提交并报告未推送原因 |
| `leave-uncommitted` | 用户要求保留、验证未完成、关键检查失败或任务边界不能安全拆分 | 不改变 index 或历史，说明位置与恢复条件 |
| `no-action` | 无本任务改动，或请求本来就是只读工作 | 不制造空提交，也不推送他人的提交 |
| `ask` | 目标仍不唯一、存在真实语义冲突，或需要 force push、删除远端、绕过保护及无法先安全完成局部动作的高影响操作 | 说明已尝试的隔离路径、对象、风险和所需决定 |

直接自动推送只允许交付提交正常 fast-forward 到已确认的目标 ref；PR 模式只推送已确认的任务分支，并按平台事实处理 PR。原 checkout 的分叉不妨碍已经隔离的交付。不能绕过认证、签名、分支保护、required checks 或 required review。提交前检查 staged diff 与项目等价检查；提交后核对提交文件与作者；推送或合并后回读对应远端 ref。网络、认证或保护规则失败时保留成果并报告恢复入口，不改写历史或改变策略重试。

## 交付边界

交付时按[收尾事实契约](references/turn-report.md)提供每个仓库的可核对事实。测试、提交、推送、CI 触发、部署和真实业务结果分别是不同证据，不能互相代替。

维护本模块时，用[行为检查](references/behavior-checks.md)演练决策边界；它用于检查判断，不是固定命令模板。
