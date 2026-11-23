# Matt Pocock Skills、pstack 与 JoyStack：当前能力对比

核对日期：2026-11-23。状态：静态评估完成；增量建议尚未实施。

## 1. 结论

**JoyStack 已具备轻量的理解、定形、纵向构建、排障、独立评审和交付骨架，没必要再安装一整套上游来补齐名称。** Matt 的突出增量是领域语言、深模块/测试 seam 与规格到依赖票据的细化；pstack 的突出增量是检查自身是否有效、性能数字可信度，以及可重复维护的项目验证资产。[M1–M8][P1–P8][J1–J6]

建议先补三个小而可验证的按需协议：**测试对错误行为敏感、性能测量可比、架构边界能具体说明**。项目验证资产维护可列第二批；任务 DAG、竞赛式多模型和形式验证不作为默认工程路径。以下都是本次评估建议，不是已采用决定或运行效果。[M3][M6][P3–P7]

本次只新增报告和来源导航，不修改 JoyStack 运行模块，不安装/更新/移除上游套件，也不将独立安装的专业 Skill 计为 JoyStack 内置能力。企业内部开发与平台适配留在私有扩展，公开报告不包含其协议、地址或安装资料。

## 2. 固定基线与证据口径

| 对象 | 本次核对版本 | 范围与许可 |
| --- | --- | --- |
| Matt Pocock Skills | `abeeaf95660ba9e8b7c753eb38f441ca707a8823` | mattpocock/skills；作者 Matt Pocock；MIT。目录有 20 个 engineering、7 个 productivity、8 个 in-progress、4 个 misc Skill；本次侧重工程主流程与 handoff，不把实验目录当稳定承诺 |
| pstack | `7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9`；plugin 0.15.46 | cursor/plugins 的 pstack 子目录；作者 Lauren Tan（poteto）；该子目录 MIT。58 个 Skill，其中 24 个 principle-*；不是 Matt 或 tstack 的项目 |
| JoyStack | `950183f1fd3af4a45e112c3c608994f382535a7f` | 1 个入口 + 10 个工程模块；这是新增本报告前的 main 基线，不用报告提交反过来证明其运行能力 |

三者均在本次 fetch 后核对本地 HEAD 与 origin/main 一致。pstack 的 SHA 是整个 cursor/plugins 仓库 commit，不能仅从该 commit 的标题推断 pstack 有变化。Skill 数量由固定树中的 SKILL.md 清点，**不是能力数量、执行成功率或评分**。[M0][P0][J0]

历史边界保持原样：JoyStack 初始提交 `cce7d148bd716d40d650010c22f0dea69462b61a` 已提到 Matt/pstack，但没有保存最初上游 SHA 或逐项移植日志。本次版本只作当前对照，不能补造最初参考版本、独占来源或历史因果。已吸收的 tstack 增量也不重新归给 Matt/pstack。[J0][J7]

覆盖标签的含义：

1. **已覆盖**：当前 JoyStack 正文明确承担该行限定的目标和输出；不表示上游完整流程、脚本或所有细节已移植。
2. **部分覆盖**：目标/原则已存在，但缺少该行列明的专门协议、产物或执行路径。
3. **未覆盖**：当前套件未提供该专项能力；可能由另一个已安装 Skill 或项目自身实现，但不计入本套件。

全部覆盖判断都是**源码与契约层**判断。本次未运行上游工作流、真实 Agent 任务、跨模型实验、基准测试或形式证明。

## 3. 能力对照，不按名称凑数量

