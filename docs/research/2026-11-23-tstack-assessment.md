# tstack 完整评估：哪些能力值得补进 JoyStack

评估日期：2026-11-23。结论状态：评估建议，尚未批准或实施新的能力融合。本次只增加本文，不修改 Skill、运行时、模型路由、安装入口或 Git 权限。

## 结论

**值得局部吸收，不值得整体搬入。** tstack 的优势是把真实 PR 交付经验压缩成可执行约束；JoyStack 已有更广的理解、定形、实现、验证、排障、评审、交付和续接边界。新增收益应落在既有模块的薄弱处，而不是重新创建一套 PR 总控流程。

优先建议四个增量：

1. `modernize` 的语义重审：旧变更是否还值得合入，比 Git 是否冲突更重要。
2. `takeover` 的继承契约与贡献保留：继承的状态和验收必须重新核对，原贡献与接手修正不能混为一谈。
3. PR watcher 的单一所有者、事件去重与终态回查：借鉴协议，但不直接把 `pr-wait` 当合并门禁。
4. `sol-loop` 的 diff 增长复查，以及针对等待生命周期的补强：JoyStack 已有轮次上限，但还缺显式的单轮时间与终止确认协议。

`file-pr` 与 `leaving-pr-comments` 可作为低成本细节补入 Git 交付；`council` 仅适合重大争议的可选交叉复核；`full-send/full-stop` 不建议新增独立入口。模型一致、分数高、CI green、watcher exit 0、PR merged 各有不同含义，不能互相替代。

## 1. 范围、版本与证据等级

| 对象 | 固定版本 | 核对内容 |
| --- | --- | --- |
| t3dotgg/tstack | `11e37a74d0a6868c121cd0910ab2b3bd9873b92a` | README、MIT LICENSE、全部 9 个 Skill、4 份展示 YAML、556 行 `pr-wait` |
| youngjunning/joystack | `8272adcdca3cbc49589361b6b7a4bb235941ddf6` | 入口、10 个组成模块、共享契约、既有融合说明、worktree 脚本与测试 |
| JoyStack 完稿前最新 main | `37a5633aabeef89bebf05bfe7349322921871e74` | 复查新增环境家目录与受限工作区适配；复核对本评估结论的影响 |

tstack 的远端 main 在核对时对应上述提交，提交时间为 2026-11-11；本报告不把 open PR 当当前 main 的功能。仓库有 16 个 tracked 文件，没有随该快照提交的测试目录、CI workflow、依赖锁或多供应商执行器；这不等于作者未手工使用或测试。[T0][T10]

JoyStack 已改编**同一版本** tstack 的 `sol-loop` 为 `joy-loop`，保留上游 MIT LICENSE 与 NOTICE。有限轮数、稳定 finding ID、开放问题复查、超时不算批准、职责拆分已经存在，不能再次计为新增吸收。[J0][J1]

评估开始时 JoyStack checkout 与远端一致。期间另一任务完成了平台路径与执行权限适配，并提交到 `37a5633`。本报告保留初始固定比较基线，并在完稿前复查最新 main：新增的环境家目录、受限路径与安装不扩权规则没有改变旧 PR 语义重审、贡献归属或 watcher 门禁结论；Loop、Review 与 Continue 的正文未变。并行成果不计入本次评估修改。[J2][J3][J6]

证据分层：

1. **当前源码事实**：上述固定版本中的文字、代码和文件清单。
2. **本轮运行证据**：JoyStack 仓库校验通过，worktree 脚本 38 项测试通过；独立后台研究对上游 watcher 做内存编译、隔离 help 和 25 个离线合成断言案例。
3. **本轮推断与建议**：以下增量、优先级、候选接口和验收设计。它们不代表已采用、已提升准确率或已降低交付成本。
4. **未验证**：真实多模型调用、真实 GitHub PR 全生命周期、watcher 实际锁并发、Windows 运行、多轮成本与真实成功率。未安装 tstack，也未执行它的合并、push、评论或设备操作。

