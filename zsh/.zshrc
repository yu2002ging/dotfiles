export PATH="$PATH:$HOME/xwybin/"
export DYLD_LIBRARY_PATH=/opt/homebrew/Cellar/zeromq/4.3.5_1/lib:$DYLD_LIBRARY_PATH

# Add TeX Live to MANPATH
export MANPATH=/usr/local/texlive/2024/texmf-dist/doc/man:$MANPATH

# Add TeX Live to INFOPATH
export INFOPATH=/usr/local/texlive/2024/texmf-dist/doc/info:$INFOPATH

# Add TeX Live to PATH
export PATH=/usr/local/texlive/2024/bin/universal-darwin:$PATH
export PATH=~/.npm-global/bin:$PATH

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$("$HOME/anaconda3/bin/conda" 'shell.zsh' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]; then
        . "$HOME/anaconda3/etc/profile.d/conda.sh"
    else
        export PATH="$HOME/anaconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

export PATH="$HOME/Library/Python/3.9/bin:$PATH"

[ -r "$HOME/.local/bin/env" ] && . "$HOME/.local/bin/env"

# Added by LM Studio CLI (lms)
export PATH="$PATH:$HOME/.lmstudio/bin"
# End of LM Studio CLI section

export PATH="$HOME/.npm-global/bin:$PATH"

# nvm
export NVM_DIR="$HOME/.nvm"
[ -s "/opt/homebrew/opt/nvm/nvm.sh" ] && source "/opt/homebrew/opt/nvm/nvm.sh"

test -e "${HOME}/.iterm2_shell_integration.zsh" && source "${HOME}/.iterm2_shell_integration.zsh"


# opencode
export PATH=$HOME/.opencode/bin:$PATH

# GHCup
[ -f "$HOME/.ghcup/env" ] && source "$HOME/.ghcup/env"

# Proxy for Haskell/Stack network access

# Shared interactive terminal setup (WezTerm and VS Code).
[ -r "$HOME/.config/zsh/local.zsh" ] && source "$HOME/.config/zsh/local.zsh"
[ -r "$HOME/.config/zsh/terminal.zsh" ] && source "$HOME/.config/zsh/terminal.zsh"
