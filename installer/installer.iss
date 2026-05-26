; 语音情绪识别系统 v2.0 - Inno Setup 安装脚本
; ==============================================
; 使用 Inno Setup 编译此脚本生成 MSI 风格安装程序
; 下载 Inno Setup: https://jrsoftware.org/isinfo.php

#define MyAppName "语音情绪识别系统"
#define MyAppVersion "2.0.0"
#define MyAppPublisher "EmoChoose"
#define MyAppURL "https://github.com/emo-choose"
#define MyAppExeName "语音情绪识别系统.exe"

[Setup]
; 基本信息
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; 安装目录
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes

; 输出配置
OutputDir=.
OutputBaseFilename=语音情绪识别系统_v2.0_安装程序
SetupIconFile=..\icon.ico
Compression=lzma2/max
SolidCompression=yes
UninstallDisplayIcon={app}\{#MyAppExeName}

; 权限
PrivilegesRequired=admin
DisableProgramGroupPage=yes

; 界面
WizardStyle=modern
WizardSizePercent=100
DisableWelcomePage=no

[Languages]
Name: "chinese"; MessagesFile: "ChineseSimplified.isl"
Name: "english"; MessagesFile: "Default.isl"

[Tasks]
Name: "desktopicon"; Description: "创建桌面快捷方式"; GroupDescription: "快捷方式:"; Flags: checkedonce

[Files]
; 主程序文件
Source: "..\dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\dist\{#MyAppName}\*"; DestDir: "{app}\bin"; Flags: ignoreversion recursesubdirs createallsubdirs

; Python 运行环境（如果需要）
; Source: "..\python_embeded\*"; DestDir: "{app}\python"; Flags: ignoreversion recursesubdirs createallsubdirs

; 项目脚本（作为备用）
Source: "..\emotion_recognizer.py"; DestDir: "{app}\src"; Flags: ignoreversion
Source: "..\gui_app.py"; DestDir: "{app}\src"; Flags: ignoreversion
Source: "..\batch_process.py"; DestDir: "{app}\src"; Flags: ignoreversion
Source: "..\requirements.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; 开始菜单
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"
Name: "{group}\卸载 {#MyAppName}"; Filename: "{uninstallexe}"

; 桌面快捷方式
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
; 安装完成后启动
Filename: "{app}\{#MyAppExeName}"; Description: "启动 {#MyAppName}"; Flags: nowait postinstall skipifsilent shellexec

[UninstallRun]
; 卸载时清理模型缓存
Filename: "{cmd}"; Parameters: "/c rmdir /s /q ""{localappdata}\huggingface\hub\models--CAiRE--SER-wav2vec2-large-xlsr-53-eng-zho-all-age"""; Flags: runhidden

[Code]
{ 安装前检查系统需求 }
function InitializeSetup: Boolean;
var
  PythonVersion: string;
  ResultCode: Integer;
begin
  Result := True;

  { 检查 Windows 版本 }
  if GetWindowsVersion < 6.1 then begin
    MsgBox('此软件需要 Windows 7 或更高版本。', mbError, MB_OK);
    Result := False;
    Exit;
  end;
end;

{ 获取安装路径（中文支持） }
function GetCustomSetupExitCode: Integer;
begin
  Result := 0;
end;
