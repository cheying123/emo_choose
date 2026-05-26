语音情绪识别系统 v2.0 - 安装程序制作说明
============================================

目录说明:
  installer/          - 安装程序相关文件
  dist/               - 编译后的 EXE 文件（由 build_exe.py 生成）

制作安装程序步骤:
========================

第一步: 安装 Inno Setup
  从 https://jrsoftware.org/isinfo.php 下载并安装 Inno Setup
  安装时选择 "Chinese Simplified" 语言包

第二步: 打包 EXE
  在项目根目录运行:
    python build_exe.py
  生成的文件在 dist/ 目录

第三步: 编译安装程序
  用 Inno Setup 打开 installer/installer.iss
  菜单 → Build → Compile (或按 Ctrl+F9)
  生成的安装程序在 installer/ 目录

完成后你将得到:
  语音情绪识别系统_v2.0_安装程序.exe
  双击即可安装，自动创建桌面快捷方式
