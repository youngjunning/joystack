# pstack 融合记录

## 来源与核对范围

pstack 的作者是 **Lauren Tan（poteto）**，来源为 [cursor/plugins 的 pstack](https://github.com/cursor/plugins/tree/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack)，不是 Matt Pocock 的 Skills，也不是 t3dotgg/tstack。本次核对日期为 2026-11-23；固定仓库快照 `7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9`，pstack/plugin.json 的版本为 `0.15.46`，pstack 子目录 LICENSE 为 MIT / Copyright 2026 Lauren Tan。该许可依据属于 pstack 子目录，不从 cursor/plugins 根目录推导全仓库许可。

JoyStack 初始提交 [cce7d14](https://github.com/youngjunning/joystack/commit/cce7d148bd716d40d650010c22f0dea69462b61a) 于 2026-11-20 已声明 pstack 是工程思想参考，不包含其文本、脚本、资产或运行时；**当时没有记录精确上游版本或逐项移植历史**。本次固定版本用于回查，不冒充最初参考版本。下表以 JoyStack `a7e74279fcb03933d026778366922827a30d72eb` 当前契约为落点证据。

## 方法、落点与差异

| pstack 来源方法 | JoyStack 落点 | 当前已体现的规则 | 未整体引入的部分 |
| --- | --- | --- | --- |
| poteto-mode：按任务选择专业能力 | joy-stack、各模块交接 | 用统一目标/边界/证据契约组合能力，按风险升级；用户不用记住子模块 | poteto-mode 总控、Todolist 工作流、固定角色/模型、Cursor 专用工具和并行默认 |
| principle-prove-it-works、principle-test-behavior-not-implementation | joy-verify、joy-build | 从具体主张反推最直接验证，不用编译/模型自报替代真实行为；切片取得反馈 | 全部验证资产、平台截图/报告格式、形式化验证 Skill 生成器 |
| principle-fix-root-causes | joy-debug | 先复现、核对假设、修源头并回归，不把症状消失当根因成立 | 上游模型/工具流程和强制取舍；未证明时保留未知而非保证一定定位 |
| principle-boundary-discipline、architect | joy-review、joy-shape | 检查现有边界、重复验证/复杂度与复用基建；有风险时先收敛接口和责任 | 未完整实现其纯函数/类型/seam 方法或强制两套设计比较；架构仍由专业 Skill 主导 |
| principle-sequence-verifiable-units | joy-build、joy-verify | 最小纵向切片与每步可观察反馈；交付把测试、构建、推送、部署分别核验 | 上游固定 commit 顺序、每项任务必须分 PR 或强制全流程 |
| principle-encode-lessons-in-structure | joy-govern、joy-debug、joy-review | 重复且可静态判定的问题先做确定性检查；需要判断时保留有证据规则，不自动修改常驻文件 | 上游环境改写、rule/metadata 工具和自动生成流程 |
| ketchup、in-your-own-words | joy-continue 的工程状态交接 | 已知结果、证据、决定、未完成项与下一步有单一可续接定位；历史摘要先回查 | pstack 报告、图像/视频、固定视觉约束或模型驱动的解释流程；joyally-report 是独立能力 |

这些是方法层对应，不等于完整采用每个 pstack Skill。相似工程原则可能有多个来源；没有证据时，不把某行指定为唯一来源或新增性能收益。

## 明确保留的不同选择

1. pstack 当前具有 swarm、arena 和模型角色配置；JoyStack 不依赖这些工具或模型，不因引用来源获得委托/调用权限。
2. pstack 的“不阻塞在人类”等自主执行倾向不替代用户、项目和平台授权。JoyStack 对不可逆动作、范围/成本改变和未知门禁仍需相应决定，不以追求持续运行绕过确认。
3. 语义重审、结果可信和减少复杂度可以借鉴，低频数据丢失/安全/并发不能机械视为无价值边界；测试深度以真实风险决定。
4. 本次记录不安装或更新 pstack；JoyStack 的运行能力由自身与宿主现有工具完成。来源后续更新不自动同步，也不作为缺项时的默认上游安装或执行方案。

## 归属与验证边界

保留 Lauren Tan / pstack 的方法归属和 MIT 依据，本次文字独立整理，不复制上游正文、脚本、图片、角色配置或运行时。未来实质复用仍需遵守该目录的 LICENSE；许可证不是平台操作或代码跨供应商传递的授权。

已核对固定来源、原始归属、JoyStack 初始参考声明及当前方法覆盖。源码和文档对应不能恢复未保存的最初参考 SHA，也不能证明所有 pstack 组件已吸收。新增静态测试只检查记录、导航和字段，不代表原系统或 JoyStack 的真实多 Agent/平台效果已经验收。

## 固定版本一手资料

- [README](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/README.md)、[plugin.json](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/plugin.json)、[LICENSE](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/LICENSE)
- [poteto-mode](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/poteto-mode/SKILL.md)、[architect](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/architect/SKILL.md)
- [principle-prove-it-works](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-prove-it-works/SKILL.md)、[principle-test-behavior-not-implementation](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-test-behavior-not-implementation/SKILL.md)
- [principle-fix-root-causes](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-fix-root-causes/SKILL.md)、[principle-boundary-discipline](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-boundary-discipline/SKILL.md)
- [principle-sequence-verifiable-units](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-sequence-verifiable-units/SKILL.md)、[principle-encode-lessons-in-structure](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-encode-lessons-in-structure/SKILL.md)
- [ketchup](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/ketchup/SKILL.md)、[in-your-own-words](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/in-your-own-words/SKILL.md)
