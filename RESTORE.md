# 新 Mac 恢复

1. 安装 Homebrew、Git、Python 3，然后克隆此仓库到一个长期保留的目录。
2. 按需运行 `brew bundle --file=Brewfile` 安装工具；下载时间不计入链接安装时间。
3. 运行 `python3 scripts/install.py --dry-run` 审阅，然后运行 `python3 scripts/install.py`。
4. 参考 `zsh/local.zsh.example`，在 `~/.config/zsh/local.zsh` 中填写本机密钥和代理。
5. 调整 Zsh 中的 TeX Live 版本等设置。
6. 打开 Neovim 后运行 `:Lazy restore`。首次运行会下载插件；语言服务器由 Mason 管理。
7. 在 VS Code 中登录账户，启用内置 Settings Sync 恢复设置、快捷键、snippets 和扩展。

8. 新开终端，运行 `python3 scripts/doctor.py`，检查命令补全、Ctrl-R、z/zi、提示符与自动建议。

Brewfile 记录基础工具，不包含完整 Anaconda、TeX Live、JDK、GHCup 和全部语言运行时。
现有 Zsh 仍保留这些工具的初始化方式；在新机器上应按实际安装情况调整。
目前 terminal.zsh 的 fzf、zoxide、Starship 路径面向 Apple Silicon Homebrew。
