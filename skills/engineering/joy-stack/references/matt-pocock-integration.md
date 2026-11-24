# Matt Pocock Skills 融合记录

后续核对见[2026-11-23 当前能力对比](https://github.com/youngjunning/joystack/blob/main/docs/research/2026-11-23-matt-pstack-current-comparison.md)：以 JoyStack `950183f1fd3af4a45e112c3c608994f382535a7f` 和下述上游快照分析当前差异，保留最初参考版本未知的事实；建议与实际采用分别记录。链接用于报告导航，不作为漂移版本的能力证据。

## 来源与核对范围

来源为 Matt Pocock 的 [mattpocock/skills](https://github.com/mattpocock/skills)，MIT / Copyright 2026 Matt Pocock。本次核对日期为 2026-11-23，上游固定快照为 `abeeaf95660ba9e8b7c753eb38f441ca707a8823`，主要读取 README、engineering 目录的相关 Skill、productivity/handoff 和 LICENSE。源码链接均固定该快照，不使用漂移的 main 作为本记录证据。

JoyStack 首次提交 [cce7d14](https://github.com/youngjunning/joystack/commit/cce7d148bd716d40d650010c22f0dea69462b61a) 于 2026-11-20 已注明 Matt Skills 是工程思想参考，包含独立的 Shape、Build、Verify、Debug、Review、Continue 等模块；**未记录当时读取的上游 SHA，也没有逐项移植日志**。本次版本是重新核对版本，不冒充最初参考版本。当前方法落点按 JoyStack `a7e74279fcb03933d026778366922827a30d72eb` 回查。

## 方法、落点与差异

下表记录已在 JoyStack 契约中体现的方法和保留差异，不声称每项只来自 Matt，也不声称本轮新增了这些运行能力。

| 来源方法 | JoyStack 落点 | 当前已体现的规则 | 未整体引入的部分 |
| --- | --- | --- | --- |
| README、ask-matt：小而可组合的工程能力、按情景选路 | joy-stack、共享套件契约 | 按未知、目标、实现、验证、排障与续接组合最少模块；简单任务不走全套 | ask-matt 手动口令、完整 idea→ship 主流程、每次强制质询 |
| grill-with-docs、domain-modeling：先收敛概念与决定 | joy-shape | 核对目标、边界、术语与验收；复用项目 GLOSSARY/ADR，不明确的决定先收敛 | 固定文档布局、每个任务强制建 glossary/ADR 或复制领域建模全集 |
| codebase-design：深模块与可替换 seam | joy-review、joy-shape | 检查复用基建、公共边界、调用复杂度与维护成本；领域架构由相应专业 Skill 主导 | 专用词汇/深模块设计工具全集；不能把语义对应说成完整实现 codebase-design |
| tdd：行为接口与 red-green 反馈 | joy-build、joy-verify | 每个纵向切片取得可观察反馈；测试先行适合时采用，定向验证而非凑覆盖率 | 所有任务强制 TDD、上游测试模板/配套参考全文；无行为文案不额外补测试 |
| diagnosing-bugs：复现、假设与证据迭代 | joy-debug | 建立可重复失败、验证/反驳假设、定位坏状态源头，再取得回归证据 | 上游诊断流程的阶段细节、独有工具与默认参数；当前模块不是该 Skill 副本 |
| code-review：Standards 与 Spec 双轴 | joy-review | 分开核对原目标是否实现、现有契约和维护性是否破坏；不把偏好当阻断项 | 原仓库的 standards 文件体系、tracker 与 review 工具约定 |
| prototype：用可运行的试验回答一个不确定问题 | joy-shape 的取舍与验证选择 | 根据目标/成本/不可逆性收敛最小结果；需要原型时由已有专业能力承接 | JoyStack 不内置完整 prototype 流程，也不默认保存临时分支或搭原型应用 |
| handoff：压缩状态、引用已有成果、去除敏感信息 | joy-continue | 保留下一位执行者需要的当前结果、决定、证据、位置、未解项和恢复条件；历史摘要回查当前事实 | 自动写入 OS 临时目录、强制推荐 Skills 段、完整会话或长期记忆写入 |

实际模块文件在各自的安装目录；跨 Skill 按名称发现，不从本记录拼兄弟路径。以上方法可能与 pstack、oil dev skills、tstack 及一般工程实践交叉；本表不建立独占作者、全部采用或性能提升的结论。

## 依赖、归属与验证边界

2026-11-24，测试专项已从独立的 joyally-test 迁入主栈 joy-test：TDD 红绿反馈、独立 oracle、测试层级与质量、目标环境和 Agent evals 现在由主栈模块承接，不要求另装旧测试 Skill。上述历史表保留当时核对范围；当前测试的完整来源、未复制部分和许可见 [joy-test 来源复核](https://github.com/youngjunning/joystack/blob/main/skills/engineering/joy-test/references/source-review.md)。这次迁移不表示 Matt 的每项默认值已原样采用，也不证明其他评审或诊断缺口已补齐。

JoyStack 不依赖安装 Matt Skills，也不把其插件、tracker、运行时、模型配置或脚本作为基础能力前提。本轮只补来源记录和导航，不安装、更新或移除用户已有 Matt Skills；用户在其它任务主动使用它们，与 JoyStack 的基础能力是否依赖它们是两个问题。

本记录使用独立表述及短方法定位，未复制上游正文或脚本；未来实质复制仍需保留 MIT 与版权声明。Matt 是原方法资料的作者，JoyStack 的适配和取舍归本项目维护者；保存或安装不证明掌握、实践或本人参与上游开发。

本次可核验：上游固定文件存在、来源/许可、JoyStack 初始历史与当前契约、映射和相对导航。文档/契约测试仅能防止链接或记录丢失，**不能证明逐条原始因果、真实 Agent 触发、任务成功率或质量提升**。本轮没有新增功能或真实平台操作。

## 固定版本一手资料

- [README](https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/README.md)、[LICENSE](https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/LICENSE)
- [ask-matt](https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/skills/engineering/ask-matt/SKILL.md)
- [grill-with-docs](https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/skills/engineering/grill-with-docs/SKILL.md)、[domain-modeling](https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/skills/engineering/domain-modeling/SKILL.md)
- [codebase-design](https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/skills/engineering/codebase-design/SKILL.md)、[tdd](https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/skills/engineering/tdd/SKILL.md)
- [diagnosing-bugs](https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/skills/engineering/diagnosing-bugs/SKILL.md)、[code-review](https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/skills/engineering/code-review/SKILL.md)
- [prototype](https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/skills/engineering/prototype/SKILL.md)、[handoff](https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/skills/productivity/handoff/SKILL.md)
