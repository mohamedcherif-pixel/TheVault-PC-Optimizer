[Setup]
AppName=The Vault PC Optimizer
AppVersion=1.0
DefaultDirName={autopf}\TheVaultOptimizer
DefaultGroupName=The Vault PC Optimizer
OutputDir=Output
OutputBaseFilename=TheVault_Setup
SetupIconFile=gamephoto.ico
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin

[Files]
Source: "dist\TheVault_Optimizer.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "Dark Fantasy - shahi77.mp3"; DestDir: "{app}"; Flags: ignoreversion
Source: "gamephoto.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\The Vault PC Optimizer"; Filename: "{app}\TheVault_Optimizer.exe"; IconFilename: "{app}\gamephoto.ico"
Name: "{autodesktop}\The Vault PC Optimizer"; Filename: "{app}\TheVault_Optimizer.exe"; IconFilename: "{app}\gamephoto.ico"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Run]
Filename: "{app}\TheVault_Optimizer.exe"; Description: "{cm:LaunchProgram,The Vault PC Optimizer}"; Flags: nowait postinstall skipifsilent
