# dotfiles

管理 macOS 上的 Zsh、Neovim、WezTerm、Starship 配置。
仓库中的文件是配置正文；应用原位置通过符号链接读取它们。

## 应用配置

需要 Python 3。先退出 Neovim，避免它们在迁移过程中写入设置。

```bash
python3 scripts/install.py --dry-run --migrate-local
python3 scripts/install.py --migrate-local
python3 scripts/doctor.py
```

安装前自动把原文件或目录移到 `~/.local/state/dotfiles/时间戳/`，再建立链接。
每次安装会输出准确的回退命令。重复运行会跳过正确链接，不创建多余备份。
`--dry-run` 不写任何文件。遇到其他符号链接时默认停止；确认后才用 `--repair-links`。
仓库移动后可用此选项重新建立链接。

`--migrate-local` 从旧 `.zshrc` 提取 Anthropic API 和代理的 export 语句，
保存到仓库外的 `~/.config/zsh/local.zsh`，权限为 600。
已有 local.zsh 且内容不一致时停止，要求先合并，不覆盖私人设置。
备份和恢复日志可能包含私人配置，应留在本机，不上传 Git。
回退时若发现目标被应用替换，或者私人配置被修改，会停止，保护后续修改。
回退恢复原配置并删除本次新建的 local.zsh；原 `.zshrc` 中的原设置随之恢复。

## 日常修改与同步

直接编辑 `~/.zshrc`、`~/.config/nvim/` 或应用中的设置即可。
通过符号链接保存的修改会出现在仓库的 `git diff` 中。
应用可能以替换文件的方式保存，导致符号链接被普通文件取代；运行 doctor 检查，
先合并该文件的新内容再重装，避免丢失修改。

```bash
git status
git diff
# 审阅后选择文件提交，再 push；另一台机器 pull 后读取最新配置。
```

不要把密钥、令牌、缓存、插件下载目录和命令历史放入仓库。
不再依赖 Git clean/smudge 过滤器来脱敏；本地文件分离才是主要措施。
这份仓库没有自动发布；公开前还应审查本机路径和个人偏好。

## 配置范围

| 仓库 | 实际位置 |
|---|---|
| zsh/.zshrc | ~/.zshrc |
| zsh/.zprofile | ~/.zprofile |
| zsh/terminal.zsh | ~/.config/zsh/terminal.zsh |
| nvim/ | ~/.config/nvim/ |
| wezterm/wezterm.lua | ~/.config/wezterm/wezterm.lua |
| starship/starship.toml | ~/.config/starship.toml |


VS Code 的设置、快捷键、snippets 和扩展由其内置 Settings Sync 管理，不纳入本仓库。
