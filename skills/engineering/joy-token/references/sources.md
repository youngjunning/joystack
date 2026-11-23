# 来源与 GPT/Sol 适配

核对日期：2026-11-23。以下是方法来源与当时的官方机制，不是实测节省量；模型、请求顺序、缓存和价格有变化时重新核对相应官方资料。

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
| 一个字节变化令整个缓存失效 | 在实际 Token/消息边界检查可复用前缀，不作全有全无判断 |
| 编辑后约 24 小时重建缓存、用首字延迟判命中 | 保留与路由是 provider 机制；以 usage 和官方资料取证 |
| 缓存省 50%+、整体省 60–80% | 缺少可比测量与计费证据，不采用这些比例 |
| 全局记忆 ALWAYS 读写 | 本模块不创建记忆流程；按用户既有授权和续接契约处理 |

## 官方依据

- [Codex Skills](https://developers.openai.com/codex/skills)：名称与 description 用于发现，完整 SKILL.md 在选用时加载。入口与条件性资料分离，不能将安装全部模块等同于每轮加载全部正文。
- [OpenAI 延迟优化](https://developers.openai.com/api/docs/guides/latency-optimization)：减少输入/输出、减少顺序请求、确定性任务不用模型是不同杠杆；并行主要优化等待，未证明 Token 变少。
- [OpenAI Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)：匹配符合资格的前缀与缓存查找边界，不要求全请求一致。保留期限、显式/隐式模式、缓存写入费率与读取使用量按模型和接口核对；不用上游 DeepSeek 经验补齐 GPT 数据。
- [GPT 最新模型使用指南](https://developers.openai.com/api/docs/guides/latest-model)：本次页面包含 GPT-6.2 Sol，说明 GPT-6.2 会在历史前缀修改、某些模型变化等情况下丢弃 reasoning items；还说明顶层 instructions 的位置发生变化。它支持保留有效前缀的方向，不证明任一宿主展示的 Sol 路由具有同样请求实现。

GPT/Sol 不是跨宿主通用配置键。自有 API 实施按当前官方文档、实际请求和 usage；Codex/其他宿主保持既有权限与能力。本文不指定模型版本、缓存时长、窗口大小、价格或压缩参数，不因缓存稳定而忽略用户纠正。

## 验证边界

目录/frontmatter/资源/公开边界校验只证明包结构。行为案例用于检视关键决策，工具演练证明相应筛选与退出码保留；没有真实 GPT Sol 对照运行时，不声称自动触发可靠性、缓存命中提升、账单或 Token 降幅已验收。
