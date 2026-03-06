[Setup]
AppName=The Vault PC Optimizer
AppVersion=1.1.7
AppPublisher=mohamedcherif-pixel
AppPublisherURL=https://github.com/mohamedcherif-pixel/TheVault-PC-Optimizer
AppSupportURL=https://github.com/mohamedcherif-pixel/TheVault-PC-Optimizer/issues
AppUpdatesURL=https://github.com/mohamedcherif-pixel/TheVault-PC-Optimizer/releases
AppCopyright=Copyright (c) 2024-2026 mohamedcherif-pixel
DefaultDirName={autopf}\TheVaultOptimizer
DefaultGroupName=The Vault PC Optimizer
OutputDir=Output
OutputBaseFilename=TheVault_Setup
SetupIconFile=gnome.ico
Compression=lzma2/max
SolidCompression=yes
PrivilegesRequired=admin
WizardStyle=modern
WizardImageFile=gnome_wizard.bmp
WizardSmallImageFile=gnome_small.bmp
LicenseFile=installer_license.txt
InfoBeforeFile=INFO_BEFORE.txt
DisableWelcomePage=no
DisableDirPage=yes
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}\gnome.ico

[Files]
Source: "dist\TheVault_Optimizer.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "Dark Fantasy - shahi77.mp3"; DestDir: "{app}"; Flags: ignoreversion
Source: "gnome.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "installer_license.txt"; DestDir: "{app}"; DestName: "LICENSE.txt"; Flags: ignoreversion
Source: "INFO_BEFORE.txt"; DestDir: "{app}"; DestName: "README.txt"; Flags: ignoreversion

[Icons]
Name: "{group}\The Vault PC Optimizer"; Filename: "{app}\TheVault_Optimizer.exe"; IconFilename: "{app}\gnome.ico"
Name: "{autodesktop}\The Vault PC Optimizer"; Filename: "{app}\TheVault_Optimizer.exe"; IconFilename: "{app}\gnome.ico"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Run]
Filename: "{app}\TheVault_Optimizer.exe"; Description: "{cm:LaunchProgram,The Vault PC Optimizer}"; Flags: nowait postinstall skipifsilent

