import os, sys, ctypes, subprocess, threading, time
import tkinter as tk
from tkinter import messagebox
import urllib.request
import json
import winreg
import shlex
import re

# ─── App Version ────────────────────────────────────────────────────────
APP_VERSION = "v1.1.4"
GITHUB_REPO = "mohamedcherif-pixel/TheVault-PC-Optimizer"

pygame = None


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


# ─── Color Palette ──────────────────────────────────────────────────────
BG          = "#1e1e1e"
BG_CARD     = "#252526"
BG_HOVER    = "#2d2d30"
BG_INPUT    = "#333333"
ACCENT      = "#007acc"
ACCENT_DIM  = "#005c99"
ACCENT_GLOW = "#0098ff"
TEXT        = "#cccccc"
TEXT_DIM    = "#999999"
TEXT_DARK   = "#666666"
GREEN       = "#00b894"
YELLOW      = "#fdcb6e"
RED         = "#d63031"
ORANGE      = "#e17055"
BORDER      = "#3e3e42"
SIDEBAR_BG  = "#252526"
SIDEBAR_SEL = "#37373d"


# ─── Risk levels ────────────────────────────────────────────────────────
# User request: show risk level colors (red/green/blue/yellow)
SAFE   = ("SAFE",   "green",      "No risk. Fully reversible, no side effects.")
LOW    = ("LOW",    "blue",       "Minimal risk. Fully reversible.")
MEDIUM = ("MEDIUM", "goldenrod",  "Moderate risk. Reduces a security layer or changes power behavior.")
HIGH   = ("HIGH",   "red",        "Higher risk. Trades security for performance. Understand before applying.")


