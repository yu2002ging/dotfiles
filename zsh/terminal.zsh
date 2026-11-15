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

if [[ -x /opt/homebrew/bin/starship ]]; then
  eval "$(/opt/homebrew/bin/starship init zsh)"
fi

# Suggest previous commands inline. Right Arrow accepts at end of line.
if [[ -r "$HOME/.config/zsh/zsh-autosuggestions.zsh" ]]; then
  source "$HOME/.config/zsh/zsh-autosuggestions.zsh"
fi