[Files]
Source: "bmp_anim1_0.bmp"; Flags: dontcopy
Source: "bmp_anim1_1.bmp"; Flags: dontcopy
Source: "bmp_anim1_2.bmp"; Flags: dontcopy
Source: "bmp_anim1_3.bmp"; Flags: dontcopy
Source: "bmp_anim1_4.bmp"; Flags: dontcopy
Source: "bmp_anim1_5.bmp"; Flags: dontcopy
Source: "bmp_anim1_6.bmp"; Flags: dontcopy
Source: "bmp_anim1_7.bmp"; Flags: dontcopy
Source: "bmp_anim1_8.bmp"; Flags: dontcopy
Source: "bmp_anim2_0.bmp"; Flags: dontcopy
Source: "bmp_anim2_1.bmp"; Flags: dontcopy
Source: "bmp_anim2_2.bmp"; Flags: dontcopy
Source: "bmp_anim2_3.bmp"; Flags: dontcopy
Source: "bmp_anim2_4.bmp"; Flags: dontcopy
Source: "bmp_anim2_5.bmp"; Flags: dontcopy
Source: "bmp_anim2_6.bmp"; Flags: dontcopy
Source: "bmp_anim2_7.bmp"; Flags: dontcopy
Source: "bmp_anim2_8.bmp"; Flags: dontcopy
Source: "bmp_anim2_9.bmp"; Flags: dontcopy
Source: "bmp_anim2_10.bmp"; Flags: dontcopy
Source: "bmp_anim2_11.bmp"; Flags: dontcopy
Source: "bmp_anim2_12.bmp"; Flags: dontcopy
Source: "bmp_anim2_13.bmp"; Flags: dontcopy
Source: "bmp_anim2_14.bmp"; Flags: dontcopy
Source: "bmp_anim2_15.bmp"; Flags: dontcopy
Source: "bmp_anim2_16.bmp"; Flags: dontcopy
Source: "bmp_anim2_17.bmp"; Flags: dontcopy
Source: "bmp_anim2_18.bmp"; Flags: dontcopy
Source: "bmp_anim2_19.bmp"; Flags: dontcopy
Source: "bmp_anim2_20.bmp"; Flags: dontcopy
Source: "bmp_anim2_21.bmp"; Flags: dontcopy
Source: "bmp_anim2_22.bmp"; Flags: dontcopy
Source: "bmp_anim2_23.bmp"; Flags: dontcopy
Source: "bmp_anim2_24.bmp"; Flags: dontcopy
Source: "bmp_anim2_25.bmp"; Flags: dontcopy
Source: "bmp_anim2_26.bmp"; Flags: dontcopy
Source: "bmp_anim2_27.bmp"; Flags: dontcopy
Source: "bmp_anim2_28.bmp"; Flags: dontcopy
Source: "bmp_anim2_29.bmp"; Flags: dontcopy
Source: "bmp_anim2_30.bmp"; Flags: dontcopy
Source: "bmp_anim2_31.bmp"; Flags: dontcopy
Source: "bmp_anim2_32.bmp"; Flags: dontcopy
Source: "bmp_anim2_33.bmp"; Flags: dontcopy
Source: "bmp_anim2_34.bmp"; Flags: dontcopy
Source: "bmp_anim2_35.bmp"; Flags: dontcopy
Source: "bmp_anim2_36.bmp"; Flags: dontcopy
Source: "bmp_anim2_37.bmp"; Flags: dontcopy
Source: "bmp_anim2_38.bmp"; Flags: dontcopy
Source: "bmp_anim2_39.bmp"; Flags: dontcopy
Source: "bmp_anim2_40.bmp"; Flags: dontcopy
Source: "bmp_anim2_41.bmp"; Flags: dontcopy
Source: "bmp_anim2_42.bmp"; Flags: dontcopy
Source: "bmp_anim2_43.bmp"; Flags: dontcopy
Source: "bmp_anim2_44.bmp"; Flags: dontcopy
Source: "bmp_anim2_45.bmp"; Flags: dontcopy
Source: "bmp_anim2_46.bmp"; Flags: dontcopy
Source: "bmp_anim2_47.bmp"; Flags: dontcopy
Source: "bmp_anim2_48.bmp"; Flags: dontcopy
Source: "bmp_anim2_49.bmp"; Flags: dontcopy
Source: "bmp_anim2_50.bmp"; Flags: dontcopy
Source: "bmp_anim2_51.bmp"; Flags: dontcopy
Source: "bmp_anim2_52.bmp"; Flags: dontcopy
Source: "bmp_anim2_53.bmp"; Flags: dontcopy
Source: "bmp_anim2_54.bmp"; Flags: dontcopy
Source: "bmp_anim2_55.bmp"; Flags: dontcopy
Source: "bmp_anim2_56.bmp"; Flags: dontcopy
Source: "bmp_anim2_57.bmp"; Flags: dontcopy
Source: "bmp_anim2_58.bmp"; Flags: dontcopy
Source: "bmp_anim2_59.bmp"; Flags: dontcopy
Source: "bmp_anim2_60.bmp"; Flags: dontcopy
Source: "bmp_anim2_61.bmp"; Flags: dontcopy
Source: "bmp_anim2_62.bmp"; Flags: dontcopy
Source: "bmp_anim2_63.bmp"; Flags: dontcopy
Source: "bmp_anim2_64.bmp"; Flags: dontcopy
Source: "bmp_anim2_65.bmp"; Flags: dontcopy
Source: "bmp_anim2_66.bmp"; Flags: dontcopy
Source: "bmp_anim2_67.bmp"; Flags: dontcopy
Source: "bmp_anim2_68.bmp"; Flags: dontcopy
Source: "bmp_anim2_69.bmp"; Flags: dontcopy
Source: "bmp_anim2_70.bmp"; Flags: dontcopy
Source: "bmp_anim2_71.bmp"; Flags: dontcopy
Source: "bmp_anim2_72.bmp"; Flags: dontcopy
Source: "bmp_anim2_73.bmp"; Flags: dontcopy
Source: "bmp_anim2_74.bmp"; Flags: dontcopy
Source: "bmp_anim2_75.bmp"; Flags: dontcopy

[Code]
var
  Anim1Image, Anim2Image: TBitmapImage;
  Anim2Container: TPanel;
  Frame1, Frame2: Integer;
  TimerActive: Boolean;
  VersionLabel, URLLabel, ElapsedLabel: TNewStaticText;
  AcceptLabel, RejectLabel, LicInfoLabel: TNewStaticText;
  MarqueeLabel, ProgressLabel: TNewStaticText;
  InstallStartTick: Cardinal;
  MarqueePos, PulseCounter: Integer;

