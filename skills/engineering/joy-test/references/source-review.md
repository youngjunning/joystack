# AI Native 测试 Skill 来源复核

## 迁入 JoyStack

2026-11-24，测试能力从 [youngjunning/joyally-skills 的固定基线](https://github.com/youngjunning/joyally-skills/tree/64150e7b2a9507a368c4eb72fbf7cc75651c9b0c/skills/engineering/joyally-test) 迁入 JoyStack 并改名为 joy-test。原有策略、方法、目标环境、评测和质量治理正文及下述来源版本保留；本次新增主栈职责交接，不把改名说成重新验证了上游或真实任务效果。

原有质量治理分支参考 [Marcello Curto 的 Test Quality Audit](https://github.com/marcellocurto/skills/tree/main/skills/test-quality-audit) 的审查目标；未复制无许可原文或上游脚本。这里保留来源与下述独立编写、许可边界，独立安装不要求读取仓库外的第三方说明。

## 原始来源核对

本页记录 2026-11-21 读取的 10 个原始 Agent Skill。筛选标准是：源码公开、能由 Coding Agent 直接执行、提供不同于通用“多写测试”的决策机制。融合时只保留机制并重新编写，不复制上游正文、示例或脚本。

| Skill 与原始来源 | 差异化能力 | 可融合机制 |
| --- | --- | --- |
| [test-driven-development](https://github.com/obra/superpowers/blob/22f0b463e7a5e579904dd6211a520321035526f7/skills/test-driven-development/SKILL.md) | 以可观察的正确失败约束 Red-Green-Refactor，而非事后补覆盖率 | 测试先因目标行为缺失而失败；最小实现转绿；重构后复跑；完成前扩大到项目门槛 |
| [webapp-testing](https://github.com/anthropics/skills/blob/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/webapp-testing/SKILL.md) | 把本地服务生命周期与动态页面侦察纳入浏览器测试 | 区分静态页面和动态应用；先等待页面稳定并观察渲染态，再选定位器和执行交互；同时收集页面与控制台证据 |
| [property-based-testing](https://github.com/trailofbits/skills/blob/149d7b21f4067765b82e67029730b42d228ef4b4/plugins/property-based-testing/skills/property-based-testing/SKILL.md) | 从样例枚举升级为对输入域的性质验证 | 只在存在 roundtrip、inverse、oracle、idempotence 或 invariant 等结构时采用；选择最强可证性质；识别同义反复和被过滤为空的性质；新增依赖由用户决定 |
| [mutation-testing](https://github.com/trailofbits/skills/blob/149d7b21f4067765b82e67029730b42d228ef4b4/plugins/mutation-testing/skills/mutation-testing/SKILL.md) | 用人为语义变化验证测试是否真能发现缺陷 | survivor 先区分测试缺口与等价变异；timeout 属于无结论；优先级按被改行为的业务风险，而非变异器自身等级 |
| [coverage-analysis](https://github.com/trailofbits/skills/blob/149d7b21f4067765b82e67029730b42d228ef4b4/plugins/testing-handbook-skills/skills/coverage-analysis/SKILL.md) | 将覆盖率作为 fuzz harness 的可达性诊断，而非质量目标 | 用同工具链和固定 corpus 建可比基线；排除 harness 噪声；把未覆盖区域转成 harness、seed 或 dictionary 动作；覆盖率只证明到达，不证明断言有效 |
| [e2e-testing-patterns](https://github.com/wshobson/agents/blob/42203085cfc5736204bf0f6d436dff7e1da0bf3f/plugins/developer-essentials/skills/e2e-testing-patterns/SKILL.md) | 把 E2E 限定在关键用户旅程和真实集成边界 | 不用 E2E 承担单元规则和边界穷举；测试相互独立并清理数据；使用用户可感知定位与断言；失败时保留 trace、截图和分步证据 |
| [screen-reader-testing](https://github.com/wshobson/agents/blob/42203085cfc5736204bf0f6d436dff7e1da0bf3f/plugins/accessibility-compliance/skills/screen-reader-testing/SKILL.md) | 把真实辅助技术、交互模式和平台组合视为目标环境 | 自动 accessibility 检查不能代替真实屏幕阅读器；覆盖 browse/focus、键盘、焦点恢复、动态公告和错误状态；明确实际执行与未执行的平台矩阵 |
| [api-test-suite-builder](https://github.com/alirezarezvani/claude-skills/blob/5909a72e62b5fbb809935fb6a55b58bdbe175074/engineering/skills/api-test-suite-builder/SKILL.md) | 从路由和协议反推 REST 契约矩阵 | 先盘点 endpoint、method、schema、auth 和状态码；逐接口覆盖 happy path、认证授权、输入边界、错误语义、分页/上传/限流等实际能力；断言响应结构与敏感字段 |
| [agent-regression-evals](https://github.com/alirezarezvani/claude-skills/blob/5909a72e62b5fbb809935fb6a55b58bdbe175074/engineering/skills/agent-regression-evals/SKILL.md) | 面向非确定性 Agent 的重复试验、轨迹约束和统计门槛 | 同一 case 至少重复运行并按 case 聚合；区分 pass@k 与更严格的 pass^k；候选与基线配对比较；关键 case 不隔离；必要时同时检查结果与禁止工具轨迹 |
| [llm-evaluation](https://github.com/wshobson/agents/blob/42203085cfc5736204bf0f6d436dff7e1da0bf3f/plugins/llm-application-dev/skills/llm-evaluation/SKILL.md) | 按生成、分类、检索等任务选择自动指标、人工评审和模型评审 | 先固定任务、基线、样本和评分维度；指标必须匹配目标；难以自动化的质量保留人工校准；LLM-as-judge 不能冒充客观真值 |

## 许可边界

1. `obra/superpowers`、`wshobson/agents` 与 `alirezarezvani/claude-skills` 使用 MIT，见各仓库的 [LICENSE](https://github.com/obra/superpowers/blob/22f0b463e7a5e579904dd6211a520321035526f7/LICENSE)、[LICENSE](https://github.com/wshobson/agents/blob/42203085cfc5736204bf0f6d436dff7e1da0bf3f/LICENSE) 和 [LICENSE](https://github.com/alirezarezvani/claude-skills/blob/5909a72e62b5fbb809935fb6a55b58bdbe175074/LICENSE)。本仓库仅重新表述决策机制；若未来复制实质代码或文本，须保留许可与版权声明。
2. Anthropic `webapp-testing` 使用 Apache-2.0，见技能目录的 [LICENSE.txt](https://github.com/anthropics/skills/blob/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/webapp-testing/LICENSE.txt)。当前不分发其脚本、示例或原文。
3. `trailofbits/skills` 根许可证为 CC BY-SA 4.0，见 [LICENSE](https://github.com/trailofbits/skills/blob/149d7b21f4067765b82e67029730b42d228ef4b4/LICENSE)。为避免把 ShareAlike 义务不清楚地带入 MIT 技能源，只记录事实性能力边界并独立编写，不复制其表达、表格、示例或脚本。

## 融合结论

这 10 个来源共同补齐六条原 Skill 缺少的路径：Red-Green-Refactor；浏览器、E2E 与辅助技术目标环境；API 契约矩阵；性质、变异与覆盖率三类测试强度证据；非确定性 Agent/LLM 的重复评测；以及每种证据的明确边界。`joy-test` 应把它们作为按风险选择的分支，不要求每个任务全部执行。