## 2. 两套产品的定位差异

| 维度 | tstack | JoyStack | 对融合的影响 |
| --- | --- | --- | --- |
| 主问题 | 把个人常用的 Agent/PR 操作交付到底 | 按任务风险组合通用工程能力 | 不把所有工程任务变成 PR 流程 |
| 入口 | full send、full stop、council、sol loop 等明确口令 | 用户描述目标，按现状自动路由 | 吸收判断标准，而不是要求用户新增口令 |
| 专业边界 | 部分 Skill 组合测试、评审、PR、等待和合并 | Review、Build、Verify、Loop、Git 分工 | 不让 Loop 接管 Git，不创建重复总控 |
| 模型 | Sol 专用 reviewer；Council 三家旗舰 | reviewer 与执行器是可选宿主适配 | 不把可用性、成本和传递代码的授权藏在固定模型要求里 |
| Git 托管 | 具体依赖 GitHub 与 gh | 交付按项目规则和现有平台工具选择 | GitHub watcher 可选，不能让 GitLab/本地交付失能 |
| 验证成熟度 | 工作流文本加一个观察脚本，当前树无测试/CI | 文档契约与 worktree 脚本测试 | 两者都不是普遍成功率的证明，需要真实任务对照 |

这些是产品取舍，不宜简单判成某一套更好。tstack 是个人经验的高密度起点，不是完整 Agent runtime，也不是生产级 PR 执行服务。[T0][J0][J2]

## 3. 全部九个 Skill 的能力映射

| 上游 Skill | 价值与当前覆盖 | 真正值得补的增量 | JoyStack 落点 | 建议 |
| --- | --- | --- | --- | --- |
| `full-send` | 完成、直接证明、评审、PR、等待、合并形成闭环；大部分已有 | 把获准终点表达得更明确；等待不能冒充交付完成 | joy-stack、joy-git、joy-verify | 不新增模块；不复制口令式扩权、强制新分支或强制 PR |
| `full-stop` | ready 与 merged 严格不同；JoyStack 已支持 pr-opened 与 pr-merged | 只准备不合并时，检查现有自动合并是否会突破终点 | joy-git | 吸收终点检查；不默认改团队 auto-merge/merge queue 设置 |
| `sol-loop` | 已改编，3/5 轮、ledger、最小修正均已有 | 每轮前后 diff 规模与必要性核对；等待时限、取消和终止确认 | joy-loop、joy-review | 补强既有模块，不重复迁入或绑定 Sol |
| `council` | 并行独立观点、保留分歧、结果到达即核对 | 对重大争议提供可选多视角复核，评审基线固定 | joy-review、joy-loop | 仅可选；不以三家模型/10 分/全体满意作为默认门禁 |
| `file-pr` | 先查已有 PR；以问题和用户影响开头 | Problem → solution → evidence → limits；提交前隐私审查 | joy-git | 小幅吸收；draft 状态、署名样式跟随仓库规则 |
| `takeover` | 独立验证继承实现，保持原贡献与后续修正 | source/head/base、原目标与后续纠正、贡献归属、期间源 PR 变化 | joy-continue、joy-git、joy-understand | 高优先级；不默认替换 PR 或改原 PR |
| `babysit-pr` | 单 PR 单 watcher、父任务所有权、事件去重、静默等待、重推后重查 | 可恢复事件游标、明确错误/终态、停止时卸载监听、当前 head 门禁回查 | joy-git 的可选平台观察适配 | 高价值协议；脚本不可直接作为合并决策器 |
| `modernize` | 重审意图，不只 rebase；检查 conceptual conflict | KEEP/MODERNIZE、REWORK、SUPERSEDED/CLOSE 建议；前后 range-diff | joy-understand、joy-shape、joy-continue、joy-git | 最高优先级；默认只读判断，改写/关闭仍需授权 |
| `leaving-pr-comments` | 表明 Agent 代用户发言；结论、证据、隐私检查；发成功再 resolve | 标识已核验身份；评论回执与 resolve 顺序 | joy-git | 吸收原则，不强制 emoji/callout 或替用户添加署名 |