function SetTimer(hWnd: longword; nIDEvent, uElapse: longword; lpTimerFunc: longword): longword;
  external 'SetTimer@user32.dll stdcall';
function KillTimer(hWnd: longword; uIDEvent: longword): boolean;
  external 'KillTimer@user32.dll stdcall';
function GetTickCount: Cardinal;
  external 'GetTickCount@kernel32.dll stdcall';
function ShellExecute(hwnd: Integer; lpOperation, lpFile, lpParameters, lpDirectory: String; nShowCmd: Integer): Integer;
  external 'ShellExecuteW@shell32.dll stdcall';

procedure TimerProc(h: longword; msg: longword; idevent: longword; dwTime: longword);
var
  ElapsedSec, Mins, Secs, Pct: Integer;
begin
  // ── Animate GIF 1 (postal dude - side panel) ──
  if (Anim1Image <> nil) and Anim1Image.Visible then begin
    Frame1 := (Frame1 + 1) mod 9;
    ExtractTemporaryFile('bmp_anim1_' + IntToStr(Frame1) + '.bmp');
    Anim1Image.Bitmap.LoadFromFile(ExpandConstant('{tmp}\bmp_anim1_' + IntToStr(Frame1) + '.bmp'));
  end;
  // ── Animate GIF 2 (regret nothing - header) ──
  if (Anim2Image <> nil) and Anim2Image.Visible then begin
    Frame2 := (Frame2 + 1) mod 76;
    ExtractTemporaryFile('bmp_anim2_' + IntToStr(Frame2) + '.bmp');
    Anim2Image.Bitmap.LoadFromFile(ExpandConstant('{tmp}\bmp_anim2_' + IntToStr(Frame2) + '.bmp'));
  end;
  // ── Elapsed time counter (visible during install) ──
  if (ElapsedLabel <> nil) and ElapsedLabel.Visible and (InstallStartTick > 0) then begin
    ElapsedSec := (GetTickCount - InstallStartTick) div 1000;
    Mins := ElapsedSec div 60;
    Secs := ElapsedSec mod 60;
    if Secs < 10 then
      ElapsedLabel.Caption := 'Elapsed: ' + IntToStr(Mins) + ':0' + IntToStr(Secs)
    else
      ElapsedLabel.Caption := 'Elapsed: ' + IntToStr(Mins) + ':' + IntToStr(Secs);
  end;
  // ── Marquee scrolling text ──
  if (MarqueeLabel <> nil) and MarqueeLabel.Visible then begin
    MarqueePos := MarqueePos - 10;
    if MarqueePos < -(MarqueeLabel.Width) then
      MarqueePos := WizardForm.ClientWidth;
    MarqueeLabel.Left := MarqueePos;
  end;
  // ── Progress percentage (during install) ──
  if (ProgressLabel <> nil) and ProgressLabel.Visible then begin
    if WizardForm.ProgressGauge.Max > 0 then begin
      Pct := (WizardForm.ProgressGauge.Position * 100) div WizardForm.ProgressGauge.Max;
      ProgressLabel.Caption := IntToStr(Pct) + '%';
    end;
  end;
  // ── Pulse effect counter ──
  PulseCounter := (PulseCounter + 1) mod 20;
end;

procedure URLLabelClick(Sender: TObject);
begin
  ShellExecute(0, 'open', 'https://github.com/mohamedcherif-pixel/TheVault-PC-Optimizer', '', '', 1);
end;

procedure AcceptLabelClick(Sender: TObject);
begin
  WizardForm.LicenseAcceptedRadio.Checked := True;
end;

procedure RejectLabelClick(Sender: TObject);
begin
  WizardForm.LicenseNotAcceptedRadio.Checked := True;
end;

