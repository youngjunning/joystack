# 来源与能力适配

上游源码首次核对：2026-11-23；通用契约与可选官方案例核对：2026-11-24。核心策略不绑定模型、供应商或宿主；下面的已知案例不是支持白名单，也不是实测节省量。未知供应商照常应用通用节流，只在需要接口级优化时核对对应资料。

## codex-token-skills

- 仓库：[lokikill123/codex-token-skills](https://github.com/lokikill123/codex-token-skills)。原作者身份以仓库维护者为准，不从用户名推断真实姓名。
- 固定核对版本：[f198d5f57bebf7ade10abb3d84a2078eb1d97261](https://github.com/lokikill123/codex-token-skills/tree/f198d5f57bebf7ade10abb3d84a2078eb1d97261)。核对了 [README](https://github.com/lokikill123/codex-token-skills/blob/f198d5f57bebf7ade10abb3d84a2078eb1d97261/README.md)、[token-saver](https://github.com/lokikill123/codex-token-skills/blob/f198d5f57bebf7ade10abb3d84a2078eb1d97261/skills/token-saver/SKILL.md)、[memory](https://github.com/lokikill123/codex-token-skills/blob/f198d5f57bebf7ade10abb3d84a2078eb1d97261/skills/memory/SKILL.md)、两份 UI 元数据与 [MIT LICENSE](https://github.com/lokikill123/codex-token-skills/blob/f198d5f57bebf7ade10abb3d84a2078eb1d97261/LICENSE)。版权行只给出 2026 年，没有署名。
- 只作方法参考：减少重复回复、合并独立请求、复用稳定上下文、用可定位的工件续接；JoyStack 独立表述与限定边界，不安装、调用或复制上游文本、UI 文件、Windows 路径与记忆运行流程。

上游 README 明确面向 DeepSeek V4 Pro，下面做法未吸收：

| 上游做法或主张 | JoyStack 处理 |
| --- | --- |
| 每次只答一句、默认取消进度/计划与验证 | 压缩冗余，但保留用户输出要求和项目验收 |
| 本轮永不重读、Skill 冻结不改 | 以证据是否失效判断刷新，必要规则正常修订 |
| 单 Skill 必然比多个省 Token | 按需加载短入口与当前 references，不加载全部模块 |
| 一个字节变化令整个缓存失效 | 按实际接口的可缓存内容、边界与复用身份检查，不作跨供应商的全有全无判断 |
| 编辑后约 24 小时重建缓存、用首字延迟判命中 | 保留与路由是 provider 机制；以 usage 和官方资料取证 |
| 缓存省 50%+、整体省 60–80% | 缺少可比测量与计费证据，不采用这些比例 |
| 全局记忆 ALWAYS 读写 | 本模块不创建记忆流程；按用户既有授权和续接契约处理 |

## 按能力适配

复用当前任务已有的接口契约和响应，只核对要用的能力；缺失不触发全供应商探测，也不阻断通用策略。

| 能力 | 实施前需要的事实 | 缺失时的处理 |
| --- | --- | --- |
| 缓存 | 是否支持、自动/显式模式、可缓存内容/边界、资源生命周期与计费 | 跳过缓存专属操作，继续减少输入与重复调用 |
| 会话与压缩 | 有状态/无状态、工具结果关联、续接方式、历史改写和 compaction 语义 | 使用必要上下文与获准交接，不假定存在状态 ID 或原生压缩 |
| 推理与输出控制 | 实际支持的参数、约束及推理/输出预算关系 | 保留当前设置，不发送不支持的参数 |
| 计量 | usage 是否暴露、字段口径、输入/缓存/输出/推理的包含或独立关系 | 缺项记未知，不复用其他接口的字段映射 |
| Token 计数 | 与实际模型版本匹配的 Tokenizer、计数接口或 usage | 仅报告明确标记的字节/字符代理，不计算伪 Token |
| 成本 | 当前模型、代理与宿主的输入/输出、缓存读写/存储或本地资源计费 | 无价格/账单证据不声称费用或额度下降 |

仅凭模型名或 OpenAI-compatible 标签不能确定这些事实。供应商、代理、模型或宿主变化时，刷新受影响能力；明确不支持与尚未核验分别记录。

## 可选官方案例

只读取当前接口对应的案例，不把任何一家实现当作通用标准。

- [Codex Skills](https://developers.openai.com/codex/skills)：这是宿主的按需加载案例，不代表所有宿主都以相同方式装载 Skill；按当前宿主机制使用短入口与条件性资料。
- [OpenAI 延迟优化](https://developers.openai.com/api/docs/guides/latency-optimization)：减少输入/输出、减少顺序请求、确定性任务不用模型是不同杠杆；并行主要优化等待，未证明 Token 变少。
- [OpenAI Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)：前缀/查找边界、缓存模式、保留与读写计量的案例；当前文档分别提供 cached_tokens 与 cache_write_tokens，不据此假定其他兼容接口存在相同字段。
- [OpenAI 模型与会话指南](https://developers.openai.com/api/docs/guides/latest-model)：只有使用相应模型/接口时才核对指令位置、历史改写与模型切换的影响；GPT/Sol 是可选案例，不是默认适配目标。
- [Google Gemini 缓存](https://aistudio.google.com/docs/caching)：模型与 API 对隐式/显式缓存的支持条件不同，实施时先确认当前 API，不把一种 API 的缓存资源流程套到另一种。
- [DeepSeek Context Caching](https://api-docs.deepseek.com/guides/kv_cache/)：该接口的 prompt_cache_hit_tokens 与 prompt_cache_miss_tokens 是不同的计量案例，不沿用 OpenAI 的字段路径。

以上资料只是按需导航，未列出的云端/本地模型无需新增供应商专属 Skill 才能使用通用策略。自有 API 实施按当前契约与实际响应；宿主控制的请求、计费或会话遵从既有权限。本文不指定通用模型版本、缓存时长、窗口大小、价格或压缩参数，不因缓存稳定而忽略用户纠正。

## 验证边界

目录/frontmatter/资源/公开边界校验只证明包结构。行为案例用于检视关键决策，工具演练证明相应筛选与退出码保留；通用契约不代表所有模型/宿主都已实测。没有对应模型、接口和质量门槛的真实对照时，不声称自动触发可靠性、缓存命中提升、账单或 Token 降幅已验收。