来源逐项见 [T1]–[T9]；当前覆盖以 [J1]–[J5] 为准。建议不是新增 9 个模块：第一轮更合理的改动范围是少数 reference、触发指针与行为案例。

## 4. 最有价值的四个增量

### 4.1 旧变更的语义重审，优先于机械 rebase

`modernize` 不只问“代码还能合吗”，还问“问题是否已经解决、旧设计是否被替代、合入是否复活被删除的行为、是否出现两个行为所有者、价值是否仍抵得过维护成本”。判断应先于 rebase/push；`git range-diff` 检查重放后是否丢了原意。[T7]

JoyStack 的 Understand/Continue 已要求历史回查，但未显式给出旧 PR/长期分支的处置分岔。建议给 Continue 一个按需指针，先让 Understand 还原原目标与当前事实，再由 Shape 判断继续、重做或被替代；Git 只执行获准的处置。这也适用于跨轮方案与半成品，不限 GitHub。

建议输入：来源、原目标、最新纠正、base/head、当前未提交范围、基线变化。建议输出：仍有效的目标、概念冲突、处置建议、最小下一步及其授权。不要用年龄或沉没成本决定关闭。

### 4.2 接手是重新承担目标，不是信任交接摘要

`takeover` 保留原 commit 作者、co-author 和源 PR 链接，将继承提交与接手者修正分开；squash 后也保留已核验的人类贡献身份。继承的测试或“完成”摘要仅是线索，要独立验证原问题；工作期间还需回查来源是否变了。[T8]

JoyStack 已有状态回读、脏现场保护和 worktree 台账，但 Continue 没有完整的贡献/接手语义。建议补一个轻量接手契约：继承内容、当前 head、责任转移、原作者、后续修正、验收负责人、未解项。它不需要新的会话数据库、固定新 PR，也不能凭名字猜邮箱。

### 4.3 监听提供新闻，父任务决定是否可合并

上游最值得借鉴的是一条 PR 只有一个主 watcher；reviewer 不监听；无变化不刷“仍在等待”；收到变化先核对，再按当前 head 处理。它有 T3 watch/unwatch 与本地脚本两条适配路径。[T6]

JoyStack 已在 joy-git 规定有界自动门禁守候与合并回读，但未提供事件所有权、游标和平台观察接口。建议先定义协议，再决定要不要实现 GitHub 适配器：

| 观察结果 | 父任务行为 |
| --- | --- |
| 新 finding 或 required CI failure | 按源代码核实，进入现有 Review/Build/Verify，不无限扩大 PR |
| checks 完成、机器人有结果 | 重新读取 head/base、required review、冲突与项目合并要求 |
| ready 候选 | 只是观察结果，不直接授权或执行 merge |
| merged/closed | 独立核对平台终态和目标成果，停止 watcher |
| rate-limited/unavailable/truncated/head-changed | 保持未知/等待，报告恢复条件，不推测 green |
| stop/handoff | 解除本任务监听，保留最小可恢复游标 |

运行数据沿用 JoyStack 全局目录，observer 只读 GitHub，不持有“可以合并”的授权。没有 watcher 的宿主使用现有有界等待；不要仅为套件引入常驻守护服务。[J2][J3]

### 4.4 轮数上限不等于等待时间上限

JoyStack joy-loop 已有默认 3 轮、高风险最多 5 轮，以及超时/失败非批准。但没有显式单轮 elapsed-time 上限、reviewer 打印 verdict 后不结束的处理，以及总时间/调用预算的归属。上游 sol-loop 也有轮数，但 async 结束通知没有 deadline；issue #8 与未合并 PR #9 提供了调查线索，不代表修复已在 main。[J1][T3][U1][U2]

