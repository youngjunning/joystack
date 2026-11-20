# JoyStack 维护约定

- `skills/engineering/` 是公开技能的唯一维护源；JoyStack 是一套自动协作的工程能力，不要求使用者记住或点名子模块。
- 只保留可公开、可验证的通用工程方法。不得加入内部项目、账号、绝对路径、凭证、私有流程或未经审查的会话材料。
- 新增或调整模块时，同步更新 `catalog.json`、README 和共享的 `joy-stack/references/stack-contract.md`；每个模块都要说明触发场景、输出、边界和交接条件。
- 修改文本使用 `apply_patch`。完成后运行 `python3 scripts/validate.py` 和受影响的测试。
- 提交作者使用 `杨俊宁 <luozhu2021@gmail.com>`；创建 Release、修改用户安装或发布到其他平台须由用户明确授权。
