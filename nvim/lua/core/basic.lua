vim.opt.number = true                   -- absolute number on the cursor line
vim.opt.relativenumber = true           -- relative line number for fast jumps
vim.opt.cursorline = true               -- hightlight on cursor line

vim.opt.colorcolumn = "80"              -- block column for lines

vim.opt.expandtab = true                -- spaces, not tab
vim.opt.tabstop = 4                     -- 4, not 8
vim.opt.shiftwidth = 0                  -- no indent level

vim.opt.scrolloff = 16                  -- keep cursor away from the screen edge

vim.opt.autoread = true

vim.keymap.set({"n", "i"}, "<C-z>", "<Cmd>undo<CR>", {silent = true})

vim.opt.splitbelow = true

vim.opt.splitright = true

-- 在出问题的代码行末尾显示诊断文字，输入时也更新。
vim.diagnostic.config({
    virtual_text = true,
    update_in_insert = true,
})


vim.opt.ignorecase = true               -- blink, 补全大小写不敏感
vim.opt.smartcase = true                -- blink, 如果明确输入大写,则开启大小写敏感

vim.api.nvim_create_autocmd({"BufRead","BufNewFile"}, {
    pattern = "*.plist",
    command = "setfiletype xml",
})