建议保留宿主中立：每轮的时间/调用上限由任务风险和宿主能力给出；超时后检查已有结果，只在结构完整、匹配当前基线且 reviewer 已终止/隔离后接受。无法确认停止时，不创建另一个写入冲突者，也不把超时当批准。

补充 diff-growth 核对：每轮记录行为 diff 与开放 finding，若审查导致新 helper、锁、缓存、选项或不相关测试增长，先核对是否必要；不为迎合 reviewer 把问题做大。不能机械将安全、并发、兼容或低频数据损坏降成 nit，应由真实后果与项目契约判断。[T3][J4]

## 5. 不应原样吸收的部分

### 5.1 口令不自动产生新授权

`full-send` 明确将口令解释为合并、PR 分支 force-with-lease、移除一些 ask-first 测试步骤；它也明确保留系统审批并排除生产变更/删数据。这是作者约定的操作模式，不应泛化成 JoyStack 对所有项目/设备的授权。[T1]

JoyStack 的更合适形态是一个交付终点：留改动、只提交、提交推送、开放 PR、合并 PR。权限来自用户具体请求、项目规则和平台上限，而不是 Skill 安装或英文口令。Full Stop 用作句末强调也触发的设计不宜迁入；既有 auto-merge/queue 的移除可能影响他人协作，需要明确范围。[T2][J2]

### 5.2 不把多模型满意或数字分数当批准

Council 要求三家旗舰模型与高 effort，默认直到全部满意；它禁止同一 checkout 审查时编辑，并要求保留分歧，这是优点。但没有明确总轮数、时间或成本预算，也没有评分校准或证明“三家更准确”的实验。[T4]

可选交叉复核应基于不同问题视角，例如行为契约、安全/迁移、测试盲区；独立证据比提供商数量更重要。保持同一不可变 diff，父任务逐项核实 finding；模型身份、effort、usage 缺失时保持未知。当前宿主未提供三供应商路由，不为研究补建或擅自调用。

### 5.3 不硬编码作者的机器人生态

`pr-wait ready` 依赖 Greptile/Macroscope，CodeRabbit advisory；full-send 与 babysit 对哪些 bot 必须等待的文字也存在粒度差异。项目实际 branch rules、rulesets、required approvals、签名或 merge queue 才是门禁权威，不能默认照搬作者仓库的机器人组合。[T1][T6][T10]

### 5.4 不让最小化原则覆盖真实风险

sol-loop 把其他路径、少见案例、较小成本等默认视作 nit，能降低审查膨胀，但不是通用严重度规则。认证绕过、少见的数据丢失或旧版本兼容仍可能在原目标内阻断交付；JoyStack 当前以触发条件、后果与边界为依据的审查标准应保留。[T3][J4]

## 6. pr-wait 的具体风险与离线证据

**它是观察脚本，不是完整合并控制器。** 为公平起见，`green + BEHIND` 或 `any-change + DIRTY` 的 exit 0 符合各模式语义，不单独认定为 bug；错误是接入方把任何 exit 0 当 merge-safe。[T10]

