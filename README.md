<p align="center">
  <img src="gamephoto.ico" alt="NormieTools Logo" width="128"/>
</p>

<h1 align="center">NormieTools</h1>

<p align="center">
  <strong>Free, open-source Windows optimizer — 174 system tweaks + 173 one-click tool installs</strong>
</p>

<p align="center">
  <img alt="Version" src="https://img.shields.io/badge/version-1.1.7-blue"/>
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green"/>
  <img alt="Platform" src="https://img.shields.io/badge/platform-Windows%2010%2F11-lightgrey"/>
  <img alt="Python" src="https://img.shields.io/badge/python-3.10%2B-yellow"/>
  <img alt="GitHub Actions" src="https://img.shields.io/github/actions/workflow/status/mohamedcherif-pixel/TheVault-PC-Optimizer/deploy.yml?label=build"/>
</p>

<p align="center">
  No ads · No telemetry · No bundled crapware · No cloud account required
</p>

---

## Table of Contents

- [What is NormieTools?](#what-is-normietools)
- [Download](#download)
- [Features at a Glance](#features-at-a-glance)
- [Tweak Categories](#tweak-categories)
- [Tool Downloads](#tool-downloads)
- [Built-in AI Assistant](#built-in-ai-assistant)
- [System Scanner](#system-scanner)
- [Multi-Language Support](#multi-language-support)
- [Background Music](#background-music)
- [Feedback System](#feedback-system)
- [Auto-Updater](#auto-updater)
- [How Tweaks Work](#how-tweaks-work)
- [Safety & Risk Levels](#safety--risk-levels)
- [Revert System](#revert-system)
- [SmartScreen Warning](#smartscreen-warning)
- [Run from Source](#run-from-source)
- [Build from Source](#build-from-source)
- [Build the Installer](#build-the-installer)
- [CI/CD Pipeline](#cicd-pipeline)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## What is NormieTools?

NormieTools is a **single-file** Windows PC optimizer built with Python and tkinter. It gives you **174 system tweaks** (registry, bcdedit, powercfg, netsh, services, scheduled tasks) and **173 curated tool installs** (via `winget`) — all in one clean, dark-themed GUI.

Every registry path is documented. Every tool install uses an official `winget` package ID. Most tweaks have a **one-click revert button** so you can undo any change instantly. Before applying tweaks, the app automatically creates a **System Restore Point** as a safety net.

The entire application is a single Python file (`main.py`, ~7000 lines) that compiles into a standalone `.exe` with PyInstaller.

---

## Download

### Option 1: Installer (Recommended)

Download **NormieTools_Setup.exe** from the [latest release](https://github.com/mohamedcherif-pixel/TheVault-PC-Optimizer/releases/latest).

The installer features a custom animated setup wizard powered by [Inno Setup](https://jrsoftware.org/isinfo.php) with frame-by-frame BMP animations (76 + 9 frames).

### Option 2: Portable EXE

Download **NormieTools.exe** from the [latest release](https://github.com/mohamedcherif-pixel/TheVault-PC-Optimizer/releases/latest) — no installation needed, runs directly from any folder.

### Verify Your Download

Every release includes a `CHECKSUMS.txt` with SHA256 hashes. Verify with PowerShell:

```powershell
(Get-FileHash .\NormieTools.exe -Algorithm SHA256).Hash
```

Compare the output with the hash in `CHECKSUMS.txt`.

---

## Features at a Glance

| Feature | Details |
|---------|---------|
| **174 system tweaks** | Registry, bcdedit, powercfg, netsh, sc, schtasks — each with a description |
| **173 tool installs** | One-click install via `winget` with verified Microsoft package IDs |
| **12 tweak categories** | Organized by area: System Core, GPU, Network, Privacy, and more |
| **8 tool subcategories** | Latency, Hardware, Security, Diagnostics, Files, UI, Dev, Productivity |
| **6 languages** | English, French, Tounsi (Tunisian Arabic), Spanish, German, Arabic |
| **Risk levels** | SAFE / LOW / MEDIUM / HIGH — color-coded for every tweak |
| **One-click revert** | Most tweaks include a revert button to undo changes instantly |
| **System Restore Point** | Auto-created before applying tweaks |
| **System scanner** | Detects which tweaks are already applied at startup |
| **AI assistant** | Built-in chat powered by free AI APIs (Groq, Gemini, Cerebras, Cohere) |
| **Auto-updater** | Checks GitHub releases and hot-patches the running EXE |
| **Dark theme** | Pure black UI with red + cyan accents |
| **Background music** | Optional looping track with animated now-playing marquee |
| **In-app feedback** | Star rating + message sent directly to the developer |
| **Select / Deselect all** | Batch tweak selection with one click |
| **Search bar** | Filter through 173 tools instantly |

---

## Tweak Categories

NormieTools organizes 174 tweaks into **12 categories**, each with its own sidebar tab:

### 1. ⚙ System Core
Core Windows kernel and memory optimizations. Includes disabling VBS/HVCI, Spectre/Meltdown mitigations, page combining, CFG, memory compression, Fault Tolerant Heap, UAC, DEP, ASLR, SEHOP, prefetcher/superfetch, fullscreen optimizations, and elevating CSRSS/DWM priority.

### 2. 🎮 GPU & Gaming
GPU and gaming-specific tweaks. Hardware-accelerated GPU scheduling, GPU preemption control, TDR timeout increase, NVIDIA P-State forcing, Game DVR/Game Bar disabling, MPO disabling, VRR control, MMCSS priority, Windows Ink workspace, exclusive fullscreen mode.

### 3. ⏱ Timer & Clock
System timer precision tweaks. Dynamic tick control, TSC timer forcing (HPET removal), global timer resolution requests, enhanced TSC sync for AMD multi-CCX chips, boot timeout elimination.

### 4. 🌐 Network
TCP/IP stack optimization. Nagle's algorithm disable, network throttling removal, SystemResponsiveness tuning, RSS/DCA enabling, TCP timestamps/ECN control, TCP Fast Open, DNS cache tuning, congestion control (CUBIC), large send offload, receive segment coalescing, NetBIOS disable.

### 5. ⚡ Power & CPU
Power plan and CPU scheduling. Ultimate Performance plan activation, sleep/display/disk timeout zeroing, hibernation & fast startup disable, USB selective suspend disable, USB controller power saving, processor idle/parking control.

### 6. 📡 MSI & Interrupts
Low-level interrupt routing. MSI mode on all PCI devices, device priority elevation, interrupt affinity policies, GPU/NIC interrupt optimization.

### 7. 🖱 Mouse & Input
Input latency optimization. Mouse acceleration curves, pointer precision override, keyboard response tuning, palm rejection control, touchpad/pen optimizations.

### 8. 🔒 Privacy & Telemetry
Disable Windows data collection. Telemetry, advertising ID, activity history, feedback frequency, diagnostic data, location tracking, camera/microphone access, clipboard history, online speech recognition, inking/typing personalization.

### 9. 🔧 Services & Tasks
Disable background services and scheduled tasks. Windows Search indexer, SysMain, DiagTrack, Connected User Experiences, Windows Error Reporting, Print Spooler, Fax, Remote Registry, retail demo, and more.

### 10. 🧹 Cleanup
System cleanup operations. Temp files, Windows Update cache, font cache, thumbnail cache, crash dumps, DNS cache flush, prefetch clearing, quick shutdown delays.

### 11. 🖥 UI & QoL
Visual and quality-of-life tweaks. Taskbar cleanup (People, Chat, Widgets), Bing search removal, context menu restoration (Win11), verbose status messages, snap layouts, file extensions visibility, dark mode enforcement, animation disabling.

### 12. 🔽 Tools & Downloads
The 173 curated tool installs (see below).

---

## Tool Downloads

173 tools installable with one click via `winget`, organized into **8 subcategories**:

### ⚡ Latency & Performance (29 tools)
LatencyMon, Process Lasso, ParkControl, ThrottleStop, RTSS, CapFrameX, MSI Afterburner, Mem Reduct, CompactGUI, CRU, Quick CPU, Special K, Intel PresentMon, NVIDIA FrameView, AMD OCAT, BenchMate, Intel XTU, UXTU, TweakPower, NetLimiter, ASIO4ALL, REAL, Core-to-Core Latency, Processes Priority Mgr, RAMMap, Windows Memory Cleaner, DNS Jumper, OCCT, FurMark

### 🔧 Hardware & Monitoring (14 tools)
HWiNFO, CPU-Z, GPU-Z, HWMonitor, CrystalDiskInfo, CrystalDiskMark, FanControl, LibreHardwareMonitor, OpenRGB, TrafficMonitor, Twinkle Tray, Monitorian, Core Temp, AIDA64

### 🛡 Security & Privacy (16 tools)
O&O ShutUp10++, Sophia Script, privacy.sexy, simplewall, Portmaster, GlassWire, WPD, SophiApp, Sandboxie-Plus, KeePassXC, Bitwarden, Malwarebytes, Brave Browser, WireGuard, Nmap, Wireshark

### 🔍 System Diagnostics (18 tools)
Process Explorer, Autoruns, Process Monitor, Sysmon, BlueScreenView, ShellExView, AppReadWriteCounter, FullEventLogView, TCPView, System Informer, RegCool, DiskCountersView, NetworkCountersWatch, WhatIsHang, USBDeview, Wireshark, HxD, MediaInfo

### 📦 Files & Drivers (26 tools)
7-Zip, NanaZip, Everything, WizTree, WizFile, dupeGuru, Bulk Rename Utility, Revo Uninstaller, NVCleanstall, DDU, Snappy Driver Installer, Bulk Crap Uninstaller, Czkawka, NTLite, WinSetView, O&O AppBuster, BleachBit, QTTabBar, PatchCleaner, SpaceSniffer, WinDirStat, FastCopy, TreeSize Free, File Converter, WinSCP, Double Commander

### 🖥 UI & Desktop (20 tools)
ExplorerPatcher, TranslucentTB, ModernFlyouts, MacType, GlazeWM, EarTrumpet, SoundVolumeView, AltSnap, SuperF4, carnac, SoundSwitch, Windhawk, Nilesoft Shell, Seelen UI, komorebi, Sizer, SharpKeys, ContextMenuManager, Lively Wallpaper, Rainmeter, ImageGlass

### 🛠 Dev & Power Tools (20 tools)
PowerToys, DevToys, x64dbg, Resource Hacker, Dependencies, AutoHotkey, Notepad++, ShareX, dnSpy, PE-bear, WinMerge, Textify, ZoomIt, OpenHashTab, Git, Windows Terminal, PowerShell 7, Postman, PuTTY, Clink

### 📱 Productivity & Media (30 tools)
Flow Launcher, QuickLook, Ditto Clipboard, UniGetUI, LosslessCut, Rufus, Ventoy, Espanso, LocalSend, ScreenToGif, Flameshot, Qalculate!, scrcpy, VLC, OBS Studio, HandBrake, Audacity, GIMP, Obsidian, Joplin, KDE Connect, Sumatra PDF, Kdenlive, foobar2000, MPC-HC, yt-dlp, MKVToolNix, qBittorrent, Paint.NET

All tools use **searchable names** — type in the built-in search bar to filter instantly.

---

## Built-in AI Assistant

NormieTools includes a built-in AI chat that helps you troubleshoot PC issues and recommends relevant tweaks/tools from the app's library.

- **Multi-provider fallback chain**: Groq → Cerebras → Gemini → Cohere — if one provider is rate-limited, the next one is tried instantly
- **Models used**: Llama 3.3 70B, Qwen3-32B, Llama 3.1 8B, Gemini 2.5 Flash/Pro, Cohere Command A
- **Context-aware**: The AI knows every tweak and tool in the app
- **Scan commands**: The AI can trigger real-time system scans (processes, startup programs, disk usage, temperatures) to diagnose issues
- **Chat history**: Keeps the last 20 messages for context continuity
- **100% free**: Uses free-tier API keys — no account or payment needed from the user

---

## System Scanner

On startup, NormieTools scans your system to detect which tweaks are **already applied**. It checks:

- **Registry values**: Reads current HKLM/HKCU keys for each tweak
- **bcdedit settings**: Parses boot configuration for timer, DEP, VBS settings
- **PowerShell queries**: Checks memory compression state, network adapter settings, power plan, sleep timeouts
- **Service states**: Detects which services are running or disabled

Already-applied tweaks show a **green checkmark** ✅ in the UI, so you know exactly what's been changed on your system.

---

## Multi-Language Support

The entire UI is translated into **6 languages**:

| Language | Code | Notes |
|----------|------|-------|
| English | `en` | Default |
| Français | `fr` | French |
| Tounsi | `tn` | Tunisian Arabic dialect — casual, conversational tone |
| Español | `es` | Spanish |
| Deutsch | `de` | German |
| العربية | `ar` | Standard Arabic |

All tweak names, descriptions, risk labels, buttons, dialogs, and status messages are translated. Switch languages instantly from the dropdown in the header bar.

---

## Background Music

NormieTools plays an optional background track ("Dark Fantasy" by shahi77) on loop with:

- **Toggle button** in the header bar (🔊 ON / 🔇 OFF)
- **Animated marquee** showing "♫ NOW PLAYING: Dark Fantasy - shahi77 ♫" scrolling across the header
- Powered by `pygame.mixer` at 22050 Hz, volume set to 35%
- Gracefully skipped if `pygame` is not available

---

## Feedback System

Built-in feedback dialog with:

- ⭐ **1-5 star rating** (interactive star icons in the header bar)
- **Feedback types**: Bug Report, Feature Request, General
- **Message box** for detailed feedback
- Sent via **Brevo SMTP API** directly to the developer
- Threaded send — no UI freeze while submitting

---

## Auto-Updater

NormieTools checks for new versions on every launch:

1. Queries the [GitHub Releases API](https://github.com/mohamedcherif-pixel/TheVault-PC-Optimizer/releases/latest)
2. Compares the latest tag with the current `APP_VERSION`
3. If a newer version exists, prompts the user with a Yes/No dialog
4. Downloads the new `NormieTools.exe` with a progress bar overlay
5. Verifies the download size matches `Content-Length`
6. **Hot-patches** the running executable — replaces the current `.exe` and restarts

---

## How Tweaks Work

NormieTools uses standard Windows administration commands. No custom drivers, no kernel patches, no DLL injection.

| Method | Command | Example |
|--------|---------|---------|
| Registry | `reg add` / `reg delete` | Disable Game DVR via `HKCU\...\GameDVR` |
| Boot config | `bcdedit /set` | Force TSC timer, disable dynamic tick |
| Power | `powercfg /change` | Set sleep timeout to 0 |
| Network | `netsh int tcp set` | Enable TCP Fast Open |
| Services | `sc config ... start=disabled` | Stop SysMain, DiagTrack |
| Tasks | `schtasks /change /disable` | Disable telemetry scheduled tasks |
| PowerShell | `powershell -Command` | Disable memory compression, enable restore |
| Tool installs | `winget install --id` | Install with verified Microsoft package IDs |

Every command runs in a subprocess with proper error handling. Failed commands are reported but don't block other tweaks.

---

## Safety & Risk Levels

Every tweak is labeled with a risk level:

| Level | Color | Meaning |
|-------|-------|---------|
| **SAFE** | 🟢 Green | Zero risk. Cosmetic or fully reversible. |
| **LOW** | 🟡 Yellow | Minimal risk. Recommended for most users. |
| **MEDIUM** | 🟠 Orange | Moderate trade-offs. Read the description. |
| **HIGH** | 🔴 Red | Trades security for performance. Understand the consequences. |

### Before applying tweaks:
- A **System Restore Point** is automatically created
- A confirmation dialog lists every selected tweak with risk levels
- You must click "Proceed" to continue

### HIGH-risk tweaks include:
- Disabling VBS / HVCI / Core Isolation (5-10% performance gain, reduces VM security)
- Disabling Spectre / Meltdown mitigations (2-8% gain, CPU vulnerability exposure)
- Disabling DEP, ASLR, SEHOP (extreme security risk — for benchmarking only)
- Disabling UAC (removes elevation prompts entirely)

---

## Revert System

Most tweaks include **reverse commands** that restore the original Windows defaults:

- Click the **↩ Revert** button next to any applied tweak
- The revert runs the exact inverse registry/bcdedit/service commands
- Reverted tweaks update their status in real-time in the UI
- System Restore is also available as a fallback via Windows Recovery

---

## SmartScreen Warning

Since NormieTools is not code-signed, Windows Defender SmartScreen will show a warning when you first run it:

1. Click **"More info"**
2. Click **"Run anyway"**

This is standard behavior for any unsigned open-source application. The source code is fully available for inspection, and every release includes SHA256 checksums for verification.

---

## Run from Source

```bash
# Clone the repository
git clone https://github.com/mohamedcherif-pixel/TheVault-PC-Optimizer.git
cd TheVault-PC-Optimizer

# Install dependencies
pip install pygame requests

# Run (requires Administrator)
python main.py
```

> **Note:** The app requires **Administrator privileges** to apply system tweaks. Right-click → "Run as administrator", or it will prompt for UAC elevation automatically.

> **Note:** `pygame` is optional — the app works without it, but background music will be unavailable.

---

## Build from Source

```bash
# Install build dependencies
pip install pyinstaller pygame requests

# Build standalone EXE
pyinstaller NormieTools.spec

# Output: dist/NormieTools.exe
```

The `NormieTools.spec` file:
- Bundles `Dark Fantasy - shahi77.mp3` for background music
- Uses `gamephoto.ico` as the application icon
- Embeds `version_info.txt` with Windows PE metadata (company name, version, copyright)
- Produces a single-file executable

---

## Build the Installer

The installer is built with [Inno Setup](https://jrsoftware.org/isinfo.php):

1. Install Inno Setup 6+
2. Open `setup.iss` in the Inno Setup Compiler
3. Click Compile → produces `Output/NormieTools_Setup.exe`

The installer features:
- Custom animated setup wizard with frame-by-frame BMP animations
- License agreement page
- Install directory selection (defaults to `Program Files\NormieTools`)
- Desktop and Start Menu shortcuts
- Uninstaller included

---

## CI/CD Pipeline

Every push to `main` automatically triggers a [GitHub Actions workflow](https://github.com/mohamedcherif-pixel/TheVault-PC-Optimizer/actions):

1. **Checkout** the repository
2. **Set up Python 3.13** on `windows-latest`
3. **Install dependencies** (`pyinstaller`, `pygame`, `requests`)
4. **Build** the standalone EXE with PyInstaller
5. **Build** the installer with Inno Setup (`iscc setup.iss`)
6. **Generate SHA256 checksums** for both artifacts
7. **Create a GitHub Release** with the version tag extracted from `main.py`
8. **Upload artifacts**: `NormieTools.exe`, `NormieTools_Setup.exe`, `CHECKSUMS.txt`

No manual release process — just push to main and the build + release happens automatically.

---

## Project Structure

```
├── main.py                  # The entire application (~7000 lines)
├── NormieTools.spec          # PyInstaller build spec
├── setup.iss                # Inno Setup installer script
├── version_info.txt         # Windows PE version metadata
├── gamephoto.ico            # Application icon
├── Dark Fantasy - shahi77.mp3  # Background music track
├── normietools_config.json  # Local config (language preference, etc.)
├── LICENSE                  # MIT License
├── README.md                # This file
├── SECURITY.md              # Security disclosure & transparency info
├── INFO_BEFORE.txt          # Pre-install information shown by installer
├── installer_license.txt    # License text shown during install
└── .github/
    └── workflows/
        └── deploy.yml       # CI/CD: auto-build and release on push
```

---

## Contributing

Contributions are welcome! Here's how:

1. **Fork** the repository
2. **Create a branch** for your feature or fix
3. **Make your changes** to `main.py` (the entire app is in one file)
4. **Test** by running `python main.py` as Administrator
5. **Submit a Pull Request** with a clear description

### Ideas for contributions:
- Additional tweaks (with risk level, description, and revert commands)
- New tool additions (must have a valid `winget` package ID)
- Additional language translations
- UI improvements
- Bug fixes

---

## License

[MIT License](LICENSE) — free to use, modify, and distribute.

Copyright © 2024-2026 MedCherif

---

## Contact

- **GitHub**: [mohamedcherif-pixel](https://github.com/mohamedcherif-pixel)
- **Email**: mohamedcherif.dev@outlook.com
- **Issues**: [Report a bug or request a feature](https://github.com/mohamedcherif-pixel/TheVault-PC-Optimizer/issues)
