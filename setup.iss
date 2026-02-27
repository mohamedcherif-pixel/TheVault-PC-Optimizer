[Setup]
AppName=The Vault PC Optimizer
AppVersion=1.1.6
DefaultDirName={autopf}\TheVaultOptimizer
DefaultGroupName=The Vault PC Optimizer
OutputDir=Output
OutputBaseFilename=TheVault_Setup
SetupIconFile=gamephoto.ico
Compression=lzma2/max
SolidCompression=yes
PrivilegesRequired=admin
WizardStyle=modern
WizardImageFile=setup_wizard.bmp
WizardSmallImageFile=setup_small.bmp
DisableWelcomePage=no
DisableDirPage=yes
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}\gamephoto.ico

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


[Files]
Source: "setup_wizard.bmp"; Flags: dontcopy
Source: "setup_small.bmp"; Flags: dontcopy

[Code]
procedure InitializeWizard;
begin
  WizardForm.Color := clBlack;
  WizardForm.Font.Color := clWhite;
  WizardForm.WelcomePage.Color := clBlack;
  WizardForm.FinishedPage.Color := clBlack;
  WizardForm.InnerPage.Color := clBlack;
  WizardForm.MainPanel.Color := clBlack;
  
  WizardForm.LicensePage.Color := clBlack;
  WizardForm.ReadyMemo.Color := clBlack;
  WizardForm.ReadyMemo.Font.Color := clWhite;
end;