| 风险 | 当前源码位置 | 本轮离线观察 / 推断 |
| --- | --- | --- |
| 保护规则读取失败与“确实没有规则”混在一起 | `pr-wait:221-245` | 两个读取均 403 后 required 为空，现有 lint pass 可两 poll 后 green；未知不能成为成功 |
| ready 不要求人工 required approvals，也不排除 UNKNOWN/BLOCKED | `pr-wait:395-403,498-513` | 人工 CHANGES_REQUESTED 且无 unresolved，以及 UNKNOWN/BLOCKED 均可 ready/exit 0；应由父门禁补查 |
| gating bot check 结束与 pass 混淆 | `pr-wait:415-435,507-513` | Greptile fail 非 required、lint pass 时仍可能被计为 bot done/ready |
| 稳定快照只比较 check name/bucket，没有绑定 head | `pr-wait:384-387` | head A→B、checks 相同时，B 首 poll 可 ready；需按 head 重置快照并核对 checks 的 commit |
| 评论、review、thread 列表不分页 | `pr-wait:80-105` | last 100、thread comments first 100；未返回 unresolved 可能使 ready 判定漏项，缺失不是无问题 |
| 无 gating bot、无 checks、未出现 required check，缺总等待预算 | `pr-wait:369-380,507-549` | 对应合成输入连续两次 poll 仍 pending、未退出；无总等待期限由静态循环确认，而非实测长期等待 |
| 平台和状态恢复限制 | `pr-wait:49,67-69,264-269` | 无条件 fcntl；状态 6 小时过期后重建 baseline，不是持久无损事件日志 |

后台独立研究做了 25 个内存合成断言，包括正常 ready、保护读取失败与缺失 required check、CHANGES_REQUESTED、head 变化、UNKNOWN/BLOCKED、非 required 的 bot fail、unresolved/BEHIND、green/any-change、CLOSED/MERGED、无 checks/bot、mock lock 和首次失败 baseline。本轮测试夹具未执行真实 gh、模型调用、文件锁或网络；原始 watcher 正常运行会调用 gh。断言通过意味着这些合成路径可复现，不是上游已有 25 项测试，也不是实测生产成功率；没有独立测试 required check fail/cancel 退出分支。

上游 open issue/PR 的证据只用作定位：#8/#9 无界 reviewer 等待、#7 无默认 bot、#11 Windows、#14 首次失败后的 baseline。未合并改动不得计入现有兼容性，贡献者的模型幻觉率或耗时叙述不作为本报告测量结果。[U1]–[U5]

## 7. 许可证、依赖与完整成本

tstack 是 MIT，版权为 Theo Browne。复制或实质改编文本/脚本时保留版权与许可；现有 joy-loop 的 LICENSE/NOTICE 是正确做法。独立用自己的文字实现方法仍应记录可追溯来源。MIT 不证明质量，也不授权上传公司代码、调用模型、修改仓库或对外发言。[T0][J1]

| 候选融合范围 | 引入成本 | 不应隐含的成本/授权 |
| --- | --- | --- |
| 语义重审与接手 reference | 少量文字、触发路由与行为案例 | 不增加服务、账号或固定新模块 |
| PR 文案与评论顺序 | Git 交付规范的小幅补充 | 不绑定 robot emoji、外部署名或非 draft PR |
| watcher 协议 | 接口、游标、预算、终态；实现还需平台适配/测试 | 不能把 Python/gh/机器人预设为所有宿主都有 |
| 多视角 review | 额外模型调用、等待、核实与人工分歧成本 | 不默认三供应商、不假装同模型委托就是三模型 Council |

评估成本应计入成功和失败任务、重试、模型输入输出、reviewer 等待、人工核实、回归与维护时间。没有真实样本前，不给出“减少多少 bug/节省多少时间”的百分比。

## 8. 可选的最小融合方案与验收

以下是下一步候选，不是当前已承诺任务；本轮无行为融合或产品发布。

### 候选 A：纯协议增量，优先

1. Continue/Understand：旧变更的语义处置和接手来源/最新纠正核对。
2. Git：贡献身份、Problem/Solution/Evidence/Limit PR 描述、评论回执后 resolve、只准备不合并终点。
3. Loop：显式等待预算、终止确认和每轮 diff-growth 必要性检查。

沿用现有模块；增加按需 reference 与入口指针，不重复创建 send/stop/modernize/takeover 总控 Skill。每项都要写输入、输出、授权、停止和证据条件，并保留来源/许可证。

### 候选 B：先 watcher 契约，后可选 GitHub 实现

