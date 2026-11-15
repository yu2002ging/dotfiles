# 在新 Mac 上恢复开发配置

这份仓库保存 Neovim、WezTerm、Starship、Zsh 和 VS Code 的配置快照。应用和插件由各自的工具重新下载。

1. 安装 Homebrew，在仓库根目录运行 `brew bundle --file=Brewfile`。清单面向当前的 Apple Silicon Mac。
2. 先备份新机上已有的同名文件，再按下表复制配置。
3. 检查 Zsh 和 VS Code 配置里的本机路径，再打开新终端。原机配置包含 Anaconda、TeX Live、自定义目录及代理等设置。按新机实际情况调整；如果本机代理不用了，删掉对应代理变量。API 密钥和自定义 API 服务地址从原机单独配置。
4. 打开 Neovim，等 lazy.nvim 安装完成，再用 `:Lazy restore` 按锁文件恢复插件。Mason 会根据 Neovim 配置安装语言服务器。
5. 在 VS Code 中执行 Shell Command: Install 'code' command in PATH，然后在仓库里运行 `while IFS= read -r id; do code --install-extension "$id"; done < vscode/extensions.txt`。清单记录扩展 ID，安装版本由 VS Code 决定。

| 仓库中 | 复制到 |
|---|---|
| `nvim/` 内的文件 | `~/.config/nvim/` |
| `wezterm/wezterm.lua` | `~/.config/wezterm/wezterm.lua` |
| `starship/starship.toml` | `~/.config/starship.toml` |
| `zsh/.zshrc`、`zsh/.zprofile` | `~/.zshrc`、`~/.zprofile` |
| `zsh/terminal.zsh` | `~/.config/zsh/terminal.zsh` |
| `vscode/settings.json`、`vscode/keybindings.json`、`vscode/snippets/` | `~/Library/Application Support/Code/User/` 下的对应位置 |

如需恢复 Zsh 自动建议，将 [zsh-autosuggestions v0.7.1](https://github.com/zsh-users/zsh-autosuggestions/releases/tag/v0.7.1) 中的 `zsh-autosuggestions.zsh` 下载到 `~/.config/zsh/`，然后新开终端。原配置引用的 Conda 环境及其他第三方工具可按需重新安装。
