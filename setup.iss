#define MyAppName "The letter editor pro"
#define MyAppPublisher "Yuvald12321"
#define MyAppURL "https://github.com/Yuvald12321/"
#define MyAppExeName "The letter editor pro.exe"
#define MyAppAssocName "Letter file"
#define MyAppAssocExt ".txt"
#define MyAppAssocKey "LetterFileText"
#define MyAppIconName "logo.ico"
#define MyAppFileIconName "file logo.ico"

[Setup]
AppId={{57076A3A-B75D-4CD6-92F4-EF4B435D84C1}
AppName={#MyAppName}
AppVerName={#MyAppName}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
DefaultDirName={localappdata}\{#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputDir=D:\python projects\letter editor pro\dist
OutputBaseFilename=The letter editor pro installer
SolidCompression=yes
WizardStyle=modern windows11

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "D:\python projects\letter editor pro\dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\python projects\letter editor pro\{#MyAppIconName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\python projects\letter editor pro\{#MyAppFileIconName}"; DestDir: "{app}"; Flags: ignoreversion

[Registry]
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocExt}"; ValueType: string; ValueName: ""; ValueData: "{#MyAppAssocKey}"; Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}"; ValueType: string; ValueName: ""; ValueData: "{#MyAppAssocName}"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppFileIconName}"""; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""
Root: HKA; Subkey: "Software\Classes\*\shell\Letterwrapper"; ValueType: string; ValueName: ""; ValueData: "&Letter this"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\*\shell\Letterwrapper"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\{#MyAppIconName}"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\*\shell\Letterwrapper\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""; Flags: uninsdeletekey

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppIconName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; IconFilename: "{app}\{#MyAppIconName}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent