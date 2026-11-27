# Worktree 生命周期

每个任务目录都要能回答：做什么、谁在用、成果往哪里合、为什么保留、何时退出。Git 负责仓库事实；本机台账只记录调用方确认的任务语义。使用 Git 和 Python 3.9+ 标准库，无第三方 CLI、后台服务或数据库依赖。

## 入口与位置

默认在当前 checkout 工作。确有隔离需要时，先查仓库协议和当前 worktree 列表，复用适合该任务的已有目录；不要为了治理改成一律新建。

- 项目或用户明确指定的位置在平台权限内优先；默认自建目录使用当前环境家目录下 `.joystack/worktrees/<repo>-<repository-id>/<task-slug>`。家目录由环境解析，不从 cwd/工作区推断。repository-id 来自 Git common directory 指纹，避免同名仓库互撞；目录名体现任务语义。
- 宿主目录保留宿主路径。已有散落目录先只读盘点，确认用途后登记；不批量搬家，不从名字、提交时间或相似 diff 推断归属。
- 项目内位置须已被 Git 忽略；脚本检查，不自动修改或提交 `.gitignore`。Git metadata 目录不作为工作目录。
- 台账在 `~/.joystack/state/worktrees.json`；统一根目录与安装边界见 JoyStack 全局目录（按技能名发现 `joy-stack`，再从其实际目录读取 `references/global-home.md`）。只存本机必要信息，不放进项目源码、附件或公开 Git，不记录凭据、完整会话或敏感业务正文。

## 原生脚本

入口为本 Skill 的 [scripts/worktrees.py](../scripts/worktrees.py)。`SKILL_DIR` 使用当前发现的实际 Skill 目录，不缓存某个账号的安装路径；参数以 `--help` 为准。`JOYSTACK_HOME` 明确覆盖数据根目录；`--index`、`--root` 用于明确的项目覆盖或隔离测试。

受限平台必须由调用层提供 `JOYSTACK_WORKSPACE` 或全局 `--workspace`：检查 cwd、目录/台账/锁文件与 Git common-dir 的真实路径在边界内，覆盖参数和符号链接也要检查。边界不改默认家目录；不兼容时报告缺项，不能静默换位置。原生 Git 执行仍由平台沙箱和权限控制，这些校验不构成安全沙箱。

用户要求初始化时执行 `python3 "$SKILL_DIR/scripts/worktrees.py" init`，幂等创建全局目录并保留已有台账。普通盘点、创建计划不执行 init。

### 盘点：先事实，后认领

```bash
python3 "$SKILL_DIR/scripts/worktrees.py" list --repo /path/to/repo --json
python3 "$SKILL_DIR/scripts/worktrees.py" list --json
```

指定 `--repo` 时只查这些仓库，可重复该参数。未指定时查台账已知仓库与当前 Git 仓库，不扫描磁盘、宿主历史或所有项目；首次跨仓库盘点时显式传入获准仓库路径。报告覆盖范围及每个仓库的读取失败，失败不等于无 worktree。

输出包含主 checkout、linked worktrees、detached HEAD、锁定/失效目录、用途与任务状态、未提交/未跟踪/忽略文件、进行中的 Git 操作、目标包含关系，以及可用的 upstream 差异。未登记目录显示用途未知，不能当空闲。台账存在而 Git 不再登记的目录单独提示，不自动 prune 或清除记录。

读取不初始化台账、不执行 fetch、不写 Git index。ref 和 upstream 差异只依据本机缓存；`last_commit_at` 是提交时间，`updated_at` 是台账更新时间，均不是最后使用时间。`--review-days` 仅提示台账多久未复查，不授权删除。台账损坏时停止，保留原文件，不重置为空表。

### 创建：计划与执行分开

```bash
python3 "$SKILL_DIR/scripts/worktrees.py" create \
  --repo /path/to/repo --branch task/fix-search --slug fix-search \
  --task '修复搜索结果' --session 'caller-task-id' \
  --base origin/main --target origin/main \
  --cleanup-when '成果进入目标分支，验收完成且没有会话或进程占用'
```

默认只返回位置、分支、基线的创建计划，不创建目录或台账。按项目规则核对最新基线和创建权限后，同一命令增加 `--apply`，用 native `git worktree add` 创建并立即登记。调用方传入真实任务/会话标识和清理条件；无法获知宿主 session ID 时使用明确的本地任务标识，不编造宿主绑定。

