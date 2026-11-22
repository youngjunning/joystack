# 来源说明

本模块改编自 Theo Browne 的 [t3dotgg/tstack `sol-loop`](https://github.com/t3dotgg/tstack/tree/11e37a74d0a6868c121cd0910ab2b3bd9873b92a/skills/sol-loop)，上游采用 MIT License。

JoyStack 版本使用 `joy-loop` 名称，把上游专用 reviewer 调用泛化为宿主无关的有限改进循环。模块只维护轮次、finding ledger 与停止条件；具体评审、修正、验证和 Git 交付分别复用 JoyStack 的 `joy-review`、`joy-build`、`joy-verify` 与 `joy-git`。视频转述中常见的 “Soul Loop” 实际对应上游的 `sol-loop`。