| 能力与判定范围 | Matt 当前实现 | pstack 当前实现 | JoyStack 当前事实与覆盖判断 |
| --- | --- | --- | --- |
| 任务路由与小能力组合 | ask-matt 给出主流程和独立入口；许多流程手动调用 | poteto-mode 按场景加载原则/工作流，并指定 worker 和宿主工具 | **已覆盖轻量路由**：joy-stack 按主导面选最少模块；不复制上游口令和宿主绑定 [M1][P1][J1] |
| 目标澄清、术语与决定 | grill-with-docs 调用 grilling + domain-modeling；主动挑战术语、维护 glossary/ADR | architect、Model the Domain 强调状态模型与所有者 | **部分覆盖**：Shape 有目标/边界/取舍/验收，但没有主动领域建模完整协议；“读术语”不等于“建模型” [M2][P2][J2] |
| 深模块、caller interface 与可替换 seam | codebase-design 明确 caller 必须知道的全部信息、leverage、locality、seam/adapter | architect 先画两种类型/签名/模块形状，比较单一状态所有者与调用负担 | **部分覆盖**：Shape/Build/Review 会检查新增边界、复用和维护性，但缺少深度、局部性和 seam 选择的具体判断资料 [M3][P2][J2][J3] |
| 规格、纵向拆票与阻塞边 | to-spec 形成规格；to-tickets 明确 blocker 和宽重构例外 | Sequence Verifiable Units；poteto-mode 的多阶段 playbook | **部分覆盖**：Shape 输出任务契约，Build 做纵向切片；没有内置建票、阻塞边和 tracker 生命周期 [M4][P9][J2] |
| 最小切片的实现反馈 | implement 调用 tdd、局部检查、收尾 review | poteto-mode、Sequence Verifiable Units | **已覆盖限定目标**：Build 每切片反馈，Verify 区分快检与收尾门禁；不是 implement 的强制提交/固定 TDD 副本 [M5][P9][J2][J4] |
| 专项 TDD 与测试有效性 | tdd 明确先确认 seam、red→green、反对同构期望值和批量先写测试 | Test Behavior 以“破坏行为/仅改内部”两种编辑判断测试 | **部分覆盖**：Build 已有适用时测试先行、反实现细节原则，Debug 要失败复现；没有完整 seam 选择及双向敏感性规则 [M6][P3][J2][J5] |
| 可证伪的根因诊断 | diagnosing-bugs 提供测试、HTTP、重放、fuzz、bisect、差分、HITL 等反馈手段 | Fix Root Causes、Attack the Premise；失败多次后直接检验共同前提 | **已覆盖核心诊断**：Debug 先失败事实、缩边界、反驳假设、定位源头和回归；上游手段全集和“共同前提”显式门槛没有整体迁入 [M7][P10][J5] |
| 原目标 + 系统契约的独立评审 | code-review 的 Standards + Spec 双轴，固定点与分开的 reviewer | interrogate 用实际运行保留对抗性 finding，不执行修复 | **已覆盖双轴与独立性**：Review/Loop 有固定范围、分级 finding、作者核实和复验；不要求每条维护性 finding 都能动态复现 [M8][P11][J3][J6] |
| 直接观察真实产物，区分验收层级 | diagnosing-bugs/tdd 等具体任务检查 | Prove It Works 明确拒绝编译、自报、缓存等代理 | **已覆盖证据原则**：Verify 分静态/测试/构建/部署/目标环境/业务；没有实际后层证据不报成功 [M6][P4][J4] |
| 性能数字的可比性与噪声 | 本次所读工程主流程没有专项测量清单；不是断言全仓不存在 | benchmark-checklist + Explain the Number：限速因素、调优、公平条件、错误/实际工作量、重复与端到端相关性 | **未覆盖专项协议**：Verify 要证据、Debug 处理性能异常，但没有 benchmark 比较和 inconclusive 判定流程 [P5][J4][J5] |
| 可复用项目验证入口与保鲜 | retro 提议改善已有环境、检查和工具 | create/maintain-verification-skill：launch/doctor/drive/evidence/cleanup、feature map、源代码与一次真实驱动回查 | **部分覆盖**：Verify 有任务证明、Govern 有入口/CI 保鲜；没有生成并维护项目 verify Skill/feature map 的完整生命周期 [M9][P6][J4][J8] |
| 形式验证与模型漂移维护 | 不在本次所读主流程的专项承诺中 | create/maintain-formal-verification-skill：选择性质/工具、声明边界、破坏变体、反例回放、sync commit | **未覆盖专项能力**：普通测试、状态模型或“关键不变量”表述不等于模型检查或形式证明 [P7][J4] |
| 不重叠工作的并行与隔离 | implement-spec 用独立 worktree、稀疏上下文与汇合 | swarm 按 slice/race 分配输出；Separate Before Serializing Shared State | **部分覆盖**：Understand/Build 有非重叠并行契约，Git 有 worktree 台账与隔离；没有完整 swarm 执行/汇总器 [M10][P8][J2][J9] |
| 多票据 DAG 的 frontier 调度 | implement-spec 从 blocking edges 启动 ready frontier 并合到 integration branch | swarm 负责有界 fan-out，不应仅凭它认定实现相同 tracker DAG | **未覆盖调度器**：Build 的“可以并行”和 worktree 脚本不等于依赖图调度、票据完成回查或集成调度 [M10][P8][J2][J9] |
| 多方案竞赛与结果合成 | ask-matt/prototype 可通过试验收敛设计问题 | arena 定评分标准、并行候选、跨供应商 judge、选基底/graft/复验 | **未覆盖完整竞赛工作流**：Review 的可选多视角不是 arena；Shape 的最小试验判断不是多候选合成器 [M1][M11][P12][J2][J3] |
| 上下文卫生与跨轮续接 | handoff 引用已有 artifact；ask-matt 指定阶段边界与新 context | Guard the Context Window、ketchup、worker 上下文约定 | **部分覆盖**：Understand 局部阅读、Continue 最小摘要与实时回查；没有统一 context 容量阈值/自动清空或跨宿主持久记忆服务 [M1][M12][P1][P13][J5][J10] |
| 经验转成结构性保护 | retro 将机械错误变检查，判断留 standards，回查既有门禁是否接线 | Encode Lessons、correct 将错误类别先架构/类型/lint/test、文字最后 | **部分覆盖**：Govern/Review 已优先确定性检查，但未提供“历史错误→执行保护→故意破坏证明保护有效”的完整台账 [M9][P14][J3][J8] |
| Git、旧工作重审、授权与门禁 | implement 有 commit；handoff 给出处；专项 pr 需另读 | poteto-mode shipping/babysit 有宿主/模型依赖与独立自治约定 | **已覆盖 JoyStack 自身的交付契约**：Git/Continue/Loop 有当前事实、继承贡献、有界门禁与回读；部分细化来自已有 tstack 适配，不证明上游 shipping 全套可跑 [M5][M12][P1][J6][J7][J9][J10] |

