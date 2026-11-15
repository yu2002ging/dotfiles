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
