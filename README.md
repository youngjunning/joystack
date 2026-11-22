# JoyStack

JoyStack 是一套自动出现的工程能力栈。你只需描述目标；遇到跨边界、目标尚未收敛、需要验证、排障或续接的产品与工程任务时，Agent 会按需调用合适模块。简单、明确且低风险的改动不会被额外流程拖慢。

它吸收了可组合的工程能力、验证优先的交付方式，以及长期协作中的事实与决策边界；不依赖、复制或要求安装任何第三方 Skill 套件。

## 安装

```bash
npx skills add youngjunning/joystack
```

安装时选择 JoyStack 的完整模块集。安装完成后正常描述任务即可，无需记忆子模块名称。

## 能力

| 阶段 | 自动能力 |
| --- | --- |
| 不清楚系统现在如何工作 | [Understand](skills/engineering/joy-understand/SKILL.md) |
| 目标、范围或验收仍模糊 | [Shape](skills/engineering/joy-shape/SKILL.md) |
| 需要实现可交付变更 | [Build](skills/engineering/joy-build/SKILL.md) |
| 需要证明结果是否成立 | [Verify](skills/engineering/joy-verify/SKILL.md) |
| 出现异常或回归 | [Debug](skills/engineering/joy-debug/SKILL.md) |
| 合入或发布前独立检查 | [Review](skills/engineering/joy-review/SKILL.md) |
| 实质行为改动需要独立评审、修正和复验到可信终态 | [Loop](skills/engineering/joy-loop/SKILL.md) |
| 阶段性治理文档、测试、规则、分支与 worktree | [Govern](skills/engineering/joy-govern/SKILL.md) |
| 需要安全提交、推送，或通过分支/PR 合入并生成可链接的逐仓库收尾事实 | [Git Delivery](skills/engineering/joy-git/SKILL.md) |
| 跨轮继续或交接 | [Continue](skills/engineering/joy-continue/SKILL.md) |

[JoyStack 入口](skills/engineering/joy-stack/SKILL.md) 统一这些能力，定义最小任务契约和按风险升级的规则。[套件契约](skills/engineering/joy-stack/references/stack-contract.md) 让未来更好的开发套件可以替换或补强单个模块，不锁定某个模型、运行时或平台。

## 维护

```bash
python3 scripts/validate.py
```

贡献者应维持模块之间明确的输入、输出与权限边界；不要把一个套件的专有运行时、模型路由或流程文本直接迁入 JoyStack。

2026-11-22，JoyStack 从 [oil-oil/oil-dev-skills](https://github.com/oil-oil/oil-dev-skills) `9bcd900`（MIT）吸收了分级探索与规划、宿主中立委托契约、风险分级审查、根因修复和仓库治理方法；具体映射与未引入边界见[融合记录](skills/engineering/joy-stack/references/oil-dev-integration.md)。`joy-loop` 改编自 [t3dotgg/tstack](https://github.com/t3dotgg/tstack/tree/11e37a74d0a6868c121cd0910ab2b3bd9873b92a) 的 `sol-loop`（MIT），固定来源与改编边界见模块内 [NOTICE](skills/engineering/joy-loop/NOTICE.md)。
每个模块的 `SKILL.md` frontmatter 必须保留作者 `杨俊宁` 与联系邮箱 `luozhu2021@gmail.com`；仓库校验会检查这两个字段。

## 许可

MIT。JoyStack 是独立实现；Matt Pocock 的 Skills、pstack 与 oil dev skills 仅作为公开工程思想的参考，不包含其脚本、资产、个人配置或运行时。`joy-loop` 保留 `sol-loop` 的 MIT 许可与来源说明。各上游方法与原始实现仍归其作者所有。