## 4. 值得继续吸收的增量

### 第一批：补强既有模块，不加新入口

| 优先级 | 建议落点与最小改动 | 为什么现有正文还不够 | 未来实施的验收条件 |
| --- | --- | --- | --- |
| P1 | Build/Verify 按需测试质量 reference：期望值来源、错误行为会失败、纯内部重构不会误报 | “不测试内部细节”仍挡不住同构期望值、宽断言、未发生的副作用；Debug 的失败复现只覆盖诊断分支 | 用同一示例分别观察正确实现 PASS、错误值/遗漏或重复副作用 FAIL、等价内部重构 PASS；测试能力不足如实标未知 |
| P1 | Verify 的性能比较 reference，Debug 指向它；固定 claim、版本、数据/配置、运行方法、错误和有效工作量 | “有数值”与“能做选型/性能结论”不同；现有分层证据没有测量公平性门禁 | 对不同配置、错误快速返回、未执行工作、差异小于波动四类案例拒绝赢家结论；公平 A/B 报单位/样本量/中位数/范围/瓶颈及端到端意义 |
| P1 | Shape/Review 的架构 seam reference：从调用者所需知识、状态唯一所有者和可替换性判断 | 只有“复用”“维护成本”可能落成泛泛评价；不宜要求所有任务先建 glossary 或多模型设计 | 单点改动不读大流程；跨边界例子能说清为什么旧接口不够、新接口缩小何种调用负担、哪些 seam 值得测、复用现有领域词 |
| P2 | Govern 的重复问题→保护机制短表，并与 Build/Verify 交接 | 已建议确定性检查，但容易只新增规则文字或未接入 CI 的孤儿测试 | 每条已实施保护对应真实错误、检查位置/CI入口和失败变体；判断类建议仍只记录，不捏造自动保护 |

上述建议依据 [M3][M6][M9][P2–P5][P14]。都是按需材料，不把内容塞进所有常驻 description。P1 的顺序是本次维护成本与风险判断，**不是 benchmark 已证明的收益**。