脚本不安装依赖、不主动运行项目脚本、不推送；native Git 仍可能触发现有 hooks，沿用其配置而不绕过。add/hook 非零退出或超时时回查实际目录和 Git 登记：报告失败原因与路径存在事实，不声称本次创建，不自动登记；即使仓库、分支与 HEAD 均吻合，也不能证明创建来源。确认归属后由 Agent 显式 register，必要时 update 为 paused 并保留 setup 原因，避免重复创建或强删。成功 add 后也核对三项身份，吻合才登记；台账保存失败时报告创建已成功、登记失败，回查后恢复。台账锁只保护台账写入，不约束外部原生 Git 操作。

### 认领与续接

```bash
python3 "$SKILL_DIR/scripts/worktrees.py" register \
  --path /path/to/existing-worktree --task '搜索修复待验收' \
  --session 'caller-task-id' --target origin/main \
  --cleanup-when '合回并验收后清理'

python3 "$SKILL_DIR/scripts/worktrees.py" update \
  --path /path/to/existing-worktree --state verify --keep-reason '等待目标环境验收'
```

register 只登记真实、完整的 linked worktree 根路径，不登记主 checkout、子目录或不存在的路径。采用已有目录时，创建时间与原始基线保持未知；确认了基线才传 `--base`，不从当前 HEAD 倒推历史。重复登记同一任务/会话/分支保留状态和保留原因；不同任务或会话不能由 register 覆盖，须核对占用和交接权限后显式 update，并明确传入新 `--state`，不继承旧任务完成状态。分支改变后先检查，再重新登记同一任务。

任务状态由调用方维护：`active` 进行中、`review` 待评审、`merge` 待合回、`verify` 保留验证、`paused` 暂缓、`done` 任务已结束。没有固定过期删除状态。done 不能替代实时 Git、PR、占用和成果采用证据；有保留原因时继续保留。更新后回读；续接或交付时给出下一步和清理条件。

## 清理：候选不是授权

```bash
python3 "$SKILL_DIR/scripts/worktrees.py" cleanup-plan --repo /path/to/repo --json
```

脚本只列候选与阻塞原因，不删除目录、分支或进程。仅当已登记任务为 done、无保留原因、目录存在且未锁定、无改动/未跟踪/忽略文件、无进行中 Git 操作，且当前 HEAD 是明确目标的祖先时，标记 `needs-occupancy-review`。此标记仍缺会话/进程检查和动作权限，不叫“可安全自动删除”。

执行删除前，由 Agent 再核对：

1. **对象与权限。** 明确路径、分支、任务和目标。主 checkout、bare repo 与用途未知目录保留；已有他人/宿主资源按明确认领和清理授权处理。
2. **成果采用。** 依据最新目标 ref 和已完成的 PR/merge 证据，确认成果进入实际目标，原工作分支已接回或有明确可恢复采用路径。推送任务分支不等于合回。squash/rebase 使祖先检查不通过时单独核对采用映射；脚本保守阻塞，不自动作内容等价判断或强删。
3. **现场与占用。** 回读 staged、unstaged、untracked、ignored、子模块与 Git 操作。忽略文件可能是缓存，也可能是凭据或资料，需逐项确认可丢弃。用当前宿主可用的任务/会话接口及系统进程信息查占用；无接口或无法确定时保留，不能用不存在锁、目录干净或提交很旧替代。当前执行目录先切换到保留的 checkout，不自动终止进程。
4. **执行与回读。** 在保留的 checkout 执行 `close --path /path/to/worktree` 预览；完成上面的人工作业/会话核对后增加 `--apply --sessions-clear`。命令在台账锁内重新检查状态、Git 事实、目标包含关系及进程 cwd，占用或事实变化即拒绝；使用不带 `--force` 的原生 `git worktree remove`，回读目录和 Git 登记均消失后才注销台账。`--sessions-clear` 是调用方已核对会话及非 cwd 进程的声明，不能用来跳过检查。失败时保留记录和分支，逐项排查，不升级删除力度。旧的手工移除流程仍可用 `forget --path ...` 单独注销已不存在的目录。

本地分支是另一对象：开放 PR、尚未采用提交或唯一恢复入口仍需保留；只有已采用且不再被任何 worktree/任务使用时，按授权单独安全删除本地分支。没有远端分支删除授权。`git worktree prune` 仅清理失效 metadata，不清理目录；用途不明、锁定或外接盘暂不可用时不自动 prune。手工移动导致登记不一致时先检查原路径与宿主状态，按 Git repair 流程恢复，不把“不见了”当“已清理”。

## 管理结果

每个 worktree 给出任务、路径、分支、目标、任务状态、Git 事实、保留原因、占用证据与清理条件；标明未登记、未检查、读取失败和范围外对象。管理状态写入本机台账不等于更改 Git，也不触发空提交；实际清理与“建议清理”分别报告。