只有真实 PR 守候出现重复漏事件、重复 watcher 或门禁误判，再实现平台适配器。建议响应包含项目/PR、head/base、观察类型、完整性、游标、终态/未知原因与观察时间；不包含 merge 授权。确认 GitLab 和无 watcher 环境仍有明确降级，不新增强制后台服务。

### 候选 C：重大争议才用交叉复核

同一不可变基线，不同评审视角，明确时间与调用预算；APPROVE 取决于可行动 blocker/should 的核实与真实验证，而不是平均分或所有模型口头满意。不存在所需路由时报告不可用，不偷偷替换。

### 验收案例

| 情景 | 应有结果 |
| --- | --- |
| 原问题已被另一实现解决，旧 PR 无冲突 | 建议被替代，而不是机械 rebase 后推进 |
| API/所有权变化，但用户目标仍有效 | 解释 REWORK 范围；不能自动扩大实现或关闭原 PR |
| 接手后用户已有新纠正，源 PR 又前进 | 以最新事实续接，保存原贡献和新修正边界 |
| squash 交付 | 核验作者/co-author，不用模型署名取代人类贡献 |
| reviewer 只输出 verdict 后不结束、无回复或超时 | 按预算终止/确认停止，缺证据则 BLOCKED，不无限挂起或批准 |
| review 修出范围外 helper/缓存/锁 | 解释必要性或撤回新增复杂度，不为讨好 reviewer 扩大范围 |
| 无 review bots / 零 checks / required checks 不可读 | 待定或 unavailable，不能默认 ready |
| head 变化、截断评论、人工 requests changes、队列要求未满足 | 不批准 merge，回查当前 head 的真实门禁 |
| watcher 重启、rate limit、父子任务都尝试监听 | 一个所有者，完整性与恢复明确，不制造重复循环 |
| 用户明确只准备 PR，现有 auto-merge 开启 | 先说明终点冲突，按授权处理，不擅自修改团队设置 |
| 无 GitHub、无多模型/后台能力的宿主 | 普通理解、实现、验证和 Git 交付仍可运行 |

先用合成契约案例做确定性验证，再在获准的真实任务中对照 baseline。测量误触发、漏触发、范围膨胀、未闭环交付、强制权限升级、人工修正、总耗时和总成本；固定样本应覆盖失败与中断，不只展示成功案例。未获得这些证据前，结论最多是“协议已实现”，不是“融合效果已证明”。

## 9. 本轮交付与未完成边界

1. 完整覆盖上游 9 个 Skill、所有依赖文件与一个 watcher；与 JoyStack 固定版本逐项映射，确认已有 sol-loop 改编。
2. 保存本报告；未安装 tstack，未修改 JoyStack 行为，未替用户调用三家模型、创建/监控/合并 PR。
3. 新能力融合尚未执行，因为本轮请求是评估能否吸收。上述方案是待选择建议，不作为未完成实施承诺。
4. 真实 PR、多模型效果、Windows、watcher 并发与预算成本尚未验收。若选择融合，它们成为对应切片的验证条件，而不是本轮评估必须自行启动的外部任务。

## 一手来源

以下源码链接固定 commit；issue/PR 链接只表明 2026-11-23 读取时的讨论，不代表已合入。