### 第二批：有真实目标才做的项目能力

1. **项目验证资产维护。** 优先复用该项目现有测试/driver；需要时形成可复跑入口和 feature→check→evidence 映射，记录基线、启动/清理所有权和证据保留位置。源代码变化后先判断检查是否漂移，再决定是改验证还是报告真实 bug。只有完整跑过才能把“生成说明”升级为可交付验证资产；不创建所有仓库都要装的额外插件。[P6][P7]
2. **依赖票据与调度。** 多会话建设确实受阻时才设计 tracker-neutral 的 ticket/blocker/frontier/integration 契约，再适配项目 tracker 和当前宿主。需要验证并发写隔离、取消/失败、依赖变化、集成冲突、门禁及关闭票据授权。没有这些证据不把普通 fan-out 宣称 DAG 能力。[M4][M10][P8]
3. **形式验证。** 只针对高代价而测试难覆盖的竞态、重试或状态不变量。先列模型→源码对应、边界/假设、工具成本、反例和漂移基线；验证过一个性质不等于证明整个服务。不默认给普通 CRUD 上 TLA+/证明工具，也不将生成输入的测试伪称形式证明。[P7]
4. **多方案探索。** 只有难以口头决定且后果足够大的架构问题，才考虑少量可比较原型；保持单一最终设计和来源记录。多供应商调用、固定 runner/model、评分或全部模型满意不成为套件通行门禁。[M11][P12][J3]

## 5. 不能直接融合的默认值与冲突

| 上游细节 | 本项目取舍 |
| --- | --- |
| Matt tdd 每次先确认 seam、refactor 移至 review | 可借鉴 seam 和测试判断；沿用项目/用户已有确认，不为每个小切片重复质询，不改变当前工程阶段所有权 [M6][J2] |
| Matt 宽重构采用 expand–contract；pstack 在受控迁移中允许阶段内暂时破坏 | 先查外部兼容承诺、可逆性和真实集成门禁。pstack “迁 callers 后删旧 API”明确限于无外部用户依赖且能协同破坏性变更，不能当公开 API/数据迁移通则 [M4][P15][J2] |
| Matt 固定 idea→spec→tickets、手动清 context、完整用户故事；pstack 固定 worker/model/rule 文件和 Cursor 功能 | 保留轻量自动组合和宿主权限上限；不复制安装布局、清空上下文命令、tracker、模型 slug、自动登录或产品私有工具 [M1][M10][P1][J1] |
| pstack interrogate 只保留运行证明的 finding | 可以作为专项对抗验证，不代替 Review 的契约、维护性和低频高损失风险审查；无法动态重现不代表风险不存在 [P11][J3] |
| pstack 自治规则允许部分外部可逆动作直接推进，commit/review 有 deslop/no-comments 依赖 | 项目和用户决定实际授权；不通过上游自治扩大消息、发布或删除权限，不默认删注释或增加插件依赖 [P1][J0][J1] |
| 上游含个人风格、写作、教学、bot UI、安装和实验 Skills | 不强行纳入工程底座；另行专业需求另行评估。目录出现不等于当前可调用或值得默认采用 [M0][P0] |

oil dev skills 继续仅作方法来源：**不安装、不调用，也不作为可选执行实现或缺失能力的降级依赖**。Matt/pstack 本轮也不是运行依赖；独立使用已安装专业 Skill 是另外的动作，不证明本套件已实现其全部能力。[J7]

## 6. 核对范围、复查与未验证项

本次实际重点读取：Matt 的 ask-matt、grill-with-docs、domain-modeling、codebase-design、to-spec、to-tickets、implement、implement-spec、tdd、diagnosing-bugs、code-review、prototype、retro、handoff；pstack 的 poteto-mode、architect、swarm、arena、interrogate、benchmark-checklist、验证/形式验证创建与维护入口，及表中涉及的原则。其余目录通过清点、README 或 description 判范围，不冒充对每个脚本和每条 playbook 都做了全审。

