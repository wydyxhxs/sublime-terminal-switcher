# Terminal Switcher for Sublime Text

一个方便的Sublime Text插件，可以快速在当前文件目录打开不同的终端。

![](https://cdn.jsdelivr.net/gh/Malrss/picgo/pic1/PixPin_2025-07-31_12-40-00.jpg)

## 功能特性
- 支持PowerShell、Kali Linux (WSL)、Ubuntu (WSL)
- 右键菜单直接访问
- 自动路径转换（Windows路径转WSL路径），自动定位到当前文件所在的目录。


## 安装方法
1. 下载插件文件

2. 复制到 `%APPDATA%\Sublime Text\Packages\` 目录

   > 目录结构：

   ```
   TerminalSwitcher/
   ├── terminal_switcher.py           # 主插件代码
   └── Context.sublime-menu           # 右键菜单配置
   ```

3. 重启Sublime Text

## 使用方法
右键点击编辑器，选择对应的终端选项即可。



## 目录结构

```
TerminalSwitcher/
├── terminal_switcher.py           # 主插件代码
└── Context.sublime-menu           # 右键菜单配置
```

## 注意

需要自行安装WSL 子系统，相应的命令才会生效。

修改`terminal_switcher.py`文件，可替换自己喜欢用的终端。
