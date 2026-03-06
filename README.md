<p align="center">
  <img src="gamephoto.ico" alt="TheVault Logo" width="128"/>
</p>

<h1 align="center">TheVault PC Optimizer</h1>

<p align="center">
  <strong>Open-source Windows optimization toolkit with 344 tweaks & tools</strong>
</p>

<p align="center">
  <img alt="Version" src="https://img.shields.io/badge/version-1.1.7-blue"/>
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green"/>
  <img alt="Platform" src="https://img.shields.io/badge/platform-Windows%2010%2F11-lightgrey"/>
  <img alt="Python" src="https://img.shields.io/badge/python-3.10%2B-yellow"/>
  <img alt="GitHub Actions" src="https://img.shields.io/github/actions/workflow/status/mohamedcherif-pixel/TheVault-PC-Optimizer/deploy.yml?label=build"/>
</p>

---

## What is this?

A free, open-source, single-file PC optimizer that applies **172 verified tweaks** and installs **172 curated tools** — all through a clean dark-themed GUI. Every tool install uses official `winget` package IDs, every registry tweak uses documented Windows keys, and most tweaks include a **revert button** to undo changes.

**No ads. No telemetry. No bundled crapware. No cloud account required.**

## Features

| Feature | Details |
|---------|---------|
| **12 tweak categories** | System Core, GPU & Gaming, Timer & Clock, Network, Power & CPU, MSI & Interrupts, Mouse & Input, Privacy & Telemetry, Services & Tasks, Cleanup, UI & QoL, Tools & Downloads |
| **172 system tweaks** | Registry, bcdedit, powercfg, netsh, sc, schtasks — all documented |
| **172 tool installs** | Via `winget` with verified package IDs |
| **6 languages** | English, French, Tounsi, Spanish, German, Arabic |
| **Risk levels** | Every tweak labeled SAFE / LOW / MEDIUM / HIGH with color coding |
| **Revert support** | Most tweaks have one-click revert to undo changes |
| **Auto-updater** | Checks GitHub releases for new versions |
| **Dark theme** | Modern VS Code-inspired dark UI |
| **AI assistant** | Built-in AI chat for PC help (free API providers) |
| **System scanner** | Detects current system state and recommendations |

## Download

### Option 1: Installer (Recommended)
Download **TheVault_Setup.exe** from the [latest release](https://github.com/mohamedcherif-pixel/TheVault-PC-Optimizer/releases/latest).

### Option 2: Portable EXE
Download **TheVault_Optimizer.exe** — no installation needed, runs directly.

### Verify Your Download
Every release includes a `CHECKSUMS.txt` file with SHA256 hashes. Verify with PowerShell:
```powershell
(Get-FileHash .\TheVault_Optimizer.exe -Algorithm SHA256).Hash
```
Compare the output with the hash in `CHECKSUMS.txt`.

## How to Run from Source

```bash
# Clone the repository
git clone https://github.com/mohamedcherif-pixel/TheVault-PC-Optimizer.git
cd TheVault-PC-Optimizer

# Install dependencies
pip install pygame

# Run (requires Administrator)
python main.py
```

> **Note:** The app requires Administrator privileges to apply system tweaks. It will prompt for UAC elevation on launch.

## Build from Source

```bash
# Install build dependencies
pip install pyinstaller pygame

# Build standalone EXE
pyinstaller TheVault_Optimizer.spec

# Output: dist/TheVault_Optimizer.exe
```

The `.spec` file includes a `version_info.txt` that embeds proper Windows metadata (company name, version, copyright) into the EXE — visible in File Properties.

## Build the Installer

1. Download and install [Inno Setup](https://jrsoftware.org/isinfo.php)
2. Open `setup.iss` in Inno Setup
3. Compile — produces `Output/TheVault_Setup.exe`

## How Tweaks Work

- **Registry tweaks**: Use `reg add` to modify documented Windows registry paths
- **Tool installs**: Use `winget install --id <ID>` with official Microsoft winget package IDs
- **Service tweaks**: Use `sc config` / `sc stop` to disable Windows services
- **Network tweaks**: Use `netsh` to configure TCP/IP stack parameters
- **Power tweaks**: Use `powercfg` to modify power plan settings
- **Boot tweaks**: Use `bcdedit` to configure boot-time parameters

## Safety

- Every tweak has a **risk level** (SAFE, LOW, MEDIUM, HIGH)
- SAFE tweaks have zero risk and are fully reversible
- HIGH tweaks trade security for performance — read the description first
- Most tweaks include a **revert** button to undo changes with one click
- **No data is collected** — the app runs 100% offline (except tool downloads and update checks)
- Source code is fully open — read every line before trusting it

## License

[MIT License](LICENSE) — free to use, modify, and distribute.

## Contact

- **GitHub**: [mohamedcherif-pixel](https://github.com/mohamedcherif-pixel)
- **Email**: mohamedcherif.dev@outlook.com
- **Issues**: [Report a bug](https://github.com/mohamedcherif-pixel/TheVault-PC-Optimizer/issues)