JoyStack 读取了上述 11 个入口、共同契约，以及已落地的继承/评审生命周期/PR交付/观察/worktree 边界。报告按文件正文和明确责任判断，未以相似名字或初次提交记录代替当前能力证据。

复查办法：分别 fetch 对应来源，记录准确 commit；核对固定链接的文件/行范围；先重读相关分支而非自动拉上游覆盖本地；新增采用决定时更新原融合记录，并把实施和验收与本报告的静态建议分开。原始 SHA 缺失说明永久保留，不能靠下次升级消除。[J7]

本轮已通过 24 项仓库契约测试、公开边界/目录/链接校验、Skill schema 校验及固定源码链接的文件/commit/行范围检查。它们只防止记录或路径失真，不能证明 Agent 触发、任务成功、模型优劣、成本下降或开发加速；这些需要另行授权并在真实任务中测量。未新建票据、发布上游插件、部署或更新用户安装。

## 7. 固定版本来源

以下为一手源码定位；区间键用于正文简写。报告独立归纳，不复制上游长文本或脚本。未来实质改编另保留其版权、许可与必要 NOTICE。

### Matt Pocock Skills

- [M0 README](https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/README.md)、[M0 LICENSE](https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/LICENSE)
- [M1 ask-matt](https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/skills/engineering/ask-matt/SKILL.md#L15-L40)
- [M2 domain-modeling](https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/skills/engineering/domain-modeling/SKILL.md#L6-L40)、[M2 grill-with-docs](https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/skills/engineering/grill-with-docs/SKILL.md)
- [M3 codebase-design](https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/skills/engineering/codebase-design/SKILL.md#L6-L28)
- [M4 to-spec](https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/skills/engineering/to-spec/SKILL.md)、[M4 to-tickets](https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/skills/engineering/to-tickets/SKILL.md#L25-L60)
- [M5 implement](https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/skills/engineering/implement/SKILL.md)
- [M6 tdd](https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/skills/engineering/tdd/SKILL.md#L12-L38)
- [M7 diagnosing-bugs](https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/skills/engineering/diagnosing-bugs/SKILL.md)
- [M8 code-review](https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/skills/engineering/code-review/SKILL.md)
- [M9 retro](https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/skills/engineering/retro/SKILL.md)
- [M10 implement-spec](https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/skills/engineering/implement-spec/SKILL.md#L11-L42)
- [M11 prototype](https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/skills/engineering/prototype/SKILL.md)
- [M12 handoff](https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/skills/productivity/handoff/SKILL.md)

### pstack

- [P0 README](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/README.md)、[P0 plugin.json](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/plugin.json)、[P0 LICENSE](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/LICENSE)
- [P1 poteto-mode](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/poteto-mode/SKILL.md)
- [P2 architect](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/architect/SKILL.md)、[P2 Model the Domain](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-model-the-domain/SKILL.md)
- [P3 Test Behavior](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-test-behavior-not-implementation/SKILL.md#L9-L16)
- [P4 Prove It Works](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-prove-it-works/SKILL.md)
- [P5 benchmark-checklist](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/benchmark-checklist/SKILL.md#L13-L34)、[P5 Explain the Number](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-explain-the-number/SKILL.md)
- [P6 create-verification-skill](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/create-verification-skill/SKILL.md)、[P6 maintain-verification-skill](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/maintain-verification-skill/SKILL.md)
- [P7 create-formal-verification-skill](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/create-formal-verification-skill/SKILL.md#L17-L39)、[P7 maintain-formal-verification-skill](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/maintain-formal-verification-skill/SKILL.md)
- [P8 swarm](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/swarm/SKILL.md)、[P8 Separate Shared State](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-separate-before-serializing-shared-state/SKILL.md)
- [P9 Sequence Verifiable Units](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-sequence-verifiable-units/SKILL.md)
- [P10 Attack the Premise](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-attack-the-premise/SKILL.md)、[P10 Fix Root Causes](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-fix-root-causes/SKILL.md)
- [P11 interrogate](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/interrogate/SKILL.md)
- [P12 arena](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/arena/SKILL.md)
- [P13 Guard the Context Window](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-guard-the-context-window/SKILL.md)
- [P14 Encode Lessons](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-encode-lessons-in-structure/SKILL.md)、[P14 correct](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/correct/SKILL.md)
- [P15 Outcome-Oriented Execution](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-outcome-oriented-execution/SKILL.md)、[P15 Migrate Callers](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.md)

### JoyStack 当前基线

- [J0 初始提交](https://github.com/youngjunning/joystack/commit/cce7d148bd716d40d650010c22f0dea69462b61a)、[J0 AGENTS](https://github.com/youngjunning/joystack/blob/950183f1fd3af4a45e112c3c608994f382535a7f/AGENTS.md)
- [J1 joy-stack](https://github.com/youngjunning/joystack/blob/950183f1fd3af4a45e112c3c608994f382535a7f/skills/engineering/joy-stack/SKILL.md)、[J1 套件契约](https://github.com/youngjunning/joystack/blob/950183f1fd3af4a45e112c3c608994f382535a7f/skills/engineering/joy-stack/references/stack-contract.md)
- [J2 Shape](https://github.com/youngjunning/joystack/blob/950183f1fd3af4a45e112c3c608994f382535a7f/skills/engineering/joy-shape/SKILL.md)、[J2 Build](https://github.com/youngjunning/joystack/blob/950183f1fd3af4a45e112c3c608994f382535a7f/skills/engineering/joy-build/SKILL.md)
- [J3 Review](https://github.com/youngjunning/joystack/blob/950183f1fd3af4a45e112c3c608994f382535a7f/skills/engineering/joy-review/SKILL.md)
- [J4 Verify](https://github.com/youngjunning/joystack/blob/950183f1fd3af4a45e112c3c608994f382535a7f/skills/engineering/joy-verify/SKILL.md)
- [J5 Debug](https://github.com/youngjunning/joystack/blob/950183f1fd3af4a45e112c3c608994f382535a7f/skills/engineering/joy-debug/SKILL.md)、[J5 Understand](https://github.com/youngjunning/joystack/blob/950183f1fd3af4a45e112c3c608994f382535a7f/skills/engineering/joy-understand/SKILL.md)
- [J6 Loop](https://github.com/youngjunning/joystack/blob/950183f1fd3af4a45e112c3c608994f382535a7f/skills/engineering/joy-loop/SKILL.md)、[J6 评审生命周期](https://github.com/youngjunning/joystack/blob/950183f1fd3af4a45e112c3c608994f382535a7f/skills/engineering/joy-loop/references/review-lifecycle.md)
- [J7 融合索引](https://github.com/youngjunning/joystack/blob/950183f1fd3af4a45e112c3c608994f382535a7f/skills/engineering/joy-stack/references/integration-sources.md)、[J7 tstack 记录](https://github.com/youngjunning/joystack/blob/950183f1fd3af4a45e112c3c608994f382535a7f/skills/engineering/joy-stack/references/tstack-integration.md)、[J7 oil 边界](https://github.com/youngjunning/joystack/blob/950183f1fd3af4a45e112c3c608994f382535a7f/skills/engineering/joy-stack/references/oil-dev-integration.md)
- [J8 Govern](https://github.com/youngjunning/joystack/blob/950183f1fd3af4a45e112c3c608994f382535a7f/skills/engineering/joy-govern/SKILL.md)
- [J9 Git](https://github.com/youngjunning/joystack/blob/950183f1fd3af4a45e112c3c608994f382535a7f/skills/engineering/joy-git/SKILL.md)、[J9 worktrees](https://github.com/youngjunning/joystack/blob/950183f1fd3af4a45e112c3c608994f382535a7f/skills/engineering/joy-git/references/worktrees.md)、[J9 PR 交付](https://github.com/youngjunning/joystack/blob/950183f1fd3af4a45e112c3c608994f382535a7f/skills/engineering/joy-git/references/pr-delivery.md)
- [J10 Continue](https://github.com/youngjunning/joystack/blob/950183f1fd3af4a45e112c3c608994f382535a7f/skills/engineering/joy-continue/SKILL.md)、[J10 继承工作](https://github.com/youngjunning/joystack/blob/950183f1fd3af4a45e112c3c608994f382535a7f/skills/engineering/joy-continue/references/inherited-work.md)
