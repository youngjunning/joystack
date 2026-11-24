# Matt 方法补强与入口收敛

2026-11-24，对照 Matt Pocock 的 [固定源码](https://github.com/mattpocock/skills/tree/abeeaf95660ba9e8b7c753eb38f441ca707a8823) 与本次移除前的已安装文本，把仍有价值的方法独立编写为现有模块的按需分支。上游按 MIT 归属 Matt Pocock，见[许可证](https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/LICENSE)；这里不复制其正文、HTML scaffold 或脚本，不重建未知的最初采用版本。

## 当前落点

| 原入口/资料 | 现有主栈模块与方法 | 本次保留与取舍 |
| --- | --- | --- |
| code-review | joy-review 的 review-axes.md | 比较对象与工作区、规格定位、Standards/Spec 独立结论和 12 类维护性线索；不强制两名 reviewer，不覆盖项目标准 |
| diagnosing-bugs | joy-debug 的 diagnosis-loop.md | 红灯反馈、缩小、竞争假设、实验、性能证据、原场景回验和临时资源清理；不带上游 HITL runner、无限重试或线上授权 |
| tdd | joy-test 的 test-methods.md 与主栈入口 | 已迁入的测试 seam、独立 oracle、有效 Red/Green 和保护质量；不照搬每次强制询问或禁止所有 refactor 的默认值 |
| domain-modeling、grill-with-docs | joy-shape 的 domain-modeling.md | 主动校准术语、场景、代码差异，lazy glossary/ADR 与上下文映射；按项目格式和写入权限，不为小事开完整质询会 |
| codebase-design | joy-shape 的 module-design.md | caller 全部约定、深度/locality、seam、依赖类别、adapter、方案比较和保护迁移；不强制词汇替换、多模型或删除内部测试 |
| prototype | joy-shape 的 prototypes.md | 逻辑/UI 分支、状态可见、可操作场景、原页面同内容 variant、键盘、生产隔离与结果留存；UI 交设计专业能力，不削减用户视觉与交互要求 |
| research | joy-understand 的 primary-research.md | 问题到一手证据、固定版本、逐项归属、失败边界与需要时的仓库研究；不默认后台 Agent 或记忆写入 |
| improve-codebase-architecture | joy-govern 的 architecture-audit.md → joy-shape | 范围/热点、真实摩擦、候选 before/after、实际收益/风险、选择后再设计；HTML/图表交专业能力，不默认 CDN 或全仓改造 |

本记录只作来源与能力导航。调用时按名称发现对应模块，从其实际目录读取上述参考，不要求模块相邻，不从此表拼装宿主路径。

## 删除范围不是“全部融合”

本次可移除的独立全局入口是 codebase-design、domain-modeling、prototype、research、improve-codebase-architecture、grill-with-docs。其常用有价值分支已接入上述所有者，原宿主绑定和过度固定的默认值有意不引入，不称为上游全文或运行时的等价复制。删除前仍需核对安装来源、配套文件、调用方、替代模块、测试和恢复档案。

grilling、writing-for-agents 及规格/拆票/教学等尚未完整接入的手动专项仍保持独立；不因本次参考就自动删除。ask-matt、implement、handoff 的核心路由/实施/交接已有主栈承接，历史差异见原融合记录；本轮不恢复旧总控或改变其他平台权限。

## 验证边界

可验：入口与参考路由、独立安装资源、来源/许可导航、关键正反场景的契约保护、已移除名字不再作为执行依赖。不可由文档测试证明：真实 Agent 总能选对分支、独立 reviewer 已运行、测试质量/性能提升或所有业务任务等价。真实任务需按新入口记录方法选择、实际结果、失败和剩余证据，不能以文件存在或清单映射充当效果验收。