# ─── All categories and tweaks ──────────────────────────────────────────
CATEGORIES = {
    "System  Core": {
        "icon": "\u2699",
        "tweaks": [
            {
                "name": "Disable VBS / HVCI / Core Isolation",
                "desc": "Removes the hypervisor layer that adds 5-10% overhead to every memory access and kernel call. Microsoft enables this silently on Win11.",
                "risk": HIGH,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\DeviceGuard" /v "EnableVirtualizationBasedSecurity" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\DeviceGuard" /v "RequirePlatformSecurityFeatures" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\DeviceGuard\\Scenarios\\HypervisorEnforcedCodeIntegrity" /v "Enabled" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\DeviceGuard\\Scenarios\\CredentialGuard" /v "Enabled" /t REG_DWORD /d 0 /f',
                    'bcdedit /set hypervisorlaunchtype off',
                ],
            },
            {
                "name": "Disable Spectre / Meltdown Mitigations",
                "desc": "Removes CPU vulnerability patches that add 2-8% overhead to every syscall and context switch. Biggest impact on I/O-heavy workloads.",
                "risk": HIGH,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v "FeatureSettingsOverride" /t REG_DWORD /d 3 /f',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v "FeatureSettingsOverrideMask" /t REG_DWORD /d 3 /f',
                ],
            },
            {
                "name": "Elevate CSRSS & DWM Priority",
                "desc": "Gives the Windows input pipeline (csrss.exe) and frame compositor (dwm.exe) high CPU/IO priority so mouse input and frame flips never wait behind game threads.",
                "risk": LOW,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\csrss.exe\\PerfOptions" /v "CpuPriorityClass" /t REG_DWORD /d 4 /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\csrss.exe\\PerfOptions" /v "IoPriority" /t REG_DWORD /d 3 /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\dwm.exe\\PerfOptions" /v "CpuPriorityClass" /t REG_DWORD /d 4 /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\dwm.exe\\PerfOptions" /v "IoPriority" /t REG_DWORD /d 3 /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\dwm.exe\\PerfOptions" /v "PagePriority" /t REG_DWORD /d 5 /f',
                ],
            },
            {
                "name": "Disable Page Combining (Memory Dedup)",
                "desc": "Stops the background RAM scanner that searches for identical pages. Saves constant CPU cycles; uses slightly more RAM.",
                "risk": LOW,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v "DisablePageCombining" /t REG_DWORD /d 1 /f',
                ],
            },
            {
                "name": "Lock Kernel & Drivers in RAM",
                "desc": "Sets DisablePagingExecutive=1 so the NT kernel and core drivers never get paged to disk. Eliminates micro-stutters from kernel page faults. Needs 8GB+ RAM.",
                "risk": LOW,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v "DisablePagingExecutive" /t REG_DWORD /d 1 /f',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v "LargeSystemCache" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Optimize Win32 CPU Scheduling",
                "desc": "Sets Win32PrioritySeparation to 0x26: short, variable quantum with 3:1 foreground boost. Your active window gets triple the CPU time of background apps.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl" /v "Win32PrioritySeparation" /t REG_DWORD /d 38 /f',
                ],
            },
            {
                "name": "Disable CFG / CET Process Mitigations",
                "desc": "Disables Control Flow Guard system-wide. Removes overhead from every function call in protected processes. 1-3% gain in CPU-heavy DX11 titles.",
                "risk": MEDIUM,
                "cmds": [
                    'powershell -Command "Set-ProcessMitigation -System -Disable CFG"',
                ],
            },
            {
                "name": "Disable Fast Startup (Hybrid Shutdown)",
                "desc": "Fast Startup saves kernel state to disk \u2014 causes driver issues, update failures, and memory leaks that never clear. Disabling forces a clean boot every time.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Power" /v "HiberbootEnabled" /t REG_DWORD /d 0 /f',
                    'powercfg /hibernate off',
                ],
            },
            {
                "name": "Disable Memory Compression",
                "desc": "Stops Windows from compressing RAM. Reduces CPU overhead and latency when accessing memory, at the cost of slightly higher RAM usage.",
                "risk": LOW,
                "cmds": [
                    'powershell -NoProfile -Command "Disable-MMAgent -mc"',
                ],
            },
            {
                "name": "Disable Fault Tolerant Heap (FTH)",
                "desc": "FTH monitors app crashes and applies mitigations that can severely degrade performance of games that crash occasionally.",
                "risk": LOW,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\FTH" /v "Enabled" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Disable UAC (User Account Control)",
                "desc": "Completely disables UAC prompts and virtualization. Removes the secure desktop transition overhead. HIGH RISK for security.",
                "risk": HIGH,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "EnableLUA" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "ConsentPromptBehaviorAdmin" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Disable SmartScreen Filter",
                "desc": "Stops Windows from scanning downloaded files and apps against Microsoft's servers. Reduces launch delays but lowers security.",
                "risk": HIGH,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\System" /v "EnableSmartScreen" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer" /v "SmartScreenEnabled" /t REG_SZ /d "Off" /f',
                ],
            },
            {
                "name": "Disable Windows Defender (Core)",
                "desc": "Attempts to disable Windows Defender real-time protection and anti-spyware. Requires Tamper Protection to be off first.",
                "risk": HIGH,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender" /v "DisableAntiSpyware" /t REG_DWORD /d 1 /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection" /v "DisableRealtimeMonitoring" /t REG_DWORD /d 1 /f',
                ],
            },
            {
                "name": "Disable DEP (Data Execution Prevention)",
                "desc": "Disables DEP globally. Removes hardware-level memory execution checks. Extreme security risk, but removes a layer of memory validation.",
                "risk": HIGH,
                "cmds": [
                    'bcdedit /set nx AlwaysOff',
                ],
            },
            {
                "name": "Disable ASLR (Address Space Layout Randomization)",
                "desc": "Forces memory to load at predictable addresses. Can slightly improve load times and CPU cache hits. Extreme security risk.",
                "risk": HIGH,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v "MoveImages" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Disable System Restore",
                "desc": "Turns off System Restore entirely. Frees up disk space and removes background snapshotting I/O.",
                "risk": HIGH,
                "cmds": [
                    'powershell -NoProfile -Command "Disable-ComputerRestore -Drive \'C:\\\'"',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows NT\\SystemRestore" /v "DisableSR" /t REG_DWORD /d 1 /f',
                ],
            },
            {
                "name": "Disable SEHOP (Exception Chain Validation)",
                "desc": "Disables Structured Exception Handling Overwrite Protection. Removes a security check on every exception thrown by applications. Good for raw performance.",
                "risk": HIGH,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\kernel" /v "DisableExceptionChainValidation" /t REG_DWORD /d 1 /f',
                ],
            },
            {
                "name": "Disable Background Apps Globally",
                "desc": "Stops all UWP/Windows apps from running in the background. Frees up CPU cycles and RAM.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\BackgroundAccessApplications" /v "GlobalUserDisabled" /t REG_DWORD /d 1 /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppPrivacy" /v "LetAppsRunInBackground" /t REG_DWORD /d 2 /f',
                ],
            },
            {
                "name": "Disable Prefetcher & Superfetch (Registry)",
                "desc": "Hard-disables the memory prefetcher at the kernel level. Essential for SSDs to prevent unnecessary write cycles and CPU overhead.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\\PrefetchParameters" /v "EnablePrefetcher" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\\PrefetchParameters" /v "EnableSuperfetch" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Disable Memory Page Trimming",
                "desc": "Prevents Windows from aggressively paging out the memory of minimized applications. Huge for alt-tabbing in and out of games instantly.",
                "risk": LOW,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v "DisablePageTrimming" /t REG_DWORD /d 1 /f',
                ],
            },
        ],
    },
    "GPU  &  Gaming": {
        "icon": "-",
        "tweaks": [
            {
                "name": "Disable GPU Preemption",
                "desc": "Tells the WDDM scheduler not to interrupt the GPU mid-frame. Frame-time variance drops 20-40%. Especially impactful in DX11.",
                "risk": LOW,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers\\Scheduler" /v "EnablePreemption" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers\\Scheduler" /v "VsyncIdleTimeout" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Force True Exclusive Fullscreen",
                "desc": "Disables SwapEffectUpgradeEnable so Windows cannot hijack your game into flip-model DWM composition. Saves 1 frame of latency.",
                "risk": LOW,
                "cmds": [
                    'reg add "HKCU\\System\\GameConfigStore" /v "GameDVR_DXGIHonorFSEWindowsCompatible" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\System\\GameConfigStore" /v "GameDVR_FSEBehavior" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\System\\GameConfigStore" /v "GameDVR_FSEBehaviorMode" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\System\\GameConfigStore" /v "GameDVR_HonorUserFSEBehaviorMode" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\DirectX\\UserGpuPreferences" /v "DirectXUserGlobalSettings" /t REG_SZ /d "SwapEffectUpgradeEnable=0;" /f',
                ],
            },
            {
                "name": "Disable Game DVR & Game Bar",
                "desc": "Kills background GPU recording, screenshot overlay, and FPS counter. Known to cause stuttering even when not actively recording.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\GameDVR" /v "AppCaptureEnabled" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\System\\GameConfigStore" /v "GameDVR_Enabled" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\GameDVR" /v "AllowGameDVR" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Enable HW Accelerated GPU Scheduling",
                "desc": "Lets the GPU manage its own VRAM scheduling instead of going through Windows. Reduces latency on NVIDIA 10-series+ / AMD 5000+.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers" /v "HwSchMode" /t REG_DWORD /d 2 /f',
                ],
            },
            {
                "name": "Increase GPU TDR Timeout to 60s",
                "desc": "Prevents false 'display driver stopped responding' crashes during heavy shader compilation or ray tracing scenes. Default is only 2 seconds.",
                "risk": LOW,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers" /v "TdrDelay" /t REG_DWORD /d 60 /f',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers" /v "TdrDdiDelay" /t REG_DWORD /d 60 /f',
                ],
            },
            {
                "name": "Force NVIDIA P-State P0 (Max Clocks)",
                "desc": "Disables dynamic P-State switching. GPU stays at max clocks, eliminating 10-50ms transition hitches. Higher idle power draw.",
                "risk": LOW,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Class\\{4d36e968-e325-11ce-bfc1-08002be10318}\\0000" /v "DisableDynamicPstate" /t REG_DWORD /d 1 /f',
                ],
            },
            {
                "name": "MMCSS Game Task Max Priority",
                "desc": "Sets GPU Priority=8, Priority=6, Scheduling=High, SFIO=High for the Games MMCSS task. Maximum scheduling priority when Windows detects a game running.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "GPU Priority" /t REG_DWORD /d 8 /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "Priority" /t REG_DWORD /d 6 /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "Scheduling Category" /t REG_SZ /d "High" /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "SFIO Priority" /t REG_SZ /d "High" /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "Background Only" /t REG_SZ /d "False" /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "Clock Rate" /t REG_DWORD /d 10000 /f',
                ],
            },
            {
                "name": "Disable Fullscreen Optimizations (Global)",
                "desc": "Prevents Windows from running fullscreen games in a hidden borderless window with DWM composition \u2014 removes added input lag.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKCU\\System\\GameConfigStore" /v "GameDVR_DXGIHonorFSEWindowsCompatible" /t REG_DWORD /d 1 /f',
                    'reg add "HKCU\\System\\GameConfigStore" /v "GameDVR_FSEBehavior" /t REG_DWORD /d 2 /f',
                ],
            },
            {
                "name": "Disable Multi-Plane Overlay (MPO)",
                "desc": "Fixes stuttering, black screens, and flickering on NVIDIA/AMD GPUs by disabling MPO. Forces standard DWM composition.",
                "risk": LOW,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\Dwm" /v "OverlayTestMode" /t REG_DWORD /d 5 /f',
                ],
            },
            {
                "name": "Disable Variable Refresh Rate (VRR) Globally",
                "desc": "Disables Windows-level VRR which can conflict with G-Sync/FreeSync and cause micro-stutters in windowed games.",
                "risk": LOW,
                "cmds": [
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\DirectX\\UserGpuPreferences" /v "DirectXUserGlobalSettings" /t REG_SZ /d "VRROptimizeEnable=0;" /f',
                ],
            },
            {
                "name": "Disable GPU Energy Driver",
                "desc": "Disables the GPU Energy Driver service which constantly polls the GPU for power metrics, causing DPC latency spikes.",
                "risk": LOW,
                "cmds": [
                    'sc stop gpuenergydrv',
                    'sc config gpuenergydrv start=disabled',
                ],
            },
            {
                "name": "Disable Xbox Game Monitoring",
                "desc": "Stops the Xbox Game Monitoring service from hooking into game processes to track playtime and stats.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\xbgm" /v "Start" /t REG_DWORD /d 4 /f',
                ],
            },
            {
                "name": "Disable Game Bar Presence Writer",
                "desc": "Prevents the Game Bar from writing presence data to the registry every time a game is launched.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\GameDVR" /v "PresenceWriterEnabled" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Disable Windows Ink Workspace",
                "desc": "Disables Windows Ink. Crucial for osu! and FPS players to remove pen/tablet input processing overhead from raw mouse input.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\WindowsInkWorkspace" /v "AllowWindowsInkWorkspace" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Optimize DirectX Graphics Kernel (MaxDxgkIter)",
                "desc": "Limits the DirectX graphics kernel iterations. Reduces the pre-rendered frame queue at the OS level for lower input lag.",
                "risk": LOW,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\DirectX" /v "MaxDxgkIter" /t REG_DWORD /d 1 /f',
                ],
            },
            {
                "name": "Disable DWM Ghosting / Composition (Legacy)",
                "desc": "Disables window ghosting and forces DWM to stop animating unresponsive windows. Helps prevent crashes during heavy game loads.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKCU\\Control Panel\\Desktop" /v "HungAppTimeout" /t REG_SZ /d "1000" /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DWM" /v "DisallowAnimations" /t REG_DWORD /d 1 /f',
                ],
            },
        ],
    },
    "Timer  &  Clock": {
        "icon": "\u23F1",
        "tweaks": [
            {
                "name": "Disable Dynamic Tick",
                "desc": "Stops Windows from collapsing the system timer when CPU idles. Yields rock-solid frame pacing. Laptops: increases power draw when idle.",
                "risk": LOW,
                "cmds": [
                    'bcdedit /set disabledynamictick yes',
                ],
            },
            {
                "name": "Force CPU TSC Timer (Remove HPET)",
                "desc": "Deletes useplatformclock/useplatformtick from BCD so your board falls back to the much faster CPU Time Stamp Counter.",
                "risk": LOW,
                "cmds": [
                    'bcdedit /deletevalue useplatformclock',
                    'bcdedit /deletevalue useplatformtick',
                ],
            },
            {
                "name": "Enable Global Timer Resolution Requests",
                "desc": "Win11 22H2+ broke background timer requests. This restores old behavior so any app requesting 0.5ms resolution gets it system-wide.",
                "risk": LOW,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\kernel" /v "GlobalTimerResolutionRequests" /t REG_DWORD /d 1 /f',
                ],
            },
            {
                "name": "Enhanced TSC Sync Policy (Multi-CCX AMD)",
                "desc": "Forces tighter TSC synchronization between chiplets on Ryzen 3000+. Fixes timer drift that causes inconsistent frame times.",
                "risk": SAFE,
                "cmds": [
                    'bcdedit /set tscsyncpolicy enhanced',
                ],
            },
            {
                "name": "Set Boot Timeout to 0",
                "desc": "Removes the OS selection menu delay. Saves 30 seconds on every boot if you only have one OS installed.",
                "risk": SAFE,
                "cmds": [
                    'bcdedit /timeout 0',
                ],
            },
            {
                "name": "Disable Synthetic Timers",
                "desc": "Disables synthetic timers in BCD. Forces the OS to rely strictly on hardware timers, reducing virtualization overhead.",
                "risk": LOW,
                "cmds": [
                    'bcdedit /set useplatformtick yes',
                    'bcdedit /set useplatformclock false',
                ],
            },
        ],
    },
    "Network": {
        "icon": "-",
        "tweaks": [
            {
                "name": "Disable Nagle's Algorithm (All Interfaces)",
                "desc": "Nagle batches small packets together adding up to 200ms latency. TcpNoDelay=1 + TcpAckFrequency=1 sends every packet immediately.",
                "risk": SAFE,
                "cmds": [
                    'powershell -NoProfile -Command "Get-ChildItem \'HKLM:\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces\' | ForEach-Object { Set-ItemProperty -Path $_.PSPath -Name \'TcpAckFrequency\' -Value 1 -Type DWord -EA SilentlyContinue; Set-ItemProperty -Path $_.PSPath -Name \'TCPNoDelay\' -Value 1 -Type DWord -EA SilentlyContinue; Set-ItemProperty -Path $_.PSPath -Name \'TcpDelAckTicks\' -Value 0 -Type DWord -EA SilentlyContinue }"',
                ],
            },
            {
                "name": "Disable Network Throttling Index",
                "desc": "Windows limits non-multimedia network traffic to ~10 packets/ms. Setting 0xFFFFFFFF removes the cap entirely.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile" /v "NetworkThrottlingIndex" /t REG_DWORD /d 4294967295 /f',
                ],
            },
            {
                "name": "Set SystemResponsiveness to 0%",
                "desc": "Default 20 reserves 20% CPU for background. Setting 0 gives your foreground app 100% CPU priority.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile" /v "SystemResponsiveness" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Enable RSS & DCA, Disable Heuristics",
                "desc": "Receive Side Scaling distributes NIC processing across cores. Direct Cache Access bypasses RAM. Heuristics override your tuning \u2014 disable them.",
                "risk": SAFE,
                "cmds": [
                    'netsh int tcp set global rss=enabled',
                    'netsh int tcp set global dca=enabled',
                    'netsh int tcp set global autotuninglevel=normal',
                    'netsh int tcp set heuristics disabled',
                ],
            },
            {
                "name": "Disable TCP Timestamps & ECN",
                "desc": "Timestamps add 12 bytes per packet. ECN adds per-packet CPU processing. Both negligible benefits for gaming but measurable overhead.",
                "risk": SAFE,
                "cmds": [
                    'netsh int tcp set global timestamps=disabled',
                    'netsh int tcp set global ecncapability=disabled',
                ],
            },
            {
                "name": "Enable TCP Fast Open",
                "desc": "Allows data in the SYN packet for faster connection establishment. Reduces handshake round trips.",
                "risk": SAFE,
                "cmds": [
                    'netsh int tcp set global fastopen=enabled',
                    'netsh int tcp set global fastopenfallback=enabled',
                ],
            },
            {
                "name": "Set TCP Congestion Control to CUBIC",
                "desc": "Changes the TCP congestion provider to CUBIC. Better for high-speed, low-latency connections compared to the default CTCP.",
                "risk": SAFE,
                "cmds": [
                    'netsh int tcp set supplemental template=internet congestionprovider=cubic',
                ],
            },
            {
                "name": "Disable Network Offloads (Chimney & Task)",
                "desc": "Disables TCP Chimney Offload and Task Offload. These often cause DPC latency spikes on consumer NICs (Realtek/Intel).",
                "risk": SAFE,
                "cmds": [
                    'netsh int tcp set global chimney=disabled',
                    'netsh int tcp set global taskoffload=disabled',
                ],
            },
            {
                "name": "Disable IPv6 Tunneling (Teredo, ISATAP, 6to4)",
                "desc": "Disables legacy IPv6 transition technologies that constantly poll the network and create unnecessary virtual adapters.",
                "risk": SAFE,
                "cmds": [
                    'netsh interface teredo set state disabled',
                    'netsh interface isatap set state default state=disabled',
                    'netsh interface ipv6 6to4 set state state=disabled',
                ],
            },
            {
                "name": "Disable WMM (Wi-Fi Multimedia) Power Save",
                "desc": "Stops the Wi-Fi adapter from entering low-power states between packet bursts. Crucial for stable wireless ping.",
                "risk": SAFE,
                "cmds": [
                    'powershell -NoProfile -Command "Get-NetAdapterAdvancedProperty -DisplayName \'*WMM*\' | Set-NetAdapterAdvancedProperty -DisplayValue \'Disabled\' -EA SilentlyContinue"',
                ],
            },
            {
                "name": "Disable Large Send Offload (LSO)",
                "desc": "LSO offloads TCP segmentation to NIC hardware, but many drivers implement it poorly causing high latency and packet loss.",
                "risk": SAFE,
                "cmds": [
                    'powershell -NoProfile -Command "Get-NetAdapter | ForEach-Object { Set-NetAdapterAdvancedProperty -Name $_.Name -DisplayName \'Large Send Offload V2 (IPv4)\' -DisplayValue \'Disabled\' -EA SilentlyContinue; Set-NetAdapterAdvancedProperty -Name $_.Name -DisplayName \'Large Send Offload V2 (IPv6)\' -DisplayValue \'Disabled\' -EA SilentlyContinue }"',
                ],
            },
            {
                "name": "Optimize TCP Port & Timeout Parameters",
                "desc": "MaxUserPort=65534, TcpTimedWaitDelay=30s, MaxFreeTcbs/MaxHashTableSize=65536. Prevents port exhaustion and speeds up port recycling.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v "MaxUserPort" /t REG_DWORD /d 65534 /f',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v "TcpTimedWaitDelay" /t REG_DWORD /d 30 /f',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v "DefaultTTL" /t REG_DWORD /d 64 /f',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v "MaxFreeTcbs" /t REG_DWORD /d 65536 /f',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v "MaxHashTableSize" /t REG_DWORD /d 65536 /f',
                ],
            },
            {
                "name": "Optimize DNS Cache (24h / 5s negative)",
                "desc": "Caches valid DNS entries for 24h (fewer lookups), but retries failed ones after just 5 seconds. Best of both worlds.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Dnscache\\Parameters" /v "MaxCacheTtl" /t REG_DWORD /d 86400 /f',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Dnscache\\Parameters" /v "MaxNegativeCacheTtl" /t REG_DWORD /d 5 /f',
                ],
            },
            {
                "name": "Increase SMB IRPStackSize & Buffer",
                "desc": "Increases I/O Request Packet stack to 30 and receive buffer to 17424 for faster file sharing and network drive access.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\LanmanServer\\Parameters" /v "IRPStackSize" /t REG_DWORD /d 30 /f',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\LanmanServer\\Parameters" /v "SizReqBuf" /t REG_DWORD /d 17424 /f',
                ],
            },
            {
                "name": "Disable Energy Efficient Ethernet (EEE)",
                "desc": "EEE puts the NIC PHY into low-power idle between traffic bursts. Waking it adds 2-5ms latency on every burst. Huge for consistent ping.",
                "risk": SAFE,
                "cmds": [
                    'powershell -NoProfile -Command "Get-NetAdapter | ForEach-Object { Set-NetAdapterAdvancedProperty -Name $_.Name -DisplayName \'Energy-Efficient Ethernet\' -DisplayValue \'Disabled\' -EA SilentlyContinue; Set-NetAdapterAdvancedProperty -Name $_.Name -DisplayName \'Energy Efficient Ethernet\' -DisplayValue \'Disabled\' -EA SilentlyContinue; Set-NetAdapterAdvancedProperty -Name $_.Name -DisplayName \'EEE\' -DisplayValue \'Disabled\' -EA SilentlyContinue }"',
                ],
            },
            {
                "name": "Disable IPv6 Completely",
                "desc": "Disables the IPv6 stack. If your ISP or game doesn't require IPv6, this removes a massive amount of background network polling.",
                "risk": MEDIUM,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip6\\Parameters" /v "DisabledComponents" /t REG_DWORD /d 255 /f',
                ],
            },
            {
                "name": "Disable QoS Packet Scheduler",
                "desc": "Stops Windows from reserving 20% of your bandwidth for Windows Updates and telemetry.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Psched" /v "NonBestEffortLimit" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Disable Receive Segment Coalescing (RSC)",
                "desc": "RSC batches incoming packets. Good for throughput, terrible for latency. Disabling it forces immediate packet processing.",
                "risk": SAFE,
                "cmds": [
                    'netsh int tcp set global rsc=disabled',
                    'powershell -NoProfile -Command "Get-NetAdapter | Disable-NetAdapterRsc -EA SilentlyContinue"',
                ],
            },
            {
                "name": "Disable NetBIOS over TCP/IP",
                "desc": "Disables legacy local network discovery protocols that constantly broadcast packets on your LAN.",
                "risk": SAFE,
                "cmds": [
                    'powershell -NoProfile -Command "Get-WmiObject Win32_NetworkAdapterConfiguration | Where-Object { $_.IPEnabled -eq $true } | ForEach-Object { $_.SetTcpipNetbios(2) }"',
                ],
            },
            {
                "name": "Disable LLMNR (Link-Local Multicast)",
                "desc": "Disables LLMNR, another legacy local name resolution protocol that generates unnecessary broadcast traffic.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows NT\\DNSClient" /v "EnableMulticast" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Disable Smart Name Resolution",
                "desc": "Stops Windows from sending DNS queries to all adapters simultaneously (which leaks DNS queries and wastes bandwidth).",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows NT\\DNSClient" /v "DisableSmartNameResolution" /t REG_DWORD /d 1 /f',
                ],
            },
        ],
    },
    "Power  &  CPU": {
        "icon": "\u26A1",
        "tweaks": [
            {
                "name": "Activate Ultimate Performance Plan",
                "desc": "Hidden power plan that eliminates ALL power-saving delays. Duplicates the scheme and activates High Performance as fallback.",
                "risk": SAFE,
                "cmds": [
                    'powercfg /duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61',
                    'powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c',
                ],
            },
            {
                "name": "Unpark All CPU Cores (100% Min)",
                "desc": "Sets Core Parking minimum to 100% so no cores ever sleep. Eliminates hitching from cores waking up under sudden load.",
                "risk": LOW,
                "cmds": [
                    'powercfg -attributes SUB_PROCESSOR 0cc5b647-c1df-4637-891a-dec35c318583 -ATTRIB_HIDE',
                    'powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR 0cc5b647-c1df-4637-891a-dec35c318583 100',
                    'powercfg /setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR 0cc5b647-c1df-4637-891a-dec35c318583 100',
                    'powercfg /setactive SCHEME_CURRENT',
                ],
            },
            {
                "name": "Disable Processor C-States (Idle Disable)",
                "desc": "Prevents CPU cores from entering C1/C3/C6 sleep states. Each state adds microseconds of wake latency. More heat but zero delay.",
                "risk": LOW,
                "cmds": [
                    'powercfg -attributes SUB_PROCESSOR 5d76a2ca-e8c0-402f-a133-2158492d58ad -ATTRIB_HIDE',
                    'powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR 5d76a2ca-e8c0-402f-a133-2158492d58ad 1',
                    'powercfg /setactive SCHEME_CURRENT',
                ],
            },
            {
                "name": "CPU Min/Max State = 100%",
                "desc": "Forces the processor to always run at maximum frequency. Eliminates frequency scaling delays entirely.",
                "risk": LOW,
                "cmds": [
                    'powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN 100',
                    'powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX 100',
                    'powercfg /setactive SCHEME_CURRENT',
                ],
            },
            {
                "name": "Aggressive Boost Mode + EPP = 0",
                "desc": "Sets boost to aggressive (ramp to max clock instantly) and Energy Performance Preference to 0 (pure performance).",
                "risk": LOW,
                "cmds": [
                    'powercfg -attributes SUB_PROCESSOR be337238-0d82-4146-a960-4f3749d470c7 -ATTRIB_HIDE',
                    'powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR be337238-0d82-4146-a960-4f3749d470c7 2',
                    'powercfg -attributes SUB_PROCESSOR 36687f9e-e3a5-4dbf-b1dc-15eb381c6863 -ATTRIB_HIDE',
                    'powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR 36687f9e-e3a5-4dbf-b1dc-15eb381c6863 0',
                    'powercfg /setactive SCHEME_CURRENT',
                ],
            },
            {
                "name": "Disable Power Throttling",
                "desc": "Windows 10+ throttles background apps to save power. This can cause stuttering if Windows mis-classifies your workload as background.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Power\\PowerThrottling" /v "PowerThrottlingOff" /t REG_DWORD /d 1 /f',
                ],
            },
            {
                "name": "Disable USB Selective Suspend",
                "desc": "Stops Windows from powering down USB devices to save energy. Fixes random mouse/keyboard disconnects and 10ms input spikes.",
                "risk": SAFE,
                "cmds": [
                    'powercfg /setacvalueindex SCHEME_CURRENT 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0',
                    'powercfg /setdcvalueindex SCHEME_CURRENT 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0',
                    'powercfg /setactive SCHEME_CURRENT',
                ],
            },
            {
                "name": "Disable PCI Express ASPM",
                "desc": "Active State Power Management adds latency to PCIe link state transitions. Disabling keeps GPU/NVMe links always active.",
                "risk": LOW,
                "cmds": [
                    'powercfg -attributes SUB_PCIEXPRESS ee12f906-d277-404b-b6da-e5fa1a576df5 -ATTRIB_HIDE',
                    'powercfg /setacvalueindex SCHEME_CURRENT SUB_PCIEXPRESS ee12f906-d277-404b-b6da-e5fa1a576df5 0',
                    'powercfg /setactive SCHEME_CURRENT',
                ],
            },
            {
                "name": "Disable Sleep & Display Timeout",
                "desc": "Prevents the PC and display from ever going to sleep automatically.",
                "risk": SAFE,
                "cmds": [
                    'powercfg /change standby-timeout-ac 0',
                    'powercfg /change monitor-timeout-ac 0',
                ],
            },
            {
                "name": "Disable Disk Sleep",
                "desc": "Prevents hard drives from spinning down. Eliminates the 3-5 second freeze when accessing a sleeping drive.",
                "risk": SAFE,
                "cmds": [
                    'powercfg /change disk-timeout-ac 0',
                ],
            },
            {
                "name": "Disable Connected Standby (Modern Standby)",
                "desc": "Forces S3 sleep instead of S0ix. Prevents the PC from waking up in a backpack, draining battery, and running background tasks while 'asleep'.",
                "risk": LOW,
                "cmds": [
                    'reg add "HKLM\\System\\CurrentControlSet\\Control\\Power" /v "PlatformAoAcOverride" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Disable Hibernation & Fast Startup",
                "desc": "Deletes the hiberfil.sys file (saving GBs of space) and forces a true clean boot every time you shut down, preventing driver rot.",
                "risk": SAFE,
                "cmds": [
                    'powercfg -h off',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Power" /v "HiberbootEnabled" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Disable Dynamic Tick",
                "desc": "Stops Windows from dynamically adjusting the system timer tick rate to save power. Keeps the tick rate constant for smoother DPC execution.",
                "risk": LOW,
                "cmds": [
                    'bcdedit /set disabledynamictick yes',
                ],
            },
        ],
    },
    "MSI  &  Interrupts": {
        "icon": "-",
        "tweaks": [
            {
                "name": "Enable MSI Mode on All PCI Devices",
                "desc": "Switches GPU, NIC, USB, Storage, Audio from legacy shared IRQ lines to private Message Signaled Interrupts. Drastically lowers DPC latency.",
                "risk": LOW,
                "cmds": [
                    'powershell -NoProfile -ExecutionPolicy Bypass -Command "$cats=@(@{C=\'Display\'}, @{C=\'Net\'}, @{C=\'SCSIAdapter\'}, @{C=\'HDC\'}, @{C=\'USB\'}); foreach($c in $cats){Get-PnpDevice -Class $c.C -Status OK -EA SilentlyContinue | ForEach-Object { $mp=\'HKLM:\\SYSTEM\\CurrentControlSet\\Enum\\\'+$_.InstanceId+\'\\Device Parameters\\Interrupt Management\\MessageSignaledInterruptProperties\'; if(!(Test-Path $mp)){New-Item -Path $mp -Force|Out-Null}; Set-ItemProperty -Path $mp -Name \'MSISupported\' -Value 1 -Type DWord -Force}}"',
                ],
            },
            {
                "name": "Disable USB Controller Power Saving",
                "desc": "Sets EnhancedPowerManagement=0, SelectiveSuspend=0 on USB host controllers. Fixes random 10ms input spikes on mice and keyboards.",
                "risk": SAFE,
                "cmds": [
                    'powershell -NoProfile -Command "Get-PnpDevice -Class USB -Status OK -EA SilentlyContinue | Where-Object {$_.FriendlyName -match \'Host Controller|xHCI|eHCI\'} | ForEach-Object { $bp=\'HKLM:\\SYSTEM\\CurrentControlSet\\Enum\\\'+$_.InstanceId+\'\\Device Parameters\'; Set-ItemProperty -Path $bp -Name \'EnhancedPowerManagementEnabled\' -Value 0 -Type DWord -Force -EA SilentlyContinue; Set-ItemProperty -Path $bp -Name \'SelectiveSuspendEnabled\' -Value 0 -Type DWord -Force -EA SilentlyContinue }"',
                ],
            },
            {
                "name": "Set GPU MSI Priority to High",
                "desc": "Forces the GPU's Message Signaled Interrupts to be processed with High priority by the CPU.",
                "risk": LOW,
                "cmds": [
                    'powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-PnpDevice -Class Display -Status OK -EA SilentlyContinue | ForEach-Object { $mp=\'HKLM:\\SYSTEM\\CurrentControlSet\\Enum\\\'+$_.InstanceId+\'\\Device Parameters\\Interrupt Management\\Affinity Policy\'; if(!(Test-Path $mp)){New-Item -Path $mp -Force|Out-Null}; Set-ItemProperty -Path $mp -Name \'DevicePriority\' -Value 3 -Type DWord -Force}"',
                ],
            },
            {
                "name": "Set NIC MSI Priority to High",
                "desc": "Forces the Network Adapter's Message Signaled Interrupts to be processed with High priority by the CPU.",
                "risk": LOW,
                "cmds": [
                    'powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-PnpDevice -Class Net -Status OK -EA SilentlyContinue | ForEach-Object { $mp=\'HKLM:\\SYSTEM\\CurrentControlSet\\Enum\\\'+$_.InstanceId+\'\\Device Parameters\\Interrupt Management\\Affinity Policy\'; if(!(Test-Path $mp)){New-Item -Path $mp -Force|Out-Null}; Set-ItemProperty -Path $mp -Name \'DevicePriority\' -Value 3 -Type DWord -Force}"',
                ],
            },
        ],
    },
    "Mouse  &  Input": {
        "icon": "-",
        "tweaks": [
            {
                "name": "MarkC Mouse Fix (1:1 Raw Input)",
                "desc": "Patches SmoothMouseXCurve/YCurve to linear 1:1 at 100% DPI. Sets MouseSpeed=0, thresholds=0. True zero acceleration for gaming.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKCU\\Control Panel\\Mouse" /v "MouseSpeed" /t REG_SZ /d "0" /f',
                    'reg add "HKCU\\Control Panel\\Mouse" /v "MouseThreshold1" /t REG_SZ /d "0" /f',
                    'reg add "HKCU\\Control Panel\\Mouse" /v "MouseThreshold2" /t REG_SZ /d "0" /f',
                    'reg add "HKCU\\Control Panel\\Mouse" /v "MouseSensitivity" /t REG_SZ /d "10" /f',
                    'reg add "HKCU\\Control Panel\\Mouse" /v "SmoothMouseXCurve" /t REG_BINARY /d 0000000000000000C0CC0C0000000000809919000000000040662600000000000033330000000000 /f',
                    'reg add "HKCU\\Control Panel\\Mouse" /v "SmoothMouseYCurve" /t REG_BINARY /d 0000000000000000000038000000000000007000000000000000A800000000000000400100000000 /f',
                ],
            },
            {
                "name": "Disable Sticky / Filter / Toggle Key Prompts",
                "desc": "Prevents the annoying Shift-5x popup during gaming. Disables the hotkey triggers without removing the accessibility features.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKCU\\Control Panel\\Accessibility\\StickyKeys" /v "Flags" /t REG_SZ /d "506" /f',
                    'reg add "HKCU\\Control Panel\\Accessibility\\Keyboard Response" /v "Flags" /t REG_SZ /d "122" /f',
                    'reg add "HKCU\\Control Panel\\Accessibility\\ToggleKeys" /v "Flags" /t REG_SZ /d "58" /f',
                ],
            },
            {
                "name": "Reduce Menu & Hover Delays to 0",
                "desc": "Sets MenuShowDelay=0, MouseHoverTime=10. Menus and tooltips appear instantly instead of the 400ms default.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKCU\\Control Panel\\Desktop" /v "MenuShowDelay" /t REG_SZ /d "0" /f',
                    'reg add "HKCU\\Control Panel\\Mouse" /v "MouseHoverTime" /t REG_SZ /d "10" /f',
                ],
            },
            {
                "name": "Disable Mouse Pointer Shadow",
                "desc": "Disables the cosmetic drop shadow under the mouse cursor. Saves a tiny amount of GPU rendering overhead.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKCU\\Control Panel\\Desktop" /v "UserPreferencesMask" /t REG_BINARY /d 9012078010000000 /f',
                ],
            },
            {
                "name": "Increase Keyboard Repeat Rate",
                "desc": "Sets KeyboardDelay=0 and KeyboardSpeed=31. Makes holding down a key register much faster.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKCU\\Control Panel\\Keyboard" /v "KeyboardDelay" /t REG_SZ /d "0" /f',
                    'reg add "HKCU\\Control Panel\\Keyboard" /v "KeyboardSpeed" /t REG_SZ /d "31" /f',
                ],
            },
            {
                "name": "Disable Mouse Smoothing (Enhance Pointer Precision)",
                "desc": "Disables Windows built-in mouse acceleration. Essential for consistent muscle memory in FPS games.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKCU\\Control Panel\\Mouse" /v "MouseSpeed" /t REG_SZ /d "0" /f',
                    'reg add "HKCU\\Control Panel\\Mouse" /v "MouseThreshold1" /t REG_SZ /d "0" /f',
                    'reg add "HKCU\\Control Panel\\Mouse" /v "MouseThreshold2" /t REG_SZ /d "0" /f',
                ],
            },
            {
                "name": "Force 1000Hz USB Polling Rate (Legacy)",
                "desc": "Attempts to force legacy USB drivers to poll at 1ms intervals. May not work on modern xHCI controllers but harmless to try.",
                "risk": LOW,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\mouclass\\Parameters" /v "MouseDataQueueSize" /t REG_DWORD /d 100 /f',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\kbdclass\\Parameters" /v "KeyboardDataQueueSize" /t REG_DWORD /d 100 /f',
                ],
            },
        ],
    },
    "Privacy  &  Telemetry": {
        "icon": "-",
        "tweaks": [
            {
                "name": "Disable All Windows Telemetry",
                "desc": "Sets AllowTelemetry=0 via policy and data collection paths. Stops diagnostic and usage data from being sent to Microsoft.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection" /v "AllowTelemetry" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\DataCollection" /v "AllowTelemetry" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppCompat" /v "AITEnable" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\SQMClient\\Windows" /v "CEIPEnable" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Disable Advertising ID & Tracking",
                "desc": "Kills the unique advertising identifier, app launch tracking, and activity history timeline. Pure privacy win.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\AdvertisingInfo" /v "Enabled" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v "Start_TrackProgs" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\System" /v "EnableActivityFeed" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\System" /v "PublishUserActivities" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Disable Location & Sensors",
                "desc": "Turns off Windows location services, Wi-Fi positioning, and location scripting. Desktop PCs almost never need this.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\LocationAndSensors" /v "DisableLocation" /t REG_DWORD /d 1 /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\LocationAndSensors" /v "DisableLocationScripting" /t REG_DWORD /d 1 /f',
                ],
            },
            {
                "name": "Disable Content Delivery & Suggestions",
                "desc": "Stops Windows from silently installing Candy Crush, showing Start menu ads, lock screen tips, and suggested apps. 11+ toggles disabled.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\CloudContent" /v "DisableWindowsConsumerFeatures" /t REG_DWORD /d 1 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" /v "SilentInstalledAppsEnabled" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" /v "SystemPaneSuggestionsEnabled" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" /v "SoftLandingEnabled" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" /v "SubscribedContent-338389Enabled" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" /v "SubscribedContent-310093Enabled" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" /v "SubscribedContent-338388Enabled" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" /v "ContentDeliveryAllowed" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" /v "PreInstalledAppsEnabled" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" /v "OemPreInstalledAppsEnabled" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" /v "FeatureManagementEnabled" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Disable Input Personalization & Speech",
                "desc": "Stops Windows from collecting typing patterns, handwriting data, and sending voice recordings to Microsoft servers.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\InputPersonalization" /v "RestrictImplicitInkCollection" /t REG_DWORD /d 1 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\InputPersonalization" /v "RestrictImplicitTextCollection" /t REG_DWORD /d 1 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Speech_OneCore\\Settings\\OnlineSpeechPrivacy" /v "HasAccepted" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Input\\TIPC" /v "Enabled" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Disable Feedback & Tailored Experiences",
                "desc": "No more 'Rate Windows' popups. Stops Microsoft from using your diagnostic data to personalize ads.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Siuf\\Rules" /v "NumberOfSIUFInPeriod" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Privacy" /v "TailoredExperiencesWithDiagnosticDataEnabled" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Disable P2P Update Delivery & Clipboard Sync",
                "desc": "Stops Windows from uploading updates to stranger PCs over the internet. Also disables cross-device clipboard sync.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DeliveryOptimization" /v "DODownloadMode" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\System" /v "AllowClipboardHistory" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\System" /v "AllowCrossDeviceClipboard" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Disable Edge Telemetry",
                "desc": "Disables Microsoft Edge's background data collection and metrics reporting.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Edge" /v "MetricsReportingEnabled" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Edge" /v "SendSiteInfoToImproveServices" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Disable Office Telemetry",
                "desc": "Disables telemetry data collection for Microsoft Office applications.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKCU\\SOFTWARE\\Policies\\Microsoft\\office\\16.0\\osm" /v "Enablelogging" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\SOFTWARE\\Policies\\Microsoft\\office\\16.0\\osm" /v "EnableUpload" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Disable Visual Studio Telemetry",
                "desc": "Disables the Customer Experience Improvement Program for Visual Studio.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\VisualStudio\\SQM" /v "OptIn" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Disable NVIDIA Telemetry",
                "desc": "Disables NVIDIA's background telemetry services and tasks.",
                "risk": SAFE,
                "cmds": [
                    'schtasks /Change /TN "NvTmRep" /Disable',
                    'schtasks /Change /TN "NvTmRepOnLogon" /Disable',
                    'schtasks /Change /TN "NvTmMon" /Disable',
                    'sc stop NvTelemetryContainer',
                    'sc config NvTelemetryContainer start=disabled',
                ],
            },
            {
                "name": "Disable Windows Defender SmartScreen",
                "desc": "Stops Windows from sending URLs and downloaded file hashes to Microsoft servers for reputation checking.",
                "risk": MEDIUM,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\System" /v "EnableSmartScreen" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\AppHost" /v "EnableWebContentEvaluation" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Disable Error Reporting (WER)",
                "desc": "Stops Windows from generating crash dumps and sending them to Microsoft. Saves disk space and CPU cycles during crashes.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Error Reporting" /v "Disabled" /t REG_DWORD /d 1 /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\Windows Error Reporting" /v "Disabled" /t REG_DWORD /d 1 /f',
                ],
            },
            {
                "name": "Disable Inventory Collector",
                "desc": "Stops Windows from scanning your hard drive to build an inventory of installed applications and files to send to Microsoft.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppCompat" /v "DisableInventory" /t REG_DWORD /d 1 /f',
                ],
            },
        ],
    },
    "Services  &  Tasks": {
        "icon": "-",
        "tweaks": [
            {
                "name": "Disable DiagTrack & WAP Push",
                "desc": "The main telemetry pipeline (Connected User Experiences) and its feeder service. Constant CPU + network drain eliminated.",
                "risk": SAFE,
                "cmds": [
                    'sc stop DiagTrack', 'sc config DiagTrack start=disabled',
                    'sc stop dmwappushservice', 'sc config dmwappushservice start=disabled',
                ],
            },
            {
                "name": "Disable SysMain / Superfetch",
                "desc": "Pre-loads apps into RAM based on usage habits. Constant disk I/O on HDDs, wastes RAM on SSDs. Safe to disable on SSDs.",
                "risk": SAFE,
                "cmds": [
                    'sc stop SysMain', 'sc config SysMain start=disabled',
                ],
            },
            {
                "name": "Disable WER, Diagnostics & Link Tracking",
                "desc": "Windows Error Reporting, Diagnostic hosts, and Distributed Link Tracking \u2014 all background services with zero user benefit.",
                "risk": SAFE,
                "cmds": [
                    'sc stop WerSvc', 'sc config WerSvc start=disabled',
                    'sc stop WdiSystemHost', 'sc config WdiSystemHost start=disabled',
                    'sc stop WdiServiceHost', 'sc config WdiServiceHost start=disabled',
                    'sc stop TrkWks', 'sc config TrkWks start=disabled',
                    'sc stop diagsvc', 'sc config diagsvc start=disabled',
                ],
            },
            {
                "name": "Disable Bloat Services (Fax, Maps, Retail...)",
                "desc": "Disables Fax, Downloaded Maps Manager, Retail Demo, AllJoyn IoT router, Windows Insider, Geolocation, Remote Registry.",
                "risk": SAFE,
                "cmds": [
                    'sc stop Fax', 'sc config Fax start=disabled',
                    'sc stop MapsBroker', 'sc config MapsBroker start=disabled',
                    'sc stop RetailDemo', 'sc config RetailDemo start=disabled',
                    'sc stop AJRouter', 'sc config AJRouter start=disabled',
                    'sc stop wisvc', 'sc config wisvc start=disabled',
                    'sc stop lfsvc', 'sc config lfsvc start=disabled',
                    'sc stop RemoteRegistry', 'sc config RemoteRegistry start=disabled',
                ],
            },
            {
                "name": "Disable Xbox Services (4 services)",
                "desc": "Xbox Live Auth, Game Save, Accessory Management, Networking. Disable if you don't use Xbox Game Pass on PC.",
                "risk": SAFE,
                "cmds": [
                    'sc stop XblAuthManager', 'sc config XblAuthManager start=disabled',
                    'sc stop XblGameSave', 'sc config XblGameSave start=disabled',
                    'sc stop XboxGipSvc', 'sc config XboxGipSvc start=disabled',
                    'sc stop XboxNetApiSvc', 'sc config XboxNetApiSvc start=disabled',
                ],
            },
            {
                "name": "Disable Telemetry Scheduled Tasks",
                "desc": "Compatibility Appraiser (uses 100% disk 15-30 min), ProgramDataUpdater, CEIP tasks, DiskDiagnostic, Error Reporting queue.",
                "risk": SAFE,
                "cmds": [
                    'schtasks /Change /TN "Microsoft\\Windows\\Application Experience\\Microsoft Compatibility Appraiser" /Disable',
                    'schtasks /Change /TN "Microsoft\\Windows\\Application Experience\\ProgramDataUpdater" /Disable',
                    'schtasks /Change /TN "Microsoft\\Windows\\Application Experience\\StartupAppTask" /Disable',
                    'schtasks /Change /TN "Microsoft\\Windows\\Customer Experience Improvement Program\\Consolidator" /Disable',
                    'schtasks /Change /TN "Microsoft\\Windows\\Customer Experience Improvement Program\\UsbCeip" /Disable',
                    'schtasks /Change /TN "Microsoft\\Windows\\Customer Experience Improvement Program\\KernelCeipTask" /Disable',
                    'schtasks /Change /TN "Microsoft\\Windows\\DiskDiagnostic\\Microsoft-Windows-DiskDiagnosticDataCollector" /Disable',
                    'schtasks /Change /TN "Microsoft\\Windows\\Windows Error Reporting\\QueueReporting" /Disable',
                ],
            },
            {
                "name": "Disable Print Spooler",
                "desc": "Disables the printer service. Only use this if you NEVER print to a physical or PDF printer.",
                "risk": MEDIUM,
                "cmds": [
                    'sc stop Spooler', 'sc config Spooler start=disabled',
                ],
            },
            {
                "name": "Disable Windows Search Service",
                "desc": "Disables the background file indexer. Search will still work but will be slower. Saves massive disk I/O.",
                "risk": MEDIUM,
                "cmds": [
                    'sc stop WSearch', 'sc config WSearch start=disabled',
                ],
            },
            {
                "name": "Disable Windows Update Service",
                "desc": "Completely disables Windows Update. HIGH RISK. You will not receive security patches or feature updates.",
                "risk": HIGH,
                "cmds": [
                    'sc stop wuauserv', 'sc config wuauserv start=disabled',
                    'sc stop WaaSMedicSvc', 'sc config WaaSMedicSvc start=disabled',
                    'sc stop UsoSvc', 'sc config UsoSvc start=disabled',
                ],
            },
            {
                "name": "Disable Background Intelligent Transfer (BITS)",
                "desc": "Disables BITS, which is used by Windows Update and other apps to download files in the background.",
                "risk": MEDIUM,
                "cmds": [
                    'sc stop BITS', 'sc config BITS start=disabled',
                ],
            },
            {
                "name": "Disable Security Center Service",
                "desc": "Disables the Windows Security Center service. Stops notifications about antivirus and firewall status.",
                "risk": HIGH,
                "cmds": [
                    'sc stop wscsvc', 'sc config wscsvc start=disabled',
                ],
            },
        ],
    },
    "Cleanup": {
        "icon": "-",
        "tweaks": [
            {
                "name": "Deep Temp / Cache / Log Cleanup",
                "desc": "Deletes user temp, system temp, prefetch, thumbnail/icon/shader caches, error reports, crash dumps, CBS logs. Recovers GBs of space.",
                "risk": SAFE,
                "cmds": [
                    'cmd /c del /q /f /s "%TEMP%\\*" 2>nul',
                    'cmd /c del /q /f /s "%WINDIR%\\Temp\\*" 2>nul',
                    'cmd /c del /q /f /s "%WINDIR%\\Prefetch\\*" 2>nul',
                    'cmd /c del /q /f /s "%LOCALAPPDATA%\\Microsoft\\Windows\\Explorer\\thumbcache_*.db" 2>nul',
                    'cmd /c del /q /f "%LOCALAPPDATA%\\IconCache.db" 2>nul',
                    'cmd /c del /q /f /s "%LOCALAPPDATA%\\D3DSCache\\*" 2>nul',
                    'cmd /c del /q /f "%WINDIR%\\MEMORY.DMP" 2>nul',
                    'cmd /c del /q /f /s "%WINDIR%\\Minidump\\*" 2>nul',
                    'cmd /c del /q /f /s "%LOCALAPPDATA%\\CrashDumps\\*" 2>nul',
                    'cmd /c del /q /f /s "%LOCALAPPDATA%\\Microsoft\\Windows\\WER\\*" 2>nul',
                    'cmd /c del /q /f /s "%WINDIR%\\Logs\\CBS\\*.log" 2>nul',
                ],
            },
            {
                "name": "Flush DNS & ARP Cache",
                "desc": "Clears stale DNS and network address mappings. Both rebuild instantly. Fixes many connection issues.",
                "risk": SAFE,
                "cmds": [
                    'ipconfig /flushdns',
                    'netsh interface ip delete arpcache',
                ],
            },
            {
                "name": "Clean Browser Caches (Chrome, Edge, Firefox)",
                "desc": "Removes cached web data from all major browsers. Does NOT delete passwords, bookmarks, or history.",
                "risk": SAFE,
                "cmds": [
                    'cmd /c del /q /f /s "%LOCALAPPDATA%\\Google\\Chrome\\User Data\\Default\\Cache\\*" 2>nul',
                    'cmd /c del /q /f /s "%LOCALAPPDATA%\\Google\\Chrome\\User Data\\Default\\Code Cache\\*" 2>nul',
                    'cmd /c del /q /f /s "%LOCALAPPDATA%\\Microsoft\\Edge\\User Data\\Default\\Cache\\*" 2>nul',
                    'cmd /c del /q /f /s "%LOCALAPPDATA%\\Microsoft\\Edge\\User Data\\Default\\Code Cache\\*" 2>nul',
                    'cmd /c del /q /f /s "%LOCALAPPDATA%\\Mozilla\\Firefox\\Profiles\\*.default*\\cache2\\*" 2>nul',
                ],
            },
            {
                "name": "NTFS Optimizations (Last Access, 8.3, Memory)",
                "desc": "Disables last-access timestamps (reduces writes), disables DOS 8.3 filenames (NTFS overhead), increases NTFS paged pool.",
                "risk": SAFE,
                "cmds": [
                    'fsutil behavior set disablelastaccess 1',
                    'fsutil behavior set disable8dot3 1',
                    'fsutil behavior set memoryusage 2',
                ],
            },
            {
                "name": "Clear Windows Update Cache (SoftwareDistribution)",
                "desc": "Deletes downloaded Windows Update files. Fixes stuck updates and frees up massive amounts of space.",
                "risk": SAFE,
                "cmds": [
                    'net stop wuauserv',
                    'net stop bits',
                    'cmd /c del /q /f /s "%WINDIR%\\SoftwareDistribution\\Download\\*" 2>nul',
                    'net start wuauserv',
                    'net start bits',
                ],
            },
            {
                "name": "Clear Event Viewer Logs",
                "desc": "Wipes all Windows Event logs. Good for a fresh start when troubleshooting, or just to free up space.",
                "risk": SAFE,
                "cmds": [
                    'powershell -NoProfile -Command "Get-EventLog -LogName * | ForEach { Clear-EventLog $_.Log }"',
                ],
            },
            {
                "name": "Disable Windows Error Reporting (WER) Folders",
                "desc": "Prevents Windows from creating massive crash dump folders in ProgramData and LocalAppData.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\Windows Error Reporting" /v "DontSendAdditionalData" /t REG_DWORD /d 1 /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\Windows Error Reporting" /v "ForceQueue" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Disable Delivery Optimization Cache",
                "desc": "Stops Windows from caching updates to share with other PCs, freeing up disk space and reducing background disk I/O.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DeliveryOptimization" /v "DOMaxCacheSize" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DeliveryOptimization" /v "DOAbsoluteMaxCacheSize" /t REG_DWORD /d 0 /f',
                ],
            },
        ],
    },
    "UI  &  QoL": {
        "icon": "-",
        "tweaks": [
            {
                "name": "Faster Shutdown Timeouts",
                "desc": "WaitToKillService=2s, WaitToKillApp=2s, HungApp=1s, AutoEndTasks=1. Makes shutdown/restart dramatically faster.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control" /v "WaitToKillServiceTimeout" /t REG_SZ /d "2000" /f',
                    'reg add "HKCU\\Control Panel\\Desktop" /v "WaitToKillAppTimeout" /t REG_SZ /d "2000" /f',
                    'reg add "HKCU\\Control Panel\\Desktop" /v "HungAppTimeout" /t REG_SZ /d "1000" /f',
                    'reg add "HKCU\\Control Panel\\Desktop" /v "AutoEndTasks" /t REG_SZ /d "1" /f',
                ],
            },
            {
                "name": "Remove Startup Program Delay",
                "desc": "Windows intentionally delays startup programs by ~10 seconds. This removes that delay. Instantly noticeable on SSDs.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Serialize" /v "StartupDelayInMSec" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Disable Cortana & Web Search in Start",
                "desc": "Disables Cortana and prevents Bing results when you search for local apps in the Start menu. Makes search 10x better.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Search" /v "AllowCortana" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Search" /v "BingSearchEnabled" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Search" /v "DisableWebSearch" /t REG_DWORD /d 1 /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Search" /v "ConnectedSearchUseWeb" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Taskbar Cleanup (People, Chat, Widgets...)",
                "desc": "Hides People, Meet Now/Chat, Task View, News/Interests/Widgets, Ink Workspace. Search set to icon-only.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\\People" /v "PeopleBand" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Chat" /v "ChatIcon" /t REG_DWORD /d 3 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v "ShowTaskViewButton" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Search" /v "SearchboxTaskbarMode" /t REG_DWORD /d 1 /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Feeds" /v "EnableFeeds" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Dsh" /v "AllowNewsAndInterests" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\PenWorkspace" /v "PenWorkspaceButtonDesiredVisibility" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Show File Extensions & Hidden Files",
                "desc": "Security essential: see the real extension of every file. Also shows hidden files and opens Explorer to This PC.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v "HideFileExt" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v "Hidden" /t REG_DWORD /d 1 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v "LaunchTo" /t REG_DWORD /d 1 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v "NavPaneExpandToCurrentFolder" /t REG_DWORD /d 1 /f',
                ],
            },
            {
                "name": "Disable Visual Animations & Transparency",
                "desc": "Removes window animations, transparency blur, and drag-full-windows. Keeps ClearType font smoothing. GPU/CPU savings.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" /v "VisualFXSetting" /t REG_DWORD /d 2 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize" /v "EnableTransparency" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\Control Panel\\Desktop\\WindowMetrics" /v "MinAnimate" /t REG_SZ /d "0" /f',
                    'reg add "HKCU\\Control Panel\\Desktop" /v "DragFullWindows" /t REG_SZ /d "0" /f',
                ],
            },
            {
                "name": "Restore Classic Right-Click Menu (Win 11)",
                "desc": "Brings back the full context menu instead of the truncated one requiring 'Show more options'. Does nothing on Win 10.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKCU\\SOFTWARE\\Classes\\CLSID\\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\\InprocServer32" /ve /t REG_SZ /d "" /f',
                ],
            },
            {
                "name": "Disable AutoPlay & Remote Assistance",
                "desc": "Stops auto-execution when inserting media (security risk). Disables Remote Assistance (rarely needed, attack vector).",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\AutoplayHandlers" /v "DisableAutoplay" /t REG_DWORD /d 1 /f',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Remote Assistance" /v "fAllowToGetHelp" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Disable Action Center / Notifications",
                "desc": "Completely disables the Windows Action Center and all toast notifications. Pure uninterrupted focus.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKCU\\SOFTWARE\\Policies\\Microsoft\\Windows\\Explorer" /v "DisableNotificationCenter" /t REG_DWORD /d 1 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\PushNotifications" /v "ToastEnabled" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Disable Lock Screen",
                "desc": "Skips the picture lock screen and goes straight to the password/PIN prompt on boot.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Personalization" /v "NoLockScreen" /t REG_DWORD /d 1 /f',
                ],
            },
            {
                "name": "Disable Aero Shake & Snap Assist",
                "desc": "Stops windows from minimizing when you shake them, and stops the annoying snap assist suggestions.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v "DisallowShaking" /t REG_DWORD /d 1 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v "SnapAssist" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Disable Windows Defender (Requires Safe Mode/TrustedInstaller)",
                "desc": "Attempts to disable Windows Defender. Note: Modern Windows 10/11 heavily protects these keys. May require third-party tools or Safe Mode to fully apply.",
                "risk": HIGH,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender" /v "DisableAntiSpyware" /t REG_DWORD /d 1 /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection" /v "DisableRealtimeMonitoring" /t REG_DWORD /d 1 /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection" /v "DisableBehaviorMonitoring" /t REG_DWORD /d 1 /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection" /v "DisableOnAccessProtection" /t REG_DWORD /d 1 /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection" /v "DisableScanOnRealtimeEnable" /t REG_DWORD /d 1 /f',
                ],
            },
            {
                "name": "Disable UAC (User Account Control)",
                "desc": "Disables the 'Do you want to allow this app to make changes' prompt. Lowers security but removes annoying popups.",
                "risk": MEDIUM,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "EnableLUA" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "ConsentPromptBehaviorAdmin" /t REG_DWORD /d 0 /f',
                ],
            },
        ],
    },
}



