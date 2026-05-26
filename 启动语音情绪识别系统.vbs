' 语音情绪识别系统 v2.0 - 桌面快捷启动脚本
' 双击此文件即可启动，无命令行窗口
' 确保已安装依赖: pip install -r requirements.txt

Dim shell, fso, currentDir
Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' 获取当前脚本所在目录
currentDir = fso.GetParentFolderName(WScript.ScriptFullName)

' 切换到项目目录
shell.CurrentDirectory = currentDir

' 静默启动 GUI（不显示控制台窗口）
shell.Run "python gui_app.py", 0, False

Set shell = Nothing
Set fso = Nothing
