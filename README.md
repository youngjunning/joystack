# JoyStack

中文 | [English](README.en.md)

JoyStack 是一套供 coding agent 使用的工程 Skills。描述目标后，Agent 按任务需要调用理解、规划、实现、验证、排障、评审和 Git 交付等能力；明确的小改保持简短，复杂工作再增加必要的检查与交接。

它依托宿主已有的模型、工具和权限运行，不提供独立 Agent runtime，也不要求安装其他 Skill 套件。实际能执行的动作取决于当前宿主与项目授权。

## 开始使用

在支持 Agent Skills 的宿主中安装完整模块集。以下命令使用 [Skills CLI](https://github.com/vercel-labs/skills/blob/main/docs/commands.md)，需要可运行 `npx` 的 Node.js 环境。

项目级安装，在目标项目目录执行：

```bash
npx skills add youngjunning/joystack
```

希望跨项目使用时，选择全局安装：

```bash
npx skills add youngjunning/joystack -g
```

按安装提示选择模块和目标宿主，核对安装范围与目录。只支持文件导入的平台，可按其流程导入各 Skill 的完整目录，保留目录内的配套文件。安装不会自动运行项目任务、初始化数据目录或执行 Git 交付。

## 日常使用

无需记住或逐个点名模块，直接说明任务和限制，例如：

- “先说明上传链路现在如何工作，暂时不要改代码。”
- “修复大文件上传偶发失败，补上能复现问题的测试。”
- “检查这次修改是否符合原目标，并复验发现的问题。”
- “列出这些仓库的 worktrees，说明用途和清理条件，先不要删除。”
- “整理当前进度，让下次能继续；这轮不要提交。”
- “保持我选的模型和验收要求，全程减少 Token 浪费。”

Agent 根据可用 Skills 选择所需能力。缺少模块、工具、权限或独立 reviewer 时，应明确说明，不把未执行的检查当作通过。

## 工程能力

| 模块 | 何时使用 | 主要结果 |
| --- | --- | --- |
| [joy-stack](skills/engineering/joy-stack/SKILL.md) | 任务跨边界、目标模糊或需要验证与续接 | 选择必要模块，保持共同任务边界 |
| [joy-token](skills/engineering/joy-token/SKILL.md) | 任意模型/宿主下全程节流，或明确要求省 Token、上下文过大/调用重复 | 定向读取、精简输出与调用，按实际接口能力处理缓存/计量 |
| [joy-understand](skills/engineering/joy-understand/SKILL.md) | 不清楚系统行为、原因或影响范围 | 当前事实、来源、推断与未知项 |
| [joy-shape](skills/engineering/joy-shape/SKILL.md) | 范围、取舍或验收尚未明确 | 可实施的目标、边界与验收条件 |
| [joy-build](skills/engineering/joy-build/SKILL.md) | 已有清楚的实现目标 | 最小可反馈的改动与局部验证 |
| [joy-test](skills/engineering/joy-test/SKILL.md) | 测试策略、TDD、用例、Web/API 验收或 Agent evals | 测试实现、运行结果、失败分类与质量治理；不替代完整交付验收 |
| [joy-verify](skills/engineering/joy-verify/SKILL.md) | 需要证明某项结果成立 | 测试或验收证据及未覆盖的边界 |
| [joy-debug](skills/engineering/joy-debug/SKILL.md) | 出现异常、失败或性能回退 | 复现、根因、修复与回归保护 |
| [joy-review](skills/engineering/joy-review/SKILL.md) | 需要独立检查当前变更 | 对照原目标的 finding 与评审结论 |
| [joy-loop](skills/engineering/joy-loop/SKILL.md) | 实质行为改动需要评审、修正与复验 | 有限轮次后的 APPROVE 或 BLOCKED |
| [joy-govern](skills/engineering/joy-govern/SKILL.md) | 文档、测试、规则或 Git 卫生需要治理 | 有证据的治理清单与最小处置建议 |
| [joy-git](skills/engineering/joy-git/SKILL.md) | 提交、推送、PR、合并或 worktree 管理 | Git 交付事实及任务目录的生命周期状态 |
| [joy-continue](skills/engineering/joy-continue/SKILL.md) | 跨轮继续、暂停或移交 | 可核对、可续接的交接信息 |

模块按技能名从当前宿主发现和加载，不要求相邻安装目录。每个 Skill 的 `references/`、`scripts/` 和资产从其自身入口目录解析；本 README 的链接仅供浏览源码。

### 测试工作

joy-test 是主栈的测试入口：承接测试策略、test-first、单元/集成/契约与关键 E2E、Web/API/辅助技术目标环境、性质/fuzz/变异、AI/Agent evals 和测试质量治理。按当前风险选择分支，不为普通功能强制全仓审计；joy-build 管产品实现，joy-verify 汇总交付证据，joy-loop 保留同一评审闭环。缺少 joy-test 时仅以现有工具取得当前任务能证明的结果，必要测试门禁未覆盖必须明示，不自动安装或用构建通过冒充测试通过。

该模块于 2026-11-24 从 joyally-test 迁入，安装入口使用 joy-test；原有五份测试参考与来源归属随包保留，不需要另装旧入口。来源和许可见[测试来源复核](skills/engineering/joy-test/references/source-review.md)。

## 工作方式与边界

2026-11-24 的[方法补强与入口收敛](skills/engineering/joy-stack/references/matt-method-completion.md)把双轴评审、可运行诊断、主动领域建模、深模块接口、逻辑/UI 原型、一手研究和架构体检接入既有模块。用户仍直接描述任务：事实研究交 joy-understand，领域/接口/原型交 joy-shape，架构摩擦候选交 joy-govern；视觉与图表由专业 Skill 主导，不要求安装 Matt 原入口或按固定流程全部运行。

- **先确定任务范围。** 当前代码、配置与运行状态是事实来源，历史摘要只作定位线索。其他任务的文件和未提交改动保持原样。
- **按风险选择检查。** 简单修改不强制走完整套流程；实质行为改动按 `joy-loop` 进行独立评审、修正与复验，重要问题未解决时保留阻塞原因。
- **分别报告证据。** 测试、构建、提交、推送、部署和真实业务结果分别确认，前一步成功不代表后一步已完成。
- **在授权内交付。** 平台权限是上限，项目协议与用户当次要求决定具体动作。已授权的自动交付正常推进；安装 Skills 不授予提交、推送、合并、删除或发布权限。

详细输入、输出与交接条件见[套件契约](skills/engineering/joy-stack/references/stack-contract.md)。

## Worktree 管理

`joy-git` 将任务目录的创建、用途登记、状态续接和清理判断放在同一条生命周期中，使用原生 Git 与 Python 3.9+ 标准库，不依赖 Worktrunk。

持久运行数据默认放在**当前运行环境解析出的用户家目录下的 `.joystack`**。家目录由环境决定，不写死账号路径，也不从 cwd 或工作区推断。

```text
~/.joystack/
├── worktrees/
│   └── <repo>-<repository-id>/<task-slug>/
└── state/
    ├── worktrees.json
    └── worktrees.json.lock
```

- 创建计划默认不写入；实际创建时登记任务、会话、基线、目标分支与清理条件。
- 总览覆盖已登记或明确指定的仓库；未知用途、读取失败和未检查的占用分别说明。
- 旧目录与宿主管理的 worktree 不自动搬迁或认领；目录很久未使用只能触发复查。
- 清理计划不删除目录。实际清理前核对成果是否采用、未保存文件、保留原因、会话与进程占用，并取得有效授权。

`JOYSTACK_HOME` 可在明确配置时覆盖数据根目录。受限平台通过 `JOYSTACK_WORKSPACE` 或 `--workspace` 提供允许的路径边界；边界不改变家目录，默认位置不兼容时应报告，而不是静默搬到 cwd。路径检查不代替平台沙箱，也不豁免 Git hooks 等原生副作用。

操作入口见[worktree 生命周期](skills/engineering/joy-git/references/worktrees.md)，目录与平台适配见[全局目录约定](skills/engineering/joy-stack/references/global-home.md)。

## 更新

更新前核对安装来源、项目级或全局范围，以及是否有本地定制。先保存需要保留的修改；不要用更新覆盖来解决冲突，也不要删除 `.joystack` 或旧 worktrees。

### 通过 Skills CLI 安装

在原项目目录更新现有 JoyStack 模块：

```bash
npx skills update -p joy-stack joy-understand joy-shape joy-build \
  joy-test joy-verify joy-debug joy-review joy-loop joy-govern joy-git joy-continue joy-token
```

全局安装使用同一命令，将 `-p` 改为 `-g`。显式列出模块名，避免顺带更新其他套件。命令只更新选定范围内已安装、由 CLI 跟踪的模块；上游新增模块时，重新执行对应范围的 `skills add`，选择完整模块集。具体选项以 [CLI 文档](https://github.com/vercel-labs/skills/blob/main/docs/commands.md)和 `npx skills --help` 为准。

### 从源码 checkout 使用

如果 Skill 入口链接到本地 JoyStack 仓库，在该仓库先检查状态；确认需要保留的修改已妥善保存且 upstream 正确后，再快进更新：

```bash
git status --short --branch
git pull --ff-only
```

存在分叉或冲突时停止处理，不强制覆盖。符号链接指向更新后的源码；若安装方式是复制，还需按原流程将审核后的 Skill 目录同步到安装位置。

### 通过平台文件导入

重新获取已选版本，先备份本地定制，再按平台提供的更新或替换流程导入各 Skill 的完整目录。保留配套引用、脚本、LICENSE 与 NOTICE，不合并来源不明的版本。平台没有更新入口时，不自行卸载旧安装。

更新后核对当前宿主能发现所需模块；是否需重载由宿主决定。Skills 文件更新与 `.joystack` 运行数据分开管理，不自动清理台账、移动目录或重跑历史任务。

## 开发与验证

2026-11-23 从 tstack 局部吸收旧变更语义重审、接手贡献保留、问题优先的 PR/评论、观察门禁分离和有界评审生命周期。均补强已有模块，不新增 Full Send/Stop、可执行 watcher 或强制三供应商 Council。映射、十二个案例与验收边界见[tstack 融合记录](skills/engineering/joy-stack/references/tstack-integration.md)，实施原文见[融合方案](docs/plans/2026-11-23-tstack-integration.md)。静态契约测试不证明真实 PR/MR 或多模型运行成功。

`skills/engineering/` 是模块维护源，`catalog.json` 是目录索引。从仓库根目录执行：

```bash
python3 scripts/validate.py
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 -m unittest discover -s skills/engineering/joy-git/scripts -p 'test_*.py'
```

校验检查模块元数据、目录一致性、配套资源与公开边界；测试覆盖独立挂载与 worktree 管理。受限平台的测试临时目录遵守其工作区约定。

修改能力时同步模块契约、目录索引和两版 README；保留作者元数据、上游归属和许可文件。验证结果仍按实际执行范围报告，不用文档或本机测试冒充目标平台验收。

## 来源与许可

JoyStack 采用 [MIT License](LICENSE)。

- 工程方法参考分别记录：[Matt Pocock Skills](skills/engineering/joy-stack/references/matt-pocock-integration.md)、[Lauren Tan 的 pstack](skills/engineering/joy-stack/references/pstack-integration.md)、[Theo Browne 的 tstack](skills/engineering/joy-stack/references/tstack-integration.md)。每份说明来源、核对版本、实际方法落点、未吸收部分与验证边界；最初版本未记录时如实标明，不将重新核对版本冒充历史。另见[Matt/pstack 当前能力对比](docs/research/2026-11-23-matt-pstack-current-comparison.md)，区分覆盖、缺口与尚未实施的增量建议。
- [oil dev skills](https://github.com/oil-oil/oil-dev-skills) 只作方法来源，不安装、调用或作为可选执行实现；能力由 JoyStack 与宿主工具提供。六类方法、固定版本与归属见[oil 融合记录](skills/engineering/joy-stack/references/oil-dev-integration.md)。完整入口见[融合记录索引](skills/engineering/joy-stack/references/integration-sources.md)。
- `joy-loop` 改编自 [t3dotgg/tstack](https://github.com/t3dotgg/tstack/tree/11e37a74d0a6868c121cd0910ab2b3bd9873b92a) 的 `sol-loop`，保留[上游 MIT 许可](skills/engineering/joy-loop/LICENSE)；原作者与改编范围见 [NOTICE](skills/engineering/joy-loop/NOTICE.md)。
- `joy-token` 参考 [codex-token-skills](https://github.com/lokikill123/codex-token-skills) 并独立表述为模型与宿主无关的通用能力，不绑定 GPT/Sol 或其他供应商；通用节流贯穿各模块，缓存/推理控制/计量按实际接口能力处理。固定版本、可选官方案例与测量边界见[来源记录](skills/engineering/joy-token/references/sources.md)。缓存命中、Token 总量与账单节省分别验收，不承诺未经实测的降幅。

这些来源不是运行依赖，无需安装上游套件即可使用 JoyStack。