procedure InitializeWizard;
begin
  // ══════════════════════════════════════════════════════════════════
  //  DARK THEME - WHITE TEXT ON BLACK (all controls)
  // ══════════════════════════════════════════════════════════════════

  WizardForm.Color := clBlack;
  WizardForm.Font.Color := clWhite;
  WizardForm.InnerPage.Color := clBlack;
  WizardForm.MainPanel.Color := $00111111;

  // ── Buttons (bold white) ──
  WizardForm.NextButton.Font.Color := clWhite;
  WizardForm.NextButton.Font.Style := [fsBold];
  WizardForm.BackButton.Font.Color := clWhite;
  WizardForm.CancelButton.Font.Color := clWhite;

  // ── Hide bevels for clean look ──
  WizardForm.Bevel.Visible := False;
  WizardForm.Bevel1.Visible := False;

  // ── Welcome page (GREEN text) ──
  WizardForm.WelcomePage.Color := clBlack;
  WizardForm.WelcomeLabel1.Font.Color := clLime;
  WizardForm.WelcomeLabel1.Font.Size := 14;
  WizardForm.WelcomeLabel1.Font.Style := [fsBold];
  WizardForm.WelcomeLabel2.Font.Color := clLime;

  // ── Finished page ──
  WizardForm.FinishedPage.Color := clBlack;
  WizardForm.FinishedHeadingLabel.Font.Color := clWhite;
  WizardForm.FinishedHeadingLabel.Font.Size := 14;
  WizardForm.FinishedHeadingLabel.Font.Style := [fsBold];
  WizardForm.FinishedLabel.Font.Color := $00CCCCCC;

  // ── Page headers (inner pages) ──
  WizardForm.PageNameLabel.Font.Color := clWhite;
  WizardForm.PageNameLabel.Font.Size := 11;
  WizardForm.PageNameLabel.Font.Style := [fsBold];
  WizardForm.PageDescriptionLabel.Font.Color := $00AAAAAA;

  // ── License page ──
  WizardForm.LicensePage.Color := clBlack;
  WizardForm.LicenseMemo.Color := $00181818;
  WizardForm.LicenseMemo.UseRichEdit := False;
  WizardForm.LicenseMemo.Font.Color := clWhite;
  WizardForm.LicenseMemo.Font.Name := 'Consolas';
  WizardForm.LicenseMemo.Font.Size := 9;

  // Hide original themed controls (their text is black and can't be changed)
  WizardForm.LicenseLabel1.Visible := False;
  WizardForm.LicenseAcceptedRadio.Width := 20;
  WizardForm.LicenseAcceptedRadio.Caption := '';
  WizardForm.LicenseNotAcceptedRadio.Width := 20;
  WizardForm.LicenseNotAcceptedRadio.Caption := '';

  // White label overlay for "Please read..." text
  LicInfoLabel := TNewStaticText.Create(WizardForm);
  LicInfoLabel.Parent := WizardForm.LicensePage;
  LicInfoLabel.Left := WizardForm.LicenseLabel1.Left;
  LicInfoLabel.Top := WizardForm.LicenseLabel1.Top;
  LicInfoLabel.Width := WizardForm.LicenseLabel1.Width;
  LicInfoLabel.Caption := 'Please read the following License Agreement. You must accept the terms before continuing.';
  LicInfoLabel.Font.Color := clWhite;
  LicInfoLabel.Font.Size := 8;
  LicInfoLabel.Color := clBlack;
  LicInfoLabel.AutoSize := True;

  // White label next to Accept radio circle
  AcceptLabel := TNewStaticText.Create(WizardForm);
  AcceptLabel.Parent := WizardForm.LicensePage;
  AcceptLabel.Left := WizardForm.LicenseAcceptedRadio.Left + 22;
  AcceptLabel.Top := WizardForm.LicenseAcceptedRadio.Top + 1;
  AcceptLabel.Caption := 'I accept the agreement';
  AcceptLabel.Font.Color := clWhite;
  AcceptLabel.Font.Size := 8;
  AcceptLabel.Color := clBlack;
  AcceptLabel.Cursor := crHand;
  AcceptLabel.OnClick := @AcceptLabelClick;

  // White label next to Reject radio circle
  RejectLabel := TNewStaticText.Create(WizardForm);
  RejectLabel.Parent := WizardForm.LicensePage;
  RejectLabel.Left := WizardForm.LicenseNotAcceptedRadio.Left + 22;
  RejectLabel.Top := WizardForm.LicenseNotAcceptedRadio.Top + 1;
  RejectLabel.Caption := 'I do not accept the agreement';
  RejectLabel.Font.Color := clWhite;
  RejectLabel.Font.Size := 8;
  RejectLabel.Color := clBlack;
  RejectLabel.Cursor := crHand;
  RejectLabel.OnClick := @RejectLabelClick;

  // ── Info Before page ──
  WizardForm.InfoBeforePage.Color := clBlack;
  WizardForm.InfoBeforeMemo.Color := $00181818;
  WizardForm.InfoBeforeMemo.UseRichEdit := False;
  WizardForm.InfoBeforeMemo.Font.Color := clWhite;
  WizardForm.InfoBeforeMemo.Font.Name := 'Consolas';
  WizardForm.InfoBeforeMemo.Font.Size := 9;
  WizardForm.InfoBeforeClickLabel.Font.Color := clWhite;

  // ── Select Tasks page ──
  WizardForm.SelectTasksPage.Color := clBlack;
  WizardForm.TasksList.Color := clBlack;
  WizardForm.TasksList.Font.Color := clWhite;

  // ── Ready page ──
  WizardForm.ReadyMemo.Color := $00181818;
  WizardForm.ReadyMemo.Font.Color := clWhite;
  WizardForm.ReadyMemo.Font.Name := 'Consolas';
  WizardForm.ReadyMemo.Font.Size := 9;

  // ── Installing page ──
  WizardForm.StatusLabel.Font.Color := clWhite;
  WizardForm.FilenameLabel.Font.Color := $00888888;

  // ── Run list (post-install) ──
  WizardForm.RunList.Color := clBlack;
  WizardForm.RunList.Font.Color := clWhite;

  // ══════════════════════════════════════════════════════════════════
  //  VERSION FOOTER (bottom-left)
  // ══════════════════════════════════════════════════════════════════
  VersionLabel := TNewStaticText.Create(WizardForm);
  VersionLabel.Parent := WizardForm;
  VersionLabel.Caption := 'v{#SetupSetting("AppVersion")}  |  MIT License';
  VersionLabel.Font.Color := $00555555;
  VersionLabel.Font.Size := 7;
  VersionLabel.Font.Name := 'Consolas';
  VersionLabel.Color := clBlack;
  VersionLabel.Left := 10;
  VersionLabel.Top := WizardForm.ClientHeight - 18;
  VersionLabel.AutoSize := True;

  // ══════════════════════════════════════════════════════════════════
  //  CLICKABLE GITHUB URL (bottom-right, orange underlined)
  // ══════════════════════════════════════════════════════════════════
  URLLabel := TNewStaticText.Create(WizardForm);
  URLLabel.Parent := WizardForm;
  URLLabel.Caption := 'github.com/mohamedcherif-pixel';
  URLLabel.Font.Color := $003399FF;
  URLLabel.Font.Size := 7;
  URLLabel.Font.Name := 'Consolas';
  URLLabel.Font.Style := [fsUnderline];
  URLLabel.Cursor := crHand;
  URLLabel.Color := clBlack;
  URLLabel.AutoSize := True;
  URLLabel.Left := WizardForm.ClientWidth - 230;
  URLLabel.Top := WizardForm.ClientHeight - 18;
  URLLabel.OnClick := @URLLabelClick;

  // ══════════════════════════════════════════════════════════════════
  //  ELAPSED TIME COUNTER (shown during installation)
  // ══════════════════════════════════════════════════════════════════
  ElapsedLabel := TNewStaticText.Create(WizardForm);
  ElapsedLabel.Parent := WizardForm.InnerPage;
  ElapsedLabel.Caption := 'Elapsed: 0:00';
  ElapsedLabel.Font.Color := $00888888;
  ElapsedLabel.Font.Size := 9;
  ElapsedLabel.Font.Name := 'Consolas';
  ElapsedLabel.Color := clBlack;
  ElapsedLabel.Left := 10;
  ElapsedLabel.Top := WizardForm.InnerPage.Height - 30;
  ElapsedLabel.AutoSize := True;
  ElapsedLabel.Visible := False;
  InstallStartTick := 0;
  PulseCounter := 0;

  // ══════════════════════════════════════════════════════════════════
  //  MARQUEE SCROLLING TEXT (green, loops across bottom)
  // ══════════════════════════════════════════════════════════════════
  MarqueeLabel := TNewStaticText.Create(WizardForm);
  MarqueeLabel.Parent := WizardForm;
  MarqueeLabel.Caption := '  ★  TheVault PC Optimizer v1.1.7  ★  344 Tools & Tweaks  ★  Free & Open Source  ★  MIT License  ★  github.com/mohamedcherif-pixel  ★  ';
  MarqueeLabel.Font.Color := clLime;
  MarqueeLabel.Font.Size := 8;
  MarqueeLabel.Font.Name := 'Consolas';
  MarqueeLabel.Color := clBlack;
  MarqueeLabel.AutoSize := True;
  MarqueeLabel.Top := 0;
  MarqueePos := WizardForm.ClientWidth;

  // ══════════════════════════════════════════════════════════════════
  //  PROGRESS PERCENTAGE (big, visible during install only)
  // ══════════════════════════════════════════════════════════════════
  ProgressLabel := TNewStaticText.Create(WizardForm);
  ProgressLabel.Parent := WizardForm.InnerPage;
  ProgressLabel.Caption := '0%';
  ProgressLabel.Font.Color := clLime;
  ProgressLabel.Font.Size := 28;
  ProgressLabel.Font.Style := [fsBold];
  ProgressLabel.Font.Name := 'Consolas';
  ProgressLabel.Color := clBlack;
  ProgressLabel.AutoSize := True;
  ProgressLabel.Left := WizardForm.InnerPage.Width - 120;
  ProgressLabel.Top := 10;
  ProgressLabel.Visible := False;

  // ══════════════════════════════════════════════════════════════════
  //  ANIMATION 1: Full side panel (Welcome & Finished pages)
  // ══════════════════════════════════════════════════════════════════
  Anim1Image := TBitmapImage.Create(WizardForm);
  Anim1Image.Parent := WizardForm.WelcomePage;
  Anim1Image.Left := 0;
  Anim1Image.Top := 0;
  Anim1Image.Width := WizardForm.WizardBitmapImage.Width;
  Anim1Image.Height := WizardForm.WizardBitmapImage.Height;
  Anim1Image.Stretch := True;
  WizardForm.WizardBitmapImage.Hide;

  // ══════════════════════════════════════════════════════════════════
  //  ANIMATION 2: BIG 130x130 floating panel (on top of everything)
  // ══════════════════════════════════════════════════════════════════
  Anim2Container := TPanel.Create(WizardForm);
  Anim2Container.Parent := WizardForm;
  Anim2Container.Left := WizardForm.ClientWidth - 145;
  Anim2Container.Top := 2;
  Anim2Container.Width := 135;
  Anim2Container.Height := 135;
  Anim2Container.Color := $00111111;
  Anim2Container.BevelOuter := bvNone;

  Anim2Image := TBitmapImage.Create(WizardForm);
  Anim2Image.Parent := Anim2Container;
  Anim2Image.Left := 2;
  Anim2Image.Top := 2;
  Anim2Image.Width := 130;
  Anim2Image.Height := 130;
  Anim2Image.Stretch := True;
  WizardForm.WizardSmallBitmapImage.Hide;
  Anim2Container.BringToFront;

  Frame1 := 0;
  Frame2 := 0;

  // Load initial animation frames
  ExtractTemporaryFile('bmp_anim1_0.bmp');
  Anim1Image.Bitmap.LoadFromFile(ExpandConstant('{tmp}\bmp_anim1_0.bmp'));
  ExtractTemporaryFile('bmp_anim2_0.bmp');
  Anim2Image.Bitmap.LoadFromFile(ExpandConstant('{tmp}\bmp_anim2_0.bmp'));

  // ── Start animation timer (100ms per frame) ──
  SetTimer(0, 1, 100, CreateCallback(@TimerProc));
  TimerActive := True;