# ─── Application Class ──────────────────────────────────────────────────
class OptimizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Tools by Blandy  —  {APP_VERSION}")
        self.root.geometry("1400x900")
        self.root.minsize(900, 600)
        self.root.state('zoomed')

        # Apply custom icon if it exists
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            icon_path = os.path.join(sys._MEIPASS, "gamephoto.ico")
        else:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gamephoto.ico")
        
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception:
                pass

        self.root.configure(bg="white")

        # Track tweak state
        self.tweak_vars = {}   # tweak_name -> (BooleanVar, tweak_dict)
        self.tweak_applied_lbls = {} # tweak_name -> Label
        self.cat_frames = {}   # cat_name -> content frame
        self.cat_btns = {}     # cat_name -> sidebar button
        self.active_cat = None
        self.tooltip_win = None
        self.chk_draw_funcs = []  # list of draw_chk callables for refresh
        self.music_error = None    # Track music loading errors
        self.music_on = True       # Track music state

        self._build_ui_basic()
        threading.Thread(target=self._load_specs, daemon=True).start()
        self._play_music()
        
        # Check for updates in background
        threading.Thread(target=self._check_for_updates, daemon=True).start()
        
        # Scan for already applied tweaks
        threading.Thread(target=self._scan_applied_tweaks, daemon=True).start()

    # ── Minimal UI (single white page) ─────────────────────────────────
    def _build_ui_basic(self):
        self.root.configure(bg="white")

        # ── Top bar (very basic) ──────────────────────────────────
        top = tk.Frame(self.root, bg="white")
        top.pack(fill="x")

        tk.Label(top, text=f"Tools by Blandy — {APP_VERSION}", font=("Segoe UI", 9, "bold"), bg="white", fg="black").pack(
            side="left", padx=8, pady=4
        )

        self.music_btn = tk.Button(top, text="Music: ON", font=("Segoe UI", 8), command=self._toggle_music)
        self.music_btn.pack(side="right", padx=8, pady=3)

        # ── Body: split screen (no scrolling) ──────────────────────
        paned = tk.PanedWindow(self.root, orient="horizontal", bg="white", sashwidth=6, relief="flat")
        paned.pack(fill="both", expand=True)

        # Left: specs
        specs_frame = tk.Frame(paned, bg="white")
        tk.Label(specs_frame, text="PC Specs", font=("Segoe UI", 8, "bold"), bg="white", fg="black", anchor="w").pack(
            fill="x", padx=8, pady=(6, 2)
        )
        self.specs_text = tk.Text(
            specs_frame,
            font=("Consolas", 6),
            bg="white",
            fg="black",
            relief="flat",
            bd=0,
            highlightthickness=0,
            state="disabled",
            wrap="none",
            padx=8,
            pady=6,
            cursor="arrow",
        )
        self.specs_text.pack(fill="both", expand=True)
        self._set_specs_text("loading...")

        # Right: tweaks (compact grid, multi-column)
        tweaks_frame = tk.Frame(paned, bg="white")
        tk.Label(tweaks_frame, text="Tweaks", font=("Segoe UI", 8, "bold"), bg="white", fg="black", anchor="w").pack(
            fill="x", padx=8, pady=(6, 2)
        )

        grid = tk.Frame(tweaks_frame, bg="white")
        grid.pack(fill="both", expand=True, padx=6, pady=2)

        # Determine how many item-columns to use based on screen width
        try:
            screen_w = int(self.root.winfo_screenwidth())
        except Exception:
            screen_w = 1920
        item_cols = 5 if screen_w >= 1900 else (4 if screen_w >= 1600 else 3)
        item_cols = max(2, min(5, item_cols))

        # Each item uses 2 grid columns: checkbox + risk label
        for c in range(item_cols * 2):
            grid.grid_columnconfigure(c, weight=1)

        def risk_to_color(risk_tuple):
            try:
                return risk_tuple[1]
            except Exception:
                return "black"

        def risk_to_text(risk_tuple):
            try:
                return risk_tuple[0]
            except Exception:
                return ""

        r = 0
        for cat_name, cat_data in CATEGORIES.items():
            # Category header spans full width
            hdr = tk.Label(grid, text=cat_name, font=("Segoe UI", 6, "bold"), bg="white", fg="black", anchor="w")
            hdr.grid(row=r, column=0, columnspan=item_cols * 2, sticky="w", padx=2, pady=(3, 0))
            r += 1

            c_group = 0
            for tw in cat_data["tweaks"]:
                var = tk.BooleanVar(value=False)
                self.tweak_vars[tw["name"]] = (var, tw)

                col_base = c_group * 2
                chk = tk.Checkbutton(
                    grid,
                    variable=var,
                    text=tw["name"],
                    font=("Segoe UI", 6),
                    bg="white",
                    fg="black",
                    anchor="w",
                    justify="left",
                    width=40,
                    command=self._update_stats,
                )
                chk.grid(row=r, column=col_base, sticky="w", padx=(2, 0), pady=0)

                # risk + applied indicator live together in one cell
                right_cell = tk.Frame(grid, bg="white")
                right_cell.grid(row=r, column=col_base + 1, sticky="w", padx=(2, 10), pady=0)

                risk_lbl = tk.Label(
                    right_cell,
                    text=risk_to_text(tw["risk"]),
                    font=("Segoe UI", 6, "bold"),
                    bg="white",
                    fg=risk_to_color(tw["risk"]),
                    anchor="w",
                )
                risk_lbl.pack(side="left")

                applied_lbl = tk.Label(right_cell, text="", font=("Segoe UI", 6), bg="white", fg="blue", anchor="w")
                applied_lbl.pack(side="left", padx=(4, 0))
                self.tweak_applied_lbls[tw["name"]] = applied_lbl

                c_group += 1
                if c_group >= item_cols:
                    c_group = 0
                    r += 1

            if c_group != 0:
                r += 1

        paned.add(specs_frame, minsize=340)
        paned.add(tweaks_frame, minsize=520)

        # ── Bottom controls (basic) ─────────────────────────────────
        bottom = tk.Frame(self.root, bg="white")
        bottom.pack(fill="x")

        self.stats_lbl = tk.Label(bottom, text="0 / 0 tweaks selected", font=("Segoe UI", 8), bg="white", fg="black")
        self.stats_lbl.pack(side="left", padx=8, pady=4)

        tk.Button(bottom, text="Select All", font=("Segoe UI", 8), command=self._select_all).pack(side="left", padx=4, pady=3)
        tk.Button(bottom, text="Deselect All", font=("Segoe UI", 8), command=self._deselect_all).pack(side="left", padx=4, pady=3)
        tk.Button(bottom, text="Apply Selected", font=("Segoe UI", 8), command=self._apply).pack(side="right", padx=8, pady=3)

        self._update_stats()

    def _scan_applied_tweaks(self):
        for cat_name, cat_data in CATEGORIES.items():
            for tweak in cat_data["tweaks"]:
                if self._is_tweak_applied(tweak["cmds"]):
                    self.root.after(0, self._set_tweak_checked, tweak["name"])

    def _set_tweak_checked(self, tweak_name):
        if tweak_name in self.tweak_vars:
            self.tweak_vars[tweak_name][0].set(True)
            if tweak_name in self.tweak_applied_lbls:
                self.tweak_applied_lbls[tweak_name].configure(text="APPLIED")
            for draw_func in self.chk_draw_funcs:
                draw_func()
            self._update_stats()

    def _is_tweak_applied(self, cmds):
        verifiable_cmds = 0
        applied_cmds = 0

        for cmd in cmds:
            cmd_lower = cmd.lower()
            
            # 1. Check Registry
            if cmd_lower.startswith('reg add'):
                try:
                    parts = shlex.split(cmd, posix=False)
                    # Remove surrounding quotes from parts
                    parts = [p.strip('"') for p in parts]
                    
                    if 'add' not in [p.lower() for p in parts]: continue
                    
                    key_path = parts[2]
                    
                    value_name = ""
                    if '/v' in parts:
                        value_name = parts[parts.index('/v') + 1]
                    elif '/ve' in parts:
                        value_name = ""
                        
                    reg_type = ""
                    if '/t' in parts:
                        reg_type = parts[parts.index('/t') + 1]
                        
                    expected_data = ""
                    if '/d' in parts:
                        expected_data = parts[parts.index('/d') + 1]
                        
                    hkey_map = {
                        "HKLM": winreg.HKEY_LOCAL_MACHINE,
                        "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
                        "HKCU": winreg.HKEY_CURRENT_USER,
                        "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
                        "HKCR": winreg.HKEY_CLASSES_ROOT,
                        "HKU": winreg.HKEY_USERS
                    }
                    
                    key_parts = key_path.split('\\', 1)
                    if len(key_parts) != 2: continue
                    hkey_str, subkey = key_parts
                    hkey = hkey_map.get(hkey_str.upper())
                    if not hkey: continue
                    
                    verifiable_cmds += 1
                    try:
                        with winreg.OpenKey(hkey, subkey) as key:
                            val, typ = winreg.QueryValueEx(key, value_name)
                            
                            is_match = False
                            if reg_type == "REG_DWORD":
                                is_match = (int(val) == int(expected_data))
                            elif reg_type in ("REG_SZ", "REG_EXPAND_SZ"):
                                is_match = (str(val) == str(expected_data))
                            elif reg_type == "REG_BINARY":
                                is_match = (val.hex().upper() == expected_data.upper())
                            
                            if is_match:
                                applied_cmds += 1
                    except FileNotFoundError:
                        pass
                    except Exception:
                        pass
                except Exception:
                    pass

            # 2. Check Services
            elif cmd_lower.startswith('sc config'):
                match = re.search(r'sc config (.*?) start=disabled', cmd, re.IGNORECASE)
                if match:
                    service_name = match.group(1).strip('"')
                    verifiable_cmds += 1
                    try:
                        output = subprocess.check_output(f'sc.exe qc "{service_name}"', shell=True, text=True, stderr=subprocess.DEVNULL, creationflags=0x08000000)
                        if "START_TYPE" in output and "4" in output: # 4 is DISABLED
                            applied_cmds += 1
                    except subprocess.CalledProcessError:
                        # Service doesn't exist -> effectively disabled
                        applied_cmds += 1

            # 3. Check Scheduled Tasks
            elif cmd_lower.startswith('schtasks /change'):
                match = re.search(r'schtasks /Change /TN "(.*?)" /Disable', cmd, re.IGNORECASE)
                if match:
                    task_name = match.group(1)
                    verifiable_cmds += 1
                    try:
                        output = subprocess.check_output(f'schtasks /Query /TN "{task_name}" /FO LIST', shell=True, text=True, stderr=subprocess.DEVNULL, creationflags=0x08000000)
                        if "Disabled" in output:
                            applied_cmds += 1
                    except subprocess.CalledProcessError:
                        # Task doesn't exist -> effectively disabled
                        applied_cmds += 1

            # 4. Check fsutil
            elif cmd_lower.startswith('fsutil behavior set'):
                try:
                    parts = shlex.split(cmd, posix=False)
                    parts = [p.strip('"') for p in parts]
                    if len(parts) >= 5:
                        prop = parts[3]
                        val = parts[4]
                        verifiable_cmds += 1
                        output = subprocess.check_output(f'fsutil behavior query {prop}', shell=True, text=True, stderr=subprocess.DEVNULL, creationflags=0x08000000)
                        if val in output:
                            applied_cmds += 1
                except Exception:
                    pass
                    
            # 5. Check powercfg
            elif cmd_lower.startswith('powercfg /change') or cmd_lower.startswith('powercfg -change'):
                try:
                    parts = shlex.split(cmd, posix=False)
                    parts = [p.strip('"') for p in parts]
                    if len(parts) >= 4:
                        setting = parts[2]
                        val = parts[3]
                        verifiable_cmds += 1
                        # This is a simplified check, powercfg querying is complex, 
                        # but we can try to query the active scheme
                        output = subprocess.check_output('powercfg /q SCHEME_CURRENT', shell=True, text=True, stderr=subprocess.DEVNULL, creationflags=0x08000000)
                        # We just assume it's applied if we can't easily verify, or we skip verification
                        # For now, let's just skip powercfg verification to avoid false negatives
                        verifiable_cmds -= 1
                except Exception:
                    pass

        # If we verified at least one command and ALL verified commands are applied, return True
        # If there are no verifiable commands, we can't be sure, so return False
        if verifiable_cmds > 0 and verifiable_cmds == applied_cmds:
            return True
        return False

    def _check_for_updates(self):
        try:
            url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                latest_version = data.get("tag_name", "")
                
                if latest_version and latest_version != APP_VERSION:
                    standalone_exe_url = ""
                    for asset in data.get("assets", []):
                        name = asset.get("name", "")
                        # Prioritize the standalone optimizer exe, NOT the setup
                        if name == "TheVault_Optimizer.exe":
                            standalone_exe_url = asset.get("browser_download_url")
                            break
                    
                    if standalone_exe_url:
                        self.root.after(2000, lambda: self._prompt_update(latest_version, standalone_exe_url))
        except Exception as e:
            print(f"Update check failed: {e}")

    def _prompt_update(self, latest_version, download_url):
        msg = f"A new version ({latest_version}) is available!\n\nWould you like to apply the update now?"
        if messagebox.askyesno("Update Available", msg):
            threading.Thread(target=self._download_and_apply_patch, args=(download_url,), daemon=True).start()

    def _download_and_apply_patch(self, url):
        try:
            # UI Overlay for progress
            progress_win = tk.Toplevel(self.root)
            progress_win.title("Updating...")
            progress_win.geometry("380x120")
            progress_win.configure(bg="white")
            progress_win.attributes("-topmost", True)
            progress_win.overrideredirect(True)
            
            # Center of the screen
            w, h = 380, 120
            x = (progress_win.winfo_screenwidth() // 2) - (w // 2)
            y = (progress_win.winfo_screenheight() // 2) - (h // 2)
            progress_win.geometry(f"{w}x{h}+{x}+{y}")

            tk.Label(progress_win, text="Updating...", font=("Segoe UI", 10, "bold"), bg="white", fg="black").pack(pady=(18, 6))
            status_lbl = tk.Label(progress_win, text="Starting download...", font=("Segoe UI", 8), bg="white", fg="black")
            status_lbl.pack()

            def update_ui(txt, pct):
                status_lbl.configure(text=txt)
                progress_win.update()

            # Download using chunks for smoother UI
            temp_new_exe = os.path.join(os.environ["TEMP"], "TheVault_New_Version.exe")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            
            with urllib.request.urlopen(req) as response:
                total_size = int(response.info().get('Content-Length', 0))
                downloaded = 0
                chunk_size = 1024 * 64
                
                with open(temp_new_exe, 'wb') as out_file:
                    while True:
                        chunk = response.read(chunk_size)
                        if not chunk: break
                        out_file.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            update_ui(f"Downloading core patches... {int(percent)}%", percent)

            update_ui("Applying update...", 100)
            time.sleep(1)

            # --- Hot Swap Logic ---
            current_exe = sys.executable if getattr(sys, 'frozen', False) else __file__
            if not getattr(sys, 'frozen', False):
                messagebox.showwarning("Developer Mode", "Hot-patching disabled in script mode. Downloaded to temp folder.")
                progress_win.destroy()
                return

            # ── Deep-fix hot swap ─────────────────────────────────────────────
            current_pid  = os.getpid()
            # current_exe already set above (sys.executable, validated frozen)

            ps_script = os.path.join(os.environ["TEMP"], "vault_launcher.ps1")
            with open(ps_script, "w", encoding="utf-8") as f:
                f.write(f"""# vault_launcher.ps1  —  written by Tools by Blandy patcher
$targetExe  = '{current_exe.replace("'", "''")}' 
$newExe     = '{temp_new_exe.replace("'", "''")}'
$oldPID     = {current_pid}

# Wait for the old process to fully exit (up to 30 s)
try {{
    $proc = Get-Process -Id $oldPID -ErrorAction SilentlyContinue
    if ($proc) {{
        $proc | Wait-Process -Timeout 30 -ErrorAction SilentlyContinue
    }}
}} catch {{ }}

Start-Sleep -Milliseconds 500

# Swap the files
$backup = $targetExe + '.patch_old'
if (Test-Path $backup) {{ Remove-Item $backup -Force -ErrorAction SilentlyContinue }}
Move-Item -LiteralPath $targetExe -Destination $backup -Force
Move-Item -LiteralPath $newExe    -Destination $targetExe -Force

# Launch the new exe with a CLEAN environment (no _MEIPASS / stale PATH / PYTHONHOME)
Start-Process -FilePath $targetExe -UseNewEnvironment

# Self-delete this script
Remove-Item -LiteralPath $MyInvocation.MyCommand.Path -Force -ErrorAction SilentlyContinue
""")

            # Launch the PowerShell script fully detached so it outlives this process.
            # Use CREATE_NEW_PROCESS_GROUP + DETACHED_PROCESS so it is NOT a child
            # of this PyInstaller exe and cannot inherit any handles or env from it.
            DETACHED_PROCESS    = 0x00000008
            CREATE_NEW_PG       = 0x00000200
            CREATE_NO_WIN       = 0x08000000
            subprocess.Popen(
                [
                    "powershell.exe",
                    "-NoProfile",
                    "-NonInteractive",
                    "-WindowStyle", "Hidden",
                    "-ExecutionPolicy", "Bypass",
                    "-File", ps_script,
                ],
                creationflags=DETACHED_PROCESS | CREATE_NEW_PG | CREATE_NO_WIN,
                close_fds=True,
                # DO NOT pass env= here — use the raw inherited env so powershell.exe
                # itself launches correctly, but -UseNewEnvironment inside the script
                # will strip everything before handing control to the new exe.
            )
            os._exit(0)

        except Exception as e:
            messagebox.showerror("Update Error", f"Patching failed: {e}")
            if 'progress_win' in locals(): progress_win.destroy()

    # ── Music ────────────────────────────────────────────────────────
    def _play_music(self):
        self.music_error = None
        # Music is optional; keep it off the critical path.
        global pygame
        if pygame is None:
            try:
                import pygame as _pygame
                pygame = _pygame
            except Exception:
                self.music_error = "pygame not available"
                try:
                    self.music_btn.configure(text="Music: N/A")
                except Exception:
                    pass
                return
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            
            # Handle PyInstaller bundled resources
            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                # Running as compiled executable
                base_path = sys._MEIPASS
            else:
                # Running as script
                base_path = os.path.dirname(os.path.abspath(__file__))
            
            mp3 = os.path.join(base_path, "Dark Fantasy - shahi77.mp3")
            
            if not os.path.exists(mp3):
                self.music_error = f"MP3 file not found:\n{mp3}"
                print(self.music_error)
                try:
                    self.music_btn.configure(text="Music: N/A")
                except Exception:
                    pass
                return
            
            file_size = os.path.getsize(mp3)
            if file_size < 1000:  # Really small files are likely placeholders
                self.music_error = f"MP3 placeholder (only {file_size} bytes). Replace with real audio file."
                print(self.music_error)
                try:
                    self.music_btn.configure(text="Music: N/A")
                except Exception:
                    pass
                return
            
            pygame.mixer.music.load(mp3)
            pygame.mixer.music.set_volume(0.35)
            pygame.mixer.music.play(-1)
            print(f"✓ Music loaded and playing: {mp3}")
            try:
                self.music_btn.configure(text="Music: ON")
            except Exception:
                pass
        except Exception as e:
            self.music_error = f"Music error: {str(e)}"
            print(self.music_error)
            try:
                self.music_btn.configure(text="Music: N/A")
            except Exception:
                pass

    # ── Build Layout ─────────────────────────────────────────────────
    def _build_ui(self):
        # Kept for backward compatibility; the app now uses _build_ui_basic().
        self._build_ui_basic()

    def _draw_apply_btn(self, color):
        c = self.apply_btn
        c.delete("all")
        self._round_rect(c, 0, 0, 180, 38, 0, fill=color, outline="")
        c.create_text(90, 19, text="APPLY SELECTED", font=("Arial", 10, "bold"), fill="white")

    def _round_rect(self, canvas, x1, y1, x2, y2, r, **kw):
        pts = [
            x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1,
            x2, y1, x2, y1+r, x2, y1+r, x2, y2-r,
            x2, y2-r, x2, y2, x2-r, y2, x2-r, y2,
            x1+r, y2, x1+r, y2, x1, y2, x1, y2-r,
            x1, y2-r, x1, y1+r, x1, y1+r, x1, y1,
        ]
        return canvas.create_polygon(pts, smooth=True, **kw)


    def _build_specs_page(self, parent):
        # Title
        tk.Label(parent, text="My PC", font=("Consolas", 18, "bold"),
                 bg=BG, fg=TEXT, anchor="w").pack(fill="x", padx=28, pady=(24, 2))
        tk.Label(parent, text="hardware specifications", font=("Consolas", 9),
                 bg=BG, fg=TEXT_DIM, anchor="w").pack(fill="x", padx=30, pady=(0, 18))
        tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", padx=28, pady=(0, 16))

        # The specs text area — plain monospace, no frills
        self.specs_text = tk.Text(
            parent,
            font=("Consolas", 10),
            bg=BG,
            fg=TEXT,
            relief="flat",
            bd=0,
            highlightthickness=0,
            state="disabled",
            wrap="word",
            padx=30,
            pady=4,
            cursor="arrow",
            selectbackground=SIDEBAR_SEL,
        )
        self.specs_text.pack(fill="both", expand=True)

        self._set_specs_text("loading...")

    def _set_specs_text(self, raw):
        t = self.specs_text
        t.config(state="normal")
        t.delete("1.0", "end")
        if raw == "loading...":
            t.insert("end", "gathering info, give it a sec...\n")
        else:
            # Plain text only (no tag styling)
            for line in raw.split("\n"):
                t.insert("end", line.rstrip() + "\n")
        t.config(state="disabled")

    def _load_specs(self):
        try:
            cmd = r'''
$ErrorActionPreference = "SilentlyContinue"

$os  = Get-CimInstance Win32_OperatingSystem
$cs  = Get-CimInstance Win32_ComputerSystem
$cpu = Get-CimInstance Win32_Processor

Write-Output ("OS: " + $os.Caption + " | Build " + $os.BuildNumber + " (" + $os.Version + ") | " + $os.OSArchitecture)
Write-Output ("Install: " + $os.InstallDate.ToString("yyyy-MM-dd") + " | Boot: " + $os.LastBootUpTime.ToString("yyyy-MM-dd HH:mm"))
Write-Output ("Host: " + $env:COMPUTERNAME + " | User: " + $env:USERNAME)
Write-Output ("Model: " + $cs.Manufacturer + " " + $cs.Model)
Write-Output ""

Write-Output ("CPU: " + $cpu.Name.Trim())
Write-Output ("Cores/Threads: " + $cpu.NumberOfCores + "/" + $cpu.NumberOfLogicalProcessors + " | Base: " + $cpu.MaxClockSpeed + " MHz | Socket: " + $cpu.SocketDesignation)
Write-Output ("Cache: L2 " + [math]::Round($cpu.L2CacheSize / 1024, 1) + " MB | L3 " + [math]::Round($cpu.L3CacheSize / 1024, 1) + " MB")
Write-Output ""

$ramTotal = [math]::Round($cs.TotalPhysicalMemory / 1GB, 2)
Write-Output ("RAM: " + $ramTotal + " GB")
$sticks = Get-CimInstance Win32_PhysicalMemory
$stickLines = @()
foreach ($s in $sticks) {
    $cap  = [math]::Round($s.Capacity / 1GB, 0)
    $spd  = $s.ConfiguredClockSpeed
    $type = switch ($s.MemoryType) { 20 {"DDR"} 21 {"DDR2"} 24 {"DDR3"} 26 {"DDR4"} 34 {"DDR5"} default {"DDR"}}
    $stickLines += ($s.DeviceLocator + ":" + $cap + "GB " + $type + "@" + $spd + "MHz")
}
if ($stickLines.Count -gt 0) { Write-Output ("Sticks: " + ($stickLines -join " | ")) }
Write-Output ""

$gpus = Get-CimInstance Win32_VideoController
foreach ($g in $gpus) {
    $vram = ""
    if ($g.AdapterRAM -gt 0) { $vram = (" | VRAM " + [math]::Round($g.AdapterRAM / 1GB, 1) + " GB") }
    $res = ""
    if ($g.CurrentHorizontalResolution -gt 0) { $res = (" | " + $g.CurrentHorizontalResolution + "x" + $g.CurrentVerticalResolution + "@" + $g.CurrentRefreshRate + "Hz") }
    Write-Output ("GPU: " + $g.Name + $vram + " | Driver " + $g.DriverVersion + " (" + $g.DriverDate.ToString("yyyy-MM-dd") + ")" + $res)
}
Write-Output ""

$disks = Get-CimInstance Win32_DiskDrive
$diskLines = @()
foreach ($d in $disks) { $diskLines += ($d.Model + " " + [math]::Round($d.Size / 1GB, 0) + "GB " + $d.InterfaceType) }
if ($diskLines.Count -gt 0) { Write-Output ("Disks: " + ($diskLines -join " | ")) }

$vols = Get-CimInstance Win32_LogicalDisk | Where-Object { $_.DriveType -eq 3 }
$volLines = @()
foreach ($v in $vols) {
    $free = [math]::Round($v.FreeSpace / 1GB, 1)
    $tot  = [math]::Round($v.Size / 1GB, 1)
    $volLines += ($v.DeviceID + " " + $free + "/" + $tot + "GB free")
}
if ($volLines.Count -gt 0) { Write-Output ("Volumes: " + ($volLines -join " | ")) }
Write-Output ""

$mb = Get-CimInstance Win32_BaseBoard
$bios = Get-CimInstance Win32_BIOS
Write-Output ("Board: " + $mb.Manufacturer + " " + $mb.Product + " | BIOS " + $bios.SMBIOSBIOSVersion + " (" + $bios.ReleaseDate.ToString("yyyy-MM-dd") + ")")
Write-Output ""

$nics = Get-CimInstance Win32_NetworkAdapter | Where-Object { $_.PhysicalAdapter -eq $true }
foreach ($n in $nics) {
    $cfg = Get-CimInstance Win32_NetworkAdapterConfiguration | Where-Object { $_.Index -eq $n.DeviceID }
    $ip = ""
    if ($cfg.IPAddress) { $ip = ($cfg.IPAddress -join ",") }
    $mac = ""
    if ($cfg.MACAddress) { $mac = $cfg.MACAddress }
    Write-Output ("NIC: " + $n.Name + " | IP " + $ip + " | MAC " + $mac)
}
Write-Output ""

$audio = Get-CimInstance Win32_SoundDevice
$aLines = @()
foreach ($a in $audio) { $aLines += $a.Name }
if ($aLines.Count -gt 0) { Write-Output ("Audio: " + ($aLines -join " | ")) }

$monitors = Get-CimInstance WmiMonitorID -Namespace root\wmi -ErrorAction SilentlyContinue
$mLines = @()
if ($monitors) {
    foreach ($m in $monitors) {
        $name = [System.Text.Encoding]::ASCII.GetString($m.UserFriendlyName -ne 0).Trim()
        if ($name) { $mLines += $name }
    }
}
if ($mLines.Count -gt 0) { Write-Output ("Monitors: " + ($mLines -join " | ")) }

$batt = Get-CimInstance Win32_Battery -ErrorAction SilentlyContinue
if ($batt) {
    $status = switch ($batt.BatteryStatus) { 1 {"Discharging"} 2 {"AC"} 3 {"Full"} default {"Unknown"}}
    Write-Output ("Power: Battery " + $batt.EstimatedChargeRemaining + "% (" + $status + ")")
} else {
    Write-Output "Power: No battery"
}
'''
            output = subprocess.check_output(
                ["powershell", "-NoProfile", "-NonInteractive", "-Command", cmd],
                text=True, creationflags=subprocess.CREATE_NO_WINDOW, timeout=30
            )
            self.root.after(0, lambda t=output.strip(): self._set_specs_text(t))
        except Exception as e:
            self.root.after(0, lambda: self._set_specs_text(f"Failed to load specs.\n{e}"))

    def _show_specs_page(self):
        if self.active_cat == "__specs__":
            return
        # deselect previous
        if self.active_cat and self.active_cat in self.cat_btns:
            self.cat_btns[self.active_cat].configure(bg=SIDEBAR_BG, fg=TEXT_DIM)
        self.pc_btn.configure(bg=SIDEBAR_SEL, fg=ACCENT_GLOW)
        self.active_cat = "__specs__"

        self.cat_header.configure(text="🖥   My PC")
        self.cat_count.configure(text="hardware at a glance")

        for f in self.cat_frames.values():
            f.pack_forget()
        self.specs_page_frame.pack(fill="both", expand=True)
        self.scroll_canvas.yview_moveto(0)

    # ── Category Switching ───────────────────────────────────────────
    def _show_category(self, cat_name):
        if self.active_cat == cat_name:
            return

        # deselect specs tab if active
        if self.active_cat == "__specs__":
            self.pc_btn.configure(bg=SIDEBAR_BG, fg=TEXT_DIM)
            self.specs_page_frame.pack_forget()

        # Reset old sidebar highlight
        if self.active_cat and self.active_cat in self.cat_btns:
            self.cat_btns[self.active_cat].configure(bg=SIDEBAR_BG, fg=TEXT_DIM)

        self.active_cat = cat_name
        self.cat_btns[cat_name].configure(bg=SIDEBAR_SEL, fg=ACCENT_GLOW)

        cat_data = CATEGORIES[cat_name]
        self.cat_header.configure(text=f"{cat_data['icon']}   {cat_name}")
        count = len(cat_data["tweaks"])
        self.cat_count.configure(text=f"{count} tweak{'s' if count != 1 else ''} available")

        # Hide all, show selected
        self.specs_page_frame.pack_forget()
        for f in self.cat_frames.values():
            f.pack_forget()
        self.cat_frames[cat_name].pack(fill="both", expand=True, padx=20, pady=4)
        self.scroll_canvas.yview_moveto(0)

    # ── Tweak Card Builder ───────────────────────────────────────────
    def _build_tweak_card(self, parent, tw):
        risk_label, risk_color, risk_tip = tw["risk"]

        card = tk.Frame(parent, bg=BG_CARD, highlightbackground=BORDER,
                        highlightthickness=1, bd=0)
        card.pack(fill="x", pady=5, ipady=10)

        # Left section: checkbox + text
        left = tk.Frame(card, bg=BG_CARD)
        left.pack(side="left", fill="both", expand=True, padx=16, pady=6)

        var = tk.BooleanVar(value=False)
        self.tweak_vars[tw["name"]] = (var, tw)

        # Custom checkbox row
        chk_row = tk.Frame(left, bg=BG_CARD)
        chk_row.pack(fill="x")

        chk_canvas = tk.Canvas(chk_row, width=20, height=20, bg=BG_CARD,
                               highlightthickness=0, bd=0, cursor="hand2")
        chk_canvas.pack(side="left", padx=(0, 10), pady=2)

        def draw_chk():
            chk_canvas.delete("all")
            if var.get():
                self._round_rect(chk_canvas, 0, 0, 20, 20, 0, fill=ACCENT, outline="")
                chk_canvas.create_text(10, 10, text="\u2713", font=("Arial", 11, "bold"), fill="white")
            else:
                self._round_rect(chk_canvas, 0, 0, 20, 20, 0, fill="", outline=TEXT_DARK)

        self.chk_draw_funcs.append(draw_chk)

        def toggle(e=None):
            var.set(not var.get())
            draw_chk()
            self._update_stats()

        draw_chk()
        chk_canvas.bind("<Button-1>", toggle)

        title = tk.Label(chk_row, text=tw["name"], font=("Arial", 11, "bold"),
                         bg=BG_CARD, fg=TEXT, cursor="hand2", anchor="w")
        title.pack(side="left")
        title.bind("<Button-1>", toggle)

        applied_lbl = tk.Label(chk_row, text="", font=("Arial", 8, "bold"),
                               bg=BG_CARD, fg=GREEN)
        applied_lbl.pack(side="left", padx=10)
        self.tweak_applied_lbls[tw["name"]] = applied_lbl

        desc = tk.Label(left, text=tw["desc"], font=("Arial", 9),
                        bg=BG_CARD, fg=TEXT_DIM, anchor="w", justify="left", wraplength=520)
        desc.pack(fill="x", padx=30, pady=(2, 0))

        # Right section: risk badge
        right = tk.Frame(card, bg=BG_CARD)
        right.pack(side="right", padx=18, pady=6)

        badge = tk.Label(right, text=f"  {risk_label}  ", font=("Arial", 8, "bold"),
                         bg=BG_CARD, fg=risk_color, cursor="hand2",
                         highlightbackground=risk_color, highlightthickness=1)
        badge.pack()

        # Risk tooltip on hover
        badge.bind("<Enter>", lambda e, t=risk_tip, c=risk_color: self._show_tooltip(e, t, c))
        badge.bind("<Leave>", lambda e: self._hide_tooltip())

        # Card hover effect
        all_widgets = [card, left, chk_row, title, desc, right]
        for w in all_widgets:
            w.bind("<Enter>", lambda e, c=card: self._card_hover(c, True), add="+")
            w.bind("<Leave>", lambda e, c=card: self._card_hover(c, False), add="+")

    def _card_hover(self, card, entering):
        bg = BG_HOVER if entering else BG_CARD
        try:
            card.configure(bg=bg)
        except:
            return
        for child in card.winfo_children():
            try:
                child.configure(bg=bg)
            except:
                pass
            for sub in child.winfo_children():
                try:
                    if not isinstance(sub, tk.Canvas):
                        sub.configure(bg=bg)
                except:
                    pass

    # ── Tooltip ──────────────────────────────────────────────────────
    def _show_tooltip(self, event, text, color):
        self._hide_tooltip()
        x = event.widget.winfo_rootx() - 120
        y = event.widget.winfo_rooty() + 26
        tw = tk.Toplevel(self.root)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tw.attributes("-topmost", True)
        frame = tk.Frame(tw, bg=color, bd=0)
        frame.pack()
        inner = tk.Frame(frame, bg="#1a1a1a")
        inner.pack(padx=1, pady=1)
        tk.Label(inner, text=text, font=("Arial", 9), bg="#1a1a1a", fg=color,
                 wraplength=250, padx=10, pady=6, justify="left").pack()
        self.tooltip_win = tw

    def _hide_tooltip(self):
        if self.tooltip_win:
            self.tooltip_win.destroy()
            self.tooltip_win = None

    # ── Scroll ───────────────────────────────────────────────────────
    def _bind_mousewheel(self):
        self.root.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self):
        self.root.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.scroll_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # ── Selection ────────────────────────────────────────────────────
    def _select_all(self, e=None):
        for var, _ in self.tweak_vars.values():
            var.set(True)
        for fn in self.chk_draw_funcs:
            fn()
        self._update_stats()

    def _deselect_all(self, e=None):
        for var, _ in self.tweak_vars.values():
            var.set(False)
        for fn in self.chk_draw_funcs:
            fn()
        self._update_stats()

    def _update_stats(self):
        count = sum(1 for var, _ in self.tweak_vars.values() if var.get())
        total = len(self.tweak_vars)
        self.stats_lbl.configure(text=f"{count} / {total} tweaks selected")

    # ── Music Toggle ─────────────────────────────────────────────────
    def _show_music_status(self):
        if self.music_error:
            self._show_tooltip_at_cursor(self.music_error, RED)
        elif self.music_on:
            self._show_tooltip_at_cursor("Music playing at 35%", ACCENT)
        else:
            self._show_tooltip_at_cursor("Music paused", TEXT_DIM)

    def _show_tooltip_at_cursor(self, text, color):
        self._hide_tooltip()
        x = self.music_btn.winfo_rootx() - 150
        y = self.music_btn.winfo_rooty() + 26
        tw = tk.Toplevel(self.root)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tw.attributes("-topmost", True)
        frame = tk.Frame(tw, bg=color, bd=0)
        frame.pack()
        inner = tk.Frame(frame, bg="#1a1a1a")
        inner.pack(padx=1, pady=1)
        tk.Label(inner, text=text, font=("Arial", 9), bg="#1a1a1a", fg=color,
                 wraplength=300, padx=10, pady=6, justify="left").pack()
        self.tooltip_win = tw

    def _toggle_music(self, e=None):
        # Works with both event binding and Button command
        if self.music_error:
            messagebox.showinfo("Music", self.music_error)
            return

        self.music_on = not self.music_on
        if pygame is None:
            self.music_on = False
            self.music_error = "pygame not available"
            try:
                self.music_btn.configure(text="Music: N/A")
            except Exception:
                pass
            return

        try:
            if self.music_on:
                pygame.mixer.music.unpause()
                self.music_btn.configure(text="Music: ON")
            else:
                pygame.mixer.music.pause()
                self.music_btn.configure(text="Music: OFF")
        except Exception:
            pass

    # ── Apply Logic ──────────────────────────────────────────────────
    def _apply(self):
        selected = [(var, tw) for var, tw in self.tweak_vars.values() if var.get()]
        if not selected:
            messagebox.showwarning("Nothing Selected", "Pick at least one tweak to apply.")
            return

        # Check for HIGH risk tweaks
        high_risk = [tw["name"] for _, tw in selected if tw["risk"] == HIGH]
        msg = f"You have {len(selected)} tweaks selected.\n"
        if high_risk:
            msg += f"\n\u26A0  HIGH RISK tweaks included:\n"
            for h in high_risk:
                msg += f"   \u2022 {h}\n"
            msg += "\nThese trade security for performance.\n"
        msg += "\nA System Restore Point will be created first.\nProceed?"

        if not messagebox.askyesno("Confirm", msg):
            return

        # Run in thread so UI doesn't freeze
        threading.Thread(target=self._run_tweaks, args=(selected,), daemon=True).start()

    def _run_tweaks(self, selected):
        # Create restore point
        try:
            subprocess.run(
                'powershell -NoProfile -Command "Enable-ComputerRestore -Drive \'C:\\\'; Checkpoint-Computer -Description \'Before_TheVault_Optimizer\' -RestorePointType \'MODIFY_SETTINGS\'"',
                shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120
            )
        except:
            pass

        total = sum(len(tw["cmds"]) for _, tw in selected)
        done = 0

        for _, tw in selected:
            for cmd in tw["cmds"]:
                try:
                    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL, timeout=60)
                except:
                    pass
                done += 1

        self.root.after(0, lambda: messagebox.showinfo(
            "Done",
            f"Applied {len(selected)} tweaks ({done} commands executed).\n\n"
            "Restart your PC for all changes to take effect."
        ))


# ─── Entry Point ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    if not is_admin():
        try:
            # Try to re-run with admin privileges
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit()  # Exit this non-admin process; the admin version will run separately
        except Exception as e:
            print(f"⚠ Admin elevation failed: {e}")
            print("⚠ Continuing without admin (some tweaks may not work).")
            # Fall through to start the app anyway

    root = tk.Tk()
    app = OptimizerApp(root)
    root.mainloop()
