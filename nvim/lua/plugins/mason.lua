return {
    "mason-org/mason-lspconfig.nvim",

    -- VeryLazy 是 lazy.nvim 的事件，启动后再加载这个插件。
    event = "VeryLazy",

    dependencies = {
        -- Mason 负责安装语言服务器。opts = {} 表示用默认设置初始化。
        { "mason-org/mason.nvim", opts = {} },

        -- 提供各语言服务器的默认配置，例如 Lua 的 lua_ls。
        "neovim/nvim-lspconfig",
    },

    -- lazy.nvim 会把这里的 opts 传给 mason-lspconfig 的 setup()。
    opts = {
        -- 这里写 Neovim 的 LSP 配置名。
        -- mason-lspconfig 会把 lua_ls 映射到 Mason 包 lua-language-server。
        -- 如果你已经装了 LuaLS，就会直接使用已有安装。
        ensure_installed = { "lua_ls" },

        -- 只自动启用这个列表里的服务器。
        -- 打开 Lua 文件时，Neovim 会按 lua_ls 的配置启动服务器。
        automatic_enable = { "lua_ls" },
    },
}
