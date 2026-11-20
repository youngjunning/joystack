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
| 需要安全提交、推送或收尾仓库改动 | [Git Delivery](skills/engineering/joy-git/SKILL.md) |
| 跨轮继续或交接 | [Continue](skills/engineering/joy-continue/SKILL.md) |

[JoyStack 入口](skills/engineering/joy-stack/SKILL.md) 统一这些能力，定义最小任务契约和按风险升级的规则。[套件契约](skills/engineering/joy-stack/references/stack-contract.md) 让未来更好的开发套件可以替换或补强单个模块，不锁定某个模型、运行时或平台。

## 维护

```bash
python3 scripts/validate.py
```

贡献者应维持模块之间明确的输入、输出与权限边界；不要把一个套件的专有运行时、模型路由或流程文本直接迁入 JoyStack。

## 许可

MIT。JoyStack 是独立实现；Matt Pocock 的 Skills 和 pstack 仅作为公开工程思想的参考，不包含其文本、脚本、资产或运行时。