| 标识 | 来源 |
| --- | --- |
| T0 | [tstack README](https://github.com/t3dotgg/tstack/blob/11e37a74d0a6868c121cd0910ab2b3bd9873b92a/README.md)、[LICENSE](https://github.com/t3dotgg/tstack/blob/11e37a74d0a6868c121cd0910ab2b3bd9873b92a/LICENSE) |
| T1 | [full-send](https://github.com/t3dotgg/tstack/blob/11e37a74d0a6868c121cd0910ab2b3bd9873b92a/skills/full-send/SKILL.md) |
| T2 | [full-stop](https://github.com/t3dotgg/tstack/blob/11e37a74d0a6868c121cd0910ab2b3bd9873b92a/skills/full-stop/SKILL.md) |
| T3 | [sol-loop](https://github.com/t3dotgg/tstack/blob/11e37a74d0a6868c121cd0910ab2b3bd9873b92a/skills/sol-loop/SKILL.md) |
| T4 | [council](https://github.com/t3dotgg/tstack/blob/11e37a74d0a6868c121cd0910ab2b3bd9873b92a/skills/council/SKILL.md) |
| T5 | [file-pr](https://github.com/t3dotgg/tstack/blob/11e37a74d0a6868c121cd0910ab2b3bd9873b92a/skills/file-pr/SKILL.md) |
| T6 | [babysit-pr](https://github.com/t3dotgg/tstack/blob/11e37a74d0a6868c121cd0910ab2b3bd9873b92a/skills/babysit-pr/SKILL.md) |
| T7 | [modernize](https://github.com/t3dotgg/tstack/blob/11e37a74d0a6868c121cd0910ab2b3bd9873b92a/skills/modernize/SKILL.md) |
| T8 | [takeover](https://github.com/t3dotgg/tstack/blob/11e37a74d0a6868c121cd0910ab2b3bd9873b92a/skills/takeover/SKILL.md) |
| T9 | [leaving-pr-comments](https://github.com/t3dotgg/tstack/blob/11e37a74d0a6868c121cd0910ab2b3bd9873b92a/skills/leaving-pr-comments/SKILL.md) |
| T10 | [pr-wait](https://github.com/t3dotgg/tstack/blob/11e37a74d0a6868c121cd0910ab2b3bd9873b92a/skills/babysit-pr/scripts/pr-wait) |
| J0 | [JoyStack README](https://github.com/youngjunning/joystack/blob/8272adcdca3cbc49589361b6b7a4bb235941ddf6/README.md) |
| J1 | [joy-loop](https://github.com/youngjunning/joystack/blob/8272adcdca3cbc49589361b6b7a4bb235941ddf6/skills/engineering/joy-loop/SKILL.md)、[NOTICE](https://github.com/youngjunning/joystack/blob/8272adcdca3cbc49589361b6b7a4bb235941ddf6/skills/engineering/joy-loop/NOTICE.md) |
| J2 | [joy-git](https://github.com/youngjunning/joystack/blob/8272adcdca3cbc49589361b6b7a4bb235941ddf6/skills/engineering/joy-git/SKILL.md) |
| J3 | [共享契约](https://github.com/youngjunning/joystack/blob/8272adcdca3cbc49589361b6b7a4bb235941ddf6/skills/engineering/joy-stack/references/stack-contract.md) |
| J4 | [joy-review](https://github.com/youngjunning/joystack/blob/8272adcdca3cbc49589361b6b7a4bb235941ddf6/skills/engineering/joy-review/SKILL.md) |
| J5 | [joy-continue](https://github.com/youngjunning/joystack/blob/8272adcdca3cbc49589361b6b7a4bb235941ddf6/skills/engineering/joy-continue/SKILL.md) |
| J6 | [完稿前 main 的平台适配变更](https://github.com/youngjunning/joystack/commit/37a5633aabeef89bebf05bfe7349322921871e74) |
| U1 | [issue #8：async reviewer 等待](https://github.com/t3dotgg/tstack/issues/8) |
| U2 | [open PR #9：有界等待提案](https://github.com/t3dotgg/tstack/pull/9) |
| U3 | [issue #7：无默认 gating bot](https://github.com/t3dotgg/tstack/issues/7) |
| U4 | [open PR #11：Windows watcher](https://github.com/t3dotgg/tstack/pull/11) |
| U5 | [open PR #14：失败 baseline](https://github.com/t3dotgg/tstack/pull/14) |

本轮后台研究的离线案例为本次评估证据，不是上游项目提交的测试；报告中的路径行号来自本轮本地固定快照。本文没有复制上游大段文字或脚本，后续实际改编仍须单独审查许可与 NOTICE。