end;

procedure CurPageChanged(CurPageID: Integer);
begin
  if CurPageID = wpWelcome then begin
    WizardForm.MainPanel.Visible := False;
    Anim2Container.Visible := False;
    Anim1Image.Parent := WizardForm.WelcomePage;
    Anim1Image.Visible := True;
    ElapsedLabel.Visible := False;
  end else if CurPageID = wpFinished then begin
    WizardForm.MainPanel.Visible := False;
    Anim2Container.Visible := False;
    Anim1Image.Parent := WizardForm.FinishedPage;
    Anim1Image.Visible := True;
    ElapsedLabel.Visible := False;
  end else begin
    WizardForm.MainPanel.Visible := True;
    Anim1Image.Visible := False;
    Anim2Container.Visible := True;
    Anim2Container.BringToFront;
    if CurPageID = wpInstalling then begin
      InstallStartTick := GetTickCount;
      ElapsedLabel.Visible := True;
      ProgressLabel.Visible := True;
    end else begin
      ElapsedLabel.Visible := False;
      ProgressLabel.Visible := False;
    end;
  end;
end;

procedure CancelButtonClick(CurPageID: Integer; var Cancel, Confirm: Boolean);
begin
  Confirm := False;
  Cancel := (MsgBox('Are you sure you want to cancel the installation?', mbConfirmation, MB_YESNO) = IDYES);
end;

procedure DeinitializeSetup;
begin
  if TimerActive then KillTimer(0, 1);
end;
