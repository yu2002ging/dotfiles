# Save and share command history across interactive Zsh sessions.
HISTFILE=${HISTFILE:-$HOME/.zsh_history}
HISTSIZE=50000
SAVEHIST=20000
setopt SHARE_HISTORY HIST_IGNORE_DUPS

# Load command, option, and path completions.
typeset -U fpath
fpath=(/opt/homebrew/share/zsh/site-functions $fpath)
autoload -Uz compinit
compinit
zstyle ':completion:*' menu select

# Use fzf for Ctrl-R; keep normal Zsh Tab completion.
if [[ -x /opt/homebrew/bin/fzf ]]; then
  FZF_CTRL_T_COMMAND= FZF_ALT_C_COMMAND= eval "$(/opt/homebrew/bin/fzf --zsh | sed -n '/^### key-bindings.zsh ###$/,/^### end: key-bindings.zsh ###$/p')"
fi

# Enable z and zi for directory jumping.
if [[ -x /opt/homebrew/bin/zoxide ]]; then
  eval "$(/opt/homebrew/bin/zoxide init zsh)"
fi

if [[ -x /opt/homebrew/bin/starship ]]; then
  eval "$(/opt/homebrew/bin/starship init zsh)"
fi

# Suggest previous commands inline. Right Arrow accepts at end of line.
if [[ -r "$HOME/.config/zsh/zsh-autosuggestions.zsh" ]]; then
  source "$HOME/.config/zsh/zsh-autosuggestions.zsh"
elif [[ -r /opt/homebrew/share/zsh-autosuggestions/zsh-autosuggestions.zsh ]]; then
  source /opt/homebrew/share/zsh-autosuggestions/zsh-autosuggestions.zsh
elif [[ -r /usr/local/share/zsh-autosuggestions/zsh-autosuggestions.zsh ]]; then
  source /usr/local/share/zsh-autosuggestions/zsh-autosuggestions.zsh
fi

# Keep syntax highlighting last so it can wrap other Zsh widgets.
if command -v brew >/dev/null 2>&1; then
  _zsh_syntax_highlighting="$(brew --prefix)/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh"
  [[ -r "$_zsh_syntax_highlighting" ]] && source "$_zsh_syntax_highlighting"
  unset _zsh_syntax_highlighting
fi
