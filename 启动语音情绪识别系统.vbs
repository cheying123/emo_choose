' 语音情绪识别系统 v2.0 - 静默启动
' 双击此文件启动，无命令行窗口

Dim shell, fso, currentDir
Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

currentDir = fso.GetParentFolderName(WScript.ScriptFullName)
shell.CurrentDirectory = currentDir

' 设置 HuggingFace 国内镜像
shell.Environment("PROCESS")("HF_ENDPOINT") = "https://hf-mirror.com"

' 后台启动 Web 服务
shell.Run "cmd /c start http://localhost:5000", 0, False
shell.Run "python web_app.py", 0, False

Set shell = Nothing
Set fso = Nothing
