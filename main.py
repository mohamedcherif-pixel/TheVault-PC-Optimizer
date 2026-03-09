import os, sys, ctypes, subprocess, threading, time
import tkinter as tk
from tkinter import messagebox
import urllib.request
from urllib.parse import quote as urlquote
import json
import winreg
import shlex
import re
import webbrowser

# ════════════════════════════ App Version ═════════════════════════════
APP_VERSION = "v1.1.8"
GITHUB_REPO = "mohamedcherif-pixel/TheVault-PC-Optimizer"
CONTACT_EMAIL = "medcherif2004@gmail.com"

SKIP_LOADING = False  # Set to True to skip the loading/splash screen

_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "normietools_config.json")
_BREVO_SENDER = "medcherif2004@gmail.com"
def _load_brevo_key():
    key = os.environ.get("BREVO_API_KEY", "")
    if not key:
        try:
            with open(_CONFIG_PATH, "r") as f:
                key = json.loads(f.read()).get("brevo_api_key", "")
        except Exception:
            pass
    return key
_BREVO_KEY = _load_brevo_key()

pygame = None


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


# ═══════════════════════════ Color Palette ════════════════════════════
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


# ════════════════════════════ Risk levels ═════════════════════════════
# User request: show risk level colors (red/green/blue/yellow)
SAFE   = ("SAFE",   "green",      "No risk. Fully reversible, no side effects.")
LOW    = ("LOW",    "blue",       "Minimal risk. Fully reversible.")
MEDIUM = ("MEDIUM", "goldenrod",  "Moderate risk. Reduces a security layer or changes power behavior.")
HIGH   = ("HIGH",   "red",        "Higher risk. Trades security for performance. Understand before applying.")

# Tool icons for the Tools tab
TOOL_ICONS = {
    "Install 7-Zip": "\U0001F4E6",
    "Install Everything (Voidtools)": "\U0001F50D",
    "Install PowerToys": "\u26A1",
    "Install HWiNFO": "\U0001F5A5",
    "Install CPU-Z": "\U0001F4BB",
    "Install GPU-Z": "\U0001F3AE",
    "Install Process Explorer": "\U0001F4CA",
    "Install Autoruns": "\U0001F680",
    "Install WizTree": "\U0001F333",
    "Install MSI Afterburner": "\U0001F525",
    "Install NVCleanstall": "\u2728",
    "Install Bulk Crap Uninstaller": "\U0001F5D1",
    "Install ShareX": "\U0001F4F8",
    "Install Notepad++": "\U0001F4DD",
    "Install Rufus": "\U0001F4BE",
    "Install CrystalDiskInfo": "\U0001F4BF",
    "Install CrystalDiskMark": "\u23F1",
    "Install HWMonitor": "\U0001F321",
    "Install UniGetUI": "\U0001F4E5",
    "Install Ventoy": "\U0001F50C",
    "Install Flow Launcher": "\U0001F50E",
    "Install EarTrumpet": "\U0001F50A",
    "Install TCPView": "\U0001F310",
    "Install O&O ShutUp10++": "\U0001F6E1",
    "Install Process Monitor": "\U0001F50E",
    "Install Revo Uninstaller": "\U0001F4A5",
    "Install Snappy Driver Installer": "\U0001F3CE",
    "Install ExplorerPatcher": "\U0001F527",
    "Install QuickLook": "\U0001F441",
    "Install Ditto Clipboard": "\U0001F4CB",
    "Install LatencyMon": "\U0001F4C9",
    "Install Process Lasso": "\U0001F3AF",
    "Install ParkControl": "\U0001F9CA",
    "Install ThrottleStop": "\u26A0",
    "Install RTSS": "\U0001F4CA",
    "Install CapFrameX": "\U0001F4C8",
    "Install DDU": "\U0001F9F9",
    "Install Sysmon": "\U0001F50D",
    "Install Sophia Script": "\U0001F9E0",
    "Install privacy.sexy": "\U0001F6E1",
    "Install simplewall": "\U0001F6A7",
    "Install Portmaster": "\U0001F310",
    "Install Mem Reduct": "\U0001F4A7",
    "Install CRU": "\U0001F4FA",
    "Install CompactGUI": "\U0001F4E6",
    "Install GlassWire": "\U0001F4F6",
    "Install WPD": "\U0001F512",
    "Install LosslessCut": "\u2702",
    "Install AutoHotkey": "\U0001F916",
    "Install WizFile": "\U0001F5C3",
    "Install dupeGuru": "\U0001F46F",
    "Install FanControl": "\U0001F4A8",
    "Install OpenRGB": "\U0001F308",
    "Install LibreHardwareMonitor": "\U0001F9EA",
    "Install BlueScreenView": "\U0001F4A5",
    "Install ShellExView": "\U0001F4C2",
    "Install AppReadWriteCounter": "\U0001F4BD",
    "Install SoundVolumeView": "\U0001F3B5",
    "Install FullEventLogView": "\U0001F4DC",
    "Install Dependencies": "\U0001F517",
    "Install Resource Hacker": "\U0001F3A8",
    "Install x64dbg": "\U0001F41B",
    "Install MacType": "\U0001F524",
    "Install TranslucentTB": "\U0001FA9F",
    "Install ModernFlyouts": "\U0001F50A",
    "Install DevToys": "\U0001F9F0",
    "Install GlazeWM": "\U0001F5BC",
    "Install NanaZip": "\U0001F4E6",
    "Install Bulk Rename Utility": "\U0001F4CB",
    "Install AltSnap": "🖱",
    "Install SoundSwitch": "🎧",
    "Install TrafficMonitor": "📊",
    "Install Twinkle Tray": "💡",
    "Install SuperF4": "💢",
    "Install System Informer": "🔎",
    "Install RegCool": "🗃",
    "Install Czkawka": "🧹",
    "Install dnSpy": "🧬",
    "Install PE-bear": "🐻",
    "Install Espanso": "⌨",
    "Install Monitorian": "💻",
    "Install LocalSend": "📤",
    "Install NTLite": "💿",
    "Install WinSetView": "📁",
    "Install ScreenToGif": "🎬",
    "Install WinMerge": "🔄",
    "Install carnac": "🎹",
    "Install Flameshot": "📷",
    "Install Qalculate!": "🧮",
    "Install Quick CPU": "⚙",
    "Install Special K": "🎯",
    "Install Intel PresentMon": "📐",
    "Install NVIDIA FrameView": "📉",
    "Install AMD OCAT": "📏",
    "Install BenchMate": "🏅",
    "Install Intel XTU": "🔬",
    "Install UXTU": "🧬",
    "Install TweakPower": "🔩",
    "Install NetLimiter": "🌐",
    "Install ASIO4ALL": "🎵",
    "Install REAL": "🔇",
    "Install Core-to-Core Latency": "🧪",
    "Install Processes Priority Mgr": "📌",
    "Install RAMMap": "🗺",
    "Install Windows Memory Cleaner": "💧",
    "Install DiskCountersView": "💽",
    "Install NetworkCountersWatch": "📡",
    "Install Windhawk": "🦅",
    "Install Nilesoft Shell": "🐚",
    "Install Seelen UI": "🪟",
    "Install komorebi": "🌊",
    "Install Textify": "📋",
    "Install Sizer": "📐",
    "Install ZoomIt": "🔍",
    "Install scrcpy": "📱",
    "Install WhatIsHang": "🧊",
    "Install SophiApp": "🧠",
    "Install O&O AppBuster": "💣",
    "Install BleachBit": "🧽",
    "Install SharpKeys": "⌨",
    "Install ContextMenuManager": "📜",
    "Install Sandboxie-Plus": "📦",
    "Install Lively Wallpaper": "🎞",
    "Install QTTabBar": "📑",
    "Install PatchCleaner": "🧯",
    "Install SpaceSniffer": "🗺",
    "Install DNS Jumper": "🌍",
    "Install OpenHashTab": "🔏",
    "Install USBDeview": "🔌",
    "Install OCCT": "🔥",
    "Install FurMark": "🌡",
    "Install Core Temp": "🌡",
    "Install AIDA64": "🖥",
    "Install KeePassXC": "🔑",
    "Install Bitwarden": "🔐",
    "Install Malwarebytes": "🛡",
    "Install Brave Browser": "🦁",
    "Install Wireshark": "🦈",
    "Install WinDirStat": "📊",
    "Install FastCopy": "⚡",
    "Install TreeSize Free": "🌳",
    "Install File Converter": "🔄",
    "Install Rainmeter": "🎨",
    "Install Git": "🔀",
    "Install Windows Terminal": "💻",
    "Install PowerShell 7": "⚙",
    "Install Postman": "📬",
    "Install VLC": "🎬",
    "Install OBS Studio": "📹",
    "Install HandBrake": "🎞",
    "Install Audacity": "🎙",
    "Install GIMP": "🖌",
    "Install Obsidian": "📓",
    "Install Joplin": "📝",
    "Install KDE Connect": "📲",
    "Install Sumatra PDF": "📄",
    "Install Kdenlive": "🎥",
    "Install WireGuard": "🔒",
    "Install Nmap": "🗺",
    "Install HxD": "🔢",
    "Install MediaInfo": "ℹ",
    "Install WinSCP": "📂",
    "Install PuTTY": "🖥",
    "Install Clink": "⌨",
    "Install ImageGlass": "🖼",
    "Install foobar2000": "🎶",
    "Install MPC-HC": "▶",
    "Install yt-dlp": "⬇",
    "Install MKVToolNix": "🎞",
    "Install qBittorrent": "🌀",
    "Install Paint.NET": "🎨",
    "Install Double Commander": "📁",
}

TOOL_SUBCATEGORIES = {
    "\u26A1 Latency & Performance": [
        "Install LatencyMon", "Install Process Lasso", "Install ParkControl",
        "Install ThrottleStop", "Install RTSS", "Install CapFrameX",
        "Install MSI Afterburner", "Install Mem Reduct", "Install CompactGUI",
        "Install CRU",
        "Install Quick CPU", "Install Special K", "Install Intel PresentMon",
        "Install NVIDIA FrameView", "Install AMD OCAT", "Install BenchMate",
        "Install Intel XTU", "Install UXTU", "Install TweakPower",
        "Install NetLimiter", "Install ASIO4ALL", "Install REAL",
        "Install Core-to-Core Latency", "Install Processes Priority Mgr",
        "Install RAMMap", "Install Windows Memory Cleaner",
        "Install DNS Jumper",
        "Install OCCT", "Install FurMark",
    ],
    "\U0001F527 Hardware & Monitoring": [
        "Install HWiNFO", "Install CPU-Z", "Install GPU-Z", "Install HWMonitor",
        "Install CrystalDiskInfo", "Install CrystalDiskMark",
        "Install FanControl", "Install LibreHardwareMonitor", "Install OpenRGB",
        "Install TrafficMonitor", "Install Twinkle Tray", "Install Monitorian",
        "Install Core Temp", "Install AIDA64",
    ],
    "\U0001F6E1 Security & Privacy": [
        "Install O&O ShutUp10++", "Install Sophia Script", "Install privacy.sexy",
        "Install simplewall", "Install Portmaster", "Install GlassWire", "Install WPD",
        "Install SophiApp", "Install Sandboxie-Plus",
        "Install KeePassXC", "Install Bitwarden",
        "Install Malwarebytes", "Install Brave Browser",
        "Install WireGuard", "Install Nmap",
    ],
    "\U0001F50D System Diagnostics": [
        "Install Process Explorer", "Install Autoruns", "Install Process Monitor",
        "Install Sysmon", "Install BlueScreenView", "Install ShellExView",
        "Install AppReadWriteCounter", "Install FullEventLogView", "Install TCPView",
        "Install System Informer", "Install RegCool",
        "Install DiskCountersView", "Install NetworkCountersWatch",
        "Install WhatIsHang", "Install USBDeview",
        "Install Wireshark",
        "Install HxD", "Install MediaInfo",
    ],
    "\U0001F4E6 Files & Drivers": [
        "Install 7-Zip", "Install NanaZip", "Install Everything (Voidtools)",
        "Install WizTree", "Install WizFile", "Install dupeGuru",
        "Install Bulk Rename Utility", "Install Revo Uninstaller",
        "Install NVCleanstall", "Install DDU", "Install Snappy Driver Installer",
        "Install Bulk Crap Uninstaller",
        "Install Czkawka", "Install NTLite", "Install WinSetView",
        "Install O&O AppBuster", "Install BleachBit", "Install QTTabBar",
        "Install PatchCleaner", "Install SpaceSniffer",
        "Install WinDirStat", "Install FastCopy",
        "Install TreeSize Free", "Install File Converter",
        "Install WinSCP", "Install Double Commander",
    ],
    "\U0001F5A5 UI & Desktop": [
        "Install ExplorerPatcher", "Install TranslucentTB", "Install ModernFlyouts",
        "Install MacType", "Install GlazeWM", "Install EarTrumpet",
        "Install SoundVolumeView",
        "Install AltSnap", "Install SuperF4", "Install carnac", "Install SoundSwitch",
        "Install Windhawk", "Install Nilesoft Shell", "Install Seelen UI",
        "Install komorebi", "Install Sizer", "Install SharpKeys",
        "Install ContextMenuManager", "Install Lively Wallpaper",
        "Install Rainmeter",
        "Install ImageGlass",
    ],
    "\U0001F6E0 Dev & Power Tools": [
        "Install PowerToys", "Install DevToys", "Install x64dbg",
        "Install Resource Hacker", "Install Dependencies", "Install AutoHotkey",
        "Install Notepad++", "Install ShareX",
        "Install dnSpy", "Install PE-bear", "Install WinMerge",
        "Install Textify", "Install ZoomIt", "Install OpenHashTab",
        "Install Git", "Install Windows Terminal",
        "Install PowerShell 7", "Install Postman",
        "Install PuTTY", "Install Clink",
    ],
    "\U0001F4F1 Productivity & Media": [
        "Install Flow Launcher", "Install QuickLook", "Install Ditto Clipboard",
        "Install UniGetUI", "Install LosslessCut", "Install Rufus", "Install Ventoy",
        "Install Espanso", "Install LocalSend", "Install ScreenToGif",
        "Install Flameshot", "Install Qalculate!",
        "Install scrcpy",
        "Install VLC", "Install OBS Studio",
        "Install HandBrake", "Install Audacity",
        "Install GIMP", "Install Obsidian",
        "Install Joplin", "Install KDE Connect",
        "Install Sumatra PDF", "Install Kdenlive",
        "Install foobar2000", "Install MPC-HC",
        "Install yt-dlp", "Install MKVToolNix",
        "Install qBittorrent", "Install Paint.NET",
    ],
}



# ════════════════════ Internationalisation (i18n) ═════════════════════
SUPPORTED_LANGS = ["English", "Français", "Tounsi", "Español", "Deutsch", "العربية"]
LANG_CODES = {"English": "en", "Français": "fr", "Tounsi": "tn", "Español": "es", "Deutsch": "de", "العربية": "ar"}

TRANSLATIONS = {
    # ── Window / Header ──
    "app_title":        {"en": "NormieTools by MedCherif  ·  {v}", "fr": "NormieTools par MedCherif  ·  {v}", "tn": "NormieTools par MedCherif  .  {v}", "es": "NormieTools de MedCherif  ·  {v}", "de": "NormieTools von MedCherif  ·  {v}", "ar": "أدوات MedCherif  ·  {v}"},
    "header":           {"en": "NormieTools // PC Optimizer :: {v}", "fr": "NormieTools // Optimiseur PC :: {v}", "tn": "NormieTools // Optimiseur PC :: {v}", "es": "NormieTools // Optimizador PC :: {v}", "de": "NormieTools // PC Optimizer :: {v}", "ar": "NormieTools // محسّن الكمبيوتر :: {v}"},
    "audio_on":         {"en": "AUDIO: ON",  "fr": "AUDIO : ACTIVÉ", "tn": "SAWT: MFAA3EL", "es": "AUDIO: ON", "de": "AUDIO: AN", "ar": "الصوت: مفعّل"},
    "audio_off":        {"en": "AUDIO: OFF", "fr": "AUDIO : DÉSACTIVÉ", "tn": "SAWT: MATFI", "es": "AUDIO: OFF", "de": "AUDIO: AUS", "ar": "الصوت: معطّل"},
    "audio_na":         {"en": "AUDIO: N/A", "fr": "AUDIO : N/D", "tn": "SAWT: MANAJEMCH", "es": "AUDIO: N/D", "de": "AUDIO: N/V", "ar": "الصوت: غ/م"},
    "feedback_btn":     {"en": "✉ FEEDBACK",  "fr": "✉ AVIS", "tn": "✉ RA2YEK", "es": "✉ OPINIÓN", "de": "✉ FEEDBACK", "ar": "✉ رأيك"},
    "specs_header":     {"en": "SYSTEM ANALYSIS", "fr": "ANALYSE SYSTÈME", "tn": "TAHLIL EL SYSTEME", "es": "ANÁLISIS DEL SISTEMA", "de": "SYSTEMANALYSE", "ar": "تحليل النظام"},
    "tweaks_header":    {"en": "TWEAKS / OPTIMIZATIONS", "fr": "TWEAKS / OPTIMISATIONS", "tn": "TWEAKS / TA7SINAT", "es": "TWEAKS / OPTIMIZACIONES", "de": "TWEAKS / OPTIMIERUNGEN", "ar": "التعديلات / التحسينات"},
    "syncing":          {"en": "synchronizing...", "fr": "synchronisation...", "tn": "jari el mzamna...", "es": "sincronizando...", "de": "synchronisiere...", "ar": "...جاري المزامنة"},
    "syncing_long":     {"en": ">> SYNCHRONIZING SYSTEM DATA...", "fr": ">> SYNCHRONISATION DES DONNÉES SYSTÈME...", "tn": ">> JARI EL MZAMNA...", "es": ">> SINCRONIZANDO DATOS DEL SISTEMA...", "de": ">> SYSTEMDATEN WERDEN SYNCHRONISIERT...", "ar": ">> جاري مزامنة بيانات النظام..."},
    "stats_init":       {"en": "0 / 0 TWEAKS PENDING", "fr": "0 / 0 TWEAKS EN ATTENTE", "tn": "0 / 0 TWEAKS YESTANAW", "es": "0 / 0 TWEAKS PENDIENTES", "de": "0 / 0 TWEAKS AUSSTEHEND", "ar": "0 / 0 تعديلات معلّقة"},
    "stats":            {"en": "> {a} APPLY + {r} RESTORE / {t} TOTAL", "fr": "> {a} APPLIQUER + {r} RESTAURER / {t} TOTAL", "tn": "> {a} TABBEK + {r} RJAA3 / {t} MAJMOU3", "es": "> {a} APLICAR + {r} RESTAURAR / {t} TOTAL", "de": "> {a} ANWENDEN + {r} ZURÜCKSETZEN / {t} GESAMT", "ar": "> {a} تطبيق + {r} استعادة / {t} المجموع"},
    "select_all":       {"en": "[ SELECT ALL ]", "fr": "[ TOUT SÉLECTIONNER ]", "tn": "[ 5TAR EL KOLL ]", "es": "[ SELECCIONAR TODO ]", "de": "[ ALLE AUSWÄHLEN ]", "ar": "[ تحديد الكل ]"},
    "purge":            {"en": "[ PURGE SELECTION ]", "fr": "[ PURGER SÉLECTION ]", "tn": "[ AMS7A EL 5TYAR ]", "es": "[ PURGAR SELECCIÓN ]", "de": "[ AUSWAHL LÖSCHEN ]", "ar": "[ مسح التحديد ]"},
    "execute":          {"en": "APPLY TWEAKS", "fr": "APPLIQUER LES TWEAKS", "tn": "TABBEK EL TWEAKS", "es": "APLICAR TWEAKS", "de": "TWEAKS ANWENDEN", "ar": "تطبيق التعديلات"},
    "applied":          {"en": "APPLIED", "fr": "APPLIQUÉ", "tn": "MATABBEK", "es": "APLICADO", "de": "ANGEWENDET", "ar": "مُطبَّق"},
    # ── Risk levels ──
    "risk_safe":        {"en": "SAFE",   "fr": "SÛR", "tn": "AMEN", "es": "SEGURO", "de": "SICHER", "ar": "آمن"},
    "risk_low":         {"en": "LOW",    "fr": "FAIBLE", "tn": "DHAIF", "es": "BAJO", "de": "NIEDRIG", "ar": "منخفض"},
    "risk_medium":      {"en": "MEDIUM", "fr": "MOYEN", "tn": "MOUTAWASSET", "es": "MEDIO", "de": "MITTEL", "ar": "متوسط"},
    "risk_high":        {"en": "HIGH",   "fr": "ÉLEVÉ", "tn": "3ALI", "es": "ALTO", "de": "HOCH", "ar": "عالي"},
    # ── Feedback dialog ──
    "fb_title":         {"en": "FEEDBACK TERMINAL", "fr": "TERMINAL DE RETOUR", "tn": "RA2YEK", "es": "TERMINAL DE OPINIONES", "de": "FEEDBACK-TERMINAL", "ar": "محطة الملاحظات"},
    "fb_header":        {"en": ">> FEEDBACK TERMINAL", "fr": ">> TERMINAL DE RETOUR", "tn": ">> RA2YEK", "es": ">> TERMINAL DE OPINIONES", "de": ">> FEEDBACK-TERMINAL", "ar": ">> محطة الملاحظات"},
    "fb_subtitle":      {"en": "Report bugs or suggest enhancements", "fr": "Signaler des bugs ou suggérer des améliorations", "tn": "A3mel signalement 3la bug walla a3ti ra2yek", "es": "Reportar errores o sugerir mejoras", "de": "Fehler melden oder Verbesserungen vorschlagen", "ar": "أبلغ عن أخطاء أو اقترح تحسينات"},
    "fb_type":          {"en": "TYPE:", "fr": "TYPE :", "tn": "NAW3 :", "es": "TIPO:", "de": "TYP:", "ar": "النوع:"},
    "fb_bug":           {"en": "Bug Report", "fr": "Rapport de bug", "tn": "Signalement bug", "es": "Informe de error", "de": "Fehlerbericht", "ar": "تقرير خطأ"},
    "fb_suggestion":    {"en": "Suggestion", "fr": "Suggestion", "tn": "Suggestion", "es": "Sugerencia", "de": "Vorschlag", "ar": "اقتراح"},
    "fb_general":       {"en": "General Feedback", "fr": "Retour général", "tn": "Ra2y 3am", "es": "Opinión general", "de": "Allgemeines Feedback", "ar": "ملاحظة عامة"},
    "fb_message":       {"en": "MESSAGE:", "fr": "MESSAGE :", "tn": "RISSALA :", "es": "MENSAJE:", "de": "NACHRICHT:", "ar": "الرسالة:"},
    "fb_placeholder":   {"en": "Describe the bug or your suggestion here...", "fr": "Décrivez le bug ou votre suggestion ici...", "tn": "Ekteb 3la el bug walla ra2yek hne...", "es": "Describe el error o tu sugerencia aquí...", "de": "Beschreiben Sie den Fehler oder Ihren Vorschlag...", "ar": "...صف الخطأ أو اقتراحك هنا"},
    "fb_send":          {"en": "TRANSMIT FEEDBACK", "fr": "TRANSMETTRE LE RETOUR", "tn": "AB3ATH", "es": "TRANSMITIR OPINIÓN", "de": "FEEDBACK SENDEN", "ar": "إرسال الملاحظات"},
    "fb_abort":         {"en": "[ ABORT ]", "fr": "[ ANNULER ]", "tn": "[ ANNULER ]", "es": "[ CANCELAR ]", "de": "[ ABBRECHEN ]", "ar": "[ إلغاء ]"},
    "fb_empty_title":   {"en": "Empty Message", "fr": "Message vide", "tn": "Rissala fergha", "es": "Mensaje vacío", "de": "Leere Nachricht", "ar": "رسالة فارغة"},
    "fb_empty_msg":     {"en": "Please write a message before sending.", "fr": "Veuillez écrire un message avant d'envoyer.", "tn": "Ouktob rissala 9bal ma tab3ath.", "es": "Escribe un mensaje antes de enviar.", "de": "Bitte schreiben Sie eine Nachricht.", "ar": "يرجى كتابة رسالة قبل الإرسال."},
    "fb_sent_title":    {"en": "Feedback", "fr": "Retour", "tn": "Ra2y", "es": "Opinión", "de": "Feedback", "ar": "ملاحظات"},
    "fb_sent_msg":      {"en": "Feedback sent successfully!\nThank you for your input.", "fr": "Retour envoyé avec succès !\nMerci pour votre contribution.", "tn": "Ra2yek twassal! Chokran.", "es": "¡Opinión enviada con éxito!\nGracias.", "de": "Feedback erfolgreich gesendet!\nVielen Dank.", "ar": "تم إرسال الملاحظات بنجاح!\nشكراً لك."},
    "fb_sent_browser":  {"en": "Your feedback has been prepared as a GitHub issue.\nPlease click 'Submit new issue' in your browser to complete.", "fr": "Votre retour a été préparé sur GitHub.\nCliquez sur 'Submit new issue' dans votre navigateur.", "tn": "Ra2yek mawjoud fi GitHub.\nA3mel Submit.", "es": "Tu opinión se ha preparado en GitHub.\nHaz clic en 'Submit new issue' en tu navegador.", "de": "Ihr Feedback wurde als GitHub-Issue vorbereitet.\nKlicken Sie auf 'Submit new issue' in Ihrem Browser.", "ar": "تم تجهيز ملاحظاتك كقضية GitHub.\nانقر على 'Submit new issue' في المتصفح."},
    "fb_sending":       {"en": "SENDING...", "fr": "ENVOI...", "tn": "YAB3ATH...", "es": "ENVIANDO...", "de": "SENDEN...", "ar": "...جاري الإرسال"},
    "fb_err_title":     {"en": "Error", "fr": "Erreur", "tn": "Ghalta", "es": "Error", "de": "Fehler", "ar": "خطأ"},
    "fb_err_msg":       {"en": "Could not send feedback:\n{e}", "fr": "Impossible d'envoyer le retour :\n{e}", "tn": "Ma najamtch nab3ath el ra2y:\n{e}", "es": "No se pudo enviar la opinión:\n{e}", "de": "Feedback konnte nicht gesendet werden:\n{e}", "ar": "تعذر إرسال الملاحظات:\n{e}"},
    "fb_rating_set":    {"en": "Current Rating: {s} ({n}/5)", "fr": "Note actuelle : {s} ({n}/5)", "tn": "Note actuelle : {s} ({n}/5)", "es": "Puntuación actual: {s} ({n}/5)", "de": "Aktuelle Bewertung: {s} ({n}/5)", "ar": "التقييم الحالي: {s} ({n}/5)"},
    "fb_rating_none":   {"en": "No rating set (use stars in the top bar)", "fr": "Aucune note (utilisez les étoiles en haut)", "tn": "Aucune note", "es": "Sin puntuación (usa las estrellas arriba)", "de": "Keine Bewertung (Sterne oben nutzen)", "ar": "لا تقييم (استخدم النجوم أعلاه)"},
    # ── Apply / Confirm dialog ──
    "nothing_title":    {"en": "Nothing Selected", "fr": "Rien de sélectionné", "tn": "Ma 5tart 7atta 7aja", "es": "Nada seleccionado", "de": "Nichts ausgewählt", "ar": "لم يتم تحديد شيء"},
    "nothing_msg":      {"en": "Pick at least one tweak to apply, or uncheck an applied tweak to restore it.", "fr": "Choisissez au moins un tweak à appliquer, ou décochez un tweak appliqué pour le restaurer.", "tn": "5tar 3al a9all tweak wa7ed.", "es": "Selecciona al menos un ajuste a aplicar o desmarca uno aplicado para restaurarlo.", "de": "Wählen Sie mindestens einen Tweak zum Anwenden oder deaktivieren Sie einen angewendeten zum Zurücksetzen.", "ar": "اختر تعديلاً واحداً على الأقل أو ألغِ تحديد تعديل مطبّق لاستعادته."},
    "conflict_title":   {"en": "Conflict", "fr": "Conflit", "tn": "Ta3arod", "es": "Conflicto", "de": "Konflikt", "ar": "تعارض"},
    "conflict_msg":     {"en": "Cannot apply both:\n\n• {a}\n• {b}\n\nThey write opposite values. Please deselect one.", "fr": "Impossible d'appliquer les deux :\n\n• {a}\n• {b}\n\nIls écrivent des valeurs opposées. Veuillez en désélectionner un.", "tn": "Impossible d'appliquer les deux :\n\n- {a}\n- {b}\n\nDeselectionnez un.", "es": "No se pueden aplicar ambos:\n\n• {a}\n• {b}\n\nEscriben valores opuestos. Deselecciona uno.", "de": "Beide können nicht angewendet werden:\n\n• {a}\n• {b}\n\nSie schreiben gegensätzliche Werte. Bitte einen abwählen.", "ar": "لا يمكن تطبيق كليهما:\n\n• {a}\n• {b}\n\nيكتبان قيماً متعاكسة. ألغِ تحديد أحدهما."},
    "confirm_title":    {"en": "Confirm", "fr": "Confirmer", "tn": "Akked", "es": "Confirmar", "de": "Bestätigen", "ar": "تأكيد"},
    "confirm_apply":    {"en": "Applying {n} tweaks.\n", "fr": "Application de {n} tweaks.\n", "tn": "Bech ntabkaw {n} tweaks.\n", "es": "Aplicando {n} ajustes.\n", "de": "{n} Tweaks werden angewendet.\n", "ar": "جاري تطبيق {n} تعديلات.\n"},
    "confirm_high":     {"en": "\n⚠  HIGH RISK tweaks included:\n", "fr": "\n⚠  Tweaks à RISQUE ÉLEVÉ inclus :\n", "tn": "\n/!\\ Tweaks a RISQUE ELEVE :\n", "es": "\n⚠  Ajustes de ALTO RIESGO incluidos:\n", "de": "\n⚠  HOHES RISIKO Tweaks enthalten:\n", "ar": "\n⚠  تعديلات عالية الخطورة:\n"},
    "confirm_high_warn":{"en": "\nThese trade security for performance.\n", "fr": "\nCeux-ci sacrifient la sécurité pour la performance.\n", "tn": "\nCeux-ci sacrifient la securite.\n", "es": "\nEstos sacrifican seguridad por rendimiento.\n", "de": "\nDiese tauschen Sicherheit gegen Leistung.\n", "ar": "\nهذه تضحي بالأمان مقابل الأداء.\n"},
    "confirm_restore":  {"en": "\n🔄  RESTORING {n} previously applied tweaks:\n", "fr": "\n🔄  RESTAURATION de {n} tweaks précédemment appliqués :\n", "tn": "\n>> RESTAURATION de {n} tweaks :\n", "es": "\n🔄  RESTAURANDO {n} ajustes aplicados:\n", "de": "\n🔄  {n} angewendete Tweaks ZURÜCKSETZEN:\n", "ar": "\n🔄  استعادة {n} تعديلات مطبّقة:\n"},
    "confirm_defaults": {"en": "\nThese will be reverted to Windows defaults.\n", "fr": "\nCeux-ci seront rétablis aux valeurs par défaut de Windows.\n", "tn": "\nCeux-ci seront retablis.\n", "es": "\nEstos se revertirán a los valores predeterminados.\n", "de": "\nDiese werden auf Standardwerte zurückgesetzt.\n", "ar": "\nسيتم إعادتها إلى الإعدادات الافتراضية.\n"},
    "confirm_footer":   {"en": "\nA System Restore Point will be created first.\nProceed?", "fr": "\nUn point de restauration système sera créé d'abord.\nProcéder ?", "tn": "\nUn point de restauration sera cree.\nProceder ?", "es": "\nSe creará un punto de restauración primero.\n¿Continuar?", "de": "\nEin Wiederherstellungspunkt wird zuerst erstellt.\nFortfahren?", "ar": "\nسيتم إنشاء نقطة استعادة أولاً.\nهل تريد المتابعة؟"},
    "done_title":       {"en": "Done", "fr": "Terminé", "tn": "Kammel", "es": "Hecho", "de": "Fertig", "ar": "تم"},
    "done_applied":     {"en": "Applied {n} tweaks ({c} commands).", "fr": "{n} tweaks appliqués ({c} commandes).", "tn": "{n} tweaks appliques ({c} commandes).", "es": "{n} ajustes aplicados ({c} comandos).", "de": "{n} Tweaks angewendet ({c} Befehle).", "ar": "تم تطبيق {n} تعديلات ({c} أوامر)."},
    "done_restored":    {"en": "Restored {n} tweaks ({c} reverse commands).", "fr": "{n} tweaks restaurés ({c} commandes inverses).", "tn": "{n} tweaks restaures ({c} commandes).", "es": "{n} ajustes restaurados ({c} comandos).", "de": "{n} Tweaks zurückgesetzt ({c} Befehle).", "ar": "تم استعادة {n} تعديلات ({c} أوامر)."},
    "done_restart":     {"en": "\n\nRestart your PC for all changes to take effect.", "fr": "\n\nRedémarrez votre PC pour que les modifications prennent effet.", "tn": "\n\nRedemarrez votre PC.", "es": "\n\nReinicia tu PC para aplicar todos los cambios.", "de": "\n\nStarten Sie Ihren PC neu, damit alle Änderungen wirksam werden.", "ar": "\n\nأعد تشغيل الكمبيوتر لتطبيق التغييرات."},
    "exec_err_title":   {"en": "Error", "fr": "Erreur", "tn": "Ghalta", "es": "Error", "de": "Fehler", "ar": "خطأ"},
    "exec_err_msg":     {"en": "Tweak execution failed:\n{e}", "fr": "L'exécution du tweak a échoué :\n{e}", "tn": "L'execution a echoue :\n{e}", "es": "La ejecución del ajuste falló:\n{e}", "de": "Tweak-Ausführung fehlgeschlagen:\n{e}", "ar": "فشل تنفيذ التعديل:\n{e}"},
    # ── Batch file text ──
    "bat_title":        {"en": "[NormieTools] Optimizer - Live Execution Log", "fr": "[NormieTools] Optimiseur - Journal d'exécution", "tn": "[NormieTools] Optimiseur - Journal", "es": "[NormieTools] Optimizador - Registro", "de": "[NormieTools] Optimierer - Ausführungsprotokoll", "ar": "[NormieTools] المحسّن - سجل التنفيذ"},
    "bat_header":       {"en": "[NormieTools] PC Optimizer - Live Execution Log", "fr": "[NormieTools] Optimiseur PC - Journal d'exécution", "tn": "[NormieTools] Optimiseur PC - Journal", "es": "[NormieTools] Optimizador PC - Registro", "de": "[NormieTools] PC-Optimierer - Protokoll", "ar": "[NormieTools] محسّن الكمبيوتر - سجل"},
    "bat_applying":     {"en": "APPLYING", "fr": "APPLICATION", "tn": "JARI NTABKAW", "es": "APLICANDO", "de": "ANWENDEN", "ar": "تطبيق"},
    "bat_restoring":    {"en": "RESTORING", "fr": "RESTAURATION", "tn": "JARI NRJA3OU", "es": "RESTAURANDO", "de": "ZURÜCKSETZEN", "ar": "استعادة"},
    "bat_ok":           {"en": "[OK] Done!", "fr": "[OK] Terminé !", "tn": "[OK] Kammel!", "es": "[OK] ¡Hecho!", "de": "[OK] Fertig!", "ar": "[OK] تم!"},
    "bat_ok_restore":   {"en": "[OK] Restored!", "fr": "[OK] Restauré !", "tn": "[OK] Rja3et!", "es": "[OK] ¡Restaurado!", "de": "[OK] Zurückgesetzt!", "ar": "[OK] تمت الاستعادة!"},
    "bat_warn":         {"en": "[WARN] Command returned error", "fr": "[AVERT] La commande a retourné l'erreur", "tn": "[AVERT] Ghalta", "es": "[AVISO] El comando devolvió un error", "de": "[WARNUNG] Befehl gab Fehler zurück", "ar": "[تحذير] أرجع الأمر خطأ"},
    "bat_complete":     {"en": "All tasks completed! ({a} apply + {r} restore)", "fr": "Toutes les tâches terminées ! ({a} appliquées + {r} restaurées)", "tn": "El koll kammel! ({a} matabbka + {r} rja3ou)", "es": "¡Todas las tareas completadas! ({a} aplicadas + {r} restauradas)", "de": "Alle Aufgaben abgeschlossen! ({a} angewendet + {r} zurückgesetzt)", "ar": "اكتملت جميع المهام! ({a} تطبيق + {r} استعادة)"},
    "bat_press_key":    {"en": "Press any key to close this window...", "fr": "Appuyez sur une touche pour fermer...", "tn": "O9ros 3la ay touche...", "es": "Pulsa cualquier tecla para cerrar...", "de": "Beliebige Taste drücken zum Schließen...", "ar": "اضغط أي مفتاح للإغلاق..."},
    # ── Update dialog ──
    "update_title":     {"en": "Update Available", "fr": "Mise à jour disponible", "tn": "Update jdid mawjoud", "es": "Actualización disponible", "de": "Update verfügbar", "ar": "تحديث متاح"},
    "update_msg":       {"en": "A new version ({v}) is available!\n\nWould you like to apply the update now?", "fr": "Une nouvelle version ({v}) est disponible !\n\nVoulez-vous appliquer la mise à jour maintenant ?", "tn": "Nouvelle version ({v}) disponible !\n\nMettre a jour maintenant ?", "es": "¡Una nueva versión ({v}) está disponible!\n\n¿Deseas actualizarla ahora?", "de": "Eine neue Version ({v}) ist verfügbar!\n\nJetzt aktualisieren?", "ar": "إصدار جديد ({v}) متاح!\n\nهل تريد التحديث الآن؟"},
    "update_patching":  {"en": ">> PATCHING...", "fr": ">> MISE À JOUR...", "tn": ">> MISE A JOUR...", "es": ">> PARCHEANDO...", "de": ">> WIRD GEPATCHT...", "ar": ">> ...جاري التحديث"},
    "update_starting":  {"en": "Starting download...", "fr": "Démarrage du téléchargement...", "tn": "Bech yebda el telechargement...", "es": "Iniciando descarga...", "de": "Download wird gestartet...", "ar": "...جاري بدء التنزيل"},
    "update_dl":        {"en": "Downloading core patches... {p}%", "fr": "Téléchargement des correctifs... {p}%", "tn": "Jari yetchargi... {p}%", "es": "Descargando parches... {p}%", "de": "Patches herunterladen... {p}%", "ar": "...جاري تنزيل التحديثات {p}%"},
    "update_dl_kb":     {"en": "Downloading... {kb} KB", "fr": "Téléchargement... {kb} Ko", "tn": "Jari yetchargi... {kb} Ko", "es": "Descargando... {kb} KB", "de": "Herunterladen... {kb} KB", "ar": "...جاري التنزيل {kb} ك.ب"},
    "update_applying":  {"en": "Applying update...", "fr": "Application de la mise à jour...", "tn": "Jari el update...", "es": "Aplicando actualización...", "de": "Update wird angewendet...", "ar": "...جاري تطبيق التحديث"},
    "update_dev_title": {"en": "Developer Mode", "fr": "Mode développeur", "tn": "Mode dev", "es": "Modo desarrollador", "de": "Entwicklermodus", "ar": "وضع المطور"},
    "update_dev_msg":   {"en": "Hot-patching disabled in script mode. Downloaded to temp folder.", "fr": "Mise à jour à chaud désactivée en mode script. Téléchargé dans le dossier temp.", "tn": "Mise a jour a chaud desactivee. Telecharge dans temp.", "es": "Parcheo en caliente deshabilitado. Descargado en carpeta temp.", "de": "Hot-Patching im Skriptmodus deaktiviert. In Temp heruntergeladen.", "ar": "التحديث المباشر معطّل. تم التنزيل في المجلد المؤقت."},
    "update_err_title": {"en": "Update Error", "fr": "Erreur de mise à jour", "tn": "Ghalta fil update", "es": "Error de actualización", "de": "Update-Fehler", "ar": "خطأ في التحديث"},
    "update_err_msg":   {"en": "Patching failed: {e}", "fr": "La mise à jour a échoué : {e}", "tn": "El update ma5demch: {e}", "es": "El parcheo falló: {e}", "de": "Patching fehlgeschlagen: {e}", "ar": "فشل التحديث: {e}"},
    # ── Language selector ──
    "lang_label":       {"en": "LANG:", "fr": "LANGUE :", "tn": "LOGHA :", "es": "IDIOMA:", "de": "SPRACHE:", "ar": "اللغة:"},
}

# ── Category display names ──
CAT_NAMES = {
    "System  Core":         {"en": "System  Core",         "fr": "Système  Noyau", "tn": "Systeme  w Noyau", "es": "Sistema  Núcleo", "de": "System  Kern", "ar": "النظام  الأساسي"},
    "GPU  &  Gaming":       {"en": "GPU  &  Gaming",       "fr": "GPU  &  Jeux", "tn": "GPU  &  L3ab", "es": "GPU  &  Juegos", "de": "GPU  &  Spiele", "ar": "بطاقة الرسوم  والألعاب"},
    "Timer  &  Clock":      {"en": "Timer  &  Clock",      "fr": "Minuteur  &  Horloge", "tn": "Timer  &  Sa3a", "es": "Temporizador  &  Reloj", "de": "Timer  &  Uhr", "ar": "المؤقت  والساعة"},
    "Network":              {"en": "Network",              "fr": "Réseau", "tn": "Réseau", "es": "Red", "de": "Netzwerk", "ar": "الشبكة"},
    "Power  &  CPU":        {"en": "Power  &  CPU",        "fr": "Énergie  &  CPU", "tn": "Ta9a  &  CPU", "es": "Energía  &  CPU", "de": "Energie  &  CPU", "ar": "الطاقة  والمعالج"},
    "MSI  &  Interrupts":   {"en": "MSI  &  Interrupts",   "fr": "MSI  &  Interruptions", "tn": "MSI  &  Interruptions", "es": "MSI  &  Interrupciones", "de": "MSI  &  Interrupts", "ar": "MSI  والمقاطعات"},
    "Mouse  &  Input":      {"en": "Mouse  &  Input",      "fr": "Souris  &  Entrée", "tn": "Mouse  &  Dkhoul", "es": "Ratón  &  Entrada", "de": "Maus  &  Eingabe", "ar": "الماوس  والإدخال"},
    "Privacy  &  Telemetry":{"en": "Privacy  &  Telemetry","fr": "Confidentialité  &  Télémétrie", "tn": "5sousiya  &  Telemetrie", "es": "Privacidad  &  Telemetría", "de": "Datenschutz  &  Telemetrie", "ar": "الخصوصية  والقياس"},
    "Services  &  Tasks":   {"en": "Services  &  Tasks",   "fr": "Services  &  Tâches", "tn": "Services  &  Taches", "es": "Servicios  &  Tareas", "de": "Dienste  &  Aufgaben", "ar": "الخدمات  والمهام"},
    "Cleanup":              {"en": "Cleanup",              "fr": "Nettoyage", "tn": "Tandhif", "es": "Limpieza", "de": "Bereinigung", "ar": "التنظيف"},
    "UI  &  QoL":           {"en": "UI  &  QoL",           "fr": "Interface  &  QdV", "tn": "Interface  &  QdV", "es": "Interfaz  &  CdV", "de": "UI  &  Komfort", "ar": "الواجهة  وجودة الحياة"},
    "Tools  &  Downloads":  {"en": "Tools  &  Downloads",  "fr": "Outils  &  Telechargements", "tn": "Outils  &  Ta7mil", "es": "Herramientas  &  Descargas", "de": "Tools  &  Downloads", "ar": "الأدوات  والتنزيلات"},
}

# ── Tweak display names ──
TWEAK_NAMES = {
    "Disable All Background UWP Apps": {"en": "Disable All Background UWP Apps", "fr": "Désactiver les applis UWP en arrière-plan", "tn": "Ymanea applis UWP mel background w enti tel3ab. Yfarregh el memoire w CPU.", "es": "Desactivar todas las apps UWP en segundo plano", "de": "Alle UWP-Hintergrund-Apps deaktivieren", "ar": "تعطيل جميع تطبيقات UWP في الخلفية"},
    "Disable VBS / HVCI / Core Isolation": {"en": "Disable VBS / HVCI / Core Isolation", "fr": "Désactiver VBS / HVCI / Isolation du noyau", "tn": "Yna77i el hyperviseur eli yzid 5-10% overhead 3la kol acces memoire. Microsoft y7otha 3al Win11 bla ma t3arrek.", "es": "Desactivar VBS / HVCI / Aislamiento del núcleo", "de": "VBS / HVCI / Kernisolierung deaktivieren", "ar": "تعطيل VBS / HVCI / عزل النواة"},
    "Disable Spectre / Meltdown Mitigations": {"en": "Disable Spectre / Meltdown Mitigations", "fr": "Désactiver les protections Spectre / Meltdown", "tn": "Yna77i les patches taa3 Spectre/Meltdown eli yzidou 2-8% overhead. Akber impact 3al I/O.", "es": "Desactivar mitigaciones Spectre / Meltdown", "de": "Spectre / Meltdown Schutzmaßnahmen deaktivieren", "ar": "تعطيل حماية Spectre / Meltdown"},
    "Elevate CSRSS & DWM Priority": {"en": "Elevate CSRSS & DWM Priority", "fr": "Élever la priorité CSRSS & DWM", "tn": "Ya3ti csrss.exe w dwm.exe priorite 3alya bech el souris w les frames ma yostannewch.", "es": "Elevar prioridad CSRSS y DWM", "de": "CSRSS & DWM Priorität erhöhen", "ar": "رفع أولوية CSRSS و DWM"},
    "Disable Page Combining (Memory Dedup)": {"en": "Disable Page Combining (Memory Dedup)", "fr": "Désactiver la combinaison de pages (dédup mémoire)", "tn": "Ywakef el scanner RAM mel background. Ywaffar CPU; yesta3mel chwaya akther RAM.", "es": "Desactivar combinación de páginas (dedup memoria)", "de": "Seitenkombination deaktivieren (Speider-Dedup)", "ar": "تعطيل دمج الصفحات (تكرار الذاكرة)"},
    "Lock Kernel & Drivers in RAM": {"en": "Lock Kernel & Drivers in RAM", "fr": "Verrouiller le noyau & pilotes en RAM", "tn": "El noyau NT w les drivers yab9aw fel RAM. Yna77i el micro-stutters. Lazem 8 Go+ RAM.", "es": "Bloquear kernel y drivers en RAM", "de": "Kernel & Treiber im RAM sperren", "ar": "قفل النواة والتعريفات في RAM"},
    "Optimize Win32 CPU Scheduling": {"en": "Optimize Win32 CPU Scheduling", "fr": "Optimiser l'ordonnancement CPU Win32", "tn": "Quantum court w variable m3a boost 3:1 lel fenetre active. 3x temps CPU lel foreground.", "es": "Optimizar planificación CPU Win32", "de": "Win32 CPU-Planung optimieren", "ar": "تحسين جدولة Win32 للمعالج"},
    "Disable CFG (Control Flow Guard)": {"en": "Disable CFG (Control Flow Guard)", "fr": "Désactiver CFG (Garde de flux de contrôle)", "tn": "Ytaffi CFG. Yna77i el overhead men kol appel de fonction. 1-3% gain fi DX11.", "es": "Desactivar CFG (Control Flow Guard)", "de": "CFG (Control Flow Guard) deaktivieren", "ar": "تعطيل CFG (حارس تدفق التحكم)"},
    "Disable Memory Compression": {"en": "Disable Memory Compression", "fr": "Désactiver la compression mémoire", "tn": "Ywakef compression el RAM. Y9allel el overhead taa3 CPU w latence.", "es": "Desactivar compresión de memoria", "de": "Speicherkomprimierung deaktivieren", "ar": "تعطيل ضغط الذاكرة"},
    "Disable Fault Tolerant Heap (FTH)": {"en": "Disable Fault Tolerant Heap (FTH)", "fr": "Désactiver le tas tolérant aux pannes (FTH)", "tn": "FTH yraqeb les crashs w y7ot mitigations eli tzid tbatti les jeux.", "es": "Desactivar FTH (Heap tolerante a fallos)", "de": "Fehlertoleranten Heap deaktivieren", "ar": "تعطيل FTH (كومة تحمل الأخطاء)"},
    "Disable UAC (User Account Control)": {"en": "Disable UAC (User Account Control)", "fr": "Désactiver le contrôle de compte utilisateur (UAC)", "tn": "Ytaffi UAC kamla. Yna77i la transition secure desktop. RISQUE 3ALI.", "es": "Desactivar UAC (Control de cuentas)", "de": "UAC (Benutzerkontensteuerung) deaktivieren", "ar": "تعطيل UAC (التحكم بحساب المستخدم)"},
    "Disable DEP (Data Execution Prevention)": {"en": "Disable DEP (Data Execution Prevention)", "fr": "Désactiver la prévention d'exécution des données (DEP)", "tn": "Ytaffi DEP. Yna77i les verifications memoire. Risque extreme.", "es": "Desactivar DEP (Prevención de ejecución de datos)", "de": "DEP (Datenausführungsverhinderung) deaktivieren", "ar": "تعطيل DEP (منع تنفيذ البيانات)"},
    "Disable ASLR (Address Space Layout Randomization)": {"en": "Disable ASLR (Address Space Layout Randomization)", "fr": "Désactiver ASLR (randomisation de l'espace d'adressage)", "tn": "Yforci el memoire t7ot fi adresses previsibles. Risque extreme lel securite.", "es": "Desactivar ASLR (Aleatorización del espacio de memoria)", "de": "ASLR deaktivieren", "ar": "تعطيل ASLR (عشوائية مخطط الذاكرة)"},
    "Disable System Restore": {"en": "Disable System Restore", "fr": "Désactiver la restauration du système", "tn": "Ytaffi la restauration systeme. Yfarregh el disque w yna77i les snapshots.", "es": "Desactivar Restaurar sistema", "de": "Systemwiederherstellung deaktivieren", "ar": "تعطيل استعادة النظام"},
    "Disable SEHOP (Exception Chain Validation)": {"en": "Disable SEHOP (Exception Chain Validation)", "fr": "Désactiver SEHOP (validation de chaîne d'exceptions)", "tn": "Ytaffi SEHOP. Yna77i verification securite 3la kol exception.", "es": "Desactivar SEHOP", "de": "SEHOP deaktivieren", "ar": "تعطيل SEHOP"},
    "Disable Prefetcher & Superfetch (Registry)": {"en": "Disable Prefetcher & Superfetch (Registry)", "fr": "Désactiver Prefetcher & Superfetch (registre)", "tn": "Ytaffi el prefetcher memoire fi kernel. Lazem lel SSD.", "es": "Desactivar Prefetcher y Superfetch (Registro)", "de": "Prefetcher & Superfetch deaktivieren", "ar": "تعطيل Prefetcher و Superfetch"},
    "Force Disable Fullscreen Optimizations (Global)": {"en": "Force Disable Fullscreen Optimizations (Global)", "fr": "Forcer la désactivation des optimisations plein écran", "tn": "Ymanea Windows men forcer borderless mode. Ysal7 el micro-stutters.", "es": "Forzar desactivar optimizaciones de pantalla completa", "de": "Vollbild-Optimierungen global deaktivieren", "ar": "فرض تعطيل تحسينات ملء الشاشة"},
    "Disable Monitor VSync Override (Legacy)": {"en": "Disable Monitor VSync Override (Legacy)", "fr": "Désactiver le remplacement VSync moniteur (ancien)", "tn": "Ytaffi el VSync override taa3 el moniteur. Parametre 9dim, ma ya3melch barcha 3al drivers jdoud.", "es": "Desactivar anulación VSync del monitor", "de": "Monitor-VSync-Override deaktivieren", "ar": "تعطيل تجاوز VSync للشاشة"},
    "Disable GPU Preemption": {"en": "Disable GPU Preemption", "fr": "Désactiver la préemption GPU", "tn": "WDDM ma y9ata3ch el GPU fi wesot el frame. Variance tan9os 20-40%.", "es": "Desactivar preempción de GPU", "de": "GPU-Preemption deaktivieren", "ar": "تعطيل استباق GPU"},
    "Force True Exclusive Fullscreen": {"en": "Force True Exclusive Fullscreen", "fr": "Forcer le vrai plein écran exclusif", "tn": "Ymanea Windows men ykhattef el jeu lel DWM composition. Ywaffar 1 frame latence.", "es": "Forzar pantalla completa exclusiva real", "de": "Echten exklusiven Vollbildmodus erzwingen", "ar": "فرض ملء الشاشة الحصري الحقيقي"},
    "Disable Game DVR & Game Bar": {"en": "Disable Game DVR & Game Bar", "fr": "Désactiver Game DVR & Game Bar", "tn": "Yna77i l'enregistrement GPU mel background w la barre de jeu. Ysabbeb stuttering 7atta kan mch actif.", "es": "Desactivar Game DVR y Game Bar", "de": "Game DVR & Game Bar deaktivieren", "ar": "تعطيل Game DVR و Game Bar"},
    "Enable HW Accelerated GPU Scheduling": {"en": "Enable HW Accelerated GPU Scheduling", "fr": "Activer l'ordonnancement GPU accéléré matériel", "tn": "El GPU ydabber VRAM wa7dou bla Windows. Y9allel latence 3la NVIDIA 10+ / AMD 5000+.", "es": "Activar planificación GPU acelerada por hardware", "de": "HW-beschleunigte GPU-Planung aktivieren", "ar": "تفعيل جدولة GPU المسرّعة"},
    "Increase GPU TDR Timeout to 60s": {"en": "Increase GPU TDR Timeout to 60s", "fr": "Augmenter le délai TDR GPU à 60s", "tn": "Ymanea les faux crashs 'driver ma yjawebch' w9t shader compilation.", "es": "Aumentar tiempo de espera TDR GPU a 60s", "de": "GPU TDR Timeout auf 60s erhöhen", "ar": "زيادة مهلة TDR لـ GPU إلى 60 ثانية"},
    "Force NVIDIA P-State P0 (Max Clocks)": {"en": "Force NVIDIA P-State P0 (Max Clocks)", "fr": "Forcer NVIDIA P-State P0 (fréquences max)", "tn": "Ytaffi el P-State dynamique. GPU yab9a 3la max frequences.", "es": "Forzar NVIDIA P-State P0 (frecuencias máx)", "de": "NVIDIA P-State P0 erzwingen (Max-Takt)", "ar": "فرض NVIDIA P-State P0 (أقصى تردد)"},
    "MMCSS Game Task Max Priority": {"en": "MMCSS Game Task Max Priority", "fr": "Priorité max tâche jeu MMCSS", "tn": "Priorite maximale MMCSS ki Windows y7oss 3la jeu.", "es": "Prioridad máx. tarea juego MMCSS", "de": "MMCSS Spielaufgabe Max-Priorität", "ar": "أقصى أولوية لمهمة MMCSS للألعاب"},
    "Disable Multi-Plane Overlay (MPO)": {"en": "Disable Multi-Plane Overlay (MPO)", "fr": "Désactiver le Multi-Plane Overlay (MPO)", "tn": "Ysal7 el stuttering w ecrans noirs b desactivation MPO.", "es": "Desactivar Multi-Plane Overlay (MPO)", "de": "Multi-Plane Overlay (MPO) deaktivieren", "ar": "تعطيل تراكب الطبقات المتعددة (MPO)"},
    "Disable Variable Refresh Rate (VRR) Globally": {"en": "Disable Variable Refresh Rate (VRR) Globally", "fr": "Désactiver le taux de rafraîchissement variable (VRR)", "tn": "Ytaffi VRR Windows eli y9adder yconfliqi m3a G-Sync/FreeSync.", "es": "Desactivar VRR (Tasa de refresco variable)", "de": "Variable Bildwiederholrate (VRR) global deaktivieren", "ar": "تعطيل معدل التحديث المتغير (VRR)"},
    "Disable GPU Energy Driver": {"en": "Disable GPU Energy Driver", "fr": "Désactiver le pilote d'énergie GPU", "tn": "Ytaffi el GPU Energy Driver eli y7awwel el GPU. Yetjawez kan ma mawjoudch.", "es": "Desactivar driver de energía GPU", "de": "GPU-Energietreiber deaktivieren", "ar": "تعطيل تعريف طاقة GPU"},
    "Disable Xbox Game Monitoring": {"en": "Disable Xbox Game Monitoring", "fr": "Désactiver la surveillance Xbox des jeux", "tn": "Ywakef Xbox Game Monitoring. Tna77at men Win10 2004+.", "es": "Desactivar monitoreo de juegos Xbox", "de": "Xbox Game Monitoring deaktivieren", "ar": "تعطيل مراقبة ألعاب Xbox"},
    "Disable Game Bar Presence Writer": {"en": "Disable Game Bar Presence Writer", "fr": "Désactiver l'écriture de présence Game Bar", "tn": "Ymanea Game Bar mel ecriture donnees de presence kol ma tlanci jeu.", "es": "Desactivar escritor de presencia Game Bar", "de": "Game Bar Presence Writer deaktivieren", "ar": "تعطيل كاتب حضور Game Bar"},
    "Disable Windows Ink Workspace": {"en": "Disable Windows Ink Workspace", "fr": "Désactiver l'espace Windows Ink", "tn": "Ytaffi Windows Ink. Mohemm lel FPS players bech yna77i traitement stylet/tablette.", "es": "Desactivar espacio Windows Ink", "de": "Windows Ink Workspace deaktivieren", "ar": "تعطيل مساحة Windows Ink"},
    "Disable DWM Ghosting / Composition (Legacy)": {"en": "Disable DWM Ghosting / Composition (Legacy)", "fr": "Désactiver le ghosting DWM / composition (ancien)", "tn": "Ytaffi animations DWM. HungAppTimeout yetgera b tweak 'delais d arret rapides'.", "es": "Desactivar DWM Ghosting / Composición", "de": "DWM Ghosting / Komposition deaktivieren", "ar": "تعطيل شبحية DWM / التركيب"},
    "Disable Dynamic Tick": {"en": "Disable Dynamic Tick", "fr": "Désactiver le tick dynamique", "tn": "Ymanea Windows men y9allel el minuteur systeme ki CPU farge. Frame pacing stable.", "es": "Desactivar tick dinámico", "de": "Dynamischen Tick deaktivieren", "ar": "تعطيل النبض الديناميكي"},
    "Force CPU TSC Timer (Remove HPET)": {"en": "Force CPU TSC Timer (Remove HPET)", "fr": "Forcer le minuteur TSC CPU (supprimer HPET)", "tn": "Yna77i les horloges plateforme mel BCD bech yerja3 lel TSC CPU, akther sar3a.", "es": "Forzar temporizador TSC CPU (eliminar HPET)", "de": "CPU TSC Timer erzwingen (HPET entfernen)", "ar": "فرض مؤقت TSC للمعالج (إزالة HPET)"},
    "Enable Global Timer Resolution Requests": {"en": "Enable Global Timer Resolution Requests", "fr": "Activer les requêtes de résolution globale du minuteur", "tn": "Win11 22H2+ kassar les requetes minuteur. Yerja3 el comportement el 9dim.", "es": "Activar solicitudes de resolución de temporizador global", "de": "Globale Timer-Auflösungsanfragen aktivieren", "ar": "تفعيل طلبات دقة المؤقت العالمية"},
    "Enhanced TSC Sync Policy (Multi-CCX AMD)": {"en": "Enhanced TSC Sync Policy (Multi-CCX AMD)", "fr": "Politique de synchro TSC améliorée (AMD multi-CCX)", "tn": "Synchronisation TSC akther serra bin chiplets 3la Ryzen 3000+. Ysal7 el derive taa3 minuteur.", "es": "Política de sincronización TSC mejorada (AMD Multi-CCX)", "de": "Erweiterte TSC-Sync-Richtlinie (Multi-CCX AMD)", "ar": "سياسة مزامنة TSC محسّنة (AMD Multi-CCX)"},
    "Set Boot Timeout to 0": {"en": "Set Boot Timeout to 0", "fr": "Définir le délai de démarrage à 0", "tn": "Yna77i el delai taa3 menu selection OS. Ywaffar 30 secondes kol demarrage.", "es": "Establecer tiempo de arranque a 0", "de": "Boot-Timeout auf 0 setzen", "ar": "تعيين مهلة الإقلاع إلى 0"},
    "Disable Nagle's Algorithm (All Interfaces)": {"en": "Disable Nagle's Algorithm (All Interfaces)", "fr": "Désactiver l'algorithme de Nagle (toutes les interfaces)", "tn": "Nagle yjmaa les paquets sghira w yzid 200ms latence. TcpNoDelay=1 yba3eth to7a.", "es": "Desactivar algoritmo de Nagle (todas las interfaces)", "de": "Nagles Algorithmus deaktivieren (alle Schnittstellen)", "ar": "تعطيل خوارزمية Nagle (جميع الواجهات)"},
    "Disable Network Throttling Index": {"en": "Disable Network Throttling Index", "fr": "Désactiver la limitation du réseau", "tn": "Windows y7odded el trafic reseau. 0xFFFFFFFF yna77i el limite.", "es": "Desactivar índice de limitación de red", "de": "Netzwerk-Drosselungsindex deaktivieren", "ar": "تعطيل مؤشر خنق الشبكة"},
    "Set SystemResponsiveness to 0%": {"en": "Set SystemResponsiveness to 0%", "fr": "Définir SystemResponsiveness à 0%", "tn": "Par defaut 20% CPU reserve. 0 y9allel lel ~10% lel taches de fond.", "es": "Establecer SystemResponsiveness a 0%", "de": "SystemResponsiveness auf 0% setzen", "ar": "تعيين استجابة النظام إلى 0%"},
    "Enable RSS, Disable Heuristics": {"en": "Enable RSS, Disable Heuristics", "fr": "Activer RSS & DCA, désactiver les heuristiques", "tn": "RSS ywazzea traitement NIC 3la les coeurs. Heuristiques yecraseou reglages.", "es": "Activar RSS y DCA, desactivar heurísticas", "de": "RSS & DCA aktivieren, Heuristiken deaktivieren", "ar": "تفعيل RSS ، تعطيل الاستدلال"},
    "Disable TCP Timestamps & ECN": {"en": "Disable TCP Timestamps & ECN", "fr": "Désactiver les horodatages TCP & ECN", "tn": "Timestamps tzid 12 octets kol paquet. ECN tzid traitement CPU. Ma ya3mlouch barcha lel gaming.", "es": "Desactivar marcas de tiempo TCP y ECN", "de": "TCP-Zeitstempel & ECN deaktivieren", "ar": "تعطيل طوابع TCP الزمنية و ECN"},
    "Enable TCP Fast Open": {"en": "Enable TCP Fast Open", "fr": "Activer TCP Fast Open", "tn": "Ysma7 b donnees fil paquet SYN bech connexion ta9oum asra3.", "es": "Activar TCP Fast Open", "de": "TCP Fast Open aktivieren", "ar": "تفعيل TCP Fast Open"},
    "Set TCP Congestion Control to CUBIC": {"en": "Set TCP Congestion Control to CUBIC", "fr": "Définir le contrôle de congestion TCP sur CUBIC", "tn": "Ybaddel el TCP congestion l CUBIC. Par defaut men Win10 1709+.", "es": "Establecer control de congestión TCP a CUBIC", "de": "TCP-Staukontrolle auf CUBIC setzen", "ar": "تعيين التحكم في ازدحام TCP إلى CUBIC"},
    "Disable IPv6 Tunneling (Teredo, ISATAP, 6to4)": {"en": "Disable IPv6 Tunneling (Teredo, ISATAP, 6to4)", "fr": "Désactiver le tunneling IPv6 (Teredo, ISATAP, 6to4)", "tn": "Ytaffi les technologies transition IPv6 eli ysondou el reseau.", "es": "Desactivar túneles IPv6 (Teredo, ISATAP, 6to4)", "de": "IPv6-Tunneling deaktivieren (Teredo, ISATAP, 6to4)", "ar": "تعطيل أنفاق IPv6 (Teredo, ISATAP, 6to4)"},
    "Disable WMM (Wi-Fi Multimedia) Power Save": {"en": "Disable WMM (Wi-Fi Multimedia) Power Save", "fr": "Désactiver l'économie WMM (Wi-Fi Multimédia)", "tn": "Ymanea el Wi-Fi adapter men mode economie bin el rafales. Mohemm lel ping stable.", "es": "Desactivar ahorro WMM (Wi-Fi Multimedia)", "de": "WMM (Wi-Fi Multimedia) Energiesparen deaktivieren", "ar": "تعطيل توفير طاقة WMM (وسائط Wi-Fi)"},
    "Disable Large Send Offload (LSO)": {"en": "Disable Large Send Offload (LSO)", "fr": "Désactiver le LSO (envoi de grands paquets)", "tn": "LSO yfarregh segmentation TCP lel NIC ama barcha drivers ma y7ottelhach behi.", "es": "Desactivar LSO (envío de paquetes grandes)", "de": "Large Send Offload (LSO) deaktivieren", "ar": "تعطيل LSO (تفريغ الإرسال الكبير)"},
    "Optimize TCP Port & Timeout Parameters": {"en": "Optimize TCP Port & Timeout Parameters", "fr": "Optimiser les paramètres de port & délai TCP", "tn": "MaxUserPort=65534, delai=30s. Ymanea l epuisement taa3 les ports.", "es": "Optimizar parámetros de puerto y tiempo TCP", "de": "TCP-Port- & Timeout-Parameter optimieren", "ar": "تحسين معاملات منفذ ومهلة TCP"},
    "Optimize DNS Cache (24h / 5s negative)": {"en": "Optimize DNS Cache (24h / 5s negative)", "fr": "Optimiser le cache DNS (24h / 5s négatif)", "tn": "Cache DNS valide 24h, y3awed les echecs ba3d 5s.", "es": "Optimizar caché DNS (24h / 5s negativo)", "de": "DNS-Cache optimieren (24h / 5s negativ)", "ar": "تحسين ذاكرة DNS المؤقتة"},
    "Increase SMB IRPStackSize & Buffer": {"en": "Increase SMB IRPStackSize & Buffer", "fr": "Augmenter IRPStackSize & tampon SMB", "tn": "Yzid pile IRP l 30 w buffer l 17424 lel partage fichiers asra3.", "es": "Aumentar IRPStackSize y búfer SMB", "de": "SMB IRPStackSize & Puffer erhöhen", "ar": "زيادة حجم IRPStackSize و تخزين SMB"},
    "Disable Energy Efficient Ethernet (EEE)": {"en": "Disable Energy Efficient Ethernet (EEE)", "fr": "Désactiver Ethernet éconergétique (EEE)", "tn": "EEE y7ot el NIC en veille bin el rafales. Reveil yzid 2-5ms. Mohemm lel ping.", "es": "Desactivar Ethernet eficiente en energía (EEE)", "de": "Energy Efficient Ethernet (EEE) deaktivieren", "ar": "تعطيل Ethernet الموفر للطاقة (EEE)"},
    "Disable IPv6 Completely": {"en": "Disable IPv6 Completely", "fr": "Désactiver complètement IPv6", "tn": "Ytaffi IPv6. Kan FAI wella jeu ma y7tajouhaech, yna77i barcha trafic reseau.", "es": "Desactivar IPv6 completamente", "de": "IPv6 vollständig deaktivieren", "ar": "تعطيل IPv6 بالكامل"},
    "Disable QoS Packet Scheduler": {"en": "Disable QoS Packet Scheduler", "fr": "Désactiver le planificateur de paquets QoS", "tn": "Limite QoS l zero. El mythe taa3 '20% bande passante reservee' faux.", "es": "Desactivar planificador de paquetes QoS", "de": "QoS-Paketplaner deaktivieren", "ar": "تعطيل جدولة حزم QoS"},
    "Disable Receive Segment Coalescing (RSC)": {"en": "Disable Receive Segment Coalescing (RSC)", "fr": "Désactiver la fusion de segments reçus (RSC)", "tn": "RSC yjmaa les paquets. Behi lel debit, khayeb lel latence.", "es": "Desactivar fusión de segmentos recibidos (RSC)", "de": "Receive Segment Coalescing (RSC) deaktivieren", "ar": "تعطيل دمج المقاطع المستلمة (RSC)"},
    "Disable NetBIOS over TCP/IP": {"en": "Disable NetBIOS over TCP/IP", "fr": "Désactiver NetBIOS sur TCP/IP", "tn": "Ytaffi les protocoles decouverte reseau local eli ywazzaou paquets.", "es": "Desactivar NetBIOS sobre TCP/IP", "de": "NetBIOS über TCP/IP deaktivieren", "ar": "تعطيل NetBIOS عبر TCP/IP"},
    "Disable LLMNR (Link-Local Multicast)": {"en": "Disable LLMNR (Link-Local Multicast)", "fr": "Désactiver LLMNR (multicast local)", "tn": "Ytaffi LLMNR, protocole resolution noms local eli ywalled trafic fadhel.", "es": "Desactivar LLMNR (Multicast local)", "de": "LLMNR (Link-Local Multicast) deaktivieren", "ar": "تعطيل LLMNR (البث المتعدد المحلي)"},
    "Disable Smart Name Resolution": {"en": "Disable Smart Name Resolution", "fr": "Désactiver la résolution de noms intelligente", "tn": "Ymanea Windows men yba3eth DNS queries lkol les adaptateurs fi nafes el wa9t.", "es": "Desactivar resolución inteligente de nombres", "de": "Smart Name Resolution deaktivieren", "ar": "تعطيل حل الأسماء الذكي"},
    "Activate Ultimate Performance Plan": {"en": "Activate Ultimate Performance Plan", "fr": "Activer le plan Performance Ultime", "tn": "Plan d alimentation makhfi eli yna77i kol les delais d economie d energie.", "es": "Activar plan Rendimiento Máximo", "de": "Ultimativen Leistungsplan aktivieren", "ar": "تفعيل خطة الأداء القصوى"},
    "Unpark All CPU Cores (100% Min)": {"en": "Unpark All CPU Cores (100% Min)", "fr": "Déparquer tous les cœurs CPU (100% min)", "tn": "7atta coeur ma yor9ad. Yna77i el saccades ki coeur yfi9 bel charge.", "es": "Desaparcar todos los núcleos CPU (100% mín)", "de": "Alle CPU-Kerne entparken (100% Min)", "ar": "إلغاء إيقاف جميع أنوية المعالج (100% كحد أدنى)"},
    "Disable Processor C-States (Idle Disable)": {"en": "Disable Processor C-States (Idle Disable)", "fr": "Désactiver les C-States processeur (pas de repos)", "tn": "Ymanea les coeurs men somneil C1/C3/C6. Kol etat yzid microsecondes latence.", "es": "Desactivar C-States del procesador", "de": "Prozessor C-States deaktivieren", "ar": "تعطيل حالات C للمعالج"},
    "CPU Min/Max State = 100%": {"en": "CPU Min/Max State = 100%", "fr": "État CPU min/max = 100%", "tn": "Yforci el processeur ykhdem 3la frequence maximale. Yna77i kol les delais.", "es": "Estado CPU mín/máx = 100%", "de": "CPU Min/Max Zustand = 100%", "ar": "حالة المعالج أدنى/أقصى = 100%"},
    "Aggressive Boost Mode + EPP = 0": {"en": "Aggressive Boost Mode + EPP = 0", "fr": "Mode Boost agressif + EPP = 0", "tn": "Boost agressif (frequence max to7a) w EPP 0 (performance pure).", "es": "Modo Boost agresivo + EPP = 0", "de": "Aggressiver Boost-Modus + EPP = 0", "ar": "وضع التعزيز العدواني + EPP = 0"},
    "Disable Power Throttling": {"en": "Disable Power Throttling", "fr": "Désactiver la limitation de puissance", "tn": "Windows 10+ y7added les applis background. Y9adder ysabbeb stuttering kan yclassifihom ghalet.", "es": "Desactivar limitación de potencia", "de": "Leistungsdrosselung deaktivieren", "ar": "تعطيل خنق الطاقة"},
    "Disable USB Selective Suspend": {"en": "Disable USB Selective Suspend", "fr": "Désactiver la suspension sélective USB", "tn": "Ymanea Windows men ytaffi les USB. Ysal7 les deconnexions souris/clavier.", "es": "Desactivar suspensión selectiva USB", "de": "USB Selective Suspend deaktivieren", "ar": "تعطيل التعليق الانتقائي لـ USB"},
    "Disable PCI Express ASPM": {"en": "Disable PCI Express ASPM", "fr": "Désactiver PCI Express ASPM", "tn": "ASPM yzid latence lel transitions PCIe. Ytaffi y7olli GPU/NVMe toujours actif.", "es": "Desactivar PCI Express ASPM", "de": "PCI Express ASPM deaktivieren", "ar": "تعطيل PCI Express ASPM"},
    "Disable Sleep & Display Timeout": {"en": "Disable Sleep & Display Timeout", "fr": "Désactiver la veille & le délai d'écran", "tn": "Ymanea el PC w l ecran men somneil automatique.", "es": "Desactivar suspensión y tiempo de pantalla", "de": "Schlaf- & Display-Timeout deaktivieren", "ar": "تعطيل مهلة السكون والشاشة"},
    "Disable Disk Sleep": {"en": "Disable Disk Sleep", "fr": "Désactiver la veille du disque", "tn": "Ymanea les disques men ywakfou. Yna77i el gel 3-5 secondes.", "es": "Desactivar suspensión de disco", "de": "Festplatten-Schlaf deaktivieren", "ar": "تعطيل سكون القرص"},
    "Disable Connected Standby (Modern Standby)": {"en": "Disable Connected Standby (Modern Standby)", "fr": "Désactiver la veille connectée (Modern Standby)", "tn": "Yforci S3 blasa men S0ix. Ymanea el PC men yfi9 fil sac.", "es": "Desactivar espera conectada (Modern Standby)", "de": "Connected Standby deaktivieren", "ar": "تعطيل الاستعداد المتصل"},
    "Disable Hibernation & Fast Startup": {"en": "Disable Hibernation & Fast Startup", "fr": "Désactiver l'hibernation & le démarrage rapide", "tn": "Yna77i hiberfil.sys (ywaffar Go) w yforci redemarrage propre.", "es": "Desactivar hibernación e inicio rápido", "de": "Ruhezustand & Schnellstart deaktivieren", "ar": "تعطيل الإسبات والبدء السريع"},
    "Enable MSI Mode on All PCI Devices": {"en": "Enable MSI Mode on All PCI Devices", "fr": "Activer le mode MSI sur tous les appareils PCI", "tn": "Ybaddel GPU, NIC, USB, Stockage, Audio l MSI. Y9allel barcha latence DPC. Attention: y9adder ysabbeb BSOD.", "es": "Activar modo MSI en todos los dispositivos PCI", "de": "MSI-Modus auf allen PCI-Geräten aktivieren", "ar": "تفعيل وضع MSI على جميع أجهزة PCI"},
    "Disable USB Controller Power Saving": {"en": "Disable USB Controller Power Saving", "fr": "Désactiver l'économie du contrôleur USB", "tn": "Ytaffi economie controleur USB. Ysal7 les pics 10ms taa3 souris w claviers.", "es": "Desactivar ahorro del controlador USB", "de": "USB-Controller Energiesparen deaktivieren", "ar": "تعطيل توفير طاقة وحدة تحكم USB"},
    "Set GPU MSI Priority to High": {"en": "Set GPU MSI Priority to High", "fr": "Définir la priorité MSI GPU sur Élevée", "tn": "Yforci MSI taa3 GPU tet3aleg b priorite 3alya.", "es": "Establecer prioridad MSI GPU en Alta", "de": "GPU MSI Priorität auf Hoch setzen", "ar": "تعيين أولوية MSI لـ GPU على عالية"},
    "Set NIC MSI Priority to High": {"en": "Set NIC MSI Priority to High", "fr": "Définir la priorité MSI carte réseau sur Élevée", "tn": "Yforci MSI taa3 carte reseau tet3aleg b priorite 3alya.", "es": "Establecer prioridad MSI NIC en Alta", "de": "NIC MSI Priorität auf Hoch setzen", "ar": "تعيين أولوية MSI لبطاقة الشبكة على عالية"},
    "Optimize Mouse & Keyboard Queue (Input Latency)": {"en": "Optimize Mouse & Keyboard Queue (Input Latency)", "fr": "Optimiser la file souris & clavier (latence d'entrée)", "tn": "Y9allel taille file d entree, y9allel chwaya latence.", "es": "Optimizar cola de ratón y teclado (latencia)", "de": "Maus- & Tastaturwarteschlange optimieren", "ar": "تحسين صفوف الماوس ولوحة المفاتيح"},
    "MarkC Mouse Fix (1:1 Raw Input)": {"en": "MarkC Mouse Fix (1:1 Raw Input)", "fr": "Fix souris MarkC (entrée brute 1:1)", "tn": "Fix souris MarkC 1:1. Vitesse w seuils 0. Zero acceleration lel gaming.", "es": "Fix ratón MarkC (entrada 1:1)", "de": "MarkC Mausfix (1:1 Roheingabe)", "ar": "إصلاح ماوس MarkC (إدخال خام 1:1)"},
    "Disable Sticky / Filter / Toggle Key Prompts": {"en": "Disable Sticky / Filter / Toggle Key Prompts", "fr": "Désactiver les invites touches rémanentes / filtres", "tn": "Ymanea el popup Shift-5x w9t el jeu. Ytaffi les raccourcis bla ma yna77i l accessibilite.", "es": "Desactivar teclas especiales / filtro / alternancia", "de": "Einrast-/Filter-/Umschalttasten deaktivieren", "ar": "تعطيل مطالبات المفاتيح اللاصقة / الفلتر"},
    "Reduce Menu & Hover Delays to 0": {"en": "Reduce Menu & Hover Delays to 0", "fr": "Réduire les délais menu & survol à 0", "tn": "Les menus w infobulles ybanoulk to7a blasa men 400ms.", "es": "Reducir retardos de menú y hover a 0", "de": "Menü- & Hover-Verzögerungen auf 0 reduzieren", "ar": "تقليل تأخير القوائم والتمرير إلى 0"},
    "Set Performance Visual Preferences (Comprehensive)": {"en": "Set Performance Visual Preferences (Comprehensive)", "fr": "Définir les préférences visuelles (performance)", "tn": "Bitmask performance. Ytaffi ombres curseur, animations menus w effets visuels.", "es": "Establecer preferencias visuales de rendimiento", "de": "Visuelle Leistungseinstellungen setzen", "ar": "تعيين تفضيلات الأداء المرئية"},
    "Increase Keyboard Repeat Rate": {"en": "Increase Keyboard Repeat Rate", "fr": "Augmenter le taux de répétition du clavier", "tn": "KeyboardDelay=0 w KeyboardSpeed=31. Maintenir touche tet7ott asra3 barcha.", "es": "Aumentar tasa de repetición del teclado", "de": "Tastatur-Wiederholrate erhöhen", "ar": "زيادة معدل تكرار لوحة المفاتيح"},
    "Disable All Windows Telemetry": {"en": "Disable All Windows Telemetry", "fr": "Désactiver toute la télémétrie Windows", "tn": "AllowTelemetry=0. Ywakef l envoi donnees diagnostic l Microsoft.", "es": "Desactivar toda la telemetría de Windows", "de": "Alle Windows-Telemetrie deaktivieren", "ar": "تعطيل جميع قياسات Windows"},
    "Disable Advertising ID & Tracking": {"en": "Disable Advertising ID & Tracking", "fr": "Désactiver l'identifiant publicitaire & le suivi", "tn": "Yna77i ID publicitaire, suivi applis w historique d activite.", "es": "Desactivar ID publicidad y rastreo", "de": "Werbe-ID & Tracking deaktivieren", "ar": "تعطيل معرّف الإعلانات والتتبع"},
    "Disable Location & Sensors": {"en": "Disable Location & Sensors", "fr": "Désactiver la localisation & les capteurs", "tn": "Ytaffi services localisation, Wi-Fi positioning w location scripting.", "es": "Desactivar ubicación y sensores", "de": "Standort & Sensoren deaktivieren", "ar": "تعطيل الموقع والمستشعرات"},
    "Disable Content Delivery & Suggestions": {"en": "Disable Content Delivery & Suggestions", "fr": "Désactiver la livraison de contenu & suggestions", "tn": "Ymanea Windows men yinstalli Candy Crush, pubs menu Demarrer w suggestions.", "es": "Desactivar entrega de contenido y sugerencias", "de": "Inhaltsbereitstellung & Vorschläge deaktivieren", "ar": "تعطيل توصيل المحتوى والاقتراحات"},
    "Disable Input Personalization & Speech": {"en": "Disable Input Personalization & Speech", "fr": "Désactiver la personnalisation de saisie & la parole", "tn": "Ywakef jma3 donnees frappe, ecriture w enregistrements vocaux.", "es": "Desactivar personalización de entrada y voz", "de": "Eingabepersonalisierung & Sprache deaktivieren", "ar": "تعطيل تخصيص الإدخال والكلام"},
    "Disable Feedback & Tailored Experiences": {"en": "Disable Feedback & Tailored Experiences", "fr": "Désactiver les commentaires & expériences personnalisées", "tn": "Ma 3adch popups 'Evaluez Windows'. Ywakef l utilisation donnees taa3ek lel pubs.", "es": "Desactivar feedback y experiencias personalizadas", "de": "Feedback & maßgeschneiderte Erlebnisse deaktivieren", "ar": "تعطيل الملاحظات والتجارب المخصصة"},
    "Disable P2P Update Delivery & Clipboard Sync": {"en": "Disable P2P Update Delivery & Clipboard Sync", "fr": "Désactiver la livraison P2P & synchro presse-papiers", "tn": "Ymanea Windows men yba3eth mises a jour l PC inconnus. Ytaffi synchro presse-papiers.", "es": "Desactivar entrega P2P y sincro portapapeles", "de": "P2P-Update-Lieferung & Zwischenablage-Sync deaktivieren", "ar": "تعطيل توصيل P2P ومزامنة الحافظة"},
    "Disable Edge Telemetry": {"en": "Disable Edge Telemetry", "fr": "Désactiver la télémétrie Edge", "tn": "Ytaffi jma3 donnees Edge men background.", "es": "Desactivar telemetría de Edge", "de": "Edge-Telemetrie deaktivieren", "ar": "تعطيل قياسات Edge"},
    "Disable Office Telemetry": {"en": "Disable Office Telemetry", "fr": "Désactiver la télémétrie Office", "tn": "Ytaffi jma3 donnees taa3 Microsoft Office.", "es": "Desactivar telemetría de Office", "de": "Office-Telemetrie deaktivieren", "ar": "تعطيل قياسات Office"},
    "Disable Visual Studio Telemetry": {"en": "Disable Visual Studio Telemetry", "fr": "Désactiver la télémétrie Visual Studio", "tn": "Ytaffi programme d amelioration experience Visual Studio.", "es": "Desactivar telemetría de Visual Studio", "de": "Visual Studio Telemetrie deaktivieren", "ar": "تعطيل قياسات Visual Studio"},
    "Disable NVIDIA Telemetry": {"en": "Disable NVIDIA Telemetry", "fr": "Désactiver la télémétrie NVIDIA", "tn": "Ytaffi services telemetrie NVIDIA. Yetjawez kan NVIDIA mch installe.", "es": "Desactivar telemetría de NVIDIA", "de": "NVIDIA-Telemetrie deaktivieren", "ar": "تعطيل قياسات NVIDIA"},
    "Disable Windows Defender SmartScreen": {"en": "Disable Windows Defender SmartScreen", "fr": "Désactiver Windows Defender SmartScreen", "tn": "Ymanea Windows men yba3eth URL w hachages fichiers l Microsoft.", "es": "Desactivar Windows Defender SmartScreen", "de": "Windows Defender SmartScreen deaktivieren", "ar": "تعطيل Windows Defender SmartScreen"},
    "Disable Error Reporting (WER)": {"en": "Disable Error Reporting (WER)", "fr": "Désactiver le rapport d'erreurs (WER)", "tn": "Ywakef generation dumps crash w l envoi l Microsoft. Ywaffar disque w CPU.", "es": "Desactivar informes de errores (WER)", "de": "Fehlerberichterstattung (WER) deaktivieren", "ar": "تعطيل تقارير الأخطاء (WER)"},
    "Disable Inventory Collector": {"en": "Disable Inventory Collector", "fr": "Désactiver le collecteur d'inventaire", "tn": "Ymanea Windows men yscanni disque bech y3amel inventaire applications.", "es": "Desactivar recolector de inventario", "de": "Inventarsammler deaktivieren", "ar": "تعطيل جامع المخزون"},
    "Disable DiagTrack & WAP Push": {"en": "Disable DiagTrack & WAP Push", "fr": "Désactiver DiagTrack & WAP Push", "tn": "Pipeline principal telemetrie. Drain CPU + reseau elimine.", "es": "Desactivar DiagTrack y WAP Push", "de": "DiagTrack & WAP Push deaktivieren", "ar": "تعطيل DiagTrack و WAP Push"},
    "Disable SysMain / Superfetch": {"en": "Disable SysMain / Superfetch", "fr": "Désactiver SysMain / Superfetch", "tn": "Ychargi applis fil RAM. I/O disque 3la HDD, gaspillage RAM 3la SSD.", "es": "Desactivar SysMain / Superfetch", "de": "SysMain / Superfetch deaktivieren", "ar": "تعطيل SysMain / Superfetch"},
    "Disable WER, Diagnostics & Link Tracking": {"en": "Disable WER, Diagnostics & Link Tracking", "fr": "Désactiver WER, diagnostics & suivi de liens", "tn": "WER, diagnostics w suivi liens - services bla fayda lel utilisateur.", "es": "Desactivar WER, diagnósticos y seguimiento", "de": "WER, Diagnose & Link-Tracking deaktivieren", "ar": "تعطيل WER والتشخيصات وتتبع الروابط"},
    "Disable Bloat Services (Fax, Maps, Retail...)": {"en": "Disable Bloat Services (Fax, Maps, Retail...)", "fr": "Désactiver les services inutiles (Fax, Cartes, Démo...)", "tn": "Ytaffi Fax, cartes, demo retail, AllJoyn, Windows Insider.", "es": "Desactivar servicios innecesarios (Fax, Mapas...)", "de": "Bloatware-Dienste deaktivieren (Fax, Karten...)", "ar": "تعطيل الخدمات غير الضرورية (فاكس، خرائط...)"},
    "Disable Xbox Services (4 services)": {"en": "Disable Xbox Services (4 services)", "fr": "Désactiver les services Xbox (4 services)", "tn": "Xbox Live Auth, sauvegarde jeu, gestion accessoires. Taffihom kan ma testa3melch Xbox.", "es": "Desactivar servicios Xbox (4 servicios)", "de": "Xbox-Dienste deaktivieren (4 Dienste)", "ar": "تعطيل خدمات Xbox (4 خدمات)"},
    "Disable Telemetry Scheduled Tasks": {"en": "Disable Telemetry Scheduled Tasks", "fr": "Désactiver les tâches planifiées de télémétrie", "tn": "Compatibility Appraiser (100% disque 15-30 min), ProgramDataUpdater, taches CEIP.", "es": "Desactivar tareas programadas de telemetría", "de": "Telemetrie-Aufgaben deaktivieren", "ar": "تعطيل مهام القياس المجدولة"},
    "Disable Print Spooler": {"en": "Disable Print Spooler", "fr": "Désactiver le spouleur d'impression", "tn": "Ytaffi service impression. 7assilha kan ma timprimich ABADAN.", "es": "Desactivar cola de impresión", "de": "Druckerspooler deaktivieren", "ar": "تعطيل خدمة الطباعة"},
    "Disable Windows Search Service": {"en": "Disable Windows Search Service", "fr": "Désactiver le service de recherche Windows", "tn": "Ytaffi l indexeur fichiers. Recherche tkheddem ama abta. Ywaffar barcha I/O.", "es": "Desactivar servicio de búsqueda de Windows", "de": "Windows-Suchdienst deaktivieren", "ar": "تعطيل خدمة بحث Windows"},
    "Disable Windows Update Service": {"en": "Disable Windows Update Service", "fr": "Désactiver le service Windows Update", "tn": "Ytaffi Windows Update kamla. RISQUE 3ALI. Ma 3adch correctifs securite.", "es": "Desactivar servicio Windows Update", "de": "Windows Update-Dienst deaktivieren", "ar": "تعطيل خدمة Windows Update"},
    "Disable Background Intelligent Transfer (BITS)": {"en": "Disable Background Intelligent Transfer (BITS)", "fr": "Désactiver le transfert intelligent (BITS)", "tn": "Ytaffi BITS, eli yesta3mlou Windows Update w applis okhrin lel telechargement background.", "es": "Desactivar transferencia inteligente (BITS)", "de": "BITS deaktivieren", "ar": "تعطيل النقل الذكي في الخلفية (BITS)"},
    "Disable Security Center Service": {"en": "Disable Security Center Service", "fr": "Désactiver le service Centre de sécurité", "tn": "Ytaffi Centre de securite Windows. Ywakef notifications antivirus w pare-feu.", "es": "Desactivar servicio Centro de seguridad", "de": "Sicherheitscenter-Dienst deaktivieren", "ar": "تعطيل خدمة مركز الأمان"},
    "Deep Temp / Cache / Log Cleanup": {"en": "Deep Temp / Cache / Log Cleanup", "fr": "Nettoyage approfondi temp / cache / logs", "tn": "Yna77i temp, prefetch, caches, rapports erreur, crash dumps, logs CBS. Yrecupere Go.", "es": "Limpieza profunda temp / caché / logs", "de": "Tiefenbereinigung Temp / Cache / Log", "ar": "تنظيف عميق للملفات المؤقتة / التخزين / السجلات"},
    "Flush DNS & ARP Cache": {"en": "Flush DNS & ARP Cache", "fr": "Vider le cache DNS & ARP", "tn": "Yna77i les mappages DNS w ARP el 9doum. Ysal7 barcha problemes connexion.", "es": "Vaciar caché DNS y ARP", "de": "DNS- & ARP-Cache leeren", "ar": "مسح ذاكرة DNS و ARP"},
    "Clean Browser Caches (Chrome, Edge, Firefox)": {"en": "Clean Browser Caches (Chrome, Edge, Firefox)", "fr": "Nettoyer les caches navigateur (Chrome, Edge, Firefox)", "tn": "Yna77i donnees web en cache. MA yna77ich mots de passe, favoris wella historique.", "es": "Limpiar cachés de navegadores (Chrome, Edge, Firefox)", "de": "Browser-Caches bereinigen (Chrome, Edge, Firefox)", "ar": "تنظيف ذاكرة المتصفحات (Chrome, Edge, Firefox)"},
    "NTFS Optimizations (Last Access, 8.3, Memory)": {"en": "NTFS Optimizations (Last Access, 8.3, Memory)", "fr": "Optimisations NTFS (dernier accès, 8.3, mémoire)", "tn": "Ytaffi horodatages acces, noms 8.3 DOS w yzid pool NTFS.", "es": "Optimizaciones NTFS (último acceso, 8.3, memoria)", "de": "NTFS-Optimierungen (Letzter Zugriff, 8.3, Speicher)", "ar": "تحسينات NTFS (آخر وصول، 8.3، الذاكرة)"},
    "Clear Windows Update Cache (SoftwareDistribution)": {"en": "Clear Windows Update Cache (SoftwareDistribution)", "fr": "Vider le cache Windows Update (SoftwareDistribution)", "tn": "Yna77i fichiers Windows Update. Ysal7 mises a jour bloquees w yfarregh espace.", "es": "Vaciar caché Windows Update (SoftwareDistribution)", "de": "Windows Update Cache leeren", "ar": "مسح ذاكرة Windows Update"},
    "Clear Event Viewer Logs": {"en": "Clear Event Viewer Logs", "fr": "Vider les journaux de l'observateur d'événements", "tn": "Yna77i kol les journaux evenements. Behi lel depart jdid.", "es": "Vaciar registros del visor de eventos", "de": "Ereignisanzeige-Protokolle löschen", "ar": "مسح سجلات عارض الأحداث"},
    "Disable Windows Error Reporting (WER) Folders": {"en": "Disable Windows Error Reporting (WER) Folders", "fr": "Désactiver les dossiers de rapport d'erreurs (WER)", "tn": "Ymanea WER men yba3eth donnees diagnostic supplementaires w ytaffi la file d attente.", "es": "Desactivar carpetas WER", "de": "WER-Ordner deaktivieren", "ar": "تعطيل مجلدات تقارير أخطاء Windows"},
    "Disable Delivery Optimization Cache": {"en": "Disable Delivery Optimization Cache", "fr": "Désactiver le cache d'optimisation de livraison", "tn": "Ymanea Windows men cache mises a jour lel partage. Yfarregh espace disque.", "es": "Desactivar caché de optimización de entrega", "de": "Übermittlungsoptimierungs-Cache deaktivieren", "ar": "تعطيل ذاكرة تحسين التسليم"},
    "Faster Shutdown Timeouts": {"en": "Faster Shutdown Timeouts", "fr": "Délais d'arrêt plus rapides", "tn": "WaitToKillService=2s, HungApp=1s. Arret/redemarrage asra3 barcha.", "es": "Tiempos de apagado más rápidos", "de": "Schnellere Shutdown-Timeouts", "ar": "مهل إيقاف أسرع"},
    "Remove Startup Program Delay": {"en": "Remove Startup Program Delay", "fr": "Supprimer le délai des programmes au démarrage", "tn": "Windows yre7tardi programmes demarrage ~10 secondes. Yna77i ce delai.", "es": "Eliminar retardo de programas al inicio", "de": "Startprogramm-Verzögerung entfernen", "ar": "إزالة تأخير برامج بدء التشغيل"},
    "Disable Cortana & Web Search in Start": {"en": "Disable Cortana & Web Search in Start", "fr": "Désactiver Cortana & la recherche web dans Démarrer", "tn": "Ytaffi Cortana w ymanea resultats Bing fi recherche menu Demarrer.", "es": "Desactivar Cortana y búsqueda web en Inicio", "de": "Cortana & Websuche im Start deaktivieren", "ar": "تعطيل Cortana والبحث على الويب"},
    "Taskbar Cleanup (People, Chat, Widgets...)": {"en": "Taskbar Cleanup (People, Chat, Widgets...)", "fr": "Nettoyage barre des tâches (Contacts, Chat, Widgets...)", "tn": "Ykhabi Contacts, Chat, Vue taches, Actualites/Widgets, Ink. Recherche icone bark.", "es": "Limpieza de barra de tareas (Contactos, Chat, Widgets)", "de": "Taskleiste bereinigen (Kontakte, Chat, Widgets)", "ar": "تنظيف شريط المهام (جهات اتصال، دردشة، أدوات)"},
    "Show File Extensions & Hidden Files": {"en": "Show File Extensions & Hidden Files", "fr": "Afficher les extensions & fichiers cachés", "tn": "Mohemm lel securite: chouf el extension el 79i9iya. Ybayyen fichiers caches.", "es": "Mostrar extensiones y archivos ocultos", "de": "Dateierweiterungen & versteckte Dateien anzeigen", "ar": "إظهار امتدادات الملفات والملفات المخفية"},
    "Disable Visual Animations & Transparency": {"en": "Disable Visual Animations & Transparency", "fr": "Désactiver les animations visuelles & la transparence", "tn": "Yna77i animations, flou transparence. Ykhalli ClearType. Economies GPU/CPU.", "es": "Desactivar animaciones y transparencia", "de": "Visuelle Animationen & Transparenz deaktivieren", "ar": "تعطيل الرسوم المتحركة والشفافية"},
    "Restore Classic Right-Click Menu (Win 11)": {"en": "Restore Classic Right-Click Menu (Win 11)", "fr": "Restaurer le menu clic droit classique (Win 11)", "tn": "Yrja3a menu clic droit kamla blasa men el tronque. Ma ya3melch 7aja 3la Win 10.", "es": "Restaurar menú clic derecho clásico (Win 11)", "de": "Klassisches Rechtsklick-Menü wiederherstellen (Win 11)", "ar": "استعادة قائمة النقر اليمني الكلاسيكية (Win 11)"},
    "Disable AutoPlay & Remote Assistance": {"en": "Disable AutoPlay & Remote Assistance", "fr": "Désactiver la lecture automatique & l'assistance à distance", "tn": "Ywakef l execution auto ki t7ot media. Ytaffi l assistance a distance.", "es": "Desactivar reproducción automática y asistencia remota", "de": "AutoPlay & Remoteunterstützung deaktivieren", "ar": "تعطيل التشغيل التلقائي والمساعدة عن بُعد"},
    "Disable Action Center / Notifications": {"en": "Disable Action Center / Notifications", "fr": "Désactiver le centre de notifications", "tn": "Ytaffi Centre d action w kol les notifications. Concentration pure.", "es": "Desactivar Centro de acciones / Notificaciones", "de": "Info-Center / Benachrichtigungen deaktivieren", "ar": "تعطيل مركز الإجراءات / الإشعارات"},
    "Disable Lock Screen": {"en": "Disable Lock Screen", "fr": "Désactiver l'écran de verrouillage", "tn": "Yfout to7a lel invite mot de passe/PIN. Lazem Windows Pro wella Enterprise.", "es": "Desactivar pantalla de bloqueo", "de": "Sperrbildschirm deaktivieren", "ar": "تعطيل شاشة القفل"},
    "Disable Aero Shake & Snap Assist": {"en": "Disable Aero Shake & Snap Assist", "fr": "Désactiver Aero Shake & Snap Assist", "tn": "Ymanea les fenetres men minimiser ki thezzhem w ywakef suggestions snap.", "es": "Desactivar Aero Shake y Snap Assist", "de": "Aero Shake & Snap Assist deaktivieren", "ar": "تعطيل Aero Shake و Snap Assist"},
    "Disable Windows Defender (Requires Safe Mode/TrustedInstaller)": {"en": "Disable Windows Defender (Requires Safe Mode/TrustedInstaller)", "fr": "Désactiver Windows Defender (nécessite le mode sans échec)", "tn": "Y7awel ytaffi Windows Defender. Windows moderne y7ami ces cles barcha.", "es": "Desactivar Windows Defender (requiere modo seguro)", "de": "Windows Defender deaktivieren (Abgesicherter Modus erforderlich)", "ar": "تعطيل Windows Defender (يتطلب الوضع الآمن)"},
    "Disable Kernel Mitigations (KVA Shadow)": {"en": "Disable Kernel Mitigations (KVA Shadow)", "fr": "Désactiver les mitigations du noyau (KVA Shadow)", "tn": "Ytaffi protections Meltdown/Spectre (KVA Shadow). 7aja risquée.", "es": "Desactivar mitigaciones del kernel (KVA Shadow)", "de": "Kernel-Mitigationen deaktivieren (KVA Shadow)", "ar": "تعطيل حماية النواة (KVA Shadow)"},
    "Increase System Working Set (Kernel Pool)": {"en": "Increase System Working Set (Kernel Pool)", "fr": "Augmenter l'ensemble de travail système", "tn": "Yzid fi system working set. Y5alli Windows ykhalli akther fi RAM.", "es": "Aumentar conjunto de trabajo del sistema", "de": "System Working Set erhöhen", "ar": "زيادة مجموعة العمل للنظام"},
    "Large System Cache (Server-Style Memory)": {"en": "Large System Cache (Server-Style Memory)", "fr": "Grand cache système (mode serveur)", "tn": "Y7ot large system cache kima serveur. Yam7i fil RAM.", "es": "Caché de sistema grande (estilo servidor)", "de": "Großer Systemcache (Server-Stil)", "ar": "ذاكرة تخزين كبيرة (نمط الخادم)"},
    "Disable Speculative Execution Side-Channel (SSBD)": {"en": "Disable Speculative Execution Side-Channel (SSBD)", "fr": "Désactiver le canal latéral d'exécution spéculative (SSBD)", "tn": "Ytaffi protection SSBD. Y7assin performances ama risque securite.", "es": "Desactivar canal lateral de ejecución especulativa (SSBD)", "de": "Spekulative Ausführung Seitenkanal deaktivieren (SSBD)", "ar": "تعطيل قناة التنفيذ التخميني (SSBD)"},
    "Disable Last Access Timestamp (Global)": {"en": "Disable Last Access Timestamp (Global)", "fr": "Désactiver l'horodatage du dernier accès", "tn": "Ytaffi last access timestamp globally b fsutil.", "es": "Desactivar marca de tiempo de último acceso", "de": "Letzten Zugriffszeitstempel deaktivieren", "ar": "تعطيل طابع وقت آخر وصول"},
    "Enable Long Paths (Win32)": {"en": "Enable Long Paths (Win32)", "fr": "Activer les chemins longs (Win32)", "tn": "Y7ot long paths Win32. Yzid men 260 caracteres lel chemins.", "es": "Habilitar rutas largas (Win32)", "de": "Lange Pfade aktivieren (Win32)", "ar": "تمكين المسارات الطويلة (Win32)"},
    "Disable 8.3 Short Name Creation": {"en": "Disable 8.3 Short Name Creation", "fr": "Désactiver la création de noms courts 8.3", "tn": "Ytaffi 8.3 short names. Y7assin performances NTFS.", "es": "Desactivar creación de nombres cortos 8.3", "de": "8.3-Kurznamen deaktivieren", "ar": "تعطيل إنشاء الأسماء القصيرة 8.3"},
    "Force DirectX 12 Shader Cache to RAM": {"en": "Force DirectX 12 Shader Cache to RAM", "fr": "Forcer le cache de shaders DX12 en RAM", "tn": "Yforci DX12 shader cache lel RAM au lieu de SSD.", "es": "Forzar caché de shaders DX12 a RAM", "de": "DirectX 12 Shader-Cache in RAM erzwingen", "ar": "فرض ذاكرة تخزين شيدر DX12 في RAM"},
    "Disable NVIDIA Shader Disk Cache Limit": {"en": "Disable NVIDIA Shader Disk Cache Limit", "fr": "Désactiver la limite du cache de shaders NVIDIA", "tn": "Yzid NVIDIA shader cache limit. Y7assin chargement jeux.", "es": "Desactivar límite de caché de shaders NVIDIA", "de": "NVIDIA Shader-Cache-Limit deaktivieren", "ar": "تعطيل حد ذاكرة شيدر NVIDIA"},
    "Disable Flip Queue Size (Pre-Rendered Frames = 1)": {"en": "Disable Flip Queue Size (Pre-Rendered Frames = 1)", "fr": "Désactiver la file de retournement (images pré-rendues = 1)", "tn": "Y7ot pre-rendered frames = 1. Ynakess latence input lel jeux.", "es": "Desactivar cola de volteo (fotogramas pre-renderizados = 1)", "de": "Flip-Queue deaktivieren (vorgerenderte Frames = 1)", "ar": "تعطيل قائمة الانتظار (إطارات مسبقة = 1)"},
    "Disable NVIDIA Telemetry & Container Processes": {"en": "Disable NVIDIA Telemetry & Container Processes", "fr": "Désactiver la télémétrie et conteneurs NVIDIA", "tn": "Ytaffi NVIDIA telemetry w container processes.", "es": "Desactivar telemetría y contenedores NVIDIA", "de": "NVIDIA-Telemetrie & Container deaktivieren", "ar": "تعطيل تتبع وعمليات حاوية NVIDIA"},
    "Disable Network Throttling Index": {"en": "Disable Network Throttling Index", "fr": "Désactiver le throttling réseau", "tn": "Yzid network throttling yfout. Y5alli NIC full speed.", "es": "Desactivar índice de limitación de red", "de": "Netzwerk-Throttling deaktivieren", "ar": "تعطيل تقييد سرعة الشبكة"},
    "Disable WPAD (Web Proxy Auto-Discovery)": {"en": "Disable WPAD (Web Proxy Auto-Discovery)", "fr": "Désactiver WPAD (découverte auto de proxy)", "tn": "Ytaffi WPAD. Risque MITM lel reseaux locaux.", "es": "Desactivar WPAD (descubrimiento automático de proxy)", "de": "WPAD deaktivieren (automatische Proxy-Erkennung)", "ar": "تعطيل WPAD (اكتشاف الوكيل التلقائي)"},
    "Disable ECN Capability": {"en": "Disable ECN Capability", "fr": "Désactiver la capacité ECN", "tn": "Ytaffi ECN. Ba3dh routeurs ybloquiw paquets ECN.", "es": "Desactivar capacidad ECN", "de": "ECN-Fähigkeit deaktivieren", "ar": "تعطيل إمكانية ECN"},
    "Disable Timer Coalescing": {"en": "Disable Timer Coalescing", "fr": "Désactiver la coalescence des timers", "tn": "Ymanea Windows men yjmea timer interrupts. Ynakess jitter.", "es": "Desactivar coalescencia de temporizadores", "de": "Timer-Koaleszenz deaktivieren", "ar": "تعطيل دمج المؤقتات"},
    "MMCSS Gaming Priority (SystemResponsiveness=0)": {"en": "MMCSS Gaming Priority (SystemResponsiveness=0)", "fr": "Priorité gaming MMCSS (SystemResponsiveness=0)", "tn": "Y7ot MMCSS gaming priority. 0% CPU lel background tasks.", "es": "Prioridad gaming MMCSS (SystemResponsiveness=0)", "de": "MMCSS Gaming-Priorität (SystemResponsiveness=0)", "ar": "أولوية الألعاب MMCSS (استجابة النظام=0)"},
    "Set Processor Performance Check Interval (5ms)": {"en": "Set Processor Performance Check Interval (5ms)", "fr": "Régler l'intervalle de vérification des performances (5ms)", "tn": "Ynakess check interval lel CPU frequency men 15ms lel 5ms.", "es": "Establecer intervalo de verificación de rendimiento (5ms)", "de": "Prozessor-Leistungsprüfintervall setzen (5ms)", "ar": "تعيين فاصل فحص أداء المعالج (5 مللي ثانية)"},
    "Disable Idle Promote / Demote Thresholds": {"en": "Disable Idle Promote / Demote Thresholds", "fr": "Désactiver les seuils de promotion/rétrogradation au repos", "tn": "Y7ot idle demote=100% w promote=0%. Cores ma ybadlouch P-states.", "es": "Desactivar umbrales de promoción/degradación en inactividad", "de": "Idle-Promote/Demote-Schwellenwerte deaktivieren", "ar": "تعطيل حدود الترقية/التخفيض في الخمول"},
    "Disable Latency-Sensitive Core Parking": {"en": "Disable Latency-Sensitive Core Parking", "fr": "Désactiver le parking de cœurs sensible à la latence", "tn": "Ynahi latency hints mel core parking algorithm.", "es": "Desactivar estacionamiento de núcleos sensible a latencia", "de": "Latenz-sensitives Core-Parking deaktivieren", "ar": "تعطيل إيقاف الأنوية الحساسة للتأخير"},
    "Pin GPU Interrupts to CPU 0 (Affinity Lock)": {"en": "Pin GPU Interrupts to CPU 0 (Affinity Lock)", "fr": "Épingler les interruptions GPU sur CPU 0", "tn": "Yforci GPU interrupts lel core 0. Ynakess frame time variance.", "es": "Fijar interrupciones GPU a CPU 0", "de": "GPU-Interrupts auf CPU 0 pinnen", "ar": "تثبيت مقاطعات GPU على المعالج 0"},
    "Disable NIC Interrupt Moderation": {"en": "Disable NIC Interrupt Moderation", "fr": "Désactiver la modération d'interruptions NIC", "tn": "Ytaffi interrupt moderation lel NIC. Ynakess latence reseau.", "es": "Desactivar moderación de interrupciones NIC", "de": "NIC-Interrupt-Moderation deaktivieren", "ar": "تعطيل تعديل مقاطعات بطاقة الشبكة"},
    "Disable Touch Input & Visual Feedback": {"en": "Disable Touch Input & Visual Feedback", "fr": "Désactiver l'entrée tactile et le retour visuel", "tn": "Ytaffi touch feedback w gestures. Ynakess input overhead.", "es": "Desactivar entrada táctil y retroalimentación visual", "de": "Touch-Eingabe & visuelles Feedback deaktivieren", "ar": "تعطيل الإدخال باللمس والتغذية الراجعة البصرية"},
    "Disable Pen & Ink Input Service": {"en": "Disable Pen & Ink Input Service", "fr": "Désactiver le service d'entrée stylet et encre", "tn": "Ytaffi TabletInputService. Ywaffir RAM w CPU.", "es": "Desactivar servicio de entrada de lápiz y tinta", "de": "Stift- & Tinteneingabedienst deaktivieren", "ar": "تعطيل خدمة إدخال القلم والحبر"},
    "Disable Handwriting Data Sharing": {"en": "Disable Handwriting Data Sharing", "fr": "Désactiver le partage de données d'écriture", "tn": "Ymanea Windows men yb3ath handwriting data lel Microsoft.", "es": "Desactivar compartir datos de escritura a mano", "de": "Handschrift-Datenfreigabe deaktivieren", "ar": "تعطيل مشاركة بيانات الكتابة اليدوية"},
    "Disable KMS Client Online AVS Validation": {"en": "Disable KMS Client Online AVS Validation", "fr": "Désactiver la validation AVS en ligne du client KMS", "tn": "Ymanea Windows men y7ott licence ping lel Microsoft.", "es": "Desactivar validación AVS en línea del cliente KMS", "de": "KMS-Client Online AVS-Validierung deaktivieren", "ar": "تعطيل التحقق من ترخيص KMS عبر الإنترنت"},
    "Disable Wi-Fi Sense & Hotspot 2.0": {"en": "Disable Wi-Fi Sense & Hotspot 2.0", "fr": "Désactiver Wi-Fi Sense et Hotspot 2.0", "tn": "Ytaffi Wi-Fi Sense w Hotspot 2.0. Privacy w securite.", "es": "Desactivar Wi-Fi Sense y Hotspot 2.0", "de": "Wi-Fi Sense & Hotspot 2.0 deaktivieren", "ar": "تعطيل Wi-Fi Sense و Hotspot 2.0"},
    "Disable Windows Biometric Service": {"en": "Disable Windows Biometric Service", "fr": "Désactiver le service biométrique Windows", "tn": "Ytaffi service biometrique. Ywaffir resources bla fingerprint/face.", "es": "Desactivar servicio biométrico de Windows", "de": "Windows Biometrie-Dienst deaktivieren", "ar": "تعطيل خدمة القياسات الحيوية"},
    "Disable Connected Devices Platform Service": {"en": "Disable Connected Devices Platform Service", "fr": "Désactiver le service de plateforme d'appareils connectés", "tn": "Ytaffi cross-device sync services. Ywaffir CPU w reseau.", "es": "Desactivar servicio de plataforma de dispositivos conectados", "de": "Verbundene-Geräte-Plattformdienst deaktivieren", "ar": "تعطيل خدمة منصة الأجهزة المتصلة"},
    "Disable Phone Link Service": {"en": "Disable Phone Link Service", "fr": "Désactiver le service Phone Link", "tn": "Ytaffi Phone Link service. Ywaffir CPU w memoire.", "es": "Desactivar servicio Phone Link", "de": "Phone Link-Dienst deaktivieren", "ar": "تعطيل خدمة ربط الهاتف"},
    "Clear Font Cache": {"en": "Clear Font Cache", "fr": "Vider le cache de polices", "tn": "Ynakki font cache. Ysalli7 texte garbled w polices manquantes.", "es": "Limpiar caché de fuentes", "de": "Schriftarten-Cache leeren", "ar": "مسح ذاكرة الخطوط"},
    "Reset Winsock & TCP/IP Stack": {"en": "Reset Winsock & TCP/IP Stack", "fr": "Réinitialiser Winsock et pile TCP/IP", "tn": "Nuclear network reset. Lazem reboot ba3dha.", "es": "Restablecer Winsock y pila TCP/IP", "de": "Winsock & TCP/IP-Stack zurücksetzen", "ar": "إعادة تعيين Winsock و TCP/IP"},
    "Disable Windows Copilot": {"en": "Disable Windows Copilot", "fr": "Désactiver Windows Copilot", "tn": "Ytaffi Copilot AI. Ywaffir RAM w ynahi sidebar.", "es": "Desactivar Windows Copilot", "de": "Windows Copilot deaktivieren", "ar": "تعطيل Windows Copilot"},
    "Disable Recall / AI Screenshots (Win 11 24H2)": {"en": "Disable Recall / AI Screenshots (Win 11 24H2)", "fr": "Désactiver Recall / captures AI (Win 11 24H2)", "tn": "Ytaffi Recall feature. Ymanea screenshots automatiques.", "es": "Desactivar Recall / capturas IA (Win 11 24H2)", "de": "Recall / KI-Screenshots deaktivieren (Win 11 24H2)", "ar": "تعطيل Recall / لقطات الذكاء الاصطناعي"},
    "Set Explorer Compact View (Remove Padding)": {"en": "Set Explorer Compact View (Remove Padding)", "fr": "Activer la vue compacte de l'Explorateur", "tn": "Y7ot Explorer compact view. Kima Windows 10 bidoun padding.", "es": "Establecer vista compacta del Explorador", "de": "Explorer Kompaktansicht aktivieren", "ar": "تعيين العرض المضغوط للمستكشف"},
    "Install 7-Zip": {"en": "Install 7-Zip", "fr": "Installer 7-Zip", "tn": "Installer 7-Zip", "es": "Instalar 7-Zip", "de": "7-Zip installieren", "ar": "تثبيت 7-Zip"},
    "Install Everything (Voidtools)": {"en": "Install Everything (Voidtools)", "fr": "Installer Everything (Voidtools)", "tn": "Installer Everything (Voidtools)", "es": "Instalar Everything (Voidtools)", "de": "Everything installieren", "ar": "تثبيت Everything"},
    "Install PowerToys": {"en": "Install PowerToys", "fr": "Installer PowerToys", "tn": "Installer PowerToys", "es": "Instalar PowerToys", "de": "PowerToys installieren", "ar": "تثبيت PowerToys"},
    "Install HWiNFO": {"en": "Install HWiNFO", "fr": "Installer HWiNFO", "tn": "Installer HWiNFO", "es": "Instalar HWiNFO", "de": "HWiNFO installieren", "ar": "تثبيت HWiNFO"},
    "Install CPU-Z": {"en": "Install CPU-Z", "fr": "Installer CPU-Z", "tn": "Installer CPU-Z", "es": "Instalar CPU-Z", "de": "CPU-Z installieren", "ar": "تثبيت CPU-Z"},
    "Install GPU-Z": {"en": "Install GPU-Z", "fr": "Installer GPU-Z", "tn": "Installer GPU-Z", "es": "Instalar GPU-Z", "de": "GPU-Z installieren", "ar": "تثبيت GPU-Z"},
    "Install Process Explorer": {"en": "Install Process Explorer", "fr": "Installer Process Explorer", "tn": "Installer Process Explorer", "es": "Instalar Process Explorer", "de": "Process Explorer installieren", "ar": "تثبيت Process Explorer"},
    "Install Autoruns": {"en": "Install Autoruns", "fr": "Installer Autoruns", "tn": "Installer Autoruns", "es": "Instalar Autoruns", "de": "Autoruns installieren", "ar": "تثبيت Autoruns"},
    "Install WizTree": {"en": "Install WizTree", "fr": "Installer WizTree", "tn": "Installer WizTree", "es": "Instalar WizTree", "de": "WizTree installieren", "ar": "تثبيت WizTree"},
    "Install MSI Afterburner": {"en": "Install MSI Afterburner", "fr": "Installer MSI Afterburner", "tn": "Installer MSI Afterburner", "es": "Instalar MSI Afterburner", "de": "MSI Afterburner installieren", "ar": "تثبيت MSI Afterburner"},
    "Install NVCleanstall": {"en": "Install NVCleanstall", "fr": "Installer NVCleanstall", "tn": "Installer NVCleanstall", "es": "Instalar NVCleanstall", "de": "NVCleanstall installieren", "ar": "تثبيت NVCleanstall"},
    "Install Bulk Crap Uninstaller": {"en": "Install Bulk Crap Uninstaller", "fr": "Installer Bulk Crap Uninstaller", "tn": "Installer Bulk Crap Uninstaller", "es": "Instalar Bulk Crap Uninstaller", "de": "Bulk Crap Uninstaller installieren", "ar": "تثبيت Bulk Crap Uninstaller"},
    "Install ShareX": {"en": "Install ShareX", "fr": "Installer ShareX", "tn": "Installer ShareX", "es": "Instalar ShareX", "de": "ShareX installieren", "ar": "تثبيت ShareX"},
    "Install Notepad++": {"en": "Install Notepad++", "fr": "Installer Notepad++", "tn": "Installer Notepad++", "es": "Instalar Notepad++", "de": "Notepad++ installieren", "ar": "تثبيت Notepad++"},
    "Install Rufus": {"en": "Install Rufus", "fr": "Installer Rufus", "tn": "Installer Rufus", "es": "Instalar Rufus", "de": "Rufus installieren", "ar": "تثبيت Rufus"},
    "Install CrystalDiskInfo": {"en": "Install CrystalDiskInfo", "fr": "Installer CrystalDiskInfo", "tn": "Installer CrystalDiskInfo", "es": "Instalar CrystalDiskInfo", "de": "CrystalDiskInfo installieren", "ar": "تثبيت CrystalDiskInfo"},
    "Install CrystalDiskMark": {"en": "Install CrystalDiskMark", "fr": "Installer CrystalDiskMark", "tn": "Installer CrystalDiskMark", "es": "Instalar CrystalDiskMark", "de": "CrystalDiskMark installieren", "ar": "تثبيت CrystalDiskMark"},
    "Install HWMonitor": {"en": "Install HWMonitor", "fr": "Installer HWMonitor", "tn": "Installer HWMonitor", "es": "Instalar HWMonitor", "de": "HWMonitor installieren", "ar": "تثبيت HWMonitor"},
    "Install UniGetUI": {"en": "Install UniGetUI", "fr": "Installer UniGetUI", "tn": "Installer UniGetUI", "es": "Instalar UniGetUI", "de": "UniGetUI installieren", "ar": "تثبيت UniGetUI"},
    "Install Ventoy": {"en": "Install Ventoy", "fr": "Installer Ventoy", "tn": "Installer Ventoy", "es": "Instalar Ventoy", "de": "Ventoy installieren", "ar": "تثبيت Ventoy"},
    "Install Flow Launcher": {"en": "Install Flow Launcher", "fr": "Installer Flow Launcher", "tn": "Installer Flow Launcher", "es": "Instalar Flow Launcher", "de": "Flow Launcher installieren", "ar": "تثبيت Flow Launcher"},
    "Install EarTrumpet": {"en": "Install EarTrumpet", "fr": "Installer EarTrumpet", "tn": "Installer EarTrumpet", "es": "Instalar EarTrumpet", "de": "EarTrumpet installieren", "ar": "تثبيت EarTrumpet"},
    "Install TCPView": {"en": "Install TCPView", "fr": "Installer TCPView", "tn": "Installer TCPView", "es": "Instalar TCPView", "de": "TCPView installieren", "ar": "تثبيت TCPView"},
    "Install O&O ShutUp10++": {"en": "Install O&O ShutUp10++", "fr": "Installer O&O ShutUp10++", "tn": "Installer O&O ShutUp10++", "es": "Instalar O&O ShutUp10++", "de": "O&O ShutUp10++ installieren", "ar": "تثبيت O&O ShutUp10++"},
    "Install Process Monitor": {"en": "Install Process Monitor", "fr": "Installer Process Monitor", "tn": "Installer Process Monitor", "es": "Instalar Process Monitor", "de": "Process Monitor installieren", "ar": "تثبيت Process Monitor"},
    "Install Revo Uninstaller": {"en": "Install Revo Uninstaller", "fr": "Installer Revo Uninstaller", "tn": "Installer Revo Uninstaller", "es": "Instalar Revo Uninstaller", "de": "Revo Uninstaller installieren", "ar": "تثبيت Revo Uninstaller"},
    "Install Snappy Driver Installer": {"en": "Install Snappy Driver Installer", "fr": "Installer Snappy Driver Installer", "tn": "Installer Snappy Driver Installer", "es": "Instalar Snappy Driver Installer", "de": "Snappy Driver Installer installieren", "ar": "تثبيت Snappy Driver Installer"},
    "Install ExplorerPatcher": {"en": "Install ExplorerPatcher", "fr": "Installer ExplorerPatcher", "tn": "Installer ExplorerPatcher", "es": "Instalar ExplorerPatcher", "de": "ExplorerPatcher installieren", "ar": "تثبيت ExplorerPatcher"},
    "Install QuickLook": {"en": "Install QuickLook", "fr": "Installer QuickLook", "tn": "Installer QuickLook", "es": "Instalar QuickLook", "de": "QuickLook installieren", "ar": "تثبيت QuickLook"},
    "Install Ditto Clipboard": {"en": "Install Ditto Clipboard", "fr": "Installer Ditto Clipboard", "tn": "Installer Ditto Clipboard", "es": "Instalar Ditto Clipboard", "de": "Ditto Clipboard installieren", "ar": "تثبيت Ditto Clipboard"},
    "Install LatencyMon": {"en": "Install LatencyMon", "fr": "Installer LatencyMon", "tn": "Installer LatencyMon", "es": "Instalar LatencyMon", "de": "LatencyMon installieren", "ar": "تثبيت LatencyMon"},
    "Install Process Lasso": {"en": "Install Process Lasso", "fr": "Installer Process Lasso", "tn": "Installer Process Lasso", "es": "Instalar Process Lasso", "de": "Process Lasso installieren", "ar": "تثبيت Process Lasso"},
    "Install ParkControl": {"en": "Install ParkControl", "fr": "Installer ParkControl", "tn": "Installer ParkControl", "es": "Instalar ParkControl", "de": "ParkControl installieren", "ar": "تثبيت ParkControl"},
    "Install ThrottleStop": {"en": "Install ThrottleStop", "fr": "Installer ThrottleStop", "tn": "Installer ThrottleStop", "es": "Instalar ThrottleStop", "de": "ThrottleStop installieren", "ar": "تثبيت ThrottleStop"},
    "Install RTSS": {"en": "Install RTSS", "fr": "Installer RTSS", "tn": "Installer RTSS", "es": "Instalar RTSS", "de": "RTSS installieren", "ar": "تثبيت RTSS"},
    "Install CapFrameX": {"en": "Install CapFrameX", "fr": "Installer CapFrameX", "tn": "Installer CapFrameX", "es": "Instalar CapFrameX", "de": "CapFrameX installieren", "ar": "تثبيت CapFrameX"},
    "Install DDU": {"en": "Install DDU", "fr": "Installer DDU", "tn": "Installer DDU", "es": "Instalar DDU", "de": "DDU installieren", "ar": "تثبيت DDU"},
    "Install Sysmon": {"en": "Install Sysmon", "fr": "Installer Sysmon", "tn": "Installer Sysmon", "es": "Instalar Sysmon", "de": "Sysmon installieren", "ar": "تثبيت Sysmon"},
    "Install Sophia Script": {"en": "Install Sophia Script", "fr": "Installer Sophia Script", "tn": "Installer Sophia Script", "es": "Instalar Sophia Script", "de": "Sophia Script installieren", "ar": "تثبيت Sophia Script"},
    "Install privacy.sexy": {"en": "Install privacy.sexy", "fr": "Installer privacy.sexy", "tn": "Installer privacy.sexy", "es": "Instalar privacy.sexy", "de": "privacy.sexy installieren", "ar": "تثبيت privacy.sexy"},
    "Install simplewall": {"en": "Install simplewall", "fr": "Installer simplewall", "tn": "Installer simplewall", "es": "Instalar simplewall", "de": "simplewall installieren", "ar": "تثبيت simplewall"},
    "Install Portmaster": {"en": "Install Portmaster", "fr": "Installer Portmaster", "tn": "Installer Portmaster", "es": "Instalar Portmaster", "de": "Portmaster installieren", "ar": "تثبيت Portmaster"},
    "Install Mem Reduct": {"en": "Install Mem Reduct", "fr": "Installer Mem Reduct", "tn": "Installer Mem Reduct", "es": "Instalar Mem Reduct", "de": "Mem Reduct installieren", "ar": "تثبيت Mem Reduct"},
    "Install CRU": {"en": "Install CRU", "fr": "Installer CRU", "tn": "Installer CRU", "es": "Instalar CRU", "de": "CRU installieren", "ar": "تثبيت CRU"},
    "Install CompactGUI": {"en": "Install CompactGUI", "fr": "Installer CompactGUI", "tn": "Installer CompactGUI", "es": "Instalar CompactGUI", "de": "CompactGUI installieren", "ar": "تثبيت CompactGUI"},
    "Install GlassWire": {"en": "Install GlassWire", "fr": "Installer GlassWire", "tn": "Installer GlassWire", "es": "Instalar GlassWire", "de": "GlassWire installieren", "ar": "تثبيت GlassWire"},
    "Install WPD": {"en": "Install WPD", "fr": "Installer WPD", "tn": "Installer WPD", "es": "Instalar WPD", "de": "WPD installieren", "ar": "تثبيت WPD"},
    "Install LosslessCut": {"en": "Install LosslessCut", "fr": "Installer LosslessCut", "tn": "Installer LosslessCut", "es": "Instalar LosslessCut", "de": "LosslessCut installieren", "ar": "تثبيت LosslessCut"},
    "Install AutoHotkey": {"en": "Install AutoHotkey", "fr": "Installer AutoHotkey", "tn": "Installer AutoHotkey", "es": "Instalar AutoHotkey", "de": "AutoHotkey installieren", "ar": "تثبيت AutoHotkey"},
    "Install WizFile": {"en": "Install WizFile", "fr": "Installer WizFile", "tn": "Installer WizFile", "es": "Instalar WizFile", "de": "WizFile installieren", "ar": "تثبيت WizFile"},
    "Install dupeGuru": {"en": "Install dupeGuru", "fr": "Installer dupeGuru", "tn": "Installer dupeGuru", "es": "Instalar dupeGuru", "de": "dupeGuru installieren", "ar": "تثبيت dupeGuru"},
    "Install FanControl": {"en": "Install FanControl", "fr": "Installer FanControl", "tn": "Installer FanControl", "es": "Instalar FanControl", "de": "FanControl installieren", "ar": "تثبيت FanControl"},
    "Install OpenRGB": {"en": "Install OpenRGB", "fr": "Installer OpenRGB", "tn": "Installer OpenRGB", "es": "Instalar OpenRGB", "de": "OpenRGB installieren", "ar": "تثبيت OpenRGB"},
    "Install LibreHardwareMonitor": {"en": "Install LibreHardwareMonitor", "fr": "Installer LibreHardwareMonitor", "tn": "Installer LibreHardwareMonitor", "es": "Instalar LibreHardwareMonitor", "de": "LibreHardwareMonitor installieren", "ar": "تثبيت LibreHardwareMonitor"},
    "Install BlueScreenView": {"en": "Install BlueScreenView", "fr": "Installer BlueScreenView", "tn": "Installer BlueScreenView", "es": "Instalar BlueScreenView", "de": "BlueScreenView installieren", "ar": "تثبيت BlueScreenView"},
    "Install ShellExView": {"en": "Install ShellExView", "fr": "Installer ShellExView", "tn": "Installer ShellExView", "es": "Instalar ShellExView", "de": "ShellExView installieren", "ar": "تثبيت ShellExView"},
    "Install AppReadWriteCounter": {"en": "Install AppReadWriteCounter", "fr": "Installer AppReadWriteCounter", "tn": "Installer AppReadWriteCounter", "es": "Instalar AppReadWriteCounter", "de": "AppReadWriteCounter installieren", "ar": "تثبيت AppReadWriteCounter"},
    "Install SoundVolumeView": {"en": "Install SoundVolumeView", "fr": "Installer SoundVolumeView", "tn": "Installer SoundVolumeView", "es": "Instalar SoundVolumeView", "de": "SoundVolumeView installieren", "ar": "تثبيت SoundVolumeView"},
    "Install FullEventLogView": {"en": "Install FullEventLogView", "fr": "Installer FullEventLogView", "tn": "Installer FullEventLogView", "es": "Instalar FullEventLogView", "de": "FullEventLogView installieren", "ar": "تثبيت FullEventLogView"},
    "Install Dependencies": {"en": "Install Dependencies", "fr": "Installer Dependencies", "tn": "Installer Dependencies", "es": "Instalar Dependencies", "de": "Dependencies installieren", "ar": "تثبيت Dependencies"},
    "Install Resource Hacker": {"en": "Install Resource Hacker", "fr": "Installer Resource Hacker", "tn": "Installer Resource Hacker", "es": "Instalar Resource Hacker", "de": "Resource Hacker installieren", "ar": "تثبيت Resource Hacker"},
    "Install x64dbg": {"en": "Install x64dbg", "fr": "Installer x64dbg", "tn": "Installer x64dbg", "es": "Instalar x64dbg", "de": "x64dbg installieren", "ar": "تثبيت x64dbg"},
    "Install MacType": {"en": "Install MacType", "fr": "Installer MacType", "tn": "Installer MacType", "es": "Instalar MacType", "de": "MacType installieren", "ar": "تثبيت MacType"},
    "Install TranslucentTB": {"en": "Install TranslucentTB", "fr": "Installer TranslucentTB", "tn": "Installer TranslucentTB", "es": "Instalar TranslucentTB", "de": "TranslucentTB installieren", "ar": "تثبيت TranslucentTB"},
    "Install ModernFlyouts": {"en": "Install ModernFlyouts", "fr": "Installer ModernFlyouts", "tn": "Installer ModernFlyouts", "es": "Instalar ModernFlyouts", "de": "ModernFlyouts installieren", "ar": "تثبيت ModernFlyouts"},
    "Install DevToys": {"en": "Install DevToys", "fr": "Installer DevToys", "tn": "Installer DevToys", "es": "Instalar DevToys", "de": "DevToys installieren", "ar": "تثبيت DevToys"},
    "Install GlazeWM": {"en": "Install GlazeWM", "fr": "Installer GlazeWM", "tn": "Installer GlazeWM", "es": "Instalar GlazeWM", "de": "GlazeWM installieren", "ar": "تثبيت GlazeWM"},
    "Install NanaZip": {"en": "Install NanaZip", "fr": "Installer NanaZip", "tn": "Installer NanaZip", "es": "Instalar NanaZip", "de": "NanaZip installieren", "ar": "تثبيت NanaZip"},
    "Install Bulk Rename Utility": {"en": "Install Bulk Rename Utility", "fr": "Installer Bulk Rename Utility", "tn": "Installer Bulk Rename Utility", "es": "Instalar Bulk Rename Utility", "de": "Bulk Rename Utility installieren", "ar": "تثبيت Bulk Rename Utility"},
    "Install privacy.sexy": {"en": "Install privacy.sexy", "fr": "Installer privacy.sexy", "tn": "Installer privacy.sexy", "es": "Instalar privacy.sexy", "de": "privacy.sexy installieren", "ar": "تثبيت privacy.sexy"},
    "Install AltSnap": {"en": "Install AltSnap", "fr": "Installer AltSnap", "tn": "Installer AltSnap", "es": "Instalar AltSnap", "de": "AltSnap installieren", "ar": "تثبيت AltSnap"},
    "Install SoundSwitch": {"en": "Install SoundSwitch", "fr": "Installer SoundSwitch", "tn": "Installer SoundSwitch", "es": "Instalar SoundSwitch", "de": "SoundSwitch installieren", "ar": "تثبيت SoundSwitch"},
    "Install TrafficMonitor": {"en": "Install TrafficMonitor", "fr": "Installer TrafficMonitor", "tn": "Installer TrafficMonitor", "es": "Instalar TrafficMonitor", "de": "TrafficMonitor installieren", "ar": "تثبيت TrafficMonitor"},
    "Install Twinkle Tray": {"en": "Install Twinkle Tray", "fr": "Installer Twinkle Tray", "tn": "Installer Twinkle Tray", "es": "Instalar Twinkle Tray", "de": "Twinkle Tray installieren", "ar": "تثبيت Twinkle Tray"},
    "Install SuperF4": {"en": "Install SuperF4", "fr": "Installer SuperF4", "tn": "Installer SuperF4", "es": "Instalar SuperF4", "de": "SuperF4 installieren", "ar": "تثبيت SuperF4"},
    "Install System Informer": {"en": "Install System Informer", "fr": "Installer System Informer", "tn": "Installer System Informer", "es": "Instalar System Informer", "de": "System Informer installieren", "ar": "تثبيت System Informer"},
    "Install RegCool": {"en": "Install RegCool", "fr": "Installer RegCool", "tn": "Installer RegCool", "es": "Instalar RegCool", "de": "RegCool installieren", "ar": "تثبيت RegCool"},
    "Install Czkawka": {"en": "Install Czkawka", "fr": "Installer Czkawka", "tn": "Installer Czkawka", "es": "Instalar Czkawka", "de": "Czkawka installieren", "ar": "تثبيت Czkawka"},
    "Install dnSpy": {"en": "Install dnSpy", "fr": "Installer dnSpy", "tn": "Installer dnSpy", "es": "Instalar dnSpy", "de": "dnSpy installieren", "ar": "تثبيت dnSpy"},
    "Install PE-bear": {"en": "Install PE-bear", "fr": "Installer PE-bear", "tn": "Installer PE-bear", "es": "Instalar PE-bear", "de": "PE-bear installieren", "ar": "تثبيت PE-bear"},
    "Install Espanso": {"en": "Install Espanso", "fr": "Installer Espanso", "tn": "Installer Espanso", "es": "Instalar Espanso", "de": "Espanso installieren", "ar": "تثبيت Espanso"},
    "Install Monitorian": {"en": "Install Monitorian", "fr": "Installer Monitorian", "tn": "Installer Monitorian", "es": "Instalar Monitorian", "de": "Monitorian installieren", "ar": "تثبيت Monitorian"},
    "Install LocalSend": {"en": "Install LocalSend", "fr": "Installer LocalSend", "tn": "Installer LocalSend", "es": "Instalar LocalSend", "de": "LocalSend installieren", "ar": "تثبيت LocalSend"},
    "Install NTLite": {"en": "Install NTLite", "fr": "Installer NTLite", "tn": "Installer NTLite", "es": "Instalar NTLite", "de": "NTLite installieren", "ar": "تثبيت NTLite"},
    "Install WinSetView": {"en": "Install WinSetView", "fr": "Installer WinSetView", "tn": "Installer WinSetView", "es": "Instalar WinSetView", "de": "WinSetView installieren", "ar": "تثبيت WinSetView"},
    "Install ScreenToGif": {"en": "Install ScreenToGif", "fr": "Installer ScreenToGif", "tn": "Installer ScreenToGif", "es": "Instalar ScreenToGif", "de": "ScreenToGif installieren", "ar": "تثبيت ScreenToGif"},
    "Install WinMerge": {"en": "Install WinMerge", "fr": "Installer WinMerge", "tn": "Installer WinMerge", "es": "Instalar WinMerge", "de": "WinMerge installieren", "ar": "تثبيت WinMerge"},
    "Install carnac": {"en": "Install carnac", "fr": "Installer carnac", "tn": "Installer carnac", "es": "Instalar carnac", "de": "carnac installieren", "ar": "تثبيت carnac"},
    "Install Flameshot": {"en": "Install Flameshot", "fr": "Installer Flameshot", "tn": "Installer Flameshot", "es": "Instalar Flameshot", "de": "Flameshot installieren", "ar": "تثبيت Flameshot"},
    "Install Qalculate!": {"en": "Install Qalculate!", "fr": "Installer Qalculate!", "tn": "Installer Qalculate!", "es": "Instalar Qalculate!", "de": "Qalculate! installieren", "ar": "تثبيت Qalculate!"},
    "Install OCCT": {"en": "Install OCCT", "fr": "Installer OCCT", "tn": "Installer OCCT", "es": "Instalar OCCT", "de": "OCCT installieren", "ar": "تثبيت OCCT"},
    "Install FurMark": {"en": "Install FurMark", "fr": "Installer FurMark", "tn": "Installer FurMark", "es": "Instalar FurMark", "de": "FurMark installieren", "ar": "تثبيت FurMark"},
    "Install Core Temp": {"en": "Install Core Temp", "fr": "Installer Core Temp", "tn": "Installer Core Temp", "es": "Instalar Core Temp", "de": "Core Temp installieren", "ar": "تثبيت Core Temp"},
    "Install AIDA64": {"en": "Install AIDA64", "fr": "Installer AIDA64", "tn": "Installer AIDA64", "es": "Instalar AIDA64", "de": "AIDA64 installieren", "ar": "تثبيت AIDA64"},
    "Install KeePassXC": {"en": "Install KeePassXC", "fr": "Installer KeePassXC", "tn": "Installer KeePassXC", "es": "Instalar KeePassXC", "de": "KeePassXC installieren", "ar": "تثبيت KeePassXC"},
    "Install Bitwarden": {"en": "Install Bitwarden", "fr": "Installer Bitwarden", "tn": "Installer Bitwarden", "es": "Instalar Bitwarden", "de": "Bitwarden installieren", "ar": "تثبيت Bitwarden"},
    "Install Malwarebytes": {"en": "Install Malwarebytes", "fr": "Installer Malwarebytes", "tn": "Installer Malwarebytes", "es": "Instalar Malwarebytes", "de": "Malwarebytes installieren", "ar": "تثبيت Malwarebytes"},
    "Install Brave Browser": {"en": "Install Brave Browser", "fr": "Installer Brave Browser", "tn": "Installer Brave Browser", "es": "Instalar Brave Browser", "de": "Brave Browser installieren", "ar": "تثبيت Brave Browser"},
    "Install Wireshark": {"en": "Install Wireshark", "fr": "Installer Wireshark", "tn": "Installer Wireshark", "es": "Instalar Wireshark", "de": "Wireshark installieren", "ar": "تثبيت Wireshark"},
    "Install WinDirStat": {"en": "Install WinDirStat", "fr": "Installer WinDirStat", "tn": "Installer WinDirStat", "es": "Instalar WinDirStat", "de": "WinDirStat installieren", "ar": "تثبيت WinDirStat"},
    "Install FastCopy": {"en": "Install FastCopy", "fr": "Installer FastCopy", "tn": "Installer FastCopy", "es": "Instalar FastCopy", "de": "FastCopy installieren", "ar": "تثبيت FastCopy"},
    "Install TreeSize Free": {"en": "Install TreeSize Free", "fr": "Installer TreeSize Free", "tn": "Installer TreeSize Free", "es": "Instalar TreeSize Free", "de": "TreeSize Free installieren", "ar": "تثبيت TreeSize Free"},
    "Install File Converter": {"en": "Install File Converter", "fr": "Installer File Converter", "tn": "Installer File Converter", "es": "Instalar File Converter", "de": "File Converter installieren", "ar": "تثبيت File Converter"},
    "Install Rainmeter": {"en": "Install Rainmeter", "fr": "Installer Rainmeter", "tn": "Installer Rainmeter", "es": "Instalar Rainmeter", "de": "Rainmeter installieren", "ar": "تثبيت Rainmeter"},
    "Install Git": {"en": "Install Git", "fr": "Installer Git", "tn": "Installer Git", "es": "Instalar Git", "de": "Git installieren", "ar": "تثبيت Git"},
    "Install Windows Terminal": {"en": "Install Windows Terminal", "fr": "Installer Windows Terminal", "tn": "Installer Windows Terminal", "es": "Instalar Windows Terminal", "de": "Windows Terminal installieren", "ar": "تثبيت Windows Terminal"},
    "Install PowerShell 7": {"en": "Install PowerShell 7", "fr": "Installer PowerShell 7", "tn": "Installer PowerShell 7", "es": "Instalar PowerShell 7", "de": "PowerShell 7 installieren", "ar": "تثبيت PowerShell 7"},
    "Install Postman": {"en": "Install Postman", "fr": "Installer Postman", "tn": "Installer Postman", "es": "Instalar Postman", "de": "Postman installieren", "ar": "تثبيت Postman"},
    "Install VLC": {"en": "Install VLC", "fr": "Installer VLC", "tn": "Installer VLC", "es": "Instalar VLC", "de": "VLC installieren", "ar": "تثبيت VLC"},
    "Install OBS Studio": {"en": "Install OBS Studio", "fr": "Installer OBS Studio", "tn": "Installer OBS Studio", "es": "Instalar OBS Studio", "de": "OBS Studio installieren", "ar": "تثبيت OBS Studio"},
    "Install HandBrake": {"en": "Install HandBrake", "fr": "Installer HandBrake", "tn": "Installer HandBrake", "es": "Instalar HandBrake", "de": "HandBrake installieren", "ar": "تثبيت HandBrake"},
    "Install Audacity": {"en": "Install Audacity", "fr": "Installer Audacity", "tn": "Installer Audacity", "es": "Instalar Audacity", "de": "Audacity installieren", "ar": "تثبيت Audacity"},
    "Install GIMP": {"en": "Install GIMP", "fr": "Installer GIMP", "tn": "Installer GIMP", "es": "Instalar GIMP", "de": "GIMP installieren", "ar": "تثبيت GIMP"},
    "Install Obsidian": {"en": "Install Obsidian", "fr": "Installer Obsidian", "tn": "Installer Obsidian", "es": "Instalar Obsidian", "de": "Obsidian installieren", "ar": "تثبيت Obsidian"},
    "Install Joplin": {"en": "Install Joplin", "fr": "Installer Joplin", "tn": "Installer Joplin", "es": "Instalar Joplin", "de": "Joplin installieren", "ar": "تثبيت Joplin"},
    "Install KDE Connect": {"en": "Install KDE Connect", "fr": "Installer KDE Connect", "tn": "Installer KDE Connect", "es": "Instalar KDE Connect", "de": "KDE Connect installieren", "ar": "تثبيت KDE Connect"},
    "Install Sumatra PDF": {"en": "Install Sumatra PDF", "fr": "Installer Sumatra PDF", "tn": "Installer Sumatra PDF", "es": "Instalar Sumatra PDF", "de": "Sumatra PDF installieren", "ar": "تثبيت Sumatra PDF"},
    "Install Kdenlive": {"en": "Install Kdenlive", "fr": "Installer Kdenlive", "tn": "Installer Kdenlive", "es": "Instalar Kdenlive", "de": "Kdenlive installieren", "ar": "تثبيت Kdenlive"},
    "Install Quick CPU": {"en": "Install Quick CPU", "fr": "Installer Quick CPU", "tn": "Installer Quick CPU", "es": "Instalar Quick CPU", "de": "Quick CPU installieren", "ar": "تثبيت Quick CPU"},
    "Install Special K": {"en": "Install Special K", "fr": "Installer Special K", "tn": "Installer Special K", "es": "Instalar Special K", "de": "Special K installieren", "ar": "تثبيت Special K"},
    "Install Intel PresentMon": {"en": "Install Intel PresentMon", "fr": "Installer Intel PresentMon", "tn": "Installer Intel PresentMon", "es": "Instalar Intel PresentMon", "de": "Intel PresentMon installieren", "ar": "تثبيت Intel PresentMon"},
    "Install NVIDIA FrameView": {"en": "Install NVIDIA FrameView", "fr": "Installer NVIDIA FrameView", "tn": "Installer NVIDIA FrameView", "es": "Instalar NVIDIA FrameView", "de": "NVIDIA FrameView installieren", "ar": "تثبيت NVIDIA FrameView"},
    "Install AMD OCAT": {"en": "Install AMD OCAT", "fr": "Installer AMD OCAT", "tn": "Installer AMD OCAT", "es": "Instalar AMD OCAT", "de": "AMD OCAT installieren", "ar": "تثبيت AMD OCAT"},
    "Install BenchMate": {"en": "Install BenchMate", "fr": "Installer BenchMate", "tn": "Installer BenchMate", "es": "Instalar BenchMate", "de": "BenchMate installieren", "ar": "تثبيت BenchMate"},
    "Install Intel XTU": {"en": "Install Intel XTU", "fr": "Installer Intel XTU", "tn": "Installer Intel XTU", "es": "Instalar Intel XTU", "de": "Intel XTU installieren", "ar": "تثبيت Intel XTU"},
    "Install UXTU": {"en": "Install UXTU", "fr": "Installer UXTU", "tn": "Installer UXTU", "es": "Instalar UXTU", "de": "UXTU installieren", "ar": "تثبيت UXTU"},
    "Install TweakPower": {"en": "Install TweakPower", "fr": "Installer TweakPower", "tn": "Installer TweakPower", "es": "Instalar TweakPower", "de": "TweakPower installieren", "ar": "تثبيت TweakPower"},
    "Install NetLimiter": {"en": "Install NetLimiter", "fr": "Installer NetLimiter", "tn": "Installer NetLimiter", "es": "Instalar NetLimiter", "de": "NetLimiter installieren", "ar": "تثبيت NetLimiter"},
    "Install ASIO4ALL": {"en": "Install ASIO4ALL", "fr": "Installer ASIO4ALL", "tn": "Installer ASIO4ALL", "es": "Instalar ASIO4ALL", "de": "ASIO4ALL installieren", "ar": "تثبيت ASIO4ALL"},
    "Install REAL": {"en": "Install REAL", "fr": "Installer REAL", "tn": "Installer REAL", "es": "Instalar REAL", "de": "REAL installieren", "ar": "تثبيت REAL"},
    "Install Core-to-Core Latency": {"en": "Install Core-to-Core Latency", "fr": "Installer Core-to-Core Latency", "tn": "Installer Core-to-Core Latency", "es": "Instalar Core-to-Core Latency", "de": "Core-to-Core Latency installieren", "ar": "تثبيت Core-to-Core Latency"},
    "Install Processes Priority Mgr": {"en": "Install Processes Priority Mgr", "fr": "Installer Processes Priority Mgr", "tn": "Installer Processes Priority Mgr", "es": "Instalar Processes Priority Mgr", "de": "Processes Priority Mgr installieren", "ar": "تثبيت Processes Priority Mgr"},
    "Install RAMMap": {"en": "Install RAMMap", "fr": "Installer RAMMap", "tn": "Installer RAMMap", "es": "Instalar RAMMap", "de": "RAMMap installieren", "ar": "تثبيت RAMMap"},
    "Install Windows Memory Cleaner": {"en": "Install Windows Memory Cleaner", "fr": "Installer Windows Memory Cleaner", "tn": "Installer Windows Memory Cleaner", "es": "Instalar Windows Memory Cleaner", "de": "Windows Memory Cleaner installieren", "ar": "تثبيت Windows Memory Cleaner"},
    "Install DiskCountersView": {"en": "Install DiskCountersView", "fr": "Installer DiskCountersView", "tn": "Installer DiskCountersView", "es": "Instalar DiskCountersView", "de": "DiskCountersView installieren", "ar": "تثبيت DiskCountersView"},
    "Install NetworkCountersWatch": {"en": "Install NetworkCountersWatch", "fr": "Installer NetworkCountersWatch", "tn": "Installer NetworkCountersWatch", "es": "Instalar NetworkCountersWatch", "de": "NetworkCountersWatch installieren", "ar": "تثبيت NetworkCountersWatch"},
    "Install Windhawk": {"en": "Install Windhawk", "fr": "Installer Windhawk", "tn": "Installer Windhawk", "es": "Instalar Windhawk", "de": "Windhawk installieren", "ar": "تثبيت Windhawk"},
    "Install Nilesoft Shell": {"en": "Install Nilesoft Shell", "fr": "Installer Nilesoft Shell", "tn": "Installer Nilesoft Shell", "es": "Instalar Nilesoft Shell", "de": "Nilesoft Shell installieren", "ar": "تثبيت Nilesoft Shell"},
    "Install Seelen UI": {"en": "Install Seelen UI", "fr": "Installer Seelen UI", "tn": "Installer Seelen UI", "es": "Instalar Seelen UI", "de": "Seelen UI installieren", "ar": "تثبيت Seelen UI"},
    "Install komorebi": {"en": "Install komorebi", "fr": "Installer komorebi", "tn": "Installer komorebi", "es": "Instalar komorebi", "de": "komorebi installieren", "ar": "تثبيت komorebi"},
    "Install Textify": {"en": "Install Textify", "fr": "Installer Textify", "tn": "Installer Textify", "es": "Instalar Textify", "de": "Textify installieren", "ar": "تثبيت Textify"},
    "Install Sizer": {"en": "Install Sizer", "fr": "Installer Sizer", "tn": "Installer Sizer", "es": "Instalar Sizer", "de": "Sizer installieren", "ar": "تثبيت Sizer"},
    "Install ZoomIt": {"en": "Install ZoomIt", "fr": "Installer ZoomIt", "tn": "Installer ZoomIt", "es": "Instalar ZoomIt", "de": "ZoomIt installieren", "ar": "تثبيت ZoomIt"},
    "Install scrcpy": {"en": "Install scrcpy", "fr": "Installer scrcpy", "tn": "Installer scrcpy", "es": "Instalar scrcpy", "de": "scrcpy installieren", "ar": "تثبيت scrcpy"},
    "Install WhatIsHang": {"en": "Install WhatIsHang", "fr": "Installer WhatIsHang", "tn": "Installer WhatIsHang", "es": "Instalar WhatIsHang", "de": "WhatIsHang installieren", "ar": "تثبيت WhatIsHang"},
    "Install SophiApp": {"en": "Install SophiApp", "fr": "Installer SophiApp", "tn": "Installer SophiApp", "es": "Instalar SophiApp", "de": "SophiApp installieren", "ar": "تثبيت SophiApp"},
    "Install O&O AppBuster": {"en": "Install O&O AppBuster", "fr": "Installer O&O AppBuster", "tn": "Installer O&O AppBuster", "es": "Instalar O&O AppBuster", "de": "O&O AppBuster installieren", "ar": "تثبيت O&O AppBuster"},
    "Install BleachBit": {"en": "Install BleachBit", "fr": "Installer BleachBit", "tn": "Installer BleachBit", "es": "Instalar BleachBit", "de": "BleachBit installieren", "ar": "تثبيت BleachBit"},
    "Install SharpKeys": {"en": "Install SharpKeys", "fr": "Installer SharpKeys", "tn": "Installer SharpKeys", "es": "Instalar SharpKeys", "de": "SharpKeys installieren", "ar": "تثبيت SharpKeys"},
    "Install ContextMenuManager": {"en": "Install ContextMenuManager", "fr": "Installer ContextMenuManager", "tn": "Installer ContextMenuManager", "es": "Instalar ContextMenuManager", "de": "ContextMenuManager installieren", "ar": "تثبيت ContextMenuManager"},
    "Install Sandboxie-Plus": {"en": "Install Sandboxie-Plus", "fr": "Installer Sandboxie-Plus", "tn": "Installer Sandboxie-Plus", "es": "Instalar Sandboxie-Plus", "de": "Sandboxie-Plus installieren", "ar": "تثبيت Sandboxie-Plus"},
    "Install Lively Wallpaper": {"en": "Install Lively Wallpaper", "fr": "Installer Lively Wallpaper", "tn": "Installer Lively Wallpaper", "es": "Instalar Lively Wallpaper", "de": "Lively Wallpaper installieren", "ar": "تثبيت Lively Wallpaper"},
    "Install QTTabBar": {"en": "Install QTTabBar", "fr": "Installer QTTabBar", "tn": "Installer QTTabBar", "es": "Instalar QTTabBar", "de": "QTTabBar installieren", "ar": "تثبيت QTTabBar"},
    "Install PatchCleaner": {"en": "Install PatchCleaner", "fr": "Installer PatchCleaner", "tn": "Installer PatchCleaner", "es": "Instalar PatchCleaner", "de": "PatchCleaner installieren", "ar": "تثبيت PatchCleaner"},
    "Install SpaceSniffer": {"en": "Install SpaceSniffer", "fr": "Installer SpaceSniffer", "tn": "Installer SpaceSniffer", "es": "Instalar SpaceSniffer", "de": "SpaceSniffer installieren", "ar": "تثبيت SpaceSniffer"},
    "Install DNS Jumper": {"en": "Install DNS Jumper", "fr": "Installer DNS Jumper", "tn": "Installer DNS Jumper", "es": "Instalar DNS Jumper", "de": "DNS Jumper installieren", "ar": "تثبيت DNS Jumper"},
    "Install OpenHashTab": {"en": "Install OpenHashTab", "fr": "Installer OpenHashTab", "tn": "Installer OpenHashTab", "es": "Instalar OpenHashTab", "de": "OpenHashTab installieren", "ar": "تثبيت OpenHashTab"},
    "Install USBDeview": {"en": "Install USBDeview", "fr": "Installer USBDeview", "tn": "Installer USBDeview", "es": "Instalar USBDeview", "de": "USBDeview installieren", "ar": "تثبيت USBDeview"},
    "Install WireGuard": {"en": "Install WireGuard", "fr": "Installer WireGuard", "tn": "Installer WireGuard", "es": "Instalar WireGuard", "de": "WireGuard installieren", "ar": "تثبيت WireGuard"},
    "Install Nmap": {"en": "Install Nmap", "fr": "Installer Nmap", "tn": "Installer Nmap", "es": "Instalar Nmap", "de": "Nmap installieren", "ar": "تثبيت Nmap"},
    "Install HxD": {"en": "Install HxD", "fr": "Installer HxD", "tn": "Installer HxD", "es": "Instalar HxD", "de": "HxD installieren", "ar": "تثبيت HxD"},
    "Install MediaInfo": {"en": "Install MediaInfo", "fr": "Installer MediaInfo", "tn": "Installer MediaInfo", "es": "Instalar MediaInfo", "de": "MediaInfo installieren", "ar": "تثبيت MediaInfo"},
    "Install WinSCP": {"en": "Install WinSCP", "fr": "Installer WinSCP", "tn": "Installer WinSCP", "es": "Instalar WinSCP", "de": "WinSCP installieren", "ar": "تثبيت WinSCP"},
    "Install PuTTY": {"en": "Install PuTTY", "fr": "Installer PuTTY", "tn": "Installer PuTTY", "es": "Instalar PuTTY", "de": "PuTTY installieren", "ar": "تثبيت PuTTY"},
    "Install Clink": {"en": "Install Clink", "fr": "Installer Clink", "tn": "Installer Clink", "es": "Instalar Clink", "de": "Clink installieren", "ar": "تثبيت Clink"},
    "Install ImageGlass": {"en": "Install ImageGlass", "fr": "Installer ImageGlass", "tn": "Installer ImageGlass", "es": "Instalar ImageGlass", "de": "ImageGlass installieren", "ar": "تثبيت ImageGlass"},
    "Install foobar2000": {"en": "Install foobar2000", "fr": "Installer foobar2000", "tn": "Installer foobar2000", "es": "Instalar foobar2000", "de": "foobar2000 installieren", "ar": "تثبيت foobar2000"},
    "Install MPC-HC": {"en": "Install MPC-HC", "fr": "Installer MPC-HC", "tn": "Installer MPC-HC", "es": "Instalar MPC-HC", "de": "MPC-HC installieren", "ar": "تثبيت MPC-HC"},
    "Install yt-dlp": {"en": "Install yt-dlp", "fr": "Installer yt-dlp", "tn": "Installer yt-dlp", "es": "Instalar yt-dlp", "de": "yt-dlp installieren", "ar": "تثبيت yt-dlp"},
    "Install MKVToolNix": {"en": "Install MKVToolNix", "fr": "Installer MKVToolNix", "tn": "Installer MKVToolNix", "es": "Instalar MKVToolNix", "de": "MKVToolNix installieren", "ar": "تثبيت MKVToolNix"},
    "Install qBittorrent": {"en": "Install qBittorrent", "fr": "Installer qBittorrent", "tn": "Installer qBittorrent", "es": "Instalar qBittorrent", "de": "qBittorrent installieren", "ar": "تثبيت qBittorrent"},
    "Install Paint.NET": {"en": "Install Paint.NET", "fr": "Installer Paint.NET", "tn": "Installer Paint.NET", "es": "Instalar Paint.NET", "de": "Paint.NET installieren", "ar": "تثبيت Paint.NET"},
    "Install Double Commander": {"en": "Install Double Commander", "fr": "Installer Double Commander", "tn": "Installer Double Commander", "es": "Instalar Double Commander", "de": "Double Commander installieren", "ar": "تثبيت Double Commander"},
    "Disable Paging Executive (Lock Kernel in RAM)": {"en": "Disable Paging Executive (Lock Kernel in RAM)", "fr": "Désactiver le paging de l'exécutif (Verrouiller le noyau en RAM)", "tn": "Ytaffi paging executive (Kernel yab9a fil RAM)", "es": "Desactivar paginación del ejecutivo (Bloquear kernel en RAM)", "de": "Paging Executive deaktivieren (Kernel im RAM sperren)", "ar": "تعطيل تصفح التنفيذ (قفل النواة في الذاكرة)"},
    "Disable NTFS Encryption Service (EFS)": {"en": "Disable NTFS Encryption Service (EFS)", "fr": "Désactiver le service de chiffrement NTFS (EFS)", "tn": "Ytaffi service chiffrement NTFS (EFS)", "es": "Desactivar servicio de cifrado NTFS (EFS)", "de": "NTFS-Verschlüsselungsdienst (EFS) deaktivieren", "ar": "تعطيل خدمة تشفير NTFS (EFS)"},
    "Increase NTFS Memory Usage (Large System Cache)": {"en": "Increase NTFS Memory Usage (Large System Cache)", "fr": "Augmenter l'utilisation mémoire NTFS (Grand cache système)", "tn": "Yzid NTFS memory usage (cache système kbir)", "es": "Aumentar uso de memoria NTFS (Caché grande del sistema)", "de": "NTFS-Speichernutzung erhöhen (Großer Systemcache)", "ar": "زيادة استخدام ذاكرة NTFS (ذاكرة تخزين مؤقت كبيرة)"},
    "Disable Desktop Window Manager Throttling": {"en": "Disable Desktop Window Manager Throttling", "fr": "Désactiver le throttling du DWM", "tn": "Ytaffi DWM throttling (latence akall)", "es": "Desactivar limitación del DWM", "de": "DWM-Throttling deaktivieren", "ar": "تعطيل خنق مدير نوافذ سطح المكتب"},
    "Disable Cursor Shadow & Smooth Scrolling": {"en": "Disable Cursor Shadow & Smooth Scrolling", "fr": "Désactiver l'ombre du curseur et le défilement fluide", "tn": "Ytaffi cursor shadow w smooth scrolling", "es": "Desactivar sombra del cursor y desplazamiento suave", "de": "Cursor-Schatten & sanftes Scrollen deaktivieren", "ar": "تعطيل ظل المؤشر والتمرير السلس"},
    "Disable Network Auto-Tuning Heuristics": {"en": "Disable Network Auto-Tuning Heuristics", "fr": "Désactiver les heuristiques d'auto-réglage réseau", "tn": "Ytaffi heuristiques auto-tuning réseau", "es": "Desactivar heurísticas de auto-ajuste de red", "de": "Netzwerk-Auto-Tuning-Heuristiken deaktivieren", "ar": "تعطيل استدلالات الضبط التلقائي للشبكة"},
    "Disable NLA Probing (Network Location Awareness)": {"en": "Disable NLA Probing (Network Location Awareness)", "fr": "Désactiver le sondage NLA (Détection d'emplacement réseau)", "tn": "Ytaffi NLA probing (ma3adch yping Microsoft)", "es": "Desactivar sondeo NLA (Detección de ubicación de red)", "de": "NLA-Prüfung deaktivieren (Netzwerkstandorterkennung)", "ar": "تعطيل فحص NLA (التعرف على موقع الشبكة)"},
    "Disable Processor Performance Autonomous Mode": {"en": "Disable Processor Performance Autonomous Mode", "fr": "Désactiver le mode autonome de performance processeur", "tn": "Ytaffi mode autonome CPU performance (OS ycontroler)", "es": "Desactivar modo autónomo de rendimiento del procesador", "de": "Prozessor-Performance-Autonommodus deaktivieren", "ar": "تعطيل الوضع المستقل لأداء المعالج"},
    "Disable CPU Idle Scaling (Processor Idle Disable)": {"en": "Disable CPU Idle Scaling (Processor Idle Disable)", "fr": "Désactiver la mise à l'échelle d'inactivité CPU", "tn": "Ytaffi CPU idle scaling (cores yab9aw full speed)", "es": "Desactivar escalado de inactividad de CPU", "de": "CPU-Leerlaufskalierung deaktivieren", "ar": "تعطيل تدريج خمول المعالج"},
    "Disable Pointer Precision Enhancement": {"en": "Disable Pointer Precision Enhancement", "fr": "Désactiver l'amélioration de précision du pointeur", "tn": "Ytaffi mouse acceleration (1:1 mapping)", "es": "Desactivar mejora de precisión del puntero", "de": "Zeigerpräzisionsverbesserung deaktivieren", "ar": "تعطيل تحسين دقة المؤشر"},
    "Set USB Mouse Polling Override (1000Hz)": {"en": "Set USB Mouse Polling Override (1000Hz)", "fr": "Définir le sondage USB souris (1000Hz)", "tn": "Y7ot USB mouse polling override (1000Hz)", "es": "Establecer sondeo USB del ratón (1000Hz)", "de": "USB-Maus-Polling auf 1000Hz setzen", "ar": "تعيين تجاوز استقصاء الماوس USB (1000Hz)"},
    "Disable Customer Experience Improvement Program (CEIP)": {"en": "Disable Customer Experience Improvement Program (CEIP)", "fr": "Désactiver le programme d'amélioration de l'expérience client (CEIP)", "tn": "Ytaffi CEIP (programme amélioration expérience client)", "es": "Desactivar programa de mejora de experiencia del cliente (CEIP)", "de": "Programm zur Verbesserung der Benutzerfreundlichkeit (CEIP) deaktivieren", "ar": "تعطيل برنامج تحسين تجربة العملاء (CEIP)"},
    "Disable Application Impact Telemetry (AIT)": {"en": "Disable Application Impact Telemetry (AIT)", "fr": "Désactiver la télémétrie d'impact des applications (AIT)", "tn": "Ytaffi AIT (telemetrie impact applications)", "es": "Desactivar telemetría de impacto de aplicaciones (AIT)", "de": "Application Impact Telemetrie (AIT) deaktivieren", "ar": "تعطيل قياس تأثير التطبيقات (AIT)"},
    "Disable Taskbar Search Box & Highlights": {"en": "Disable Taskbar Search Box & Highlights", "fr": "Désactiver la boîte de recherche et les highlights de la barre des tâches", "tn": "Ytaffi search box w highlights mel taskbar", "es": "Desactivar cuadro de búsqueda y destacados de la barra de tareas", "de": "Taskleisten-Suchfeld & Highlights deaktivieren", "ar": "تعطيل مربع البحث والإبرازات في شريط المهام"},
    "Disable News & Interests Widget": {"en": "Disable News & Interests Widget", "fr": "Désactiver le widget Actualités et centres d'intérêt", "tn": "Ytaffi widget News & Interests mel taskbar", "es": "Desactivar widget de Noticias e Intereses", "de": "Neuigkeiten & Interessen Widget deaktivieren", "ar": "تعطيل أداة الأخبار والاهتمامات"},
}

TWEAK_DESCS = {
    "Disable All Background UWP Apps": {"en": "Prevents modern Windows apps (UWP) from running in the background while you game. Frees up memory and CPU cycles.", "fr": "Empêche les applis UWP de tourner en arrière-plan pendant vos jeux. Libère mémoire et cycles CPU.", "tn": "Ymanea les applis UWP mel background w enti tel3ab. Yfarregh el memoire w CPU.", "es": "Evita que las apps UWP se ejecuten en segundo plano mientras juegas. Libera memoria y ciclos de CPU.", "de": "Verhindert, dass UWP-Apps im Hintergrund laufen. Gibt RAM und CPU-Zyklen frei.", "ar": "يمنع تطبيقات UWP من العمل في الخلفية أثناء اللعب. يحرر الذاكرة ودورات المعالج."},
    "Disable VBS / HVCI / Core Isolation": {"en": "Removes the hypervisor layer that adds 5-10% overhead to every memory access and kernel call. Microsoft enables this silently on Win11.", "fr": "Supprime la couche hyperviseur qui ajoute 5-10% de surcharge à chaque accès mémoire. Microsoft l'active silencieusement sur Win11.", "tn": "Yna77i el hyperviseur eli yzid 5-10% overhead 3la kol acces memoire. Microsoft y7otha 3al Win11 bla ma t3arfek.", "es": "Elimina la capa del hipervisor que añade 5-10% de sobrecarga en cada acceso a memoria. Microsoft lo activa silenciosamente en Win11.", "de": "Entfernt die Hypervisor-Schicht, die 5-10% Overhead bei jedem Speicherzugriff verursacht. Microsoft aktiviert dies unter Win11 stillschweigend.", "ar": "يزيل طبقة المشرف الافتراضي التي تضيف 5-10% عبء على كل وصول للذاكرة. مايكروسوفت تفعّلها بصمت على Win11."},
    "Disable Spectre / Meltdown Mitigations": {"en": "Removes CPU vulnerability patches that add 2-8% overhead to every syscall and context switch. Biggest impact on I/O-heavy workloads.", "fr": "Supprime les correctifs de vulnérabilité CPU qui ajoutent 2-8% de surcharge. Plus grand impact sur les charges I/O.", "tn": "Yna77i les patches taa3 Spectre/Meltdown eli yzidou 2-8% overhead. Akber impact 3al I/O.", "es": "Elimina parches de vulnerabilidad de CPU que añaden 2-8% de sobrecarga. Mayor impacto en cargas de E/S.", "de": "Entfernt CPU-Sicherheitspatches, die 2-8% Overhead verursachen. Größter Einfluss auf I/O-intensive Workloads.", "ar": "يزيل تصحيحات ثغرات المعالج التي تضيف 2-8% عبء. أكبر تأثير على أحمال الإدخال/الإخراج."},
    "Elevate CSRSS & DWM Priority": {"en": "Gives csrss.exe and dwm.exe High CPU priority (class 3) and High I/O priority so mouse input and frame flips never wait behind game threads.", "fr": "Donne à csrss.exe et dwm.exe une priorité CPU élevée pour que la souris et les frames ne soient jamais bloquées.", "tn": "Ya3ti csrss.exe w dwm.exe priorite 3alya bech el souris w les frames ma yostannewch.", "es": "Da a csrss.exe y dwm.exe prioridad alta de CPU para que ratón y frames nunca esperen.", "de": "Gibt csrss.exe und dwm.exe hohe CPU-Priorität, damit Maus-Input und Frames nie warten.", "ar": "يعطي csrss.exe و dwm.exe أولوية عالية للمعالج لضمان عدم انتظار الماوس والإطارات."},
    "Disable Page Combining (Memory Dedup)": {"en": "Stops the background RAM scanner that searches for identical pages. Saves constant CPU cycles; uses slightly more RAM.", "fr": "Arrête le scanner RAM en arrière-plan. Économise des cycles CPU constants ; utilise légèrement plus de RAM.", "tn": "Ywakef el scanner RAM mel background. Ywaffar CPU ; yesta3mel chwaya akther RAM.", "es": "Detiene el escáner de RAM en segundo plano. Ahorra ciclos de CPU constantes; usa un poco más de RAM.", "de": "Stoppt den RAM-Hintergrundscanner. Spart konstante CPU-Zyklen; nutzt etwas mehr RAM.", "ar": "يوقف ماسح RAM في الخلفية. يوفر دورات معالج ثابتة؛ يستخدم ذاكرة أكثر قليلاً."},
    "Lock Kernel & Drivers in RAM": {"en": "Sets DisablePagingExecutive=1 so the NT kernel and core drivers never get paged to disk. Eliminates micro-stutters from kernel page faults. Needs 8GB+ RAM.", "fr": "Le noyau NT et les pilotes restent en RAM. Élimine les micro-saccades. Nécessite 8 Go+ de RAM.", "tn": "El noyau NT w les drivers yab9aw fel RAM. Yna77i el micro-stutters. Lazem 8 Go+ RAM.", "es": "El kernel NT y drivers se quedan en RAM. Elimina micro-tirones por fallos de página. Requiere 8GB+ RAM.", "de": "NT-Kernel und Treiber bleiben im RAM. Eliminiert Mikro-Ruckler durch Kernel-Seitenfehler. Erfordert 8GB+ RAM.", "ar": "يبقي نواة NT والتعريفات في RAM. يزيل التقطعات الدقيقة. يحتاج 8 جيجا+ RAM."},
    "Optimize Win32 CPU Scheduling": {"en": "Sets Win32PrioritySeparation to 0x26: short, variable quantum with 3:1 foreground boost. Your active window gets triple the CPU time of background apps.", "fr": "Quantum court et variable avec boost 3:1 pour la fenêtre active. Triple le temps CPU du premier plan.", "tn": "Quantum court w variable m3a boost 3:1 lel fenetre active. 3x temps CPU lel foreground.", "es": "Quantum corto y variable con boost 3:1 para ventana activa. Triple de tiempo CPU para primer plano.", "de": "Kurzes, variables Quantum mit 3:1 Vordergrund-Boost. Aktives Fenster bekommt dreifache CPU-Zeit.", "ar": "يضبط الجدولة بنسبة 3:1 للنافذة النشطة. تحصل على ثلاثة أضعاف وقت المعالج."},
    "Disable CFG (Control Flow Guard)": {"en": "Disables Control Flow Guard (CFG) system-wide. Removes overhead from every function call in protected processes. Note: CET (Shadow Stack) is a separate setting. 1-3% gain in CPU-heavy DX11 titles.", "fr": "Désactive CFG. Supprime la surcharge de chaque appel de fonction. Gain de 1-3% en DX11.", "tn": "Ytaffi CFG. Yna77i el overhead men kol appel de fonction. 1-3% gain fi DX11.", "es": "Desactiva CFG. Elimina sobrecarga de cada llamada a función. Ganancia de 1-3% en DX11.", "de": "Deaktiviert CFG systemweit. Entfernt Overhead bei jedem Funktionsaufruf. 1-3% Gewinn in DX11-Titeln.", "ar": "يعطّل CFG. يزيل العبء من كل استدعاء دالة. مكسب 1-3% في ألعاب DX11."},
    "Disable Memory Compression": {"en": "Stops Windows from compressing RAM. Reduces CPU overhead and latency when accessing memory, at the cost of slightly higher RAM usage.", "fr": "Arrête la compression RAM. Réduit la surcharge CPU et la latence d'accès mémoire.", "tn": "Ywakef compression el RAM. Y9allel el overhead taa3 CPU w latency.", "es": "Detiene la compresión de RAM. Reduce la sobrecarga de CPU y latencia de acceso a memoria.", "de": "Stoppt RAM-Komprimierung. Reduziert CPU-Overhead und Speicherzugriffs-Latenz.", "ar": "يوقف ضغط الذاكرة. يقلل عبء المعالج وتأخر الوصول للذاكرة."},
    "Disable Fault Tolerant Heap (FTH)": {"en": "FTH monitors app crashes and applies mitigations that can severely degrade performance of games that crash occasionally.", "fr": "FTH surveille les crashs et applique des mitigations qui dégradent les performances des jeux.", "tn": "FTH yraqeb les crashs w y7ot mitigations eli tzid tbatti les jeux.", "es": "FTH monitorea crashes y aplica mitigaciones que degradan el rendimiento de juegos.", "de": "FTH überwacht App-Abstürze und wendet Maßnahmen an, die Spiele stark verlangsamen können.", "ar": "FTH يراقب أعطال التطبيقات ويطبّق تخفيفات تضعف أداء الألعاب."},
    "Disable UAC (User Account Control)": {"en": "Completely disables UAC prompts and virtualization. Removes the secure desktop transition overhead. HIGH RISK for security.", "fr": "Désactive complètement UAC. Supprime la transition bureau sécurisé. RISQUE ÉLEVÉ.", "tn": "Ytaffi UAC kamla. Yna77i la transition secure desktop. RISQUE 3ALI.", "es": "Desactiva UAC completamente. Elimina la transición de escritorio seguro. ALTO RIESGO.", "de": "Deaktiviert UAC komplett. Entfernt den sicheren Desktop-Übergang. HOHES RISIKO.", "ar": "يعطّل UAC بالكامل. يزيل تحويل سطح المكتب الآمن. خطر عالي."},
    "Disable DEP (Data Execution Prevention)": {"en": "Disables DEP globally. Removes hardware-level memory execution checks. Extreme security risk, but removes a layer of memory validation.", "fr": "Désactive DEP globalement. Supprime les vérifications d'exécution mémoire. Risque extrême.", "tn": "Ytaffi DEP. Yna77i les verifications memoire. Risque extreme.", "es": "Desactiva DEP globalmente. Elimina verificaciones de ejecución de memoria. Riesgo extremo.", "de": "Deaktiviert DEP global. Entfernt Hardware-Speicherausführungsprüfungen. Extremes Risiko.", "ar": "يعطّل DEP. يزيل فحوصات تنفيذ الذاكرة. خطر شديد."},
    "Disable ASLR (Address Space Layout Randomization)": {"en": "Forces memory to load at predictable addresses. Can slightly improve load times and CPU cache hits. Extreme security risk.", "fr": "Force le chargement mémoire à des adresses prévisibles. Risque de sécurité extrême.", "tn": "Yforci el memoire t7ot fi adresses previsibles. Risque extreme lel securite.", "es": "Carga la memoria en direcciones predecibles. Riesgo de seguridad extremo.", "de": "Lädt Speicher an vorhersagbare Adressen. Extremes Sicherheitsrisiko.", "ar": "يحمّل الذاكرة في عناوين متوقعة. خطر أمني شديد."},
    "Disable System Restore": {"en": "Turns off System Restore entirely. Frees up disk space and removes background snapshotting I/O.", "fr": "Désactive la restauration système. Libère de l'espace disque et supprime les snapshots en arrière-plan.", "tn": "Ytaffi la restauration systeme. Yfarregh el disque w yna77i les snapshots.", "es": "Desactiva Restaurar Sistema. Libera espacio y elimina E/S de snapshots.", "de": "Deaktiviert Systemwiederherstellung. Gibt Speicherplatz frei und entfernt Snapshot-I/O.", "ar": "يعطّل استعادة النظام. يحرر مساحة القرص ويزيل عمليات اللقطات."},
    "Disable SEHOP (Exception Chain Validation)": {"en": "Disables Structured Exception Handling Overwrite Protection. Removes a security check on every exception thrown by applications. Good for raw performance.", "fr": "Désactive SEHOP. Supprime une vérification de sécurité sur chaque exception.", "tn": "Ytaffi SEHOP. Yna77i verification securite 3la kol exception.", "es": "Desactiva SEHOP. Elimina verificación de seguridad en cada excepción.", "de": "Deaktiviert SEHOP. Entfernt eine Sicherheitsprüfung bei jeder Ausnahme.", "ar": "يعطّل SEHOP. يزيل فحص أمني عند كل استثناء."},
    "Disable Prefetcher & Superfetch (Registry)": {"en": "Hard-disables the memory prefetcher at the kernel level. Essential for SSDs to prevent unnecessary write cycles and CPU overhead.", "fr": "Désactive le prefetcher mémoire au niveau noyau. Essentiel pour SSD.", "tn": "Ytaffi el prefetcher memoire fi kernel. Lazem lel SSD.", "es": "Desactiva el prefetcher de memoria a nivel kernel. Esencial para SSDs.", "de": "Deaktiviert den Speicher-Prefetcher auf Kernel-Ebene. Essentiell für SSDs.", "ar": "يعطّل prefetcher الذاكرة على مستوى النواة. ضروري لأقراص SSD."},
    "Force Disable Fullscreen Optimizations (Global)": {"en": "Prevents Windows from forcing pseudo-borderless mode on classic exclusive fullscreen games. Fixes micro-stutter. Conflicts with 'Force True Exclusive Fullscreen'.", "fr": "Empêche Windows de forcer le mode sans bordure. Corrige les micro-saccades.", "tn": "Ymanea Windows men forcer borderless mode. Ysalla7 el micro-stutters.", "es": "Evita que Windows fuerce modo sin bordes. Corrige micro-tirones.", "de": "Verhindert, dass Windows randloses Fenster erzwingt. Behebt Mikro-Ruckler.", "ar": "يمنع Windows من فرض وضع بلا حدود. يصلح التقطعات الدقيقة."},
    "Disable Monitor VSync Override (Legacy)": {"en": "Disables the undocumented MonitorVsync registry override under GraphicsDrivers. Legacy setting – may have no effect on modern WDDM 2.x+ drivers.", "fr": "Désactive le remplacement VSync du moniteur. Ancien paramètre, peu d'effet sur les pilotes modernes.", "tn": "Ytaffi el VSync override taa3 el moniteur. Parametre 9dim, ma ya3melch barcha 3al drivers jdoud.", "es": "Desactiva la anulación VSync del monitor. Ajuste legacy, poco efecto en drivers modernos.", "de": "Deaktiviert das VSync-Override des Monitors. Legacy-Einstellung, wenig Wirkung bei modernen Treibern.", "ar": "يعطّل تجاوز VSync للشاشة. إعداد قديم، قد لا يؤثر على التعريفات الحديثة."},
    "Disable GPU Preemption": {"en": "Tells the WDDM scheduler not to interrupt the GPU mid-frame. Frame-time variance drops 20-40%. Especially impactful in DX11.", "fr": "Le planificateur WDDM n'interrompt plus le GPU en plein frame. Variance réduite de 20-40%.", "tn": "WDDM ma y9ata3ch el GPU fi wesot el frame. Variance tan9os 20-40%.", "es": "El programador WDDM no interrumpe la GPU a mitad de frame. Varianza baja 20-40%.", "de": "WDDM-Scheduler unterbricht die GPU nicht mehr mitten im Frame. Varianz sinkt 20-40%.", "ar": "يمنع مجدول WDDM من مقاطعة GPU أثناء الإطار. تنخفض التباينات 20-40%."},
    "Force True Exclusive Fullscreen": {"en": "Disables SwapEffectUpgradeEnable so Windows cannot hijack your game into flip-model DWM composition. Saves 1 frame of latency. Conflicts with 'Force Disable Fullscreen Optimizations'.", "fr": "Empêche Windows de détourner votre jeu vers la composition DWM. Économise 1 frame de latence.", "tn": "Ymanea Windows men ykhattef el jeu lel DWM composition. Ywaffar 1 frame latence.", "es": "Evita que Windows secuestre tu juego al modo DWM. Ahorra 1 frame de latencia.", "de": "Verhindert, dass Windows das Spiel in DWM-Komposition umleitet. Spart 1 Frame Latenz.", "ar": "يمنع Windows من اختطاف لعبتك إلى تركيب DWM. يوفر إطاراً واحداً من التأخير."},
    "Disable Game DVR & Game Bar": {"en": "Kills background GPU recording, screenshot overlay, and FPS counter. Known to cause stuttering even when not actively recording.", "fr": "Supprime l'enregistrement GPU en arrière-plan et la barre de jeu. Cause des saccades même inactif.", "tn": "Yna77i l'enregistrement GPU mel background w la barre de jeu. Ysabbeb stuttering 7atta kan mch actif.", "es": "Elimina grabación GPU en segundo plano y barra de juego. Causa tirones incluso sin grabar.", "de": "Beendet GPU-Hintergrundaufnahme und Game Bar. Verursacht Ruckler auch ohne aktive Aufnahme.", "ar": "يحذف تسجيل GPU في الخلفية وشريط اللعبة. يسبب تقطعات حتى بدون تسجيل."},
    "Enable HW Accelerated GPU Scheduling": {"en": "Lets the GPU manage its own VRAM scheduling instead of going through Windows. Reduces latency on NVIDIA 10-series+ / AMD 5000+.", "fr": "Le GPU gère son propre ordonnancement VRAM. Réduit la latence sur NVIDIA 10+ / AMD 5000+.", "tn": "El GPU ydabber VRAM wa7dou bla Windows. Y9allel latence 3la NVIDIA 10+ / AMD 5000+.", "es": "La GPU gestiona su propia VRAM sin Windows. Reduce latencia en NVIDIA 10+ / AMD 5000+.", "de": "GPU verwaltet eigenes VRAM-Scheduling ohne Windows. Reduziert Latenz bei NVIDIA 10+ / AMD 5000+.", "ar": "يتيح لـ GPU إدارة جدولة VRAM بدون Windows. يقلل التأخير على NVIDIA 10+ / AMD 5000+."},
    "Increase GPU TDR Timeout to 60s": {"en": "Prevents false 'display driver stopped responding' crashes during heavy shader compilation or ray tracing scenes. Default is only 2 seconds.", "fr": "Empêche les faux crashs 'pilote d'affichage ne répond plus' pendant la compilation de shaders.", "tn": "Ymanea les faux crashs 'driver ma yjawebch' w9t shader compilation.", "es": "Evita crashs falsos de 'driver de pantalla no responde' durante compilación de shaders.", "de": "Verhindert falsche 'Anzeigetreiber reagiert nicht'-Abstürze bei Shader-Kompilierung.", "ar": "يمنع أعطال 'تعريف العرض توقف عن الاستجابة' الزائفة أثناء تجميع الشيدرات."},
    "Force NVIDIA P-State P0 (Max Clocks)": {"en": "Disables dynamic P-State switching. GPU stays at max clocks, eliminating 10-50ms transition hitches. Higher idle power draw.", "fr": "Désactive le changement dynamique de P-State. GPU reste aux fréquences max.", "tn": "Ytaffi el P-State dynamique. GPU yab9a 3la max frequences.", "es": "Desactiva cambio dinámico de P-State. GPU se queda en frecuencias máximas.", "de": "Deaktiviert dynamisches P-State-Switching. GPU bleibt auf Max-Takt.", "ar": "يعطّل تبديل P-State الديناميكي. تبقى GPU على أقصى تردد."},
    "MMCSS Game Task Max Priority": {"en": "Sets GPU Priority=8, Priority=6, Scheduling=High, SFIO=High for the Games MMCSS task. Maximum scheduling priority when Windows detects a game running.", "fr": "Priorité maximale d'ordonnancement MMCSS quand Windows détecte un jeu.", "tn": "Priorite maximale MMCSS ki Windows y7oss 3la jeu.", "es": "Prioridad máxima MMCSS cuando Windows detecta un juego.", "de": "Maximale MMCSS-Scheduling-Priorität wenn Windows ein Spiel erkennt.", "ar": "أقصى أولوية جدولة MMCSS عندما يكتشف Windows لعبة."},
    "Disable Multi-Plane Overlay (MPO)": {"en": "Fixes stuttering, black screens, and flickering on NVIDIA/AMD GPUs by disabling MPO. Forces standard DWM composition.", "fr": "Corrige les saccades et écrans noirs en désactivant MPO. Force la composition DWM standard.", "tn": "Ysalla7 el stuttering w ecrans noirs b desactivation MPO.", "es": "Corrige tirones y pantallas negras desactivando MPO.", "de": "Behebt Ruckler und Schwarzbilder durch Deaktivierung von MPO.", "ar": "يصلح التقطعات والشاشات السوداء بتعطيل MPO."},
    "Disable Variable Refresh Rate (VRR) Globally": {"en": "Disables Windows-level VRR which can conflict with G-Sync/FreeSync and cause micro-stutters in windowed games.", "fr": "Désactive VRR Windows qui peut confliter avec G-Sync/FreeSync.", "tn": "Ytaffi VRR Windows eli y9adder yconfliqi m3a G-Sync/FreeSync.", "es": "Desactiva VRR de Windows que puede conflictuar con G-Sync/FreeSync.", "de": "Deaktiviert Windows-VRR, das mit G-Sync/FreeSync kollidieren kann.", "ar": "يعطّل VRR على مستوى Windows الذي قد يتعارض مع G-Sync/FreeSync."},
    "Disable GPU Energy Driver": {"en": "Disables the GPU Energy Driver service which constantly polls the GPU for power metrics, causing DPC latency spikes. Skips gracefully if the service doesn't exist.", "fr": "Désactive le pilote d'énergie GPU qui sonde constamment le GPU. Ignoré si le service n'existe pas.", "tn": "Ytaffi el GPU Energy Driver eli y7awwel el GPU. Yetjawez kan ma mawjoudch.", "es": "Desactiva el driver de energía GPU que consulta constantemente la GPU.", "de": "Deaktiviert den GPU Energy Driver, der ständig GPU-Leistungsdaten abfragt.", "ar": "يعطّل تعريف طاقة GPU الذي يستقصي GPU باستمرار."},
    "Disable Xbox Game Monitoring": {"en": "Stops the Xbox Game Monitoring service from hooking into game processes. Note: service was removed on Win10 2004+; harmless if not present.", "fr": "Arrête la surveillance Xbox des processus de jeu. Supprimé depuis Win10 2004+.", "tn": "Ywakef Xbox Game Monitoring. Tna77at men Win10 2004+.", "es": "Detiene la monitorización Xbox de procesos de juego. Eliminado desde Win10 2004+.", "de": "Stoppt Xbox Game Monitoring. Seit Win10 2004+ entfernt.", "ar": "يوقف مراقبة ألعاب Xbox. أُزيل من Win10 2004+."},
    "Disable Game Bar Presence Writer": {"en": "Prevents the Game Bar from writing presence data to the registry every time a game is launched.", "fr": "Empêche la Game Bar d'écrire des données de présence à chaque lancement de jeu.", "tn": "Ymanea Game Bar mel ecriture donnees de presence kol ma tlanci jeu.", "es": "Evita que Game Bar escriba datos de presencia al iniciar cada juego.", "de": "Verhindert, dass die Game Bar bei jedem Spielstart Präsenzdaten schreibt.", "ar": "يمنع Game Bar من كتابة بيانات الحضور عند تشغيل كل لعبة."},
    "Disable Windows Ink Workspace": {"en": "Disables Windows Ink. Crucial for osu! and FPS players to remove pen/tablet input processing overhead from raw mouse input.", "fr": "Désactive Windows Ink. Crucial pour les joueurs FPS pour supprimer les traitements stylet/tablette.", "tn": "Ytaffi Windows Ink. Mohemm lel FPS players bech yna77i traitement stylet/tablette.", "es": "Desactiva Windows Ink. Crucial para jugadores FPS para eliminar procesamiento de tableta.", "de": "Deaktiviert Windows Ink. Entscheidend für FPS-Spieler zur Entfernung von Stift-/Tablet-Overhead.", "ar": "يعطّل Windows Ink. مهم للاعبي FPS لإزالة معالجة إدخال القلم/الجهاز اللوحي."},
    "Disable DWM Ghosting / Composition (Legacy)": {"en": "Disables DWM composition animations. Note: HungAppTimeout is handled by the 'Faster Shutdown Timeouts' tweak. Does not disable window ghosting (that requires a Win32 API call).", "fr": "Désactive les animations de composition DWM. HungAppTimeout est géré par le tweak 'Délais d'arrêt rapides'.", "tn": "Ytaffi animations DWM. HungAppTimeout yetgera b tweak 'delais d'arret rapides'.", "es": "Desactiva animaciones de composición DWM. HungAppTimeout se gestiona por otro tweak.", "de": "Deaktiviert DWM-Kompositionsanimationen. HungAppTimeout wird vom Tweak 'Schnellere Shutdown-Timeouts' behandelt.", "ar": "يعطّل رسوم DWM المتحركة. يُدار HungAppTimeout بواسطة تعديل آخر."},
    "Disable Dynamic Tick": {"en": "Stops Windows from collapsing the system timer when CPU idles. Yields rock-solid frame pacing. Laptops: increases power draw when idle.", "fr": "Empêche Windows de réduire le minuteur système quand le CPU est inactif. Cadence d'images stable.", "tn": "Ymanea Windows men y9allel el minuteur sistem ki CPU farge. Frame pacing stable.", "es": "Evita que Windows colapse el temporizador cuando CPU está inactivo. Pacing de frames estable.", "de": "Stoppt Windows daran, den Timer im Leerlauf zu reduzieren. Stabiles Frame-Pacing.", "ar": "يمنع Windows من تقليص المؤقت عند خمول المعالج. وتيرة إطارات ثابتة."},
    "Force CPU TSC Timer (Remove HPET)": {"en": "Deletes useplatformclock/useplatformtick from BCD so your board falls back to the much faster CPU Time Stamp Counter.", "fr": "Supprime les horloges plateforme du BCD pour revenir au compteur TSC du CPU, bien plus rapide.", "tn": "Yna77i les horloges plateforme mel BCD bech yerja3 lel TSC CPU, akther sar3a.", "es": "Elimina relojes de plataforma del BCD para volver al TSC de CPU, mucho más rápido.", "de": "Entfernt Plattform-Uhren aus BCD und fällt auf den schnelleren CPU TSC zurück.", "ar": "يحذف ساعات المنصة من BCD للعودة إلى عداد TSC الأسرع."},
    "Enable Global Timer Resolution Requests": {"en": "Win11 22H2+ broke background timer requests. This restores old behavior so any app requesting 0.5ms resolution gets it system-wide.", "fr": "Win11 22H2+ a cassé les requêtes de minuteur. Restaure l'ancien comportement.", "tn": "Win11 22H2+ kassar les requetes minuteur. Yerja3 el comportement el 9dim.", "es": "Win11 22H2+ rompió solicitudes de temporizador. Restaura el comportamiento anterior.", "de": "Win11 22H2+ hat Timer-Anfragen kaputt gemacht. Stellt altes Verhalten wieder her.", "ar": "Win11 22H2+ أفسد طلبات المؤقت. يستعيد السلوك القديم."},
    "Enhanced TSC Sync Policy (Multi-CCX AMD)": {"en": "Forces tighter TSC synchronization between chiplets on Ryzen 3000+. Fixes timer drift that causes inconsistent frame times.", "fr": "Synchronisation TSC plus serrée entre chiplets sur Ryzen 3000+. Corrige la dérive du minuteur.", "tn": "Synchronisation TSC akther serra bin chiplets 3la Ryzen 3000+. Ysalla7 el derive taa3 minuteur.", "es": "Sincronización TSC más estrecha entre chiplets en Ryzen 3000+. Corrige deriva del temporizador.", "de": "Engere TSC-Synchronisation zwischen Chiplets auf Ryzen 3000+. Behebt Timer-Drift.", "ar": "مزامنة TSC أدق بين الشرائح على Ryzen 3000+. يصلح انحراف المؤقت."},
    "Set Boot Timeout to 0": {"en": "Removes the OS selection menu delay. Saves 30 seconds on every boot if you only have one OS installed.", "fr": "Supprime le délai du menu de sélection OS. Économise 30 secondes à chaque démarrage.", "tn": "Yna77i el delai taa3 menu selection OS. Ywaffar 30 secondes kol demarrage.", "es": "Elimina el retraso del menú de selección de SO. Ahorra 30 segundos en cada arranque.", "de": "Entfernt die OS-Auswahlmenü-Verzögerung. Spart 30 Sekunden bei jedem Start.", "ar": "يزيل تأخير قائمة اختيار نظام التشغيل. يوفر 30 ثانية في كل إقلاع."},
    "Disable Nagle's Algorithm (All Interfaces)": {"en": "Nagle batches small packets together adding up to 200ms latency. TcpNoDelay=1 + TcpAckFrequency=1 sends every packet immediately.", "fr": "Nagle regroupe les petits paquets ajoutant jusqu'à 200ms. TcpNoDelay=1 envoie immédiatement.", "tn": "Nagle yjmaa les paquets sghira w yzid 200ms latence. TcpNoDelay=1 yba3eth to7a.", "es": "Nagle agrupa paquetes pequeños sumando hasta 200ms. TcpNoDelay=1 envía inmediatamente.", "de": "Nagle bündelt kleine Pakete und fügt bis zu 200ms Latenz hinzu. TcpNoDelay=1 sendet sofort.", "ar": "Nagle يجمع الحزم الصغيرة ويضيف حتى 200 مللي ثانية تأخير. TcpNoDelay=1 يرسل فوراً."},
    "Disable Network Throttling Index": {"en": "Windows limits non-multimedia network traffic to ~10 packets/ms. Setting 0xFFFFFFFF removes the cap entirely.", "fr": "Windows limite le trafic réseau non-multimédia. 0xFFFFFFFF supprime la limite.", "tn": "Windows y7odded el trafic reseau. 0xFFFFFFFF yna77i el limite.", "es": "Windows limita el tráfico de red no multimedia. 0xFFFFFFFF elimina el límite.", "de": "Windows begrenzt Nicht-Multimedia-Netzwerkverkehr. 0xFFFFFFFF entfernt das Limit.", "ar": "Windows يحدّ حركة الشبكة. 0xFFFFFFFF يزيل الحد بالكامل."},
    "Set SystemResponsiveness to 0%": {"en": "Default 20 reserves 20% CPU for background. Setting 0 (Windows internally treats as 10) minimizes CPU reserved for background tasks to ~10%.", "fr": "Par défaut, 20% CPU réservé au système. 0 réduit à ~10% pour les tâches de fond.", "tn": "Par defaut 20% CPU reserve. 0 y9allel lel ~10% lel taches de fond.", "es": "Por defecto 20% CPU reservado. 0 minimiza a ~10% para tareas de fondo.", "de": "Standard reserviert 20% CPU. 0 minimiert auf ~10% für Hintergrundaufgaben.", "ar": "الافتراضي يحجز 20% للمعالج. 0 يقلل إلى ~10% للمهام الخلفية."},
    "Enable RSS, Disable Heuristics": {"en": "Receive Side Scaling distributes NIC processing across cores. Heuristics override your tuning — disable them.", "fr": "RSS distribue le traitement NIC. Les heuristiques écrasent vos réglages.", "tn": "RSS ywazzea traitement NIC 3la les coeurs. Heuristiques yecraseou reglages.", "es": "RSS distribuye procesamiento NIC. Heurísticas anulan tu configuración.", "de": "RSS verteilt NIC-Verarbeitung. Heuristiken überschreiben Ihre Einstellungen.", "ar": "RSS يوزع معالجة بطاقة الشبكة. DCA يتجاوز RAM. الاستدلال يتجاوز إعداداتك."},
    "Disable TCP Timestamps & ECN": {"en": "Timestamps add 12 bytes per packet. ECN adds per-packet CPU processing. Both negligible benefits for gaming but measurable overhead.", "fr": "Les timestamps ajoutent 12 octets par paquet. ECN ajoute du traitement CPU. Peu de bénéfice pour le gaming.", "tn": "Timestamps tzid 12 octets kol paquet. ECN tzid traitement CPU. Ma ya3mlouch barcha lel gaming.", "es": "Timestamps añaden 12 bytes por paquete. ECN añade procesamiento CPU. Poco beneficio para juegos.", "de": "Zeitstempel fügen 12 Bytes pro Paket hinzu. ECN fügt CPU-Verarbeitung hinzu. Wenig Nutzen für Gaming.", "ar": "الطوابع الزمنية تضيف 12 بايت لكل حزمة. ECN يضيف معالجة CPU. فائدة قليلة للألعاب."},
    "Enable TCP Fast Open": {"en": "Allows data in the SYN packet for faster connection establishment. Reduces handshake round trips.", "fr": "Permet les données dans le paquet SYN pour un établissement de connexion plus rapide.", "tn": "Ysma7 b donnees fil paquet SYN bech connexion ta9oum asra3.", "es": "Permite datos en el paquete SYN para conexión más rápida.", "de": "Erlaubt Daten im SYN-Paket für schnelleren Verbindungsaufbau.", "ar": "يسمح بالبيانات في حزمة SYN لإنشاء اتصال أسرع."},
    "Set TCP Congestion Control to CUBIC": {"en": "Changes the TCP congestion provider to CUBIC. Already default on Win10 1709+. Better for high-speed, low-latency connections.", "fr": "Change le fournisseur de congestion TCP en CUBIC. Par défaut depuis Win10 1709+.", "tn": "Ybaddel el TCP congestion l CUBIC. Par defaut men Win10 1709+.", "es": "Cambia el proveedor de congestión TCP a CUBIC. Por defecto desde Win10 1709+.", "de": "Ändert TCP-Staukontrolle auf CUBIC. Bereits Standard ab Win10 1709+.", "ar": "يغير مزود ازدحام TCP إلى CUBIC. الافتراضي من Win10 1709+."},
    "Disable IPv6 Tunneling (Teredo, ISATAP, 6to4)": {"en": "Disables legacy IPv6 transition technologies that constantly poll the network and create unnecessary virtual adapters.", "fr": "Désactive les technologies de transition IPv6 qui sondent constamment le réseau.", "tn": "Ytaffi les technologies transition IPv6 eli ysondou el reseau.", "es": "Desactiva tecnologías de transición IPv6 que consultan constantemente la red.", "de": "Deaktiviert IPv6-Übergangstechnologien, die ständig das Netzwerk abfragen.", "ar": "يعطّل تقنيات انتقال IPv6 التي تستقصي الشبكة باستمرار."},
    "Disable WMM (Wi-Fi Multimedia) Power Save": {"en": "Stops the Wi-Fi adapter from entering low-power states between packet bursts. Crucial for stable wireless ping.", "fr": "Empêche l'adaptateur Wi-Fi de passer en mode économie entre les rafales de paquets.", "tn": "Ymanea el Wi-Fi adapter men mode economie bin el rafales. Mohemm lel ping stable.", "es": "Evita que el adaptador Wi-Fi entre en ahorro de energía. Crucial para ping estable.", "de": "Stoppt den WLAN-Adapter vor Energiesparmodus zwischen Paket-Bursts. Wichtig für stabilen Ping.", "ar": "يمنع محول Wi-Fi من دخول وضع الطاقة المنخفضة. مهم لبينغ مستقر."},
    "Disable Large Send Offload (LSO)": {"en": "LSO offloads TCP segmentation to NIC hardware, but many drivers implement it poorly causing high latency and packet loss.", "fr": "LSO décharge la segmentation TCP mais beaucoup de drivers l'implémentent mal.", "tn": "LSO yfarregh segmentation TCP lel NIC ama barcha drivers ma y7ottelhach behi.", "es": "LSO descarga la segmentación TCP pero muchos drivers lo implementan mal.", "de": "LSO verlagert TCP-Segmentierung auf NIC-Hardware, aber viele Treiber implementieren es schlecht.", "ar": "LSO ينقل تجزئة TCP لبطاقة الشبكة لكن كثير من التعريفات تطبّقه بشكل سيء."},
    "Optimize TCP Port & Timeout Parameters": {"en": "MaxUserPort=65534, TcpTimedWaitDelay=30s, MaxFreeTcbs/MaxHashTableSize=65536. Prevents port exhaustion and speeds up port recycling.", "fr": "MaxUserPort=65534, TcpTimedWaitDelay=30s. Empêche l'épuisement des ports.", "tn": "MaxUserPort=65534, delai=30s. Ymanea l'epuisement taa3 les ports.", "es": "MaxUserPort=65534, TcpTimedWaitDelay=30s. Evita agotamiento de puertos.", "de": "MaxUserPort=65534, TcpTimedWaitDelay=30s. Verhindert Port-Erschöpfung.", "ar": "MaxUserPort=65534, TcpTimedWaitDelay=30s. يمنع نفاد المنافذ ويسرّع إعادة التدوير."},
    "Optimize DNS Cache (24h / 5s negative)": {"en": "Caches valid DNS entries for 24h (fewer lookups), but retries failed ones after just 5 seconds. Best of both worlds.", "fr": "Cache DNS valide 24h, réessaie les échecs après 5s. Le meilleur des deux mondes.", "tn": "Cache DNS valide 24h, y3awed les echecs ba3d 5s.", "es": "Cachea DNS válido 24h, reintenta fallos después de 5s.", "de": "Cachet gültige DNS-Einträge 24h, wiederholt Fehler nach 5s.", "ar": "يخزّن DNS الصالح لمدة 24 ساعة، يعيد المحاولة بعد 5 ثوانٍ."},
    "Increase SMB IRPStackSize & Buffer": {"en": "Increases I/O Request Packet stack to 30 and receive buffer to 17424 for faster file sharing and network drive access.", "fr": "Augmente la pile IRP à 30 et le buffer à 17424 pour un partage de fichiers plus rapide.", "tn": "Yzid pile IRP l 30 w buffer l 17424 lel partage fichiers asra3.", "es": "Aumenta pila IRP a 30 y buffer a 17424 para compartir archivos más rápido.", "de": "Erhöht IRP-Stapel auf 30 und Puffer auf 17424 für schnelleren Dateitransfer.", "ar": "يزيد مكدس IRP إلى 30 والتخزين المؤقت إلى 17424 لمشاركة أسرع."},
    "Disable Energy Efficient Ethernet (EEE)": {"en": "EEE puts the NIC PHY into low-power idle between traffic bursts. Waking it adds 2-5ms latency on every burst. Huge for consistent ping.", "fr": "EEE met le NIC en veille entre les rafales. Le réveil ajoute 2-5ms. Énorme pour un ping stable.", "tn": "EEE y7ot el NIC en veille bin el rafales. Reveil yzid 2-5ms. Mohemm lel ping.", "es": "EEE pone la NIC en reposo entre ráfagas. Despertar añade 2-5ms. Enorme para ping estable.", "de": "EEE versetzt NIC in Schlafmodus zwischen Bursts. Aufwachen fügt 2-5ms hinzu. Wichtig für Ping.", "ar": "EEE يضع بطاقة الشبكة في سكون. الاستيقاظ يضيف 2-5 مللي ثانية. مهم لبينغ ثابت."},
    "Disable IPv6 Completely": {"en": "Disables the IPv6 stack. If your ISP or game doesn't require IPv6, this removes a massive amount of background network polling.", "fr": "Désactive IPv6. Si votre FAI ne nécessite pas IPv6, supprime beaucoup de trafic réseau.", "tn": "Ytaffi IPv6. Kan FAI wella jeu ma y7tajouhaech, yna77i barcha trafic reseau.", "es": "Desactiva IPv6. Si tu ISP no lo requiere, elimina mucho tráfico de red.", "de": "Deaktiviert IPv6. Entfernt viel Hintergrund-Netzwerkverkehr wenn nicht benötigt.", "ar": "يعطّل IPv6. يزيل كمية كبيرة من استقصاء الشبكة إذا لم يكن مطلوباً."},
    "Disable QoS Packet Scheduler": {"en": "Sets the QoS non-best-effort bandwidth limit to zero. Only affects traffic tagged with QoS policies (rare on consumer PCs). The '20% reserved bandwidth' myth is debunked.", "fr": "Limite QoS à zéro. Le mythe des '20% de bande passante réservée' est démystifié.", "tn": "Limite QoS l zero. El mythe taa3 '20% bande passante reservee' faux.", "es": "Límite QoS a cero. El mito del '20% de ancho de banda reservado' es falso.", "de": "QoS-Bandbreitenlimit auf Null. Der '20% reservierte Bandbreite'-Mythos ist widerlegt.", "ar": "يضع حد QoS على صفر. خرافة '20% نطاق ترددي محجوز' خاطئة."},
    "Disable Receive Segment Coalescing (RSC)": {"en": "RSC batches incoming packets. Good for throughput, terrible for latency. Disabling it forces immediate packet processing.", "fr": "RSC regroupe les paquets entrants. Bon pour le débit, mauvais pour la latence.", "tn": "RSC yjmaa les paquets. Behi lel debit, khayeb lel latence.", "es": "RSC agrupa paquetes. Bueno para throughput, malo para latencia.", "de": "RSC bündelt eingehende Pakete. Gut für Durchsatz, schlecht für Latenz.", "ar": "RSC يجمع الحزم الواردة. جيد للإنتاجية، سيء للتأخير."},
    "Disable NetBIOS over TCP/IP": {"en": "Disables legacy local network discovery protocols that constantly broadcast packets on your LAN.", "fr": "Désactive les protocoles de découverte réseau local qui diffusent constamment des paquets.", "tn": "Ytaffi les protocoles decouverte reseau local eli ywazzaou paquets.", "es": "Desactiva protocolos de descubrimiento de red local que envían broadcast constantemente.", "de": "Deaktiviert Legacy-Netzwerkerkennungsprotokolle, die ständig Pakete senden.", "ar": "يعطّل بروتوكولات اكتشاف الشبكة المحلية التي تبث حزماً باستمرار."},
    "Disable LLMNR (Link-Local Multicast)": {"en": "Disables LLMNR, another legacy local name resolution protocol that generates unnecessary broadcast traffic.", "fr": "Désactive LLMNR, un protocole de résolution de noms local générant du trafic inutile.", "tn": "Ytaffi LLMNR, protocole resolution noms local eli ywalled trafic fadhel.", "es": "Desactiva LLMNR, protocolo de resolución de nombres que genera tráfico innecesario.", "de": "Deaktiviert LLMNR, ein Legacy-Protokoll, das unnötigen Broadcast-Traffic erzeugt.", "ar": "يعطّل LLMNR، بروتوكول حل أسماء محلي يولّد حركة بث غير ضرورية."},
    "Disable Smart Name Resolution": {"en": "Stops Windows from sending DNS queries to all adapters simultaneously (which leaks DNS queries and wastes bandwidth).", "fr": "Empêche Windows d'envoyer des requêtes DNS à tous les adaptateurs simultanément.", "tn": "Ymanea Windows men yba3eth DNS queries lkol les adaptateurs fi nafes el wa9t.", "es": "Evita que Windows envíe consultas DNS a todos los adaptadores simultáneamente.", "de": "Stoppt Windows daran, DNS-Anfragen an alle Adapter gleichzeitig zu senden.", "ar": "يمنع Windows من إرسال استعلامات DNS لجميع المحولات في نفس الوقت."},
    "Activate Ultimate Performance Plan": {"en": "Hidden power plan that eliminates ALL power-saving delays. Duplicates the scheme and activates High Performance as fallback.", "fr": "Plan d'alimentation caché qui élimine tous les délais d'économie d'énergie.", "tn": "Plan d'alimentation makhfi eli yna77i kol les delais d'economie d'energie.", "es": "Plan de energía oculto que elimina todos los retrasos de ahorro de energía.", "de": "Versteckter Energieplan, der alle Energiespar-Verzögerungen eliminiert.", "ar": "خطة طاقة مخفية تزيل جميع تأخيرات توفير الطاقة."},
    "Unpark All CPU Cores (100% Min)": {"en": "Sets Core Parking minimum to 100% so no cores ever sleep. Eliminates hitching from cores waking up under sudden load.", "fr": "Aucun cœur ne dort. Élimine les saccades du réveil des cœurs sous charge soudaine.", "tn": "7atta coeur ma yor9ad. Yna77i el saccades ki coeur yfi9 bel charge.", "es": "Ningún núcleo duerme. Elimina tirones al despertar núcleos bajo carga repentina.", "de": "Kein Kern schläft. Eliminiert Ruckler beim Aufwachen unter plötzlicher Last.", "ar": "لا ينام أي نواة. يزيل التقطعات عند استيقاظ الأنوية تحت حمل مفاجئ."},
    "Disable Processor C-States (Idle Disable)": {"en": "Prevents CPU cores from entering C1/C3/C6 sleep states. Each state adds microseconds of wake latency. More heat but zero delay.", "fr": "Empêche les cœurs d'entrer en veille C1/C3/C6. Chaque état ajoute des microsecondes de latence.", "tn": "Ymanea les coeurs men somneil C1/C3/C6. Kol etat yzid microsecondes latence.", "es": "Evita que los núcleos entren en reposo C1/C3/C6. Cada estado añade microsegundos de latencia.", "de": "Verhindert C1/C3/C6-Schlafzustände. Jeder Zustand fügt Mikrosekunden Latenz hinzu.", "ar": "يمنع أنوية المعالج من دخول سكون C1/C3/C6. كل حالة تضيف ميكروثوانٍ تأخير."},
    "CPU Min/Max State = 100%": {"en": "Forces the processor to always run at maximum frequency. Eliminates frequency scaling delays entirely.", "fr": "Force le processeur à fonctionner à fréquence maximale. Élimine les délais de mise à l'échelle.", "tn": "Yforci el processeur ykhdem 3la frequence maximale. Yna77i kol les delais.", "es": "Fuerza al procesador a funcionar a frecuencia máxima. Elimina retrasos de escalado.", "de": "Zwingt den Prozessor auf maximale Frequenz. Eliminiert Frequenzskalierungs-Verzögerungen.", "ar": "يجبر المعالج على العمل بأقصى تردد. يزيل تأخيرات تغيير التردد."},
    "Aggressive Boost Mode + EPP = 0": {"en": "Sets boost to aggressive (ramp to max clock instantly) and Energy Performance Preference to 0 (pure performance).", "fr": "Boost agressif (fréquence max instantanée) et EPP à 0 (performance pure).", "tn": "Boost agressif (frequence max to7a) w EPP 0 (performance pure).", "es": "Boost agresivo (clock máximo instantáneo) y EPP a 0 (rendimiento puro).", "de": "Aggressiver Boost (sofort auf Max-Takt) und EPP auf 0 (reine Leistung).", "ar": "تعزيز عدواني (أقصى تردد فوري) و EPP عند 0 (أداء صرف)."},
    "Disable Power Throttling": {"en": "Windows 10+ throttles background apps to save power. This can cause stuttering if Windows mis-classifies your workload as background.", "fr": "Windows 10+ limite les applis en arrière-plan. Peut causer des saccades si mal classifié.", "tn": "Windows 10+ y7added les applis background. Y9adder ysabbeb stuttering kan yclassifihom ghalet.", "es": "Windows 10+ limita apps en segundo plano. Puede causar tirones si clasifica mal tu carga.", "de": "Windows 10+ drosselt Hintergrund-Apps. Kann Ruckler verursachen bei falscher Klassifizierung.", "ar": "Windows 10+ يخنق تطبيقات الخلفية. قد يسبب تقطعات إذا صُنّف حملك كخلفية."},
    "Disable USB Selective Suspend": {"en": "Stops Windows from powering down USB devices to save energy. Fixes random mouse/keyboard disconnects and 10ms input spikes.", "fr": "Empêche Windows de couper les appareils USB. Corrige les déconnexions souris/clavier aléatoires.", "tn": "Ymanea Windows men ytaffi les USB. Ysalla7 les deconnexions souris/clavier.", "es": "Evita que Windows apague dispositivos USB. Corrige desconexiones aleatorias de ratón/teclado.", "de": "Stoppt Windows daran, USB-Geräte abzuschalten. Behebt zufällige Maus-/Tastatur-Trennungen.", "ar": "يمنع Windows من إيقاف أجهزة USB. يصلح انفصال الماوس/لوحة المفاتيح العشوائي."},
    "Disable PCI Express ASPM": {"en": "Active State Power Management adds latency to PCIe link state transitions. Disabling keeps GPU/NVMe links always active.", "fr": "ASPM ajoute de la latence aux transitions d'état PCIe. Désactiver garde GPU/NVMe toujours actif.", "tn": "ASPM yzid latence lel transitions PCIe. Ytaffi y7olli GPU/NVMe toujours actif.", "es": "ASPM añade latencia a transiciones PCIe. Desactivar mantiene GPU/NVMe siempre activo.", "de": "ASPM fügt Latenz zu PCIe-Zustandsübergängen hinzu. Deaktivierung hält GPU/NVMe aktiv.", "ar": "ASPM يضيف تأخيراً لتحولات PCIe. تعطيله يبقي GPU/NVMe نشطاً دائماً."},
    "Disable Sleep & Display Timeout": {"en": "Prevents the PC and display from ever going to sleep automatically.", "fr": "Empêche le PC et l'écran de se mettre en veille automatiquement.", "tn": "Ymanea el PC w l'ecran men somneil automatique.", "es": "Evita que el PC y la pantalla entren en reposo automáticamente.", "de": "Verhindert, dass PC und Bildschirm automatisch in den Schlaf gehen.", "ar": "يمنع الكمبيوتر والشاشة من الدخول في سكون تلقائي."},
    "Disable Disk Sleep": {"en": "Prevents hard drives from spinning down. Eliminates the 3-5 second freeze when accessing a sleeping drive.", "fr": "Empêche les disques durs de s'arrêter. Élimine le gel de 3-5 secondes.", "tn": "Ymanea les disques men ywakfou. Yna77i el gel 3-5 secondes.", "es": "Evita que los discos se detengan. Elimina el congelamiento de 3-5 segundos.", "de": "Verhindert Festplatten-Stillstand. Eliminiert das 3-5 Sekunden Einfrieren.", "ar": "يمنع توقف الأقراص. يزيل التجمد لمدة 3-5 ثوانٍ."},
    "Disable Connected Standby (Modern Standby)": {"en": "Forces S3 sleep instead of S0ix. Prevents the PC from waking up in a backpack, draining battery, and running background tasks while 'asleep'.", "fr": "Force S3 au lieu de S0ix. Empêche le PC de se réveiller dans un sac.", "tn": "Yforci S3 blasa men S0ix. Ymanea el PC men yfi9 fil sac.", "es": "Fuerza S3 en vez de S0ix. Evita que el PC despierte en la mochila.", "de": "Erzwingt S3 statt S0ix. Verhindert, dass der PC im Rucksack aufwacht.", "ar": "يفرض S3 بدل S0ix. يمنع الكمبيوتر من الاستيقاظ في الحقيبة."},
    "Disable Hibernation & Fast Startup": {"en": "Deletes the hiberfil.sys file (saving GBs of space) and forces a true clean boot every time you shut down, preventing driver rot.", "fr": "Supprime hiberfil.sys (économise des Go) et force un vrai redémarrage propre.", "tn": "Yna77i hiberfil.sys (ywaffar Go) w yforci redemarrage propre.", "es": "Elimina hiberfil.sys (ahorra GBs) y fuerza un arranque limpio real.", "de": "Löscht hiberfil.sys (spart GBs) und erzwingt einen echten sauberen Neustart.", "ar": "يحذف hiberfil.sys (يوفر غيغابايت) ويفرض إقلاع نظيف حقيقي."},
    "Enable MSI Mode on All PCI Devices": {"en": "Switches GPU, NIC, USB, Storage, Audio from legacy shared IRQ lines to private Message Signaled Interrupts. Drastically lowers DPC latency. Warning: may cause BSODs on devices with broken MSI implementations (some Realtek NICs, older USB3 controllers).", "fr": "Passe GPU, NIC, USB, Stockage, Audio en MSI. Réduit drastiquement la latence DPC. Attention: peut causer des BSOD.", "tn": "Ybaddel GPU, NIC, USB, Stockage, Audio l MSI. Y9allel barcha latence DPC. Attention: y9adder ysabbeb BSOD.", "es": "Cambia GPU, NIC, USB, Almacenamiento, Audio a MSI. Reduce drásticamente latencia DPC. Advertencia: puede causar BSOD.", "de": "Schaltet GPU, NIC, USB, Speicher, Audio auf MSI um. Reduziert DPC-Latenz drastisch. Warnung: kann BSODs verursachen.", "ar": "يحوّل GPU وبطاقة الشبكة وUSB والتخزين إلى MSI. يقلل تأخر DPC بشكل كبير. تحذير: قد يسبب شاشة زرقاء."},
    "Disable USB Controller Power Saving": {"en": "Sets EnhancedPowerManagement=0, SelectiveSuspend=0 on USB host controllers. Fixes random 10ms input spikes on mice and keyboards.", "fr": "Désactive l'économie de contrôleur USB. Corrige les pics d'entrée de 10ms sur souris et claviers.", "tn": "Ytaffi economie controleur USB. Ysalla7 les pics 10ms taa3 souris w claviers.", "es": "Desactiva ahorro de energía del controlador USB. Corrige picos de 10ms en ratón y teclado.", "de": "Deaktiviert USB-Controller-Energiesparen. Behebt 10ms-Eingabespitzen bei Maus und Tastatur.", "ar": "يعطّل توفير طاقة وحدة تحكم USB. يصلح قفزات إدخال 10 مللي ثانية."},
    "Set GPU MSI Priority to High": {"en": "Forces the GPU's Message Signaled Interrupts to be processed with High priority by the CPU.", "fr": "Force les MSI du GPU à être traités en priorité haute par le CPU.", "tn": "Yforci MSI taa3 GPU tet3aleg b priorite 3alya.", "es": "Fuerza que los MSI de la GPU se procesen con prioridad alta.", "de": "Erzwingt hohe Priorität für GPU-MSI-Verarbeitung.", "ar": "يفرض معالجة MSI لـ GPU بأولوية عالية."},
    "Set NIC MSI Priority to High": {"en": "Forces the Network Adapter's Message Signaled Interrupts to be processed with High priority by the CPU.", "fr": "Force les MSI de la carte réseau à être traités en priorité haute.", "tn": "Yforci MSI taa3 carte reseau tet3aleg b priorite 3alya.", "es": "Fuerza que los MSI de la NIC se procesen con prioridad alta.", "de": "Erzwingt hohe Priorität für NIC-MSI-Verarbeitung.", "ar": "يفرض معالجة MSI لبطاقة الشبكة بأولوية عالية."},
    "Optimize Mouse & Keyboard Queue (Input Latency)": {"en": "Decreases data queue size for inputs, slightly reducing input latency at the driver level.", "fr": "Réduit la taille de la file de données d'entrée, diminuant légèrement la latence.", "tn": "Y9allel taille file d'entree, y9allel chwaya latence.", "es": "Reduce el tamaño de cola de entrada, disminuyendo ligeramente la latencia.", "de": "Verringert die Eingabe-Warteschlangengröße, reduziert leicht die Latenz.", "ar": "يقلل حجم صف الإدخال، يقلل التأخير قليلاً."},
    "MarkC Mouse Fix (1:1 Raw Input)": {"en": "Patches SmoothMouseXCurve/YCurve to linear 1:1 at 100% DPI. Sets MouseSpeed=0, thresholds=0. True zero acceleration for gaming.", "fr": "Correction souris MarkC 1:1. Vitesse et seuils à 0. Zéro accélération pour le gaming.", "tn": "Fix souris MarkC 1:1. Vitesse w seuils 0. Zero acceleration lel gaming.", "es": "Fix ratón MarkC 1:1. Velocidad y umbrales en 0. Cero aceleración para juegos.", "de": "MarkC Mausfix 1:1. Geschwindigkeit und Schwellen auf 0. Null Beschleunigung für Gaming.", "ar": "إصلاح MarkC 1:1. السرعة والعتبات عند 0. تسارع صفري للألعاب."},
    "Disable Sticky / Filter / Toggle Key Prompts": {"en": "Prevents the annoying Shift-5x popup during gaming. Disables the hotkey triggers without removing the accessibility features.", "fr": "Empêche le popup agaçant Shift-5x pendant le jeu. Désactive les raccourcis sans supprimer l'accessibilité.", "tn": "Ymanea el popup Shift-5x w9t el jeu. Ytaffi les raccourcis bla ma yna77i l'accessibilite.", "es": "Evita el molesto popup Shift-5x durante el juego. Desactiva atajos sin eliminar accesibilidad.", "de": "Verhindert das nervige Shift-5x-Popup beim Spielen. Deaktiviert Hotkeys ohne Barrierefreiheit zu entfernen.", "ar": "يمنع نافذة Shift-5x المزعجة أثناء اللعب. يعطّل الاختصارات دون إزالة إمكانية الوصول."},
    "Reduce Menu & Hover Delays to 0": {"en": "Sets MenuShowDelay=0, MouseHoverTime=10. Menus and tooltips appear instantly instead of the 400ms default.", "fr": "Menus et infobulles apparaissent instantanément au lieu des 400ms par défaut.", "tn": "Les menus w infobulles ybanoulk to7a blasa men 400ms.", "es": "Menús e infobulles aparecen instantáneamente en vez de los 400ms por defecto.", "de": "Menüs und Tooltips erscheinen sofort statt nach 400ms Standard.", "ar": "القوائم والتلميحات تظهر فوراً بدلاً من 400 مللي ثانية."},
    "Set Performance Visual Preferences (Comprehensive)": {"en": "Sets UserPreferencesMask to a performance-oriented bitmask. Disables cursor shadow, menu/tooltip animations, and other visual effects. Overwrites ALL visual preference flags.", "fr": "Bitmask orienté performance. Désactive ombres de curseur, animations de menus et effets visuels.", "tn": "Bitmask performance. Ytaffi ombres curseur, animations menus w effets visuels.", "es": "Bitmask de rendimiento. Desactiva sombras de cursor, animaciones de menú y efectos visuales.", "de": "Performance-Bitmaske. Deaktiviert Cursor-Schatten, Menü-Animationen und visuelle Effekte.", "ar": "قناع بت للأداء. يعطّل ظل المؤشر ورسوم القوائم والتأثيرات البصرية."},
    "Increase Keyboard Repeat Rate": {"en": "Sets KeyboardDelay=0 and KeyboardSpeed=31. Makes holding down a key register much faster.", "fr": "KeyboardDelay=0 et KeyboardSpeed=31. Maintenir une touche s'enregistre beaucoup plus vite.", "tn": "KeyboardDelay=0 w KeyboardSpeed=31. Maintenir touche tet7ott asra3 barcha.", "es": "KeyboardDelay=0 y KeyboardSpeed=31. Mantener una tecla se registra mucho más rápido.", "de": "KeyboardDelay=0 und KeyboardSpeed=31. Tastenhalten registriert viel schneller.", "ar": "KeyboardDelay=0 و KeyboardSpeed=31. الضغط المطوّل يُسجّل أسرع بكثير."},
    "Disable All Windows Telemetry": {"en": "Sets AllowTelemetry=0 via policy and data collection paths. Stops diagnostic and usage data from being sent to Microsoft.", "fr": "AllowTelemetry=0 via stratégie. Arrête l'envoi de données de diagnostic à Microsoft.", "tn": "AllowTelemetry=0. Ywakef l'envoi donnees diagnostic l Microsoft.", "es": "AllowTelemetry=0 vía política. Detiene envío de datos de diagnóstico a Microsoft.", "de": "AllowTelemetry=0 via Richtlinie. Stoppt Senden von Diagnosedaten an Microsoft.", "ar": "AllowTelemetry=0. يوقف إرسال بيانات التشخيص إلى مايكروسوفت."},
    "Disable Advertising ID & Tracking": {"en": "Kills the unique advertising identifier, app launch tracking, and activity history timeline. Pure privacy win.", "fr": "Supprime l'identifiant publicitaire, le suivi des applis et l'historique d'activité.", "tn": "Yna77i ID publicitaire, suivi applis w historique d'activite.", "es": "Elimina ID publicitario, seguimiento de apps e historial de actividad.", "de": "Entfernt Werbe-ID, App-Tracking und Aktivitätsverlauf.", "ar": "يحذف معرّف الإعلانات وتتبع التطبيقات وسجل النشاط."},
    "Disable Location & Sensors": {"en": "Turns off Windows location services, Wi-Fi positioning, and location scripting. Desktop PCs almost never need this.", "fr": "Désactive les services de localisation, positionnement Wi-Fi et scripting de localisation.", "tn": "Ytaffi services localisation, Wi-Fi positioning w location scripting.", "es": "Desactiva servicios de ubicación, posicionamiento Wi-Fi y scripting de ubicación.", "de": "Deaktiviert Standortdienste, WLAN-Positionierung und Standort-Scripting.", "ar": "يعطّل خدمات الموقع وتحديد موقع Wi-Fi وبرمجة الموقع."},
    "Disable Content Delivery & Suggestions": {"en": "Stops Windows from silently installing Candy Crush, showing Start menu ads, lock screen tips, and suggested apps. 11+ toggles disabled.", "fr": "Empêche Windows d'installer Candy Crush, les pubs du menu Démarrer et les suggestions.", "tn": "Ymanea Windows men yinstalli Candy Crush, pubs menu Demarrer w suggestions.", "es": "Evita que Windows instale Candy Crush, muestre anuncios en Inicio y sugerencias.", "de": "Stoppt Windows daran, Candy Crush zu installieren, Startmenü-Werbung und Vorschläge anzuzeigen.", "ar": "يمنع Windows من تثبيت Candy Crush وإعلانات قائمة ابدأ والتطبيقات المقترحة."},
    "Disable Input Personalization & Speech": {"en": "Stops Windows from collecting typing patterns, handwriting data, and sending voice recordings to Microsoft servers.", "fr": "Arrête la collecte de données de frappe, écriture manuscrite et enregistrements vocaux.", "tn": "Ywakef jma3 donnees frappe, ecriture w enregistrements vocaux.", "es": "Detiene la recolección de patrones de escritura, manuscrita y grabaciones de voz.", "de": "Stoppt das Sammeln von Tipp-Mustern, Handschrift und Sprachaufnahmen.", "ar": "يوقف جمع أنماط الكتابة والخط اليدوي والتسجيلات الصوتية."},
    "Disable Feedback & Tailored Experiences": {"en": "No more 'Rate Windows' popups. Stops Microsoft from using your diagnostic data to personalize ads.", "fr": "Plus de popups 'Évaluez Windows'. Arrête l'utilisation de vos données pour personnaliser les pubs.", "tn": "Ma 3adch popups 'Evaluez Windows'. Ywakef l'utilisation donnees taa3ek lel pubs.", "es": "Sin más popups 'Valora Windows'. Deja de usar tus datos para personalizar anuncios.", "de": "Keine 'Windows bewerten'-Popups mehr. Stoppt personalisierte Werbung.", "ar": "لا مزيد من نوافذ 'قيّم Windows'. يوقف استخدام بياناتك لتخصيص الإعلانات."},
    "Disable P2P Update Delivery & Clipboard Sync": {"en": "Stops Windows from uploading updates to stranger PCs over the internet. Also disables cross-device clipboard sync.", "fr": "Empêche Windows de partager les mises à jour avec des PC inconnus. Désactive la synchro presse-papiers.", "tn": "Ymanea Windows men yba3eth mises a jour l PC inconnus. Ytaffi synchro presse-papiers.", "es": "Evita que Windows suba actualizaciones a PCs desconocidos. Desactiva sincro de portapapeles.", "de": "Stoppt Upload von Updates an fremde PCs. Deaktiviert Zwischenablage-Sync.", "ar": "يمنع Windows من رفع التحديثات لأجهزة غرباء. يعطّل مزامنة الحافظة."},
    "Disable Edge Telemetry": {"en": "Disables Microsoft Edge's background data collection and metrics reporting.", "fr": "Désactive la collecte de données en arrière-plan de Microsoft Edge.", "tn": "Ytaffi jma3 donnees Edge men background.", "es": "Desactiva la recolección de datos en segundo plano de Edge.", "de": "Deaktiviert Edges Hintergrund-Datensammlung und Metrik-Berichte.", "ar": "يعطّل جمع بيانات Edge في الخلفية."},
    "Disable Office Telemetry": {"en": "Disables telemetry data collection for Microsoft Office applications.", "fr": "Désactive la collecte de données pour les applications Microsoft Office.", "tn": "Ytaffi jma3 donnees taa3 Microsoft Office.", "es": "Desactiva la recolección de datos de telemetría de Office.", "de": "Deaktiviert Telemetrie-Datensammlung für Microsoft Office.", "ar": "يعطّل جمع بيانات القياس لتطبيقات Office."},
    "Disable Visual Studio Telemetry": {"en": "Disables the Customer Experience Improvement Program for Visual Studio.", "fr": "Désactive le programme d'amélioration de l'expérience client pour Visual Studio.", "tn": "Ytaffi programme d'amelioration experience Visual Studio.", "es": "Desactiva el programa de mejora de experiencia de Visual Studio.", "de": "Deaktiviert das Programm zur Verbesserung der Benutzerfreundlichkeit für Visual Studio.", "ar": "يعطّل برنامج تحسين تجربة العملاء لـ Visual Studio."},
    "Disable NVIDIA Telemetry": {"en": "Disables NVIDIA's background telemetry services and tasks. Skips gracefully if NVIDIA is not installed.", "fr": "Désactive les services de télémétrie NVIDIA en arrière-plan. Ignoré si NVIDIA n'est pas installé.", "tn": "Ytaffi services telemetrie NVIDIA. Yetjawez kan NVIDIA mch installe.", "es": "Desactiva servicios de telemetría de NVIDIA. Se omite si NVIDIA no está instalado.", "de": "Deaktiviert NVIDIAs Telemetrie-Dienste. Wird übersprungen wenn NVIDIA nicht installiert.", "ar": "يعطّل خدمات قياس NVIDIA. يتجاوز إذا لم تكن مثبتة."},
    "Disable Windows Defender SmartScreen": {"en": "Stops Windows from sending URLs and downloaded file hashes to Microsoft servers for reputation checking.", "fr": "Empêche Windows d'envoyer les URL et les hachages de fichiers à Microsoft.", "tn": "Ymanea Windows men yba3eth URL w hachages fichiers l Microsoft.", "es": "Evita que Windows envíe URLs y hashes de archivos a Microsoft.", "de": "Stoppt Windows daran, URLs und Datei-Hashes an Microsoft zu senden.", "ar": "يمنع Windows من إرسال عناوين URL وتجزئات الملفات إلى مايكروسوفت."},
    "Disable Error Reporting (WER)": {"en": "Stops Windows from generating crash dumps and sending them to Microsoft. Saves disk space and CPU cycles during crashes.", "fr": "Arrête la génération de dumps de crash et l'envoi à Microsoft. Économise espace disque et CPU.", "tn": "Ywakef generation dumps crash w l'envoi l Microsoft. Ywaffar disque w CPU.", "es": "Detiene la generación de dumps de crash y envío a Microsoft. Ahorra disco y CPU.", "de": "Stoppt Crash-Dump-Erstellung und Senden an Microsoft. Spart Speicherplatz und CPU.", "ar": "يوقف إنشاء ملفات الأعطال وإرسالها لمايكروسوفت. يوفر مساحة ودورات معالج."},
    "Disable Inventory Collector": {"en": "Stops Windows from scanning your hard drive to build an inventory of installed applications and files to send to Microsoft.", "fr": "Empêche Windows de scanner votre disque pour inventorier les applications installées.", "tn": "Ymanea Windows men yscanni disque bech y3amel inventaire applications.", "es": "Evita que Windows escanee tu disco para inventariar aplicaciones instaladas.", "de": "Stoppt Windows daran, Ihre Festplatte nach installierten Apps zu durchsuchen.", "ar": "يمنع Windows من مسح القرص لجرد التطبيقات المثبتة."},
    "Disable DiagTrack & WAP Push": {"en": "The main telemetry pipeline (Connected User Experiences) and its feeder service. Constant CPU + network drain eliminated.", "fr": "Le pipeline principal de télémétrie. Drain constant CPU + réseau éliminé.", "tn": "Pipeline principal telemetrie. Drain CPU + reseau elimine.", "es": "Pipeline principal de telemetría. Drenaje constante de CPU + red eliminado.", "de": "Die Haupt-Telemetrie-Pipeline. Konstanter CPU- und Netzwerk-Verbrauch eliminiert.", "ar": "خط القياس الرئيسي. يزيل استنزاف المعالج والشبكة الدائم."},
    "Disable SysMain / Superfetch": {"en": "Pre-loads apps into RAM based on usage habits. Constant disk I/O on HDDs, wastes RAM on SSDs. Safe to disable on SSDs.", "fr": "Précharge les applis en RAM. I/O disque constant sur HDD, gaspille RAM sur SSD.", "tn": "Ychargi applis fil RAM. I/O disque 3la HDD, gaspillage RAM 3la SSD.", "es": "Precarga apps en RAM. E/S constante en HDD, desperdicia RAM en SSD.", "de": "Lädt Apps in RAM vor. Konstante I/O auf HDDs, verschwendet RAM auf SSDs.", "ar": "يحمّل التطبيقات مسبقاً في RAM. عمليات قرص مستمرة على HDD، يهدر RAM على SSD."},
    "Disable WER, Diagnostics & Link Tracking": {"en": "Windows Error Reporting, Diagnostic hosts, and Distributed Link Tracking — all background services with zero user benefit.", "fr": "WER, hôtes diagnostics et suivi de liens distribué — services sans bénéfice utilisateur.", "tn": "WER, diagnostics w suivi liens - services bla fayda lel utilisateur.", "es": "WER, hosts de diagnóstico y seguimiento de enlaces — servicios sin beneficio para el usuario.", "de": "WER, Diagnose-Hosts und Link-Tracking — Hintergrunddienste ohne Nutzernutzen.", "ar": "WER والتشخيصات وتتبع الروابط — خدمات خلفية بدون فائدة للمستخدم."},
    "Disable Bloat Services (Fax, Maps, Retail...)": {"en": "Disables Fax, Downloaded Maps Manager, Retail Demo, AllJoyn IoT router, Windows Insider, Geolocation, Remote Registry.", "fr": "Désactive Fax, gestionnaire de cartes, démo retail, routeur IoT AllJoyn, Windows Insider.", "tn": "Ytaffi Fax, cartes, demo retail, AllJoyn, Windows Insider.", "es": "Desactiva Fax, Mapas, Demo retail, AllJoyn, Windows Insider.", "de": "Deaktiviert Fax, Karten, Retail-Demo, AllJoyn, Windows Insider.", "ar": "يعطّل فاكس، خرائط، عرض تجريبي، AllJoyn، Windows Insider."},
    "Disable Xbox Services (4 services)": {"en": "Xbox Live Auth, Game Save, Accessory Management, Networking. Disable if you don't use Xbox Game Pass on PC.", "fr": "Xbox Live Auth, sauvegarde de jeu, gestion des accessoires. Désactivez si vous n'utilisez pas Xbox sur PC.", "tn": "Xbox Live Auth, sauvegarde jeu, gestion accessoires. Taffihom kan ma testa3melch Xbox.", "es": "Xbox Live Auth, guardado, accesorios, red. Desactiva si no usas Xbox Game Pass en PC.", "de": "Xbox Live Auth, Spielstand, Zubehör, Netzwerk. Deaktivieren wenn kein Xbox Game Pass.", "ar": "Xbox Live Auth، حفظ ألعاب، إدارة ملحقات. عطّل إذا لم تستخدم Xbox."},
    "Disable Telemetry Scheduled Tasks": {"en": "Compatibility Appraiser (uses 100% disk 15-30 min), ProgramDataUpdater, CEIP tasks, DiskDiagnostic, Error Reporting queue.", "fr": "Compatibility Appraiser (100% disque 15-30 min), ProgramDataUpdater, tâches CEIP.", "tn": "Compatibility Appraiser (100% disque 15-30 min), ProgramDataUpdater, taches CEIP.", "es": "Compatibility Appraiser (100% disco 15-30 min), ProgramDataUpdater, tareas CEIP.", "de": "Compatibility Appraiser (100% Datenträger 15-30 Min), ProgramDataUpdater, CEIP-Aufgaben.", "ar": "Compatibility Appraiser (100% قرص 15-30 دقيقة)، ProgramDataUpdater، مهام CEIP."},
    "Disable Print Spooler": {"en": "Disables the printer service. Only use this if you NEVER print to a physical or PDF printer.", "fr": "Désactive le service d'impression. Uniquement si vous n'imprimez JAMAIS.", "tn": "Ytaffi service impression. 7assilha kan ma timprimich ABADAN.", "es": "Desactiva el servicio de impresión. Solo si NUNCA imprimes.", "de": "Deaktiviert den Druckdienst. Nur wenn Sie NIE drucken.", "ar": "يعطّل خدمة الطباعة. فقط إذا لم تطبع أبداً."},
    "Disable Windows Search Service": {"en": "Disables the background file indexer. Search will still work but will be slower. Saves massive disk I/O.", "fr": "Désactive l'indexeur de fichiers. La recherche fonctionne mais plus lente. Économise beaucoup d'I/O.", "tn": "Ytaffi l'indexeur fichiers. Recherche tkheddem ama abta. Ywaffar barcha I/O.", "es": "Desactiva el indexador de archivos. La búsqueda funciona pero más lenta. Ahorra mucha E/S.", "de": "Deaktiviert den Dateiindexer. Suche funktioniert, aber langsamer. Spart massive I/O.", "ar": "يعطّل مفهرس الملفات. البحث يعمل لكن أبطأ. يوفر عمليات قرص كثيرة."},
    "Disable Windows Update Service": {"en": "Completely disables Windows Update. HIGH RISK. You will not receive security patches or feature updates.", "fr": "Désactive Windows Update complètement. RISQUE ÉLEVÉ. Plus de correctifs de sécurité.", "tn": "Ytaffi Windows Update kamla. RISQUE 3ALI. Ma 3adch correctifs securite.", "es": "Desactiva Windows Update completamente. ALTO RIESGO. Sin parches de seguridad.", "de": "Deaktiviert Windows Update vollständig. HOHES RISIKO. Keine Sicherheitsupdates mehr.", "ar": "يعطّل Windows Update بالكامل. خطر عالي. لن تتلقى تصحيحات أمنية."},
    "Disable Background Intelligent Transfer (BITS)": {"en": "Disables BITS, which is used by Windows Update and other apps to download files in the background.", "fr": "Désactive BITS, utilisé par Windows Update et d'autres applis pour télécharger en arrière-plan.", "tn": "Ytaffi BITS, eli yesta3mlou Windows Update w applis okhrin lel telechargement background.", "es": "Desactiva BITS, usado por Windows Update y otras apps para descargar en segundo plano.", "de": "Deaktiviert BITS, das von Windows Update und anderen Apps für Hintergrund-Downloads verwendet wird.", "ar": "يعطّل BITS الذي يستخدمه Windows Update وتطبيقات أخرى للتنزيل في الخلفية."},
    "Disable Security Center Service": {"en": "Disables the Windows Security Center service. Stops notifications about antivirus and firewall status.", "fr": "Désactive le Centre de sécurité Windows. Arrête les notifications antivirus et pare-feu.", "tn": "Ytaffi Centre de securite Windows. Ywakef notifications antivirus w pare-feu.", "es": "Desactiva el Centro de seguridad de Windows. Detiene notificaciones de antivirus y firewall.", "de": "Deaktiviert das Windows-Sicherheitscenter. Stoppt Antivirus- und Firewall-Benachrichtigungen.", "ar": "يعطّل مركز أمان Windows. يوقف إشعارات مكافح الفيروسات وجدار الحماية."},
    "Deep Temp / Cache / Log Cleanup": {"en": "Deletes user temp, system temp, prefetch, thumbnail/icon/shader caches, error reports, crash dumps, CBS logs. Recovers GBs of space.", "fr": "Supprime temp, prefetch, caches, rapports d'erreur, dumps de crash, logs CBS. Récupère des Go.", "tn": "Yna77i temp, prefetch, caches, rapports erreur, crash dumps, logs CBS. Yrecupere Go.", "es": "Elimina temp, prefetch, cachés, informes de error, dumps crash, logs CBS. Recupera GBs.", "de": "Löscht Temp, Prefetch, Caches, Fehlerberichte, Crash-Dumps, CBS-Logs. Gibt GBs frei.", "ar": "يحذف الملفات المؤقتة وPrefetch والتخزين المؤقت والسجلات. يستعيد غيغابايت."},
    "Flush DNS & ARP Cache": {"en": "Clears stale DNS and network address mappings. Both rebuild instantly. Fixes many connection issues.", "fr": "Efface les mappages DNS et ARP obsolètes. Corrige de nombreux problèmes de connexion.", "tn": "Yna77i les mappages DNS w ARP el 9doum. Ysalla7 barcha problemes connexion.", "es": "Limpia mappings DNS y ARP obsoletos. Corrige muchos problemas de conexión.", "de": "Löscht veraltete DNS- und ARP-Zuordnungen. Behebt viele Verbindungsprobleme.", "ar": "يمسح خرائط DNS وARP القديمة. يصلح كثيراً من مشاكل الاتصال."},
    "Clean Browser Caches (Chrome, Edge, Firefox)": {"en": "Removes cached web data from all major browsers. Does NOT delete passwords, bookmarks, or history.", "fr": "Supprime les données web en cache. NE supprime PAS mots de passe, favoris ou historique.", "tn": "Yna77i donnees web en cache. MA yna77ich mots de passe, favoris wella historique.", "es": "Elimina datos web en caché. NO borra contraseñas, marcadores ni historial.", "de": "Entfernt gecachte Webdaten. Löscht KEINE Passwörter, Lesezeichen oder Verlauf.", "ar": "يزيل بيانات الويب المخزّنة. لا يحذف كلمات المرور أو المفضلة أو السجل."},
    "NTFS Optimizations (Last Access, 8.3, Memory)": {"en": "Disables last-access timestamps (reduces writes), disables DOS 8.3 filenames (NTFS overhead), increases NTFS paged pool.", "fr": "Désactive les horodatages d'accès, les noms 8.3 DOS et augmente le pool NTFS.", "tn": "Ytaffi horodatages acces, noms 8.3 DOS w yzid pool NTFS.", "es": "Desactiva timestamps de acceso, nombres 8.3 DOS y aumenta pool NTFS.", "de": "Deaktiviert Zugriffszeitstempel, DOS-8.3-Dateinamen und erhöht NTFS-Pool.", "ar": "يعطّل طوابع الوصول وأسماء 8.3 ويزيد مجمع NTFS."},
    "Clear Windows Update Cache (SoftwareDistribution)": {"en": "Deletes downloaded Windows Update files. Fixes stuck updates and frees up massive amounts of space.", "fr": "Supprime les fichiers Windows Update téléchargés. Corrige les mises à jour bloquées.", "tn": "Yna77i fichiers Windows Update. Ysalla7 mises a jour bloquees w yfarregh espace.", "es": "Elimina archivos de Windows Update descargados. Corrige actualizaciones atascadas.", "de": "Löscht heruntergeladene Windows-Update-Dateien. Behebt hängende Updates.", "ar": "يحذف ملفات Windows Update المحمّلة. يصلح التحديثات المتعلقة."},
    "Clear Event Viewer Logs": {"en": "Wipes all Windows Event logs. Good for a fresh start when troubleshooting, or just to free up space.", "fr": "Efface tous les journaux d'événements Windows. Bon pour un nouveau départ.", "tn": "Yna77i kol les journaux evenements. Behi lel depart jdid.", "es": "Limpia todos los registros de eventos de Windows. Bueno para empezar de nuevo.", "de": "Löscht alle Windows-Ereignisprotokolle. Gut für einen Neuanfang.", "ar": "يمسح جميع سجلات أحداث Windows. جيد لبداية جديدة."},
    "Disable Windows Error Reporting (WER) Folders": {"en": "Prevents WER from sending additional diagnostic data and disables report queuing. The WER folders may still be created but will contain less data.", "fr": "Empêche WER d'envoyer des données de diagnostic supplémentaires et désactive la file d'attente.", "tn": "Ymanea WER men yba3eth donnees diagnostic supplementaires w ytaffi la file d'attente.", "es": "Evita que WER envíe datos de diagnóstico adicionales y desactiva la cola de informes.", "de": "Verhindert, dass WER zusätzliche Diagnosedaten sendet und deaktiviert die Berichtswarteschlange.", "ar": "يمنع WER من إرسال بيانات تشخيص إضافية ويعطّل ترتيب التقارير."},
    "Disable Delivery Optimization Cache": {"en": "Stops Windows from caching updates to share with other PCs, freeing up disk space and reducing background disk I/O.", "fr": "Empêche Windows de mettre en cache les mises à jour pour les partager. Libère de l'espace disque.", "tn": "Ymanea Windows men cache mises a jour lel partage. Yfarregh espace disque.", "es": "Evita que Windows cache actualizaciones para compartir. Libera espacio de disco.", "de": "Stoppt Windows daran, Updates zum Teilen zu cachen. Gibt Speicherplatz frei.", "ar": "يمنع Windows من تخزين التحديثات للمشاركة. يحرر مساحة القرص."},
    "Faster Shutdown Timeouts": {"en": "WaitToKillService=2s, WaitToKillApp=2s, HungApp=1s, AutoEndTasks=1. Makes shutdown/restart dramatically faster.", "fr": "WaitToKillService=2s, HungApp=1s, AutoEndTasks=1. Arrêt/redémarrage beaucoup plus rapide.", "tn": "WaitToKillService=2s, HungApp=1s. Arret/redemarrage asra3 barcha.", "es": "WaitToKillService=2s, HungApp=1s. Apagado/reinicio mucho más rápido.", "de": "WaitToKillService=2s, HungApp=1s. Herunterfahren/Neustart viel schneller.", "ar": "WaitToKillService=2s, HungApp=1s. إيقاف/إعادة تشغيل أسرع بكثير."},
    "Remove Startup Program Delay": {"en": "Windows intentionally delays startup programs by ~10 seconds. This removes that delay. Instantly noticeable on SSDs.", "fr": "Windows retarde les programmes de démarrage de ~10 secondes. Supprime ce délai.", "tn": "Windows yre7tardi programmes demarrage ~10 secondes. Yna77i ce delai.", "es": "Windows retrasa programas de inicio ~10 segundos. Elimina ese retraso.", "de": "Windows verzögert Startprogramme um ~10 Sekunden. Entfernt diese Verzögerung.", "ar": "Windows يؤخر برامج بدء التشغيل ~10 ثوانٍ. يزيل هذا التأخير."},
    "Disable Cortana & Web Search in Start": {"en": "Disables Cortana and prevents Bing results when you search for local apps in the Start menu. Makes search 10x better.", "fr": "Désactive Cortana et empêche les résultats Bing dans la recherche du menu Démarrer.", "tn": "Ytaffi Cortana w ymanea resultats Bing fi recherche menu Demarrer.", "es": "Desactiva Cortana y evita resultados Bing en búsqueda del menú Inicio.", "de": "Deaktiviert Cortana und verhindert Bing-Ergebnisse in der Startmenü-Suche.", "ar": "يعطّل Cortana ويمنع نتائج Bing في بحث قائمة ابدأ."},
    "Taskbar Cleanup (People, Chat, Widgets...)": {"en": "Hides People, Meet Now/Chat, Task View, News/Interests/Widgets, Ink Workspace. Search set to icon-only.", "fr": "Cache Contacts, Chat, Vue des tâches, Actualités/Widgets, Ink. Recherche en icône seule.", "tn": "Ykhabi Contacts, Chat, Vue taches, Actualites/Widgets, Ink. Recherche icone bark.", "es": "Oculta Contactos, Chat, Vista de tareas, Noticias/Widgets, Ink. Búsqueda solo icono.", "de": "Blendet Kontakte, Chat, Aufgabenansicht, Nachrichten/Widgets, Ink aus. Suche nur Icon.", "ar": "يخفي جهات الاتصال والدردشة وعرض المهام والأخبار والأدوات. البحث أيقونة فقط."},
    "Show File Extensions & Hidden Files": {"en": "Security essential: see the real extension of every file. Also shows hidden files and opens Explorer to This PC.", "fr": "Essentiel sécurité : voir la vraie extension. Affiche les fichiers cachés et ouvre l'Explorateur sur Ce PC.", "tn": "Mohemm lel securite: chouf el extension el 79i9iya. Ybayyen fichiers caches.", "es": "Esencial de seguridad: ver la extensión real. Muestra archivos ocultos y abre Explorer en Este PC.", "de": "Sicherheitsessentiell: echte Erweiterung sehen. Zeigt versteckte Dateien und öffnet Explorer bei Dieser PC.", "ar": "ضروري للأمان: عرض الامتداد الحقيقي. يظهر الملفات المخفية ويفتح المستكشف على هذا الكمبيوتر."},
    "Disable Visual Animations & Transparency": {"en": "Removes window animations, transparency blur, and drag-full-windows. Keeps ClearType font smoothing. GPU/CPU savings.", "fr": "Supprime les animations, flou de transparence. Garde le lissage ClearType. Économies GPU/CPU.", "tn": "Yna77i animations, flou transparence. Ykhalli ClearType. Economies GPU/CPU.", "es": "Elimina animaciones, desenfoque de transparencia. Mantiene ClearType. Ahorro GPU/CPU.", "de": "Entfernt Animationen, Transparenz-Unschärfe. Behält ClearType. GPU/CPU-Einsparungen.", "ar": "يزيل الرسوم المتحركة وضبابية الشفافية. يحافظ على ClearType. توفير GPU/CPU."},
    "Restore Classic Right-Click Menu (Win 11)": {"en": "Brings back the full context menu instead of the truncated one requiring 'Show more options'. Does nothing on Win 10.", "fr": "Ramène le menu contextuel complet au lieu de celui tronqué. Sans effet sur Win 10.", "tn": "Yraj3a menu clic droit kamla blasa men el tronque. Ma ya3melch 7aja 3la Win 10.", "es": "Devuelve el menú contextual completo en vez del truncado. Sin efecto en Win 10.", "de": "Bringt das vollständige Kontextmenü zurück statt des verkürzten. Kein Effekt auf Win 10.", "ar": "يستعيد قائمة النقر اليمني الكاملة بدلاً من المختصرة. لا تأثير على Win 10."},
    "Disable AutoPlay & Remote Assistance": {"en": "Stops auto-execution when inserting media (security risk). Disables Remote Assistance (rarely needed, attack vector).", "fr": "Arrête l'exécution auto lors de l'insertion de médias. Désactive l'assistance à distance.", "tn": "Ywakef l'execution auto ki t7ot media. Ytaffi l'assistance a distance.", "es": "Detiene ejecución auto al insertar medios. Desactiva Asistencia Remota.", "de": "Stoppt Auto-Ausführung beim Einlegen von Medien. Deaktiviert Remoteunterstützung.", "ar": "يوقف التشغيل التلقائي عند إدخال الوسائط. يعطّل المساعدة عن بُعد."},
    "Disable Action Center / Notifications": {"en": "Completely disables the Windows Action Center and all toast notifications. Pure uninterrupted focus.", "fr": "Désactive complètement le Centre d'action et toutes les notifications. Concentration pure.", "tn": "Ytaffi Centre d'action w kol les notifications. Concentration pure.", "es": "Desactiva completamente el Centro de acciones y todas las notificaciones. Concentración pura.", "de": "Deaktiviert das Info-Center und alle Benachrichtigungen vollständig. Reiner Fokus.", "ar": "يعطّل مركز الإجراءات وجميع الإشعارات بالكامل. تركيز مطلق."},
    "Disable Lock Screen": {"en": "Skips the picture lock screen and goes straight to the password/PIN prompt on boot. Requires Windows Pro or Enterprise (does not work on Home edition).", "fr": "Passe directement à l'invite de mot de passe/PIN. Nécessite Windows Pro ou Enterprise.", "tn": "Yfout to7a lel invite mot de passe/PIN. Lazem Windows Pro wella Enterprise.", "es": "Va directo a la solicitud de contraseña/PIN. Requiere Windows Pro o Enterprise.", "de": "Geht direkt zur Passwort/PIN-Eingabe. Erfordert Windows Pro oder Enterprise.", "ar": "يتخطى شاشة القفل مباشرةً لطلب كلمة المرور. يتطلب Windows Pro أو Enterprise."},
    "Disable Aero Shake & Snap Assist": {"en": "Stops windows from minimizing when you shake them, and stops the annoying snap assist suggestions.", "fr": "Empêche les fenêtres de se minimiser quand vous les secouez et arrête les suggestions snap.", "tn": "Ymanea les fenetres men minimiser ki thezzhem w ywakef suggestions snap.", "es": "Evita que las ventanas se minimicen al sacudirlas y detiene las sugerencias snap.", "de": "Stoppt Minimieren beim Schütteln und nervige Snap-Vorschläge.", "ar": "يمنع تصغير النوافذ عند هزها ويوقف اقتراحات Snap المزعجة."},
    "Disable Windows Defender (Requires Safe Mode/TrustedInstaller)": {"en": "Attempts to disable Windows Defender. Note: Modern Windows 10/11 heavily protects these keys. May require third-party tools or Safe Mode to fully apply.", "fr": "Tentative de désactivation de Windows Defender. Windows moderne protège fortement ces clés.", "tn": "Y7awel ytaffi Windows Defender. Windows moderne y7ami ces cles barcha.", "es": "Intenta desactivar Windows Defender. Windows moderno protege estas claves.", "de": "Versucht Windows Defender zu deaktivieren. Modernes Windows schützt diese Schlüssel stark.", "ar": "يحاول تعطيل Windows Defender. ملاحظة: Windows الحديث يحمي هذه المفاتيح بشدة."},
    "Disable Kernel Mitigations (KVA Shadow)": {"en": "Disables Kernel Virtual Address Shadow (Meltdown fix) and Spectre V2 Branch Target Injection mitigations. HIGH RISK: exposes the system to Meltdown/Spectre but gains 5-30% kernel call performance.", "fr": "Désactive les protections Meltdown/Spectre. RISQUE ÉLEVÉ: expose le système mais gagne 5-30% de performances.", "tn": "Ytaffi protections Meltdown/Spectre. Risque kbir: ynakess securite ama yzid 5-30% performances.", "es": "Desactiva protecciones Meltdown/Spectre. ALTO RIESGO: expone el sistema pero gana 5-30% rendimiento.", "de": "Deaktiviert Meltdown/Spectre-Schutz. HOHES RISIKO: 5-30% Performance-Gewinn.", "ar": "يعطل حماية Meltdown/Spectre. خطر عالي: يكشف النظام لكن يكسب 5-30% أداء."},
    "Increase System Working Set (Kernel Pool)": {"en": "Sets SystemPages=0 to let Windows dynamically maximize the number of page table entries in the system working set. More kernel memory available for drivers and file cache.", "fr": "SystemPages=0 pour maximiser les entrées de table de pages du noyau.", "tn": "Y7ot SystemPages=0. Y5alli Windows ykhalli akther memoire lel drivers w cache.", "es": "SystemPages=0 para maximizar entradas de tabla de páginas del kernel.", "de": "SystemPages=0 für maximale Kernel-Seitentabelleneinträge.", "ar": "يضبط SystemPages=0 لتعظيم ذاكرة النواة للتعريفات والتخزين المؤقت."},
    "Large System Cache (Server-Style Memory)": {"en": "Sets LargeSystemCache=1 (server mode). Windows aggressively caches file system data in RAM. Can starve applications on systems with less than 8GB RAM.", "fr": "LargeSystemCache=1 (mode serveur). Cache aggressif des fichiers en RAM. Peut manquer de RAM sous 8GB.", "tn": "Y7ot large system cache kima serveur. Lazem 8GB+ RAM sinon ya3mel probleme.", "es": "LargeSystemCache=1 (modo servidor). Cache agresivo de archivos en RAM. Puede causar problemas con menos de 8GB.", "de": "LargeSystemCache=1 (Server-Modus). Aggressives Dateisystem-Caching im RAM.", "ar": "يضبط ذاكرة تخزين كبيرة (وضع الخادم). قد يسبب مشاكل مع أقل من 8 جيجا RAM."},
    "Disable Speculative Execution Side-Channel (SSBD)": {"en": "Disables Speculative Store Bypass Disable mitigation via registry. HIGH RISK: removes protection against Spectre Variant 4 but eliminates the 2-8% performance penalty.", "fr": "Désactive la mitigation SSBD via registre. RISQUE ÉLEVÉ: supprime la protection Spectre V4 mais gagne 2-8%.", "tn": "Ytaffi SSBD mitigation. Risque kbir: ynakess protection Spectre V4 ama yzid 2-8%.", "es": "Desactiva mitigación SSBD. ALTO RIESGO: elimina protección Spectre V4 pero gana 2-8%.", "de": "Deaktiviert SSBD-Mitigation. HOHES RISIKO: 2-8% Performance-Gewinn.", "ar": "يعطل حماية SSBD. خطر عالي: يزيل حماية Spectre V4 لكن يكسب 2-8% أداء."},
    "Disable Last Access Timestamp (Global)": {"en": "Uses fsutil to globally disable NTFS last-access timestamp updates. Reduces disk writes on every file read. Different from the per-volume Cleanup tweak.", "fr": "Désactive globalement les timestamps d'accès via fsutil. Réduit les écritures disque.", "tn": "Ytaffi last access timestamps b fsutil globally. Ynakess disk writes.", "es": "Desactiva globalmente las marcas de tiempo de acceso via fsutil.", "de": "Deaktiviert global NTFS-Zugriffszeitstempel via fsutil.", "ar": "يعطل عالمياً تحديثات طابع وقت الوصول لتقليل الكتابة على القرص."},
    "Enable Long Paths (Win32)": {"en": "Removes the legacy 260-character path limit in Win32 applications. Required for deep Node.js, Rust, and Java project trees.", "fr": "Supprime la limite de 260 caractères pour les chemins Win32.", "tn": "Yzid men 260 caracteres lel chemins. Lazem lel Node.js, Rust, Java.", "es": "Elimina el límite de 260 caracteres en rutas Win32.", "de": "Entfernt das 260-Zeichen-Pfadlimit in Win32-Anwendungen.", "ar": "يزيل حد 260 حرفاً للمسارات في تطبيقات Win32."},
    "Disable 8.3 Short Name Creation": {"en": "Disables legacy DOS 8.3 short filename generation on NTFS via fsutil. Reduces NTFS overhead for directories with many files.", "fr": "Désactive la génération de noms courts 8.3 DOS via fsutil.", "tn": "Ytaffi 8.3 short names b fsutil. Y7assin performances NTFS.", "es": "Desactiva la generación de nombres cortos DOS 8.3 via fsutil.", "de": "Deaktiviert DOS 8.3-Kurznamen via fsutil. Reduziert NTFS-Overhead.", "ar": "يعطل إنشاء أسماء DOS القصيرة عبر fsutil."},
    "Force DirectX 12 Shader Cache to RAM": {"en": "Redirects the DX12 pipeline state cache from disk to a RAM-backed path. Eliminates shader compilation stutter on NVMe-constrained systems.", "fr": "Redirige le cache de shaders DX12 du disque vers la RAM.", "tn": "Y7awel DX12 shader cache men disk lel RAM. Ynakess stutter.", "es": "Redirige caché de shaders DX12 del disco a RAM.", "de": "Leitet DX12-Shader-Cache vom Datenträger in den RAM um.", "ar": "يعيد توجيه ذاكرة شيدر DX12 من القرص إلى RAM."},
    "Disable NVIDIA Shader Disk Cache Limit": {"en": "Sets NVIDIA shader disk cache to unlimited (10GB). Prevents shader recompilation in games with many unique shaders.", "fr": "Cache de shaders NVIDIA illimité (10Go). Empêche la recompilation.", "tn": "Yzid NVIDIA shader cache lel 10GB. Ymanea recompilation shaders.", "es": "Cache de shaders NVIDIA ilimitado (10GB). Evita recompilación.", "de": "Setzt NVIDIA-Shader-Cache auf unbegrenzt (10GB).", "ar": "يضبط ذاكرة شيدر NVIDIA غير محدودة (10 جيجا)."},
    "Disable Flip Queue Size (Pre-Rendered Frames = 1)": {"en": "Forces pre-rendered frames to 1 via the Direct3D FlipQueueSize registry key. Reduces input lag by ~1 frame at the cost of slightly less smooth frametimes.", "fr": "Force les frames pré-rendues à 1. Réduit le lag d'entrée d'~1 frame.", "tn": "Y7ot pre-rendered frames = 1. Ynakess input lag b ~1 frame.", "es": "Fuerza fotogramas pre-renderizados a 1. Reduce lag de entrada ~1 fotograma.", "de": "Erzwingt vorgerenderte Frames auf 1. Reduziert Input-Lag um ~1 Frame.", "ar": "يفرض إطاراً مسبقاً واحداً. يقلل تأخر الإدخال بإطار واحد تقريباً."},
    "Disable NVIDIA Telemetry & Container Processes": {"en": "Kills NvContainerLocalSystem, NvContainerNetworkService, and NvTelemetry scheduled tasks. Stops NVIDIA from collecting usage data in the background.", "fr": "Arrête les conteneurs et télémétrie NVIDIA en arrière-plan.", "tn": "Ytaffi NVIDIA containers w telemetry. Ywaffir CPU w reseau.", "es": "Detiene contenedores y telemetría NVIDIA en segundo plano.", "de": "Stoppt NVIDIA-Container und Telemetrie-Prozesse.", "ar": "يوقف حاويات وتتبع NVIDIA في الخلفية."},
    "Disable Network Throttling Index": {"en": "Removes the 10-packets-per-millisecond throttle Windows applies to non-multimedia network traffic. Allows full NIC throughput.", "fr": "Supprime le throttle de 10 paquets/ms appliqué au trafic non-multimédia.", "tn": "Yzid network throttle yfout. Y5alli NIC full speed.", "es": "Elimina la limitación de 10 paquetes/ms para tráfico no multimedia.", "de": "Entfernt die 10-Pakete/ms-Drosselung für Nicht-Multimedia-Traffic.", "ar": "يزيل تقييد 10 حزم/مللي ثانية للشبكة."},
    "Disable WPAD (Web Proxy Auto-Discovery)": {"en": "Stops Windows from broadcasting WPAD requests to discover proxy servers. A known attack vector for man-in-the-middle on local networks.", "fr": "Empêche Windows de diffuser des requêtes WPAD. Vecteur d'attaque MITM connu.", "tn": "Ytaffi WPAD. Vecteur d'attaque MITM connu lel reseaux locaux.", "es": "Detiene solicitudes WPAD. Vector de ataque MITM conocido.", "de": "Stoppt WPAD-Anfragen. Bekannter MITM-Angriffsvektor.", "ar": "يوقف طلبات WPAD. ناقل هجوم MITM معروف."},
    "Disable ECN Capability": {"en": "Disables Explicit Congestion Notification. Some routers and firewalls drop ECN-marked packets, causing random connection stalls.", "fr": "Désactive ECN. Certains routeurs rejettent les paquets ECN.", "tn": "Ytaffi ECN. Ba3dh routeurs ybloquiw paquets ECN w ya3mlou stalls.", "es": "Desactiva ECN. Algunos routers rechazan paquetes ECN.", "de": "Deaktiviert ECN. Einige Router verwerfen ECN-markierte Pakete.", "ar": "يعطل ECN. بعض أجهزة التوجيه ترفض حزم ECN."},
    "Disable Timer Coalescing": {"en": "Prevents Windows from batching hardware timer interrupts together to save power. Reduces jitter at the cost of slightly more CPU wake-ups.", "fr": "Empêche Windows de regrouper les interruptions timer. Réduit le jitter.", "tn": "Ymanea Windows men yjmea timer interrupts. Ynakess jitter.", "es": "Evita que Windows agrupe interrupciones de temporizador. Reduce jitter.", "de": "Verhindert Timer-Interrupt-Bündelung. Reduziert Jitter.", "ar": "يمنع تجميع مقاطعات المؤقت. يقلل التذبذب."},
    "MMCSS Gaming Priority (SystemResponsiveness=0)": {"en": "Tells the Multimedia Class Scheduler to reserve 0% of CPU for background tasks during gaming. Sets Games task to High priority with High SFIO.", "fr": "Le MMCSS réserve 0% CPU pour les tâches en arrière-plan pendant le jeu.", "tn": "Y7ot MMCSS gaming priority. 0% CPU lel background, kol chay lel jeux.", "es": "MMCSS reserva 0% CPU para tareas en segundo plano durante juegos.", "de": "MMCSS reserviert 0% CPU für Hintergrundaufgaben beim Gaming.", "ar": "يخصص 0% من المعالج للمهام الخلفية أثناء الألعاب."},
    "Set Processor Performance Check Interval (5ms)": {"en": "Reduces the interval at which Windows checks if the CPU frequency needs adjusting from 15ms to 5ms. Faster boost clocks under sudden load.", "fr": "Réduit l'intervalle de vérification de fréquence CPU de 15ms à 5ms.", "tn": "Ynakess check interval CPU frequency men 15ms lel 5ms. Boost plus rapide.", "es": "Reduce el intervalo de verificación de frecuencia de 15ms a 5ms.", "de": "Reduziert CPU-Frequenzprüfintervall von 15ms auf 5ms.", "ar": "يقلل فاصل فحص تردد المعالج من 15 إلى 5 مللي ثانية."},
    "Disable Idle Promote / Demote Thresholds": {"en": "Sets idle demote threshold to 100% and promote threshold to 0%. Cores never downshift to lower C-states unless fully idle.", "fr": "Seuil de rétrogradation=100%, promotion=0%. Les cœurs ne descendent jamais.", "tn": "Y7ot demote=100% w promote=0%. Cores ma ybadlouch P-states.", "es": "Demote=100%, promote=0%. Los núcleos nunca bajan de C-state.", "de": "Demote=100%, Promote=0%. Kerne wechseln nie in niedrigere C-States.", "ar": "يضبط حدود التخفيض=100% والترقية=0%."},
    "Disable Latency-Sensitive Core Parking": {"en": "Removes latency hints from the core parking algorithm. Combined with unparking, ensures all cores respond equally fast.", "fr": "Supprime les indices de latence de l'algorithme de parking. Tous les cœurs répondent pareil.", "tn": "Ynahi latency hints mel core parking. Kol les cores yjiw pareil.", "es": "Elimina indicaciones de latencia del algoritmo de parking.", "de": "Entfernt Latenz-Hinweise aus dem Core-Parking-Algorithmus.", "ar": "يزيل تلميحات التأخير من خوارزمية إيقاف الأنوية."},
    "Pin GPU Interrupts to CPU 0 (Affinity Lock)": {"en": "Forces GPU interrupt handling to a single core, eliminating cross-core migration overhead. Can reduce frame time variance by 5-15%.", "fr": "Force le traitement des interruptions GPU sur un seul cœur. Réduit la variance de 5-15%.", "tn": "Yforci GPU interrupts lel core wa7ed. Ynakess frame time variance 5-15%.", "es": "Fuerza interrupciones GPU a un solo núcleo. Reduce varianza 5-15%.", "de": "Erzwingt GPU-Interrupt-Verarbeitung auf einem Kern. 5-15% weniger Varianz.", "ar": "يفرض معالجة مقاطعات GPU على نواة واحدة. يقلل التذبذب 5-15%."},
    "Disable NIC Interrupt Moderation": {"en": "Forces the NIC to fire an interrupt for every packet instead of batching. Lowers network latency at the cost of slightly more CPU usage.", "fr": "Force la NIC à déclencher une interruption par paquet. Moins de latence réseau.", "tn": "Ytaffi interrupt moderation. Kol paquet yfire interrupt. Ynakess latence.", "es": "Fuerza la NIC a disparar una interrupción por paquete.", "de": "Erzwingt einen Interrupt pro Paket. Weniger Netzwerklatenz.", "ar": "يفرض مقاطعة لكل حزمة. يقلل تأخر الشبكة."},
    "Disable Touch Input & Visual Feedback": {"en": "Disables touch feedback animations, touch gestures, and edge swipe. Reduces input processing overhead on non-touch desktops.", "fr": "Désactive les animations tactiles, gestes et glissement du bord.", "tn": "Ytaffi touch feedback w gestures w edge swipe. Ynakess overhead.", "es": "Desactiva animaciones táctiles, gestos y deslizamiento lateral.", "de": "Deaktiviert Touch-Feedback, Gesten und Randwischen.", "ar": "يعطل رسوم اللمس والإيماءات والسحب من الحافة."},
    "Disable Pen & Ink Input Service": {"en": "Stops the Touch Keyboard and Handwriting Panel Service. Saves RAM and CPU on desktops without pen/touch input.", "fr": "Arrête le service clavier tactile et panneau d'écriture.", "tn": "Ytaffi TabletInputService. Ywaffir RAM w CPU bla touch/pen.", "es": "Detiene el servicio de teclado táctil y panel de escritura.", "de": "Stoppt den Touch-Tastatur- und Handschrift-Dienst.", "ar": "يوقف خدمة لوحة المفاتيح اللمسية والكتابة اليدوية."},
    "Disable Handwriting Data Sharing": {"en": "Prevents Windows from sending handwriting recognition data and ink samples to Microsoft for product improvement.", "fr": "Empêche l'envoi de données d'écriture manuscrite à Microsoft.", "tn": "Ymanea Windows men yb3ath handwriting data lel Microsoft.", "es": "Evita enviar datos de escritura a mano a Microsoft.", "de": "Verhindert das Senden von Handschriftdaten an Microsoft.", "ar": "يمنع إرسال بيانات الكتابة اليدوية إلى Microsoft."},
    "Disable KMS Client Online AVS Validation": {"en": "Stops Windows from phoning home to validate your license activation status. Reduces background network traffic.", "fr": "Empêche Windows de vérifier en ligne le statut d'activation de la licence.", "tn": "Ymanea Windows men ychecki licence activation online. Ynakess traffic.", "es": "Evita que Windows verifique el estado de activación de licencia en línea.", "de": "Verhindert die Online-Lizenzvalidierung.", "ar": "يمنع التحقق من حالة تنشيط الترخيص عبر الإنترنت."},
    "Disable Wi-Fi Sense & Hotspot 2.0": {"en": "Prevents Windows from auto-connecting to suggested hotspots and sharing Wi-Fi credentials. Privacy and security improvement.", "fr": "Empêche la connexion automatique aux hotspots et le partage des identifiants Wi-Fi.", "tn": "Ytaffi auto-connect hotspots w partage Wi-Fi credentials. Privacy.", "es": "Evita conexión automática a hotspots y compartir credenciales Wi-Fi.", "de": "Verhindert automatische Hotspot-Verbindung und Wi-Fi-Freigabe.", "ar": "يمنع الاتصال التلقائي بنقاط الاتصال ومشاركة بيانات Wi-Fi."},
    "Disable Windows Biometric Service": {"en": "Stops the fingerprint/face recognition service. Saves resources on desktops without biometric hardware.", "fr": "Arrête le service de reconnaissance digitale/faciale.", "tn": "Ytaffi service biometrique. Ywaffir resources bla fingerprint/face.", "es": "Detiene el servicio de reconocimiento biométrico.", "de": "Stoppt den Fingerabdruck/Gesichtserkennung-Dienst.", "ar": "يوقف خدمة التعرف البيومتري."},
    "Disable Connected Devices Platform Service": {"en": "Disables cross-device experience services (Bluetooth sync, phone link background, nearby sharing). Saves CPU and network.", "fr": "Désactive les services d'expérience multi-appareils.", "tn": "Ytaffi cross-device sync. Ywaffir CPU w reseau.", "es": "Desactiva servicios de experiencia multi-dispositivo.", "de": "Deaktiviert geräteübergreifende Erlebnisdienste.", "ar": "يعطل خدمات التجربة عبر الأجهزة."},
    "Disable Phone Link Service": {"en": "Stops the Phone Service used by Windows Phone Link app. Saves background CPU and memory if you don't use phone integration.", "fr": "Arrête le service Phone Link. Économise CPU et mémoire en arrière-plan.", "tn": "Ytaffi Phone Link service. Ywaffir CPU w memoire fi background.", "es": "Detiene el servicio Phone Link. Ahorra CPU y memoria.", "de": "Stoppt den Phone Link-Dienst. Spart CPU und Speicher.", "ar": "يوقف خدمة ربط الهاتف. يوفر المعالج والذاكرة."},
    "Clear Font Cache": {"en": "Stops the font cache service, deletes corrupted font cache files, and restarts. Fixes garbled text and missing font glyphs.", "fr": "Arrête le cache de polices, supprime les fichiers corrompus et redémarre.", "tn": "Ynakki font cache. Ysalli7 texte garbled w polices manquantes.", "es": "Detiene el caché de fuentes, elimina archivos corruptos y reinicia.", "de": "Stoppt den Schriftarten-Cache, löscht beschädigte Dateien.", "ar": "يوقف خدمة تخزين الخطوط ويحذف الملفات التالفة."},
    "Reset Winsock & TCP/IP Stack": {"en": "Nuclear network reset. Clears all Winsock LSP entries and resets the TCP/IP stack to factory defaults. Requires reboot.", "fr": "Réinitialisation nucléaire du réseau. Efface Winsock LSP et réinitialise TCP/IP. Redémarrage requis.", "tn": "Nuclear network reset. Lazem reboot ba3dha. Ysalli7 kol problemes reseau.", "es": "Reset nuclear de red. Limpia Winsock LSP y restablece TCP/IP. Requiere reinicio.", "de": "Nuklearer Netzwerk-Reset. Löscht Winsock LSP, setzt TCP/IP zurück. Neustart nötig.", "ar": "إعادة تعيين شاملة للشبكة. يتطلب إعادة التشغيل."},
    "Disable Windows Copilot": {"en": "Prevents Windows Copilot AI assistant from loading. Saves RAM, removes the sidebar icon, and stops background Edge WebView processes.", "fr": "Empêche le chargement de Copilot AI. Économise RAM et arrête Edge WebView.", "tn": "Ytaffi Copilot AI. Ywaffir RAM w ynahi sidebar w edge webview.", "es": "Evita la carga de Copilot AI. Ahorra RAM y detiene Edge WebView.", "de": "Verhindert das Laden von Copilot AI. Spart RAM, stoppt Edge WebView.", "ar": "يمنع تحميل Copilot AI. يوفر الذاكرة ويوقف عمليات Edge."},
    "Disable Recall / AI Screenshots (Win 11 24H2)": {"en": "Prevents the Recall feature from taking periodic screenshots of your desktop. Only relevant on Windows 11 24H2+ with compatible NPU.", "fr": "Empêche la fonctionnalité Recall de prendre des captures d'écran. Win 11 24H2+ uniquement.", "tn": "Ytaffi Recall feature. Ymanea screenshots automatiques. Win 11 24H2+ bark.", "es": "Evita que Recall tome capturas periódicas. Solo Win 11 24H2+.", "de": "Verhindert Recall-Screenshots. Nur relevant für Win 11 24H2+.", "ar": "يمنع ميزة Recall من التقاط لقطات الشاشة. Win 11 24H2+ فقط."},
    "Set Explorer Compact View (Remove Padding)": {"en": "Removes the extra spacing Windows 11 added to File Explorer. Makes it dense like Windows 10 without losing any functionality.", "fr": "Supprime l'espacement supplémentaire de Windows 11 dans l'Explorateur.", "tn": "Y7ot Explorer compact view. Kima Windows 10 bla padding zayed.", "es": "Elimina el espaciado extra de Windows 11 en el Explorador.", "de": "Entfernt den zusätzlichen Windows 11-Abstand im Explorer.", "ar": "يزيل المسافات الإضافية في مستكشف Windows 11."},
    "Install 7-Zip": {"en": "Best open-source archive manager. Handles ZIP, RAR, 7z, TAR, GZ and more. Way better than WinRAR.", "fr": "Meilleur gestionnaire d'archives open-source. Gere ZIP, RAR, 7z, TAR et plus.", "tn": "A7sen outil d'archives. Ydir ZIP, RAR, 7z, TAR w akther. Khir mel WinRAR.", "es": "Mejor gestor de archivos open-source. Maneja ZIP, RAR, 7z, TAR y mas.", "de": "Bester Open-Source-Archivmanager. Verarbeitet ZIP, RAR, 7z, TAR und mehr.", "ar": "أفضل مدير أرشيف. يدعم ZIP, RAR, 7z, TAR وأكثر."},
    "Install Everything (Voidtools)": {"en": "Instant file search for Windows. Indexes your entire drive in seconds and finds any file in milliseconds. Life-changing.", "fr": "Recherche instantanee de fichiers. Indexe tout le disque en secondes.", "tn": "Recherche fichiers instantanee. Yindex el disque kamla fi secondes. Y7awlek 7yatek.", "es": "Busqueda instantanea de archivos. Indexa todo el disco en segundos.", "de": "Sofortige Dateisuche. Indiziert die gesamte Festplatte in Sekunden.", "ar": "بحث فوري عن الملفات. يفهرس القرص بالكامل في ثوان."},
    "Install PowerToys": {"en": "Microsoft's power-user utilities: FancyZones, Color Picker, PowerRename, Image Resizer, Keyboard Manager and more.", "fr": "Utilitaires Microsoft: FancyZones, Color Picker, PowerRename, Image Resizer et plus.", "tn": "Outils Microsoft lel power users: FancyZones, Color Picker, PowerRename w barcha.", "es": "Utilidades Microsoft: FancyZones, Color Picker, PowerRename, Image Resizer y mas.", "de": "Microsoft Power-User-Tools: FancyZones, Color Picker, PowerRename und mehr.", "ar": "أدوات Microsoft للمحترفين: FancyZones, Color Picker, PowerRename وأكثر."},
    "Install HWiNFO": {"en": "The most comprehensive hardware monitoring tool. CPU/GPU temps, voltages, fan speeds, power draw in real-time.", "fr": "Outil de monitoring le plus complet. Temps CPU/GPU, voltages, ventilateurs en temps reel.", "tn": "A7sen outil monitoring. Temperatures CPU/GPU, voltages, ventilateurs fi waqt 7a9i9i.", "es": "La herramienta de monitoreo mas completa. Temps CPU/GPU, voltajes, ventiladores en tiempo real.", "de": "Umfassendstes Hardware-Monitoring. CPU/GPU-Temps, Spannungen, Luefter in Echtzeit.", "ar": "أشمل أداة مراقبة. درجات حرارة CPU/GPU, فولتية, مراوح."},
    "Install CPU-Z": {"en": "Lightweight CPU identification tool. Shows detailed CPU, memory, motherboard and SPD info at a glance.", "fr": "Outil d'identification CPU leger. Affiche CPU, memoire, carte mere et SPD.", "tn": "Outil khfif lel CPU. Ywari CPU, memoire, carte mere w SPD fel blasa.", "es": "Herramienta ligera de identificacion de CPU. Muestra CPU, memoria y placa base.", "de": "Leichtes CPU-Identifikationstool. Zeigt CPU, RAM, Mainboard und SPD.", "ar": "أداة خفيفة لمعرفة CPU. تعرض CPU, ذاكرة, لوحة أم."},
    "Install GPU-Z": {"en": "GPU identification and monitoring tool. Shows GPU specs, BIOS version, clock speeds, VRAM info and sensor data.", "fr": "Outil d'identification GPU. Affiche specs GPU, version BIOS, horloges et capteurs.", "tn": "Outil lel GPU. Ywari specs GPU, BIOS, clocks, VRAM w capteurs.", "es": "Herramienta de identificacion GPU. Muestra specs GPU, version BIOS, relojes y sensores.", "de": "GPU-Identifikation und Monitoring. GPU-Specs, BIOS, Taktraten und Sensoren.", "ar": "أداة لمعرفة GPU. تعرض مواصفات GPU, BIOS, سرعات."},
    "Install Process Explorer": {"en": "Sysinternals advanced task manager. Shows DLL handles, process trees, GPU per-process usage. Far beyond Task Manager.", "fr": "Gestionnaire de taches avance Sysinternals. Arbres de processus, DLLs, GPU par processus.", "tn": "Task manager avance Sysinternals. Arbres processus, DLLs, GPU par processus. A7sen mel Task Manager.", "es": "Gestor de tareas avanzado Sysinternals. Arboles de procesos, DLLs, GPU por proceso.", "de": "Erweiterter Sysinternals Task-Manager. Prozessbaeume, DLLs, GPU pro Prozess.", "ar": "مدير مهام متقدم. شجرة العمليات, DLLs, GPU لكل عملية."},
    "Install Autoruns": {"en": "Sysinternals startup manager. Shows EVERY auto-start entry: services, drivers, scheduled tasks, shell extensions. The ultimate cleanup tool.", "fr": "Gestionnaire demarrage Sysinternals. Montre CHAQUE entree auto-start: services, pilotes, taches.", "tn": "Gestionnaire demarrage Sysinternals. Ywari KOL les entries demarrage: services, drivers, taches.", "es": "Gestor de inicio Sysinternals. Muestra CADA entrada de inicio: servicios, drivers, tareas.", "de": "Sysinternals Autostart-Manager. Zeigt JEDEN Autostart-Eintrag: Dienste, Treiber, Aufgaben.", "ar": "مدير بدء التشغيل. يعرض كل إدخال تشغيل تلقائي."},
    "Install WizTree": {"en": "Fastest disk space analyzer. Uses MFT to scan in seconds what WinDirStat takes minutes. Underrated gem.", "fr": "Analyseur d'espace disque le plus rapide. Utilise MFT pour scanner en secondes.", "tn": "A7sen w asra3 disk analyzer. Yesta3mel MFT. Yscanniha fi secondes. Gem underrated.", "es": "Analizador de espacio mas rapido. Usa MFT para escanear en segundos.", "de": "Schnellster Speicherplatzanalysator. Nutzt MFT fuer Scan in Sekunden.", "ar": "أسرع محلل مساحة قرص. يستخدم MFT للفحص في ثوان."},
    "Install MSI Afterburner": {"en": "GPU overclocking, undervolting and monitoring tool by MSI. Real-time OSD overlay for FPS, temps, usage in games.", "fr": "Outil d'overclocking et monitoring GPU par MSI. OSD en temps reel pour FPS et temperatures.", "tn": "Outil overclocking GPU MSI. OSD en temps reel lel FPS, temperatures w usage fi les jeux.", "es": "Herramienta de overclocking GPU de MSI. OSD en tiempo real para FPS y temperaturas.", "de": "GPU-Overclocking und Monitoring von MSI. Echtzeit-OSD fuer FPS, Temps in Spielen.", "ar": "أداة كسر سرعة GPU. OSD في الوقت الحقيقي للألعاب."},
    "Install NVCleanstall": {"en": "Clean NVIDIA driver installer. Strips telemetry, GeForce Experience, and bloat from the driver package. Installs only what you need.", "fr": "Installateur propre de pilotes NVIDIA. Supprime telemetrie et GeForce Experience.", "tn": "Installateur propre NVIDIA. Yna77i telemetrie, GeForce Experience w el bloat mel driver.", "es": "Instalador limpio de drivers NVIDIA. Elimina telemetria y GeForce Experience.", "de": "Sauberer NVIDIA-Treiberinstaller. Entfernt Telemetrie und GeForce Experience.", "ar": "مثبت تعريفات NVIDIA نظيف. يزيل التليمتري وGeForce Experience."},
    "Install Bulk Crap Uninstaller": {"en": "Mass uninstaller that detects leftover files, registry entries and orphan folders. Cleans what normal uninstall misses.", "fr": "Desinstalleur en masse. Detecte fichiers residuels, registres et dossiers orphelins.", "tn": "Desinstalleur en masse. Yla99a fichiers residuels, registres w dossiers orphelins.", "es": "Desinstalador masivo. Detecta archivos residuales, registros y carpetas huerfanas.", "de": "Massen-Deinstaller. Erkennt Restdateien, Registrierungseintraege und Ordner.", "ar": "مزيل برامج جماعي. يكتشف الملفات والسجلات المتبقية."},
    "Install ShareX": {"en": "Screenshot and screen recording tool with auto-upload, annotation, OCR. Replaces Snipping Tool, Greenshot and more.", "fr": "Capture d'ecran et enregistrement avec upload auto, annotation et OCR.", "tn": "Capture d'ecran w enregistrement. Upload auto, annotation, OCR. Y3awwedh Snipping Tool.", "es": "Captura de pantalla y grabacion con subida auto, anotacion y OCR.", "de": "Screenshot- und Aufnahmetool mit Auto-Upload, Anmerkungen und OCR.", "ar": "أداة لقطات الشاشة مع رفع تلقائي وOCR."},
    "Install Notepad++": {"en": "Powerful text editor with syntax highlighting, regex search, macros, plugins. Essential for config file editing.", "fr": "Editeur de texte puissant avec coloration syntaxique, regex, macros et plugins.", "tn": "Editeur de texte puissant. Coloration syntaxique, regex, macros w plugins.", "es": "Editor de texto potente con resaltado de sintaxis, regex, macros y plugins.", "de": "Leistungsstarker Texteditor mit Syntaxhervorhebung, Regex, Makros und Plugins.", "ar": "محرر نصوص قوي مع تلوين الصيغة وregex وإضافات."},
    "Install Rufus": {"en": "Create bootable USB drives from ISOs. Supports UEFI, GPT, MBR. The standard tool for Windows/Linux install media.", "fr": "Cree des cles USB bootables depuis des ISOs. Supporte UEFI, GPT, MBR.", "tn": "Ya3mel USB bootable men ISO. Supporte UEFI, GPT, MBR. Standard lel install Windows/Linux.", "es": "Crea USBs arrancables desde ISOs. Soporta UEFI, GPT, MBR.", "de": "Erstellt bootfaehige USB-Laufwerke aus ISOs. Unterstuetzt UEFI, GPT, MBR.", "ar": "ينشئ USB قابل للإقلاع من ISO. يدعم UEFI, GPT, MBR."},
    "Install CrystalDiskInfo": {"en": "S.M.A.R.T. disk health monitor. Warns you before your SSD or HDD fails. Tracks temperature, reallocated sectors, power-on hours.", "fr": "Moniteur de santé S.M.A.R.T. Prévient avant la panne de disque.", "tn": "Moniteur santé disque S.M.A.R.T. Y3arfek 9bal ma disque yet7asser.", "es": "Monitor de salud S.M.A.R.T. Avisa antes de que falle el disco.", "de": "S.M.A.R.T. Festplattengesundheitsmonitor. Warnt vor Laufwerksausfall.", "ar": "مراقب صحة القرص S.M.A.R.T. ينبهك قبل تلف القرص."},
    "Install CrystalDiskMark": {"en": "SSD/HDD speed benchmark. Tests sequential and random read/write speeds. Essential after installing a new drive.", "fr": "Benchmark vitesse SSD/HDD. Teste lecture/écriture séquentielle et aléatoire.", "tn": "Benchmark vitesse SSD/HDD. Ytesti lecture/écriture. Lazem ki trakkeb disque jdid.", "es": "Benchmark de velocidad SSD/HDD. Prueba lectura/escritura secuencial y aleatoria.", "de": "SSD/HDD Geschwindigkeitsbenchmark. Testet sequentielles und zufälliges Lesen/Schreiben.", "ar": "اختبار سرعة SSD/HDD. يختبر القراءة/الكتابة التسلسلية والعشوائية."},
    "Install HWMonitor": {"en": "Real-time CPU/GPU/RAM temperature, voltage and fan speed monitor by CPUID. Lightweight and accurate.", "fr": "Moniteur temps réel CPU/GPU/RAM: températures, voltages, ventilateurs.", "tn": "Moniteur temperatures CPU/GPU/RAM, voltages w ventilateurs fi waqt 7a9i9i.", "es": "Monitor en tiempo real de temperaturas CPU/GPU/RAM, voltajes y ventiladores.", "de": "Echtzeit CPU/GPU/RAM Temperatur-, Spannungs- und Lüftermonitor von CPUID.", "ar": "مراقب حرارة CPU/GPU/RAM وفولتية وسرعة المراوح."},
    "Install UniGetUI": {"en": "GUI for managing winget, scoop, chocolatey, npm and pip packages all in one place. Browse, install, update, uninstall visually.", "fr": "Interface graphique pour gérer winget, scoop, chocolatey, npm et pip en un seul endroit.", "tn": "Interface graphique lel winget, scoop, chocolatey, npm w pip f blaça wa7da.", "es": "Interfaz gráfica para gestionar winget, scoop, chocolatey, npm y pip en un solo lugar.", "de": "GUI für winget, scoop, chocolatey, npm und pip Pakete an einem Ort.", "ar": "واجهة رسومية لإدارة حزم winget, scoop, chocolatey, npm وpip."},
    "Install Ventoy": {"en": "Multi-boot USB creator. Just drop ISO files onto the USB drive — no reformatting needed. Supports 900+ ISOs simultaneously.", "fr": "Créateur USB multi-boot. Déposez les ISOs sur la clé USB, pas de reformatage.", "tn": "Ya3mel USB multi-boot. 7ot les ISOs 3al USB, bla reformatage.", "es": "Creador USB multi-arranque. Solo arrastra ISOs al USB sin reformatear.", "de": "Multi-Boot-USB-Ersteller. ISOs auf USB ziehen, kein Neuformatieren nötig.", "ar": "منشئ USB متعدد الإقلاع. ضع ملفات ISO على USB بدون تهيئة."},
    "Install Flow Launcher": {"en": "Spotlight-like quick launcher for Windows. Search apps, files, web, calculations, everything from Alt+Space. Highly extensible with plugins.", "fr": "Lanceur rapide comme Spotlight. Cherche applis, fichiers, web depuis Alt+Espace.", "tn": "Lanceur rapide kima Spotlight. Yfattech applis, fichiers, web mel Alt+Espace.", "es": "Lanzador rápido estilo Spotlight. Busca apps, archivos, web desde Alt+Espacio.", "de": "Spotlight-ähnlicher Schnellstarter. Apps, Dateien, Web suchen per Alt+Leertaste.", "ar": "مشغل سريع مثل Spotlight. بحث تطبيقات، ملفات، ويب من Alt+Space."},
    "Install EarTrumpet": {"en": "Per-app volume control from system tray. Way better than the default Windows volume mixer. Drag to set volume per app.", "fr": "Contrôle du volume par application. Bien meilleur que le mixeur Windows par défaut.", "tn": "Contrôle volume par application. A7sen barcha mel mixeur Windows.", "es": "Control de volumen por aplicación. Mucho mejor que el mezclador de Windows.", "de": "Lautstärkeregelung pro App. Viel besser als der Windows-Mixer.", "ar": "تحكم بالصوت لكل تطبيق. أفضل من خلاط Windows."},
    "Install TCPView": {"en": "Sysinternals real-time network connections viewer. See every TCP/UDP endpoint, process, port, state. Find what's phoning home.", "fr": "Visualiseur de connexions réseau Sysinternals. Voir chaque point TCP/UDP et processus.", "tn": "Visualiseur connexions réseau Sysinternals. Tchouf kol TCP/UDP endpoint w processus.", "es": "Visor de conexiones de red Sysinternals. Ver cada endpoint TCP/UDP y proceso.", "de": "Sysinternals Netzwerkverbindungs-Viewer. TCP/UDP Endpunkte und Prozesse sehen.", "ar": "عارض اتصالات الشبكة. يعرض كل نقطة TCP/UDP وعملية."},
    "Install O&O ShutUp10++": {"en": "The ultimate Windows privacy tool. Toggles 150+ telemetry, tracking, and data-collection settings with one click. Free, portable, no install needed. Every PC tweaker NEEDS this.", "fr": "L'outil ultime de confidentialité Windows. Bascule 150+ réglages télémétrie et tracking en un clic. Gratuit, portable.", "tn": "A7sen outil lel privacy fi Windows. Ybeddel 150+ réglages télémétrie w tracking b click wa7ed. Majjani w portable.", "es": "La herramienta definitiva de privacidad Windows. Alterna 150+ ajustes de telemetría con un clic. Gratis y portable.", "de": "Das ultimative Windows-Datenschutztool. Schaltet 150+ Telemetrie- und Tracking-Einstellungen um. Kostenlos, portabel.", "ar": "أداة الخصوصية المثلى لـ Windows. تبديل 150+ إعداد تليمتري وتتبع بنقرة واحدة. مجانية ومحمولة."},
    "Install Process Monitor": {"en": "Sysinternals deep system tracer. Logs every file, registry, network and process operation in real-time. The #1 debugging tool for Windows internals.", "fr": "Traceur système profond Sysinternals. Log chaque opération fichier, registre, réseau en temps réel.", "tn": "Traceur système profond Sysinternals. Y3abbi kol opération fichier, registre, réseau fi waqt 7a9i9i.", "es": "Trazador de sistema profundo Sysinternals. Registra cada operación de archivo, registro y red en tiempo real.", "de": "Sysinternals System-Tracer. Protokolliert jede Datei-, Registry- und Netzwerkoperation in Echtzeit.", "ar": "متتبع نظام عميق Sysinternals. يسجل كل عملية ملف وسجل وشبكة في الوقت الحقيقي."},
    "Install Revo Uninstaller": {"en": "Deep uninstaller that scans for leftover files, folders, and registry entries AFTER normal uninstall. Finds what Add/Remove Programs misses.", "fr": "Désinstalleur profond. Scanne les fichiers, dossiers et registres résiduels après désinstallation normale.", "tn": "Désinstalleur profond. Yscanniha fichiers, dossiers w registres eli yeb9aw ba3d désinstallation normale.", "es": "Desinstalador profundo. Escanea archivos, carpetas y registros residuales después de la desinstalación normal.", "de": "Tiefer Deinstaller. Scannt nach Restdateien, Ordnern und Registry-Einträgen nach normaler Deinstallation.", "ar": "مزيل برامج عميق. يفحص الملفات والمجلدات والسجلات المتبقية بعد الإزالة العادية."},
    "Install Snappy Driver Installer": {"en": "Offline driver updater with massive driver packs. No internet needed for updates. Finds missing/outdated drivers automatically. Extremely underrated for fresh installs.", "fr": "Mise à jour de pilotes hors-ligne avec packs massifs. Pas besoin d'internet. Très sous-estimé pour les installations fraîches.", "tn": "Mise à jour drivers offline b driver packs kbar. Bla internet. Yla99a drivers na9sin/9dom. Très underrated lel fresh install.", "es": "Actualizador de drivers offline con packs masivos. Sin internet. Encuentra drivers faltantes/anticuados automáticamente.", "de": "Offline-Treiberupdater mit riesigen Treiberpaketen. Kein Internet nötig. Extrem unterschätzt für Neuinstallationen.", "ar": "محدث تعريفات بدون إنترنت مع حزم ضخمة. يجد التعريفات المفقودة/القديمة تلقائياً."},
    "Install ExplorerPatcher": {"en": "Restores Windows 10 taskbar, start menu, and UI elements on Windows 11. Fixes every annoying Win11 regression. A must for Win11 power users.", "fr": "Restaure la barre des tâches et le menu démarrer de Windows 10 sur Windows 11. Corrige chaque régression Win11.", "tn": "Yrjaa3 taskbar w start menu Windows 10 3al Windows 11. Ysal7 kol régression Win11.", "es": "Restaura la barra de tareas y menú inicio de Windows 10 en Windows 11. Corrige cada regresión de Win11.", "de": "Stellt Windows 10 Taskbar und Startmenü auf Windows 11 wieder her. Behebt jede Win11-Regression.", "ar": "يستعيد شريط المهام وقائمة البدء من Windows 10 على Windows 11. يصلح كل تراجع في Win11."},
    "Install QuickLook": {"en": "Press Spacebar to preview ANY file in Explorer — images, PDFs, Office docs, code, videos. Just like macOS Quick Look. Zero-click file preview.", "fr": "Appuyez sur Espace pour prévisualiser N'IMPORTE QUEL fichier dans l'Explorateur. Comme Quick Look sur macOS.", "tn": "O9ros Espace bach tchouf n'importe quel fichier fel Explorateur — images, PDFs, code, vidéos. Kima macOS.", "es": "Presiona Espacio para previsualizar CUALQUIER archivo en el Explorador. Como Quick Look en macOS.", "de": "Leertaste drücken für Vorschau JEDER Datei im Explorer — Bilder, PDFs, Code, Videos. Wie macOS Quick Look.", "ar": "اضغط المسافة لمعاينة أي ملف في المستكشف — صور, PDF, مستندات, فيديو. مثل macOS."},
    "Install Ditto Clipboard": {"en": "Clipboard history manager that saves EVERYTHING you copy. Search through past clipboard entries, pin favorites, sync across machines. Ctrl+` to access.", "fr": "Gestionnaire d'historique presse-papier. Sauvegarde TOUT ce que vous copiez. Recherchez les entrées passées.", "tn": "Gestionnaire historique presse-papier. Y7afdh KOL 7aja tcoppiha. Fattach fel historique, pin favorites.", "es": "Gestor de historial del portapapeles. Guarda TODO lo que copias. Busca entradas pasadas, fija favoritos.", "de": "Zwischenablage-Verlaufsmanager. Speichert ALLES was Sie kopieren. Vergangene Einträge durchsuchen.", "ar": "مدير سجل الحافظة. يحفظ كل ما تنسخه. ابحث في الإدخالات السابقة."},
    "Install LatencyMon": {"en": "Real-time DPC latency monitor. Identifies which kernel driver causes audio glitches, mouse stuttering, or input lag. The #1 diagnostic tool for latency issues. If you tweak for performance, you NEED this.", "fr": "Moniteur de latence DPC en temps réel. Identifie quel pilote noyau cause crachotements audio ou lag d'entrée. L'outil #1 pour diagnostiquer la latence.", "tn": "Moniteur latence DPC fi waqt 7a9i9i. Yla99a quel driver noyau ysabbeb lag audio wella mouse stuttering. Outil #1 lel latence.", "es": "Monitor de latencia DPC en tiempo real. Identifica qué driver del kernel causa chasquidos de audio o lag de entrada. La herramienta #1.", "de": "Echtzeit-DPC-Latenzmonitor. Identifiziert welcher Kerneltreiber Audio-Knacken oder Eingabeverzögerung verursacht.", "ar": "مراقب زمن استجابة DPC. يحدد أي تعريف نواة يسبب تقطع الصوت أو تأخر الإدخال."},
    "Install Process Lasso": {"en": "Automatic process priority and CPU affinity optimizer. ProBalance algorithm prevents system hangs from runaway processes. SmartTrim reduces latency spikes. The most underrated anti-stutter tool.", "fr": "Optimiseur automatique de priorité et affinité CPU des processus. ProBalance empêche les blocages. SmartTrim réduit les pics de latence.", "tn": "Optimiseur automatique priorité w affinité CPU. ProBalance ymanea el blocages. SmartTrim yna99es pics latence. A7sen outil anti-stutter.", "es": "Optimizador automático de prioridad y afinidad CPU. ProBalance previene bloqueos. SmartTrim reduce picos de latencia.", "de": "Automatischer Prozesspriorität- und CPU-Affinitäts-Optimizer. ProBalance verhindert Systemhänger. SmartTrim reduziert Latenzspitzen.", "ar": "محسن أولويات العمليات وتقارب المعالج تلقائياً. يمنع تجمد النظام ويقلل قفزات التأخير."},
    "Install ParkControl": {"en": "Controls CPU core parking and frequency scaling. Windows parks cores to save power, causing micro-stutters in games. This tool keeps cores awake when you need them. Must-have for competitive gaming.", "fr": "Contrôle le parking des cœurs CPU. Windows met en veille les cœurs pour économiser l'énergie, causant des micro-saccades. Garde-les actifs quand nécessaire.", "tn": "Ycontroliha CPU core parking. Windows yna3es les cœurs lel économie, ysabbeb micro-stutters. Ykhallihoum 9aymin ki tlazem.", "es": "Controla el estacionamiento de núcleos CPU. Windows apaga núcleos para ahorrar energía, causando micro-tartamudeos. Los mantiene activos.", "de": "Steuert CPU Core Parking. Windows parkt Kerne zum Stromsparen, was Mikro-Ruckler verursacht. Hält Kerne wach wenn nötig.", "ar": "يتحكم في إيقاف أنوية المعالج. Windows يوقف الأنوية لتوفير الطاقة مسبباً تقطعات. يبقيها نشطة عند الحاجة."},
    "Install ThrottleStop": {"en": "Advanced Intel CPU undervolt and throttle-bypass tool. Unlock sustained turbo clocks, disable power throttling, reduce temperatures by 10-20°C with undervolting. Not for beginners — but insanely powerful.", "fr": "Outil avancé d'undervolt et bypass throttle Intel. Débloque turbo soutenu, désactive le throttling, réduit les températures de 10-20°C.", "tn": "Outil avancé undervolt w bypass throttle Intel. Yfetak turbo soutenu, ytaffi power throttling, yna99es 7arara 10-20°C.", "es": "Herramienta avanzada de undervolt Intel. Desbloquea turbo sostenido, desactiva throttling, reduce temperaturas 10-20°C.", "de": "Fortgeschrittenes Intel CPU Undervolt- und Throttle-Bypass-Tool. Entsperrt Turbo, deaktiviert Throttling, senkt Temperaturen um 10-20°C.", "ar": "أداة متقدمة لخفض فولتية معالجات Intel. فتح تيربو مستدام وتقليل الحرارة 10-20 درجة."},
    "Install RTSS": {"en": "RivaTuner Statistics Server — the lowest-latency frame limiter in existence. Scanline sync eliminates tearing without V-Sync input lag. OSD overlay shows FPS, frametime, CPU/GPU usage. Used by every serious benchmarker.", "fr": "Limiteur de FPS à la latence la plus basse. Scanline sync élimine le tearing sans le lag V-Sync. OSD montre FPS et frametime.", "tn": "Limiteur FPS b a9all latence mawjouda. Scanline sync yna77i tearing bla V-Sync lag. OSD ywari FPS w frametime.", "es": "Limitador de FPS con la menor latencia. Scanline sync elimina tearing sin lag de V-Sync. OSD muestra FPS y frametime.", "de": "Frame-Limiter mit niedrigster Latenz. Scanline Sync eliminiert Tearing ohne V-Sync-Lag. OSD zeigt FPS und Frametime.", "ar": "محدد إطارات بأقل تأخير. يزيل التمزق بدون تأخير V-Sync. OSD يعرض FPS وزمن الإطار."},
    "Install CapFrameX": {"en": "Advanced frame time capture and analysis. Records individual frame times to reveal stutters that average FPS counters miss. Compare hardware configs, detect 1% lows, export to CSV. The serious benchmarker's secret weapon.", "fr": "Analyse avancée des temps de frame. Enregistre chaque temps de frame pour révéler les saccades que les compteurs FPS moyens manquent.", "tn": "Analyse avancée frame times. Y3abbi kol frame time bash yla99a stutters eli FPS counter ma ychoufhomch.", "es": "Análisis avanzado de tiempo de frame. Graba tiempos individuales para revelar tartamudeos que los contadores FPS promedian ocultan.", "de": "Fortgeschrittene Frametime-Analyse. Zeichnet individuelle Framezeiten auf, um Ruckler zu finden die FPS-Counter übersehen.", "ar": "تحليل متقدم لأزمنة الإطارات. يسجل كل إطار لكشف التقطعات التي يخفيها عداد FPS العادي."},
    "Install DDU": {"en": "Display Driver Uninstaller — completely removes NVIDIA/AMD/Intel GPU drivers, registry entries, and leftover files. The ONLY way to do a truly clean driver install. Run in Safe Mode for best results.", "fr": "Supprime complètement les pilotes GPU et fichiers résiduels. La SEULE façon de faire une installation propre de pilotes.", "tn": "Yna77i drivers GPU complet — NVIDIA/AMD/Intel. El SEULE façon ta3mel clean install driver. 5admha fi Safe Mode.", "es": "Elimina completamente drivers GPU y archivos residuales. La ÚNICA forma de hacer una instalación limpia de drivers.", "de": "Entfernt GPU-Treiber vollständig. Der EINZIGE Weg für eine saubere Treiberinstallation. Im abgesicherten Modus ausführen.", "ar": "يزيل تعريفات GPU بالكامل. الطريقة الوحيدة لتثبيت تعريف نظيف. شغّله في الوضع الآمن."},
    "Install Sysmon": {"en": "Sysinternals System Monitor — kernel-level logging of process creation, network connections, file changes, and registry modifications. The gold standard for threat hunting and audit trails. Most people don't know this exists.", "fr": "Moniteur système niveau noyau. Log création processus, connexions réseau, modifications fichiers/registre. Standard pour la chasse aux menaces.", "tn": "Moniteur système niveau noyau. Y3abbi création processus, connexions réseau, modifications fichiers/registre. La plupart manajemch.", "es": "Monitor de sistema a nivel kernel. Registra creación de procesos, conexiones de red, cambios en archivos/registro.", "de": "Systemmonitor auf Kernel-Ebene. Protokolliert Prozesserstellung, Netzwerkverbindungen, Datei-/Registry-Änderungen.", "ar": "مراقب نظام على مستوى النواة. يسجل إنشاء العمليات واتصالات الشبكة وتغييرات الملفات والسجل."},
    "Install Sophia Script": {"en": "The most powerful open-source Windows tweaking script on GitHub. 150+ optimizations: disable telemetry, remove bloatware, configure privacy, optimize performance. Used by IT professionals worldwide. The mother of all tweakers.", "fr": "Le script de tweaking Windows open-source le plus puissant. 150+ optimisations: télémétrie, bloatware, confidentialité, performances.", "tn": "A9wa script tweaking Windows open-source. 150+ optimisations: télémétrie, bloatware, confidentialité, performances. IT professionals y7ebouh.", "es": "El script de tweaking Windows más potente. 150+ optimizaciones: telemetría, bloatware, privacidad, rendimiento.", "de": "Das leistungsstärkste Open-Source Windows-Tweaking-Skript. 150+ Optimierungen: Telemetrie, Bloatware, Datenschutz, Leistung.", "ar": "أقوى سكريبت تحسين Windows مفتوح المصدر. 150+ تحسين: تليمتري، برامج غير مرغوبة، خصوصية، أداء."},
    "Install privacy.sexy": {'en': 'Open-source tool to enforce privacy and security on Windows and macOS. Generates and runs scripts that disable tracking, telemetry, and bloatware. Curated community scripts — transparent and auditable. The privacy hardening tool for the paranoid.', 'fr': 'Outil open-source pour la confidentialité et la sécurité Windows/macOS. Génère des scripts anti-tracking et anti-télémétrie.', 'tn': 'Outil open-source lel confidentialité w sécurité Windows/macOS. Ygénère scripts anti-tracking w anti-télémétrie.', 'es': 'Herramienta open-source para privacidad y seguridad en Windows/macOS. Genera scripts anti-rastreo y anti-telemetría.', 'de': 'Open-Source-Tool für Datenschutz und Sicherheit auf Windows/macOS. Generiert Anti-Tracking- und Anti-Telemetrie-Skripte.', 'ar': 'أداة مفتوحة المصدر للخصوصية والأمان على Windows/macOS. تولد سكريبتات ضد التتبع والتليمتري.'},
    "Install simplewall": {"en": "Lightweight firewall configurator using Windows Filtering Platform. Block any process from connecting to the internet with one click. See exactly what's phoning home. No bloat, no ads, just pure network control.", "fr": "Configurateur de pare-feu léger via WFP. Bloquez tout processus d'accéder à Internet en un clic. Voyez ce qui communique.", "tn": "Configurateur pare-feu khfif via WFP. Bloquer n'importe quel processus mel internet b click wa7ed. Tchouf chkoun ytéléphoni.", "es": "Configurador de firewall ligero via WFP. Bloquea cualquier proceso de conectarse a internet con un clic.", "de": "Leichter Firewall-Konfigurator über WFP. Jeden Prozess mit einem Klick blockieren. Sehen was nach Hause telefoniert.", "ar": "أداة جدار ناري خفيفة عبر WFP. حظر أي عملية من الاتصال بالإنترنت بنقرة واحدة."},
    "Install Portmaster": {"en": "Free open-source application firewall with system-wide tracker blocking and DNS privacy. See every network connection per-app, auto-block known trackers, use encrypted DNS. Like Pi-hole but built into your PC.", "fr": "Pare-feu applicatif open-source avec blocage trackers et DNS privé. Voir chaque connexion par appli, bloquer les trackers connus.", "tn": "Pare-feu applicatif open-source. Ychouf kol connexion par appli, ybloki trackers connus, DNS crypté. Kima Pi-hole fi PC.", "es": "Firewall de aplicación open-source con bloqueo de rastreadores y DNS privado. Ver cada conexión por app.", "de": "Open-Source-Application-Firewall mit Tracker-Blocking und DNS-Privatsphäre. Jede Verbindung pro App sehen.", "ar": "جدار ناري مفتوح المصدر مع حظر المتتبعات وخصوصية DNS. عرض كل اتصال لكل تطبيق."},
    "Install Mem Reduct": {"en": "Lightweight real-time memory management tool. Purges the standby list and working set to prevent memory-related stuttering. Auto-cleans when usage exceeds threshold. Like ISLC but always on winget.", "fr": "Outil de gestion mémoire léger. Purge la standby list pour empêcher les saccades liées à la mémoire. Nettoyage auto quand le seuil est dépassé.", "tn": "Outil gestion mémoire khfif. Yfarregh el standby list bash ymanea stuttering mémoire. Nettoyage auto ki ywassal el seuil.", "es": "Herramienta ligera de gestión de memoria. Purga la standby list para prevenir tartamudeos. Limpieza automática cuando supera el umbral.", "de": "Leichtes Speichermanagement-Tool. Löscht Standby-Liste um speicherbedingtes Ruckeln zu verhindern. Auto-Bereinigung bei Schwellenwert.", "ar": "أداة إدارة ذاكرة خفيفة. تنظف قائمة الانتظار لمنع التقطع. تنظيف تلقائي عند تجاوز الحد."},
    "Install CRU": {"en": "Custom Resolution Utility — create resolutions and refresh rates your monitor claims it doesn't support. Unlock hidden modes, add ultra-low resolutions for competitive gaming, force specific timings. Power users only.", "fr": "Créez des résolutions et taux de rafraîchissement que votre écran dit ne pas supporter. Débloquez les modes cachés.", "tn": "Ya3mel résolutions w refresh rates eli el écran ta3ek ygoulek ma ysupporthomch. Yfetak modes cachés.", "es": "Crea resoluciones y tasas de refresco que tu monitor dice no soportar. Desbloquea modos ocultos.", "de": "Erstellt Auflösungen und Bildwiederholraten die Ihr Monitor angeblich nicht unterstützt. Versteckte Modi freischalten.", "ar": "إنشاء دقات عرض ومعدلات تحديث لا يدعمها شاشتك ظاهرياً. فتح الأوضاع المخفية."},
    "Install CompactGUI": {"en": "GUI for Windows NTFS transparent compression. Compress game folders by 30-60% with ZERO performance impact (often faster due to less disk I/O). Algorithm selection: XPRESS4K, XPRESS8K, XPRESS16K, LZX. Saves hundreds of GB.", "fr": "Compression NTFS transparente pour les jeux. Compressez les dossiers de 30-60% sans impact sur les performances. Économisez des centaines de Go.", "tn": "Compression NTFS transparente lel jeux. Compresser dossiers jeux 30-60% bla impact performances. Y7awlok des centaines de Go.", "es": "Compresión NTFS transparente para juegos. Comprime carpetas 30-60% sin impacto en rendimiento. Ahorra cientos de GB.", "de": "NTFS-Transparenzkompression für Spiele. Ordner um 30-60% komprimieren ohne Performance-Einbußen. Hunderte GB sparen.", "ar": "ضغط NTFS شفاف للألعاب. ضغط المجلدات 30-60% بدون تأثير على الأداء. توفير مئات الجيجابايت."},
    "Install GlassWire": {"en": "Beautiful real-time network monitor and firewall. Visual timeline of every connection, per-app bandwidth usage, alerts for new connections. Catches background apps eating your bandwidth you never knew about.", "fr": "Moniteur réseau et pare-feu visuel en temps réel. Timeline de chaque connexion, usage bande passante par appli, alertes.", "tn": "Moniteur réseau w pare-feu visuel fi waqt 7a9i9i. Timeline kol connexion, usage bandwidth par appli, alertes.", "es": "Monitor de red y firewall visual en tiempo real. Timeline de cada conexión, uso de ancho de banda por app, alertas.", "de": "Echtzeit-Netzwerkmonitor und Firewall. Visuelle Timeline jeder Verbindung, Bandbreitennutzung pro App, Warnungen.", "ar": "مراقب شبكة مرئي في الوقت الحقيقي. عرض مخطط زمني لكل اتصال واستخدام النطاق الترددي لكل تطبيق."},
    "Install WPD": {"en": "Windows Privacy Dashboard — disable telemetry services, block Microsoft tracking IPs via firewall rules, remove preinstalled UWP apps. All in a single clean portable tool. Like ShutUp10 but with network-level blocking.", "fr": "Tableau de bord Windows Privacy. Désactive les services télémétrie, bloque les IPs Microsoft, supprime les UWP pré-installées.", "tn": "Windows Privacy Dashboard. Ytaffi services télémétrie, ybloki IPs Microsoft, yna77i UWP pré-installées.", "es": "Windows Privacy Dashboard. Desactiva servicios de telemetría, bloquea IPs de Microsoft, elimina apps UWP preinstaladas.", "de": "Windows Privacy Dashboard. Telemetrie-Dienste deaktivieren, Microsoft-IPs blockieren, UWP-Apps entfernen.", "ar": "لوحة خصوصية Windows. تعطيل خدمات التليمتري وحظر عناوين Microsoft وإزالة تطبيقات UWP المثبتة مسبقاً."},
    "Install LosslessCut": {"en": "Lossless video editor — trim, cut, and merge videos WITHOUT re-encoding. Instant processing regardless of file size. Supports every format via FFmpeg. Saves HOURS compared to traditional editors.", "fr": "Éditeur vidéo lossless. Couper et fusionner les vidéos SANS ré-encodage. Traitement instantané quelle que soit la taille.", "tn": "Éditeur vidéo lossless. Y9otaa3 w yjam3a vidéos BLA ré-encodage. Traitement instantané quel que soit la taille.", "es": "Editor de video sin pérdida. Corta y fusiona videos SIN recodificar. Procesamiento instantáneo sin importar el tamaño.", "de": "Verlustfreier Video-Editor. Videos schneiden und zusammenführen OHNE Neu-Encoding. Sofortige Verarbeitung unabhängig von Dateigröße.", "ar": "محرر فيديو بدون فقدان. قص ودمج الفيديو بدون إعادة ترميز. معالجة فورية بغض النظر عن الحجم."},
    "Install AutoHotkey": {"en": "The ultimate Windows automation scripting language. Remap any key, create macros, auto-type text expansions, build custom GUIs, automate repetitive tasks. The power-user's Swiss army knife. If you're not using AHK, you're wasting time.", "fr": "Le langage d'automatisation ultime pour Windows. Remapper les touches, créer des macros, expansions texte, GUIs, automatiser.", "tn": "A7sen langage automatisation lel Windows. Ybeddel les touches, ya3mel macros, expansions texte, automatiser taches.", "es": "El lenguaje de automatización definitivo para Windows. Remapear teclas, crear macros, expansiones de texto, automatizar.", "de": "Die ultimative Windows-Automatisierungssprache. Tasten umbelegen, Makros erstellen, Textexpansionen, GUIs bauen.", "ar": "لغة أتمتة Windows المطلقة. إعادة تعيين المفاتيح وإنشاء ماكرو وتوسيع النصوص وأتمتة المهام."},
    "Install WizFile": {"en": "Ultra-fast file search tool by the WizTree developers. Uses MFT (Master File Table) to find ANY file on your NTFS drives in milliseconds. Faster than Everything for simple searches. Lightweight and portable.", "fr": "Recherche de fichiers ultra-rapide par les développeurs de WizTree. Utilise MFT pour trouver n'importe quel fichier en millisecondes.", "tn": "Recherche fichiers ultra-rapide mel WizTree devs. Yesta3mel MFT bash yla99a n'importe quel fichier fi millisecondes.", "es": "Búsqueda de archivos ultrarrápida por los desarrolladores de WizTree. Usa MFT para encontrar cualquier archivo en milisegundos.", "de": "Ultraschnelle Dateisuche von den WizTree-Entwicklern. Nutzt MFT um jede Datei in Millisekunden zu finden.", "ar": "بحث فائق السرعة عن الملفات. يستخدم MFT للعثور على أي ملف في ميلي ثانية."},
    "Install dupeGuru": {"en": "Intelligent duplicate file finder. Scans by content hash, not just filename. Finds duplicate photos by visual similarity. Reference-based deletion keeps the best copy. Recovers GBs of wasted space.", "fr": "Détecteur intelligent de fichiers dupliqués. Scan par hash de contenu. Trouve les photos similaires visuellement. Récupère des Go.", "tn": "Détecteur fichiers dupliqués. Yscanniha par hash contenu. Yla99a photos similaires visuellement. Ystarj3aa des Go.", "es": "Buscador inteligente de archivos duplicados. Escanea por hash de contenido. Encuentra fotos duplicadas visualmente.", "de": "Intelligenter Duplikat-Finder. Scannt nach Content-Hash. Findet ähnliche Fotos visuell. Stellt GBs verschwendeten Speicher frei.", "ar": "كاشف ملفات مكررة ذكي. يفحص بتجزئة المحتوى ويجد الصور المتشابهة بصرياً. يستعيد جيجابايت مهدرة."},
    "Install FanControl": {"en": "Create custom fan curves for ANY fan connected to ANY sensor. Mix-and-match CPU temp to case fans, GPU temp to AIO pump. Replaces 5 vendor apps with one universal solution. Open-source, free, beautiful UI.", "fr": "Courbes de ventilateur personnalisées pour toute combinaison ventilateur/capteur. Remplace 5 applis constructeurs par une solution universelle.", "tn": "Ya3mel courbes ventilateur personnalisées lel n'importe quel ventilateur/capteur. Y3awwedh 5 applis constructeurs b solution wa7da.", "es": "Curvas de ventilador personalizadas para cualquier combo ventilador/sensor. Reemplaza 5 apps de fabricante con una solución universal.", "de": "Benutzerdefinierte Lüfterkurven für jede Lüfter/Sensor-Kombination. Ersetzt 5 Hersteller-Apps durch eine universelle Lösung.", "ar": "منحنيات مروحة مخصصة لأي مروحة/مستشعر. يستبدل 5 تطبيقات شركات بحل واحد شامل."},
    "Install OpenRGB": {"en": "Control ALL your RGB from ONE app. Corsair iCUE, ASUS Aura, MSI Mystic, Razer Synapse, Logitech G — all replaced. No more 5 bloated RGB apps eating 500MB RAM. Supports 200+ devices. Open-source revolution.", "fr": "Contrôlez TOUT votre RGB depuis UNE seule appli. iCUE, Aura, Mystic, Synapse — tous remplacés. Plus de 5 applis RGB qui mangent 500Mo.", "tn": "Contrôler KOL el RGB ta3ek b appli WA7DA. iCUE, Aura, Mystic, Synapse — koll remplacés. Bla 5 applis RGB yeklou 500Mo RAM.", "es": "Controla TODO tu RGB desde UNA app. iCUE, Aura, Mystic, Synapse — todos reemplazados. Sin 5 apps RGB consumiendo 500MB RAM.", "de": "Steuert ALLE RGB von EINER App. iCUE, Aura, Mystic, Synapse — alle ersetzt. Keine 5 aufgeblähten RGB-Apps mehr.", "ar": "تحكم بكل RGB من تطبيق واحد. iCUE, Aura, Mystic, Synapse — الكل مستبدل. بدون 5 تطبيقات تأكل 500 ميجا."},
    "Install LibreHardwareMonitor": {"en": "Open-source fork of OpenHardwareMonitor with better sensor support. Has a web server API — build your own monitoring dashboards, send data to Grafana, or display on a second screen. The hacker's HWiNFO.", "fr": "Fork open-source d'OpenHardwareMonitor. API serveur web — construisez vos propres tableaux de bord de monitoring.", "tn": "Fork open-source OpenHardwareMonitor. 3andha API serveur web — ta3mel dashboards monitoring mta3ek.", "es": "Fork open-source de OpenHardwareMonitor con mejor soporte de sensores. API web server para construir dashboards propios.", "de": "Open-Source-Fork von OpenHardwareMonitor. Web-Server-API — eigene Monitoring-Dashboards bauen.", "ar": "نسخة مفتوحة من OpenHardwareMonitor مع دعم أفضل. واجهة API لبناء لوحات مراقبة مخصصة."},
    "Install BlueScreenView": {"en": "Analyzes all past Blue Screen crash dumps on your PC. Shows the EXACT driver that caused each crash, bug check code, and crash stack. Stop guessing why your PC crashed — this tool TELLS you. NirSoft hidden gem.", "fr": "Analyse tous les crash dumps d'écran bleu passés. Montre le pilote EXACT qui a causé chaque crash et le bug check code.", "tn": "Y7allel kol crash dumps écran bleu 9dam. Ywari el driver EXACT eli sababha w bug check code. Ywakfek mel guessing.", "es": "Analiza todos los crash dumps de pantalla azul pasados. Muestra el driver EXACTO que causó cada crash y el código de error.", "de": "Analysiert alle vergangenen Bluescreen-Crashdumps. Zeigt den EXAKTEN Treiber der jeden Crash verursachte.", "ar": "يحلل كل تقارير الشاشة الزرقاء السابقة. يعرض التعريف الدقيق الذي سبّب كل تعطل."},
    "Install ShellExView": {"en": "Shows EVERY shell extension registered on your system — right-click menus, drag-and-drop handlers, property sheets. Disable the bloated ones to fix slow right-click menus. The solution to a problem EVERYONE has but nobody knows how to fix.", "fr": "Montre CHAQUE extension shell — menus clic-droit, gestionnaires glisser-déposer. Désactivez les lourdes pour réparer les menus lents.", "tn": "Ywari KOL extension shell — menus clic-droit, drag-drop. Ytaffi eli thi9al bash ysal7 menus lents. El solution lel problème eli KOLL 3andou.", "es": "Muestra CADA extensión shell — menús clic derecho, drag-and-drop. Desactiva las pesadas para arreglar menús lentos.", "de": "Zeigt JEDE Shell-Erweiterung — Rechtsklickmenüs, Drag-and-Drop-Handler. Deaktivieren für schnellere Kontextmenüs.", "ar": "يعرض كل امتدادات Shell — قوائم النقر اليمنى، السحب والإفلات. عطّل الثقيلة لإصلاح القوائم البطيئة."},
    "Install AppReadWriteCounter": {"en": "Reveals which applications are reading/writing the MOST to your disk. Find the hidden background process destroying your SSD lifespan. Shows total bytes read/written per app since boot. NirSoft's most underrated tool.", "fr": "Révèle quelles applications lisent/écrivent le PLUS sur votre disque. Trouvez le processus caché qui détruit votre SSD.", "tn": "Ywari les applications eli ta9ra/tekteb EL AKTHAR 3al disque. Yla99a el processus caché eli y7asser el SSD ta3ek.", "es": "Revela qué aplicaciones leen/escriben MÁS en tu disco. Encuentra el proceso oculto destruyendo tu SSD.", "de": "Zeigt welche Apps am MEISTEN auf Ihre Festplatte lesen/schreiben. Finden Sie den versteckten Prozess der Ihre SSD zerstört.", "ar": "يكشف أي تطبيقات تقرأ/تكتب الأكثر على القرص. اعثر على العملية المخفية التي تدمر SSD."},
    "Install SoundVolumeView": {"en": "Shows EVERY audio device, mixer line, and per-app audio routing on your system. Set different apps to different audio outputs via command-line. The audio routing tool Windows should have built-in but never will.", "fr": "Montre CHAQUE périphérique audio, ligne mixer et routage audio par appli. Définissez différentes sorties audio par application.", "tn": "Ywari KOL périphérique audio, mixer line w routage audio par appli. 7ot applis différentes lel sorties audio différentes.", "es": "Muestra CADA dispositivo de audio, línea de mezclador y enrutamiento por app. Configura diferentes salidas de audio por app.", "de": "Zeigt JEDES Audiogerät, Mixerleitung und App-Audio-Routing. Verschiedene Apps verschiedenen Audioausgängen zuweisen.", "ar": "يعرض كل جهاز صوت وتوجيه صوت لكل تطبيق. اضبط تطبيقات مختلفة لمخرجات صوت مختلفة."},
    "Install FullEventLogView": {"en": "Aggregates ALL Windows event logs into one sortable, filterable table. Way better than the built-in Event Viewer. Export to CSV/HTML, advanced filtering, color-coded severity. Find why your PC crashed/froze/restarted.", "fr": "Agrège TOUS les journaux d'événements Windows en une table triable et filtrable. Bien meilleur que l'Observateur d'événements intégré.", "tn": "Yjam3a KOL journaux d'événements Windows fi table wa7da triable w filtrable. A7sen barcha mel Event Viewer intégré.", "es": "Agrega TODOS los registros de eventos de Windows en una tabla filtrable. Mucho mejor que el Visor de Eventos integrado.", "de": "Aggregiert ALLE Windows-Ereignisprotokolle in eine sortier-/filterbare Tabelle. Viel besser als die eingebaute Ereignisanzeige.", "ar": "يجمع كل سجلات أحداث Windows في جدول واحد قابل للفرز والتصفية. أفضل بكثير من عارض الأحداث المدمج."},
    "Install Dependencies": {"en": "Modern replacement for Dependency Walker. View DLL dependencies of any .exe, find missing DLLs, resolve side-by-side assembly errors. The tool you need when you get 'DLL not found' errors. Open-source.", "fr": "Remplacement moderne de Dependency Walker. Voir les dépendances DLL de tout .exe, trouver les DLL manquantes.", "tn": "Remplacement moderne Dependency Walker. Tchouf dépendances DLL n'importe quel .exe, yla99a DLLs manquantes.", "es": "Reemplazo moderno de Dependency Walker. Ver dependencias DLL de cualquier .exe, encontrar DLLs faltantes.", "de": "Moderner Ersatz für Dependency Walker. DLL-Abhängigkeiten jeder .exe anzeigen, fehlende DLLs finden.", "ar": "بديل حديث لـ Dependency Walker. عرض تبعيات DLL لأي ملف تنفيذي والعثور على المفقودة."},
    "Install Resource Hacker": {"en": "View and edit resources embedded inside Windows executables — icons, bitmaps, dialogs, menus, strings, version info. Change any program's icon, modify embedded resources, extract assets. Legendary niche tool since 1999.", "fr": "Voir et éditer les ressources intégrées dans les exécutables — icônes, bitmaps, dialogues, menus, chaînes.", "tn": "Tchouf w tbeddel ressources fi les exécutables — icônes, bitmaps, dialogues, menus, chaînes. Outil légendaire men 1999.", "es": "Ver y editar recursos dentro de ejecutables — íconos, bitmaps, diálogos, menús, cadenas. Herramienta legendaria desde 1999.", "de": "Ressourcen in Executables ansehen/bearbeiten — Icons, Bitmaps, Dialoge, Menüs, Strings. Legendäres Nischentool seit 1999.", "ar": "عرض وتحرير الموارد داخل الملفات التنفيذية — أيقونات، صور، حوارات، قوائم. أداة أسطورية منذ 1999."},
    "Install x64dbg": {"en": "Open-source x64/x32 debugger for Windows. The modern replacement for OllyDbg. Breakpoints, memory map, disassembler, decompiler plugins. Used by security researchers and reverse engineers worldwide. Not for the faint of heart.", "fr": "Débogueur x64/x32 open-source. Le remplacement moderne d'OllyDbg. Points d'arrêt, carte mémoire, désassembleur.", "tn": "Débogueur x64/x32 open-source. Remplacement moderne OllyDbg. Breakpoints, memory map, désassembleur. Mch lel faibles.", "es": "Depurador x64/x32 open-source. El reemplazo moderno de OllyDbg. Breakpoints, mapa de memoria, desensamblador.", "de": "Open-Source x64/x32 Debugger. Der moderne OllyDbg-Ersatz. Breakpoints, Speicherkarte, Disassembler.", "ar": "مصحح أخطاء x64/x32 مفتوح المصدر. البديل الحديث لـ OllyDbg. نقاط توقف، خريطة ذاكرة، مفكك."},
    "Install MacType": {"en": "Replaces Windows' terrible ClearType font rendering with macOS-style subpixel rendering. Text looks DRAMATICALLY smoother and more readable across the entire OS. Once you try it you can never go back. The ultimate hidden QoL upgrade.", "fr": "Remplace le rendu ClearType de Windows par un rendu macOS. Le texte est DRAMATIQUEMENT plus lisse et lisible sur tout l'OS.", "tn": "Y3awwedh ClearType Windows b rendu macOS. El texte yji DRAMATIQUEMENT a7sen w plus lisible fi kol el OS.", "es": "Reemplaza el renderizado ClearType de Windows con estilo macOS. El texto se ve DRAMÁTICAMENTE más suave y legible.", "de": "Ersetzt Windows ClearType durch macOS-Schriftrendering. Text sieht DRAMATISCH glatter und lesbarer aus.", "ar": "يستبدل عرض خطوط Windows بأسلوب macOS. النص يبدو أفضل بشكل كبير في كل النظام."},
    "Install TranslucentTB": {"en": "Makes your Windows taskbar transparent, acrylic, or blurred. Different states for maximized windows, start menu open, searching. Tiny 2MB app that does one thing PERFECTLY. The single prettiest Windows mod.", "fr": "Rend votre barre des tâches transparente, acrylique ou floue. 2Mo qui fait UNE chose PARFAITEMENT.", "tn": "Ya3mel taskbar Windows transparente, acrylique, wella floue. 2Mo ya3mel 7aja WA7DA PARFAITEMENT. A7sen mod Windows.", "es": "Hace tu barra de tareas transparente, acrílica o borrosa. 2MB que hace UNA cosa PERFECTAMENTE.", "de": "Macht Ihre Taskbar transparent, acryl oder verschwommen. 2MB App die EINE Sache PERFEKT macht.", "ar": "يجعل شريط المهام شفافاً أو أكريليك أو ضبابياً. 2 ميجا يفعل شيئاً واحداً بشكل مثالي."},
    "Install ModernFlyouts": {"en": "Replaces the ancient Windows volume, brightness, airplane mode, and Caps Lock popups with beautiful modern Fluent Design flyouts. Customizable position, animations, timeouts. Fixes a 20-year-old Windows eyesore.", "fr": "Remplace les anciens popups volume/luminosité/Caps Lock par de beaux flyouts modernes Fluent Design. Corrige une horreur Windows vieille de 20 ans.", "tn": "Y3awwedh les popups volume/luminosité/Caps Lock 9dima b flyouts modernes Fluent Design. Ysal7 7aja horrible men 20 sna.", "es": "Reemplaza los antiguos popups de volumen/brillo/Caps Lock con flyouts modernos de Fluent Design.", "de": "Ersetzt die alten Windows Lautstärke/Helligkeit/Caps-Lock-Popups durch moderne Fluent Design Flyouts.", "ar": "يستبدل نوافذ الصوت/السطوع/Caps Lock القديمة بتصميم Fluent حديث وجميل."},
    "Install DevToys": {"en": "Swiss army knife for developers. Base64 encode/decode, JSON formatter/validator, hash generator, UUID generator, regex tester, color picker, Lorem ipsum, JWT decoder, URL encoder — ALL offline. Never use random websites again.", "fr": "Couteau suisse pour développeurs. Base64, JSON, hash, UUID, regex, couleurs — TOUT hors-ligne. Plus jamais de sites web random.", "tn": "Couteau suisse lel développeurs. Base64, JSON, hash, UUID, regex, couleurs — KOL offline. Ma t3awedch testa3mel sites random.", "es": "Navaja suiza para desarrolladores. Base64, JSON, hash, UUID, regex, colores — TODO offline. Nunca más uses sitios web random.", "de": "Schweizer Taschenmesser für Entwickler. Base64, JSON, Hash, UUID, Regex, Farben — ALLES offline.", "ar": "سكين سويسرية للمطورين. Base64, JSON, تجزئة, UUID, regex, ألوان — الكل بدون إنترنت."},
    "Install GlazeWM": {"en": "Tiling window manager for Windows — inspired by i3wm on Linux. Keyboard-driven window management, virtual desktops, custom keybindings. Your windows automatically tile without overlap. For the 1% of power users who know what tiling WMs are.", "fr": "Gestionnaire de fenêtres en mosaïque pour Windows — inspiré par i3wm. Gestion au clavier, bureaux virtuels, raccourcis personnalisés.", "tn": "Gestionnaire fenêtres mosaïque lel Windows — inspiré par i3wm fi Linux. Gestion clavier, bureaux virtuels.", "es": "Gestor de ventanas en mosaico para Windows — inspirado en i3wm. Gestión por teclado, escritorios virtuales.", "de": "Tiling Window Manager für Windows — inspiriert von i3wm. Tastaturgesteuerte Fensterverwaltung, virtuelle Desktops.", "ar": "مدير نوافذ فسيفسائي لـ Windows — مستوحى من i3wm. إدارة بلوحة المفاتيح وأسطح مكتب افتراضية."},
    "Install NanaZip": {"en": "Modern fork of 7-Zip with native Windows 11 context menu integration, Zstandard (zstd) compression support, and ARM64 builds. Same engine as 7-Zip but with all the modern OS integration 7-Zip refuses to add.", "fr": "Fork moderne de 7-Zip avec intégration native du menu contextuel Windows 11 et support Zstandard (zstd).", "tn": "Fork moderne 7-Zip b intégration native menu contextuel Windows 11 w support Zstandard (zstd).", "es": "Fork moderno de 7-Zip con integración nativa de menú contextual Windows 11 y soporte Zstandard.", "de": "Moderner 7-Zip-Fork mit nativer Windows-11-Kontextmenü-Integration und Zstandard-Unterstützung.", "ar": "نسخة حديثة من 7-Zip مع تكامل قائمة Windows 11 ودعم Zstandard وبنيات ARM64."},
    "Install Bulk Rename Utility": {"en": "The most powerful mass file renamer ever made. Regex patterns, sequential numbering, case conversion, date stamps, MP3 tag extraction, folder rename. Rename 10,000 files with one click. Free for personal use.", "fr": "Le renommeur de fichiers en masse le plus puissant. Regex, numérotation, casse, dates. Renommez 10 000 fichiers en un clic.", "tn": "A9wa outil renommage fichiers en masse. Regex, numérotation, casse, dates. Ybeddel 10 000 fichiers b click wa7ed.", "es": "El renombrador masivo de archivos más potente. Regex, numeración, mayúsculas, fechas. Renombra 10,000 archivos con un clic.", "de": "Der mächtigste Massendatei-Umbenenner. Regex, Nummerierung, Groß-/Kleinschreibung. 10.000 Dateien mit einem Klick.", "ar": "أقوى أداة إعادة تسمية ملفات جماعية. Regex، ترقيم، حالة أحرف. إعادة تسمية 10,000 ملف بنقرة."},
    "Install AltSnap": {"en": "Hold Alt and drag ANY window to move it. Alt+right-drag to resize any edge. Linux-style window management that Windows desperately needs. 200KB app that changes how you use your PC forever.", "fr": "Maintenez Alt et glissez pour déplacer/redimensionner TOUTE fenêtre. Gestion de fenêtres style Linux en 200Ko.", "tn": "Appuyer Alt w drag TOUTE fenêtre bash t7arkha. Alt+clic-droit bash tbaddel el taille. 200Ko ybaddel 7ayetek.", "es": "Mantén Alt y arrastra CUALQUIER ventana para moverla. Alt+clic derecho para redimensionar. 200KB que cambia tu vida.", "de": "Alt gedrückt halten und JEDES Fenster verschieben. Alt+Rechtsklick zum Ändern der Größe. 200KB Linux-Stil.", "ar": "اضغط Alt واسحب أي نافذة لتحريكها. Alt+يمين لتغيير الحجم. 200 كيلوبايت تغير حياتك."},
    "Install SoundSwitch": {"en": "Switch audio output/input device with a keyboard shortcut. One hotkey to toggle between headphones and speakers. Cycle through devices with scroll. Windows should have this built-in but never will.", "fr": "Changez de périphérique audio avec un raccourci clavier. Un raccourci pour basculer casque ↔ enceintes.", "tn": "Baddel périphérique audio b raccourci clavier. Raccourci wa7ed bash tbaddel casque ↔ haut-parleurs.", "es": "Cambia dispositivo de audio con un atajo de teclado. Un atajo para alternar auriculares ↔ altavoces.", "de": "Audioausgabegerät per Tastenkürzel wechseln. Ein Shortcut für Kopfhörer ↔ Lautsprecher.", "ar": "بدّل جهاز الصوت بضغطة زر. اختصار واحد للتبديل بين السماعات والمكبرات."},
    "Install TrafficMonitor": {"en": "Displays network upload/download speed, CPU usage, RAM usage, and temperature directly in your taskbar. Tiny, beautiful, always visible. The real-time system monitor you didn't know you needed.", "fr": "Affiche vitesse réseau, CPU, RAM et température directement dans la barre des tâches. Petit, beau, toujours visible.", "tn": "Ywari vitesse réseau, CPU, RAM w température fil taskbar directement. S8ir, jmil, toujours visible.", "es": "Muestra velocidad de red, CPU, RAM y temperatura directamente en la barra de tareas. Pequeño, bonito, siempre visible.", "de": "Zeigt Netzwerkgeschwindigkeit, CPU, RAM und Temperatur direkt in der Taskbar. Klein, schön, immer sichtbar.", "ar": "يعرض سرعة الشبكة والمعالج والذاكرة والحرارة مباشرة في شريط المهام. صغير وجميل ودائماً مرئي."},
    "Install Twinkle Tray": {"en": "Control brightness of external monitors from your taskbar using DDC/CI protocol. Works with DisplayPort, HDMI, USB-C. Keyboard shortcuts for brightness. The solution for people with no brightness buttons on their monitor.", "fr": "Contrôlez la luminosité des moniteurs externes depuis la barre des tâches via DDC/CI. Fonctionne en HDMI/DP.", "tn": "Contrôler luminosité écrans externes mel taskbar b DDC/CI. Yemchi b HDMI/DP. Raccourcis clavier lel luminosité.", "es": "Controla brillo de monitores externos desde la barra de tareas vía DDC/CI. Funciona con HDMI/DP.", "de": "Externe Monitorhelligkeit per Taskbar via DDC/CI steuern. HDMI/DP-kompatibel. Tastaturkürzel.", "ar": "تحكم بسطوع الشاشات الخارجية من شريط المهام عبر DDC/CI. يعمل مع HDMI/DP."},
    "Install SuperF4": {"en": "Ctrl+Alt+F4 to instantly force-kill ANY foreground window. No more waiting for 'Not Responding' dialogs. Xkill mode (Ctrl+Alt+F4 then click any window to kill it). 50KB nuclear option for frozen apps.", "fr": "Ctrl+Alt+F4 pour tuer instantanément TOUTE fenêtre gelée. Plus d'attente 'Ne répond pas'. 50Ko d'option nucléaire.", "tn": "Ctrl+Alt+F4 bash to9tel TOUTE fenêtre gelée fi th7a. Bla attente 'Ne répond pas'. 50Ko option nucléaire.", "es": "Ctrl+Alt+F4 para matar instantáneamente CUALQUIER ventana congelada. Sin esperar 'No responde'. 50KB opción nuclear.", "de": "Ctrl+Alt+F4 um JEDES eingefrorene Fenster sofort zu beenden. Kein Warten auf 'Keine Rückmeldung'. 50KB Nuklearoption.", "ar": "Ctrl+Alt+F4 لقتل أي نافذة متجمدة فوراً. بدون انتظار 'لا يستجيب'. 50 كيلوبايت خيار نووي."},
    "Install System Informer": {"en": "The successor to Process Hacker. Process tree, DLL list, handles, network connections, GPU usage per-process, stack traces. Makes Windows Task Manager look like a children's toy. For serious system administrators.", "fr": "Successeur de Process Hacker. Arbre de processus, DLL, handles, réseau, GPU par processus. Rend le Gestionnaire de tâches ridicule.", "tn": "Successeur Process Hacker. Arbre processus, DLL, handles, réseau, GPU par processus. Ya3mel Task Manager yban jouet.", "es": "Sucesor de Process Hacker. Árbol de procesos, DLL, handles, red, GPU por proceso. Hace que Task Manager parezca un juguete.", "de": "Process Hacker Nachfolger. Prozessbaum, DLLs, Handles, Netzwerk, GPU pro Prozess. Macht den Task-Manager lächerlich.", "ar": "خليفة Process Hacker. شجرة العمليات، DLL، المقابض، الشبكة، GPU لكل عملية. يجعل مدير المهام لعبة أطفال."},
    "Install RegCool": {"en": "Advanced Windows registry editor with multi-tab interface, UNDO support (yes, undo registry changes!), compare registries, search & replace values, bookmarks, cut/copy/paste keys. Makes regedit look like Notepad.", "fr": "Éditeur de registre avancé avec onglets, annulation, comparaison, rechercher & remplacer. Rend regedit obsolète.", "tn": "Éditeur registre avancé b onglets, annulation (!), comparaison, rechercher & remplacer. Ya3mel regedit obsolète.", "es": "Editor de registro avanzado con pestañas, deshacer, comparar, buscar y reemplazar. Hace que regedit sea obsoleto.", "de": "Erweiterter Registry-Editor mit Tabs, Rückgängig, Vergleichen, Suchen & Ersetzen. Macht regedit obsolet.", "ar": "محرر سجل متقدم مع علامات تبويب، تراجع، مقارنة، بحث واستبدال. يجعل regedit قديماً."},
    "Install Czkawka": {"en": "Ultra-fast duplicate file finder written in Rust. Finds exact duplicates, similar images (perceptual hash), empty files/folders, temp files, broken symlinks. 10x faster than alternatives. Open-source Polish engineering.", "fr": "Chercheur de doublons ultra-rapide en Rust. Doublons exacts, images similaires, fichiers vides. 10x plus rapide.", "tn": "Chercheur doublons ultra-rapide fi Rust. Doublons exacts, images similaires, fichiers vides. 10x a7sen mel ba9i.", "es": "Buscador de duplicados ultra-rápido en Rust. Duplicados exactos, imágenes similares, archivos vacíos. 10x más rápido.", "de": "Ultraschneller Duplikatfinder in Rust. Exakte Duplikate, ähnliche Bilder, leere Dateien. 10x schneller.", "ar": "باحث ملفات مكررة فائق السرعة بلغة Rust. مكررات دقيقة، صور متشابهة، ملفات فارغة. أسرع 10 مرات."},
    "Install dnSpy": {"en": "Decompile, debug, and EDIT .NET assemblies without source code. See the C# code inside any .NET exe/dll, modify it live, recompile. Debugger that attaches to running .NET processes. The ultimate .NET reverse engineering tool.", "fr": "Décompiler, déboguer et ÉDITER des assemblies .NET sans code source. Voir le C# dans tout exe/dll .NET et le modifier.", "tn": "Décompiler, déboguer w ÉDITER assemblies .NET bla code source. Tchouf el C# fi tout exe/dll .NET w tbaddlou live.", "es": "Descompilar, depurar y EDITAR ensamblados .NET sin código fuente. Ver el C# dentro de cualquier exe/dll .NET.", "de": ".NET-Assemblies dekompilieren, debuggen und BEARBEITEN ohne Quellcode. C# in jeder .NET exe/dll sehen und live ändern.", "ar": "فك تجميع وتصحيح وتحرير ملفات .NET بدون كود مصدر. عرض C# داخل أي exe/dll وتعديله مباشرة."},
    "Install PE-bear": {"en": "Portable Executable file analyzer with beautiful UI. Inspect PE headers, sections, imports/exports, resources, signatures of any .exe or .dll. Used by malware analysts and reverse engineers. If you know what a PE file is, you need this.", "fr": "Analyseur de fichiers PE avec belle interface. Inspectez en-têtes PE, sections, imports/exports de tout .exe/.dll.", "tn": "Analyseur fichiers PE b interface jmila. Inspectez en-têtes PE, sections, imports/exports n'importe quel .exe/.dll.", "es": "Analizador de archivos PE con interfaz bonita. Inspeccionar cabeceras PE, secciones, importaciones de cualquier .exe/.dll.", "de": "PE-Datei-Analyzer mit schöner UI. PE-Header, Sektionen, Imports/Exports jeder .exe/.dll inspizieren.", "ar": "محلل ملفات PE بواجهة جميلة. فحص رؤوس PE والأقسام والاستيرادات لأي .exe/.dll."},
    "Install Espanso": {"en": "Cross-platform text expander written in Rust. Type ':email' and it expands to your email. ':date' → today's date. Custom regex triggers, shell command output, clipboard content. Automate repetitive typing forever.", "fr": "Expandeur de texte écrit en Rust. Tapez ':email' → votre email. ':date' → date du jour. Regex, commandes shell.", "tn": "Expandeur texte fi Rust. Tap ':email' → email ta3ek. ':date' → date lyoum. Regex, commandes shell. Automatiser typing.", "es": "Expansor de texto en Rust. Escribe ':email' → tu email. ':date' → fecha de hoy. Regex, comandos shell.", "de": "Text-Expander in Rust. ':email' → Ihre E-Mail. ':date' → heutiges Datum. Regex, Shell-Befehle.", "ar": "موسع نصوص بـ Rust. اكتب ':email' → بريدك. ':date' → تاريخ اليوم. Regex، أوامر shell."},
    "Install Monitorian": {"en": "Control brightness of multiple external monitors independently from your taskbar. Uses DDC/CI protocol over HDMI/DisplayPort. Link monitors together or control separately. The brightness control Windows forgot to build.", "fr": "Contrôlez la luminosité de plusieurs moniteurs externes indépendamment. DDC/CI via HDMI/DP. Liez ou séparez les moniteurs.", "tn": "Contrôler luminosité plusieurs écrans externes indépendamment. DDC/CI via HDMI/DP. Lier wella séparer écrans.", "es": "Controla brillo de múltiples monitores externos independientemente. DDC/CI vía HDMI/DP.", "de": "Helligkeit mehrerer externer Monitore unabhängig steuern. DDC/CI über HDMI/DP.", "ar": "تحكم بسطوع عدة شاشات خارجية مستقلاً. DDC/CI عبر HDMI/DP."},
    "Install LocalSend": {"en": "AirDrop alternative that works between Windows, Android, iOS, macOS, and Linux. Send files over local network — no internet needed, no account needed. Encrypted, fast, open-source. The file sharing tool every OS should have.", "fr": "Alternative AirDrop entre Windows, Android, iOS, macOS. Envoyez des fichiers en local — pas d'internet, pas de compte.", "tn": "Alternative AirDrop entre Windows, Android, iOS, macOS. Ab3ath fichiers en local — bla internet, bla compte.", "es": "Alternativa a AirDrop entre Windows, Android, iOS, macOS. Envía archivos en red local — sin internet, sin cuenta.", "de": "AirDrop-Alternative für Windows, Android, iOS, macOS. Dateien lokal senden — kein Internet, kein Konto.", "ar": "بديل AirDrop بين Windows وAndroid وiOS وmacOS. إرسال ملفات محلياً — بدون إنترنت أو حساب."},
    "Install NTLite": {"en": "Customize Windows installation ISO: remove built-in apps, disable telemetry, integrate drivers/updates, configure registry — all BEFORE installing Windows. Create your perfect debloated Windows image. The ultimate pre-install weapon.", "fr": "Personnalisez l'ISO Windows : supprimez les applis intégrées, désactivez la télémétrie, intégrez pilotes — AVANT l'installation.", "tn": "Personnaliser ISO Windows : na77i applis intégrées, désactiver télémétrie, intégrer pilotes — AVANT l'installation.", "es": "Personaliza ISO de Windows: elimina apps integradas, desactiva telemetría, integra drivers — ANTES de instalar.", "de": "Windows-ISO anpassen: integrierte Apps entfernen, Telemetrie deaktivieren, Treiber integrieren — VOR der Installation.", "ar": "تخصيص ISO Windows: حذف التطبيقات المدمجة وتعطيل القياس عن بعد ودمج التعريفات — قبل التثبيت."},
    "Install WinSetView": {"en": "Permanently set default folder view in Windows Explorer. Stop Explorer from randomly switching between Details, Icons, Tiles. Set ONCE, applies EVERYWHERE. Fixes the most annoying Explorer bug that has existed for 20 years.", "fr": "Définissez la vue par défaut PERMANENTE dans l'Explorateur. Empêchez l'Explorateur de changer aléatoirement la vue.", "tn": "Définir vue par défaut PERMANENTE fil Explorateur. Ywakkef l'Explorateur mel changement aléatoire ta3 la vue.", "es": "Establece vista predeterminada PERMANENTE en el Explorador. Deja de que el Explorador cambie la vista aleatoriamente.", "de": "Standard-Ordneransicht im Explorer DAUERHAFT festlegen. Explorer hört auf, zufällig die Ansicht zu wechseln.", "ar": "ضبط عرض المجلد الافتراضي بشكل دائم في المستكشف. أوقف تغيير العرض العشوائي للأبد."},
    "Install ScreenToGif": {"en": "Record screen, webcam, or sketchboard and save as GIF, APNG, or video. Built-in editor lets you trim, add text, draw, adjust speed frame-by-frame. Tiny portable app. The fastest way to create GIFs on Windows.", "fr": "Enregistrez l'écran et sauvegardez en GIF, APNG ou vidéo. Éditeur intégré image par image. Le plus rapide pour créer des GIFs.", "tn": "Enregistrer écran w sauvegarder fi GIF, APNG, wella vidéo. Éditeur intégré image par image. A7sen haja lel GIFs.", "es": "Graba pantalla y guarda como GIF, APNG o vídeo. Editor integrado fotograma a fotograma. Lo más rápido para crear GIFs.", "de": "Bildschirm aufnehmen und als GIF, APNG oder Video speichern. Integrierter Editor mit Einzelbild-Bearbeitung.", "ar": "سجل الشاشة واحفظ كـ GIF أو APNG أو فيديو. محرر مدمج إطار بإطار. أسرع طريقة لإنشاء GIF."},
    "Install WinMerge": {"en": "Visual file and folder comparison tool. See differences side by side with color highlighting. Merge changes between versions. Compare entire folder trees. Essential for anyone who works with multiple file versions.", "fr": "Comparaison visuelle de fichiers et dossiers. Voyez les différences côte à côte avec coloration. Fusionnez les changements.", "tn": "Comparaison visuelle fichiers w dossiers. Tchouf les différences côte à côte b coloration. Fusionnez les changements.", "es": "Comparación visual de archivos y carpetas. Ver diferencias lado a lado con colores. Fusionar cambios entre versiones.", "de": "Visueller Datei-/Ordnervergleich. Unterschiede nebeneinander mit Farbhervorhebung sehen. Änderungen zusammenführen.", "ar": "مقارنة ملفات ومجلدات مرئية. عرض الفروقات جنباً إلى جنب مع تلوين. دمج التغييرات بين الإصدارات."},
    "Install carnac": {"en": "Displays keyboard shortcuts as a translucent overlay as you press them. Perfect for presentations, streaming, tutorials. Viewers see exactly which keys you're pressing. Customizable position, font, fade time.", "fr": "Affiche les raccourcis clavier en overlay translucide quand vous les tapez. Parfait pour présentations et streaming.", "tn": "Ywari raccourcis clavier fi overlay translucide ki tap3as. Parfait lel présentations w streaming.", "es": "Muestra atajos de teclado como superposición translúcida al presionarlos. Perfecto para presentaciones y streaming.", "de": "Zeigt Tastaturkürzel als durchscheinendes Overlay beim Drücken. Perfekt für Präsentationen und Streaming.", "ar": "يعرض اختصارات لوحة المفاتيح كطبقة شفافة عند الضغط. مثالي للعروض والبث المباشر."},
    "Install Flameshot": {"en": "Take screenshots and instantly annotate them — arrows, circles, text, blur sensitive areas, highlight, numbering, pixelate. Upload to Imgur with one click. The screenshot tool that makes Snipping Tool embarrassing.", "fr": "Captures d'écran avec annotation instantanée — flèches, cercles, texte, flou, surlignage. Upload Imgur en un clic.", "tn": "Captures d'écran b annotation instantanée — flèches, cercles, texte, flou, surlignage. Upload Imgur b click wa7ed.", "es": "Capturas de pantalla con anotación instantánea — flechas, círculos, texto, desenfoque, resaltado. Subir a Imgur con un clic.", "de": "Screenshots mit sofortiger Annotation — Pfeile, Kreise, Text, Unschärfe, Hervorhebung. Imgur-Upload mit einem Klick.", "ar": "لقطات شاشة مع تعليقات فورية — أسهم، دوائر، نص، تمويه، تمييز. رفع إلى Imgur بنقرة."},
    "Install Qalculate!": {"en": "The most powerful calculator application ever created. 1500+ unit conversions, symbolic algebra, calculus, statistics, currency conversions (live rates), complex numbers, matrices, plots, programming. Makes Windows Calculator a joke.", "fr": "La calculatrice la plus puissante jamais créée. 1500+ conversions d'unités, algèbre symbolique, calcul, statistiques, devises.", "tn": "A9wa calculatrice fi l'histoire. 1500+ conversions unités, algèbre symbolique, calcul, statistiques, devises live.", "es": "La calculadora más potente jamás creada. 1500+ conversiones de unidades, álgebra simbólica, cálculo, estadísticas.", "de": "Der mächtigste Taschenrechner aller Zeiten. 1500+ Einheitenumrechnungen, symbolische Algebra, Analysis, Statistik.", "ar": "أقوى آلة حاسبة صُنعت. 1500+ تحويل وحدات، جبر رمزي، تفاضل، إحصاء، عملات مباشرة."},
    "Install Quick CPU": {'en': 'Control CPU core parking, frequency scaling, turbo boost, C-states, power plan switching — all from one tiny GUI. The only tool that exposes EVERY hidden Windows power parameter. Overclockers and latency chasers swear by it.', 'fr': "Contrôlez le core parking, la fréquence, le turbo boost, les C-states — tous les paramètres d'énergie cachés de Windows dans un seul outil.", 'tn': "Control el core parking, fréquence, turbo boost, C-states — kol les paramètres d'énergie cachés ta3 Windows fi outil wa7da.", 'es': 'Controla core parking, escalado de frecuencia, turbo boost, C-states — todos los parámetros ocultos de energía de Windows en una herramienta.', 'de': 'CPU Core Parking, Frequenzskalierung, Turbo Boost, C-States — alle versteckten Windows-Energieparameter in einem Tool.', 'ar': 'تحكم في إيقاف النوى وتدرج التردد وتيربو بوست وحالات C — كل معلمات الطاقة المخفية في أداة واحدة.'},
    "Install Special K": {'en': "The Swiss Army knife of PC gaming injection. Fixes frame pacing, adds HDR to non-HDR games, reduces input latency, fixes stuttering, adds DLSS/FSR where unsupported. Frame generation, flip model override, texture modding. Reddit's #1 secret weapon for smooth gaming.", 'fr': "Couteau suisse du jeu PC. Corrige le frame pacing, ajoute le HDR, réduit la latence d'entrée, corrige le stuttering, ajoute DLSS/FSR.", 'tn': 'Couteau suisse lel gaming. Ysa77e7 el frame pacing, yzid HDR, yna99es latence, ysa77e7 stuttering, yzid DLSS/FSR.', 'es': 'Navaja suiza del gaming. Corrige frame pacing, añade HDR, reduce latencia de entrada, corrige stuttering, añade DLSS/FSR.', 'de': 'Schweizer Taschenmesser für PC-Gaming. Behebt Frame Pacing, fügt HDR hinzu, reduziert Input-Latenz, behebt Stottern, fügt DLSS/FSR hinzu.', 'ar': 'السكين السويسري للألعاب. يصلح تزامن الإطارات ويضيف HDR ويقلل زمن الاستجابة ويصلح التقطع ويضيف DLSS/FSR.'},
    "Install Intel PresentMon": {'en': "Intel's open-source frametime & latency analysis tool. Measures GPU busy time, CPU frame time, display latency, input-to-photon delay. Used by hardware reviewers. Shows exactly WHERE your frametime spikes come from. The scientific approach to 'why does my game stutter'.", 'fr': "Outil open-source Intel d'analyse frametime et latence. Mesure le temps GPU, CPU, latence d'affichage, délai entrée-photon.", 'tn': 'Outil Intel open-source ta7lil frametime w latence. Y9is wakt GPU, CPU, latence affichage, délai entrée-photon.', 'es': 'Herramienta Intel de análisis frametime y latencia. Mide tiempo GPU/CPU, latencia de pantalla, retardo entrada-fotón.', 'de': 'Intels Open-Source Frametime- & Latenz-Analyse. Misst GPU-Zeit, CPU-Zeit, Display-Latenz, Input-to-Photon-Delay.', 'ar': 'أداة إنتل مفتوحة المصدر لتحليل وقت الإطار والكمون. تقيس وقت GPU وCPU وكمون العرض وتأخير الإدخال.'},
    "Install NVIDIA FrameView": {'en': "NVIDIA's frametime benchmarking & GPU power measurement tool. Records frame times, percentiles (1% low, 0.1% low), GPU power draw, GPU temperature during gameplay. The gold standard for benchmarking methodology. Free but almost nobody knows it exists.", 'fr': 'Outil NVIDIA de benchmarking frametime et mesure de puissance GPU. Enregistre frametimes, percentiles, consommation GPU.', 'tn': 'Outil NVIDIA benchmarking frametime w mesure puissance GPU. Y9ayed frametimes, percentiles, consommation GPU.', 'es': 'Herramienta NVIDIA de benchmarking frametime y medición de potencia GPU. Registra frametimes, percentiles, consumo GPU.', 'de': 'NVIDIAs Frametime-Benchmarking & GPU-Leistungsmessung. Zeichnet Frametimes, Perzentile, GPU-Stromverbrauch auf.', 'ar': 'أداة NVIDIA لقياس وقت الإطار واستهلاك طاقة GPU. تسجل أوقات الإطارات والنسب المئوية واستهلاك GPU.'},
    "Install AMD OCAT": {'en': 'Open Capture and Analytics Tool by AMD. Captures frametime data overlaid on gameplay, exports CSV for analysis. Works with any GPU (not AMD-only). The forgotten AMD tool that competes with FrameView but nobody talks about.', 'fr': 'Outil AMD de capture et analyse. Capture les frametimes en overlay pendant le jeu, exporte CSV. Fonctionne avec tout GPU.', 'tn': 'Outil AMD capture w analyse. Y9ayed frametimes fi overlay pendant el jeu, exporte CSV. Yakhdem m3a kol GPU.', 'es': 'Herramienta AMD de captura y análisis. Captura frametimes en overlay durante el juego, exporta CSV. Funciona con cualquier GPU.', 'de': 'AMDs Capture & Analytics Tool. Erfasst Frametime-Daten als Overlay im Spiel, exportiert CSV. Funktioniert mit jeder GPU.', 'ar': 'أداة AMD للالتقاط والتحليل. تلتقط أوقات الإطارات كطبقة فوق اللعب وتصدر CSV. تعمل مع أي GPU.'},
    "Install BenchMate": {'en': 'Anti-cheat benchmarking validation tool used in overclocking competitions (HWBOT). Ensures benchmark scores are legitimate by monitoring system state, detecting cheats, verifying hardware. If competitive benchmarking had a referee, this is it.', 'fr': "Outil de validation anti-triche pour benchmarks d'overclocking (HWBOT). Vérifie la légitimité des scores en surveillant le système.", 'tn': 'Outil validation anti-triche lel benchmarks overclocking (HWBOT). Yverifie el scores b surveillance ta3 el système.', 'es': 'Herramienta anti-trampas para benchmarks de overclocking (HWBOT). Verifica la legitimidad de puntuaciones monitoreando el sistema.', 'de': 'Anti-Cheat Benchmark-Validierung für Overclocking-Wettbewerbe (HWBOT). Überwacht Systemzustand und verifiziert Hardware.', 'ar': 'أداة تحقق مضادة للغش لمسابقات كسر السرعة (HWBOT). تراقب حالة النظام وتتحقق من العتاد.'},
    "Install Intel XTU": {'en': 'Intel Extreme Tuning Utility — official Intel tool for overclocking, undervolting, and stress-testing Intel CPUs. Adjust voltage offsets, power limits, turbo ratios. The ONLY safe way to undervolt modern Intel laptops. Reduces thermals and boosts performance.', 'fr': "Outil officiel Intel pour l'overclocking, l'undervolting et le stress test. Ajustez voltage, power limits, turbo ratios.", 'tn': 'Outil officiel Intel lel overclocking, undervolting w stress test. Ajuster voltage, power limits, turbo ratios.', 'es': 'Herramienta oficial Intel para overclocking, undervolting y test de estrés. Ajusta voltaje, límites de potencia, ratios turbo.', 'de': 'Offizielles Intel-Tool für Übertaktung, Undervolting und Stresstest. Spannung, Leistungslimits, Turbo-Ratios anpassen.', 'ar': 'أداة إنتل الرسمية لكسر السرعة وخفض الجهد واختبار الإجهاد. ضبط الجهد وحدود الطاقة ونسب التيربو.'},
    "Install UXTU": {'en': "Universal x86 Tuning Utility — adjust AMD AND Intel CPU power limits, TDP, boost behavior from a simple GUI. Originally made for Steam Deck/ROG Ally but works on any x86 laptop/desktop. The hidden gem for mobile CPU tuning that Reddit's r/HandheldGamePC worships.", 'fr': 'Ajustez les limites de puissance CPU AMD/Intel, TDP, boost depuis une GUI simple. Conçu pour Steam Deck/ROG Ally, fonctionne partout.', 'tn': 'Ajuster limites puissance CPU AMD/Intel, TDP, boost men GUI simple. Fait lel Steam Deck/ROG Ally, yakhdem partout.', 'es': 'Ajusta límites de potencia CPU AMD/Intel, TDP, boost desde una GUI simple. Hecho para Steam Deck/ROG Ally pero funciona en todo.', 'de': 'AMD/Intel CPU-Leistungslimits, TDP, Boost-Verhalten über einfache GUI anpassen. Für Steam Deck/ROG Ally gemacht, funktioniert überall.', 'ar': 'ضبط حدود طاقة معالجات AMD/Intel وTDP والتعزيز من واجهة بسيطة. صُنع لـ Steam Deck لكن يعمل في كل مكان.'},
    "Install TweakPower": {'en': "German-made all-in-one Windows optimization suite. Power plan editor, startup manager, service configurator, junk cleaner, context menu editor, drive analyzer — all without bloatware. The niche European alternative to CCleaner that actually works and isn't adware.", 'fr': "Suite d'optimisation Windows tout-en-un allemande. Éditeur de plans d'alimentation, gestionnaire de démarrage, nettoyeur. Alternative à CCleaner sans pub.", 'tn': "Suite optimisation Windows tout-en-un allemande. Éditeur plans d'alimentation, gestionnaire démarrage, nettoyeur. Alternative CCleaner bla pub.", 'es': 'Suite de optimización Windows todo en uno alemana. Editor de planes de energía, gestor de inicio, limpiador. Alternativa a CCleaner sin anuncios.', 'de': 'Deutsche All-in-One Windows-Optimierungssuite. Energieplan-Editor, Autostart-Manager, Dienste-Konfigurator, Bereinigung. CCleaner-Alternative ohne Werbung.', 'ar': 'حزمة تحسين ويندوز ألمانية شاملة. محرر خطط الطاقة ومدير بدء التشغيل ومنظف. بديل CCleaner بدون إعلانات.'},
    "Install NetLimiter": {'en': 'Per-process network bandwidth limiter and monitor. Set upload/download speed limits for ANY application. Stop Windows Update from eating your bandwidth mid-game. Reduce network latency by throttling background apps. The network equivalent of Process Lasso.', 'fr': 'Limiteur de bande passante par processus. Définissez des limites de vitesse pour chaque application. Réduisez la latence réseau.', 'tn': 'Limiteur bande passante par processus. 7ot limites vitesse l kol application. Na99es latence réseau.', 'es': 'Limitador de ancho de banda por proceso. Establece límites de velocidad para cada aplicación. Reduce latencia de red.', 'de': 'Bandbreitenbegrenzer pro Prozess. Geschwindigkeitslimits für jede Anwendung setzen. Netzwerklatenz reduzieren.', 'ar': 'محدد عرض نطاق لكل عملية. حدد سرعة الرفع/التنزيل لأي تطبيق. قلل زمن استجابة الشبكة.'},
    "Install ASIO4ALL": {'en': 'Universal ASIO driver that works with ANY sound card. Bypasses Windows audio stack entirely for ultra-low latency audio (2-10ms). Essential for musicians, audio producers, and anyone who needs real-time audio. The free alternative to expensive dedicated audio interfaces.', 'fr': 'Pilote ASIO universel pour toute carte son. Contourne la pile audio Windows pour une latence ultra-faible (2-10ms). Essentiel pour musiciens.', 'tn': 'Pilote ASIO universel l kol carte son. Ycontourner pile audio Windows lel latence ultra-faible (2-10ms). Essentiel lel musiciens.', 'es': 'Controlador ASIO universal para cualquier tarjeta de sonido. Evita la pila de audio de Windows para latencia ultra baja (2-10ms).', 'de': 'Universeller ASIO-Treiber für jede Soundkarte. Umgeht den Windows-Audio-Stack für Ultra-Low-Latency (2-10ms).', 'ar': 'تعريف ASIO عالمي لأي بطاقة صوت. يتجاوز مكدس صوت ويندوز لزمن استجابة فائق الانخفاض (2-10 مللي ثانية).'},
    "Install REAL": {'en': 'Reduce Audio Latency — patches the Windows audio pipeline to minimize latency without ASIO. Works system-wide on all applications. Reduces audio delay by modifying buffer sizes and thread priorities. The tool audiophile Redditors whisper about in niche threads.', 'fr': 'Réduit la latence audio en patchant le pipeline audio Windows. Fonctionne sur toutes les applications sans ASIO.', 'tn': 'Yna99es latence audio b patch pipeline audio Windows. Yakhdem 3la kol les applications bla ASIO.', 'es': 'Reduce la latencia de audio parcheando el pipeline de audio de Windows. Funciona en todas las aplicaciones sin ASIO.', 'de': 'Reduziert Audio-Latenz durch Patchen der Windows-Audio-Pipeline. Funktioniert systemweit ohne ASIO.', 'ar': 'يقلل زمن استجابة الصوت عبر تعديل خط أنابيب صوت ويندوز. يعمل على كل التطبيقات بدون ASIO.'},
    "Install Core-to-Core Latency": {'en': 'Measures inter-core communication latency in nanoseconds. Reveals CPU cache topology, NUMA nodes, chiplet boundaries. Shows which cores can talk fastest — essential for manual CPU affinity optimization. The tool that makes you understand WHY core pinning matters.', 'fr': "Mesure la latence inter-cœurs en nanosecondes. Révèle la topologie du cache, les nœuds NUMA, les chiplets. Essentiel pour l'affinité CPU.", 'tn': 'Y9is latence inter-cœurs b nanosecondes. Ykachef topologie cache, nœuds NUMA, chiplets. Essentiel lel CPU affinity.', 'es': 'Mide la latencia entre núcleos en nanosegundos. Revela topología de caché, nodos NUMA, chiplets. Esencial para afinidad CPU.', 'de': 'Misst Inter-Core-Latenz in Nanosekunden. Zeigt Cache-Topologie, NUMA-Knoten, Chiplet-Grenzen. Essenziell für CPU-Affinität.', 'ar': 'يقيس زمن الاتصال بين النوى بالنانو ثانية. يكشف طوبولوجيا الذاكرة المخبئية وعقد NUMA وحدود الشريحة.'},
    "Install Processes Priority Mgr": {'en': 'Set PERMANENT CPU priorities and affinities for any process. Unlike Task Manager (resets on restart), this persists across reboots. Auto-applies your rules whenever a process launches. The set-and-forget process priority tool nobody knows exists.', 'fr': 'Définissez des priorités CPU PERMANENTES pour tout processus. Contrairement au Gestionnaire des tâches, persiste après redémarrage.', 'tn': '7ot priorités CPU PERMANENTES l kol processus. Contrairement au Gestionnaire des tâches, yab9a ba3d restart.', 'es': 'Establece prioridades CPU PERMANENTES para cualquier proceso. A diferencia del Administrador de tareas, persiste tras reinicio.', 'de': 'PERMANENTE CPU-Prioritäten für jeden Prozess setzen. Bleibt im Gegensatz zum Task-Manager nach Neustart bestehen.', 'ar': 'تعيين أولويات CPU دائمة لأي عملية. على عكس مدير المهام، تستمر بعد إعادة التشغيل.'},
    "Install RAMMap": {'en': 'Sysinternals tool that shows EXACTLY what your physical RAM is being used for — Active, Standby, Modified, Page Table, Driver Locked, AWE. Purge standby list, see memory-mapped files, identify memory hogs at the physical page level. The tool RAM nerds dream about.', 'fr': "Outil Sysinternals montrant exactement l'utilisation de la RAM physique. Purge standby list, fichiers mappés en mémoire.", 'tn': 'Outil Sysinternals ywari ki famma utilisation RAM physique. Purge standby list, fichiers mappés en mémoire.', 'es': 'Herramienta Sysinternals que muestra exactamente el uso de RAM física. Purga standby list, archivos mapeados en memoria.', 'de': 'Sysinternals-Tool zeigt genaue physische RAM-Nutzung. Standby-Liste leeren, speicherabgebildete Dateien, Speicherfresser finden.', 'ar': 'أداة Sysinternals تظهر بالضبط استخدام الذاكرة الفعلية. تطهير قائمة الانتظار وملفات الذاكرة المعيّنة.'},
    "Install Windows Memory Cleaner": {'en': 'Lightweight tool to free standby list, modified page list, and working set memory with one click. The free, open-source alternative to ISLC (Intelligent Standby List Cleaner). Auto-clean when RAM usage exceeds threshold. Keeps your RAM fresh for gaming.', 'fr': "Outil léger pour libérer la standby list et la mémoire d'un clic. Alternative gratuite open-source à ISLC.", 'tn': 'Outil léger y7arrar standby list w mémoire b click wa7ed. Alternative gratuite open-source l ISLC.', 'es': 'Herramienta ligera para liberar standby list y memoria con un clic. Alternativa gratuita open-source a ISLC.', 'de': 'Leichtgewichtiges Tool zum Freigeben der Standby-Liste und des Arbeitsspeichers. Kostenlose Open-Source-Alternative zu ISLC.', 'ar': 'أداة خفيفة لتحرير قائمة الانتظار والذاكرة بنقرة. بديل مجاني مفتوح المصدر لـ ISLC.'},
    "Install DiskCountersView": {'en': 'NirSoft tool showing live disk performance counters per drive — read/write bytes per second, queue depth, average response time, split I/O count. See which drive is bottlenecking your system RIGHT NOW. The disk performance tool nobody downloads but everyone needs.', 'fr': 'Outil NirSoft montrant les compteurs de performance disque en direct — octets lus/écrits par seconde, profondeur de file.', 'tn': 'Outil NirSoft ywari compteurs performance disque live — octets lus/écrits par seconde, profondeur file.', 'es': 'Herramienta NirSoft que muestra contadores de rendimiento de disco en vivo — bytes leídos/escritos por segundo, profundidad de cola.', 'de': 'NirSoft-Tool zeigt Live-Festplattenleistungszähler — Lese-/Schreibbytes pro Sekunde, Warteschlangentiefe.', 'ar': 'أداة NirSoft تعرض عدادات أداء القرص المباشرة — بايت القراءة/الكتابة في الثانية وعمق قائمة الانتظار.'},
    "Install NetworkCountersWatch": {'en': 'NirSoft tool showing live network performance counters per adapter — bytes sent/received per second, packets, errors, discards, unicast/broadcast. The lightest network monitor that exists. See exactly what your NIC is doing at the hardware counter level.', 'fr': 'Outil NirSoft montrant les compteurs réseau en direct par adaptateur — octets envoyés/reçus, paquets, erreurs.', 'tn': 'Outil NirSoft ywari compteurs réseau live par adaptateur — octets envoyés/reçus, paquets, erreurs.', 'es': 'Herramienta NirSoft que muestra contadores de red en vivo por adaptador — bytes enviados/recibidos, paquetes, errores.', 'de': 'NirSoft-Tool zeigt Live-Netzwerkleistungszähler pro Adapter — gesendete/empfangene Bytes, Pakete, Fehler.', 'ar': 'أداة NirSoft تعرض عدادات أداء الشبكة المباشرة لكل محول — بايت مرسلة/مستقبلة وحزم وأخطاء.'},
    "Install Windhawk": {'en': 'The Xposed Framework for Windows. Injects community-made mods at runtime to change ANY Windows behavior — fix taskbar, Explorer, Start Menu, system tray, title bars. 600+ mods on the Windhawk mod hub. The modding tool that makes ExplorerPatcher look like a toy.', 'fr': 'Framework de modding Windows. Injecte des mods communautaires pour modifier tout comportement Windows — taskbar, Explorer, menu Start. 600+ mods.', 'tn': 'Framework modding Windows. Y injecti mods communautaires bech ybaddel ay 7aja fi Windows — taskbar, Explorer, Start Menu. 600+ mods.', 'es': 'Framework de modding de Windows. Inyecta mods comunitarios para cambiar cualquier comportamiento — barra de tareas, Explorer, menú Inicio. 600+ mods.', 'de': 'Windows-Modding-Framework. Injiziert Community-Mods zur Laufzeit um JEDES Windows-Verhalten zu ändern — Taskbar, Explorer, Startmenü. 600+ Mods.', 'ar': 'إطار عمل تعديل ويندوز. يحقن تعديلات مجتمعية لتغيير أي سلوك — شريط المهام والمستكشف وقائمة ابدأ. 600+ تعديل.'},
    "Install Nilesoft Shell": {'en': 'COMPLETELY replaces the Windows right-click context menu with a beautiful, fast, infinitely customizable alternative. Custom commands, icons, cascading submenus, conditional items, separators, keyboard shortcuts. Written in C, loads in microseconds. The context menu Windows should have shipped.', 'fr': "Remplace COMPLÈTEMENT le menu clic-droit Windows par un menu rapide et personnalisable à l'infini. Commandes, icônes, sous-menus, raccourcis.", 'tn': 'Y baddel KOLESH le menu clic-droit Windows b menu sari3 w personnalisable. Commandes, icônes, sous-menus, raccourcis. Écrit en C.', 'es': 'Reemplaza COMPLETAMENTE el menú de clic derecho con una alternativa rápida e infinitamente personalizable. Comandos, iconos, submenús.', 'de': 'Ersetzt das Windows-Rechtsklickmenü KOMPLETT durch ein schnelles, unendlich anpassbares Menü. Befehle, Icons, Untermenüs, Tastenkürzel.', 'ar': 'يستبدل تماماً قائمة النقر بزر الماوس الأيمن بقائمة سريعة وقابلة للتخصيص بلا حدود. أوامر وأيقونات وقوائم فرعية.'},
    "Install Seelen UI": {'en': 'Turns Windows 11 into a fully riced desktop environment. Auto-tiling window manager + custom taskbar + app launcher + system widgets + workspace manager. What happens when Linux desktop enthusiasts build for Windows. The most ambitious Windows UI overhaul project that exists.', 'fr': 'Transforme Windows 11 en un environnement bureau personnalisé. Tiling WM + taskbar + lanceur + widgets. Le projet UI Windows le plus ambitieux.', 'tn': 'Y7awwel Windows 11 l environment bureau personnalisé. Tiling WM + taskbar + lanceur + widgets. A9wa projet UI Windows yji.', 'es': 'Convierte Windows 11 en un escritorio completamente personalizado. WM de mosaico + barra de tareas + lanzador + widgets. El proyecto UI más ambicioso.', 'de': 'Verwandelt Windows 11 in eine vollständig angepasste Desktop-Umgebung. Tiling WM + Taskbar + Launcher + Widgets. Das ambitionierteste Windows-UI-Projekt.', 'ar': 'يحول ويندوز 11 إلى بيئة سطح مكتب مخصصة بالكامل. مدير نوافذ + شريط مهام + مشغل + ودجات. أطموح مشروع واجهة ويندوز.'},
    "Install komorebi": {'en': 'Tiling window manager for Windows written in Rust. Automatic i3/bspwm-style window tiling with workspaces, rules, gaps, focus-follows-mouse. Keyboard-driven workflow. For people who want Linux tiling on Windows without the Linux. Works with YASB or Seelen UI as a status bar.', 'fr': 'Gestionnaire de fenêtres en mosaïque écrit en Rust. Tiling automatique style i3/bspwm avec espaces de travail. Pour ceux qui veulent le tiling Linux sur Windows.', 'tn': 'Gestionnaire fenêtres mosaïque écrit en Rust. Tiling automatique style i3/bspwm m3a espaces de travail. Lelli y7eb tiling Linux 3la Windows.', 'es': 'Gestor de ventanas en mosaico escrito en Rust. Mosaico automático estilo i3/bspwm con espacios de trabajo. Para quienes quieren mosaico Linux en Windows.', 'de': 'Tiling-Fenstermanager für Windows in Rust geschrieben. Automatisches i3/bspwm-style Tiling mit Workspaces. Für Linux-Tiling auf Windows.', 'ar': 'مدير نوافذ تبليط لويندوز مكتوب بـ Rust. تبليط تلقائي بأسلوب i3 مع مساحات عمل. لمن يريد تبليط لينكس على ويندوز.'},
    "Install Textify": {'en': "Click on ANY text in ANY window and copy it — even text that Windows normally doesn't let you select. Error dialogs, About boxes, installer messages, status bars, buttons labels. Made by the same legend who created 7+ Taskbar Tweaker. The tool that makes you wonder why Windows can't do this natively.", 'fr': "Cliquez sur N'IMPORTE QUEL texte et copiez-le — même le texte non-sélectionnable. Boîtes d'erreur, installeurs, barres d'état.", 'tn': "Click 3la AY texte w copieh — 7atta texte elli Windows ma y5allikch t selectih. Boîtes d'erreur, installeurs, barres d'état.", 'es': 'Haz clic en CUALQUIER texto y cópialo — incluso texto que Windows no deja seleccionar. Diálogos de error, instaladores, barras de estado.', 'de': 'Klicken Sie auf JEDEN Text und kopieren Sie ihn — auch nicht-auswählbaren Text. Fehlerdialoge, Installer, Statusleisten.', 'ar': 'انقر على أي نص وانسخه — حتى النص الذي لا يسمح ويندوز بتحديده. مربعات الخطأ والمثبتات وأشرطة الحالة.'},
    "Install Sizer": {'en': "Right-click any window's resize grip and pick an exact pixel size from a menu. Presets for 1920x1080, 1280x720, or any custom size. Essential for consistent screenshots, video recording at specific resolutions, web development viewport testing. The tiny tool with zero UI that solves a problem nobody else fixes.", 'fr': "Clic-droit sur la bordure d'une fenêtre pour choisir une taille exacte en pixels. Présets 1920x1080, 1280x720, ou taille personnalisée.", 'tn': 'Clic-droit 3la bordure fenêtre bech t5tar taille exacte b pixels. Présets 1920x1080, 1280x720, wella taille personnalisée.', 'es': 'Clic derecho en el borde de ventana para elegir tamaño exacto en píxeles. Presets 1920x1080, 1280x720 o tamaño personalizado.', 'de': 'Rechtsklick auf Fensterrand für exakte Pixelgröße. Voreinstellungen für 1920x1080, 1280x720 oder benutzerdefinierte Größe.', 'ar': 'انقر بزر الماوس الأيمن على حافة النافذة لاختيار حجم دقيق بالبكسل. إعدادات مسبقة 1920×1080 أو أي حجم مخصص.'},
    "Install ZoomIt": {'en': 'Sysinternals screen magnifier and annotation tool by Mark Russinovich himself. Zoom into any screen area with a hotkey, draw arrows/shapes/text live, set a presentation countdown timer. Zero install, zero UI, maximum power. The tool every presenter needs but nobody finds.', 'fr': "Loupe d'écran et outil d'annotation Sysinternals par Mark Russinovich. Zoomez, dessinez en direct, minuteur de présentation.", 'tn': 'Loupe écran w outil annotation Sysinternals par Mark Russinovich. Zoomez, dessinez en direct, minuteur présentation.', 'es': 'Lupa de pantalla y herramienta de anotación Sysinternals por Mark Russinovich. Zoom, dibujo en vivo, temporizador de presentación.', 'de': 'Sysinternals Bildschirmlupe und Annotations-Tool von Mark Russinovich. Zoomen, live zeichnen, Präsentations-Countdown.', 'ar': 'مكبر شاشة وأداة تعليق من Sysinternals بواسطة مارك روسينوفيتش. تكبير ورسم مباشر ومؤقت عرض تقديمي.'},
    "Install scrcpy": {'en': 'Display and control your Android phone on your PC over USB or WiFi. No root required, no app to install on the phone. Sub-100ms latency, 60fps, audio forwarding, copy-paste between phone and PC. Record your phone screen. The tool that replaces $50 phone mirroring apps with a free open-source masterpiece.', 'fr': "Affichez et contrôlez votre Android sur PC via USB ou WiFi. Pas de root, pas d'app. Latence <100ms, 60fps, audio, copier-coller.", 'tn': 'Wari w controli Android 3la PC via USB wella WiFi. Bla root, bla app. Latence <100ms, 60fps, audio, copier-coller.', 'es': 'Muestra y controla tu Android en PC por USB o WiFi. Sin root, sin app. Latencia <100ms, 60fps, audio, copiar-pegar.', 'de': 'Android-Handy auf dem PC anzeigen und steuern via USB oder WiFi. Kein Root, keine App. <100ms Latenz, 60fps, Audio, Copy-Paste.', 'ar': 'اعرض وتحكم بهاتف أندرويد على الكمبيوتر عبر USB أو WiFi. بدون روت، بدون تطبيق. أقل من 100 مللي ثانية.'},
    "Install WhatIsHang": {'en': "When a program freezes and you see 'Not Responding', this NirSoft tool attaches to the hung process and tells you EXACTLY which DLL function is stuck. Is it waiting for disk I/O? Network? A locked resource? Like giving a doctor an MRI of your frozen app. The diagnostic tool that should be built into Windows.", 'fr': "Quand un programme gèle, cet outil NirSoft s'attache au processus et montre EXACTEMENT quelle fonction DLL est bloquée. I/O disque ? Réseau ?", 'tn': "Ki programme y geli, l'outil NirSoft heda y attacha lel processus w ywari EXACTEMENT anhi fonction DLL bloquée. I/O disque ? Réseau ?", 'es': 'Cuando un programa se congela, esta herramienta NirSoft muestra EXACTAMENTE qué función DLL está atascada. ¿E/S de disco? ¿Red?', 'de': 'Wenn ein Programm hängt, zeigt dieses NirSoft-Tool GENAU welche DLL-Funktion blockiert ist. Festplatten-I/O? Netzwerk?', 'ar': 'عندما يتجمد برنامج، تتصل أداة NirSoft هذه بالعملية وتظهر بالضبط أي دالة DLL متوقفة. هل ينتظر القرص أم الشبكة؟'},
    "Install SophiApp": {'en': 'The beautiful GUI companion to Sophia Script. Toggle 150+ Windows debloating and privacy settings with checkboxes instead of PowerShell. Remove OneDrive, disable telemetry, unpin apps, configure privacy — all visually. Made by the same team. If Sophia Script is the CLI, SophiApp is the remote control.', 'fr': 'GUI compagnon de Sophia Script. Activez/désactivez 150+ paramètres Windows avec des cases au lieu de PowerShell. OneDrive, télémétrie, confidentialité.', 'tn': 'GUI compagnon ta3 Sophia Script. Activez/désactivez 150+ paramètres Windows b cases blasa PowerShell. OneDrive, télémétrie, confidentialité.', 'es': 'GUI compañera de Sophia Script. Activa/desactiva 150+ ajustes Windows con casillas en vez de PowerShell. OneDrive, telemetría, privacidad.', 'de': 'GUI-Begleiter zu Sophia Script. 150+ Windows-Einstellungen per Checkbox statt PowerShell. OneDrive, Telemetrie, Datenschutz.', 'ar': 'الواجهة الرسومية المرافقة لـ Sophia Script. تبديل 150+ إعداد ويندوز بمربعات اختيار بدلاً من PowerShell.'},
    "Install O&O AppBuster": {'en': 'See every preinstalled Windows app — bloatware, hidden packages, provisioned apps — and remove them with one click. Shows which apps are safe to remove vs. system-critical. Remove Cortana, Xbox Game Bar, Your Phone, Get Help, and 50+ other apps you never asked for. Free, no install required.', 'fr': 'Voyez chaque appli préinstallée et supprimez-les en un clic. Montre lesquelles sont sûres à supprimer. Cortana, Xbox, Your Phone, 50+ apps.', 'tn': 'Chouf kol application préinstallée w na77iha b click. Ywari anhi apps sûres bech tna77iha. Cortana, Xbox, Your Phone, 50+ apps.', 'es': 'Ve cada app preinstalada y elimínala con un clic. Muestra cuáles son seguras de eliminar. Cortana, Xbox, Your Phone, 50+ apps.', 'de': 'Alle vorinstallierten Windows-Apps sehen und mit einem Klick entfernen. Zeigt welche sicher zu entfernen sind. Cortana, Xbox, 50+ Apps.', 'ar': 'شاهد كل تطبيق مثبت مسبقاً واحذفه بنقرة. يظهر التطبيقات الآمنة للحذف. كورتانا وXbox و50+ تطبيقاً لم تطلبه.'},
    "Install BleachBit": {'en': 'The open-source disk cleaner that CCleaner was before Avast bought it. Cleans browser cache, cookies, logs, temp files, thumbnails, recycle bin — for 90+ applications. No ads, no upsells, no bundled software, no PUPs. Used by journalists and activists for secure file deletion. Open source, auditable, trustworthy.', 'fr': 'Le nettoyeur de disque open-source que CCleaner était avant Avast. Cache navigateur, logs, temp, corbeille. Pas de pub, pas de bloatware.', 'tn': 'Nettoyeur disque open-source elli CCleaner ken 9bal Avast. Cache navigateur, logs, temp, corbeille. Bla pub, bla bloatware.', 'es': 'El limpiador de disco open-source que era CCleaner antes de Avast. Caché del navegador, logs, temp, papelera. Sin anuncios ni bloatware.', 'de': 'Der Open-Source-Festplattenreiniger, der CCleaner vor Avast war. Browser-Cache, Logs, Temp, Papierkorb. Keine Werbung, keine Bloatware.', 'ar': 'منظف الأقراص مفتوح المصدر الذي كان CCleaner قبل أن تشتريه Avast. ذاكرة المتصفح والسجلات والمؤقتات. بدون إعلانات.'},
    "Install SharpKeys": {'en': 'Remap any keyboard key to any other key — at the Windows registry level. No background process, no driver, no service. Swap Caps Lock and Ctrl, disable Windows key, remap anything. Changes take effect at next login and persist forever. The most elegant key remapping solution that exists.', 'fr': "Remappez n'importe quelle touche au niveau du registre Windows. Pas de processus, pas de pilote. Échangez Caps Lock et Ctrl, désactivez touche Windows.", 'tn': 'Remappez ay touche au niveau registre Windows. Bla processus, bla pilote. Badlou Caps Lock w Ctrl, désactivez touche Windows.', 'es': 'Reasigna cualquier tecla a nivel de registro de Windows. Sin proceso, sin driver. Intercambia Caps Lock y Ctrl, desactiva tecla Windows.', 'de': 'Tastenzuordnung auf Registry-Ebene. Kein Prozess, kein Treiber. Caps Lock und Strg tauschen, Windows-Taste deaktivieren.', 'ar': 'أعد تعيين أي مفتاح على مستوى سجل ويندوز. بدون عملية أو تعريف. بدّل Caps Lock وCtrl أو عطّل مفتاح Windows.'},
    "Install ContextMenuManager": {'en': 'See EVERY entry in your right-click context menu and manage them all. Enable, disable, delete entries added by programs you installed. Find out why your context menu has 30 items. Separate management for File, Folder, Directory, Desktop, and New menus. The context menu detective.', 'fr': 'Voyez CHAQUE entrée du menu clic-droit et gérez-les. Activez, désactivez, supprimez les entrées ajoutées par des programmes. Menus Fichier, Dossier, Bureau.', 'tn': 'Chouf KOL entrée fil menu clic-droit w gérez. Activez, désactivez, supprimez entrées ajoutées par programmes. Menus Fichier, Dossier, Bureau.', 'es': 'Ve CADA entrada del menú clic derecho y gestiónala. Activa, desactiva, elimina entradas de programas instalados. Menús Archivo, Carpeta, Escritorio.', 'de': 'JEDEN Eintrag im Rechtsklickmenü sehen und verwalten. Einträge aktivieren, deaktivieren, löschen. Datei-, Ordner-, Desktop-Menüs.', 'ar': 'شاهد كل إدخال في قائمة النقر بزر الماوس الأيمن وأدرها. فعّل أو عطّل أو احذف إدخالات البرامج.'},
    "Install Sandboxie-Plus": {'en': "Run ANY program in a completely isolated sandbox. The app thinks it's running normally, but all changes go into a virtual container that you can delete. Test suspicious downloads, try software before committing, browse sketchy websites safely. Originally a $40 commercial product, now free and open-source.", 'fr': "Exécutez N'IMPORTE QUEL programme dans un sandbox isolé. Testez des téléchargements suspects, essayez des logiciels. Ancien produit commercial à 40$.", 'tn': 'Exécutez AY programme fi sandbox isolé. Testez téléchargements suspects, essayez logiciels. Ken produit commercial b 40$, tawa free.', 'es': 'Ejecuta CUALQUIER programa en un sandbox aislado. Prueba descargas sospechosas, prueba software. Antes producto comercial de $40, ahora gratuito.', 'de': 'JEDES Programm in einer isolierten Sandbox ausführen. Verdächtige Downloads testen, Software ausprobieren. Ehemals $40, jetzt kostenlos.', 'ar': 'شغّل أي برنامج في صندوق رمل معزول تماماً. اختبر التنزيلات المشتبه بها. كان منتجاً تجارياً بـ 40 دولاراً والآن مجاني.'},
    "Install Lively Wallpaper": {'en': 'Set videos, GIFs, YouTube URLs, HTML webpages, Unity/Godot games, or GLSL shaders as your desktop wallpaper. GPU-accelerated, pauses when apps are maximized (zero CPU impact). Free open-source alternative to Wallpaper Engine. Community gallery with hundreds of wallpapers. The living desktop.', 'fr': "Définissez vidéos, GIFs, URLs YouTube, pages web comme fond d'écran. Accéléré GPU, pause quand apps sont maximisées. Alternative gratuite à Wallpaper Engine.", 'tn': "7ot vidéos, GIFs, URLs YouTube, pages web ka fond d'écran. GPU-accéléré, pause ki apps maximisées. Alternative gratuite l Wallpaper Engine.", 'es': 'Pon videos, GIFs, URLs de YouTube, páginas web como fondo de escritorio. GPU-acelerado, pausa con apps maximizadas. Alternativa gratuita a Wallpaper Engine.', 'de': 'Videos, GIFs, YouTube-URLs, Webseiten als Desktop-Hintergrund. GPU-beschleunigt, Pause bei maximierten Apps. Kostenlose Wallpaper Engine Alternative.', 'ar': 'اجعل الفيديو وGIF وصفحات الويب خلفية سطح مكتبك. مسرّع بـ GPU ويتوقف تلقائياً. بديل مجاني لـ Wallpaper Engine.'},
    "Install QTTabBar": {'en': 'Adds REAL tabbed browsing to Windows Explorer — open multiple folders in tabs within a single Explorer window. Tab groups, folder previews, file content preview on hover, keyboard shortcuts, custom toolbars. The feature Microsoft tried to add in Windows 11 but did poorly. Open source and rock solid.', 'fr': "Ajoute de VRAIS onglets à l'Explorateur Windows. Plusieurs dossiers en onglets, prévisualisation, raccourcis clavier. Ce que Microsoft a mal fait dans Windows 11.", 'tn': 'Yzid onglets VRAIS lel Explorateur Windows. Plusieurs dossiers fi onglets, prévisualisation, raccourcis clavier. Elli Microsoft 3amlitha m7alkha fi Win 11.', 'es': 'Añade pestañas REALES al Explorador de Windows. Múltiples carpetas en pestañas, previsualización, atajos de teclado. Lo que Microsoft hizo mal en Win 11.', 'de': 'Echte Tabs im Windows Explorer. Mehrere Ordner in Tabs, Vorschau, Tastenkürzel. Was Microsoft in Windows 11 schlecht gemacht hat.', 'ar': 'يضيف تبويبات حقيقية لمستكشف ويندوز. مجلدات متعددة في تبويبات ومعاينة واختصارات لوحة المفاتيح. ما فشلت مايكروسوفت فيه.'},
    "Install PatchCleaner": {'en': "Your C:\\Windows\\Installer folder is secretly eating 5-30GB of disk space with orphaned .msp and .msi files from old updates. PatchCleaner identifies which patches are still needed vs. safely deletable. Recover gigabytes of wasted space that Windows Disk Cleanup can't touch. The disk space tool nobody knows about.", 'fr': 'Votre dossier C:\\Windows\\Installer mange secrètement 5-30GB avec des fichiers .msp orphelins. PatchCleaner identifie lesquels sont supprimables. Récupérez des Go.', 'tn': 'Dossier C:\\Windows\\Installer yakol 5-30GB b fichiers .msp orphelins. PatchCleaner y identifie anhi supprimables. Récupérez Go mel espace.', 'es': 'Tu carpeta C:\\Windows\\Installer consume secretamente 5-30GB con archivos .msp huérfanos. PatchCleaner identifica cuáles son eliminables. Recupera GB.', 'de': 'C:\\Windows\\Installer frisst 5-30GB mit verwaisten .msp-Dateien. PatchCleaner findet löschbare Patches. Gigabytes zurückgewinnen.', 'ar': 'مجلد C:\\Windows\\Installer يستهلك سراً 5-30 غيغابايت بملفات يتيمة. PatchCleaner يحدد الملفات القابلة للحذف بأمان.'},
    "Install SpaceSniffer": {'en': "Instant visual treemap of your entire disk. See EXACTLY what's eating your storage in colored rectangles proportional to file/folder size. Click to drill deeper, right-click to act. Updates in real-time as you delete things. The fastest way to answer 'where did all my disk space go?' Makes WizTree look like a spreadsheet.", 'fr': 'Treemap visuel instantané de votre disque. Voyez EXACTEMENT ce qui mange votre espace en rectangles colorés proportionnels. Temps réel, interactif.', 'tn': 'Treemap visuel instantané ta3 disque. Chouf EXACTEMENT chnou yakol espace fi rectangles colorés proportionnels. Temps réel, interactif.', 'es': 'Mapa visual instantáneo de tu disco. Ve EXACTAMENTE qué consume espacio en rectángulos proporcionales. Tiempo real, interactivo.', 'de': 'Sofortige visuelle Treemap Ihrer Festplatte. Sehen Sie GENAU was Speicher frisst — proportionale Farbrechtecke. Echtzeit, interaktiv.', 'ar': 'خريطة شجرية مرئية فورية لقرصك. شاهد بالضبط ما يستهلك مساحتك بمستطيلات ملونة متناسبة. تحديث فوري.'},
    "Install DNS Jumper": {'en': 'One-click DNS server switcher and speed tester by Sordum. Tests 20+ DNS servers (Google, Cloudflare, Quad9, OpenDNS...) and shows latency for each. Switch your DNS instantly without digging through network settings. Also flushes DNS cache. The fastest way to optimize your DNS. Portable, no install.', 'fr': 'Changeur DNS et testeur de vitesse en un clic par Sordum. Teste 20+ serveurs DNS et montre la latence. Changez DNS sans paramètres réseau.', 'tn': 'Changeur DNS w testeur vitesse b click wa7ed par Sordum. Teste 20+ serveurs DNS w ywari latence. Baddel DNS bla paramètres réseau.', 'es': 'Cambiador DNS y tester de velocidad en un clic por Sordum. Prueba 20+ servidores DNS y muestra latencia. Cambia DNS sin configuración de red.', 'de': 'DNS-Wechsler und Geschwindigkeitstester von Sordum. Testet 20+ DNS-Server und zeigt Latenz. DNS sofort wechseln ohne Netzwerkeinstellungen.', 'ar': 'مبدّل DNS واختبار سرعة بنقرة واحدة من Sordum. يختبر 20+ خادم DNS ويظهر زمن الاستجابة. بدّل DNS بدون إعدادات الشبكة.'},
    "Install OpenHashTab": {'en': "Adds a 'Hashes' tab to the Windows file Properties dialog. Right-click any file, go to Properties, see SHA-1, SHA-256, SHA-512, MD5, CRC32, xxHash — all calculated automatically. Compare hashes by pasting expected values. Verify downloads are legitimate without opening a terminal. Shell extension that weighs 1MB.", 'fr': "Ajoute un onglet 'Hashes' aux Propriétés de fichier. SHA-256, MD5, CRC32 — calculés automatiquement. Vérifiez les téléchargements sans terminal.", 'tn': "Yzid onglet 'Hashes' lel Propriétés fichier. SHA-256, MD5, CRC32 — calculés automatiquement. Vérifiez téléchargements bla terminal.", 'es': "Añade una pestaña 'Hashes' a las Propiedades de archivo. SHA-256, MD5, CRC32 — calculados automáticamente. Verifica descargas sin terminal.", 'de': "Fügt einen 'Hashes'-Tab zu Dateieigenschaften hinzu. SHA-256, MD5, CRC32 — automatisch berechnet. Downloads ohne Terminal verifizieren.", 'ar': "يضيف تبويب 'Hashes' لخصائص الملف. SHA-256 وMD5 وCRC32 — محسوبة تلقائياً. تحقق من التنزيلات بدون سطر أوامر."},
    "Install USBDeview": {'en': "Shows EVERY USB device that has EVER been connected to your PC — with vendor name, serial number, connection date, last plug/unplug time, device status. Disconnect, disable, or uninstall old USB drivers. Find which USB port a device was connected to. Forensic-level USB history that Windows Task Manager can't show.", 'fr': 'Montre CHAQUE périphérique USB jamais connecté — nom, numéro de série, date connexion. Déconnectez, désactivez, désinstallez anciens pilotes USB.', 'tn': 'Ywari KOL périphérique USB elli connecta — nom, numéro série, tarikh connexion. Déconnectez, désactivez, désinstallez anciens pilotes USB.', 'es': 'Muestra CADA dispositivo USB que se conectó — nombre, número de serie, fecha de conexión. Desconecta, desactiva, desinstala drivers USB viejos.', 'de': 'Zeigt JEDES jemals verbundene USB-Gerät — Name, Seriennummer, Verbindungsdatum. Alte USB-Treiber trennen, deaktivieren, deinstallieren.', 'ar': 'يظهر كل جهاز USB اتصل بالكمبيوتر — الاسم والرقم التسلسلي وتاريخ الاتصال. افصل أو عطّل أو أزل التعريفات القديمة.'},
    "Install OCCT": {'en': 'All-in-one stability testing and monitoring tool. CPU, GPU, RAM, PSU stress tests with real-time error detection. If your overclock is unstable, OCCT will find it. Built-in hardware monitoring with graphs. The overclocker\'s validation tool.', 'fr': 'Test de stabilité tout-en-un. Tests de stress CPU, GPU, RAM, PSU avec détection d\'erreurs en temps réel. L\'outil de validation des overclockeurs.', 'tn': 'Test stabilité tout-en-un. Stress test CPU, GPU, RAM, PSU b détection erreurs en temps réel. Outil validation overclocking.', 'es': 'Prueba de estabilidad todo en uno. Estrés CPU, GPU, RAM, PSU con detección de errores en tiempo real. La herramienta de validación del overclocker.', 'de': 'All-in-one Stabilitätstest. CPU, GPU, RAM, PSU Stresstests mit Echtzeit-Fehlererkennung. Das Validierungstool für Übertakter.', 'ar': 'أداة اختبار استقرار شاملة. اختبارات ضغط المعالج وGPU والذاكرة مع كشف الأخطاء. أداة التحقق للمعجّلين.'},
    "Install FurMark": {'en': 'The most brutal GPU stress test in existence. Pushes your graphics card to absolute maximum power draw and temperature. If your GPU can survive FurMark, it can survive anything. Also useful for testing GPU cooling and stability after overclocking.', 'fr': 'Le test de stress GPU le plus brutal. Pousse votre carte graphique à la puissance et température maximales absolues. Si votre GPU survit à FurMark, il survit à tout.', 'tn': 'A9wa stress test GPU mawjoud. Yd5ol el carte graphique lel maximum absolu ta3 puissance w 7arara. Ken GPU ta3ek yosbor FurMark, yosbor kolchi.', 'es': 'La prueba de estrés GPU más brutal. Lleva tu tarjeta gráfica al máximo absoluto de potencia y temperatura. Si tu GPU sobrevive FurMark, sobrevive a todo.', 'de': 'Der brutalste GPU-Stresstest. Treibt die Grafikkarte an absolute Leistungs- und Temperaturgrenze. Wenn Ihre GPU FurMark übersteht, übersteht sie alles.', 'ar': 'أقسى اختبار ضغط GPU. يدفع بطاقة الرسوم لأقصى طاقة وحرارة. إذا نجت GPU من FurMark فستنجو من أي شيء.'},
    "Install Core Temp": {'en': 'Lightweight CPU temperature monitor that reads DTS (Digital Thermal Sensor) directly from each core. Shows per-core temperatures, load, frequency. Tiny system tray footprint. Supports every Intel and AMD processor. The simplest way to keep an eye on CPU temps.', 'fr': 'Moniteur de température CPU léger. Lit le capteur thermique de chaque cœur. Températures par cœur dans la barre système.', 'tn': 'Moniteur température CPU khfif. Ya9ra 7arara kol noyau directement. Températures par cœur fil system tray.', 'es': 'Monitor de temperatura CPU ligero. Lee el sensor térmico de cada núcleo. Temperaturas por núcleo en la bandeja del sistema.', 'de': 'Leichter CPU-Temperaturmonitor. Liest den Temperatursensor jedes Kerns direkt aus. Pro-Kern-Temperaturen im System Tray.', 'ar': 'مراقب حرارة معالج خفيف. يقرأ المستشعر الحراري لكل نواة مباشرة. درجات حرارة كل نواة في شريط النظام.'},
    "Install AIDA64": {'en': 'The most comprehensive hardware information and benchmarking tool. CPU, RAM, GPU, motherboard — every sensor, every spec, every detail. Stress testing, memory benchmarks, sensor monitoring with logging. The tool hardware reviewers use. Nothing else comes close.', 'fr': 'L\'outil d\'information matérielle et de benchmark le plus complet. CPU, RAM, GPU, carte mère — chaque capteur, chaque spec, chaque détail.', 'tn': 'A7sen outil information matérielle w benchmark. CPU, RAM, GPU, carte mère — kol capteur, kol spec, kol détail.', 'es': 'La herramienta de información de hardware y benchmark más completa. CPU, RAM, GPU, placa base — cada sensor, cada spec, cada detalle.', 'de': 'Das umfassendste Hardware-Info- und Benchmark-Tool. CPU, RAM, GPU, Mainboard — jeder Sensor, jede Spec, jedes Detail.', 'ar': 'أشمل أداة معلومات عتاد ومعايير. المعالج والذاكرة وGPU واللوحة الأم — كل مستشعر وكل مواصفة وكل تفصيل.'},
    "Install KeePassXC": {'en': 'Open-source offline password manager. Your vault stays on YOUR device — no cloud, no subscription, no trust required. Auto-type, browser integration, TOTP, YubiKey, SSH agent. The password manager for people who understand security.', 'fr': 'Gestionnaire de mots de passe open-source hors-ligne. Votre coffre reste sur VOTRE appareil — pas de cloud, pas d\'abonnement.', 'tn': 'Gestionnaire mots de passe open-source offline. El coffre yab9a 3andek — bla cloud, bla abonnement, bla thiq fi 7add.', 'es': 'Gestor de contraseñas open-source offline. Tu bóveda se queda en TU dispositivo — sin nube, sin suscripción.', 'de': 'Open-Source-Passwortmanager offline. Ihr Tresor bleibt auf IHREM Gerät — keine Cloud, kein Abo nötig.', 'ar': 'مدير كلمات مرور مفتوح المصدر بدون إنترنت. خزنتك تبقى على جهازك — بدون سحابة ولا اشتراك.'},
    "Install Bitwarden": {'en': 'Free open-source password manager with cloud sync. Cross-platform: Windows, Mac, Linux, iOS, Android, browser extensions. Auto-fill passwords, generate secure passwords, share vaults with family. The best free cloud password manager — period.', 'fr': 'Gestionnaire de mots de passe open-source gratuit avec synchronisation cloud. Multi-plateforme, auto-remplissage, génération.', 'tn': 'Gestionnaire mots de passe open-source gratuit b cloud sync. Multi-plateforme, auto-fill, génération mots de passe.', 'es': 'Gestor de contraseñas open-source gratis con sincronización en la nube. Multiplataforma, autocompletar, generar contraseñas.', 'de': 'Kostenloser Open-Source-Passwortmanager mit Cloud-Sync. Plattformübergreifend, Auto-Fill, Passwortgenerierung.', 'ar': 'مدير كلمات مرور مجاني مفتوح المصدر مع مزامنة سحابية. متعدد المنصات، ملء تلقائي، توليد كلمات مرور.'},
    "Install Malwarebytes": {'en': 'Industry-leading malware scanner and removal tool. Catches threats that Windows Defender misses. Real-time protection, ransomware shield, exploit prevention. Free version does excellent on-demand scanning. Run it alongside Defender for maximum protection.', 'fr': 'Scanner de malware leader du secteur. Attrape les menaces que Windows Defender manque. Analyse à la demande excellente en version gratuite.', 'tn': 'A7sen scanner malware. Yla99a menaces eli Windows Defender ma ychoufhomch. Version gratuite ta3mel scan excellent.', 'es': 'Escáner de malware líder del sector. Detecta amenazas que Windows Defender no ve. Escaneo bajo demanda excelente en versión gratuita.', 'de': 'Branchenführender Malware-Scanner. Erkennt Bedrohungen die Windows Defender übersieht. Exzellenter On-Demand-Scan in der Gratisversion.', 'ar': 'ماسح برمجيات خبيثة رائد في المجال. يكتشف تهديدات يفوتها Windows Defender. فحص ممتاز عند الطلب في النسخة المجانية.'},
    "Install Brave Browser": {'en': 'Privacy-focused Chromium browser with built-in ad and tracker blocking. 3x faster page loads than Chrome. No extensions needed for basic privacy. Tor integration, IPFS support, crypto wallet. The browser for people who are tired of being tracked.', 'fr': 'Navigateur Chromium axé sur la vie privée avec blocage intégré des pubs et traceurs. 3x plus rapide que Chrome.', 'tn': 'Navigateur Chromium axé vie privée b blocage pubs w traceurs intégré. 3x asra3 men Chrome. Bla extensions lel privacy.', 'es': 'Navegador Chromium centrado en privacidad con bloqueo integrado de anuncios y rastreadores. 3x más rápido que Chrome.', 'de': 'Datenschutzorientierter Chromium-Browser mit eingebautem Werbe-/Tracker-Blocker. 3x schnellere Seitenladev als Chrome.', 'ar': 'متصفح Chromium للخصوصية مع حظر إعلانات ومتتبعات مدمج. أسرع 3 مرات من Chrome. بدون إضافات للخصوصية الأساسية.'},
    "Install Wireshark": {'en': 'The world\'s most popular network protocol analyzer. Capture and inspect every packet flowing through your network interface. Deep inspection of hundreds of protocols. Essential for network troubleshooting, security analysis, and understanding what your PC sends over the wire.', 'fr': 'L\'analyseur de protocoles réseau le plus populaire. Capturez et inspectez chaque paquet. Essentiel pour le dépannage réseau et l\'analyse de sécurité.', 'tn': 'A7sen analyseur protocoles réseau. Capture w inspecte kol paquet. Essentiel lel dépannage réseau w analyse sécurité.', 'es': 'El analizador de protocolos de red más popular. Captura e inspecciona cada paquete. Esencial para diagnóstico de red y análisis de seguridad.', 'de': 'Der weltweit beliebteste Netzwerkprotokoll-Analyzer. Jedes Paket erfassen und inspizieren. Unverzichtbar für Netzwerk-Troubleshooting.', 'ar': 'أشهر محلل بروتوكولات شبكة في العالم. التقط وافحص كل حزمة. ضروري لاستكشاف أخطاء الشبكة وتحليل الأمان.'},
    "Install WinDirStat": {'en': 'Visual disk space analyzer with colorful treemap. Instantly see which folders and file types consume the most space. Drill down into directories, right-click to clean up. The classic \'where did my disk space go?\' tool that has saved millions of users.', 'fr': 'Analyseur d\'espace disque visuel avec treemap coloré. Voyez instantanément quels dossiers consomment le plus d\'espace.', 'tn': 'Analyseur espace disque visuel b treemap coloré. Tchouf fi th7a quel dossiers yaklou a9all espace.', 'es': 'Analizador visual de espacio en disco con mapa de árbol colorido. Ve instantáneamente qué carpetas consumen más espacio.', 'de': 'Visueller Speicherplatz-Analyzer mit farbiger Treemap. Sofort sehen welche Ordner am meisten Platz verbrauchen.', 'ar': 'محلل مساحة قرص مرئي بخريطة شجرية ملونة. شاهد فوراً أي مجلدات تستهلك أكثر مساحة.'},
    "Install FastCopy": {'en': 'The fastest file copy/move/delete tool for Windows. Bypasses Windows Explorer\'s slow copy engine using direct I/O. 2-3x faster than normal copy for large files. Verify with hash after copy, auto-retry on error, filter by extension. Essential for moving large datasets.', 'fr': 'L\'outil de copie/déplacement le plus rapide pour Windows. 2-3x plus rapide que l\'Explorateur pour les gros fichiers. Vérification hash après copie.', 'tn': 'A7sen outil copie/déplacement lel Windows. 2-3x asra3 mel Explorateur lel fichiers kbar. Vérification hash ba3d el copie.', 'es': 'La herramienta de copia más rápida para Windows. 2-3x más rápida que el Explorador para archivos grandes. Verificación hash después de copiar.', 'de': 'Das schnellste Kopier-/Verschiebetool für Windows. 2-3x schneller als Explorer bei großen Dateien. Hash-Verifizierung nach dem Kopieren.', 'ar': 'أسرع أداة نسخ/نقل ملفات لـ Windows. أسرع 2-3 مرات من المستكشف للملفات الكبيرة. تحقق بالتجزئة بعد النسخ.'},
    "Install TreeSize Free": {'en': 'Instant disk space analysis with folder-level breakdown. See exactly how big every folder is, sorted by size. Scan entire drives in seconds using MFT. Export reports, filter by date/size/type. The professional way to manage disk space.', 'fr': 'Analyse d\'espace disque instantanée par dossier. Voyez exactement la taille de chaque dossier, trié par taille. Scan MFT en secondes.', 'tn': 'Analyse espace disque instantanée par dossier. Tchouf exactement qaddech kol dossier, trié par taille. Scan MFT fi thweni.', 'es': 'Análisis de espacio en disco instantáneo por carpeta. Ve exactamente cuánto ocupa cada carpeta, ordenado por tamaño. Escaneo MFT en segundos.', 'de': 'Sofortige Speicherplatzanalyse pro Ordner. Sehen Sie genau wie groß jeder Ordner ist — nach Größe sortiert. MFT-Scan in Sekunden.', 'ar': 'تحليل فوري لمساحة القرص بتفصيل المجلدات. شاهد حجم كل مجلد بالضبط مرتباً بالحجم. فحص MFT في ثوانٍ.'},
    "Install File Converter": {'en': 'Right-click any file to convert it to another format. Images (PNG/JPG/WebP/ICO), documents (PDF/DOCX), audio (MP3/FLAC/WAV), video (MP4/AVI/GIF). Uses FFmpeg and LibreOffice under the hood. The simplest file conversion tool — no websites, no uploads, just right-click.', 'fr': 'Clic-droit pour convertir n\'importe quel fichier. Images, documents, audio, vidéo. Aucun site web, aucun upload — juste clic-droit.', 'tn': 'Clic-droit 3la n\'importe quel fichier bash tconvertih. Images, documents, audio, vidéo. Bla sites web, bla upload — juste clic-droit.', 'es': 'Clic derecho en cualquier archivo para convertirlo. Imágenes, documentos, audio, vídeo. Sin sitios web, sin subidas — solo clic derecho.', 'de': 'Rechtsklick zum Konvertieren jeder Datei. Bilder, Dokumente, Audio, Video. Keine Websites, kein Upload — nur Rechtsklick.', 'ar': 'انقر بزر الماوس الأيمن على أي ملف لتحويله. صور ومستندات وصوت وفيديو. بدون مواقع ولا رفع — فقط نقرة يمنى.'},
    "Install Rainmeter": {'en': 'Desktop customization platform. Display system stats, weather, music player, clocks, RSS feeds — anything — as beautiful widgets on your desktop. Thousands of community skins. Transform your Windows desktop from boring to stunning. The OG desktop rice tool.', 'fr': 'Plateforme de personnalisation bureau. Affichez stats système, météo, musique en widgets. Des milliers de skins communautaires.', 'tn': 'Plateforme personnalisation bureau. Stats système, météo, musique fi widgets jmila. Des milliers de skins communautaires.', 'es': 'Plataforma de personalización de escritorio. Muestra stats del sistema, clima, reproductor como widgets. Miles de skins comunitarios.', 'de': 'Desktop-Anpassungsplattform. Systemstats, Wetter, Musikplayer als schöne Widgets. Tausende Community-Skins.', 'ar': 'منصة تخصيص سطح المكتب. عرض إحصائيات النظام والطقس والموسيقى كأدوات جميلة. آلاف الأشكال من المجتمع.'},
    "Install Git": {'en': 'The world\'s most used version control system. Track every change to your code, collaborate with teams, branch and merge fearlessly. Created by Linus Torvalds. If you write code and don\'t use Git, you\'re living dangerously. Includes Git Bash.', 'fr': 'Le système de contrôle de version le plus utilisé. Suivez chaque modification, collaborez, branches et fusions. Créé par Linus Torvalds.', 'tn': 'A7sen système contrôle de version. Suivez kol modification, collaborez, branches w fusions. Créé par Linus Torvalds.', 'es': 'El sistema de control de versiones más usado. Rastrea cada cambio, colabora, ramifica y fusiona. Creado por Linus Torvalds.', 'de': 'Das weltweit meistgenutzte Versionskontrollsystem. Jede Änderung verfolgen, zusammenarbeiten, verzweigen. Von Linus Torvalds.', 'ar': 'أكثر نظام تحكم بالإصدارات استخداماً. تتبع كل تغيير وتعاون وتفرع بلا خوف. أنشأه لينوس تورفالدز.'},
    "Install Windows Terminal": {'en': 'Microsoft\'s modern terminal app. Tabbed interface for PowerShell, CMD, WSL, SSH — all in one window. GPU-accelerated text rendering, customizable themes, split panes, quake mode dropdown. Makes the old CMD window feel like a relic from 1995.', 'fr': 'Terminal moderne de Microsoft. Onglets pour PowerShell, CMD, WSL, SSH — tout en une fenêtre. Rendu GPU, thèmes personnalisables.', 'tn': 'Terminal moderne ta3 Microsoft. Onglets lel PowerShell, CMD, WSL, SSH — kol fi fenêtre wa7da. Rendu GPU, thèmes personnalisables.', 'es': 'Terminal moderno de Microsoft. Pestañas para PowerShell, CMD, WSL, SSH — todo en una ventana. Renderizado GPU, temas personalizables.', 'de': 'Microsofts modernes Terminal. Tabs für PowerShell, CMD, WSL, SSH — alles in einem Fenster. GPU-Rendering, anpassbare Themes.', 'ar': 'تطبيق طرفية مايكروسوفت الحديث. علامات تبويب لـ PowerShell وCMD وWSL وSSH — الكل في نافذة واحدة. عرض GPU.'},
    "Install PowerShell 7": {'en': 'Cross-platform PowerShell built on .NET. Faster than Windows PowerShell 5.1, supports Linux/macOS, parallel foreach, ternary operators, null-coalescing, pipeline chain operators. The modern shell that makes automation a joy.', 'fr': 'PowerShell multi-plateforme sur .NET. Plus rapide que PowerShell 5.1, supporte Linux/macOS, foreach parallèle, opérateurs modernes.', 'tn': 'PowerShell multi-plateforme 3la .NET. Asra3 mel PowerShell 5.1, supporte Linux/macOS, foreach parallèle.', 'es': 'PowerShell multiplataforma sobre .NET. Más rápido que PowerShell 5.1, soporta Linux/macOS, foreach paralelo, operadores modernos.', 'de': 'Plattformübergreifende PowerShell auf .NET. Schneller als PS 5.1, Linux/macOS-Unterstützung, paralleles ForEach, moderne Operatoren.', 'ar': 'PowerShell متعدد المنصات على .NET. أسرع من PowerShell 5.1 ويدعم Linux/macOS وforeach متوازي وعوامل حديثة.'},
    "Install Postman": {'en': 'The most popular API development and testing platform. Send HTTP requests, inspect responses, automate API testing, mock servers, document APIs. Build collections of requests, chain them with scripts. If you work with APIs, you need Postman.', 'fr': 'Plateforme de développement et test API la plus populaire. Envoyez des requêtes HTTP, inspectez les réponses, automatisez les tests.', 'tn': 'A7sen plateforme développement w test API. Ab3ath requêtes HTTP, inspecte réponses, automatisez tests.', 'es': 'La plataforma de desarrollo y pruebas API más popular. Envía solicitudes HTTP, inspecciona respuestas, automatiza pruebas.', 'de': 'Die beliebteste API-Entwicklungs- und Testplattform. HTTP-Anfragen senden, Antworten inspizieren, API-Tests automatisieren.', 'ar': 'أشهر منصة تطوير واختبار API. أرسل طلبات HTTP وافحص الاستجابات وأتمت الاختبارات.'},
    "Install VLC": {'en': 'The legendary open-source media player that plays EVERYTHING. Any codec, any container, any format — VLC handles it. No codec packs needed, no ads, no tracking. Network streams, disc playback, subtitle support, audio equalization. 4 billion downloads can\'t be wrong.', 'fr': 'Le lecteur multimédia légendaire qui lit TOUT. Aucun codec supplémentaire nécessaire, pas de pubs, pas de tracking.', 'tn': 'Lecteur multimédia légendaire eli ya9ra KOLCHI. Bla codecs supplémentaires, bla pubs, bla tracking. 4 milliards downloads.', 'es': 'El legendario reproductor multimedia que reproduce TODO. Sin codecs adicionales, sin anuncios, sin rastreo. 4 mil millones de descargas.', 'de': 'Der legendäre Open-Source-Mediaplayer der ALLES abspielt. Keine Codec-Packs nötig, keine Werbung, kein Tracking.', 'ar': 'مشغل الوسائط الأسطوري الذي يشغل كل شيء. بدون حزم ترميز إضافية ولا إعلانات ولا تتبع. 4 مليارات تنزيل.'},
    "Install OBS Studio": {'en': 'Free open-source screen recording and live streaming software. Record gameplay, create tutorials, stream to Twitch/YouTube. Scene-based switching, audio mixing, plugins, virtual camera. The professional tool that replaced $500 streaming software.', 'fr': 'Logiciel d\'enregistrement d\'écran et de streaming en direct open-source. Enregistrez le gameplay, créez des tutoriels, diffusez sur Twitch/YouTube.', 'tn': 'Logiciel enregistrement écran w live streaming open-source. Enregistrez gameplay, tutoriels, diffusez 3la Twitch/YouTube.', 'es': 'Software de grabación de pantalla y streaming en vivo open-source. Graba gameplay, crea tutoriales, transmite en Twitch/YouTube.', 'de': 'Open-Source Bildschirmaufnahme und Livestreaming. Gameplay aufnehmen, Tutorials erstellen, auf Twitch/YouTube streamen.', 'ar': 'برنامج تسجيل شاشة وبث مباشر مفتوح المصدر. سجل الألعاب وأنشئ دروساً وابث على Twitch/YouTube.'},
    "Install HandBrake": {'en': 'Open-source video transcoder. Convert any video to MP4/MKV with hardware encoding (NVENC/QSV/VCN). Preset profiles for every device: iPhone, Android, PlayStation, web. Batch convert entire folders. The free alternative to expensive video converters.', 'fr': 'Transcodeur vidéo open-source. Convertissez toute vidéo en MP4/MKV avec encodage matériel. Profils prédéfinis pour chaque appareil.', 'tn': 'Transcodeur vidéo open-source. Convertissez toute vidéo fi MP4/MKV b encodage matériel. Profils prédéfinis lel kol appareil.', 'es': 'Transcodificador de vídeo open-source. Convierte cualquier vídeo a MP4/MKV con codificación hardware. Perfiles para cada dispositivo.', 'de': 'Open-Source Video-Transcoder. Jedes Video zu MP4/MKV mit Hardware-Encoding. Voreinstellungen für jedes Gerät.', 'ar': 'محول فيديو مفتوح المصدر. حوّل أي فيديو إلى MP4/MKV بترميز العتاد. ملفات تعريف لكل جهاز.'},
    "Install Audacity": {'en': 'Free open-source audio editor and recorder. Multi-track editing, noise removal, effects, format conversion. Record from microphone or system audio. Cut, copy, paste, mix audio tracks. The go-to tool for podcasters, musicians, and audio engineers on a budget.', 'fr': 'Éditeur et enregistreur audio open-source gratuit. Édition multi-piste, suppression de bruit, effets, conversion de format.', 'tn': 'Éditeur w enregistreur audio open-source gratuit. Édition multi-piste, suppression bruit, effets, conversion format.', 'es': 'Editor y grabador de audio open-source gratuito. Edición multipista, eliminación de ruido, efectos, conversión de formato.', 'de': 'Kostenloser Open-Source Audio-Editor und -Rekorder. Mehrspureditor, Rauschentfernung, Effekte, Formatkonvertierung.', 'ar': 'محرر ومسجل صوت مجاني مفتوح المصدر. تحرير متعدد المسارات وإزالة الضوضاء والتأثيرات وتحويل التنسيقات.'},
    "Install GIMP": {'en': 'Free open-source image editor — the Photoshop alternative. Layers, masks, curves, filters, plugins. Photo retouching, digital art, graphic design. Supports PSD files. Not as polished as Photoshop, but infinitely cheaper and incredibly capable.', 'fr': 'Éditeur d\'images open-source gratuit — l\'alternative à Photoshop. Calques, masques, courbes, filtres, plugins.', 'tn': 'Éditeur images open-source gratuit — alternative Photoshop. Calques, masques, courbes, filtres, plugins.', 'es': 'Editor de imágenes open-source gratuito — la alternativa a Photoshop. Capas, máscaras, curvas, filtros, plugins.', 'de': 'Kostenloser Open-Source Bildbearbeiter — die Photoshop-Alternative. Ebenen, Masken, Kurven, Filter, Plugins.', 'ar': 'محرر صور مجاني مفتوح المصدر — بديل Photoshop. طبقات وأقنعة ومنحنيات ومرشحات وإضافات.'},
    "Install Obsidian": {'en': 'Knowledge base and note-taking app using local Markdown files. Bi-directional linking, graph view of connections, plugin ecosystem, customizable themes. Your notes are plain text files — you own them forever. The second brain for power users.', 'fr': 'Base de connaissances et prise de notes en Markdown local. Liens bidirectionnels, vue graphe, plugins. Vos notes sont des fichiers texte — vous les possédez.', 'tn': 'Base de connaissances w prise de notes fi Markdown local. Liens bidirectionnels, vue graphe, plugins. Notes ta3ek fichiers texte.', 'es': 'Base de conocimiento y notas en Markdown local. Enlaces bidireccionales, vista de grafo, plugins. Tus notas son archivos de texto — tuyas para siempre.', 'de': 'Wissensbasis und Notizen in lokalen Markdown-Dateien. Bidirektionale Links, Graphansicht, Plugins. Ihre Notizen gehören Ihnen.', 'ar': 'قاعدة معرفة وتدوين ملاحظات بملفات Markdown محلية. روابط ثنائية الاتجاه وعرض رسم بياني وإضافات. ملاحظاتك ملفات نصية — ملكك للأبد.'},
    "Install Joplin": {'en': 'Free open-source note-taking app with end-to-end encryption and cloud sync. Markdown editor, tags, notebooks, web clipper, to-do lists. Sync via Dropbox, OneDrive, Nextcloud, or WebDAV. The privacy-respecting Evernote replacement.', 'fr': 'Prise de notes open-source avec chiffrement de bout en bout et synchronisation cloud. Markdown, tags, cahiers, clipper web.', 'tn': 'Prise de notes open-source b chiffrement bout en bout w sync cloud. Markdown, tags, cahiers, clipper web.', 'es': 'Toma de notas open-source con cifrado de extremo a extremo y sincronización en la nube. Markdown, etiquetas, libretas.', 'de': 'Open-Source Notizen mit Ende-zu-Ende-Verschlüsselung und Cloud-Sync. Markdown, Tags, Notizbücher, Web Clipper.', 'ar': 'تطبيق ملاحظات مفتوح المصدر مع تشفير شامل ومزامنة سحابية. Markdown وعلامات ودفاتر وقاطع ويب.'},
    "Install KDE Connect": {'en': 'Connect your Android/iOS phone to your PC wirelessly. Share clipboard, transfer files, receive notifications on desktop, use phone as trackpad/presentation remote, SMS from PC. The phone-to-PC integration Microsoft should have built into Windows.', 'fr': 'Connectez votre téléphone Android/iOS à votre PC sans fil. Presse-papier partagé, transfert fichiers, notifications sur le bureau.', 'tn': 'Connectez téléphone Android/iOS b PC bla fil. Presse-papier partagé, transfert fichiers, notifications 3al bureau.', 'es': 'Conecta tu teléfono Android/iOS a tu PC sin cables. Portapapeles compartido, transferir archivos, notificaciones en escritorio.', 'de': 'Verbinden Sie Ihr Android/iOS-Telefon drahtlos mit dem PC. Gemeinsame Zwischenablage, Dateitransfer, Desktop-Benachrichtigungen.', 'ar': 'اربط هاتف Android/iOS بالكمبيوتر لاسلكياً. حافظة مشتركة ونقل ملفات وإشعارات على سطح المكتب.'},
    "Install Sumatra PDF": {'en': 'Ultra-lightweight PDF reader. Opens instantly, uses minimal RAM, no bloat. Also reads EPUB, MOBI, XPS, DjVu, CBZ/CBR. The antithesis of Adobe Acrobat — fast, free, portable, does one thing perfectly. 5MB installer vs Acrobat\'s 500MB.', 'fr': 'Lecteur PDF ultra-léger. Ouverture instantanée, RAM minimale, pas de bloat. Lit aussi EPUB, MOBI, XPS, DjVu. L\'antithèse d\'Acrobat.', 'tn': 'Lecteur PDF ultra-léger. Ouverture instantanée, RAM minimale, pas de bloat. Ya9ra EPUB, MOBI, XPS, DjVu zeda.', 'es': 'Lector PDF ultraligero. Abre instantáneamente, usa mínima RAM, sin bloat. También lee EPUB, MOBI, XPS, DjVu.', 'de': 'Ultraleichter PDF-Reader. Öffnet sofort, minimaler RAM, kein Bloat. Liest auch EPUB, MOBI, XPS, DjVu. Die Antithese zu Acrobat.', 'ar': 'قارئ PDF خفيف جداً. يفتح فوراً بأقل ذاكرة وبدون انتفاخ. يقرأ أيضاً EPUB وMOBI وXPS وDjVu. نقيض Acrobat.'},
    "Install Kdenlive": {'en': 'Free open-source video editor with professional features. Multi-track timeline, keyframe animation, effects, transitions, titling, audio mixing. Supports proxy editing for 4K. The best free video editor that isn\'t DaVinci Resolve. KDE project quality.', 'fr': 'Éditeur vidéo open-source gratuit avec fonctions professionnelles. Timeline multi-piste, animations, effets, transitions, titrage.', 'tn': 'Éditeur vidéo open-source gratuit b fonctions professionnelles. Timeline multi-piste, animations, effets, transitions.', 'es': 'Editor de vídeo open-source gratuito con funciones profesionales. Timeline multipista, animaciones, efectos, transiciones.', 'de': 'Kostenloser Open-Source Video-Editor mit Profi-Funktionen. Multi-Track Timeline, Animationen, Effekte, Übergänge, Titel.', 'ar': 'محرر فيديو مجاني مفتوح المصدر بميزات احترافية. خط زمني متعدد المسارات وتأثيرات وانتقالات وعناوين.'},
    "Install WireGuard": {'en': 'Modern VPN protocol — faster, simpler, and more secure than OpenVPN or IPSec. Uses state-of-the-art cryptography (ChaCha20, Curve25519). Minimal attack surface with ~4000 lines of code vs OpenVPN\'s 100,000+. Built into the Linux kernel. The VPN protocol that makes everything else obsolete.', 'fr': 'Protocole VPN moderne — plus rapide, plus simple et plus sûr qu\'OpenVPN ou IPSec. Cryptographie de pointe, surface d\'attaque minimale.', 'tn': 'Protocole VPN moderne — asra3, absaT w aktar sécurité men OpenVPN wela IPSec. Cryptographie de pointe, surface d\'attaque minimale.', 'es': 'Protocolo VPN moderno — más rápido, simple y seguro que OpenVPN o IPSec. Criptografía de última generación, superficie de ataque mínima.', 'de': 'Modernes VPN-Protokoll — schneller, einfacher und sicherer als OpenVPN oder IPSec. Modernste Kryptographie, minimale Angriffsfläche.', 'ar': 'بروتوكول VPN حديث — أسرع وأبسط وأكثر أماناً من OpenVPN أو IPSec. تشفير متطور وسطح هجوم أدنى.'},
    "Install Nmap": {'en': 'The legendary network scanner and security auditor. Discover hosts, open ports, running services, OS detection, vulnerability scripts. Used by sysadmins and pentesters worldwide. The first tool you run when diagnosing network issues or auditing security.', 'fr': 'Le scanner réseau et auditeur de sécurité légendaire. Découvrez les hôtes, ports ouverts, services, détection OS.', 'tn': 'Scanner réseau w auditeur sécurité légendaire. Découvrez les hôtes, ports ouverts, services, détection OS.', 'es': 'El legendario escáner de red y auditor de seguridad. Descubre hosts, puertos abiertos, servicios, detección de SO.', 'de': 'Der legendäre Netzwerkscanner und Sicherheits-Auditor. Hosts, offene Ports, Dienste, OS-Erkennung entdecken.', 'ar': 'ماسح الشبكة ومدقق الأمان الأسطوري. اكتشف المضيفين والمنافذ المفتوحة والخدمات وكشف نظام التشغيل.'},
    "Install HxD": {'en': 'Fast hex editor for raw binary data. Edit files, RAM, and disks at the byte level. Compare files, search patterns, data inspector, checksum calculator. Essential for reverse engineering, forensics, and data recovery. Handles files of any size with instant response.', 'fr': 'Éditeur hexadécimal rapide pour données binaires. Éditez fichiers, RAM et disques au niveau octet. Comparaison, recherche de motifs.', 'tn': 'Éditeur hexadécimal rapide lel données binaires. Éditez fichiers, RAM w disques au niveau octet. Comparaison, recherche motifs.', 'es': 'Editor hexadecimal rápido para datos binarios. Edita archivos, RAM y discos a nivel de byte. Comparación, búsqueda de patrones.', 'de': 'Schneller Hex-Editor für Binärdaten. Dateien, RAM und Festplatten auf Byte-Ebene bearbeiten. Dateivergleich, Mustersuche.', 'ar': 'محرر ست عشري سريع للبيانات الثنائية. حرر الملفات والذاكرة والأقراص على مستوى البايت. مقارنة وبحث أنماط.'},
    "Install MediaInfo": {'en': 'Detailed technical metadata viewer for audio/video files. Codec, bitrate, resolution, frame rate, audio channels, HDR info, subtitle tracks — every technical detail in one click. Essential for media professionals to verify encoding quality and compatibility.', 'fr': 'Visionneuse de métadonnées techniques détaillées pour fichiers audio/vidéo. Codec, débit, résolution, fréquence d\'image — chaque détail technique.', 'tn': 'Visionneuse métadonnées techniques détaillées lel fichiers audio/vidéo. Codec, débit, résolution — kol détail technique fi click.', 'es': 'Visor detallado de metadatos técnicos para audio/vídeo. Codec, bitrate, resolución, fps — cada detalle técnico en un clic.', 'de': 'Detaillierter technischer Metadaten-Viewer für Audio/Video. Codec, Bitrate, Auflösung, Framerate — jedes technische Detail.', 'ar': 'عارض بيانات وصفية تقنية مفصلة لملفات الصوت/الفيديو. الترميز والمعدل والدقة — كل تفصيل تقني بنقرة.'},
    "Install WinSCP": {'en': 'Free SFTP, SCP, FTP, and S3 client for Windows. Drag-and-drop file transfer to remote servers with two-panel interface. Scripting, synchronization, PuTTY integration. The standard tool for securely moving files to/from Linux servers.', 'fr': 'Client SFTP, SCP, FTP et S3 gratuit pour Windows. Transfert de fichiers par glisser-déposer vers serveurs distants. Interface deux panneaux.', 'tn': 'Client SFTP, SCP, FTP w S3 gratuit lel Windows. Transfert fichiers b glisser-déposer vers serveurs distants. Interface deux panneaux.', 'es': 'Cliente SFTP, SCP, FTP y S3 gratuito para Windows. Transferencia de archivos arrastrando a servidores remotos. Interfaz de dos paneles.', 'de': 'Kostenloser SFTP-, SCP-, FTP- und S3-Client für Windows. Drag-and-Drop-Dateitransfer zu Remote-Servern mit Zwei-Panel-Interface.', 'ar': 'عميل SFTP وSCP وFTP وS3 مجاني لـ Windows. نقل ملفات بالسحب والإفلات إلى خوادم بعيدة بواجهة لوحتين.'},
    "Install PuTTY": {'en': 'The classic SSH and Telnet client for Windows. Terminal emulator with serial port support, key generation (PuTTYgen), SCP transfer (PSCP), SSH tunneling. Still the most widely used SSH client on Windows after 25+ years. Lightweight and reliable.', 'fr': 'Le client SSH et Telnet classique pour Windows. Émulateur de terminal avec support port série, génération de clés, tunneling SSH.', 'tn': 'Client SSH w Telnet classique lel Windows. Émulateur terminal b support port série, génération clés, tunneling SSH.', 'es': 'El cliente SSH y Telnet clásico para Windows. Emulador de terminal con soporte de puerto serie, generación de claves, túneles SSH.', 'de': 'Der klassische SSH- und Telnet-Client für Windows. Terminalemulator mit serieller Schnittstelle, Schlüsselgenerierung, SSH-Tunneling.', 'ar': 'عميل SSH وTelnet الكلاسيكي لـ Windows. محاكي طرفية مع دعم المنفذ التسلسلي وتوليد المفاتيح والأنفاق.'},
    "Install Clink": {'en': 'Supercharges the Windows CMD prompt with bash-style features. Tab completion, history search (Ctrl+R), syntax highlighting, scriptable prompts, persistent history. Makes CMD actually usable without switching to PowerShell. Drop-in enhancement, no config needed.', 'fr': 'Améliore CMD avec des fonctions bash. Complétion par tabulation, recherche d\'historique, coloration syntaxique, historique persistant.', 'tn': 'Ya7ssin CMD b fonctions bash. Tab completion, recherche historique (Ctrl+R), coloration syntaxique, historique persistant.', 'es': 'Mejora CMD con funciones bash. Completado con Tab, búsqueda de historial, resaltado de sintaxis, historial persistente.', 'de': 'Verbessert CMD mit Bash-Funktionen. Tab-Vervollständigung, Verlaufssuche, Syntaxhervorhebung, persistenter Verlauf.', 'ar': 'يعزز CMD بميزات bash. إكمال بالتبويب وبحث في السجل وتلوين بناء الجملة وسجل دائم.'},
    "Install ImageGlass": {'en': 'Modern lightweight image viewer that replaces Windows Photo Viewer. Supports 80+ formats including WebP, SVG, RAW, PSD, HEIC. Instant loading, touch-friendly, color management, slideshow. Beautiful UI with dark mode. The image viewer Windows deserves.', 'fr': 'Visionneuse d\'images légère et moderne. Supporte 80+ formats dont WebP, SVG, RAW, PSD. Chargement instantané, mode sombre.', 'tn': 'Visionneuse images légère w moderne. Supporte 80+ formats dont WebP, SVG, RAW, PSD. Chargement instantané, mode sombre.', 'es': 'Visor de imágenes ligero y moderno. Soporta 80+ formatos incluyendo WebP, SVG, RAW, PSD. Carga instantánea, modo oscuro.', 'de': 'Moderner leichter Bildbetrachter. Unterstützt 80+ Formate inkl. WebP, SVG, RAW, PSD. Sofortiges Laden, Dunkelmodus.', 'ar': 'عارض صور حديث وخفيف. يدعم 80+ تنسيقاً بما فيها WebP وSVG وRAW وPSD. تحميل فوري ووضع مظلم.'},
    "Install foobar2000": {'en': 'Audiophile-grade music player with extreme customizability. Bit-perfect playback, ReplayGain, gapless playback, advanced tagging, format conversion, DSP effects. Supports FLAC, APE, WavPack, Opus, every format. Uses 5MB RAM. The music player for people who care about sound quality.', 'fr': 'Lecteur musique audiophile ultra-personnalisable. Lecture bit-perfect, ReplayGain, gapless, conversion de format. Supporte tous les formats.', 'tn': 'Lecteur musique audiophile ultra-personnalisable. Lecture bit-perfect, ReplayGain, gapless. Supporte kol les formats. 5MB RAM.', 'es': 'Reproductor de música audiófilo ultra-personalizable. Reproducción bit-perfect, ReplayGain, gapless. Soporta todos los formatos.', 'de': 'Audiophiler Musikplayer mit extremer Anpassbarkeit. Bit-perfekte Wiedergabe, ReplayGain, lückenlos. Alle Formate. 5MB RAM.', 'ar': 'مشغل موسيقى لعشاق الصوت قابل للتخصيص بالكامل. تشغيل مثالي وReplayGain وبدون فجوات. يدعم كل التنسيقات.'},
    "Install MPC-HC": {'en': 'Ultra-lightweight media player with built-in codecs. Plays everything with zero bloat — 15MB total. Hardware-accelerated decoding, subtitle support, custom shaders. The spiritual successor to Windows Media Player Classic. Fast, clean, no telemetry.', 'fr': 'Lecteur multimédia ultra-léger avec codecs intégrés. Lit tout sans bloat — 15MB total. Décodage accéléré matériel, sous-titres.', 'tn': 'Lecteur multimédia ultra-léger b codecs intégrés. Ya9ra kolchi bla bloat — 15MB total. Décodage accéléré matériel.', 'es': 'Reproductor multimedia ultraligero con codecs integrados. Reproduce todo sin bloat — 15MB total. Decodificación por hardware.', 'de': 'Ultraleichter Mediaplayer mit eingebauten Codecs. Spielt alles ohne Bloat — 15MB. Hardware-beschleunigte Dekodierung.', 'ar': 'مشغل وسائط خفيف جداً بترميزات مدمجة. يشغل كل شيء بدون انتفاخ — 15 ميغابايت. فك ترميز بتسريع العتاد.'},
    "Install yt-dlp": {'en': 'Command-line tool to download videos from YouTube and 1000+ sites. Supports playlists, chapters, subtitles, metadata, sponsorblock integration. Download in any quality/format. The actively maintained youtube-dl fork that actually works in 2024+.', 'fr': 'Outil en ligne de commande pour télécharger des vidéos de YouTube et 1000+ sites. Playlists, chapitres, sous-titres, qualité au choix.', 'tn': 'Outil ligne de commande bash tna99as vidéos men YouTube w 1000+ sites. Playlists, chapitres, sous-titres, qualité au choix.', 'es': 'Herramienta de línea de comandos para descargar vídeos de YouTube y 1000+ sitios. Playlists, capítulos, subtítulos, calidad a elegir.', 'de': 'Kommandozeilen-Tool zum Download von YouTube und 1000+ Seiten. Playlists, Kapitel, Untertitel, beliebige Qualität/Format.', 'ar': 'أداة سطر أوامر لتنزيل فيديوهات من YouTube و1000+ موقع. قوائم تشغيل وفصول وترجمات وجودة حسب الاختيار.'},
    "Install MKVToolNix": {'en': 'Swiss Army knife for MKV files. Merge, split, edit, inspect Matroska containers. Add/remove audio tracks, subtitles, chapters without re-encoding. Lossless MKV manipulation. Essential for anyone who works with video files — no quality loss, instant processing.', 'fr': 'Couteau suisse pour fichiers MKV. Fusionnez, divisez, éditez les conteneurs Matroska. Ajoutez/supprimez pistes audio, sous-titres sans réencodage.', 'tn': 'Couteau suisse lel fichiers MKV. Fusionnez, divisez, éditez conteneurs Matroska. Zid/na77i pistes audio, sous-titres bla réencodage.', 'es': 'Navaja suiza para archivos MKV. Fusiona, divide, edita contenedores Matroska. Añade/elimina pistas de audio, subtítulos sin recodificar.', 'de': 'Schweizer Taschenmesser für MKV-Dateien. Zusammenführen, teilen, bearbeiten von Matroska-Containern. Audio/Untertitel ohne Neukodierung.', 'ar': 'سكين سويسرية لملفات MKV. ادمج وقسّم وحرر حاويات Matroska. أضف/أزل مسارات صوت وترجمات بدون إعادة ترميز.'},
    "Install qBittorrent": {'en': 'Free open-source BitTorrent client — the uTorrent replacement without ads or crypto miners. Sequential downloading, RSS feed, torrent search, IP filtering, bandwidth scheduler. Clean interface with no bundled crapware. The torrent client that respects you.', 'fr': 'Client BitTorrent open-source gratuit — le remplacement d\'uTorrent sans pubs ni miners. Téléchargement séquentiel, flux RSS, recherche.', 'tn': 'Client BitTorrent open-source gratuit — remplacement uTorrent bla pubs wela miners. Téléchargement séquentiel, RSS, recherche.', 'es': 'Cliente BitTorrent open-source gratuito — reemplazo de uTorrent sin anuncios ni miners. Descarga secuencial, RSS, búsqueda.', 'de': 'Kostenloser Open-Source BitTorrent-Client — uTorrent-Ersatz ohne Werbung oder Miner. Sequentieller Download, RSS, Suche.', 'ar': 'عميل BitTorrent مجاني مفتوح المصدر — بديل uTorrent بدون إعلانات أو تعدين. تنزيل تسلسلي وRSS وبحث.'},
    "Install Paint.NET": {'en': 'Powerful yet simple image editor for Windows. Layers, effects, plugins, selection tools, magic wand, unlimited undo. More capable than MS Paint, simpler than GIMP/Photoshop. GPU-accelerated rendering. The sweet spot between simplicity and power for photo editing.', 'fr': 'Éditeur d\'images puissant mais simple. Calques, effets, plugins, outils de sélection. Plus capable que Paint, plus simple que GIMP.', 'tn': 'Éditeur images puissant mais simple. Calques, effets, plugins, outils sélection. Aktar capable men Paint, absaT men GIMP.', 'es': 'Editor de imágenes potente pero simple. Capas, efectos, plugins, herramientas de selección. Más capaz que Paint, más simple que GIMP.', 'de': 'Leistungsstarker aber einfacher Bildeditor. Ebenen, Effekte, Plugins, Auswahlwerkzeuge. Leistungsfähiger als Paint, einfacher als GIMP.', 'ar': 'محرر صور قوي وبسيط. طبقات وتأثيرات وإضافات وأدوات تحديد. أقوى من Paint وأبسط من GIMP.'},
    "Install Double Commander": {'en': 'Free dual-pane file manager inspired by Total Commander. Tabbed interface, built-in text editor, archive handling, FTP client, file comparison, multi-rename tool. Keyboard-driven with customizable shortcuts. The power user file manager that makes Explorer look like a toy.', 'fr': 'Gestionnaire de fichiers à double panneau gratuit inspiré de Total Commander. Onglets, éditeur texte intégré, gestion d\'archives, FTP.', 'tn': 'Gestionnaire fichiers double panneau gratuit inspiré de Total Commander. Onglets, éditeur texte, archives, FTP.', 'es': 'Gestor de archivos de doble panel gratuito inspirado en Total Commander. Pestañas, editor de texto, archivos, FTP.', 'de': 'Kostenloser Zwei-Panel-Dateimanager inspiriert von Total Commander. Tabs, integrierter Texteditor, Archive, FTP.', 'ar': 'مدير ملفات ثنائي اللوحة مجاني مستوحى من Total Commander. علامات تبويب ومحرر نصوص ومعالجة أرشيف وFTP.'},
    "Disable Paging Executive (Lock Kernel in RAM)": {'en': 'Forces the Windows kernel and drivers to stay in physical RAM instead of being paged to disk. Reduces latency spikes on systems with 16GB+ RAM.', 'fr': 'Force le noyau et les pilotes à rester en RAM physique. Réduit les pics de latence sur les systèmes avec 16Go+ de RAM.', 'tn': 'Yforci kernel w drivers yab9aw fil RAM physique. Ynaqi latence spikes 3la systems b 16Go+.', 'es': 'Fuerza al kernel y drivers a permanecer en RAM física. Reduce picos de latencia en sistemas con 16GB+.', 'de': 'Zwingt Kernel und Treiber im physischen RAM zu bleiben. Reduziert Latenzspitzen bei 16GB+ RAM.', 'ar': 'يجبر النواة والتعريفات على البقاء في الذاكرة الفعلية. يقلل قفزات التأخير على أنظمة 16 جيجا+.'},
    "Disable NTFS Encryption Service (EFS)": {'en': 'Stops the Encrypting File System service. If you don\'t use EFS-encrypted folders, this saves a background service and avoids rare permission issues.', 'fr': 'Arrête le service EFS. Si vous n\'utilisez pas le chiffrement EFS, économise un service en arrière-plan.', 'tn': 'Ytaffi service EFS. Ken ma testa3melch dossiers EFS, ywaffir service en arrière-plan.', 'es': 'Detiene el servicio EFS. Si no usas carpetas cifradas EFS, ahorra un servicio en segundo plano.', 'de': 'Stoppt den EFS-Dienst. Wenn Sie keine EFS-verschlüsselten Ordner verwenden, spart das einen Hintergrunddienst.', 'ar': 'يوقف خدمة تشفير EFS. إذا لا تستخدم مجلدات مشفرة EFS، يوفر خدمة خلفية.'},
    "Increase NTFS Memory Usage (Large System Cache)": {'en': 'Tells NTFS to use more RAM for file system caching. Improves file I/O performance on systems with 16GB+ RAM. The server-tuning trick applied to desktop.', 'fr': 'Dit à NTFS d\'utiliser plus de RAM pour le cache système. Améliore les performances I/O sur systèmes avec 16Go+.', 'tn': 'Y9ol lel NTFS yesta3mel aktar RAM lel cache système. Ya7sin I/O 3la systèmes b 16Go+.', 'es': 'Indica a NTFS usar más RAM para caché del sistema. Mejora el rendimiento I/O en sistemas con 16GB+.', 'de': 'Weist NTFS an mehr RAM für Dateisystem-Cache zu nutzen. Verbessert I/O bei 16GB+ RAM.', 'ar': 'يخبر NTFS باستخدام مزيد من الذاكرة للتخزين المؤقت. يحسن أداء الإدخال/الإخراج على أنظمة 16 جيجا+.'},
    "Disable Desktop Window Manager Throttling": {'en': 'Sets DWM max frame latency to 1 frame. Reduces compositor buffering for lower display latency in windowed/borderless games.', 'fr': 'Définit la latence max DWM à 1 frame. Réduit le buffering du compositeur pour moins de latence d\'affichage.', 'tn': 'Y7ot DWM max frame latency 3la 1 frame. Ynaqi latence affichage fil windowed/borderless.', 'es': 'Establece la latencia máxima DWM a 1 frame. Reduce el buffering del compositor para menor latencia de pantalla.', 'de': 'Setzt DWM-Max-Frame-Latenz auf 1 Frame. Reduziert Compositor-Pufferung für niedrigere Anzeigelatenz.', 'ar': 'يعيّن أقصى تأخير إطار DWM إلى إطار واحد. يقلل التخزين المؤقت للعرض.'},
    "Disable Cursor Shadow & Smooth Scrolling": {'en': 'Removes the cursor drop shadow and smooth scroll animations. Tiny GPU driver overhead savings — mostly placebo but satisfying for purists.', 'fr': 'Supprime l\'ombre du curseur et le défilement fluide. Économie GPU minimale mais satisfaisante pour les puristes.', 'tn': 'Ynahi cursor shadow w smooth scrolling. GPU overhead zghir — satisfaisant lel puristes.', 'es': 'Elimina la sombra del cursor y las animaciones de desplazamiento suave. Ahorro mínimo de GPU pero satisfactorio para puristas.', 'de': 'Entfernt Cursor-Schatten und sanftes Scrollen. Minimale GPU-Einsparung — zufriedenstellend für Puristen.', 'ar': 'يزيل ظل المؤشر والتمرير السلس. توفير طفيف في GPU — مُرضٍ للمتشددين.'},
    "Disable Network Auto-Tuning Heuristics": {'en': 'Prevents Windows from dynamically shrinking the TCP receive window based on its own heuristics. Keeps the auto-tuning level at normal without interference.', 'fr': 'Empêche Windows de réduire dynamiquement la fenêtre TCP. Garde l\'auto-tuning à normal sans interférence.', 'tn': 'Ymanea Windows men yna99as TCP receive window dynamiquement. Ykhalli auto-tuning normal bla interférence.', 'es': 'Evita que Windows reduzca dinámicamente la ventana TCP. Mantiene el auto-ajuste en normal sin interferencia.', 'de': 'Verhindert dynamisches Verkleinern des TCP-Empfangsfensters. Hält Auto-Tuning auf Normal ohne Eingriffe.', 'ar': 'يمنع Windows من تقليص نافذة استقبال TCP ديناميكياً. يبقي الضبط التلقائي عادياً بدون تدخل.'},
    "Disable NLA Probing (Network Location Awareness)": {'en': 'Stops Windows from periodically pinging Microsoft servers (msftconnecttest.com) to check internet connectivity. Reduces background traffic and DNS queries.', 'fr': 'Empêche Windows de pinger les serveurs Microsoft pour vérifier la connectivité. Réduit le trafic en arrière-plan.', 'tn': 'Ymanea Windows men yping serveurs Microsoft bash ychecky internet. Ynaqi trafic background w DNS.', 'es': 'Evita que Windows haga ping a servidores Microsoft para verificar conectividad. Reduce tráfico y consultas DNS.', 'de': 'Verhindert regelmäßige Pings an Microsoft-Server zur Konnektivitätsprüfung. Reduziert Hintergrundtraffic.', 'ar': 'يمنع Windows من إرسال نبضات لخوادم Microsoft للتحقق من الاتصال. يقلل حركة البيانات الخلفية.'},
    "Disable Processor Performance Autonomous Mode": {'en': 'Forces the OS to control CPU P-states instead of letting the processor firmware decide autonomously. Gives Windows full control over frequency scaling.', 'fr': 'Force l\'OS à contrôler les P-states CPU au lieu du firmware. Donne à Windows le contrôle total de la fréquence.', 'tn': 'Yforci OS ycontrola CPU P-states bla firmware. Ya3ti Windows contrôle complet 3la fréquence.', 'es': 'Fuerza al OS a controlar P-states de CPU en vez del firmware. Da a Windows control total de frecuencia.', 'de': 'Zwingt das OS CPU P-States zu kontrollieren statt die Firmware. Gibt Windows volle Frequenzkontrolle.', 'ar': 'يجبر النظام على التحكم في حالات P للمعالج بدلاً من البرنامج الثابت. يمنح Windows تحكماً كاملاً بالتردد.'},
    "Disable CPU Idle Scaling (Processor Idle Disable)": {'en': 'Prevents the CPU from entering low-power idle states during brief inactivity — cores stay at full speed. Measurably reduces wake-up latency for real-time tasks.', 'fr': 'Empêche le CPU d\'entrer en états de repos basse consommation. Les cœurs restent à pleine vitesse. Réduit la latence de réveil.', 'tn': 'Ymanea CPU men ydkhol fi idle states. Cores yab9aw 3la full speed. Ynaqi latence wake-up.', 'es': 'Evita que la CPU entre en estados de inactividad de bajo consumo. Los núcleos se mantienen a máxima velocidad.', 'de': 'Verhindert CPU-Leerlaufzustände — Kerne bleiben auf voller Geschwindigkeit. Reduziert Aufwachlatenz messbar.', 'ar': 'يمنع المعالج من دخول حالات الخمول — تبقى الأنوية بأقصى سرعة. يقلل تأخير الاستيقاظ.'},
    "Disable Pointer Precision Enhancement": {'en': 'Fully disables Windows mouse acceleration. Sets flat 1:1 scaling so physical movement matches cursor movement exactly. Essential for FPS gamers.', 'fr': 'Désactive complètement l\'accélération de la souris. Mouvement physique = mouvement curseur. Essentiel pour les joueurs FPS.', 'tn': 'Ytaffi mouse acceleration kamla. Mouvement physique = mouvement curseur. Essentiel lel joueurs FPS.', 'es': 'Desactiva completamente la aceleración del ratón. Movimiento físico = movimiento del cursor. Esencial para jugadores FPS.', 'de': 'Deaktiviert Mausbeschleunigung vollständig. 1:1-Skalierung — physische Bewegung = Cursorbewegung. Essentiell für FPS-Spieler.', 'ar': 'يعطل تسارع الماوس بالكامل. تحجيم 1:1 — الحركة الفعلية = حركة المؤشر. ضروري للاعبي FPS.'},
    "Set USB Mouse Polling Override (1000Hz)": {'en': 'Optimizes USB mouse driver parameters for lowest latency. Sets mouse data queue to 16 (smallest safe value) and forces the MS HID mouse driver for consistency.', 'fr': 'Optimise les paramètres du pilote souris USB pour la latence minimale. File d\'attente données souris à 16.', 'tn': 'Ya7sin paramètres pilote souris USB lel latence minimale. Mouse data queue 3la 16.', 'es': 'Optimiza parámetros del driver del ratón USB para mínima latencia. Cola de datos del ratón a 16.', 'de': 'Optimiert USB-Maustreiber-Parameter für niedrigste Latenz. Maus-Datenwarteschlange auf 16.', 'ar': 'يحسّن معلمات تعريف الماوس USB لأقل تأخير. يضبط طابور بيانات الماوس على 16.'},
    "Disable Customer Experience Improvement Program (CEIP)": {'en': 'Disables the application CEIP data collection across Windows and Office. Stops background SQM data uploads that waste bandwidth and CPU.', 'fr': 'Désactive la collecte de données CEIP dans Windows et Office. Arrête les uploads SQM en arrière-plan.', 'tn': 'Ytaffi collecte données CEIP fil Windows w Office. Ytaffi uploads SQM fi background.', 'es': 'Desactiva la recopilación de datos CEIP en Windows y Office. Detiene subidas SQM en segundo plano.', 'de': 'Deaktiviert CEIP-Datensammlung in Windows und Office. Stoppt SQM-Hintergrund-Uploads.', 'ar': 'يعطل جمع بيانات CEIP في Windows وOffice. يوقف رفع بيانات SQM في الخلفية.'},
    "Disable Application Impact Telemetry (AIT)": {'en': 'Stops Windows from tracking which apps you launch, how often, and for how long. Removes a hidden performance monitoring layer that runs on every process start.', 'fr': 'Empêche Windows de suivre quelles apps vous lancez et combien de temps. Supprime une couche de surveillance cachée.', 'tn': 'Ymanea Windows men ytracker quel applis testa3melhom w qaddech de temps. Ynahi couche surveillance cachée.', 'es': 'Evita que Windows rastree qué apps abres, con qué frecuencia y cuánto tiempo. Elimina capa de monitoreo oculta.', 'de': 'Verhindert App-Startverfolgung — welche Apps, wie oft, wie lange. Entfernt versteckte Überwachungsschicht.', 'ar': 'يمنع Windows من تتبع التطبيقات المفتوحة ومدة استخدامها. يزيل طبقة مراقبة مخفية.'},
    "Disable Taskbar Search Box & Highlights": {'en': 'Removes the Bing search box and trending search highlights from the taskbar. Reclaim space and stop accidental web searches from Start menu.', 'fr': 'Supprime la boîte de recherche Bing et les highlights de la barre des tâches. Récupérez de l\'espace.', 'tn': 'Ynahi search box Bing w highlights mel taskbar. Récupérez espace w twaqqaf recherches web accidentelles.', 'es': 'Elimina el cuadro de búsqueda Bing y los destacados de la barra de tareas. Recupera espacio y evita búsquedas web accidentales.', 'de': 'Entfernt Bing-Suchfeld und Trending-Highlights aus der Taskleiste. Platz zurückgewinnen.', 'ar': 'يزيل مربع بحث Bing والاتجاهات من شريط المهام. استعد المساحة وأوقف البحث العرضي.'},
    "Disable News & Interests Widget": {'en': 'Kills the Windows 10/11 news widget that wastes RAM, CPU, and bandwidth loading MSN content. Removes it from taskbar completely.', 'fr': 'Supprime le widget d\'actualités Windows qui gaspille RAM, CPU et bande passante. Le retire complètement de la barre des tâches.', 'tn': 'Ytaffi widget actualités Windows eli ykassr RAM, CPU w bandwidth. Ynah7ih mel taskbar kamla.', 'es': 'Elimina el widget de noticias que desperdicia RAM, CPU y ancho de banda. Lo quita completamente de la barra de tareas.', 'de': 'Entfernt das Nachrichten-Widget das RAM, CPU und Bandbreite verschwendet. Vollständig aus Taskleiste entfernen.', 'ar': 'يزيل أداة الأخبار التي تهدر الذاكرة والمعالج وعرض النطاق. يزيلها من شريط المهام بالكامل.'},
}

_current_lang = "en"

def _t(key, **kwargs):
    """Translate a UI string key to the current language."""
    entry = TRANSLATIONS.get(key, {})
    text = entry.get(_current_lang, entry.get("en", key))
    if kwargs:
        text = text.format(**kwargs)
    return text

def _tn(tweak_name):
    """Translate a tweak internal name to the current display language."""
    entry = TWEAK_NAMES.get(tweak_name, {})
    return entry.get(_current_lang, tweak_name)

def _cat(cat_key):
    """Translate a category name."""
    entry = CAT_NAMES.get(cat_key, {})
    return entry.get(_current_lang, cat_key)

def _risk_text(risk_tuple):
    """Get translated risk level text."""
    risk_map = {"SAFE": "risk_safe", "LOW": "risk_low", "MEDIUM": "risk_medium", "HIGH": "risk_high"}
    key = risk_map.get(risk_tuple[0], "")
    return f"[{_t(key)}]" if key else "[-]"


def _td(tweak_name):
    """Get translated description for a tweak."""
    entry = TWEAK_DESCS.get(tweak_name, {})
    return entry.get(_current_lang, entry.get("en", ""))



# ═════════════════════ All categories and tweaks ══════════════════════
CATEGORIES = {
    "System  Core": {
        "icon": "\u2699",
        "tweaks": [
            {
                "name": "Disable All Background UWP Apps",
                "desc": "Prevents modern Windows apps (UWP) from running in the background while you game. Frees up memory and CPU cycles.",
                "risk": MEDIUM,
                "cmds": [
                    'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\BackgroundAccessApplications" /v "GlobalUserDisabled" /t REG_DWORD /d 1 /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppPrivacy" /v "LetAppsRunInBackground" /t REG_DWORD /d 2 /f'
                ]
            },
            {
                "name": "Disable VBS / HVCI / Core Isolation",
                "reverse": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\DeviceGuard" /v "EnableVirtualizationBasedSecurity" /t REG_DWORD /d 1 /f',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\DeviceGuard" /v "RequirePlatformSecurityFeatures" /t REG_DWORD /d 1 /f',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\DeviceGuard\\Scenarios\\HypervisorEnforcedCodeIntegrity" /v "Enabled" /t REG_DWORD /d 1 /f',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\DeviceGuard\\Scenarios\\CredentialGuard" /v "Enabled" /t REG_DWORD /d 1 /f',
                    'bcdedit /set hypervisorlaunchtype auto',
                ],
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
                "reverse": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v "FeatureSettingsOverride" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v "FeatureSettingsOverrideMask" /t REG_DWORD /d 3 /f',
                ],
                "desc": "Removes CPU vulnerability patches that add 2-8% overhead to every syscall and context switch. Biggest impact on I/O-heavy workloads.",
                "risk": HIGH,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v "FeatureSettingsOverride" /t REG_DWORD /d 3 /f',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v "FeatureSettingsOverrideMask" /t REG_DWORD /d 3 /f',
                ],
            },
            {
                "name": "Elevate CSRSS & DWM Priority",
                "reverse": [
                    'reg delete "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\csrss.exe\\PerfOptions" /f',
                    'reg delete "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\dwm.exe\\PerfOptions" /f',
                ],
                "desc": "Gives csrss.exe and dwm.exe High CPU priority (class 3) and High I/O priority so mouse input and frame flips never wait behind game threads.",
                "risk": LOW,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\csrss.exe\\PerfOptions" /v "CpuPriorityClass" /t REG_DWORD /d 3 /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\csrss.exe\\PerfOptions" /v "IoPriority" /t REG_DWORD /d 3 /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\dwm.exe\\PerfOptions" /v "CpuPriorityClass" /t REG_DWORD /d 3 /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\dwm.exe\\PerfOptions" /v "IoPriority" /t REG_DWORD /d 3 /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\dwm.exe\\PerfOptions" /v "PagePriority" /t REG_DWORD /d 5 /f',
                ],
            },
            {
                "name": "Disable Page Combining (Memory Dedup)",
                "reverse": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v "DisablePageCombining" /t REG_DWORD /d 0 /f',
                ],
                "desc": "Stops the background RAM scanner that searches for identical pages. Saves constant CPU cycles; uses slightly more RAM.",
                "risk": LOW,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v "DisablePageCombining" /t REG_DWORD /d 1 /f',
                ],
            },
            {
                "name": "Lock Kernel & Drivers in RAM",
                "reverse": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v "DisablePagingExecutive" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v "LargeSystemCache" /t REG_DWORD /d 0 /f',
                ],
                "desc": "Sets DisablePagingExecutive=1 so the NT kernel and core drivers never get paged to disk. Eliminates micro-stutters from kernel page faults. Needs 8GB+ RAM.",
                "risk": LOW,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v "DisablePagingExecutive" /t REG_DWORD /d 1 /f',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v "LargeSystemCache" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Optimize Win32 CPU Scheduling",
                "reverse": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl" /v "Win32PrioritySeparation" /t REG_DWORD /d 2 /f',
                ],
                "desc": "Sets Win32PrioritySeparation to 0x26: short, variable quantum with 3:1 foreground boost. Your active window gets triple the CPU time of background apps.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl" /v "Win32PrioritySeparation" /t REG_DWORD /d 38 /f',
                ],
            },
            {
                "name": "Disable CFG (Control Flow Guard)",
                "reverse": ["powershell -Command \"Set-ProcessMitigation -System -Enable CFG\""],
                "desc": "Disables Control Flow Guard (CFG) system-wide. Removes overhead from every function call in protected processes. Note: CET (Shadow Stack) is a separate setting. 1-3% gain in CPU-heavy DX11 titles.",
                "risk": MEDIUM,
                "cmds": [
                    'powershell -Command "Set-ProcessMitigation -System -Disable CFG"',
                ],
            },
            {
                "name": "Disable Memory Compression",
                "reverse": [
                    'powershell -NoProfile -Command "Enable-MMAgent -MemoryCompression"',
                ],
                "desc": "Stops Windows from compressing RAM. Reduces CPU overhead and latency when accessing memory, at the cost of slightly higher RAM usage.",
                "risk": LOW,
                "cmds": [
                    'powershell -NoProfile -Command "Disable-MMAgent -MemoryCompression"',
                ],
            },
            {
                "name": "Disable Fault Tolerant Heap (FTH)",
                "reverse": [
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\FTH" /v "Enabled" /t REG_DWORD /d 1 /f',
                ],
                "desc": "FTH monitors app crashes and applies mitigations that can severely degrade performance of games that crash occasionally.",
                "risk": LOW,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\FTH" /v "Enabled" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Disable UAC (User Account Control)",
                "reverse": [
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "EnableLUA" /t REG_DWORD /d 1 /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "ConsentPromptBehaviorAdmin" /t REG_DWORD /d 5 /f',
                ],
                "desc": "Completely disables UAC prompts and virtualization. WARNING: Breaks ALL Microsoft Store/UWP apps and may cause boot loops on Win11. Reboot required.",
                "risk": HIGH,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "EnableLUA" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "ConsentPromptBehaviorAdmin" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Disable DEP (Data Execution Prevention)",
                "reverse": ["bcdedit /set nx OptIn"],
                "desc": "Disables DEP globally. Removes hardware-level memory execution checks. Extreme security risk, but removes a layer of memory validation.",
                "risk": HIGH,
                "cmds": [
                    'bcdedit /set nx AlwaysOff',
                ],
            },
            {
                "name": "Disable ASLR (Address Space Layout Randomization)",
                "reverse": [
                    'reg delete "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v "MoveImages" /f',
                ],
                "desc": "Forces memory to load at predictable addresses. Can slightly improve load times and CPU cache hits. Extreme security risk.",
                "risk": HIGH,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v "MoveImages" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Disable System Restore",
                "reverse": [
                    "powershell -NoProfile -Command \"Enable-ComputerRestore -Drive 'C:\\\\'\"",
                    'reg delete "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows NT\\SystemRestore" /v "DisableSR" /f',
                ],
                "desc": "Turns off System Restore entirely. Frees up disk space and removes background snapshotting I/O.",
                "risk": HIGH,
                "cmds": [
                    'powershell -NoProfile -Command "Disable-ComputerRestore -Drive \'C:\\\'"',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows NT\\SystemRestore" /v "DisableSR" /t REG_DWORD /d 1 /f',
                ],
            },
            {
                "name": "Disable SEHOP (Exception Chain Validation)",
                "reverse": [
                    'reg delete "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\kernel" /v "DisableExceptionChainValidation" /f',
                ],
                "desc": "Disables Structured Exception Handling Overwrite Protection. Removes a security check on every exception thrown by applications. Good for raw performance.",
                "risk": HIGH,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\kernel" /v "DisableExceptionChainValidation" /t REG_DWORD /d 1 /f',
                ],
            },
            {
                "name": "Disable Prefetcher & Superfetch (Registry)",
                "reverse": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\\PrefetchParameters" /v "EnablePrefetcher" /t REG_DWORD /d 3 /f',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\\PrefetchParameters" /v "EnableSuperfetch" /t REG_DWORD /d 3 /f',
                ],
                "desc": "Hard-disables the memory prefetcher at the kernel level. Essential for SSDs to prevent unnecessary write cycles and CPU overhead.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\\PrefetchParameters" /v "EnablePrefetcher" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\\PrefetchParameters" /v "EnableSuperfetch" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Disable Kernel Mitigations (KVA Shadow)",
                "desc": "Disables Kernel Virtual Address shadowing (Meltdown fix). Eliminates 5-30% syscall overhead on Intel CPUs. EXTREME security risk — only for air-gapped gaming rigs.",
                "risk": HIGH,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v "FeatureSettingsOverride" /t REG_DWORD /d 3 /f',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v "FeatureSettingsOverrideMask" /t REG_DWORD /d 3 /f',
                ],
            },
            {
                "name": "Increase System Working Set (Kernel Pool)",
                "desc": "Sets SystemPages=0 letting Windows dynamically allocate maximum PTEs. Prevents 'RESOURCE_NOT_OWNED' BSoDs on high-RAM systems with many drivers.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v "SystemPages" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Large System Cache (Server-Style Memory)",
                "desc": "Tells the memory manager to behave like Windows Server: prioritizes file cache over application working sets. Huge for streaming/NAS use. Don't use with <16GB RAM.",
                "risk": MEDIUM,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v "LargeSystemCache" /t REG_DWORD /d 1 /f',
                ],
            },
            {
                "name": "Disable Speculative Execution Side-Channel (SSBD)",
                "desc": "Disables Speculative Store Bypass Disable mitigation. Removes branch prediction penalty on AMD Zen+ and Intel CPUs. Niche security tradeoff.",
                "risk": HIGH,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v "FeatureSettingsOverride" /t REG_DWORD /d 72 /f',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v "FeatureSettingsOverrideMask" /t REG_DWORD /d 3 /f',
                ],
            },
            {
                "name": "Disable Last Access Timestamp (Global)",
                "desc": "Stops NTFS from updating the 'last accessed' timestamp on every file read. Reduces disk I/O by thousands of writes/hour on busy systems.",
                "risk": SAFE,
                "cmds": [
                    'fsutil behavior set disablelastaccess 3',
                ],
            },
            {
                "name": "Enable Long Paths (Win32)",
                "desc": "Removes the legacy 260-character MAX_PATH limit for Win32 applications. Essential for deep node_modules, git repos, and Java projects.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\FileSystem" /v "LongPathsEnabled" /t REG_DWORD /d 1 /f',
                ],
            },
            {
                "name": "Disable 8.3 Short Name Creation",
                "desc": "Stops NTFS from creating DOS-compatible 8.3 filenames for every file. Saves ~20% overhead on file creation in directories with 300k+ files.",
                "risk": SAFE,
                "cmds": [
                    'fsutil behavior set disable8dot3 1',
                ],
            },
            {
                "name": "Disable Paging Executive (Lock Kernel in RAM)",
                "reverse": ['reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v "DisablePagingExecutive" /t REG_DWORD /d 0 /f'],
                "desc": "Forces the Windows kernel and drivers to stay in physical RAM instead of being paged to disk. Reduces latency spikes on systems with 16GB+ RAM.",
                "risk": LOW,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v "DisablePagingExecutive" /t REG_DWORD /d 1 /f',
                ],
            },
            {
                "name": "Disable NTFS Encryption Service (EFS)",
                "reverse": ['sc config EFS start= demand'],
                "desc": "Stops the Encrypting File System service. If you don't use EFS-encrypted folders, this saves a background service and avoids rare permission issues.",
                "risk": SAFE,
                "cmds": [
                    'sc stop EFS 2>nul',
                    'sc config EFS start= disabled',
                ],
            },
            {
                "name": "Increase NTFS Memory Usage (Large System Cache)",
                "reverse": ['reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v "LargeSystemCache" /t REG_DWORD /d 0 /f'],
                "desc": "Tells NTFS to use more RAM for file system caching. Improves file I/O performance on systems with 16GB+ RAM. The server-tuning trick applied to desktop.",
                "risk": LOW,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v "LargeSystemCache" /t REG_DWORD /d 1 /f',
                ],
            },
        ],
    },
    "GPU  &  Gaming": {
        "icon": "-",
        "tweaks": [
            {
                "name": "Force Disable Fullscreen Optimizations (Global)",
                "desc": "Prevents Windows from forcing pseudo-borderless mode on classic exclusive fullscreen games. Fixes micro-stutter. Conflicts with 'Force True Exclusive Fullscreen'.",
                "risk": LOW,
                "cmds": [
                    'reg add "HKCU\\System\\GameConfigStore" /v "GameDVR_FSEBehaviorMode" /t REG_DWORD /d 2 /f',
                    'reg add "HKCU\\System\\GameConfigStore" /v "GameDVR_DXGIHonorFSEWindowsCompatible" /t REG_DWORD /d 1 /f',
                    'reg add "HKCU\\System\\GameConfigStore" /v "GameDVR_FSEBehavior" /t REG_DWORD /d 2 /f',
                ]
            },
            {
                "name": "Disable Monitor VSync Override (Legacy)",
                "desc": "Disables the undocumented MonitorVsync registry override under GraphicsDrivers. Legacy setting — may have no effect on modern WDDM 2.x+ drivers.",
                "risk": LOW,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers" /v "MonitorVsync" /t REG_DWORD /d 0 /f'
                ]
            },
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
                "reverse": [
                    'reg delete "HKCU\\System\\GameConfigStore" /v "GameDVR_DXGIHonorFSEWindowsCompatible" /f',
                    'reg delete "HKCU\\System\\GameConfigStore" /v "GameDVR_FSEBehavior" /f',
                    'reg delete "HKCU\\System\\GameConfigStore" /v "GameDVR_FSEBehaviorMode" /f',
                    'reg delete "HKCU\\System\\GameConfigStore" /v "GameDVR_HonorUserFSEBehaviorMode" /f',
                    'powershell -NoProfile -Command "$p=\'HKCU:\\SOFTWARE\\Microsoft\\DirectX\\UserGpuPreferences\'; $k=\'DirectXUserGlobalSettings\'; $v=(Get-ItemProperty -Path $p -Name $k -EA SilentlyContinue).$k; if($v){$v=$v -replace \'SwapEffectUpgradeEnable=\\d+;\',\'SwapEffectUpgradeEnable=1;\'; Set-ItemProperty -Path $p -Name $k -Value $v -Force}"',
                ],
                "desc": "Disables SwapEffectUpgradeEnable so Windows cannot hijack your game into flip-model DWM composition. Saves 1 frame of latency. Conflicts with 'Force Disable Fullscreen Optimizations'.",
                "risk": LOW,
                "cmds": [
                    'reg add "HKCU\\System\\GameConfigStore" /v "GameDVR_DXGIHonorFSEWindowsCompatible" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\System\\GameConfigStore" /v "GameDVR_FSEBehavior" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\System\\GameConfigStore" /v "GameDVR_FSEBehaviorMode" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\System\\GameConfigStore" /v "GameDVR_HonorUserFSEBehaviorMode" /t REG_DWORD /d 0 /f',
                    'powershell -NoProfile -Command "$p=\'HKCU:\\SOFTWARE\\Microsoft\\DirectX\\UserGpuPreferences\'; $k=\'DirectXUserGlobalSettings\'; $v=(Get-ItemProperty -Path $p -Name $k -EA SilentlyContinue).$k; if(!$v){$v=\'\'}; if($v -notmatch \'SwapEffectUpgradeEnable\'){$v+=\'SwapEffectUpgradeEnable=0;\'} else {$v=$v -replace \'SwapEffectUpgradeEnable=\\d+;\',\'SwapEffectUpgradeEnable=0;\'}; New-Item -Path $p -Force -EA SilentlyContinue|Out-Null; Set-ItemProperty -Path $p -Name $k -Value $v -Force"',
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
                "reverse": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers" /v "HwSchMode" /t REG_DWORD /d 1 /f',
                ],
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
                    'powershell -NoProfile -Command "Get-ChildItem \"HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Class\\{4d36e968-e325-11ce-bfc1-08002be10318}\" -EA SilentlyContinue | ForEach-Object { $drv=(Get-ItemProperty $_.PSPath -Name \"DriverDesc\" -EA SilentlyContinue).DriverDesc; if($drv -match \"NVIDIA\"){Set-ItemProperty $_.PSPath -Name \"DisableDynamicPstate\" -Value 1 -Type DWord -Force} }"',
                ],
                "reverse": [
                    'powershell -NoProfile -Command "Get-ChildItem \"HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Class\\{4d36e968-e325-11ce-bfc1-08002be10318}\" -EA SilentlyContinue | ForEach-Object { Remove-ItemProperty $_.PSPath -Name \"DisableDynamicPstate\" -EA SilentlyContinue }"',
                ],
            },
            {
                "name": "MMCSS Game Task Max Priority",
                "reverse": [
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "GPU Priority" /t REG_DWORD /d 8 /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "Priority" /t REG_DWORD /d 2 /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "Scheduling Category" /t REG_SZ /d "Medium" /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "SFIO Priority" /t REG_SZ /d "Normal" /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "Background Only" /t REG_SZ /d "True" /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "Clock Rate" /t REG_DWORD /d 10000 /f',
                ],
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
                "name": "Disable Multi-Plane Overlay (MPO)",
                "desc": "Fixes stuttering, black screens, and flickering on NVIDIA/AMD GPUs by disabling MPO. Forces standard DWM composition.",
                "risk": LOW,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\Dwm" /v "OverlayTestMode" /t REG_DWORD /d 5 /f',
                ],
            },
            {
                "name": "Disable Variable Refresh Rate (VRR) Globally",
                "reverse": [
                    'powershell -NoProfile -Command "$p=\'HKCU:\\SOFTWARE\\Microsoft\\DirectX\\UserGpuPreferences\'; $k=\'DirectXUserGlobalSettings\'; $v=(Get-ItemProperty -Path $p -Name $k -EA SilentlyContinue).$k; if($v){$v=$v -replace \'VRROptimizeEnable=\\d+;\',\'VRROptimizeEnable=1;\'; Set-ItemProperty -Path $p -Name $k -Value $v -Force}"',
                ],
                "desc": "Disables Windows-level VRR which can conflict with G-Sync/FreeSync and cause micro-stutters in windowed games.",
                "risk": LOW,
                "cmds": [
                    'powershell -NoProfile -Command "$p=\'HKCU:\\SOFTWARE\\Microsoft\\DirectX\\UserGpuPreferences\'; $k=\'DirectXUserGlobalSettings\'; $v=(Get-ItemProperty -Path $p -Name $k -EA SilentlyContinue).$k; if(!$v){$v=\'\'}; if($v -notmatch \'VRROptimizeEnable\'){$v+=\'VRROptimizeEnable=0;\'} else {$v=$v -replace \'VRROptimizeEnable=\\d+;\',\'VRROptimizeEnable=0;\'}; New-Item -Path $p -Force -EA SilentlyContinue|Out-Null; Set-ItemProperty -Path $p -Name $k -Value $v -Force"',
                ],
            },
            {
                "name": "Disable GPU Energy Driver",
                "reverse": [
                    'powershell -NoProfile -Command "$s=Get-Service gpuenergydrv -EA SilentlyContinue; if($s){Set-Service gpuenergydrv -StartupType Automatic -EA SilentlyContinue; Start-Service gpuenergydrv -EA SilentlyContinue; Write-Host \'GPU Energy Driver re-enabled\'} else {Write-Host \'gpuenergydrv service not found (nothing to restore)\'}"',
                ],
                "desc": "Disables the GPU Energy Driver service which constantly polls the GPU for power metrics, causing DPC latency spikes. Skips gracefully if the service doesn't exist.",
                "risk": LOW,
                "cmds": [
                    'powershell -NoProfile -Command "$s=Get-Service gpuenergydrv -EA SilentlyContinue; if($s){Stop-Service gpuenergydrv -Force -EA SilentlyContinue; Set-Service gpuenergydrv -StartupType Disabled -EA SilentlyContinue; Write-Host \'GPU Energy Driver disabled\'} else {Write-Host \'gpuenergydrv service not found (ok)\'}"',
                ],
            },
            {
                "name": "Disable Xbox Game Monitoring",
                "reverse": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\xbgm" /v "Start" /t REG_DWORD /d 3 /f',
                ],
                "desc": "Stops the Xbox Game Monitoring service from hooking into game processes. Note: service was removed on Win10 2004+; harmless if not present.",
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
                "name": "Disable DWM Ghosting / Composition (Legacy)",
                "desc": "Disables DWM composition animations. Note: HungAppTimeout is handled by the 'Faster Shutdown Timeouts' tweak. Does not disable window ghosting (that requires a Win32 API call).",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DWM" /v "DisallowAnimations" /t REG_DWORD /d 1 /f',
                ],
            },
            {
                "name": "Force DirectX 12 Shader Cache to RAM",
                "desc": "Moves the DX pipeline state cache to a RAM-backed location and increases size limit. Eliminates shader compilation stutter on second launch.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKCU\\Software\\Microsoft\\DirectX\\UserGpuPreferences" /v "DirectXPipelineStateCache" /t REG_SZ /d "UseRamCache=1;MaxSize=4096" /f',
                ],
            },
            {
                "name": "Disable NVIDIA Shader Disk Cache Limit",
                "desc": "Removes the default 4GB shader cache cap via NVIDIA profile. Games with huge shader counts (Hogwarts Legacy, Cyberpunk) won't re-compile shaders after eviction.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKCU\\Software\\NVIDIA Corporation\\Global\\NVTweak" /v "NvCplShaderCacheLimitMB" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Disable Flip Queue Size (Pre-Rendered Frames = 1)",
                "desc": "Forces the GPU driver to render only 1 frame ahead. Reduces input lag by 1-3 frames at the cost of slightly lower average FPS. Essential for competitive FPS.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\Dwm" /v "MaximumPreRenderedFrames" /t REG_DWORD /d 1 /f',
                ],
            },
            {
                "name": "Disable NVIDIA Telemetry & Container Processes",
                "desc": "Kills NvTelemetryContainer, NvContainerLocalSystem, NvContainerNetworkService. These run 24/7 phoning home and using 50-100MB RAM even when not gaming.",
                "risk": SAFE,
                "cmds": [
                    'sc config NvTelemetryContainer start= disabled 2>nul',
                    'sc stop NvTelemetryContainer 2>nul',
                    'schtasks /change /tn "NvTmRep_CrashReport1_{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8}" /disable 2>nul',
                    'schtasks /change /tn "NvTmRep_CrashReport2_{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8}" /disable 2>nul',
                    'schtasks /change /tn "NvTmRep_CrashReport3_{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8}" /disable 2>nul',
                    'schtasks /change /tn "NvTmRep_CrashReport4_{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8}" /disable 2>nul',
                ],
            },
            {
                "name": "Disable Desktop Window Manager Throttling",
                "reverse": ['reg delete "HKCU\\SOFTWARE\\Microsoft\\Windows\\DWM" /v "MaxFrameLatency" /f 2>nul'],
                "desc": "Sets DWM max frame latency to 1 frame. Reduces compositor buffering for lower display latency in windowed/borderless games.",
                "risk": LOW,
                "cmds": [
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\DWM" /v "MaxFrameLatency" /t REG_DWORD /d 1 /f',
                ],
            },
            {
                "name": "Disable Cursor Shadow & Smooth Scrolling",
                "reverse": ['reg add "HKCU\\Control Panel\\Desktop" /v "CursorShadow" /t REG_DWORD /d 1 /f', 'reg add "HKCU\\Control Panel\\Desktop" /v "SmoothScroll" /t REG_DWORD /d 1 /f'],
                "desc": "Removes the cursor drop shadow and smooth scroll animations. Tiny GPU driver overhead savings — mostly placebo but satisfying for purists.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKCU\\Control Panel\\Desktop" /v "CursorShadow" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\Control Panel\\Desktop" /v "SmoothScroll" /t REG_DWORD /d 0 /f',
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
                    'cmd /c "bcdedit /deletevalue useplatformclock 2>nul"',
                    'cmd /c "bcdedit /deletevalue useplatformtick 2>nul"',
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
                "reverse": ["bcdedit /timeout 30"],
                "desc": "Removes the OS selection menu delay. Saves 30 seconds on every boot if you only have one OS installed.",
                "risk": SAFE,
                "cmds": [
                    'bcdedit /timeout 0',
                ],
            },
            {
                "name": "Disable Timer Coalescing",
                "desc": "Prevents Windows from batching hardware timer interrupts together to save power. Reduces jitter at the cost of slightly more CPU wake-ups.",
                "risk": LOW,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\kernel" /v "CoalescingTimerInterval" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "MMCSS Gaming Priority (SystemResponsiveness=0)",
                "desc": "Tells the Multimedia Class Scheduler to reserve 0% of CPU for background tasks during gaming. Sets Games task to High priority with High SFIO.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile" /v "SystemResponsiveness" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "Scheduling Category" /t REG_SZ /d "High" /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "SFIO Priority" /t REG_SZ /d "High" /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "Priority" /t REG_DWORD /d 6 /f',
                ],
            },
        ],
    },
    "Network": {
        "icon": "-",
        "tweaks": [
            {
                "name": "Disable Nagle's Algorithm (All Interfaces)",
                "reverse": ["powershell -NoProfile -Command \"Get-ChildItem 'HKLM:\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces' | ForEach-Object { Remove-ItemProperty -Path $_.PSPath -Name 'TcpAckFrequency' -EA SilentlyContinue; Remove-ItemProperty -Path $_.PSPath -Name 'TCPNoDelay' -EA SilentlyContinue; Remove-ItemProperty -Path $_.PSPath -Name 'TcpDelAckTicks' -EA SilentlyContinue }\""],
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
                "desc": "Default 20 reserves 20% CPU for background. Setting 0 (Windows internally treats as 10) minimizes CPU reserved for background tasks to ~10%.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile" /v "SystemResponsiveness" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Enable RSS, Disable Heuristics",
                "reverse": [
                    "netsh int tcp set global rss=default",
                    "netsh int tcp set global dca=default",
                    "netsh int tcp set heuristics default"
                ],
                "desc": "Receive Side Scaling distributes NIC processing across cores. Heuristics override your tuning \u2014 disable them.",
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
                "reverse": [
                    "netsh int tcp set global timestamps=default",
                    "netsh int tcp set global ecncapability=default"
                ],
                "desc": "Timestamps add 12 bytes per packet. ECN adds per-packet CPU processing. Both negligible benefits for gaming but measurable overhead.",
                "risk": SAFE,
                "cmds": [
                    'netsh int tcp set global timestamps=disabled',
                    'netsh int tcp set global ecncapability=disabled',
                ],
            },
            {
                "name": "Enable TCP Fast Open",
                "reverse": ["netsh int tcp set global fastopen=default fastopenfallback=default"],
                "desc": "Allows data in the SYN packet for faster connection establishment. Reduces handshake round trips.",
                "risk": SAFE,
                "cmds": [
                    'netsh int tcp set global fastopen=enabled',
                    'netsh int tcp set global fastopenfallback=enabled',
                ],
            },
            {
                "name": "Set TCP Congestion Control to CUBIC",
                "reverse": ["netsh int tcp set supplemental template=internet congestionprovider=default"],
                "desc": "Changes the TCP congestion provider to CUBIC. Already default on Win10 1709+. Better for high-speed, low-latency connections.",
                "risk": SAFE,
                "cmds": [
                    'netsh int tcp set supplemental template=internet congestionprovider=cubic',
                ],
            },

            {
                "name": "Disable IPv6 Tunneling (Teredo, ISATAP, 6to4)",
                "reverse": ["netsh int ipv6 isatap set state default", "netsh int ipv6 6to4 set state default", "netsh int teredo set state default"],
                "desc": "Disables legacy IPv6 transition technologies that constantly poll the network and create unnecessary virtual adapters.",
                "risk": SAFE,
                "cmds": [
                    'netsh interface teredo set state disabled',
                    'netsh interface isatap set state disabled',
                    'netsh interface ipv6 6to4 set state disabled',
                ],
            },
            {
                "name": "Disable WMM (Wi-Fi Multimedia) Power Save",
                "desc": "Stops the Wi-Fi adapter from entering low-power states between packet bursts. Crucial for stable wireless ping.",
                "risk": SAFE,
                "cmds": [
                    'powershell -NoProfile -Command "Get-NetAdapterAdvancedProperty -EA SilentlyContinue | Where-Object { $_.RegistryKeyword -match \'WMM|uAPSD\' } | Set-NetAdapterAdvancedProperty -RegistryValue \'0\' -EA SilentlyContinue"',
                ],
            },
            {
                "name": "Disable Large Send Offload (LSO)",
                "desc": "LSO offloads TCP segmentation to NIC hardware, but many drivers implement it poorly causing high latency and packet loss.",
                "risk": SAFE,
                "cmds": [
                    'powershell -NoProfile -Command "Get-NetAdapterAdvancedProperty -EA SilentlyContinue | Where-Object { $_.RegistryKeyword -match \'LsoV2IPv[46]\' } | Set-NetAdapterAdvancedProperty -RegistryValue \'0\' -EA SilentlyContinue"',
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
                    'powershell -NoProfile -Command "Get-NetAdapterAdvancedProperty -EA SilentlyContinue | Where-Object { $_.RegistryKeyword -match \'EEE\' } | Set-NetAdapterAdvancedProperty -RegistryValue \'0\' -EA SilentlyContinue"',
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
                "desc": "Sets the QoS non-best-effort bandwidth limit to zero. Only affects traffic tagged with QoS policies (rare on consumer PCs). The '20% reserved bandwidth' myth is debunked.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Psched" /v "NonBestEffortLimit" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Disable Receive Segment Coalescing (RSC)",
                "reverse": [
                    'powershell -NoProfile -Command "Get-NetAdapter | Enable-NetAdapterRsc -EA SilentlyContinue"',
                ],
                "desc": "RSC batches incoming packets. Good for throughput, terrible for latency. Disabling it forces immediate packet processing.",
                "risk": SAFE,
                "cmds": [
                    'powershell -NoProfile -Command "Get-NetAdapter | Disable-NetAdapterRsc -EA SilentlyContinue"',
                ],
            },
            {
                "name": "Disable NetBIOS over TCP/IP",
                "reverse": ["powershell -NoProfile -Command \"Get-WmiObject Win32_NetworkAdapterConfiguration | Where-Object { $_.IPEnabled -eq $true } | ForEach-Object { $_.SetTcpipNetbios(0) }\""],
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
            {
                "name": "Disable Network Throttling Index",
                "desc": "Removes the 10-packets-per-millisecond throttle Windows applies to non-multimedia network traffic. Allows full NIC throughput.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile" /v "NetworkThrottlingIndex" /t REG_DWORD /d 0xffffffff /f',
                ],
            },
            {
                "name": "Disable WPAD (Web Proxy Auto-Discovery)",
                "desc": "Stops Windows from broadcasting WPAD requests to discover proxy servers. A known attack vector for man-in-the-middle on local networks.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings\\Wpad" /v "WpadOverride" /t REG_DWORD /d 1 /f',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\WinHttpAutoProxySvc" /v "Start" /t REG_DWORD /d 4 /f',
                ],
            },
            {
                "name": "Disable ECN Capability",
                "desc": "Disables Explicit Congestion Notification. Some routers and firewalls drop ECN-marked packets, causing random connection stalls.",
                "risk": SAFE,
                "cmds": [
                    'netsh int tcp set global ecncapability=disabled',
                ],
            },
            {
                "name": "Disable Network Auto-Tuning Heuristics",
                "reverse": ['netsh int tcp set heuristics enabled'],
                "desc": "Prevents Windows from dynamically shrinking the TCP receive window based on its own heuristics. Keeps the auto-tuning level at 'normal' without interference.",
                "risk": SAFE,
                "cmds": [
                    'netsh int tcp set heuristics disabled',
                ],
            },
            {
                "name": "Disable NLA Probing (Network Location Awareness)",
                "reverse": ['reg delete "HKLM\\SYSTEM\\CurrentControlSet\\Services\\NlaSvc\\Parameters\\Internet" /v "EnableActiveProbing" /f 2>nul'],
                "desc": "Stops Windows from periodically pinging Microsoft servers (msftconnecttest.com) to check internet connectivity. Reduces background traffic and DNS queries.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\NlaSvc\\Parameters\\Internet" /v "EnableActiveProbing" /t REG_DWORD /d 0 /f',
                ],
            },
        ],
    },
    "Power  &  CPU": {
        "icon": "\u26A1",
        "tweaks": [
            {
                "name": "Activate Ultimate Performance Plan",
                "reverse": ["powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e"],
                "desc": "Hidden power plan that eliminates ALL power-saving delays. Duplicates the scheme and activates High Performance as fallback.",
                "risk": SAFE,
                "cmds": [
                    'powershell -NoProfile -Command "$out = powercfg /duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61; if ($out -match \'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\') { powercfg /setactive $matches[0] } else { powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c }"',
                ],
            },
            {
                "name": "Unpark All CPU Cores (100% Min)",
                "reverse": [
                    "powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR 0cc5b647-c1df-4637-891a-dec35c318583 10",
                    "powercfg /setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR 0cc5b647-c1df-4637-891a-dec35c318583 10",
                    "powercfg /setactive SCHEME_CURRENT"
                ],
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
                "reverse": ["powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR 5d76a2ca-e8c0-402f-a133-2158492d58ad 0", "powercfg /setactive SCHEME_CURRENT"],
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
                "reverse": [
                    "powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN 5",
                    "powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX 100",
                    "powercfg /setactive SCHEME_CURRENT"
                ],
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
                "reverse": [
                    "powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR be337238-0d82-4146-a960-4f3749d470c7 1",
                    "powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR 36687f9e-e3a5-4dbf-b1dc-15eb381c6863 33",
                    "powercfg /setactive SCHEME_CURRENT"
                ],
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
                "reverse": [
                    'reg delete "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Power\\PowerThrottling" /v "PowerThrottlingOff" /f',
                ],
                "desc": "Windows 10+ throttles background apps to save power. This can cause stuttering if Windows mis-classifies your workload as background.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Power\\PowerThrottling" /v "PowerThrottlingOff" /t REG_DWORD /d 1 /f',
                ],
            },
            {
                "name": "Disable USB Selective Suspend",
                "reverse": [
                    "powercfg /setacvalueindex SCHEME_CURRENT 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 1",
                    "powercfg /setdcvalueindex SCHEME_CURRENT 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 1",
                    "powercfg /setactive SCHEME_CURRENT"
                ],
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
                "reverse": ["powercfg /setacvalueindex SCHEME_CURRENT SUB_PCIEXPRESS ee12f906-d277-404b-b6da-e5fa1a576df5 1", "powercfg /setactive SCHEME_CURRENT"],
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
                "reverse": ["powercfg /change standby-timeout-ac 30", "powercfg /change monitor-timeout-ac 15"],
                "desc": "Prevents the PC and display from ever going to sleep automatically.",
                "risk": SAFE,
                "cmds": [
                    'powercfg /change standby-timeout-ac 0',
                    'powercfg /change monitor-timeout-ac 0',
                ],
            },
            {
                "name": "Disable Disk Sleep",
                "reverse": ["powercfg /change disk-timeout-ac 20"],
                "desc": "Prevents hard drives from spinning down. Eliminates the 3-5 second freeze when accessing a sleeping drive.",
                "risk": SAFE,
                "cmds": [
                    'powercfg /change disk-timeout-ac 0',
                ],
            },
            {
                "name": "Disable Connected Standby (Modern Standby)",
                "reverse": [
                    'reg delete "HKLM\\System\\CurrentControlSet\\Control\\Power" /v "PlatformAoAcOverride" /f',
                ],
                "desc": "Forces S3 sleep instead of S0ix. Prevents the PC from waking up in a backpack, draining battery, and running background tasks while 'asleep'.",
                "risk": LOW,
                "cmds": [
                    'reg add "HKLM\\System\\CurrentControlSet\\Control\\Power" /v "PlatformAoAcOverride" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Disable Hibernation & Fast Startup",
                "reverse": [
                    'powercfg -h on',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Power" /v "HiberbootEnabled" /t REG_DWORD /d 1 /f',
                ],
                "desc": "Deletes the hiberfil.sys file (saving GBs of space) and forces a true clean boot every time you shut down, preventing driver rot.",
                "risk": SAFE,
                "cmds": [
                    'powercfg -h off',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Power" /v "HiberbootEnabled" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Set Processor Performance Check Interval (5ms)",
                "reverse": [
                    "powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR 4d2b0152-7d5c-498b-88e2-34345392a2c5 15000",
                    "powercfg /setactive SCHEME_CURRENT"
                ],
                "desc": "Reduces the interval at which Windows checks if the CPU frequency needs adjusting from 15ms to 5ms. Faster boost clocks under sudden load.",
                "risk": LOW,
                "cmds": [
                    'powercfg -attributes SUB_PROCESSOR 4d2b0152-7d5c-498b-88e2-34345392a2c5 -ATTRIB_HIDE',
                    'powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR 4d2b0152-7d5c-498b-88e2-34345392a2c5 5000',
                    'powercfg /setactive SCHEME_CURRENT',
                ],
            },
            {
                "name": "Disable Idle Promote / Demote Thresholds",
                "reverse": [
                    "powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR 4b92d758-5a24-4851-a470-815d78aee119 20",
                    "powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR 7b224883-b3cc-4d79-819f-8374152cbe7c 60",
                    "powercfg /setactive SCHEME_CURRENT"
                ],
                "desc": "Sets idle demote threshold to 100% and promote threshold to 0%. Cores never downshift to lower C-states unless fully idle.",
                "risk": LOW,
                "cmds": [
                    'powercfg -attributes SUB_PROCESSOR 4b92d758-5a24-4851-a470-815d78aee119 -ATTRIB_HIDE',
                    'powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR 4b92d758-5a24-4851-a470-815d78aee119 100',
                    'powercfg -attributes SUB_PROCESSOR 7b224883-b3cc-4d79-819f-8374152cbe7c -ATTRIB_HIDE',
                    'powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR 7b224883-b3cc-4d79-819f-8374152cbe7c 0',
                    'powercfg /setactive SCHEME_CURRENT',
                ],
            },
            {
                "name": "Disable Latency-Sensitive Core Parking",
                "reverse": [
                    "powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR 619b7505-003b-4e82-b7a6-4dd29c300971 1",
                    "powercfg /setactive SCHEME_CURRENT"
                ],
                "desc": "Removes latency hints from the core parking algorithm. Combined with unparking, ensures all cores respond equally fast.",
                "risk": LOW,
                "cmds": [
                    'powercfg -attributes SUB_PROCESSOR 619b7505-003b-4e82-b7a6-4dd29c300971 -ATTRIB_HIDE',
                    'powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR 619b7505-003b-4e82-b7a6-4dd29c300971 0',
                    'powercfg /setactive SCHEME_CURRENT',
                ],
            },
            {
                "name": "Disable Processor Performance Autonomous Mode",
                "reverse": ['powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR 8baa4a8a-14c6-4451-8e8b-14bdbd197537 1', 'powercfg /setactive SCHEME_CURRENT'],
                "desc": "Forces the OS to control CPU P-states instead of letting the processor firmware decide autonomously. Gives Windows full control over frequency scaling.",
                "risk": LOW,
                "cmds": [
                    'powercfg -attributes SUB_PROCESSOR 8baa4a8a-14c6-4451-8e8b-14bdbd197537 -ATTRIB_HIDE',
                    'powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR 8baa4a8a-14c6-4451-8e8b-14bdbd197537 0',
                    'powercfg /setactive SCHEME_CURRENT',
                ],
            },
            {
                "name": "Disable CPU Idle Scaling (Processor Idle Disable)",
                "reverse": ['powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR 5d76a2ca-e8c0-402f-a133-2158492d58ad 0', 'powercfg /setactive SCHEME_CURRENT'],
                "desc": "Prevents the CPU from entering low-power idle states during brief inactivity — cores stay at full speed. Measurably reduces wake-up latency for real-time tasks.",
                "risk": LOW,
                "cmds": [
                    'powercfg -attributes SUB_PROCESSOR 5d76a2ca-e8c0-402f-a133-2158492d58ad -ATTRIB_HIDE',
                    'powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR 5d76a2ca-e8c0-402f-a133-2158492d58ad 1',
                    'powercfg /setactive SCHEME_CURRENT',
                ],
            },
        ],
    },
    "MSI  &  Interrupts": {
        "icon": "-",
        "tweaks": [
            {
                "name": "Enable MSI Mode on All PCI Devices",
                "reverse": ["powershell -NoProfile -Command \"$cats=@(@{C='Display'}, @{C='Net'}, @{C='SCSIAdapter'}, @{C='HDC'}, @{C='USB'}); foreach($c in $cats){Get-PnpDevice -Class $c.C -Status OK -EA SilentlyContinue | ForEach-Object { $mp='HKLM:\\SYSTEM\\CurrentControlSet\\Enum\\'+$_.InstanceId+'\\Device Parameters\\Interrupt Management\\MessageSignaledInterruptProperties'; if(Test-Path $mp){ Remove-ItemProperty -Path $mp -Name 'MSISupported' -EA SilentlyContinue }}}\""],
                "desc": "Switches GPU, NIC, USB, Storage, Audio from legacy shared IRQ lines to private Message Signaled Interrupts. Drastically lowers DPC latency. Warning: may cause BSODs on devices with broken MSI implementations (some Realtek NICs, older USB3 controllers).",
                "risk": MEDIUM,
                "cmds": [
                    'powershell -NoProfile -ExecutionPolicy Bypass -Command "$cats=@(@{C=\'Display\'}, @{C=\'Net\'}, @{C=\'SCSIAdapter\'}, @{C=\'HDC\'}, @{C=\'USB\'}); foreach($c in $cats){Get-PnpDevice -Class $c.C -Status OK -EA SilentlyContinue | ForEach-Object { $mp=\'HKLM:\\SYSTEM\\CurrentControlSet\\Enum\\\'+$_.InstanceId+\'\\Device Parameters\\Interrupt Management\\MessageSignaledInterruptProperties\'; if(!(Test-Path $mp)){New-Item -Path $mp -Force|Out-Null}; Set-ItemProperty -Path $mp -Name \'MSISupported\' -Value 1 -Type DWord -Force}}"',
                ],
            },
            {
                "name": "Disable USB Controller Power Saving",
                "reverse": ["powershell -NoProfile -Command \"Get-PnpDevice -Class USB -Status OK -EA SilentlyContinue | Where-Object {($_.Service -match 'xhci|ehci') -or ($_.FriendlyName -match 'Host Controller|xHCI|eHCI')} | ForEach-Object { $bp='HKLM:\\SYSTEM\\CurrentControlSet\\Enum\\'+$_.InstanceId+'\\Device Parameters'; Remove-ItemProperty -Path $bp -Name 'EnhancedPowerManagementEnabled' -EA SilentlyContinue; Remove-ItemProperty -Path $bp -Name 'SelectiveSuspendEnabled' -EA SilentlyContinue }\""],
                "desc": "Sets EnhancedPowerManagement=0, SelectiveSuspend=0 on USB host controllers. Fixes random 10ms input spikes on mice and keyboards.",
                "risk": SAFE,
                "cmds": [
                    'powershell -NoProfile -Command "Get-PnpDevice -Class USB -Status OK -EA SilentlyContinue | Where-Object {($_.Service -match \'xhci|ehci\') -or ($_.FriendlyName -match \'Host Controller|xHCI|eHCI\')} | ForEach-Object { $bp=\'HKLM:\\SYSTEM\\CurrentControlSet\\Enum\\\'+$_.InstanceId+\'\\Device Parameters\'; Set-ItemProperty -Path $bp -Name \'EnhancedPowerManagementEnabled\' -Value 0 -Type DWord -Force -EA SilentlyContinue; Set-ItemProperty -Path $bp -Name \'SelectiveSuspendEnabled\' -Value 0 -Type DWord -Force -EA SilentlyContinue }"',
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
            {
                "name": "Pin GPU Interrupts to CPU 0 (Affinity Lock)",
                "desc": "Forces GPU interrupt handling to a single core, eliminating cross-core migration overhead. Can reduce frame time variance by 5-15%.",
                "risk": MEDIUM,
                "cmds": [
                    'powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-PnpDevice -Class Display -Status OK -EA SilentlyContinue | ForEach-Object { $ap=\'HKLM:\\SYSTEM\\CurrentControlSet\\Enum\\\'+$_.InstanceId+\'\\Device Parameters\\Interrupt Management\\Affinity Policy\'; if(!(Test-Path $ap)){New-Item -Path $ap -Force|Out-Null}; Set-ItemProperty -Path $ap -Name \'DevicePolicy\' -Value 4 -Type DWord -Force; Set-ItemProperty -Path $ap -Name \'AssignmentSetOverride\' -Value ([byte[]]@(1)) -Type Binary -Force}"',
                ],
            },
            {
                "name": "Disable NIC Interrupt Moderation",
                "desc": "Forces the NIC to fire an interrupt for every packet instead of batching. Lowers network latency at the cost of slightly more CPU usage.",
                "risk": LOW,
                "cmds": [
                    'powershell -NoProfile -Command "Get-NetAdapterAdvancedProperty -DisplayName \"*Interrupt Moderation*\" -EA SilentlyContinue | Set-NetAdapterAdvancedProperty -DisplayValue \"Disabled\" -EA SilentlyContinue"',
                ],
            },
        ],
    },
    "Mouse  &  Input": {
        "icon": "-",
        "tweaks": [
            {
                "name": "Optimize Mouse & Keyboard Queue (Input Latency)",
                "desc": "Decreases data queue size for inputs, slightly reducing input latency at the driver level.",
                "risk": LOW,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\kbdclass\\Parameters" /v "KeyboardDataQueueSize" /t REG_DWORD /d 20 /f',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\mouclass\\Parameters" /v "MouseDataQueueSize" /t REG_DWORD /d 20 /f'
                ]
            },
            {
                "name": "MarkC Mouse Fix (1:1 Raw Input)",
                "reverse": [
                    'reg add "HKCU\\Control Panel\\Mouse" /v "MouseSpeed" /t REG_SZ /d "1" /f',
                    'reg add "HKCU\\Control Panel\\Mouse" /v "MouseThreshold1" /t REG_SZ /d "6" /f',
                    'reg add "HKCU\\Control Panel\\Mouse" /v "MouseThreshold2" /t REG_SZ /d "10" /f',
                    'reg add "HKCU\\Control Panel\\Mouse" /v "MouseSensitivity" /t REG_SZ /d "10" /f',
                    'reg add "HKCU\\Control Panel\\Mouse" /v "SmoothMouseXCurve" /t REG_BINARY /d 0000000000000000156e000000000000004001000000000029dc0300000000000000280000000000 /f',
                    'reg add "HKCU\\Control Panel\\Mouse" /v "SmoothMouseYCurve" /t REG_BINARY /d 0000000000000000b85e010000000000cd4c050000000000cd4c1800000000000038020000000000 /f',
                ],
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
                "reverse": [
                    'reg add "HKCU\\Control Panel\\Accessibility\\StickyKeys" /v "Flags" /t REG_SZ /d "510" /f',
                    'reg add "HKCU\\Control Panel\\Accessibility\\Keyboard Response" /v "Flags" /t REG_SZ /d "126" /f',
                    'reg add "HKCU\\Control Panel\\Accessibility\\ToggleKeys" /v "Flags" /t REG_SZ /d "62" /f',
                ],
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
                "name": "Set Performance Visual Preferences (Comprehensive)",
                "reverse": [
                    'reg add "HKCU\\Control Panel\\Desktop" /v "UserPreferencesMask" /t REG_BINARY /d 9e3e078012000000 /f',
                ],
                "desc": "Sets UserPreferencesMask to a performance-oriented bitmask. Disables cursor shadow, menu/tooltip animations, and other visual effects. Overwrites ALL visual preference flags.",
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
                "name": "Disable Touch Input & Visual Feedback",
                "desc": "Disables touch feedback animations, touch gestures, and edge swipe. Reduces input processing overhead on non-touch desktops.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKCU\\Control Panel\\Cursors" /v "ContactVisualization" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\Control Panel\\Cursors" /v "GestureVisualization" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\EdgeUI" /v "AllowEdgeSwipe" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Disable Pen & Ink Input Service",
                "reverse": [
                    'sc config TabletInputService start= auto',
                ],
                "desc": "Stops the Touch Keyboard and Handwriting Panel Service. Saves RAM and CPU on desktops without pen/touch input.",
                "risk": SAFE,
                "cmds": [
                    'sc stop TabletInputService',
                    'sc config TabletInputService start= disabled',
                ],
            },
            {
                "name": "Disable Pointer Precision Enhancement",
                "reverse": ['reg add "HKCU\\Control Panel\\Mouse" /v "MouseSpeed" /t REG_SZ /d "1" /f', 'reg add "HKCU\\Control Panel\\Mouse" /v "MouseThreshold1" /t REG_SZ /d "6" /f', 'reg add "HKCU\\Control Panel\\Mouse" /v "MouseThreshold2" /t REG_SZ /d "10" /f'],
                "desc": "Fully disables Windows mouse acceleration (Enhanced Pointer Precision). Sets flat 1:1 scaling so physical movement matches cursor movement exactly. Essential for FPS gamers.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKCU\\Control Panel\\Mouse" /v "MouseSpeed" /t REG_SZ /d "0" /f',
                    'reg add "HKCU\\Control Panel\\Mouse" /v "MouseThreshold1" /t REG_SZ /d "0" /f',
                    'reg add "HKCU\\Control Panel\\Mouse" /v "MouseThreshold2" /t REG_SZ /d "0" /f',
                ],
            },
            {
                "name": "Set USB Mouse Polling Override (1000Hz)",
                "reverse": ['reg delete "HKLM\\SYSTEM\\CurrentControlSet\\Services\\mouclass\\Parameters" /v "MouseDataQueueSize" /f 2>nul', 'reg delete "HKLM\\SYSTEM\\CurrentControlSet\\Services\\mouhid\\Parameters" /v "UseOnlyMSHidMouse" /f 2>nul'],
                "desc": "Optimizes USB mouse driver parameters for lowest latency. Sets mouse data queue to 16 (smallest safe value) and forces the MS HID mouse driver for consistency.",
                "risk": LOW,
                "cmds": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\mouclass\\Parameters" /v "MouseDataQueueSize" /t REG_DWORD /d 16 /f',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\mouhid\\Parameters" /v "UseOnlyMSHidMouse" /t REG_DWORD /d 1 /f',
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
                "reverse": [
                    'powershell -NoProfile -Command "Get-ScheduledTask -TaskName \"NvTm*\" -EA SilentlyContinue | Enable-ScheduledTask -EA SilentlyContinue; $s=Get-Service NvTelemetryContainer -EA SilentlyContinue; if($s){Set-Service NvTelemetryContainer -StartupType Automatic -EA SilentlyContinue; Start-Service NvTelemetryContainer -EA SilentlyContinue}"',
                ],
                "desc": "Disables NVIDIA's background telemetry services and tasks. Skips gracefully if NVIDIA is not installed.",
                "risk": SAFE,
                "cmds": [
                    'powershell -NoProfile -Command "Get-ScheduledTask -TaskName \"NvTm*\" -EA SilentlyContinue | Disable-ScheduledTask -EA SilentlyContinue; $s=Get-Service NvTelemetryContainer -EA SilentlyContinue; if($s){Stop-Service NvTelemetryContainer -Force -EA SilentlyContinue; Set-Service NvTelemetryContainer -StartupType Disabled -EA SilentlyContinue; Write-Host \"NVIDIA telemetry disabled\"} else {Write-Host \"No NVIDIA telemetry service found (ok)\"}"',
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
            {
                "name": "Disable Handwriting Data Sharing",
                "desc": "Prevents Windows from sending handwriting recognition data and ink samples to Microsoft for product improvement.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\TabletPC" /v "PreventHandwritingDataSharing" /t REG_DWORD /d 1 /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\HandwritingErrorReports" /v "PreventHandwritingErrorReports" /t REG_DWORD /d 1 /f',
                ],
            },
            {
                "name": "Disable KMS Client Online AVS Validation",
                "desc": "Stops Windows from phoning home to validate your license activation status. Reduces background network traffic.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows NT\\CurrentVersion\\Software Protection Platform" /v "NoGenTicket" /t REG_DWORD /d 1 /f',
                ],
            },
            {
                "name": "Disable Wi-Fi Sense & Hotspot 2.0",
                "desc": "Prevents Windows from auto-connecting to suggested hotspots and sharing Wi-Fi credentials. Privacy and security improvement.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\WcmSvc\\wifinetworkmanager\\config" /v "AutoConnectAllowedOEM" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\PolicyManager\\default\\WiFi\\AllowAutoConnectToWiFiSenseHotspots" /v "value" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\WlanSvc\\AnqpCache" /v "OsuRegistrationStatus" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Disable Customer Experience Improvement Program (CEIP)",
                "desc": "Disables the application CEIP data collection across Windows and Office. Stops background SQM data uploads that waste bandwidth and CPU.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\SQMClient\\Windows" /v "CEIPEnable" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\AppV\\CEIP" /v "CEIPEnable" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\SOFTWARE\\Policies\\Microsoft\\Messenger\\Client" /v "CEIP" /t REG_DWORD /d 2 /f',
                ],
            },
            {
                "name": "Disable Application Impact Telemetry (AIT)",
                "reverse": ['reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppCompat" /v "AITEnable" /t REG_DWORD /d 1 /f'],
                "desc": "Stops Windows from tracking which apps you launch, how often, and for how long. Removes a hidden performance monitoring layer that runs on every process start.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppCompat" /v "AITEnable" /t REG_DWORD /d 0 /f',
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
                "reverse": [
                    'sc config DiagTrack start= auto',
                    'sc config dmwappushservice start= demand',
                    'net start DiagTrack',
                ],
                "desc": "The main telemetry pipeline (Connected User Experiences) and its feeder service. Constant CPU + network drain eliminated.",
                "risk": SAFE,
                "cmds": [
                    'sc stop DiagTrack', 'sc config DiagTrack start= disabled',
                    'sc stop dmwappushservice', 'sc config dmwappushservice start= disabled',
                ],
            },
            {
                "name": "Disable SysMain / Superfetch",
                "reverse": [
                    'sc config SysMain start= auto',
                    'net start SysMain',
                ],
                "desc": "Pre-loads apps into RAM based on usage habits. Constant disk I/O on HDDs, wastes RAM on SSDs. Safe to disable on SSDs.",
                "risk": SAFE,
                "cmds": [
                    'sc stop SysMain', 'sc config SysMain start= disabled',
                ],
            },
            {
                "name": "Disable WER, Diagnostics & Link Tracking",
                "reverse": [
                    'sc config WerSvc start= demand',
                    'sc config WdiSystemHost start= demand',
                    'sc config WdiServiceHost start= demand',
                    'sc config TrkWks start= auto',
                    'sc config diagsvc start= demand',
                    'net start TrkWks',
                ],
                "desc": "Windows Error Reporting, Diagnostic hosts, and Distributed Link Tracking \u2014 all background services with zero user benefit.",
                "risk": SAFE,
                "cmds": [
                    'sc stop WerSvc', 'sc config WerSvc start= disabled',
                    'sc stop WdiSystemHost', 'sc config WdiSystemHost start= disabled',
                    'sc stop WdiServiceHost', 'sc config WdiServiceHost start= disabled',
                    'sc stop TrkWks', 'sc config TrkWks start= disabled',
                    'sc stop diagsvc', 'sc config diagsvc start= disabled',
                ],
            },
            {
                "name": "Disable Bloat Services (Fax, Maps, Retail...)",
                "reverse": [
                    'sc config Fax start= demand',
                    'sc config MapsBroker start= auto',
                    'sc config RetailDemo start= demand',
                    'sc config AJRouter start= demand',
                    'sc config wisvc start= demand',
                    'sc config lfsvc start= demand',
                    'sc config RemoteRegistry start= disabled',
                ],
                "desc": "Disables Fax, Downloaded Maps Manager, Retail Demo, AllJoyn IoT router, Windows Insider, Geolocation, Remote Registry.",
                "risk": SAFE,
                "cmds": [
                    'sc stop Fax', 'sc config Fax start= disabled',
                    'sc stop MapsBroker', 'sc config MapsBroker start= disabled',
                    'sc stop RetailDemo', 'sc config RetailDemo start= disabled',
                    'sc stop AJRouter', 'sc config AJRouter start= disabled',
                    'sc stop wisvc', 'sc config wisvc start= disabled',
                    'sc stop lfsvc', 'sc config lfsvc start= disabled',
                    'sc stop RemoteRegistry', 'sc config RemoteRegistry start= disabled',
                ],
            },
            {
                "name": "Disable Xbox Services (4 services)",
                "reverse": [
                    'sc config XblAuthManager start= demand',
                    'sc config XblGameSave start= demand',
                    'sc config XboxGipSvc start= demand',
                    'sc config XboxNetApiSvc start= demand',
                ],
                "desc": "Xbox Live Auth, Game Save, Accessory Management, Networking. Disable if you don't use Xbox Game Pass on PC.",
                "risk": SAFE,
                "cmds": [
                    'sc stop XblAuthManager', 'sc config XblAuthManager start= disabled',
                    'sc stop XblGameSave', 'sc config XblGameSave start= disabled',
                    'sc stop XboxGipSvc', 'sc config XboxGipSvc start= disabled',
                    'sc stop XboxNetApiSvc', 'sc config XboxNetApiSvc start= disabled',
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
                    'schtasks /Change /TN "Microsoft\\Windows\\DiskDiagnostic\\Microsoft-Windows-DiskDiagnosticDataCollector" /Disable',
                    'schtasks /Change /TN "Microsoft\\Windows\\Windows Error Reporting\\QueueReporting" /Disable',
                ],
            },
            {
                "name": "Disable Print Spooler",
                "reverse": [
                    'sc config Spooler start= auto',
                    'net start Spooler',
                ],
                "desc": "Disables the printer service. Only use this if you NEVER print to a physical or PDF printer.",
                "risk": MEDIUM,
                "cmds": [
                    'sc stop Spooler', 'sc config Spooler start= disabled',
                ],
            },
            {
                "name": "Disable Windows Search Service",
                "reverse": [
                    'sc config WSearch start= delayed-auto',
                    'net start WSearch',
                ],
                "desc": "Disables the background file indexer. Search will still work but will be slower. Saves massive disk I/O.",
                "risk": MEDIUM,
                "cmds": [
                    'sc stop WSearch', 'sc config WSearch start= disabled',
                ],
            },
            {
                "name": "Disable Windows Update Service",
                "reverse": [
                    'sc config wuauserv start= demand',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\WaaSMedicSvc" /v "Start" /t REG_DWORD /d 3 /f',
                    'sc config UsoSvc start= delayed-auto',
                    'net start UsoSvc',
                    'net start wuauserv',
                ],
                "desc": "Completely disables Windows Update. HIGH RISK. You will not receive security patches or feature updates.",
                "risk": HIGH,
                "cmds": [
                    'sc stop wuauserv', 'sc config wuauserv start= disabled',
                    'sc stop WaaSMedicSvc', 'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\WaaSMedicSvc" /v "Start" /t REG_DWORD /d 4 /f',
                    'sc stop UsoSvc', 'sc config UsoSvc start= disabled',
                ],
            },
            {
                "name": "Disable Background Intelligent Transfer (BITS)",
                "reverse": [
                    'sc config BITS start= demand',
                    'net start BITS',
                ],
                "desc": "Disables BITS, which is used by Windows Update and other apps to download files in the background.",
                "risk": MEDIUM,
                "cmds": [
                    'sc stop BITS', 'sc config BITS start= disabled',
                ],
            },
            {
                "name": "Disable Security Center Service",
                "reverse": [
                    'sc config wscsvc start= auto',
                    'net start wscsvc',
                ],
                "desc": "Disables the Windows Security Center service. Stops notifications about antivirus and firewall status.",
                "risk": HIGH,
                "cmds": [
                    'sc stop wscsvc', 'sc config wscsvc start= disabled',
                ],
            },
            {
                "name": "Disable Windows Biometric Service",
                "reverse": [
                    'sc config WbioSrvc start= demand',
                ],
                "desc": "Stops the fingerprint/face recognition service. Saves resources on desktops without biometric hardware.",
                "risk": SAFE,
                "cmds": [
                    'sc stop WbioSrvc', 'sc config WbioSrvc start= disabled',
                ],
            },
            {
                "name": "Disable Connected Devices Platform Service",
                "reverse": [
                    'sc config CDPSvc start= auto',
                    'sc config CDPUserSvc start= auto',
                ],
                "desc": "Disables cross-device experience services (Bluetooth sync, phone link background, nearby sharing). Saves CPU and network.",
                "risk": SAFE,
                "cmds": [
                    'sc stop CDPSvc', 'sc config CDPSvc start= disabled',
                    'sc stop CDPUserSvc', 'sc config CDPUserSvc start= disabled',
                ],
            },
            {
                "name": "Disable Phone Link Service",
                "reverse": [
                    'sc config PhoneSvc start= demand',
                ],
                "desc": "Stops the Phone Service used by Windows Phone Link app. Saves background CPU and memory if you don't use phone integration.",
                "risk": SAFE,
                "cmds": [
                    'sc stop PhoneSvc', 'sc config PhoneSvc start= disabled',
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
                    'arp -d *',
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
                    'powershell -NoProfile -Command "Get-ChildItem \"$env:LOCALAPPDATA\\Mozilla\\Firefox\\Profiles\" -Directory -Filter \"*.default*\" -EA SilentlyContinue | ForEach-Object { Remove-Item (Join-Path $_.FullName \"cache2\\*\") -Recurse -Force -EA SilentlyContinue }"',
                ],
            },
            {
                "name": "NTFS Optimizations (Last Access, 8.3, Memory)",
                "reverse": [
                    "fsutil behavior set disablelastaccess 2",
                    "fsutil behavior set disable8dot3 0",
                    "fsutil behavior set memoryusage 1"
                ],
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
                "desc": "Wipes all Windows Event logs (classic + modern). Good for a fresh start when troubleshooting, or just to free up space.",
                "risk": SAFE,
                "cmds": [
                    'powershell -NoProfile -Command "Get-EventLog -List -EA SilentlyContinue | ForEach-Object { Clear-EventLog $_.Log -EA SilentlyContinue }"',
                    'powershell -NoProfile -Command "wevtutil el | ForEach-Object { wevtutil cl $_ 2>$null }"',
                ],
            },
            {
                "name": "Disable Windows Error Reporting (WER) Folders",
                "desc": "Prevents WER from sending additional diagnostic data and disables report queuing. The WER folders may still be created but will contain less data.",
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
            {
                "name": "Clear Font Cache",
                "desc": "Stops the font cache service, deletes corrupted font cache files, and restarts. Fixes garbled text and missing font glyphs.",
                "risk": SAFE,
                "cmds": [
                    'net stop FontCache',
                    'cmd /c del /q /f /s "%WINDIR%\\ServiceProfiles\\LocalService\\AppData\\Local\\FontCache\\*" 2>nul',
                    'cmd /c del /q /f "%LOCALAPPDATA%\\FontCache\\*" 2>nul',
                    'net start FontCache',
                ],
            },
            {
                "name": "Reset Winsock & TCP/IP Stack",
                "desc": "Nuclear network reset. Clears all Winsock LSP entries and resets the TCP/IP stack to factory defaults. Requires reboot.",
                "risk": MEDIUM,
                "cmds": [
                    'netsh winsock reset',
                    'netsh int ip reset',
                ],
            },
        ],
    },
    "UI  &  QoL": {
        "icon": "-",
        "tweaks": [
            {
                "name": "Faster Shutdown Timeouts",
                "reverse": [
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control" /v "WaitToKillServiceTimeout" /t REG_SZ /d "5000" /f',
                    'reg add "HKCU\\Control Panel\\Desktop" /v "WaitToKillAppTimeout" /t REG_SZ /d "20000" /f',
                    'reg add "HKCU\\Control Panel\\Desktop" /v "HungAppTimeout" /t REG_SZ /d "5000" /f',
                    'reg add "HKCU\\Control Panel\\Desktop" /v "AutoEndTasks" /t REG_SZ /d "0" /f',
                ],
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
                "reverse": [
                    'reg delete "HKCU\\SOFTWARE\\Classes\\CLSID\\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}" /f',
                ],
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
                "desc": "Skips the picture lock screen and goes straight to the password/PIN prompt on boot. Requires Windows Pro or Enterprise (does not work on Home edition).",
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
                "reverse": [
                    'reg delete "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender" /v "DisableAntiSpyware" /f',
                    'reg delete "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection" /v "DisableRealtimeMonitoring" /f',
                    'reg delete "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection" /v "DisableBehaviorMonitoring" /f',
                    'reg delete "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection" /v "DisableOnAccessProtection" /f',
                    'reg delete "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection" /v "DisableScanOnRealtimeEnable" /f',
                ],
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
                "name": "Disable Windows Copilot",
                "desc": "Prevents Windows Copilot AI assistant from loading. Saves RAM, removes the sidebar icon, and stops background Edge WebView processes.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKCU\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsCopilot" /v "TurnOffWindowsCopilot" /t REG_DWORD /d 1 /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsCopilot" /v "TurnOffWindowsCopilot" /t REG_DWORD /d 1 /f',
                ],
            },
            {
                "name": "Disable Recall / AI Screenshots (Win 11 24H2)",
                "desc": "Prevents the Recall feature from taking periodic screenshots of your desktop. Only relevant on Windows 11 24H2+ with compatible NPU.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsAI" /v "DisableAIDataAnalysis" /t REG_DWORD /d 1 /f',
                    'reg add "HKCU\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsAI" /v "DisableAIDataAnalysis" /t REG_DWORD /d 1 /f',
                ],
            },
            {
                "name": "Set Explorer Compact View (Remove Padding)",
                "desc": "Removes the extra spacing Windows 11 added to File Explorer. Makes it dense like Windows 10 without losing any functionality.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v "UseCompactMode" /t REG_DWORD /d 1 /f',
                ],
            },
            {
                "name": "Disable Taskbar Search Box & Highlights",
                "reverse": ['reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Search" /v "SearchboxTaskbarMode" /t REG_DWORD /d 2 /f', 'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\SearchSettings" /v "IsDynamicSearchBoxEnabled" /t REG_DWORD /d 1 /f'],
                "desc": "Removes the Bing search box and trending search highlights from the taskbar. Reclaim space and stop accidental web searches from Start menu.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Search" /v "SearchboxTaskbarMode" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\SearchSettings" /v "IsDynamicSearchBoxEnabled" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "name": "Disable News & Interests Widget",
                "reverse": ['reg delete "HKLM\\SOFTWARE\\Policies\\Microsoft\\Dsh" /v "AllowNewsAndInterests" /f 2>nul', 'reg delete "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Feeds" /v "ShellFeedsTaskbarViewMode" /f 2>nul'],
                "desc": "Kills the Windows 10/11 news widget that wastes RAM, CPU, and bandwidth loading MSN content. Removes it from taskbar completely.",
                "risk": SAFE,
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Dsh" /v "AllowNewsAndInterests" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Feeds" /v "ShellFeedsTaskbarViewMode" /t REG_DWORD /d 2 /f',
                ],
            },
        ],
    },
    "Tools  &  Downloads": {
        "icon": "⬇",
        "tweaks": [
            {
                "name": "Install 7-Zip",
                "desc": "Best open-source archive manager. Handles ZIP, RAR, 7z, TAR and more.",
                "risk": SAFE,
                "cmds": ['winget install --id 7zip.7zip --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Everything (Voidtools)",
                "desc": "Instant file search for Windows. Indexes your entire drive in seconds.",
                "risk": SAFE,
                "cmds": ['winget install --id voidtools.Everything --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install PowerToys",
                "desc": "Microsoft utilities: FancyZones, Color Picker, PowerRename and more.",
                "risk": SAFE,
                "cmds": ['winget install --id Microsoft.PowerToys --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install HWiNFO",
                "desc": "Most comprehensive hardware monitoring tool. Real-time sensors.",
                "risk": SAFE,
                "cmds": ['winget install --id REALiX.HWiNFO --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install CPU-Z",
                "desc": "Lightweight CPU identification and benchmarking tool.",
                "risk": SAFE,
                "cmds": ['winget install --id CPUID.CPU-Z --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install GPU-Z",
                "desc": "GPU identification and monitoring tool by TechPowerUp.",
                "risk": SAFE,
                "cmds": ['winget install --id TechPowerUp.GPU-Z --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Process Explorer",
                "desc": "Sysinternals advanced task manager. DLL handles, process trees, GPU usage.",
                "risk": SAFE,
                "cmds": ['winget install --id Microsoft.Sysinternals.ProcessExplorer --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Autoruns",
                "desc": "Sysinternals startup manager. Shows every auto-start entry in your system.",
                "risk": SAFE,
                "cmds": ['winget install --id Microsoft.Sysinternals.Autoruns --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install WizTree",
                "desc": "Fastest disk space analyzer. Uses MFT to scan in seconds. Underrated gem.",
                "risk": SAFE,
                "cmds": ['winget install --id AntibodySoftware.WizTree --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install MSI Afterburner",
                "desc": "GPU overclocking, undervolting and real-time OSD overlay for games.",
                "risk": SAFE,
                "cmds": ['winget install --id Guru3D.Afterburner --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install NVCleanstall",
                "desc": "Clean NVIDIA driver installer. Strips telemetry and bloat. Installs only what you need.",
                "risk": SAFE,
                "cmds": ['winget install --id TechPowerUp.NVCleanstall --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Bulk Crap Uninstaller",
                "desc": "Mass uninstaller. Finds leftover files, registry entries and orphan folders.",
                "risk": SAFE,
                "cmds": ['winget install --id Klocman.BulkCrapUninstaller --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install ShareX",
                "desc": "Screenshot and screen recording tool with auto-upload, annotation and OCR.",
                "risk": SAFE,
                "cmds": ['winget install --id ShareX.ShareX --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Notepad++",
                "desc": "Powerful text editor with syntax highlighting, regex and plugins.",
                "risk": SAFE,
                "cmds": ['winget install --id Notepad++.Notepad++ --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Rufus",
                "desc": "Create bootable USB drives from ISOs. Supports UEFI, GPT, MBR.",
                "risk": SAFE,
                "cmds": ['winget install --id Rufus.Rufus --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install CrystalDiskInfo",
                "desc": "S.M.A.R.T. disk health monitor. Warns before drive failure.",
                "risk": SAFE,
                "cmds": ['winget install --id CrystalDewWorld.CrystalDiskInfo --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install CrystalDiskMark",
                "desc": "SSD/HDD speed benchmark. Test sequential and random read/write.",
                "risk": SAFE,
                "cmds": ['winget install --id CrystalDewWorld.CrystalDiskMark --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install HWMonitor",
                "desc": "Real-time temperature, voltage and fan speed monitor by CPUID.",
                "risk": SAFE,
                "cmds": ['winget install --id CPUID.HWMonitor --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install UniGetUI",
                "desc": "GUI for winget, scoop, chocolatey, npm and pip in one place.",
                "risk": SAFE,
                "cmds": ['winget install --id MartiCliment.UniGetUI --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Ventoy",
                "desc": "Multi-boot USB. Drop ISOs on the drive, no reformatting needed.",
                "risk": SAFE,
                "cmds": ['winget install --id Ventoy.Ventoy --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Flow Launcher",
                "desc": "Spotlight-like quick launcher. Search apps, files, web from Alt+Space.",
                "risk": SAFE,
                "cmds": ['winget install --id Flow-Launcher.Flow-Launcher --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install EarTrumpet",
                "desc": "Per-app volume control from system tray. Better than Windows mixer.",
                "risk": SAFE,
                "cmds": ['winget install --id File-New-Project.EarTrumpet --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install TCPView",
                "desc": "Sysinternals real-time network connections viewer. Find what phones home.",
                "risk": SAFE,
                "cmds": ['winget install --id Microsoft.Sysinternals.TCPView --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install O&O ShutUp10++",
                "desc": "Ultimate Windows privacy tool. Toggle 150+ telemetry settings in one click.",
                "risk": SAFE,
                "cmds": ['winget install --id OandO.ShutUp10 --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Process Monitor",
                "desc": "Sysinternals deep system tracer. Logs every file, registry, network op.",
                "risk": SAFE,
                "cmds": ['winget install --id Microsoft.Sysinternals.ProcessMonitor --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Revo Uninstaller",
                "desc": "Deep uninstaller. Finds leftover files/registry after normal uninstall.",
                "risk": SAFE,
                "cmds": ['winget install --id RevoUninstaller.RevoUninstaller --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Snappy Driver Installer",
                "desc": "Offline driver updater with massive driver packs. No internet needed.",
                "risk": SAFE,
                "cmds": ['winget install --id GlennDelahoy.SnappyDriverInstallerOrigin --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install ExplorerPatcher",
                "desc": "Restore Windows 10 taskbar/start menu on Win11. Fix every Win11 regression.",
                "risk": SAFE,
                "cmds": ['winget install --id valinet.ExplorerPatcher --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install QuickLook",
                "desc": "Press Spacebar to preview any file in Explorer. Like macOS Quick Look.",
                "risk": SAFE,
                "cmds": ['winget install --id QL-Win.QuickLook --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Ditto Clipboard",
                "desc": "Clipboard history manager. Saves everything you copy. Search & pin.",
                "risk": SAFE,
                "cmds": ['winget install --id Ditto.Ditto --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install LatencyMon",
                "desc": "DPC latency monitor. Finds which driver causes audio/input lag spikes.",
                "risk": SAFE,
                "cmds": ['winget install --id Resplendence.LatencyMon --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Process Lasso",
                "desc": "Auto process priority/affinity optimizer. Prevents stuttering and hangs.",
                "risk": SAFE,
                "cmds": ['winget install --id BitSum.ProcessLasso --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install ParkControl",
                "desc": "CPU core parking control. Prevents cores from sleeping during games.",
                "risk": SAFE,
                "cmds": ['winget install --id BitSum.ParkControl --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install ThrottleStop",
                "desc": "Intel CPU undervolt, throttle bypass, turbo control. Advanced.",
                "risk": SAFE,
                "cmds": ['winget install --id TechPowerUp.ThrottleStop --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install RTSS",
                "desc": "Frame limiter with lowest latency. OSD overlay for FPS/frametime.",
                "risk": SAFE,
                "cmds": ['winget install --id Guru3D.RTSS --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install CapFrameX",
                "desc": "Frame time analysis and benchmarking. Detect stutters invisible to FPS counters.",
                "risk": SAFE,
                "cmds": ['winget install --id CXWorld.CapFrameX --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install DDU",
                "desc": "Clean GPU driver removal. Essential before fresh driver install.",
                "risk": SAFE,
                "cmds": ['winget install --id Wagnardsoft.DisplayDriverUninstaller --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Sysmon",
                "desc": "Advanced system monitor. Logs process creation, network connections, file changes.",
                "risk": SAFE,
                "cmds": ['winget install --id Microsoft.Sysinternals.Sysmon --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Sophia Script",
                "desc": "The most advanced Windows tweaking script. 150+ configurable optimizations.",
                "risk": SAFE,
                "cmds": ['winget install --id TeamSophia.SophiaScript --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install privacy.sexy",
                "desc": "Privacy hardening script generator. Pick tweaks, generate .bat/.ps1.",
                "risk": SAFE,
                "cmds": ['winget install --id undergroundwires.privacy.sexy --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install simplewall",
                "desc": "Lightweight Windows firewall configurator. Block anything phoning home.",
                "risk": SAFE,
                "cmds": ['winget install --id Henry++.simplewall --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Portmaster",
                "desc": "Application firewall with DNS privacy. Block trackers system-wide.",
                "risk": SAFE,
                "cmds": ['winget install --id Safing.Portmaster --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Mem Reduct",
                "desc": "Real-time memory cleaner. Purge standby list to prevent stuttering.",
                "risk": SAFE,
                "cmds": ['winget install --id Henry++.MemReduct --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install CRU",
                "desc": "Create custom resolutions and refresh rates. Unlock hidden display modes.",
                "risk": SAFE,
                "cmds": ['winget install --id ToastyX.CustomResolutionUtility --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install CompactGUI",
                "desc": "NTFS compression for games. Save 50%+ space with zero performance hit.",
                "risk": SAFE,
                "cmds": ['winget install --id IridiumIO.CompactGUI --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install GlassWire",
                "desc": "Beautiful network monitor. See what apps use bandwidth in real-time.",
                "risk": SAFE,
                "cmds": ['winget install --id GlassWire.GlassWire --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install WPD",
                "desc": "Windows Privacy Dashboard. Disable telemetry, blocker, firewall rules.",
                "risk": SAFE,
                "cmds": ['winget install --id WPD.WPD --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install LosslessCut",
                "desc": "Instant lossless video trimming. Cut without re-encoding. Saves hours.",
                "risk": SAFE,
                "cmds": ['winget install --id ch.LosslessCut --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install AutoHotkey",
                "desc": "Automation scripting for Windows. Remap keys, macros, hotstrings.",
                "risk": SAFE,
                "cmds": ['winget install --id AutoHotkey.AutoHotkey --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install WizFile",
                "desc": "Instant file search using MFT. Finds any file in milliseconds.",
                "risk": SAFE,
                "cmds": ['winget install --id AntibodySoftware.WizFile --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install dupeGuru",
                "desc": "Duplicate file finder. Find and delete wasted space from duplicates.",
                "risk": SAFE,
                "cmds": ['winget install --id DupeGuru.DupeGuru --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install FanControl",
                "desc": "Custom fan curves for any fan/sensor combo. Open-source.",
                "risk": SAFE,
                "cmds": ['winget install --id Rem0o.FanControl --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install OpenRGB",
                "desc": "Universal RGB controller. One app for ALL RGB brands. Kill iCUE/Aura/etc.",
                "risk": SAFE,
                "cmds": ['winget install --id OpenRGB.OpenRGB --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install LibreHardwareMonitor",
                "desc": "Open-source hardware monitor. API for custom dashboards/widgets.",
                "risk": SAFE,
                "cmds": ['winget install --id LibreHardwareMonitor.LibreHardwareMonitor --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install BlueScreenView",
                "desc": "BSOD crash dump analyzer. See which driver crashed your PC.",
                "risk": SAFE,
                "cmds": ['winget install --id NirSoft.BlueScreenView --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install ShellExView",
                "desc": "See/disable ALL right-click menu extensions. Fix slow right-click.",
                "risk": SAFE,
                "cmds": ['winget install --id NirSoft.ShellExView --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install AppReadWriteCounter",
                "desc": "Shows which apps read/write the most to your SSD. Find I/O hogs.",
                "risk": SAFE,
                "cmds": ['winget install --id NirSoft.AppReadWriteCounter --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install SoundVolumeView",
                "desc": "Advanced per-app audio routing. Route any app to any audio device.",
                "risk": SAFE,
                "cmds": ['winget install --id NirSoft.SoundVolumeView --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install FullEventLogView",
                "desc": "Better Event Viewer. All Windows logs in one table with filtering.",
                "risk": SAFE,
                "cmds": ['winget install --id NirSoft.FullEventLogView --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Dependencies",
                "desc": "Modern DLL dependency viewer. Debug missing DLL errors instantly.",
                "risk": SAFE,
                "cmds": ['winget install --id lucasg.Dependencies --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Resource Hacker",
                "desc": "View/edit resources inside .exe files. Icons, dialogs, strings, bitmaps.",
                "risk": SAFE,
                "cmds": ['winget install --id AngusJohnson.ResourceHacker --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install x64dbg",
                "desc": "x64/x32 debugger. The modern OllyDbg. For reverse engineering.",
                "risk": SAFE,
                "cmds": ['winget install --id x64dbg.x64dbg --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install MacType",
                "desc": "macOS-quality font rendering on Windows. Text looks DRAMATICALLY better.",
                "risk": SAFE,
                "cmds": ['winget install --id MacType.MacType --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install TranslucentTB",
                "desc": "Transparent/acrylic/blurred taskbar. Tiny, clean, does one thing perfectly.",
                "risk": SAFE,
                "cmds": ['winget install --id CharlesMilette.TranslucentTB --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install ModernFlyouts",
                "desc": "Replace ugly Win volume/brightness popups with modern beautiful ones.",
                "risk": SAFE,
                "cmds": ['winget install --id ModernFlyouts.ModernFlyouts --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install DevToys",
                "desc": "Swiss army knife for devs. Base64, JSON, hash, regex, UUID — all offline.",
                "risk": SAFE,
                "cmds": ['winget install --id DevToys-app.DevToys --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install GlazeWM",
                "desc": "Tiling window manager for Windows. Like i3wm but for Windows.",
                "risk": SAFE,
                "cmds": ['winget install --id glzr-io.glazewm --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install NanaZip",
                "desc": "Modern 7-Zip fork. Win11 integration, Zstandard support, ARM64.",
                "risk": SAFE,
                "cmds": ['winget install --id M2Team.NanaZip --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Bulk Rename Utility",
                "desc": "Mass file renamer. Regex, numbering, case, dates. The most powerful ever.",
                "risk": SAFE,
                "cmds": ['winget install --id TGRMNSoftware.BulkRenameUtility --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install privacy.sexy",
                "desc": "Script generator for 300+ Windows privacy tweaks. Fully auditable.",
                "risk": SAFE,
                "cmds": ['winget install --id undergroundwires.privacy.sexy --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install AltSnap",
                "desc": "Alt+drag to move/resize ANY window. Linux-style window management.",
                "risk": SAFE,
                "cmds": ['winget install --id AltSnap.AltSnap --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install SoundSwitch",
                "desc": "Switch audio output device with a hotkey. Headphones ↔ speakers instantly.",
                "risk": SAFE,
                "cmds": ['winget install --id AntoineAflalo.SoundSwitch --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install TrafficMonitor",
                "desc": "Network speed + CPU + RAM in your taskbar. Real-time mini-monitor.",
                "risk": SAFE,
                "cmds": ['winget install --id zhongyang219.TrafficMonitor.Full --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Twinkle Tray",
                "desc": "Control external monitor brightness from taskbar via DDC/CI.",
                "risk": SAFE,
                "cmds": ['winget install --id xanderfrangos.twinkletray --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install SuperF4",
                "desc": "Ctrl+Alt+F4 force kills ANY frozen app. No 'not responding' wait.",
                "risk": SAFE,
                "cmds": ['winget install --id StefanSundin.Superf4 --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install System Informer",
                "desc": "Process Hacker successor. Makes Task Manager look like a toy.",
                "risk": SAFE,
                "cmds": ['winget install --id WinsiderSS.SystemInformer --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install RegCool",
                "desc": "Advanced registry editor. Multi-tab, undo, compare, search & replace.",
                "risk": SAFE,
                "cmds": ['winget install --id KurtZimmermann.RegCool --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Czkawka",
                "desc": "Ultra-fast duplicate finder written in Rust. Finds similar images too.",
                "risk": SAFE,
                "cmds": ['winget install --id qarmin.czkawka.gui --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install dnSpy",
                "desc": ".NET assembly editor/debugger/decompiler. Edit .NET DLLs live.",
                "risk": SAFE,
                "cmds": ['winget install --id dnSpyEx.dnSpy --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install PE-bear",
                "desc": "PE file analyzer. Inspect exe/dll headers, sections, imports.",
                "risk": SAFE,
                "cmds": ['winget install --id hasherezade.PE-bear --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Espanso",
                "desc": "Text expander. Type :email → expands to your@email.com. Written in Rust.",
                "risk": SAFE,
                "cmds": ['winget install --id Espanso.Espanso --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Monitorian",
                "desc": "External monitor brightness control via DDC/CI. Multi-monitor slider.",
                "risk": SAFE,
                "cmds": ['winget install --id emoacht.Monitorian --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install LocalSend",
                "desc": "AirDrop for Windows/Android/iOS. Transfer files over local network.",
                "risk": SAFE,
                "cmds": ['winget install --id LocalSend.LocalSend --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install NTLite",
                "desc": "Windows ISO customizer. Remove bloatware BEFORE installing Windows.",
                "risk": SAFE,
                "cmds": ['winget install --id Nlitesoft.NTLite --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install WinSetView",
                "desc": "Set default Explorer view permanently. Stop Explorer resetting your views.",
                "risk": SAFE,
                "cmds": ['winget install --id LesFerch.WinSetView --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install ScreenToGif",
                "desc": "Record screen as GIF/APNG/video. Tiny editor with frame-by-frame editing.",
                "risk": SAFE,
                "cmds": ['winget install --id NickeManarin.ScreenToGif --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install WinMerge",
                "desc": "File/folder comparison & merge. See differences side-by-side.",
                "risk": SAFE,
                "cmds": ['winget install --id WinMerge.WinMerge --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install carnac",
                "desc": "Shows keyboard shortcuts on-screen as you type. Perfect for streaming.",
                "risk": SAFE,
                "cmds": ['winget install --id code52.Carnac --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Flameshot",
                "desc": "Screenshot tool with instant annotation. Arrows, blur, text, shapes.",
                "risk": SAFE,
                "cmds": ['winget install --id Flameshot.Flameshot --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Qalculate!",
                "desc": "Most powerful calculator ever. Unit conversions, symbolic math, plots.",
                "risk": SAFE,
                "cmds": ['winget install --id Qalculate.Qalculate --accept-package-agreements --accept-source-agreements -h'],
            },            {
                "name": "Install Quick CPU",
                "desc": "CPU core parking, frequency scaling, turbo, power management tuner.",
                "risk": SAFE,
                "cmds": ['winget install --id CoderBag.QuickCPUx64 --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Special K",
                "desc": "Frame pacing fixer, latency reducer, HDR retrofit for games.",
                "risk": SAFE,
                "cmds": ['winget install --id SpecialK.SpecialK --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Intel PresentMon",
                "desc": "GPU/CPU frametime & latency analysis tool by Intel.",
                "risk": SAFE,
                "cmds": ['winget install --id Intel.PresentMon --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install NVIDIA FrameView",
                "desc": "Frametime benchmarking & GPU power measurement tool.",
                "risk": SAFE,
                "cmds": ['winget install --id Nvidia.FrameView --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install AMD OCAT",
                "desc": "Open Capture & Analytics Tool. Frametime capture & analysis.",
                "risk": SAFE,
                "cmds": ['winget install --id AMD.OCAT --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install BenchMate",
                "desc": "Anti-cheat benchmarking validator for overclocking competitions.",
                "risk": SAFE,
                "cmds": ['winget install --id MatthiasZronek.BenchMate --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Intel XTU",
                "desc": "Intel CPU overclocking, undervolting & stress testing utility.",
                "risk": SAFE,
                "cmds": ['winget install --id Intel.IntelExtremeTuningUtility --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install UXTU",
                "desc": "Universal x86 Tuning Utility — AMD/Intel CPU power tuning.",
                "risk": SAFE,
                "cmds": ['winget install --id JamesCJ60.Universalx86TuningUtility --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install TweakPower",
                "desc": "All-in-one Windows tuning & cleanup suite. Niche German tool.",
                "risk": SAFE,
                "cmds": ['winget install --id KurtZimmermann.TweakPower --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install NetLimiter",
                "desc": "Per-process network bandwidth limiter. Control latency per app.",
                "risk": SAFE,
                "cmds": ['winget install --id LocktimeSoftware.NetLimiter --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install ASIO4ALL",
                "desc": "Universal ASIO driver. Ultra-low audio latency on any sound card.",
                "risk": SAFE,
                "cmds": ['winget install --id MichaelTippach.ASIO4ALL --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install REAL",
                "desc": "Reduce audio latency on Windows. Patches audio pipeline.",
                "risk": SAFE,
                "cmds": ['winget install --id MiniantGit.REAL --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Core-to-Core Latency",
                "desc": "Test CPU core-to-core latency in nanoseconds. Cache topology tool.",
                "risk": SAFE,
                "cmds": ['winget install --id KCORES.core-to-core-latency-plus --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Processes Priority Mgr",
                "desc": "Set PERMANENT process CPU priorities & affinities. Survives reboots.",
                "risk": SAFE,
                "cmds": ['winget install --id ArturKharin.ProcessesPriorityManager --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install RAMMap",
                "desc": "Physical memory analysis — standby list, page tables, mapped files.",
                "risk": SAFE,
                "cmds": ['winget install --id Microsoft.Sysinternals.RAMMap --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Windows Memory Cleaner",
                "desc": "Free standby list & working set memory. Lightweight ISLC alternative.",
                "risk": SAFE,
                "cmds": ['winget install --id IgorMundstein.WinMemoryCleaner --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install DiskCountersView",
                "desc": "Live disk read/write performance counters per drive.",
                "risk": SAFE,
                "cmds": ['winget install --id NirSoft.DiskCountersView --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install NetworkCountersWatch",
                "desc": "Live network performance counters per adapter.",
                "risk": SAFE,
                "cmds": ['winget install --id NirSoft.NetworkCountersWatch --accept-package-agreements --accept-source-agreements -h'],
            },

            {
                "name": "Install Windhawk",
                "desc": "Windows modding framework. Inject community mods to fix anything.",
                "risk": SAFE,
                "cmds": ['winget install --id RamenSoftware.Windhawk --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Nilesoft Shell",
                "desc": "Complete right-click context menu replacement. Custom commands & icons.",
                "risk": SAFE,
                "cmds": ['winget install --id Nilesoft.Shell --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Seelen UI",
                "desc": "Full desktop environment overhaul: tiling WM + taskbar + launcher.",
                "risk": SAFE,
                "cmds": ['winget install --id Seelen.SeelenUI --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install komorebi",
                "desc": "Rust-based tiling window manager. i3/bspwm-style automatic tiling.",
                "risk": SAFE,
                "cmds": ['winget install --id LGUG2Z.komorebi --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Textify",
                "desc": "Copy text from ANY window or dialog, even un-selectable text.",
                "risk": SAFE,
                "cmds": ['winget install --id rammichael.Textify --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Sizer",
                "desc": "Resize any window to exact pixel dimensions via right-click.",
                "risk": SAFE,
                "cmds": ['winget install --id BrianApps.Sizer --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install ZoomIt",
                "desc": "Screen zoom, draw & annotate for presentations. Timer countdown.",
                "risk": SAFE,
                "cmds": ['winget install --id Microsoft.Sysinternals.ZoomIt --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install scrcpy",
                "desc": "Mirror & control Android phone from PC. USB or WiFi. Sub-100ms.",
                "risk": SAFE,
                "cmds": ['winget install --id Genymobile.scrcpy --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install WhatIsHang",
                "desc": "Diagnose WHY a program is frozen. Shows stuck DLL/function.",
                "risk": SAFE,
                "cmds": ['winget install --id NirSoft.WhatIsHang --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install SophiApp",
                "desc": "GUI for Sophia Script. Debloat & configure Windows with checkboxes.",
                "risk": SAFE,
                "cmds": ['winget install --id TeamSophia.SophiApp --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install O&O AppBuster",
                "desc": "One-click removal of all preinstalled Windows bloatware apps.",
                "risk": SAFE,
                "cmds": ['winget install --id OO-Software.AppBuster --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install BleachBit",
                "desc": "Open-source disk cleaner. The CCleaner that isn't adware.",
                "risk": SAFE,
                "cmds": ['winget install --id BleachBit.BleachBit --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install SharpKeys",
                "desc": "Remap keyboard keys at registry level. No background process needed.",
                "risk": SAFE,
                "cmds": ['winget install --id RandyRants.SharpKeys --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install ContextMenuManager",
                "desc": "See & manage every right-click context menu entry on your system.",
                "risk": SAFE,
                "cmds": ['winget install --id BluePointLilac.ContextMenuManager --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Sandboxie-Plus",
                "desc": "Run any app in an isolated sandbox. Test suspicious software safely.",
                "risk": SAFE,
                "cmds": ['winget install --id Sandboxie.Plus --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Lively Wallpaper",
                "desc": "Animated desktop wallpapers — videos, GIFs, webpages. GPU-accelerated.",
                "risk": SAFE,
                "cmds": ['winget install --id rocksdanister.LivelyWallpaper --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install QTTabBar",
                "desc": "Adds folder tabs to Windows Explorer. Tab browsing for files.",
                "risk": SAFE,
                "cmds": ['winget install --id QTTabBar.QTTabBar --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install PatchCleaner",
                "desc": "Remove orphaned Windows Installer patches. Recover 5-30GB disk space.",
                "risk": SAFE,
                "cmds": ['winget install --id HomeDev.PatchCleanerPortable --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install SpaceSniffer",
                "desc": "Visual treemap disk space analyzer. Instant disk usage visualization.",
                "risk": SAFE,
                "cmds": ['winget install --id UderzoSoftware.SpaceSniffer --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install DNS Jumper",
                "desc": "Test & switch DNS servers instantly. Find fastest DNS one-click.",
                "risk": SAFE,
                "cmds": ['winget install --id sordum.DnsJumper --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install OpenHashTab",
                "desc": "Adds hash verification tab to file Properties. SHA256/MD5 right-click.",
                "risk": SAFE,
                "cmds": ['winget install --id namazso.OpenHashTab --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install USBDeview",
                "desc": "Shows all USB devices ever connected. Remove old drivers & see serials.",
                "risk": SAFE,
                "cmds": ['winget install --id NirSoft.USBDeview --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install OCCT",
                "desc": "All-in-one stability testing: CPU, GPU, RAM, PSU stress tests with error detection.",
                "risk": SAFE,
                "cmds": ['winget install --id OCBase.OCCT.Personal --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install FurMark",
                "desc": "Brutal GPU stress test — pushes graphics card to max power & temperature.",
                "risk": SAFE,
                "cmds": ['winget install --id Geeks3D.FurMark.2 --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Core Temp",
                "desc": "Lightweight per-core CPU temperature monitor in the system tray.",
                "risk": SAFE,
                "cmds": ['winget install --id ALCPU.CoreTemp --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install AIDA64",
                "desc": "Comprehensive hardware info, benchmarks & sensor monitoring tool.",
                "risk": SAFE,
                "cmds": ['winget install --id FinalWire.AIDA64.Engineer --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install KeePassXC",
                "desc": "Open-source offline password manager — your vault stays on your device.",
                "risk": SAFE,
                "cmds": ['winget install --id KeePassXCTeam.KeePassXC --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Bitwarden",
                "desc": "Free open-source password manager with cloud sync across all devices.",
                "risk": SAFE,
                "cmds": ['winget install --id Bitwarden.Bitwarden --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Malwarebytes",
                "desc": "Industry-leading malware scanner. Catches threats Defender misses.",
                "risk": SAFE,
                "cmds": ['winget install --id Malwarebytes.Malwarebytes --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Brave Browser",
                "desc": "Privacy-focused Chromium browser with built-in ad & tracker blocking.",
                "risk": SAFE,
                "cmds": ['winget install --id Brave.Brave --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Wireshark",
                "desc": "Network protocol analyzer — capture & inspect every packet on your network.",
                "risk": SAFE,
                "cmds": ['winget install --id WiresharkFoundation.Wireshark --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install WinDirStat",
                "desc": "Visual disk space analyzer with colorful treemap to find space hogs.",
                "risk": SAFE,
                "cmds": ['winget install --id WinDirStat.WinDirStat --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install FastCopy",
                "desc": "Fastest file copy/move tool for Windows — 2-3x faster than Explorer.",
                "risk": SAFE,
                "cmds": ['winget install --id FastCopy.FastCopy --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install TreeSize Free",
                "desc": "Instant disk space analysis with folder-level breakdown sorted by size.",
                "risk": SAFE,
                "cmds": ['winget install --id JAMSoftware.TreeSize.Free --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install File Converter",
                "desc": "Right-click any file to convert — images, docs, audio, video formats.",
                "risk": SAFE,
                "cmds": ['winget install --id AdrienAllard.FileConverter --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Rainmeter",
                "desc": "Desktop customization platform — system stats, weather, widgets & skins.",
                "risk": SAFE,
                "cmds": ['winget install --id Rainmeter.Rainmeter --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Git",
                "desc": "World's most used version control system. Track code changes & collaborate.",
                "risk": SAFE,
                "cmds": ['winget install --id Git.Git --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Windows Terminal",
                "desc": "Modern tabbed terminal for PowerShell, CMD, WSL, SSH — GPU-accelerated.",
                "risk": SAFE,
                "cmds": ['winget install --id Microsoft.WindowsTerminal --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install PowerShell 7",
                "desc": "Cross-platform PowerShell on .NET — faster and more powerful than 5.1.",
                "risk": SAFE,
                "cmds": ['winget install --id Microsoft.PowerShell --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Postman",
                "desc": "API development & testing platform — send requests, inspect responses, automate.",
                "risk": SAFE,
                "cmds": ['winget install --id Postman.Postman --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install VLC",
                "desc": "Legendary open-source media player that plays everything — no codecs needed.",
                "risk": SAFE,
                "cmds": ['winget install --id VideoLAN.VLC --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install OBS Studio",
                "desc": "Free screen recording & live streaming — Twitch, YouTube, scenes, mixing.",
                "risk": SAFE,
                "cmds": ['winget install --id OBSProject.OBSStudio --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install HandBrake",
                "desc": "Open-source video transcoder — convert any video to MP4/MKV with HW encoding.",
                "risk": SAFE,
                "cmds": ['winget install --id HandBrake.HandBrake --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Audacity",
                "desc": "Free audio editor — multi-track editing, noise removal, effects, recording.",
                "risk": SAFE,
                "cmds": ['winget install --id Audacity.Audacity --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install GIMP",
                "desc": "Free image editor — the Photoshop alternative with layers, masks & filters.",
                "risk": SAFE,
                "cmds": ['winget install --id GIMP.GIMP.3 --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Obsidian",
                "desc": "Knowledge base & notes in local Markdown. Graph view, plugins, your files forever.",
                "risk": SAFE,
                "cmds": ['winget install --id Obsidian.Obsidian --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Joplin",
                "desc": "Open-source notes with end-to-end encryption and cloud sync. Markdown editor.",
                "risk": SAFE,
                "cmds": ['winget install --id Joplin.Joplin --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install KDE Connect",
                "desc": "Connect phone to PC wirelessly — clipboard, files, notifications, remote.",
                "risk": SAFE,
                "cmds": ['winget install --id KDE.KDEConnect --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Sumatra PDF",
                "desc": "Ultra-lightweight PDF reader — instant open, minimal RAM, also reads EPUB.",
                "risk": SAFE,
                "cmds": ['winget install --id SumatraPDF.SumatraPDF --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Kdenlive",
                "desc": "Free video editor — multi-track timeline, effects, transitions, proxy editing.",
                "risk": SAFE,
                "cmds": ['winget install --id KDE.Kdenlive --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install WireGuard",
                "desc": "Ultra-modern VPN protocol. Faster than OpenVPN/IPsec, minimal attack surface, built into Linux kernel.",
                "risk": SAFE,
                "cmds": ['winget install --id WireGuard.WireGuard --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Nmap",
                "desc": "Network discovery and security auditing tool. Port scanning, OS detection, service enumeration.",
                "risk": SAFE,
                "cmds": ['winget install --id Insecure.Nmap --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install HxD",
                "desc": "Fast hex editor for raw disk/RAM/file editing. Supports files of any size, data inspector, checksums.",
                "risk": SAFE,
                "cmds": ['winget install --id MHNexus.HxD --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install MediaInfo",
                "desc": "Displays codec, bitrate, resolution, and tag info for any media file. Essential for video encoding workflows.",
                "risk": SAFE,
                "cmds": ['winget install --id MediaArea.MediaInfo --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install WinSCP",
                "desc": "SFTP/FTP/SCP/S3/WebDAV file transfer client with integrated text editor and scripting support.",
                "risk": SAFE,
                "cmds": ['winget install --id WinSCP.WinSCP --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install PuTTY",
                "desc": "Classic SSH/Telnet/serial terminal client. Includes PuTTYgen for key generation and Pageant for SSH agent.",
                "risk": SAFE,
                "cmds": ['winget install --id PuTTY.PuTTY --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Clink",
                "desc": "Adds GNU Readline to cmd.exe — tab completion, persistent history, syntax coloring, Lua scripting.",
                "risk": SAFE,
                "cmds": ['winget install --id chrisant996.Clink --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install ImageGlass",
                "desc": "GPU-accelerated image viewer. Supports 80+ formats, fast startup, color management, slideshow.",
                "risk": SAFE,
                "cmds": ['winget install --id DuongDieuPhap.ImageGlass --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install foobar2000",
                "desc": "Audiophile music player. Gapless playback, ReplayGain, extensive plugin ecosystem, minimal CPU usage.",
                "risk": SAFE,
                "cmds": ['winget install --id PeterPawlowski.foobar2000 --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install MPC-HC",
                "desc": "Lightweight media player. Hardware decoding, HDR support, subtitle rendering, no bloat.",
                "risk": SAFE,
                "cmds": ['winget install --id clsid2.mpc-hc --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install yt-dlp",
                "desc": "Command-line video/audio downloader supporting 1000+ sites. Fork of youtube-dl with active development.",
                "risk": SAFE,
                "cmds": ['winget install --id yt-dlp.yt-dlp --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install MKVToolNix",
                "desc": "MKV muxer/demuxer — remux video streams, add/remove audio tracks and subtitles without re-encoding.",
                "risk": SAFE,
                "cmds": ['winget install --id MoritzBunkus.MKVToolNix --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install qBittorrent",
                "desc": "Open-source torrent client. No ads, sequential downloading, RSS feeds, IP filtering, web UI.",
                "risk": SAFE,
                "cmds": ['winget install --id qBittorrent.qBittorrent --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Paint.NET",
                "desc": "Fast image editor with layers, effects, plugins. Much lighter than Photoshop, much more capable than MS Paint.",
                "risk": SAFE,
                "cmds": ['winget install --id dotPDN.PaintDotNet --accept-package-agreements --accept-source-agreements -h'],
            },
            {
                "name": "Install Double Commander",
                "desc": "Dual-pane file manager inspired by Total Commander. Tabs, built-in viewer, FTP, archive support.",
                "risk": SAFE,
                "cmds": ['winget install --id alexx2000.DoubleCommander --accept-package-agreements --accept-source-agreements -h'],
            },
        ],
    },

}



# ═════════════════════════ Application Class ══════════════════════════
class OptimizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(_t("app_title", v=APP_VERSION))
        self.root.geometry("1400x900")
        self.root.minsize(900, 600)
        self.root.state('zoomed')

        # Apply custom icon if it exists
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            icon_path = os.path.join(sys._MEIPASS, "icon.ico")
        else:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
        
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception:
                pass

        self.root.configure(bg="#000000")

        # Track tweak state
        self.tweak_vars = {}   # tweak_name -> (BooleanVar, tweak_dict)
        self.tweak_applied_lbls = {} # tweak_name -> Label
        self.tooltip_win = None
        self.music_error = None    # Track music loading errors
        self.music_on = True       # Track music state
        self.initially_applied = set()  # Track tweaks detected as applied at startup
        self._applying = False  # Guard against double-click on EXECUTE
        self.rating_var = tk.IntVar(value=0)  # Star rating (visible on main page)

        self._build_ui_basic()
        self._play_music()

        # ── Show loading screen, then reveal main window once ready ──
        if SKIP_LOADING:
            self._load_specs()
            self.root.state('zoomed')
            threading.Thread(target=self._check_for_updates, daemon=True).start()
        else:
            self._show_loading_screen()

    # ══════════════════════ Loading / Splash Screen ═══════════════════════
    def _show_loading_screen(self):
        self.root.withdraw()

        splash = tk.Toplevel(self.root)
        splash.title("NormieTools // INITIALIZING")
        splash.overrideredirect(True)
        splash.configure(bg="#000000")
        splash.attributes("-topmost", True)

        sw, sh = 780, 420
        x = (splash.winfo_screenwidth() - sw) // 2
        y = (splash.winfo_screenheight() - sh) // 2
        splash.geometry(f"{sw}x{sh}+{x}+{y}")

        # Red border
        border = tk.Frame(splash, bg="#FF1A00", bd=0)
        border.pack(fill="both", expand=True, padx=2, pady=2)
        inner = tk.Frame(border, bg="#000000", bd=0)
        inner.pack(fill="both", expand=True, padx=1, pady=1)

        # Layout: left = animation, right = text/progress
        content = tk.Frame(inner, bg="#000000")
        content.pack(fill="both", expand=True, padx=10, pady=10)

        # LEFT: BMP animation panel
        anim_frame = tk.Frame(content, bg="#0A0A0A", highlightbackground="#FF1A00",
                              highlightthickness=1, width=170, height=320)
        anim_frame.pack(side="left", padx=(5, 15), pady=5)
        anim_frame.pack_propagate(False)

        # Load BMP animation frames
        self._splash_frames = []
        self._splash_frame_idx = 0
        try:
            from PIL import Image, ImageTk
            base = os.path.dirname(os.path.abspath(__file__))
            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                base = sys._MEIPASS
            for i in range(9):
                fp = os.path.join(base, f"bmp_anim1_{i}.bmp")
                if os.path.exists(fp):
                    img = Image.open(fp)
                    self._splash_frames.append(ImageTk.PhotoImage(img))
        except Exception:
            self._splash_frames = []

        self._anim_label = tk.Label(anim_frame, bg="#0A0A0A", bd=0)
        self._anim_label.pack(expand=True)
        if self._splash_frames:
            self._anim_label.configure(image=self._splash_frames[0])
        else:
            # Fallback: show styled text when BMP frames can't load
            self._anim_label.configure(
                text="N\nO\nR\nM\nI\nE",
                font=("Arial Black", 28), fg="#FF1A00", justify="center")

        # RIGHT: info panel
        right = tk.Frame(content, bg="#000000")
        right.pack(side="left", fill="both", expand=True)

        # Title
        tk.Label(right, text="NormieTools", font=("Arial Black", 20),
                 bg="#000000", fg="#FF1A00", anchor="w").pack(fill="x", pady=(5, 0))
        tk.Frame(right, bg="#FF1A00", height=2).pack(fill="x", pady=(2, 0))
        tk.Label(right, text="PC Optimizer  //  v" + APP_VERSION,
                 font=("Courier New", 9, "bold"),
                 bg="#000000", fg="#00DDFF", anchor="w").pack(fill="x", pady=(2, 8))

        # Terminal log (scrolling text feed)
        log_frame = tk.Frame(right, bg="#050505", highlightbackground="#222222",
                             highlightthickness=1, height=140)
        log_frame.pack(fill="x", pady=(0, 8))
        log_frame.pack_propagate(False)
        self._splash_log = tk.Text(log_frame, bg="#050505", fg="#00FF88",
                                   font=("Courier New", 8), relief="flat", bd=0,
                                   highlightthickness=0, state="disabled",
                                   wrap="none", padx=6, pady=4, cursor="arrow")
        self._splash_log.pack(fill="both", expand=True)
        self._splash_log.tag_configure("dim", foreground="#555555")
        self._splash_log.tag_configure("ok", foreground="#00FF88")
        self._splash_log.tag_configure("warn", foreground="#FFD700")
        self._splash_log.tag_configure("cmd", foreground="#00DDFF")
        self._splash_log.tag_configure("red", foreground="#FF1A00")

        # Status line
        status_var = tk.StringVar(value=">> INITIALIZING SUBSYSTEMS...")
        tk.Label(right, textvariable=status_var, font=("Courier New", 10, "bold"),
                 bg="#000000", fg="#888888", anchor="w").pack(fill="x", pady=(0, 4))

        # Progress bar
        bar_outer = tk.Frame(right, bg="#222222", height=16)
        bar_outer.pack(fill="x", pady=(0, 4))
        bar_outer.pack_propagate(False)
        bar_fill = tk.Frame(bar_outer, bg="#FF1A00", height=16, width=0)
        bar_fill.place(x=0, y=0, relheight=1)
        # Scan line overlay on progress bar
        self._splash_scan_line = tk.Frame(bar_outer, bg="#FFFFFF", width=2, height=16)
        self._splash_scan_line.place(x=0, y=0, relheight=1)
        self._splash_scan_pos = 0

        # Bottom info
        bottom_info = tk.Frame(right, bg="#000000")
        bottom_info.pack(fill="x")
        pct_var = tk.StringVar(value="0%")
        tk.Label(bottom_info, textvariable=pct_var, font=("Courier New", 10, "bold"),
                 bg="#000000", fg="#FF1A00", anchor="w").pack(side="left")
        sub_var = tk.StringVar(value="warming up subsystems...")
        tk.Label(bottom_info, textvariable=sub_var, font=("Courier New", 8),
                 bg="#000000", fg="#555555", anchor="e").pack(side="right")

        # Branding
        tk.Label(right, text="tools by MedCherif", font=("Courier New", 8),
                 bg="#000000", fg="#333333", anchor="e").pack(fill="x", pady=(4, 0))

        self._splash = splash
        self._splash_status = status_var
        self._splash_sub = sub_var
        self._splash_pct = pct_var
        self._splash_bar_fill = bar_fill
        self._splash_bar_width = bar_outer.winfo_reqwidth() or 540
        self._splash_bar_outer = bar_outer

        # Start animation loop
        if self._splash_frames:
            self._animate_splash()
        # Start scan line animation
        self._animate_scan_line()

        # Kick off loading
        threading.Thread(target=self._loading_worker, daemon=True).start()

    def _animate_splash(self):
        """Cycle BMP animation frames on the splash screen."""
        try:
            if not self._splash.winfo_exists():
                return
            self._splash_frame_idx = (self._splash_frame_idx + 1) % len(self._splash_frames)
            self._anim_label.configure(image=self._splash_frames[self._splash_frame_idx])
            self.root.after(120, self._animate_splash)
        except Exception:
            pass

    def _animate_scan_line(self):
        """Moving scan line on progress bar."""
        try:
            if not self._splash.winfo_exists():
                return
            w = self._splash_bar_outer.winfo_width()
            if w < 10:
                w = 540
            self._splash_scan_pos = (self._splash_scan_pos + 3) % w
            self._splash_scan_line.place(x=self._splash_scan_pos, y=0, relheight=1, width=2)
            self.root.after(20, self._animate_scan_line)
        except Exception:
            pass

    def _splash_log_append(self, text, tag="ok"):
        """Thread-safe append to splash terminal log."""
        def _do():
            try:
                t = self._splash_log
                t.config(state="normal")
                t.insert("end", text + "\n", tag)
                t.see("end")
                t.config(state="disabled")
            except Exception:
                pass
        self.root.after(0, _do)

    def _update_splash(self, status=None, sub=None, pct=None):
        """Thread-safe update of splash screen widgets."""
        if not hasattr(self, '_splash'):
            return
        def _do():
            try:
                if not self._splash.winfo_exists():
                    return
                if status is not None:
                    self._splash_status.set(status)
                if sub is not None:
                    self._splash_sub.set(sub)
                if pct is not None:
                    self._splash_pct.set(f"{int(pct)}%")
                    w = self._splash_bar_outer.winfo_width()
                    if w < 10:
                        w = 540
                    pw = int(w * pct / 100)
                    self._splash_bar_fill.place(x=0, y=0, relheight=1, width=pw)
            except Exception:
                pass
        self.root.after(0, _do)

    def _loading_worker(self):
        """Background thread: loads system state and populates tweak checkboxes."""
        from concurrent.futures import ThreadPoolExecutor

        self._splash_log_append("[SYS] NormieTools bootstrap sequence initiated", "cmd")
        self._splash_log_append(f"[SYS] version {APP_VERSION} | pid {os.getpid()}", "dim")
        self._update_splash(status=">> QUERYING SYSTEM STATE...", sub="parallel subsystem probe", pct=5)

        # ── Step 1+2: Run bcdedit + PowerShell IN PARALLEL for speed ──
        def _bcdedit_task():
            try:
                return subprocess.check_output(
                    "bcdedit /enum", shell=True, text=True,
                    creationflags=0x08000000, timeout=15
                ).lower()
            except Exception:
                return ""

        def _ps_task():
            try:
                ps_script = self._get_ps_scan_script()
                out = subprocess.check_output(
                    ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_script],
                    text=True, creationflags=0x08000000, timeout=35
                )
                return json.loads(out)
            except Exception:
                return {}

        self._splash_log_append("[CMD] bcdedit /enum", "cmd")
        self._splash_log_append("[CMD] powershell subsystem probe", "cmd")

        with ThreadPoolExecutor(max_workers=2) as pool:
            fut_bcd = pool.submit(_bcdedit_task)
            fut_ps = pool.submit(_ps_task)
            self._bcdedit_cache = fut_bcd.result()
            self._splash_log_append("[OK ] bcdedit cache loaded", "ok")
            self._update_splash(pct=25)
            self._custom_cache = fut_ps.result()
            self._splash_log_append("[OK ] powershell state captured", "ok")
            self._update_splash(pct=40)

        self._splash_log_append(f"[INF] cached keys: {len(self._custom_cache)}", "dim")
        self._update_splash(status=">> MATCHING TWEAK STATES...", sub="scanning tweak registry", pct=45)

        # ── Step 3: Walk tweaks and flag applied ones ──
        total_tweaks = sum(len(cd["tweaks"]) for cd in CATEGORIES.values())
        done = 0
        applied_count = 0
        for cat_name, cat_data in CATEGORIES.items():
            if "Tools" in cat_name and "Downloads" in cat_name:
                continue
            for tweak in cat_data["tweaks"]:
                custom_state = self._check_custom(tweak["name"])
                is_applied = False
                if custom_state is True:
                    is_applied = True
                elif custom_state is not False:
                    if self._is_tweak_applied(tweak["cmds"]):
                        is_applied = True
                if is_applied:
                    self.root.after(0, self._set_tweak_checked, tweak["name"])
                    applied_count += 1
                done += 1
                p = 45 + int(40 * done / max(total_tweaks, 1))
                if done % 10 == 0:
                    self._update_splash(pct=p)
            self._splash_log_append(f"[SCN] {cat_name.strip()}: scanned", "dim")
        self._update_splash(pct=85)
        self._splash_log_append(f"[OK ] {applied_count}/{total_tweaks} tweaks detected active", "ok")

        self._update_splash(status=">> LOADING SYSTEM SPECS...", sub="WMI hardware query", pct=88)
        self._splash_log_append("[CMD] WMI CIM query (hardware specs)", "cmd")

        # ── Step 4: Load specs ──
        self._load_specs()
        self._splash_log_append("[OK ] hardware specs loaded", "ok")
        self._update_splash(status=">> SYSTEM READY", sub="all subsystems nominal", pct=100)
        self._splash_log_append("[SYS] initialization complete", "ok")
        time.sleep(0.4)  # Brief pause so user sees 100%

        # ── Step 5: Check for updates in background (non-blocking) ──
        threading.Thread(target=self._check_for_updates, daemon=True).start()

        # ── Done — destroy splash and show main window ──
        def _reveal():
            try:
                self._splash.destroy()
                self._splash_frames.clear()  # Free BMP frame memory
            except Exception:
                pass
            self.root.deiconify()
            self.root.state('zoomed')
        self.root.after(0, _reveal)

    def _get_ps_scan_script(self):
        """Return the PowerShell script for the big state query."""
        return r"""
            $state = @{}
            try { $state.mmagent = [bool](Get-MMAgent).MemoryCompression } catch {}
            try { $state.cfg = ((Get-ProcessMitigation -System).CFG.Enable.ToString() -ne 'OFF') } catch {}
            try {
                $ifaces = Get-ChildItem 'HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces'
                $nagleOk = $false
                foreach ($i in $ifaces) {
                    $ack = Get-ItemProperty -Path $i.PSPath -Name 'TcpAckFrequency' -EA SilentlyContinue
                    $nd = Get-ItemProperty -Path $i.PSPath -Name 'TCPNoDelay' -EA SilentlyContinue
                    if ($ack -and $ack.TcpAckFrequency -eq 1 -and $nd -and $nd.TCPNoDelay -eq 1) { $nagleOk = $true; break }
                }
                $state.nagle = $nagleOk
            } catch {}
            try { $state.netbios = [bool](Get-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Services\NetBT\Parameters\Interfaces\*" -Name "NetbiosOptions" -EA SilentlyContinue | Where-Object { $_.NetbiosOptions -eq 2 }) } catch {}
            try { $state.lso = [bool]((Get-NetAdapterAdvancedProperty -EA SilentlyContinue | Where-Object RegistryKeyword -match 'LsoV2IPv[46]').RegistryValue -contains '0') } catch {}
            try { $state.rsc = [bool]((Get-NetAdapterRsc -EA SilentlyContinue | Where-Object IPv4Enabled -eq $true)) } catch {}
            try { $state.msi = [bool](Get-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Enum\*\*\*\Device Parameters\Interrupt Management\MessageSignaledInterruptProperties" -Name "MSISupported" -EA SilentlyContinue | Where-Object { $_.MSISupported -eq 1 }) } catch {}
            try { 
                $tcp = Get-NetTcpSetting -SettingName Internet -EA SilentlyContinue
                $state.rss = [bool](Get-NetAdapterRss -EA SilentlyContinue | Where-Object Enabled -eq $true)
                $state.heuristics = ($tcp.ScalingHeuristics -eq "Disabled")
                $state.timestamps = ($tcp.Timestamps -eq "Disabled")
                $state.ecn = ($tcp.EcnCapability -eq "Disabled")
                $state.cubic = ($tcp.CongestionProvider -eq "CUBIC")
            } catch {}
            try { $state.powerScheme = (powercfg /getactivescheme 2>$null) } catch {}
            try {
                $slOut = powercfg /q SCHEME_CURRENT SUB_SLEEP 29f6c1db-86da-48c5-9fdb-f2b67b1f44da 2>$null | Out-String
                $slHex = [regex]::Matches($slOut, ':\s*0x([0-9a-fA-F]+)')
                if ($slHex.Count -ge 2) { $state.sleepAC = [int]("0x" + $slHex[$slHex.Count - 2].Groups[1].Value) }
            } catch {}
            try {
                $mnOut = powercfg /q SCHEME_CURRENT 7516b95f-f776-4464-8c53-06167f40cc99 3c0bc021-c8a8-4e07-a973-6b14cbcb2b7e 2>$null | Out-String
                $mnHex = [regex]::Matches($mnOut, ':\s*0x([0-9a-fA-F]+)')
                if ($mnHex.Count -ge 2) { $state.monitorAC = [int]("0x" + $mnHex[$mnHex.Count - 2].Groups[1].Value) }
            } catch {}
            try {
                $dkOut = powercfg /q SCHEME_CURRENT 0012ee47-9041-4b5d-9b77-535fba8b1442 6738e2c4-e8a5-4a42-b16a-e040e769756e 2>$null | Out-String
                $dkHex = [regex]::Matches($dkOut, ':\s*0x([0-9a-fA-F]+)')
                if ($dkHex.Count -ge 2) { $state.diskAC = [int]("0x" + $dkHex[$dkHex.Count - 2].Groups[1].Value) }
            } catch {}
            try {
                $foText = netsh int tcp show global 2>$null | Out-String
                $state.fastOpen = ($foText -match '(?i)fast.?open\s*:\s*enabled|ouverture.rapide\s*:\s*activ')
            } catch {}
            try {
                $state.hibernation = (Test-Path "$env:SystemDrive\hiberfil.sys")
            } catch {}
            try {
                $teredoState = netsh interface teredo show state 2>$null | Out-String
                $isatapState = netsh interface isatap show state 2>$null | Out-String
                $s6to4 = netsh int ipv6 6to4 show state 2>$null | Out-String
                $state.ipv6tunnel = (($teredoState -match 'disabled|d.sactiv') -and ($isatapState -match 'disabled|d.sactiv') -and ($s6to4 -match 'disabled|d.sactiv'))
            } catch {}
            try {
                $wmmProps = Get-NetAdapterAdvancedProperty -EA SilentlyContinue | Where-Object RegistryKeyword -match 'WMM|uAPSD'
                $state.wmm = [bool]($wmmProps.RegistryValue -contains '0')
            } catch {}
            try {
                $eeeProps = Get-NetAdapterAdvancedProperty -EA SilentlyContinue | Where-Object RegistryKeyword -match 'EEE'
                $state.eee = [bool]($eeeProps.RegistryValue -contains '0')
            } catch {}
            try {
                $qosVal = Get-ItemProperty "HKLM:\SOFTWARE\Policies\Microsoft\Windows\Psched" -Name "NonBestEffortLimit" -EA SilentlyContinue
                $state.qos = ($qosVal.NonBestEffortLimit -eq 0)
            } catch {}
            try {
                $usbCtrl = Get-PnpDevice -Class USB -Status OK -EA SilentlyContinue | Where-Object {($_.Service -match 'xhci|ehci') -or ($_.FriendlyName -match 'Host Controller|xHCI|eHCI')}
                $usbOk = $true
                foreach ($u in $usbCtrl) {
                    $bp = "HKLM:\SYSTEM\CurrentControlSet\Enum\" + $u.InstanceId + "\Device Parameters"
                    $ep = Get-ItemProperty -Path $bp -Name 'EnhancedPowerManagementEnabled' -EA SilentlyContinue
                    $ss = Get-ItemProperty -Path $bp -Name 'SelectiveSuspendEnabled' -EA SilentlyContinue
                    if ($ep -and $ep.EnhancedPowerManagementEnabled -ne 0) { $usbOk = $false }
                    if ($ss -and $ss.SelectiveSuspendEnabled -ne 0) { $usbOk = $false }
                }
                $state.usbPowerSaving = $usbOk
            } catch {}
            try {
                $gpuDev = Get-PnpDevice -Class Display -Status OK -EA SilentlyContinue
                $gpuOk = $false
                foreach ($g in $gpuDev) {
                    $mp = "HKLM:\SYSTEM\CurrentControlSet\Enum\" + $g.InstanceId + "\Device Parameters\Interrupt Management\Affinity Policy"
                    $dp = Get-ItemProperty -Path $mp -Name 'DevicePriority' -EA SilentlyContinue
                    if ($dp -and $dp.DevicePriority -eq 3) { $gpuOk = $true }
                }
                $state.gpuMsiPriority = $gpuOk
            } catch {}
            try {
                $nicDev = Get-PnpDevice -Class Net -Status OK -EA SilentlyContinue
                $nicOk = $false
                foreach ($n in $nicDev) {
                    $mp = "HKLM:\SYSTEM\CurrentControlSet\Enum\" + $n.InstanceId + "\Device Parameters\Interrupt Management\Affinity Policy"
                    $dp = Get-ItemProperty -Path $mp -Name 'DevicePriority' -EA SilentlyContinue
                    if ($dp -and $dp.DevicePriority -eq 3) { $nicOk = $true }
                }
                $state.nicMsiPriority = $nicOk
            } catch {}
            try {
                $nvDev = Get-ChildItem "HKLM:\SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}" -EA SilentlyContinue
                $nvPstateOk = $false
                foreach ($d in $nvDev) {
                    $drv = (Get-ItemProperty $d.PSPath -Name 'DriverDesc' -EA SilentlyContinue).DriverDesc
                    if ($drv -match 'NVIDIA') {
                        $dp = (Get-ItemProperty $d.PSPath -Name 'DisableDynamicPstate' -EA SilentlyContinue).DisableDynamicPstate
                        if ($dp -eq 1) { $nvPstateOk = $true }
                    }
                }
                $state.nvPstate = $nvPstateOk
            } catch {}
            try {
                $sr = (Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\SystemRestore' -Name 'RPSessionInterval' -EA SilentlyContinue).RPSessionInterval
                $state.systemRestoreDisabled = ($sr -eq 0)
            } catch {}
            try {
                $vrrVal = (Get-ItemProperty 'HKCU:\SOFTWARE\Microsoft\DirectX\UserGpuPreferences' -Name 'DirectXUserGlobalSettings' -EA SilentlyContinue).DirectXUserGlobalSettings
                $state.vrr = ($vrrVal -match 'VRROptimizeEnable=0')
            } catch {}
            try {
                $fseVal = (Get-ItemProperty 'HKCU:\SOFTWARE\Microsoft\DirectX\UserGpuPreferences' -Name 'DirectXUserGlobalSettings' -EA SilentlyContinue).DirectXUserGlobalSettings
                $state.fse = ($fseVal -match 'SwapEffectUpgradeEnable=0')
            } catch {}
            try {
                $tasks = @(
                    '\Microsoft\Windows\Application Experience\Microsoft Compatibility Appraiser',
                    '\Microsoft\Windows\Application Experience\ProgramDataUpdater',
                    '\Microsoft\Windows\Application Experience\StartupAppTask',
                    '\Microsoft\Windows\Customer Experience Improvement Program\Consolidator',
                    '\Microsoft\Windows\Customer Experience Improvement Program\UsbCeip',
                    '\Microsoft\Windows\DiskDiagnostic\Microsoft-Windows-DiskDiagnosticDataCollector',
                    '\Microsoft\Windows\Windows Error Reporting\QueueReporting'
                )
                $ts = @{}
                foreach ($tn in $tasks) {
                    try {
                        $t = Get-ScheduledTask -TaskPath ($tn.Substring(0, $tn.LastIndexOf('\') + 1)) -TaskName ($tn.Split('\')[-1]) -EA SilentlyContinue
                        if ($t) { $ts[$tn] = $t.State.ToString() } else { $ts[$tn] = '' }
                    } catch { $ts[$tn] = '' }
                }
                $state.taskStates = $ts
            } catch {}
            try {
                $fsu = @{}
                $fsuOut = fsutil behavior query disablelastaccess 2>$null
                if ($fsuOut) { $fsu['disablelastaccess'] = $fsuOut }
                $fsuOut = fsutil behavior query disable8dot3 2>$null
                if ($fsuOut) { $fsu['disable8dot3'] = $fsuOut }
                $fsuOut = fsutil behavior query memoryusage 2>$null
                if ($fsuOut) { $fsu['memoryusage'] = $fsuOut }
                $state.fsutil = $fsu
            } catch {}
            ConvertTo-Json $state -Compress -Depth 3
            """

    # ═══════════════════ NormieTools PC Optimization UI ═══════════════════
    def _build_ui_basic(self):
        BG_COLOR = "#000000"
        PANEL_COLOR = "#050505"
        ACCENT_RED = "#FF1A00"
        ACCENT_CYAN = "#00DDFF"
        TEXT_MUTED = "#888888"
        
        self.root.configure(bg=BG_COLOR)

        # ════════════════════════ Top bar (App Header) ════════════════════════
        top = tk.Frame(self.root, bg=BG_COLOR, bd=0)
        top.pack(fill="x", pady=(10, 5))

        self.header_lbl = tk.Label(top, text=_t("header", v=APP_VERSION), font=("Arial Black", 14), bg=BG_COLOR, fg=ACCENT_RED)
        self.header_lbl.pack(side="left", padx=15, pady=4)

        # ── Music controls (button + animated now-playing marquee) ──
        music_frame = tk.Frame(top, bg=BG_COLOR)
        music_frame.pack(side="right", padx=15, pady=3)

        self.music_btn = tk.Button(music_frame, text=_t("audio_on"), font=("Courier New", 10, "bold"), bg=ACCENT_RED, fg=BG_COLOR, relief="flat", bd=0, activebackground=ACCENT_CYAN, activeforeground=BG_COLOR, command=self._toggle_music)
        self.music_btn.pack(side="left", ipadx=10)

        # Animated song name marquee
        self._song_name = "Dark Fantasy - shahi77"
        marquee_container = tk.Frame(music_frame, bg="#111111", highlightbackground=ACCENT_RED, highlightthickness=1, width=180, height=20)
        marquee_container.pack(side="left", padx=(6, 0))
        marquee_container.pack_propagate(False)
        self._marquee_canvas = tk.Canvas(marquee_container, bg="#111111", highlightthickness=0, height=18)
        self._marquee_canvas.pack(fill="both", expand=True)
        padded = f"  \u266B  NOW PLAYING: {self._song_name}  \u266B  "
        self._marquee_text_id = self._marquee_canvas.create_text(180, 9, text=padded, font=("Courier New", 8, "bold"), fill=ACCENT_CYAN, anchor="w")
        self._marquee_offset = 180
        self._marquee_paused = False
        self.root.after(50, self._animate_marquee)

        # Language selector
        lang_frame = tk.Frame(top, bg=BG_COLOR)
        lang_frame.pack(side="right", padx=5)
        self.lang_lbl = tk.Label(lang_frame, text=_t("lang_label"), font=("Courier New", 9, "bold"), bg=BG_COLOR, fg="#888888")
        self.lang_lbl.pack(side="left")
        self.lang_combo = tk.StringVar(value="English")
        lang_menu = tk.OptionMenu(lang_frame, self.lang_combo, *SUPPORTED_LANGS, command=self._on_lang_change)
        lang_menu.configure(font=("Courier New", 9), bg="#111111", fg="#00DDFF", highlightthickness=0, relief="flat", activebackground="#FF1A00")
        lang_menu["menu"].configure(bg="#111111", fg="#00DDFF", font=("Courier New", 9))
        lang_menu.pack(side="left", padx=4)

        # ”€”€ Star Rating (always visible on main page) + Feedback button ”€”€
        rate_area = tk.Frame(top, bg=BG_COLOR)
        rate_area.pack(side="right", padx=8, pady=2)

        self.star_labels = []
        for i in range(5):
            sl = tk.Label(rate_area, text="\u2606", font=("Arial", 20),
                          bg=BG_COLOR, fg="#444444", cursor="hand2")
            sl.pack(side="left", padx=1)
            self.star_labels.append(sl)

        def _set_star(n):
            self.rating_var.set(n)
            for j, sl in enumerate(self.star_labels):
                sl.configure(text="\u2605" if j < n else "\u2606",
                             fg="#FF8800" if j < n else "#444444")

        def _star_enter(n):
            for j, sl in enumerate(self.star_labels):
                sl.configure(fg="#FF8800" if j < n else "#444444")

        def _star_leave():
            cur = self.rating_var.get()
            for j, sl in enumerate(self.star_labels):
                sl.configure(fg="#FF8800" if j < cur else "#444444")

        for i in range(5):
            self.star_labels[i].bind("<Button-1>", lambda e, n=i+1: _set_star(n))
            self.star_labels[i].bind("<Enter>", lambda e, n=i+1: _star_enter(n))
            self.star_labels[i].bind("<Leave>", lambda e: _star_leave())

        # Highlighted FEEDBACK button
        self.fb_btn = tk.Button(rate_area, text=_t("feedback_btn"), font=("Arial Black", 10),
                           bg="#FF8800", fg="#000000", relief="flat", bd=0, cursor="hand2",
                           activebackground=ACCENT_CYAN, activeforeground="#000000",
                           command=self._show_feedback_dialog)
        self.fb_btn.pack(side="left", padx=(8, 0), ipadx=10, ipady=2)


        # -- Red scan line separator --
        scan_line = tk.Frame(self.root, bg=ACCENT_RED, height=2)
        scan_line.pack(fill="x", padx=10, pady=(0, 0))
        scan_shadow = tk.Frame(self.root, bg="#330800", height=1)
        scan_shadow.pack(fill="x", padx=10, pady=(0, 5))

        # ═══════════════ Body Minimalist Brutalist Split Screen ═══════════════
        paned = tk.PanedWindow(self.root, orient="horizontal", bg=ACCENT_RED, sashwidth=2, relief="flat")
        paned.pack(fill="both", expand=True, padx=10, pady=10)

        # Left: Specs (System Analysis)
        specs_frame = tk.Frame(paned, bg=PANEL_COLOR)
        self.specs_hdr = tk.Label(specs_frame, text=_t("specs_header"), font=("Arial Black", 10), bg=PANEL_COLOR, fg=ACCENT_RED, anchor="w")
        self.specs_hdr.pack(fill="x", padx=10, pady=(10, 0))
        tk.Frame(specs_frame, bg=ACCENT_RED, height=1).pack(fill="x", padx=10, pady=(2, 4))
        self.specs_text = tk.Text(
            specs_frame,
            font=("Courier New", 8),
            bg=PANEL_COLOR,
            fg=ACCENT_CYAN,
            relief="flat",
            bd=0,
            highlightthickness=0,
            state="disabled",
            wrap="none",
            padx=10,
            pady=10,
            cursor="arrow",
        )
        self.specs_text.pack(fill="both", expand=True)
        self._set_specs_text(_t("syncing"))

        # Right: Tweaks Grid (with scrollbar for small screens)
        tweaks_frame = tk.Frame(paned, bg=PANEL_COLOR)
        self.tweaks_hdr = tk.Label(tweaks_frame, text=_t("tweaks_header"), font=("Arial Black", 10), bg=PANEL_COLOR, fg=ACCENT_RED, anchor="w")
        self.tweaks_hdr.pack(fill="x", padx=10, pady=(10, 0))
        tk.Frame(tweaks_frame, bg=ACCENT_RED, height=1).pack(fill="x", padx=10, pady=(2, 4))

        # ════════════════════════ Scrollable container ════════════════════════

        # ── Tab bar (Tweaks vs Tools) ──
        tab_bar = tk.Frame(tweaks_frame, bg=PANEL_COLOR)
        tab_bar.pack(fill="x", padx=10, pady=(4, 2))
        
        self._tweaks_tab_btn = tk.Button(tab_bar, text="\U0001F527 TWEAKS", font=("Arial Black", 9),
            bg=ACCENT_RED, fg="#FFFFFF", relief="flat", bd=0, padx=12, pady=3,
            activebackground=ACCENT_RED, activeforeground="#FFFFFF",
            command=lambda: self._switch_tab("tweaks"))
        self._tweaks_tab_btn.pack(side="left", padx=(0, 4))
        
        self._tools_tab_btn = tk.Button(tab_bar, text="\u2B07 TOOLS", font=("Arial Black", 9),
            bg="#333333", fg="#888888", relief="flat", bd=0, padx=12, pady=3,
            activebackground=ACCENT_RED, activeforeground="#FFFFFF",
            command=lambda: self._switch_tab("tools"))
        self._tools_tab_btn.pack(side="left", padx=(0, 4))

        self._aihelp_tab_btn = tk.Button(tab_bar, text="\U0001F916 AI HELP", font=("Arial Black", 9),
            bg="#333333", fg="#888888", relief="flat", bd=0, padx=12, pady=3,
            activebackground=ACCENT_RED, activeforeground="#FFFFFF",
            command=lambda: self._switch_tab("aihelp"))
        self._aihelp_tab_btn.pack(side="left", padx=(0, 4))
        

        scroll_container = tk.Frame(tweaks_frame, bg=PANEL_COLOR)
        scroll_container.pack(fill="both", expand=True, padx=0, pady=0)

        self.tweaks_canvas = tk.Canvas(scroll_container, bg=PANEL_COLOR, highlightthickness=0, bd=0)
        tweaks_vscroll = tk.Scrollbar(scroll_container, orient="vertical", command=self.tweaks_canvas.yview)
        self.tweaks_canvas.configure(yscrollcommand=tweaks_vscroll.set)

        tweaks_vscroll.pack(side="right", fill="y")
        self.tweaks_canvas.pack(side="left", fill="both", expand=True)

        grid = tk.Frame(self.tweaks_canvas, bg=PANEL_COLOR)
        _cw = self.tweaks_canvas.create_window((0, 0), window=grid, anchor="nw")

        def _on_grid_cfg(e):
            self.tweaks_canvas.configure(scrollregion=self.tweaks_canvas.bbox("all"))
        def _on_canvas_cfg(e):
            self.tweaks_canvas.itemconfig(_cw, width=e.width)
        grid.bind("<Configure>", _on_grid_cfg)
        self.tweaks_canvas.bind("<Configure>", _on_canvas_cfg)

        def _on_tweaks_mousewheel(event):
            # Only scroll the tweaks canvas when the mouse is actually over it
            widget = event.widget
            try:
                # Walk up the widget tree to check if mouse is over the tweaks canvas or its children
                w = widget
                while w:
                    if w is self.tweaks_canvas or w is grid:
                        self.tweaks_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
                        return
                    w = w.master
            except Exception:
                pass
        self.tweaks_canvas.bind_all("<MouseWheel>", _on_tweaks_mousewheel)

        def risk_to_color(risk_tuple):
            try:
                risk_name = risk_tuple[0].upper()
                if "HIGH" in risk_name: return ACCENT_RED
                if "MEDIUM" in risk_name: return "#FF8800"
                return "#66BB6A"
            except Exception:
                return TEXT_MUTED

        def risk_to_text(risk_tuple):
            try:
                return f"[{risk_tuple[0].upper()}]"
            except Exception:
                return "[-]"

        self._cat_labels = {}
        self._tweak_chks = {}
        self._risk_labels = {}
        self._tool_name_lbls = {}
        self._tool_desc_lbls = {}
        for cat_name, cat_data in CATEGORIES.items():
            if "Tools" in cat_name and "Downloads" in cat_name:
                continue
            # Category header
            cat_hdr = tk.Frame(grid, bg=PANEL_COLOR)
            cat_hdr.pack(fill="x", padx=4, pady=(14, 4))
            cat_lbl = tk.Label(cat_hdr, text=f"// {_cat(cat_name).upper()}", font=("Arial Black", 9),
                     bg=PANEL_COLOR, fg=ACCENT_CYAN, anchor="w")
            cat_lbl.pack(side="left")
            self._cat_labels[cat_name] = cat_lbl
            tk.Label(cat_hdr, text=f"({len(cat_data['tweaks'])})", font=("Courier New", 8),
                     bg=PANEL_COLOR, fg=TEXT_MUTED, anchor="w").pack(side="left", padx=6)

            for tw in cat_data["tweaks"]:
                var = tk.BooleanVar(value=False)
                self.tweak_vars[tw["name"]] = (var, tw)

                # Full-width row for each tweak
                row = tk.Frame(grid, bg=PANEL_COLOR)
                row.pack(fill="x", padx=4, pady=1)

                # Left: checkbox with full name
                chk = tk.Checkbutton(
                    row,
                    variable=var,
                    text=_tn(tw["name"]),
                    font=("Courier New", 8, "bold"),
                    bg=PANEL_COLOR,
                    fg="#FFFFFF",
                    selectcolor=BG_COLOR,
                    activebackground=PANEL_COLOR,
                    activeforeground=ACCENT_RED,
                    anchor="w",
                    justify="left",
                    command=self._update_stats,
                )
                chk.pack(side="left", anchor="w")
                self._tweak_chks[tw["name"]] = chk

                # Tooltip on hover for tweak description
                _desc = tw.get("desc", "")
                if _desc:
                    _tip_color = risk_to_color(tw["risk"])
                    chk.bind("<Enter>", lambda e, n=tw["name"], c=_tip_color: self._show_tooltip(e, _td(n), c))
                    chk.bind("<Leave>", lambda e: self._hide_tooltip())
                    row.bind("<Enter>", lambda e, n=tw["name"], c=_tip_color: self._show_tooltip(e, _td(n), c))
                    row.bind("<Leave>", lambda e: self._hide_tooltip())

                # Right side: risk badge + applied status
                right_side = tk.Frame(row, bg=PANEL_COLOR)
                right_side.pack(side="right", padx=(4, 6))

                applied_lbl = tk.Label(right_side, text="", font=("Courier New", 8, "bold"),
                                       bg=PANEL_COLOR, fg="#00FF66", anchor="e")
                applied_lbl.pack(side="right", padx=(4, 0))
                self.tweak_applied_lbls[tw["name"]] = applied_lbl

                risk_lbl = tk.Label(
                    right_side,
                    text=_risk_text(tw["risk"]),
                    font=("Consolas", 8, "bold"),
                    bg=PANEL_COLOR,
                    fg=risk_to_color(tw["risk"]),
                    anchor="e",
                )
                risk_lbl.pack(side="right")
                self._risk_labels[tw["name"]] = risk_lbl


        # ── Tools Grid (separate tab) — categorized 2-column grid ──
        self._tools_frame = tk.Frame(tweaks_frame, bg=PANEL_COLOR)
        
        # Search bar at top
        search_frame = tk.Frame(self._tools_frame, bg=PANEL_COLOR)
        search_frame.pack(fill="x", padx=8, pady=(8, 4))
        tk.Label(search_frame, text="\U0001F50D", font=("Segoe UI Emoji", 12),
                 bg=PANEL_COLOR, fg=TEXT_MUTED).pack(side="left", padx=(0, 6))
        self._tools_search_var = tk.StringVar()
        tools_search_entry = tk.Entry(search_frame, textvariable=self._tools_search_var,
                                      font=("Courier New", 10), bg="#1a1a1a", fg="#FFFFFF",
                                      insertbackground="#FFFFFF", relief="flat",
                                      highlightbackground="#333333", highlightthickness=1)
        tools_search_entry.pack(side="left", fill="x", expand=True, ipady=4)
        tools_search_entry.insert(0, "")
        self._tools_search_var.trace_add("write", lambda *a: self._filter_tools())
        
        tools_canvas = tk.Canvas(self._tools_frame, bg=PANEL_COLOR, highlightthickness=0, bd=0)
        tools_vscroll = tk.Scrollbar(self._tools_frame, orient="vertical", command=tools_canvas.yview)
        tools_canvas.configure(yscrollcommand=tools_vscroll.set)
        tools_vscroll.pack(side="right", fill="y")
        tools_canvas.pack(side="left", fill="both", expand=True)
        
        tools_grid = tk.Frame(tools_canvas, bg=PANEL_COLOR)
        _tw = tools_canvas.create_window((0, 0), window=tools_grid, anchor="nw")
        
        tools_grid.columnconfigure(0, weight=1, uniform="toolcol")
        tools_grid.columnconfigure(1, weight=1, uniform="toolcol")
        
        def _on_tools_grid_cfg(e):
            tools_canvas.configure(scrollregion=tools_canvas.bbox("all"))
        def _on_tools_canvas_cfg(e):
            tools_canvas.itemconfig(_tw, width=e.width)
        tools_grid.bind("<Configure>", _on_tools_grid_cfg)
        tools_canvas.bind("<Configure>", _on_tools_canvas_cfg)
        
        def _on_tools_mousewheel(event):
            if self._current_tab == "tools":
                tools_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        tools_canvas.bind_all("<MouseWheel>", _on_tools_mousewheel, add="+")
        
        # Build tool cards grouped by subcategory in a 2-column grid
        tools_cat = CATEGORIES.get("Tools  &  Downloads", {})
        tools_by_name = {tw["name"]: tw for tw in tools_cat.get("tweaks", [])}
        
        self._tool_cards = {}       # tool_name -> card Frame
        self._tool_cat_hdrs = {}    # subcat_name -> header Frame
        self._tool_subcat_map = {}  # tool_name -> subcat_name
        self._tools_grid = tools_grid
        
        grid_row = 0
        for subcat_name, tool_names in TOOL_SUBCATEGORIES.items():
            # ── Subcategory header (spans both columns) ──
            cat_hdr = tk.Frame(tools_grid, bg=PANEL_COLOR)
            cat_hdr.grid(row=grid_row, column=0, columnspan=2, sticky="ew", padx=8, pady=(14, 4))
            tk.Label(cat_hdr, text=f"// {subcat_name.upper()}", font=("Arial Black", 9),
                     bg=PANEL_COLOR, fg=ACCENT_CYAN, anchor="w").pack(side="left")
            tk.Label(cat_hdr, text=f"({len([n for n in tool_names if n in tools_by_name])})", font=("Courier New", 8),
                     bg=PANEL_COLOR, fg=TEXT_MUTED, anchor="w").pack(side="left", padx=6)
            self._tool_cat_hdrs[subcat_name] = cat_hdr
            grid_row += 1
            
            col = 0
            for tool_name in tool_names:
                tw = tools_by_name.get(tool_name)
                if not tw:
                    continue
                
                icon = TOOL_ICONS.get(tw["name"], "\U0001F4E6")
                var = tk.BooleanVar(value=False)
                self.tweak_vars[tw["name"]] = (var, tw)
                
                card = tk.Frame(tools_grid, bg="#1a1a1a", highlightbackground="#333333",
                               highlightthickness=1, padx=10, pady=6)
                card.grid(row=grid_row, column=col, sticky="nsew", padx=4, pady=3)
                self._tool_cards[tw["name"]] = card
                self._tool_subcat_map[tw["name"]] = subcat_name
                
                top_row = tk.Frame(card, bg="#1a1a1a")
                top_row.pack(fill="x")
                
                try:
                    icon_lbl = tk.Label(top_row, text=icon, font=("Segoe UI Emoji", 16),
                                       bg="#1a1a1a", fg="#FFFFFF")
                except Exception:
                    icon_lbl = tk.Label(top_row, text=icon, font=("Arial", 16),
                                       bg="#1a1a1a", fg="#FFFFFF")
                icon_lbl.pack(side="left", padx=(0, 8))
                
                name_frame = tk.Frame(top_row, bg="#1a1a1a")
                name_frame.pack(side="left", fill="x", expand=True)
                
                display_name = _tn(tw["name"])
                for prefix in ["Install ", "Installer ", "Instalar ", "\u062a\u062b\u0628\u064a\u062a "]:
                    if display_name.startswith(prefix):
                        display_name = display_name[len(prefix):]
                        break
                if display_name.endswith(" installieren"):
                    display_name = display_name[:-len(" installieren")]
                
                name_lbl = tk.Label(name_frame, text=display_name,
                        font=("Arial Black", 10), bg="#1a1a1a", fg="#FFFFFF",
                        anchor="w")
                name_lbl.pack(fill="x")
                self._tool_name_lbls[tw["name"]] = name_lbl
                
                desc_lbl = tk.Label(name_frame, text=_td(tw["name"]),
                        font=("Courier New", 7), bg="#1a1a1a", fg="#999999",
                        anchor="w", wraplength=250, justify="left")
                desc_lbl.pack(fill="x")
                self._tool_desc_lbls[tw["name"]] = desc_lbl
                
                install_btn = tk.Checkbutton(
                    top_row, variable=var,
                    text="INSTALL",
                    font=("Courier New", 8, "bold"),
                    bg="#1a1a1a", fg="#00FF66",
                    selectcolor="#000000",
                    activebackground="#1a1a1a",
                    activeforeground="#FF1A00",
                    anchor="e",
                    command=self._update_stats,
                    indicatoron=True,
                )
                install_btn.pack(side="right", padx=(6, 0))
                self._tweak_chks[tw["name"]] = install_btn
                
                applied_lbl = tk.Label(top_row, text="", font=("Courier New", 7, "bold"),
                                       bg="#1a1a1a", fg="#00FF66", anchor="e")
                applied_lbl.pack(side="right", padx=(2, 0))
                self.tweak_applied_lbls[tw["name"]] = applied_lbl
                
                col += 1
                if col >= 2:
                    col = 0
                    grid_row += 1
            
            if col != 0:
                grid_row += 1
        
        self._tweaks_scroll_frame = scroll_container
        self._tools_canvas = tools_canvas
        self._current_tab = "tweaks"

        # ── AI Help Frame (Groq LLM-powered assistant) ──
        self._aihelp_frame = tk.Frame(tweaks_frame, bg=PANEL_COLOR)

        self._ai_chat = tk.Text(self._aihelp_frame, bg="#0a0a0a", fg="#CCCCCC",
                                font=("Courier New", 9), wrap="word",
                                state="disabled", cursor="arrow",
                                relief="flat", highlightthickness=0,
                                padx=12, pady=12)
        ai_vscroll = tk.Scrollbar(self._aihelp_frame, orient="vertical", command=self._ai_chat.yview)
        self._ai_chat.configure(yscrollcommand=ai_vscroll.set)

        ai_input_frame = tk.Frame(self._aihelp_frame, bg=PANEL_COLOR)
        ai_input_frame.pack(side="bottom", fill="x", padx=8, pady=(4, 8))

        self._ai_input_var = tk.StringVar()
        self._ai_entry = tk.Entry(ai_input_frame, textvariable=self._ai_input_var,
                                  font=("Courier New", 10), bg="#1a1a1a", fg="#FFFFFF",
                                  insertbackground="#FFFFFF", relief="flat",
                                  highlightbackground="#333333", highlightthickness=1)
        self._ai_entry.pack(side="left", fill="x", expand=True, ipady=5)
        self._ai_entry.bind("<Return>", lambda e: self._ai_send())

        tk.Button(ai_input_frame, text="SEND", font=("Courier New", 9, "bold"),
                  bg=ACCENT_RED, fg="#FFFFFF", relief="flat", bd=0,
                  padx=12, cursor="hand2",
                  activebackground=ACCENT_CYAN, activeforeground="#000000",
                  command=self._ai_send).pack(side="right", padx=(6, 0))

        # Model selector
        ai_model_frame = tk.Frame(self._aihelp_frame, bg="#111111")
        ai_model_frame.pack(side="top", fill="x", padx=8, pady=(4, 0))
        tk.Label(ai_model_frame, text="MODEL:", font=("Courier New", 8, "bold"),
                 bg="#111111", fg="#888888").pack(side="left", padx=(4, 4))
        self._ai_model_var = tk.StringVar(value="\u26a1 Auto")
        self._ai_model_menu = tk.OptionMenu(ai_model_frame, self._ai_model_var, "\u26a1 Auto")
        self._ai_model_menu.configure(font=("Courier New", 8), bg="#1a1a1a", fg="#CCCCCC",
                                       activebackground="#333333", activeforeground="#FFFFFF",
                                       relief="flat", highlightthickness=0, bd=0)
        self._ai_model_menu["menu"].configure(font=("Courier New", 8), bg="#1a1a1a",
                                                fg="#CCCCCC", activebackground="#FF1A00",
                                                activeforeground="#FFFFFF")
        self._ai_model_menu.pack(side="left", fill="x", expand=True)

        ai_vscroll.pack(side="right", fill="y")
        self._ai_chat.pack(fill="both", expand=True, padx=8, pady=(8, 0))

        self._ai_chat.tag_configure("you", foreground=ACCENT_CYAN, font=("Courier New", 9, "bold"))
        self._ai_chat.tag_configure("ai", foreground=ACCENT_RED, font=("Courier New", 9, "bold"))
        self._ai_chat.tag_configure("msg", foreground="#CCCCCC", font=("Courier New", 9))
        self._ai_chat.tag_configure("dim", foreground="#666666", font=("Courier New", 8))

        self._ai_history = []
        self._ai_api_key = self._load_ai_key()
        self._ai_daily_usage = self._ai_load_daily_usage()
        self._ai_update_model_menu()
        self._ai_show_welcome()

        paned.add(specs_frame, minsize=340)
        paned.add(tweaks_frame, minsize=520)

        # ══════════════ Bottom controls (Brutalist flat buttons) ══════════════

        # -- Bottom scan line separator --
        btm_scan = tk.Frame(self.root, bg=ACCENT_RED, height=1)
        btm_scan.pack(fill="x", padx=10, pady=(0, 0))

        bottom = tk.Frame(self.root, bg=BG_COLOR)
        bottom.pack(fill="x", pady=10)

        self.stats_lbl = tk.Label(bottom, text=_t("stats_init"), font=("Arial Black", 9), bg=BG_COLOR, fg=ACCENT_CYAN)
        self.stats_lbl.pack(side="left", padx=15, pady=4)

        self.sel_all_btn = tk.Button(bottom, text=_t("select_all"), font=("Courier New", 9, "bold"), bg=PANEL_COLOR, fg=ACCENT_CYAN, relief="flat", activebackground=ACCENT_RED, command=self._select_all)
        self.sel_all_btn.pack(side="left", padx=5, pady=3)
        self.purge_btn = tk.Button(bottom, text=_t("purge"), font=("Courier New", 9, "bold"), bg=PANEL_COLOR, fg=TEXT_MUTED, relief="flat", activebackground=ACCENT_CYAN, command=self._deselect_all)
        self.purge_btn.pack(side="left", padx=5, pady=3)
        
        self.exec_btn = tk.Button(bottom, text=f">> {_t('execute')} <<", font=("Arial Black", 11), bg=ACCENT_RED, fg=BG_COLOR, relief="flat", activebackground=ACCENT_CYAN, activeforeground=BG_COLOR, command=self._apply, cursor="hand2")
        self.exec_btn.pack(side="right", padx=15, pady=3, ipadx=14, ipady=4)

        self._update_stats()

    # ══════════════════════ Feedback / Rating Dialog ══════════════════════

    def _switch_tab(self, tab):
        """Switch between Tweaks, Tools and AI Help tabs."""
        ACCENT_RED = "#FF1A00"
        frames = {
            "tweaks": self._tweaks_scroll_frame,
            "tools": self._tools_frame,
            "aihelp": self._aihelp_frame,
        }
        btns = {
            "tweaks": self._tweaks_tab_btn,
            "tools": self._tools_tab_btn,
            "aihelp": self._aihelp_tab_btn,
        }
        for name, frame in frames.items():
            frame.pack_forget()
        frames[tab].pack(fill="both", expand=True, padx=0, pady=0)
        for name, btn in btns.items():
            if name == tab:
                btn.configure(bg=ACCENT_RED, fg="#FFFFFF")
            else:
                btn.configure(bg="#333333", fg="#888888")
        self._current_tab = tab
        if tab == "aihelp":
            self._ai_entry.focus_set()

    def _filter_tools(self):
        """Filter tools grid based on search query — soft fuzzy matching."""
        query = self._tools_search_var.get().lower().strip()
        words = query.split() if query else []
        
        # Hide everything first
        for widget in self._tools_grid.winfo_children():
            widget.grid_forget()
        
        grid_row = 0
        for subcat_name, tool_names in TOOL_SUBCATEGORIES.items():
            hdr = self._tool_cat_hdrs.get(subcat_name)
            if not hdr:
                continue
            
            # Collect matching tools in this category
            matching = []
            for tool_name in tool_names:
                card = self._tool_cards.get(tool_name)
                if not card:
                    continue
                if words:
                    # Combine all searchable text into one blob
                    blob = f"{tool_name} {_tn(tool_name)} {_td(tool_name)} {subcat_name}".lower()
                    # Remove common install prefixes for better matching
                    for pfx in ["install ", "installer ", "instalar ", "installieren "]:
                        blob = blob.replace(pfx, " ")
                    # ANY search word can match (soft mode)
                    if not any(w in blob for w in words):
                        continue
                matching.append((tool_name, card))
            
            if not matching:
                continue
            
            # Show category header
            hdr.grid(row=grid_row, column=0, columnspan=2, sticky="ew", padx=8, pady=(14, 4))
            grid_row += 1
            
            col = 0
            for tool_name, card in matching:
                card.grid(row=grid_row, column=col, sticky="nsew", padx=4, pady=3)
                col += 1
                if col >= 2:
                    col = 0
                    grid_row += 1
            if col != 0:
                grid_row += 1
        
        # Update scroll region and reset to top
        self._tools_grid.update_idletasks()
        self._tools_canvas.configure(scrollregion=self._tools_canvas.bbox("all"))
        self._tools_canvas.yview_moveto(0)

    # ════════════════════ AI Chat Helper Methods ═════════════════════════

    def _load_ai_key(self):
        try:
            with open(_CONFIG_PATH, "r") as f:
                return json.loads(f.read()).get("groq_api_key", "")
        except Exception:
            return ""

    def _save_ai_key(self, key):
        cfg = {}
        try:
            with open(_CONFIG_PATH, "r") as f:
                cfg = json.loads(f.read())
        except Exception:
            pass
        cfg["groq_api_key"] = key
        with open(_CONFIG_PATH, "w") as f:
            f.write(json.dumps(cfg))
        self._ai_api_key = key

    def _ai_show_welcome(self):
        self._ai_chat.configure(state="normal")
        self._ai_chat.delete("1.0", "end")
        if not self._ai_api_key:
            self._ai_chat.insert("end", "AI ASSISTANT - SETUP\n\n", "ai")
            self._ai_chat.insert("end",
                "To use the free AI features, you need an API key.\n\n"
                "Setup (takes 30 seconds):\n"
                "  1. Go to aistudio.google.com/apikey (or groq.com)\n"
                "  2. Create a free API key\n"
                "  3. Paste your key below and press SEND\n\n", "msg")
            self._ai_chat.insert("end",
                "Your key is saved locally in the config.\n", "dim")
        else:
            self._ai_chat.insert("end", "AI ASSISTANT\n\n", "ai")
            self._ai_chat.insert("end",
                "Describe your PC problem and I'll recommend\n"
                "the best tools and tweaks.\n", "msg")
        self._ai_chat.configure(state="disabled")

    def _ai_send(self):
        text = self._ai_input_var.get().strip()
        if not text:
            return
        self._ai_input_var.set("")

        if not self._ai_api_key:
            if len(text) > 20 and ("AIza" in text or text.startswith("gsk_") or "csk" in text):
                self._save_ai_key(text)
                self._ai_chat.configure(state="normal")
                self._ai_chat.delete("1.0", "end")
                self._ai_chat.insert("end", "AI ASSISTANT\n\n", "ai")
                self._ai_chat.insert("end",
                    "API key saved. Ask me anything about your PC.\n", "msg")
                self._ai_chat.configure(state="disabled")
                return
            else:
                self._ai_chat.configure(state="normal")
                self._ai_chat.insert("end",
                    "\nPaste a valid Gemini, Groq, Cerebras, or Cohere API key.\n", "dim")
                self._ai_chat.configure(state="disabled")
                self._ai_chat.see("end")
                return

        self._ai_chat.configure(state="normal")
        self._ai_chat.insert("end", f"\nYOU: ", "you")
        self._ai_chat.insert("end", text + "\n", "msg")
        self._ai_chat.insert("end", "\n...\n", "dim")
        self._ai_chat.configure(state="disabled")
        self._ai_chat.see("end")

        self._ai_history.append({"role": "user", "content": text})

        def _call():
            result = self._ai_call_fallback()
            self.root.after(0, lambda r=result: self._ai_show_response(r))
        threading.Thread(target=_call, daemon=True).start()

    def _ai_show_response(self, result):
        model_name, response = result
        self._ai_chat.configure(state="normal")
        idx = self._ai_chat.search("...", "end-3l", "end")
        if idx:
            self._ai_chat.delete(idx + " linestart", idx + " lineend +1c")
        if model_name:
            self._ai_chat.insert("end", f"AI ({model_name}): ", "ai")
        else:
            self._ai_chat.insert("end", "AI: ", "ai")
        self._ai_chat.insert("end", response + "\n", "msg")
        self._ai_chat.configure(state="disabled")
        self._ai_chat.see("end")
        self._ai_history.append({"role": "assistant", "content": response})
        if len(self._ai_history) > 20:
            self._ai_history = self._ai_history[-20:]

    def _ai_build_system_prompt(self):
        tool_cats = []
        for subcat, names in TOOL_SUBCATEGORIES.items():
            short = [n.replace("Install ", "") for n in names]
            tool_cats.append(f"{subcat}: {', '.join(short)}")
        tweak_cats = []
        for cat_name, cat_data in CATEGORIES.items():
            if "Tools" in cat_name and "Downloads" in cat_name:
                continue
            tw_names = [tw["name"] for tw in cat_data["tweaks"]]
            tweak_cats.append(f"{cat_name}: {', '.join(tw_names)}")
        return (
            "You are a helpful AI assistant inside NormieTools PC Optimizer for Windows.\n"
            "Answer naturally. If the user asks a general question or says hello, respond normally.\n"
            "When the user describes a SPECIFIC PC problem, recommend tools/tweaks from these lists:\n"
            "TOOLS (winget install): " + " | ".join(tool_cats) + "\n"
            "TWEAKS (registry/PS): " + " | ".join(tweak_cats) + "\n"
            "SCAN COMMANDS - ONLY use when the user describes a specific problem that needs diagnosis:\n"
            "  [SCAN:system] [SCAN:processes] [SCAN:startup] [SCAN:disk] [SCAN:temps]\n"
            "Do NOT scan for general questions, greetings, or simple tool/tweak recommendations.\n"
            "RULES: Only recommend tools/tweaks from the lists above. Be concise, max 6 items."
        )

    _AI_FALLBACK_KEYS = {
        "gemini": os.environ.get("GEMINI_API_KEY", ""),
        "groq": os.environ.get("GROQ_API_KEY", ""),
        "cerebras": os.environ.get("CEREBRAS_API_KEY", ""),
        "cohere": os.environ.get("COHERE_API_KEY", ""),
    }

    # Fallback chain: ordered for SPEED. On 429/error, try next instantly.
    _AI_PROVIDERS = [
        {"n": "Groq Llama 3.3 70B", "u": "https://api.groq.com/openai/v1/chat/completions", "m": "llama-3.3-70b-versatile", "k": "groq"},
        {"n": "Groq Qwen3-32B", "u": "https://api.groq.com/openai/v1/chat/completions", "m": "qwen/qwen3-32b", "k": "groq"},
        {"n": "Cerebras Llama 3.3 70B", "u": "https://api.cerebras.ai/v1/chat/completions", "m": "llama-3.3-70b", "k": "cerebras"},
        {"n": "Groq Llama 3.1 8B", "u": "https://api.groq.com/openai/v1/chat/completions", "m": "llama-3.1-8b-instant", "k": "groq"},
        {"n": "Cerebras Llama 3.1 8B", "u": "https://api.cerebras.ai/v1/chat/completions", "m": "llama3.1-8b", "k": "cerebras"},
        {"n": "Gemini 2.5 Flash", "u": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions", "m": "gemini-2.5-flash", "k": "gemini"},
        {"n": "Gemini 2.0 Flash", "u": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions", "m": "gemini-2.0-flash", "k": "gemini"},
        {"n": "Gemini 1.5 Flash", "u": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions", "m": "gemini-1.5-flash", "k": "gemini"},
        {"n": "Cohere Command A", "u": "https://api.cohere.com/v2/chat", "m": "command-a-03-2025", "k": "cohere", "co": True},
    ]

    _AI_DAILY_LIMITS = {
        "Groq Llama 3.3 70B": 30, "Groq Qwen3-32B": 30,
        "Cerebras Llama 3.3 70B": 30, "Groq Llama 3.1 8B": 30,
        "Cerebras Llama 3.1 8B": 30,
        "Gemini 2.5 Flash": 15, "Gemini 2.5 Flash-Lite": 15,
        "Gemini 3 Flash": 10, "Gemini 3.1 Flash-Lite": 10,
        "Gemini 2.0 Flash": 15, "Gemini 2.5 Pro": 5,
        "Cohere Command A": 5,
    }

    _AI_SCAN_CMDS = {
        "system": (
            "$os=Get-CimInstance Win32_OperatingSystem;"
            "$cpu=Get-CimInstance Win32_Processor;"
            "$ram=[math]::Round($os.TotalVisibleMemorySize/1MB,1);"
            "$free=[math]::Round($os.FreePhysicalMemory/1MB,1);"
            "echo \"OS: $($os.Caption) Build $($os.BuildNumber)\";"
            "echo \"CPU: $($cpu.Name)\";"
            "echo \"RAM: ${ram}GB total, ${free}GB free\";"
            "Get-PSDrive -PSProvider FileSystem|Select Name,"
            "@{N='FreeGB';E={[math]::Round($_.Free/1GB,1)}},"
            "@{N='UsedGB';E={[math]::Round($_.Used/1GB,1)}}|"
            "Format-Table -AutoSize|Out-String"
        ),
        "processes": (
            "Get-Process|Sort CPU -Desc|Select -First 12 Name,"
            "@{N='CPU_s';E={[math]::Round($_.CPU,1)}},"
            "@{N='RAM_MB';E={[math]::Round($_.WorkingSet64/1MB,1)}}|"
            "Format-Table -AutoSize|Out-String"
        ),
        "startup": (
            "Get-CimInstance Win32_StartupCommand|"
            "Select Name,Command,Location|Format-Table -AutoSize -Wrap|Out-String"
        ),
        "disk": (
            "Get-PSDrive -PSProvider FileSystem|Select Name,"
            "@{N='FreeGB';E={[math]::Round($_.Free/1GB,1)}},"
            "@{N='UsedGB';E={[math]::Round($_.Used/1GB,1)}},"
            "@{N='TotalGB';E={[math]::Round(($_.Free+$_.Used)/1GB,1)}},"
            "@{N='PctFree';E={[math]::Round($_.Free/($_.Free+$_.Used)*100,0)}}|"
            "Format-Table -AutoSize|Out-String"
        ),
        "temps": (
            "$t=[IO.Path]::GetTempPath();"
            "$ts=(gci $t -R -Force -EA 0|Measure Length -Sum).Sum/1MB;"
            "$wt=\"$env:WINDIR\\Temp\";"
            "$ws=(gci $wt -R -Force -EA 0|Measure Length -Sum).Sum/1MB;"
            "$pf=\"$env:WINDIR\\Prefetch\";"
            "$ps=(gci $pf -R -Force -EA 0|Measure Length -Sum).Sum/1MB;"
            "echo \"User Temp: $([math]::Round($ts,1)) MB\";"
            "echo \"Windows Temp: $([math]::Round($ws,1)) MB\";"
            "echo \"Prefetch: $([math]::Round($ps,1)) MB\""
        ),
    }

    def _ai_load_daily_usage(self):
        try:
            with open(_CONFIG_PATH, "r") as f:
                usage = json.loads(f.read()).get("ai_usage", {})
            if usage.get("date") == time.strftime("%Y-%m-%d"):
                return usage
        except Exception:
            pass
        return {"date": time.strftime("%Y-%m-%d"), "counts": {}}

    def _ai_get_remaining(self, name):
        limit = self._AI_DAILY_LIMITS.get(name, 9999)
        used = self._ai_daily_usage.get("counts", {}).get(name, 0)
        return max(0, limit - used)

    def _ai_inc_usage(self, name):
        today = time.strftime("%Y-%m-%d")
        if self._ai_daily_usage.get("date") != today:
            self._ai_daily_usage = {"date": today, "counts": {}}
        counts = self._ai_daily_usage.setdefault("counts", {})
        counts[name] = counts.get(name, 0) + 1
        try:
            cfg = {}
            with open(_CONFIG_PATH, "r") as f:
                cfg = json.loads(f.read())
        except Exception:
            pass
        cfg["ai_usage"] = self._ai_daily_usage
        with open(_CONFIG_PATH, "w") as f:
            f.write(json.dumps(cfg))

    def _ai_update_model_menu(self):
        menu = self._ai_model_menu["menu"]
        menu.delete(0, "end")
        menu.add_command(label="\u26a1 Auto (best available)",
                         command=lambda: self._ai_model_var.set("\u26a1 Auto"))
        for p in self._AI_PROVIDERS:
            rem = self._ai_get_remaining(p["n"])
            lim = self._AI_DAILY_LIMITS.get(p["n"], "?")
            label = f"{p['n']}  [{rem}/{lim}]"
            menu.add_command(label=label,
                             command=lambda n=p["n"]: self._ai_model_var.set(n))

    def _ai_run_scan(self, tool_name):
        cmd = self._AI_SCAN_CMDS.get(tool_name)
        if not cmd:
            return f"Unknown scan: {tool_name}"
        try:
            result = subprocess.run(
                ["powershell", "-NoProfile", "-Command", cmd],
                capture_output=True, text=True, timeout=15,
                creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0)
            )
            return (result.stdout.strip() or result.stderr.strip() or "No output")[:1500]
        except subprocess.TimeoutExpired:
            return "Scan timed out"
        except Exception as e:
            return f"Scan error: {e}"

    def _ai_do_single_call(self, messages):
        """Make one API call with provider fallback. Returns text or None."""
        last_err = ""
        selected = self._ai_model_var.get()
        providers = self._AI_PROVIDERS
        if selected != "\u26a1 Auto":
            providers = sorted(providers, key=lambda p: 0 if p["n"] == selected else 1)

        for p in providers:
            if self._ai_get_remaining(p["n"]) <= 0:
                continue
            api_key = self._AI_FALLBACK_KEYS.get(p["k"], "")
            if self._ai_api_key:
                if self._ai_api_key.startswith("AIza") and p["k"] == "gemini": api_key = self._ai_api_key
                elif self._ai_api_key.startswith("gsk_") and p["k"] == "groq": api_key = self._ai_api_key
                elif self._ai_api_key.startswith("csk") and p["k"] == "cerebras": api_key = self._ai_api_key
                elif not (self._ai_api_key.startswith("AIza") or self._ai_api_key.startswith("gsk_") or self._ai_api_key.startswith("csk")) and p["k"] == "cohere": api_key = self._ai_api_key

            if not api_key:
                continue

            payload = {"model": p["m"], "messages": messages, "temperature": 0.3, "max_tokens": 500}
            if p.get("co"):
                payload["stream"] = False

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
                "User-Agent": "NormieTools/1.0",
            }

            req = urllib.request.Request(p["u"], data=json.dumps(payload).encode("utf-8"), headers=headers)
            try:
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    if p.get("co"):
                        text = data["message"]["content"][0]["text"]
                    else:
                        text = data["choices"][0]["message"]["content"]
                    if text:
                        self._ai_inc_usage(p["n"])
                        self.root.after(0, self._ai_update_model_menu)
                        return (p["n"], text)
            except urllib.error.HTTPError as e:
                body = ""
                try:
                    body = e.read().decode("utf-8", errors="replace")
                except:
                    pass
                if e.code in (401, 403):
                    if p["k"] == "gemini":
                        self._ai_api_key = ""
                    last_err = f"API Key error: {body[:100]}"
                    return (None, f"Invalid API key for {p['n']}. Re-enter your key.")
                if e.code in (429, 503, 502):
                    last_err = f"{p['n']} busy/rate-limited"
                    continue
                if e.code == 400:
                    last_err = f"{p['n']} model invalid. Body: {body[:100]}"
                    continue
                last_err = f"{p['n']}: HTTP {e.code} - {body[:100]}"
                continue
            except Exception as e:
                last_err = str(e)[:80]
                continue
        return (None, last_err if last_err else "No valid API keys. Re-enter your key.")

    def _ai_call_fallback(self):
        system_prompt = self._ai_build_system_prompt()
        messages = [{"role": "system", "content": system_prompt}]
        for msg in self._ai_history[-6:]:
            messages.append({"role": msg["role"], "content": msg["content"]})

        # First API call
        result = self._ai_do_single_call(messages)
        if not result or not result[0]:
            err_msg = result[1] if result else "Unknown error"
            return (None, f"All AI models busy. Try again in a minute.\n\nDebug Info: {err_msg}")
        model_name, response = result

        # Check for scan tool calls
        scans = re.findall(r'\[SCAN:(\w+)\]', response)
        if scans:
            # Execute scans
            tool_results = []
            for scan in scans:
                if scan in self._AI_SCAN_CMDS:
                    output = self._ai_run_scan(scan)
                    tool_results.append(f"[{scan}]\n{output}")

            if tool_results:
                clean = re.sub(r'\[SCAN:\w+\]', '', response).strip()
                if clean:
                    messages.append({"role": "assistant", "content": clean})
                results_text = "SCAN RESULTS:\n" + "\n---\n".join(tool_results)
                messages.append({"role": "user", "content": results_text})

                # Second API call with scan results
                result2 = self._ai_do_single_call(messages)
                if result2:
                    return result2
                return (model_name, f"Scan complete but analysis failed.\n\n{results_text}")

        return (model_name, response)

    def _show_feedback_dialog(self):
        BG_D = "#0a0a0a"
        ACCENT_RED = "#FF1A00"
        ACCENT_CYAN = "#00DDFF"
        dialog = tk.Toplevel(self.root)
        dialog.title(_t("fb_title"))
        dialog.configure(bg=BG_D)
        dialog.resizable(False, False)
        dialog.attributes("-topmost", True)

        w, h = 480, 440
        x = (dialog.winfo_screenwidth() // 2) - (w // 2)
        y = (dialog.winfo_screenheight() // 2) - (h // 2)
        dialog.geometry(f"{w}x{h}+{x}+{y}")

        # Try to apply the app icon to the dialog
        try:
            dialog.iconbitmap(self.root.iconbitmap())
        except Exception:
            pass

        # Header
        tk.Label(dialog, text=_t("fb_header"), font=("Arial Black", 14),
                 bg=BG_D, fg=ACCENT_RED).pack(pady=(15, 2))
        tk.Label(dialog, text=_t("fb_subtitle"),
                 font=("Courier New", 8), bg=BG_D, fg="#888888").pack(pady=(0, 5))

        # Show current rating (read-only display)
        cur_r = self.rating_var.get()
        stars_display = "\u2605" * cur_r + "\u2606" * (5 - cur_r)
        rating_txt = _t("fb_rating_set", s=stars_display, n=cur_r) if cur_r > 0 else _t("fb_rating_none")
        tk.Label(dialog, text=rating_txt, font=("Courier New", 9, "bold"),
                 bg=BG_D, fg="#FF8800").pack(pady=(0, 8))

        tk.Frame(dialog, bg=ACCENT_RED, height=1).pack(fill="x", padx=20, pady=(0, 12))

        # ═══════════════════════════ Feedback Type ════════════════════════════
        tk.Label(dialog, text=_t("fb_type"), font=("Arial Black", 9),
                 bg=BG_D, fg=ACCENT_CYAN).pack(anchor="w", padx=25)

        type_var = tk.StringVar(value=_t("fb_bug"))
        type_frame = tk.Frame(dialog, bg=BG_D)
        type_frame.pack(pady=(4, 10), padx=25, anchor="w")

        for label in [_t("fb_bug"), _t("fb_suggestion"), _t("fb_general")]:
            tk.Radiobutton(type_frame, text=label, variable=type_var, value=label,
                           font=("Courier New", 9, "bold"), bg=BG_D, fg="#DDDDDD",
                           selectcolor="#000000", activebackground=BG_D,
                           activeforeground=ACCENT_RED, cursor="hand2",
                           indicatoron=True).pack(side="left", padx=(0, 12))

        # ══════════════════════════════ Message ═══════════════════════════════
        tk.Label(dialog, text=_t("fb_message"), font=("Arial Black", 9),
                 bg=BG_D, fg=ACCENT_CYAN).pack(anchor="w", padx=25, pady=(5, 0))

        msg_text = tk.Text(dialog, font=("Courier New", 9), bg="#111111", fg=ACCENT_CYAN,
                           insertbackground=ACCENT_CYAN, relief="flat", bd=0,
                           highlightthickness=1, highlightcolor=ACCENT_RED,
                           highlightbackground="#333333", height=8, wrap="word")
        msg_text.pack(fill="x", padx=25, pady=(5, 15))

        placeholder = _t("fb_placeholder")
        msg_text.insert("1.0", placeholder)
        msg_text.configure(fg="#555555")

        def on_focus_in(e):
            if msg_text.get("1.0", "end").strip() == placeholder:
                msg_text.delete("1.0", "end")
                msg_text.configure(fg=ACCENT_CYAN)

        def on_focus_out(e):
            if not msg_text.get("1.0", "end").strip():
                msg_text.insert("1.0", placeholder)
                msg_text.configure(fg="#555555")

        msg_text.bind("<FocusIn>", on_focus_in)
        msg_text.bind("<FocusOut>", on_focus_out)

        # ════════════════════════════ Send Button ═════════════════════════════
        btn_frame = tk.Frame(dialog, bg=BG_D)
        btn_frame.pack(fill="x", padx=25, pady=(0, 15))

        send_btn = tk.Button(btn_frame, text=_t("fb_send"), font=("Arial Black", 10),
                  bg=ACCENT_RED, fg="#000000", relief="flat", cursor="hand2",
                  activebackground=ACCENT_CYAN, activeforeground="#000000")
        send_btn.pack(side="right", ipadx=12, ipady=3)

        abort_btn = tk.Button(btn_frame, text=_t("fb_abort"), font=("Courier New", 9, "bold"),
                  bg="#111111", fg="#888888", relief="flat", cursor="hand2",
                  activebackground=ACCENT_RED, activeforeground="#000000",
                  command=dialog.destroy)
        abort_btn.pack(side="right", padx=10)

        def send_feedback():
            rating = self.rating_var.get()
            fb_type = type_var.get()
            message = msg_text.get("1.0", "end").strip()

            if not message or message == placeholder:
                messagebox.showwarning(_t("fb_empty_title"),
                                       _t("fb_empty_msg"), parent=dialog)
                return

            # Disable buttons and show sending state
            send_btn.configure(text=_t("fb_sending"), state="disabled",
                               bg="#555555", cursor="arrow")
            abort_btn.configure(state="disabled")
            msg_text.configure(state="disabled")

            stars_str = "\u2605" * rating + "\u2606" * (5 - rating)
            subject = f"[NormieOptimizer {APP_VERSION}] {fb_type}"
            if rating > 0:
                subject += f" - {stars_str}"

            body_text = (f"Type: {fb_type}\n"
                         f"Rating: {stars_str} ({rating}/5)\n"
                         f"Version: {APP_VERSION}\n"
                         f"{'=' * 40}\n\n"
                         f"{message}")

            def _on_success(via_browser=False):
                msg = _t("fb_sent_browser") if via_browser else _t("fb_sent_msg")
                messagebox.showinfo(_t("fb_sent_title"), msg, parent=dialog)
                dialog.destroy()

            def _on_error(ex):
                send_btn.configure(text=_t("fb_send"), state="normal",
                                   bg=ACCENT_RED, cursor="hand2")
                abort_btn.configure(state="normal")
                msg_text.configure(state="normal")
                messagebox.showerror(_t("fb_err_title"),
                                     _t("fb_err_msg", e=ex), parent=dialog)

            def _do_send():
                # ── Path A: Brevo API (if key is configured) ──
                if _BREVO_KEY:
                    payload = {
                        "sender": {"name": "NormieTools Feedback",
                                   "email": _BREVO_SENDER},
                        "to": [{"email": CONTACT_EMAIL}],
                        "subject": subject,
                        "textContent": body_text,
                    }
                    req = urllib.request.Request(
                        "https://api.brevo.com/v3/smtp/email",
                        data=json.dumps(payload).encode("utf-8"),
                        headers={
                            "api-key": _BREVO_KEY,
                            "Content-Type": "application/json",
                            "Accept": "application/json",
                        },
                    )
                    urllib.request.urlopen(req, timeout=15)
                    dialog.after(0, lambda: _on_success(False))
                    return

                # ── Path B: GitHub Issue (always works, zero config) ──
                title = urlquote(f"[{fb_type}] {subject}")
                body_md = (f"**Type:** {fb_type}\n"
                           f"**Rating:** {stars_str} ({rating}/5)\n"
                           f"**Version:** {APP_VERSION}\n\n---\n\n"
                           f"{message}")
                issue_url = (f"https://github.com/{GITHUB_REPO}/issues/new"
                             f"?title={title}"
                             f"&body={urlquote(body_md)}"
                             f"&labels=feedback")
                webbrowser.open(issue_url)
                dialog.after(0, lambda: _on_success(True))

            def _send_threaded():
                try:
                    _do_send()
                except Exception as ex:
                    dialog.after(0, lambda e=ex: _on_error(e))

            threading.Thread(target=_send_threaded, daemon=True).start()

        send_btn.configure(command=send_feedback)

    def _scan_applied_tweaks(self):
        """Now handled by _loading_worker at startup. Kept as no-op for compatibility."""
        pass

    def _check_custom(self, tweak_name):
        c = getattr(self, "_custom_cache", {})
        bc = getattr(self, "_bcdedit_cache", "")
        
        if tweak_name == "Disable Memory Compression": return c.get("mmagent") == False
        if tweak_name == "Disable CFG (Control Flow Guard)": return c.get("cfg") == False
        if "Nagle's Algorithm" in tweak_name: return c.get("nagle") == True
        if "NetBIOS over TCP/IP" in tweak_name: return c.get("netbios") == True
        if "Large Send Offload" in tweak_name: return c.get("lso") == True
        if "Receive Segment Coalescing" in tweak_name: return c.get("rsc") == False
        if "MSI Mode on All PCI Devices" in tweak_name: return c.get("msi") == True
        
        if "RSS & DCA" in tweak_name: return c.get("rss") == True and c.get("heuristics") == True
        if "TCP Timestamps & ECN" in tweak_name: return c.get("timestamps") == True and c.get("ecn") == True
        if "Congestion Control to CUBIC" in tweak_name: return c.get("cubic") == True
        
        # BCDEDIT checks ” use regex to avoid false positives from substring matches
        if "DEP (Data Execution" in tweak_name: return bool(re.search(r'\bnx\s+alwaysoff\b', bc))
        if "Dynamic Tick" in tweak_name: return bool(re.search(r'disabledynamictick\s+yes', bc))
        if "TSC Timer (Remove HPET)" in tweak_name: return "useplatformclock" not in bc and "useplatformtick" not in bc
        if "TSC Sync Policy" in tweak_name: return bool(re.search(r'tscsyncpolicy\s+enhanced', bc))
        if "Boot Timeout to 0" in tweak_name: return bool(re.search(r'timeout\s+0\b', bc))


        # Power plan detection
        if "Ultimate Performance" in tweak_name:
            scheme = str(c.get("powerScheme", "")).lower()
            return "ultimate" in scheme or "e9a42b02" in scheme or "8c5e7fda" in scheme or "high performance" in scheme

        # powercfg /change timeout tweaks (queried via PS cache)
        if "Sleep & Display Timeout" in tweak_name or "Sleep & Display" in tweak_name:
            return c.get("sleepAC") == 0 and c.get("monitorAC") == 0
        if "Disk Sleep" in tweak_name:
            return c.get("diskAC") == 0

        # VBS bcdedit check (also has registry keys; return None if bcdedit not set to let registry check run)
        if "VBS / HVCI" in tweak_name:
            if not bool(re.search(r'hypervisorlaunchtype\s+off', bc)):
                return False
            return None  # Let _is_tweak_applied check registry values too

        # TCP Fast Open
        if "TCP Fast Open" in tweak_name:
            return c.get("fastOpen") == True

        # Hibernation & Fast Startup (powercfg -h off part) - checks hiberfil.sys gone
        # Returns None (not False) when hiberfil.sys gone so _is_tweak_applied also verifies HiberbootEnabled
        if "Hibernation & Fast Startup" in tweak_name:
            if c.get("hibernation") != False:
                return False  # hiberfil.sys still exists
            return None  # hiberfil.sys gone; let _is_tweak_applied verify HiberbootEnabled reg key too



        # WMM Power Save
        if "WMM" in tweak_name:
            return c.get("wmm") == True

        # Energy Efficient Ethernet
        if "Energy Efficient Ethernet" in tweak_name:
            return c.get("eee") == True

        # IPv6 Tunneling (Teredo, ISATAP, 6to4) - pure netsh commands
        if "IPv6 Tunneling" in tweak_name:
            return c.get("ipv6tunnel") == True

        # QoS Packet Scheduler - has registry key but also add custom check
        if "QoS Packet Scheduler" in tweak_name:
            return c.get("qos") == True

        # USB Controller Power Saving - checks EnhancedPowerManagementEnabled on USB controllers
        if "USB Controller Power Saving" in tweak_name:
            return c.get("usbPowerSaving") == True

        # GPU MSI Priority to High
        if "GPU MSI Priority" in tweak_name:
            return c.get("gpuMsiPriority") == True

        # NIC MSI Priority to High
        if "NIC MSI Priority" in tweak_name:
            return c.get("nicMsiPriority") == True

        # NVIDIA P-State P0 detection
        if "NVIDIA P-State" in tweak_name or "P-State P0" in tweak_name:
            return c.get("nvPstate") == True

        # System Restore detection
        if "System Restore" in tweak_name:
            if c.get("systemRestoreDisabled") == True:
                return None  # PS says disabled; let _is_tweak_applied verify DisableSR reg too
            return False

        if "Variable Refresh Rate" in tweak_name:
            return c.get("vrr") == True

        if "True Exclusive Fullscreen" in tweak_name:
            if c.get("fse") != True:
                return False  # SwapEffectUpgradeEnable not disabled
            return None  # PS check passed; let _is_tweak_applied verify 4 reg values too

        # GPU Energy Driver - check service registry directly
        if "GPU Energy Driver" in tweak_name:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Services\\gpuenergydrv") as k:
                    start_val, _ = winreg.QueryValueEx(k, "Start")
                    return start_val == 4  # 4 = SERVICE_DISABLED
            except FileNotFoundError:
                return False  # Service doesn't exist = tweak is irrelevant, don't mark applied
            except Exception:
                return None

        # NVIDIA Telemetry - check service registry directly
        if "NVIDIA Telemetry" in tweak_name:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Services\\NvTelemetryContainer") as k:
                    start_val, _ = winreg.QueryValueEx(k, "Start")
                    return start_val == 4  # 4 = SERVICE_DISABLED
            except FileNotFoundError:
                return False  # Service doesn't exist = tweak is irrelevant, don't mark applied
            except Exception:
                return None

        # Cleanup / one-shot tweaks - these delete temp files, never persistently "applied"
        if any(x in tweak_name for x in ["Temp / Cache", "Flush DNS", "Browser Caches",
                                          "Update Cache", "Event Viewer", "Install "]):
            return False

        return None
    def _set_tweak_checked(self, tweak_name):
        if tweak_name in self.tweak_vars:
            self.tweak_vars[tweak_name][0].set(True)
            self.initially_applied.add(tweak_name)  # Track as initially applied
            if tweak_name in self.tweak_applied_lbls:
                self.tweak_applied_lbls[tweak_name].configure(text=_t("applied"))
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
                                try:
                                    is_match = (int(val) == int(str(expected_data), 0))
                                except (ValueError, TypeError):
                                    is_match = False
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

            # 2. Check Services (via registry — locale-independent, no subprocess)
            elif cmd_lower.startswith('sc config'):
                match = re.search(r'sc config\s+(.*?)\s+start=\s*disabled', cmd, re.IGNORECASE)
                if match:
                    service_name = match.group(1).strip('"')
                    verifiable_cmds += 1
                    try:
                        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                f"SYSTEM\\CurrentControlSet\\Services\\{service_name}") as svc_key:
                            start_val, _ = winreg.QueryValueEx(svc_key, "Start")
                            if start_val == 4:  # 4 = SERVICE_DISABLED
                                applied_cmds += 1
                    except FileNotFoundError:
                        # Service key doesn't exist → effectively disabled
                        applied_cmds += 1
                    except Exception:
                        verifiable_cmds -= 1  # Can\'t read, don\'t penalize

            # 3. Check Scheduled Tasks (via cached taskStates from PS scan - no subprocess!)
            elif cmd_lower.startswith('schtasks /change'):
                match = re.search(r'schtasks /Change /TN "(.*?)" /Disable', cmd, re.IGNORECASE)
                if match:
                    task_name = match.group(1)
                    verifiable_cmds += 1
                    task_cache = getattr(self, '_custom_cache', {}).get('taskStates', {})
                    if task_cache:
                        lookup = task_name if task_name.startswith('\\') else '\\' + task_name
                        state = task_cache.get(lookup, '')
                        if state == 'Disabled':
                            applied_cmds += 1
                        elif state == '':
                            verifiable_cmds -= 1  # Task doesn't exist on this system
                    else:
                        verifiable_cmds -= 1

            # 4. Check fsutil (via cached fsutil from PS scan - no subprocess!)
            elif cmd_lower.startswith('fsutil behavior set'):
                try:
                    parts = shlex.split(cmd, posix=False)
                    parts = [p.strip('"') for p in parts]
                    if len(parts) >= 5:
                        prop = parts[3]
                        val = parts[4]
                        verifiable_cmds += 1
                        fsu_cache = getattr(self, '_custom_cache', {}).get('fsutil', {})
                        cached_output = fsu_cache.get(prop, '')
                        if cached_output and re.search(rf'=\s*{re.escape(val)}\b', cached_output):
                            applied_cmds += 1
                        elif not cached_output:
                            verifiable_cmds -= 1
                except Exception:
                    pass
                    
            # 5. Check powercfg /change (sleep, display, disk timeouts)
            elif cmd_lower.startswith('powercfg /change') or cmd_lower.startswith('powercfg -change'):
                pass  # Handled in _check_custom via PS cache

            # 6. Check powercfg /setacvalueindex (core parking, c-states, boost, etc.)
            elif 'setacvalueindex' in cmd_lower:
                try:
                    parts = cmd.split()
                    # Format: powercfg /setacvalueindex <scheme> <subgroup> <setting> <value>
                    if len(parts) >= 6:
                        scheme, subgroup, setting_guid, expected_str = parts[2], parts[3], parts[4], parts[5]
                        expected_val = int(expected_str)
                        verifiable_cmds += 1
                        try:
                            output = subprocess.check_output(
                                f'powercfg /q {scheme} {subgroup} {setting_guid}',
                                shell=True, text=True, stderr=subprocess.DEVNULL,
                                creationflags=0x08000000, timeout=10
                            )
                            # Locale-independent: extract all hex values, AC is second-to-last
                            hex_matches = re.findall(r':\s*0x([0-9a-fA-F]+)', output)
                            if len(hex_matches) >= 2 and int(hex_matches[-2], 16) == expected_val:
                                applied_cmds += 1
                        except Exception:
                            verifiable_cmds -= 1  # Can\'t query, don\'t penalize
                except Exception:
                    pass

            # 6b. Check powercfg /setdcvalueindex (battery power settings)
            elif 'setdcvalueindex' in cmd_lower:
                try:
                    parts = cmd.split()
                    if len(parts) >= 6:
                        scheme, subgroup, setting_guid, expected_str = parts[2], parts[3], parts[4], parts[5]
                        expected_val = int(expected_str)
                        verifiable_cmds += 1
                        try:
                            output = subprocess.check_output(
                                f'powercfg /q {scheme} {subgroup} {setting_guid}',
                                shell=True, text=True, stderr=subprocess.DEVNULL,
                                creationflags=0x08000000, timeout=10
                            )
                            # Locale-independent: extract all hex values, DC is last
                            hex_matches = re.findall(r':\s*0x([0-9a-fA-F]+)', output)
                            if len(hex_matches) >= 1 and int(hex_matches[-1], 16) == expected_val:
                                applied_cmds += 1
                        except Exception:
                            verifiable_cmds -= 1
                except Exception:
                    pass

            # 7. netsh commands - handled in _check_custom
            elif cmd_lower.startswith('netsh'):
                pass  # Handled in _check_custom via PS cache

            # 8. powershell commands - handled in _check_custom  
            elif 'powershell' in cmd_lower:
                pass  # Handled in _check_custom via PS cache

            # 9. bcdedit commands - handled in _check_custom
            elif cmd_lower.startswith('bcdedit'):
                pass  # Handled in _check_custom via bcdedit cache

            # 10. powercfg -attributes (just unhiding settings)
            elif 'powercfg' in cmd_lower and '-attrib' in cmd_lower:
                pass  # Just unhiding a setting, no verification needed

            # 11. powercfg /setactive (just activating scheme)
            elif 'powercfg' in cmd_lower and 'setactive' in cmd_lower:
                pass  # Handled in _check_custom

            # 12. powercfg -h (hibernation toggle)
            elif 'powercfg' in cmd_lower and '-h' in cmd_lower:
                pass  # Handled in _check_custom

            # 13. cmd /c del (cleanup - one-shot, no state)
            elif cmd_lower.startswith('cmd /c del') or cmd_lower.startswith('cmd /c rd'):
                pass  # Cleanup, no persistent state

            # 14. ipconfig, net stop/start - one-shot
            elif any(cmd_lower.startswith(x) for x in ['ipconfig', 'net stop', 'net start']):
                pass  # One-shot commands

            # 15. sc stop (without config) - just stopping, separate from disabling  
            elif cmd_lower.startswith('sc stop'):
                pass  # Just stopping a service, not changing startup type

        # If we verified at least one command and ALL verified commands are applied, return True
        # If there are no verifiable commands, we can't be sure, so return False
        if verifiable_cmds > 0 and verifiable_cmds == applied_cmds:
            return True
        return False

    # ═════════════════════ Reverse / Restore Commands ═════════════════════
    def _generate_reverse_cmds(self, tweak):
        """Generate reverse commands to undo/restore a tweak back to Windows defaults."""
        # If the tweak has explicit hand-crafted reverse commands, use those
        if "reverse" in tweak and tweak["reverse"]:
            return list(tweak["reverse"])

        # Otherwise, auto-generate reverse commands from the apply commands
        reverse = []
        for cmd in tweak["cmds"]:
            cmd_lower = cmd.lower().strip()

            # Registry add †’ delete the value (restores to Windows default)
            if cmd_lower.startswith('reg add'):
                try:
                    parts = shlex.split(cmd, posix=False)
                    parts = [p.strip('"') for p in parts]
                    key_path = parts[2]
                    if '/v' in parts:
                        vn = parts[parts.index('/v') + 1]
                        reverse.append(f'reg delete "{key_path}" /v "{vn}" /f')
                    elif '/ve' in parts:
                        reverse.append(f'reg delete "{key_path}" /ve /f')
                except Exception:
                    pass

            # Service disable †’ re-enable as manual (demand) start
            elif cmd_lower.startswith('sc config') and 'start= disabled' in cmd_lower:
                m = re.search(r'sc config\s+(\S+)\s+start=\s*disabled', cmd, re.IGNORECASE)
                if m:
                    svc = m.group(1).strip('"')
                    reverse.append(f'sc config {svc} start= demand')

            # Service stop †’ start it back
            elif cmd_lower.startswith('sc stop'):
                parts = cmd.split()
                if len(parts) >= 3:
                    svc = parts[2].strip('"')
                    reverse.append(f'sc start {svc}')

            # Scheduled task disable †’ enable
            elif cmd_lower.startswith('schtasks /change') and '/disable' in cmd_lower:
                reverse.append(re.sub(r'/[Dd]isable', '/Enable', cmd))

            # bcdedit /set X Y †’ bcdedit /deletevalue X
            elif cmd_lower.startswith('bcdedit /set'):
                parts = cmd.split()
                if len(parts) >= 3:
                    reverse.append(f'bcdedit /deletevalue {parts[2]}')

            # bcdedit /timeout X - restore default 30s
            elif cmd_lower.startswith('bcdedit /timeout'):
                reverse.append('bcdedit /timeout 30')

            # --- Advanced Reverse Inference for PowerShell & Powercfg ---
            elif 'powercfg' in cmd_lower:
                if '/h off' in cmd_lower or '-h off' in cmd_lower:
                    reverse.append('powercfg /h on')
                elif 'idledisable' in cmd_lower:
                    reverse.append(cmd.replace(' 1', ' 0'))
                elif 'procthrottlemin' in cmd_lower:
                    reverse.append(cmd.replace(' 100', ' 5'))
                elif 'procthrottlemax' in cmd_lower:
                    pass  # PROCTHROTTLEMAX default is 100, same as our value
                    
            elif 'powershell' in cmd_lower:
                if 'disable-computerrestore' in cmd_lower:
                    reverse.append(cmd.replace('Disable-ComputerRestore', 'Enable-ComputerRestore'))
                elif 'disable-mmagent' in cmd_lower:
                    reverse.append(cmd.replace('Disable-MMAgent', 'Enable-MMAgent'))
                elif 'disable-netadapterrsc' in cmd_lower:
                    reverse.append(cmd.replace('Disable-', 'Enable-'))
                elif 'set-netadapteradvancedproperty' in cmd_lower:
                    if "'disabled'" in cmd_lower:
                        reverse.append(cmd.replace("'Disabled'", "'Enabled'"))
                    elif "registryvalue '0'" in cmd_lower:
                        reverse.append(cmd.replace("'0'", "'1'"))
                elif 'devicepriority' in cmd_lower:
                    reverse.append(cmd.replace(' 3 ', ' 0 '))  # 0 is 'Undefined'

            # netsh ... disabled → enabled (generic)
            elif cmd_lower.startswith('netsh') and 'disabled' in cmd_lower:
                reverse.append(cmd.replace('disabled', 'enabled').replace('Disabled', 'Enabled'))

            # bcdedit /deletevalue, cmd /c del: Cannot safely auto-reverse

        # Reverse the list so undo operations run in the correct order.
        # E.g. original: [sc stop X, sc config X start= disabled]
        # Naive reverse: [sc start X, sc config X start= demand] † wrong: can't start a disabled service
        # Reversed list:  [sc config X start= demand, sc start X] † correct order
        reverse.reverse()
        return reverse

    def _check_for_updates(self):
        try:
            url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                latest_version = data.get("tag_name", "")
                
                if latest_version and latest_version.lstrip('v') != APP_VERSION.lstrip('v'):
                    standalone_exe_url = ""
                    for asset in data.get("assets", []):
                        name = asset.get("name", "")
                        # Prioritize the standalone optimizer exe, NOT the setup
                        if name == "NormieTools.exe":
                            standalone_exe_url = asset.get("browser_download_url")
                            break
                    
                    if standalone_exe_url and standalone_exe_url.startswith('https://github.com/'):
                        self.root.after(2000, lambda: self._prompt_update(latest_version, standalone_exe_url))
        except Exception as e:
            print(f"Update check failed: {e}")

    def _prompt_update(self, latest_version, download_url):
        if messagebox.askyesno(_t("update_title"), _t("update_msg", v=latest_version), parent=self.root):
            # Create UI safely on the main thread before spawning the background worker
            progress_win = tk.Toplevel(self.root)
            progress_win.title("Updating...")
            progress_win.geometry("380x120")
            progress_win.configure(bg="#0a0a0a")
            progress_win.attributes("-topmost", True)
            progress_win.overrideredirect(True)
            
            w, h = 380, 120
            x = (progress_win.winfo_screenwidth() // 2) - (w // 2)
            y = (progress_win.winfo_screenheight() // 2) - (h // 2)
            progress_win.geometry(f"{w}x{h}+{x}+{y}")

            tk.Label(progress_win, text=_t("update_patching"), font=("Arial Black", 10), bg="#0a0a0a", fg="#FF1A00").pack(pady=(18, 6))
            status_lbl = tk.Label(progress_win, text=_t("update_starting"), font=("Courier New", 8), bg="#0a0a0a", fg="#00DDFF")
            status_lbl.pack()
            progress_win.grab_set()  # Modal: block interaction with main window during update
            
            threading.Thread(target=self._download_and_apply_patch, args=(download_url, progress_win, status_lbl), daemon=True).start()

    def _download_and_apply_patch(self, url, progress_win, status_lbl):
        try:
            def update_ui(txt, pct):
                # Safely queue UI updates to the main thread
                self.root.after(0, lambda: status_lbl.configure(text=txt))

            # Download using chunks for smoother UI
            temp_new_exe = os.path.join(os.environ["TEMP"], "NormieTools_New_Version.exe")
            # Clean up any stale temp file from a previous failed download
            if os.path.exists(temp_new_exe):
                try:
                    os.remove(temp_new_exe)
                except OSError:
                    pass
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            
            with urllib.request.urlopen(req, timeout=30) as response:
                total_size = int(response.headers.get('Content-Length', 0))
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
                            update_ui(_t("update_dl", p=int(percent)), percent)
                        else:
                            update_ui(_t("update_dl_kb", kb=downloaded // 1024), 0)

            update_ui(_t("update_applying"), 100)

            # Verify download integrity: size must match Content-Length
            if total_size > 0:
                actual_size = os.path.getsize(temp_new_exe)
                if actual_size != total_size:
                    raise RuntimeError(f"Download corrupted: expected {total_size} bytes, got {actual_size}")

            time.sleep(1)

            if getattr(sys, 'frozen', False):
                current_exe = sys.executable
            else:
                current_exe = __file__
                
            if not getattr(sys, 'frozen', False):
                self.root.after(0, lambda: messagebox.showwarning(_t("update_dev_title"), _t("update_dev_msg"), parent=self.root))
                self.root.after(0, progress_win.destroy)
                return

            # ═════════════════════════ Deep-fix hot swap ══════════════════════════
            current_pid  = os.getpid()
            # current_exe already set above (sys.executable, validated frozen)

            # We use a VBScript wrapper to launch the PowerShell script completely
            # detached from the current process tree, ensuring it survives when we exit.
            vbs_script = os.path.join(os.environ["TEMP"], "vault_launcher.vbs")
            ps_script = os.path.join(os.environ["TEMP"], "vault_launcher.ps1")
            
            with open(ps_script, "w", encoding="utf-8") as f:
                f.write(f"""# vault_launcher.ps1  ”  written by Tools by MedCherif patcher
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

# Self-delete scripts
Remove-Item -LiteralPath '{vbs_script.replace("'", "''")}' -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath $MyInvocation.MyCommand.Path -Force -ErrorAction SilentlyContinue
""")

            with open(vbs_script, "w", encoding="utf-8") as f:
                f.write(f'''Set objShell = CreateObject("WScript.Shell")
objShell.Run "powershell.exe -NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File """ & "{ps_script}" & """", 0, False
''')

            # Launch the VBScript using wscript.exe (which naturally detaches)
            os.startfile(vbs_script)
            
            # Force exit immediately so the PowerShell script can proceed
            os._exit(0)

        except Exception as e:
            # Clean up partial download on failure
            try:
                if os.path.exists(temp_new_exe):
                    os.remove(temp_new_exe)
            except (OSError, UnboundLocalError):
                pass
            err_msg = str(e)
            self.root.after(0, lambda m=err_msg: messagebox.showerror(_t("update_err_title"), _t("update_err_msg", e=m), parent=self.root))
            self.root.after(0, progress_win.destroy)

    # ═══════════════════════════════ Music ════════════════════════════════
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
                self.root.after(0, lambda: self.music_btn.configure(text=_t("audio_na")))
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
                self.root.after(0, lambda: self.music_btn.configure(text=_t("audio_na")))
                return
            
            file_size = os.path.getsize(mp3)
            if file_size < 1000:  # Really small files are likely placeholders
                self.music_error = f"MP3 placeholder (only {file_size} bytes). Replace with real audio file."
                print(self.music_error)
                self.root.after(0, lambda: self.music_btn.configure(text=_t("audio_na")))
                return
            
            pygame.mixer.music.load(mp3)
            pygame.mixer.music.set_volume(0.35)
            pygame.mixer.music.play(-1)
            print(f"œ“ Music loaded and playing: {mp3}")
            self.root.after(0, lambda: self.music_btn.configure(text=_t("audio_on")))
        except Exception as e:
            self.music_error = f"Music error: {str(e)}"
            print(self.music_error)
            self.root.after(0, lambda: self.music_btn.configure(text=_t("audio_na")))

    def _animate_marquee(self):
        """Scrolling marquee for the now-playing song name."""
        try:
            if not self.root.winfo_exists():
                return  # App closed, stop animation loop
            if not self._marquee_paused:
                self._marquee_offset -= 1
                self._marquee_canvas.coords(self._marquee_text_id, self._marquee_offset, 9)
                # Get text width; reset when fully scrolled off
                bbox = self._marquee_canvas.bbox(self._marquee_text_id)
                if bbox and bbox[2] < 0:
                    self._marquee_offset = 180
            self.root.after(35, self._animate_marquee)
        except Exception:
            pass  # Widget destroyed

    def _set_specs_text(self, raw):
        t = self.specs_text
        t.config(state="normal")
        t.delete("1.0", "end")
        # Configure colored tags for section headers
        t.tag_configure("section", foreground="#FF1A00", font=("Courier New", 8, "bold"))
        t.tag_configure("separator", foreground="#660A00")
        t.tag_configure("label", foreground="#00DDFF", font=("Courier New", 8, "bold"))
        t.tag_configure("value", foreground="#AAAAAA", font=("Courier New", 8))
        t.tag_configure("bar_fill", foreground="#FF1A00")
        t.tag_configure("bar_empty", foreground="#333333")
        t.tag_configure("warn", foreground="#FFD700")
        t.tag_configure("good", foreground="#00FF88")
        t.tag_configure("bad", foreground="#FF4444")
        if raw in ("loading...", "synchronizing...", _t("syncing")):
            t.insert("end", _t("syncing_long") + "\n")
        else:
            for line in raw.split("\n"):
                stripped = line.rstrip()
                if stripped.startswith("[SECTION]"):
                    label = stripped.replace("[SECTION]", "").strip()
                    t.insert("end", f"{'=' * 40}\n", "separator")
                    t.insert("end", f"  {label}\n", "section")
                    t.insert("end", f"{'=' * 40}\n", "separator")
                elif stripped.startswith("[BAR]"):
                    # Format: [BAR]label|used|total|unit
                    parts = stripped.replace("[BAR]", "").split("|")
                    if len(parts) >= 4:
                        lbl, used, total, unit = parts[0], float(parts[1]), float(parts[2]), parts[3]
                        pct = (used / total * 100) if total > 0 else 0
                        bar_len = 20
                        filled = int(pct / 100 * bar_len)
                        bar_f = "\u2588" * filled
                        bar_e = "\u2591" * (bar_len - filled)
                        t.insert("end", f"  {lbl}: ", "label")
                        t.insert("end", bar_f, "bar_fill")
                        t.insert("end", bar_e, "bar_empty")
                        tag = "bad" if pct > 90 else ("warn" if pct > 75 else "good")
                        t.insert("end", f" {pct:.0f}% ", tag)
                        t.insert("end", f"({used:.1f}/{total:.1f} {unit})\n", "value")
                elif stripped.startswith("[STATUS]"):
                    parts = stripped.replace("[STATUS]", "").split("|")
                    if len(parts) >= 3:
                        lbl, val, state = parts[0], parts[1], parts[2].strip()
                        t.insert("end", f"  {lbl}: ", "label")
                        tag = "good" if state == "OK" else ("bad" if state == "BAD" else "warn")
                        t.insert("end", f"{val}\n", tag)
                else:
                    if stripped == "":
                        t.insert("end", "\n")
                    else:
                        # Split on first ": " for label:value coloring
                        if ": " in stripped:
                            idx = stripped.index(": ")
                            lbl_part = stripped[:idx + 2]
                            val_part = stripped[idx + 2:]
                            t.insert("end", f"  {lbl_part}", "label")
                            t.insert("end", f"{val_part}\n", "value")
                        else:
                            t.insert("end", f"  {stripped}\n", "value")
        t.config(state="disabled")

    def _load_specs(self):
        try:
            cmd = r'''
$ErrorActionPreference = "SilentlyContinue"

$os  = Get-CimInstance Win32_OperatingSystem
$cs  = Get-CimInstance Win32_ComputerSystem
$cpu = Get-CimInstance Win32_Processor

# === SYSTEM ===
Write-Output "[SECTION] SYSTEM"
Write-Output ("OS: " + $os.Caption)
$dispVer = (Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion" -ErrorAction SilentlyContinue).DisplayVersion
if ($dispVer) { Write-Output ("Version: " + $dispVer + " (Build " + $os.BuildNumber + " | " + $os.Version + ")") }
else { Write-Output ("Build: " + $os.BuildNumber + " (" + $os.Version + ")") }
Write-Output ("Arch: " + $os.OSArchitecture)
Write-Output ("Host: " + $env:COMPUTERNAME + " | User: " + $env:USERNAME)
$sysType = $cs.PCSystemType
$typeStr = switch ($sysType) { 1 {"Desktop"} 2 {"Laptop"} 3 {"Workstation"} 4 {"Enterprise Server"} 5 {"SOHO Server"} 8 {"Tablet"} default {"Other"} }
if ($cs.Model -match "Virtual|VMware|VirtualBox|Hyper-V|QEMU") { $typeStr = "Virtual Machine" }
Write-Output ("Type: " + $typeStr + " | " + $cs.Manufacturer + " " + $cs.Model)
Write-Output ("Installed: " + $os.InstallDate.ToString("yyyy-MM-dd"))
$uptime = (Get-Date) - $os.LastBootUpTime
$uptimeStr = [string]::Format("{0}d {1}h {2}m", $uptime.Days, $uptime.Hours, $uptime.Minutes)
Write-Output ("Uptime: " + $uptimeStr + " (Boot: " + $os.LastBootUpTime.ToString("yyyy-MM-dd HH:mm") + ")")
$lic = (Get-CimInstance SoftwareLicensingProduct | Where-Object { $_.PartialProductKey -and $_.LicenseStatus -eq 1 } | Select-Object -First 1)
if ($lic) { Write-Output "[STATUS]Activation|Licensed (Genuine)|OK" }
else { Write-Output "[STATUS]Activation|Not Activated|BAD" }
Write-Output ""

# === CPU ===
Write-Output "[SECTION] PROCESSOR"
Write-Output ("CPU: " + $cpu.Name.Trim())
Write-Output ("Cores: " + $cpu.NumberOfCores + " | Threads: " + $cpu.NumberOfLogicalProcessors)
Write-Output ("Base Clock: " + $cpu.MaxClockSpeed + " MHz")
Write-Output ("Socket: " + $cpu.SocketDesignation)
Write-Output ("Cache: L2 " + [math]::Round($cpu.L2CacheSize / 1024, 1) + " MB | L3 " + [math]::Round($cpu.L3CacheSize / 1024, 1) + " MB")
$cpuLoad = $cpu.LoadPercentage
if ($cpuLoad -ne $null) { Write-Output ("[BAR]CPU Load|" + $cpuLoad + "|100|%") }
Write-Output ""

# === MEMORY ===
Write-Output "[SECTION] MEMORY"
$ramTotalGB = [math]::Round($cs.TotalPhysicalMemory / 1GB, 2)
$ramFreeGB  = [math]::Round($os.FreePhysicalMemory / 1MB, 2)
$ramUsedGB  = [math]::Round($ramTotalGB - $ramFreeGB, 2)
Write-Output ("[BAR]RAM|" + $ramUsedGB + "|" + $ramTotalGB + "|GB")
$sticks = Get-CimInstance Win32_PhysicalMemory
foreach ($s in $sticks) {
    $cap  = [math]::Round($s.Capacity / 1GB, 0)
    $spd  = $s.ConfiguredClockSpeed
    $smfType = $s.SMBIOSMemoryType
    $type = switch ($smfType) { 20 {"DDR"} 21 {"DDR2"} 24 {"DDR3"} 26 {"DDR4"} 34 {"DDR5"} default {"DDR"} }
    Write-Output ("Stick: " + $s.DeviceLocator + " | " + $cap + "GB " + $type + " @ " + $spd + " MHz")
}
$pageFile = Get-CimInstance Win32_PageFileUsage -ErrorAction SilentlyContinue
if ($pageFile) {
    $pfUsed = [math]::Round($pageFile.CurrentUsage / 1024, 1)
    $pfTotal = [math]::Round($pageFile.AllocatedBaseSize / 1024, 1)
    Write-Output ("[BAR]PageFile|" + $pfUsed + "|" + $pfTotal + "|GB")
}
Write-Output ""

# === GPU ===
Write-Output "[SECTION] GRAPHICS"
$gpus = Get-CimInstance Win32_VideoController
foreach ($g in $gpus) {
    Write-Output ("GPU: " + $g.Name)
    $details = @()
    if ($g.AdapterRAM -gt 0) { $details += ("VRAM: " + [math]::Round($g.AdapterRAM / 1GB, 1) + " GB") }
    if ($g.CurrentHorizontalResolution -gt 0) { $details += ($g.CurrentHorizontalResolution.ToString() + "x" + $g.CurrentVerticalResolution.ToString() + " @ " + $g.CurrentRefreshRate.ToString() + "Hz") }
    if ($details.Count -gt 0) { Write-Output ("  " + ($details -join " | ")) }
    Write-Output ("Driver: " + $g.DriverVersion + " (" + $g.DriverDate.ToString("yyyy-MM-dd") + ")")
}
Write-Output ""

# === STORAGE ===
Write-Output "[SECTION] STORAGE"
$disks = Get-CimInstance Win32_DiskDrive
foreach ($d in $disks) {
    $sizeGB = [math]::Round($d.Size / 1GB, 0)
    $mediaType = $d.MediaType
    if ($mediaType -match "Fixed") { $mediaType = "Fixed" }
    Write-Output ("Drive: " + $d.Model + " (" + $sizeGB + " GB, " + $d.InterfaceType + ")")
}

$vols = Get-CimInstance Win32_LogicalDisk | Where-Object { $_.DriveType -eq 3 }
foreach ($v in $vols) {
    $free = [math]::Round($v.FreeSpace / 1GB, 1)
    $tot  = [math]::Round($v.Size / 1GB, 1)
    $used = [math]::Round($tot - $free, 1)
    Write-Output ("[BAR]" + $v.DeviceID + "|" + $used + "|" + $tot + "|GB")
}
Write-Output ""

# === MOTHERBOARD ===
Write-Output "[SECTION] MOTHERBOARD"
$mb = Get-CimInstance Win32_BaseBoard
$bios = Get-CimInstance Win32_BIOS
Write-Output ("Board: " + $mb.Manufacturer + " " + $mb.Product)
Write-Output ("BIOS: " + $bios.SMBIOSBIOSVersion + " (" + $bios.ReleaseDate.ToString("yyyy-MM-dd") + ")")
$tpm = Get-CimInstance -Namespace "root\cimv2\Security\MicrosoftTpm" -ClassName Win32_Tpm -ErrorAction SilentlyContinue
if ($tpm) {
    $tpmVer = $tpm.SpecVersion
    if ($tpmVer) { $tpmVer = $tpmVer.Split(",")[0].Trim() }
    Write-Output "[STATUS]TPM|v$tpmVer Present|OK"
} else { Write-Output "[STATUS]TPM|Not Detected|WARN" }
$sb = Confirm-SecureBootUEFI -ErrorAction SilentlyContinue
if ($sb -eq $true) { Write-Output "[STATUS]Secure Boot|Enabled|OK" }
elseif ($sb -eq $false) { Write-Output "[STATUS]Secure Boot|Disabled|WARN" }
else { Write-Output "[STATUS]Secure Boot|N/A (Legacy BIOS)|WARN" }
Write-Output ""

# === NETWORK ===
Write-Output "[SECTION] NETWORK"
$nics = Get-CimInstance Win32_NetworkAdapter | Where-Object { $_.PhysicalAdapter -eq $true -and $_.NetConnectionStatus -ne $null }
foreach ($n in $nics) {
    $cfg = Get-CimInstance Win32_NetworkAdapterConfiguration | Where-Object { $_.Index -eq $n.DeviceID }
    $status = if ($n.NetConnectionStatus -eq 2) { "Connected" } else { "Disconnected" }
    Write-Output ("NIC: " + $n.Name)
    $nicDetails = @()
    if ($cfg.IPAddress) { $nicDetails += ("IP: " + ($cfg.IPAddress[0])) }
    if ($n.Speed -gt 0) { $nicDetails += ("Speed: " + [math]::Round($n.Speed / 1MB, 0) + " Mbps") }
    $nicDetails += $status
    Write-Output ("  " + ($nicDetails -join " | "))
    if ($cfg.MACAddress) { Write-Output ("  MAC: " + $cfg.MACAddress) }
}
Write-Output ""

# === AUDIO & DISPLAY ===
Write-Output "[SECTION] PERIPHERALS"
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
    Write-Output ("[BAR]Battery|" + $batt.EstimatedChargeRemaining + "|100|%")
    Write-Output ("  Status: " + $status)
} else {
    Write-Output "Power: AC (No battery)"
}
Write-Output ""

# === SECURITY ===
Write-Output "[SECTION] SECURITY"
$fw = Get-NetFirewallProfile -ErrorAction SilentlyContinue
if ($fw) {
    $fwOn = ($fw | Where-Object { $_.Enabled -eq $true }).Count
    $fwTotal = $fw.Count
    if ($fwOn -eq $fwTotal) { Write-Output "[STATUS]Firewall|All Profiles Enabled ($fwOn/$fwTotal)|OK" }
    else { Write-Output "[STATUS]Firewall|$fwOn/$fwTotal Profiles Enabled|WARN" }
}
$def = Get-MpComputerStatus -ErrorAction SilentlyContinue
if ($def) {
    if ($def.RealTimeProtectionEnabled) { Write-Output "[STATUS]Defender|Real-Time Protection ON|OK" }
    else { Write-Output "[STATUS]Defender|Real-Time Protection OFF|BAD" }
    if ($def.AntivirusSignatureLastUpdated) {
        $sigAge = ((Get-Date) - $def.AntivirusSignatureLastUpdated).Days
        if ($sigAge -le 3) { Write-Output "[STATUS]Signatures|Updated $sigAge days ago|OK" }
        else { Write-Output "[STATUS]Signatures|Updated $sigAge days ago|WARN" }
    }
}
Write-Output ""

# === PROCESSES ===
Write-Output "[SECTION] RUNTIME"
$procCount = (Get-Process).Count
$svcCount = (Get-Service | Where-Object { $_.Status -eq "Running" }).Count
Write-Output ("Processes: " + $procCount + " running")
Write-Output ("Services: " + $svcCount + " active")
$startups = Get-CimInstance Win32_StartupCommand -ErrorAction SilentlyContinue
if ($startups) { Write-Output ("Startup Items: " + $startups.Count) }
'''
            output = subprocess.check_output(
                ["powershell", "-NoProfile", "-NonInteractive", "-Command", cmd],
                text=True, creationflags=subprocess.CREATE_NO_WINDOW, timeout=30
            )
            self.root.after(0, lambda t=output.strip(): self._set_specs_text(t))
        except Exception as e:
            err_msg = str(e)
            self.root.after(0, lambda m=err_msg: self._set_specs_text(f"Failed to load specs.\n{m}"))

    # ═════════════════════════ Category Switching ═════════════════════════
    # ═════════════════════════ Tweak Card Builder ═════════════════════════
    # ══════════════════════════════ Tooltip ═══════════════════════════════
    def _show_tooltip(self, event, text, color):
        self._hide_tooltip()
        x = event.widget.winfo_rootx() + 20
        y = event.widget.winfo_rooty() + 26
        # Clamp to screen bounds so tooltip doesn't go off-screen
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        if x + 270 > screen_w:
            x = screen_w - 280
        if x < 0:
            x = 5
        if y + 60 > screen_h:
            y = event.widget.winfo_rooty() - 40
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

    # ═══════════════════════════════ Scroll ═══════════════════════════════


    # ═════════════════════════════ Selection ══════════════════════════════
    def _select_all(self, e=None):
        for var, _ in self.tweak_vars.values():
            var.set(True)
        self._update_stats()

    def _deselect_all(self, e=None):
        for var, _ in self.tweak_vars.values():
            var.set(False)
        self._update_stats()

    def _on_lang_change(self, selection):
        global _current_lang
        _current_lang = LANG_CODES.get(selection, "en")
        self._refresh_lang()

    def _refresh_lang(self):
        """Refresh ALL translatable text in the UI."""
        self.root.title(_t("app_title", v=APP_VERSION))
        self.header_lbl.configure(text=_t("header", v=APP_VERSION))

        # Music button
        if self.music_error:
            self.music_btn.configure(text=_t("audio_na"))
        elif self.music_on:
            self.music_btn.configure(text=_t("audio_on"))
        else:
            self.music_btn.configure(text=_t("audio_off"))

        self.fb_btn.configure(text=_t("feedback_btn"))
        self.lang_lbl.configure(text=_t("lang_label"))
        self.specs_hdr.configure(text=_t("specs_header"))
        self.tweaks_hdr.configure(text=_t("tweaks_header"))

        # Category headers
        for cat_name, lbl in self._cat_labels.items():
            lbl.configure(text=f"// {_cat(cat_name).upper()}")

        # Tweak checkboxes
        for tw_name, chk in self._tweak_chks.items():
            chk.configure(text=_tn(tw_name))

        # Risk labels
        for tw_name, rl in self._risk_labels.items():
            _, tw = self.tweak_vars[tw_name]
            rl.configure(text=_risk_text(tw["risk"]))

        # Applied labels
        for tw_name, al in self.tweak_applied_lbls.items():
            if tw_name in self.initially_applied:
                al.configure(text=_t("applied"))

        # Tool name & description labels
        for tw_name, nl in self._tool_name_lbls.items():
            display_name = _tn(tw_name)
            for prefix in ["Install ", "Installer ", "Instalar ", "\u062a\u062b\u0628\u064a\u062a "]:
                if display_name.startswith(prefix):
                    display_name = display_name[len(prefix):]
                    break
            if display_name.endswith(" installieren"):
                display_name = display_name[:-len(" installieren")]
            nl.configure(text=display_name)
        for tw_name, dl in self._tool_desc_lbls.items():
            dl.configure(text=_td(tw_name))

        # Bottom bar
        self.sel_all_btn.configure(text=_t("select_all"))
        self.purge_btn.configure(text=_t("purge"))
        self.exec_btn.configure(text=f">> {_t('execute')} <<")
        self._update_stats()

    def _update_stats(self):
        to_apply = sum(1 for var, tw in self.tweak_vars.values()
                       if var.get() and tw["name"] not in self.initially_applied)
        to_restore = sum(1 for name in self.initially_applied
                         if name in self.tweak_vars and not self.tweak_vars[name][0].get())
        total = len(self.tweak_vars)
        self.stats_lbl.configure(text=_t("stats", a=to_apply, r=to_restore, t=total))

    # ════════════════════════════ Music Toggle ════════════════════════════
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
            messagebox.showinfo("Music", self.music_error, parent=self.root)
            return

        self.music_on = not self.music_on
        if pygame is None:
            self.music_on = False
            self.music_error = "pygame not available"
            try:
                self.music_btn.configure(text=_t("audio_na"))
            except Exception:
                pass
            return

        try:
            if self.music_on:
                pygame.mixer.music.unpause()
                self.music_btn.configure(text=_t("audio_on"))
                self._marquee_paused = False
            else:
                pygame.mixer.music.pause()
                self.music_btn.configure(text=_t("audio_off"))
                self._marquee_paused = True
        except Exception:
            pass

    # ════════════════════════════ Apply Logic ═════════════════════════════
    def _apply(self):
        if self._applying:
            return  # Guard against double-click while batch is running
        # Warn if not admin — tweaks will silently fail
        if not is_admin():
            messagebox.showwarning(
                "Not Admin",
                "This app is NOT running as Administrator.\n\n"
                "Tweaks will fail silently. Please restart as admin.",
                parent=self.root)
            return
        # Only process tweaks that are checked AND not already applied
        selected = [(var, tw) for var, tw in self.tweak_vars.values() if var.get() and tw["name"] not in self.initially_applied]

        # Detect tweaks to RESTORE (were applied at startup, now unchecked)
        to_restore = []
        for name in list(self.initially_applied):
            if name in self.tweak_vars:
                var, tw = self.tweak_vars[name]
                if not var.get():
                    to_restore.append(tw)

        if not selected and not to_restore:
            messagebox.showwarning(_t("nothing_title"), _t("nothing_msg"), parent=self.root)
            return

        # Check for mutually exclusive tweak conflicts
        sel_names = {tw["name"] for _, tw in selected}
        _conflict_pairs = [
            ("Force Disable Fullscreen Optimizations (Global)", "Force True Exclusive Fullscreen"),

        ]
        for a, b in _conflict_pairs:
            if a in sel_names and b in sel_names:
                messagebox.showerror(_t("conflict_title"), _t("conflict_msg", a=_tn(a), b=_tn(b)), parent=self.root)
                return

        # Build confirmation message
        msg = ""
        if selected:
            msg += _t("confirm_apply", n=len(selected))
            high_risk = [tw["name"] for _, tw in selected if tw["risk"] == HIGH]
            if high_risk:
                msg += _t("confirm_high")
                for h in high_risk:
                    msg += f"   \u2022 {_tn(h)}\n"
                msg += _t("confirm_high_warn")

        if to_restore:
            msg += _t("confirm_restore", n=len(to_restore))
            for tw in to_restore:
                msg += f"   \u2022 {_tn(tw['name'])}\n"
            msg += _t("confirm_defaults")

        msg += _t("confirm_footer")

        if not messagebox.askyesno(_t("confirm_title"), msg, parent=self.root):
            return

        # Show apply overlay immediately
        try:
            self._show_apply_overlay(len(selected), len(to_restore))
        except Exception:
            self._close_apply_overlay()

        # Run in thread so UI doesn't freeze
        self._applying = True
        threading.Thread(target=self._run_tweaks, args=(selected, to_restore), daemon=True).start()

    def _run_tweaks(self, selected, to_restore=None):
        if to_restore is None:
            to_restore = []

        def _finish_applying():
            self._applying = False

        try:
            self.__run_tweaks_inner(selected, to_restore)
        except Exception as e:
            self._close_apply_overlay()
            err_msg = str(e)
            self.root.after(0, lambda m=err_msg: messagebox.showerror(_t("exec_err_title"), _t("exec_err_msg", e=m), parent=self.root))
        finally:
            self.root.after(0, _finish_applying)


    # ═══════════════════════════ Apply overlay ════════════════════════════
    def _show_apply_overlay(self, apply_count, restore_count):
        """Overlay shown while tweaks are being prepared."""
        _RED = "#FF1A00"
        _CYAN = "#00DDFF"
        ov = tk.Toplevel(self.root)
        self._overlay = ov  # assign early so cleanup works if widget creation fails
        self._ov_anim_id = None
        ov.overrideredirect(True)
        ov.attributes("-topmost", True)
        ov.configure(bg="#000000")
        w, h = 420, 200
        sx = self.root.winfo_x() + (self.root.winfo_width() - w) // 2
        sy = self.root.winfo_y() + (self.root.winfo_height() - h) // 2
        ov.geometry(f"{w}x{h}+{sx}+{sy}")
        border = tk.Frame(ov, bg=_RED, padx=2, pady=2)
        border.pack(fill="both", expand=True)
        inner = tk.Frame(border, bg="#050505")
        inner.pack(fill="both", expand=True, padx=1, pady=1)
        tk.Label(inner, text="APPLYING TWEAKS", font=("Consolas", 14, "bold"),
                 bg="#050505", fg=_RED).pack(pady=(15, 5))
        info = f"Applying {apply_count} tweak(s)"
        if restore_count:
            info += f" | Restoring {restore_count}"
        tk.Label(inner, text=info, font=("Consolas", 10),
                 bg="#050505", fg=_CYAN).pack()
        self._ov_status = tk.Label(inner, text="Initializing...", font=("Consolas", 9),
                                   bg="#050505", fg="#888888")
        self._ov_status.pack(pady=(8, 4))
        self._ov_canvas = tk.Canvas(inner, width=360, height=18, bg="#111111",
                                    highlightthickness=1, highlightbackground=_RED)
        self._ov_canvas.pack(pady=(4, 10))
        self._ov_bar = self._ov_canvas.create_rectangle(0, 0, 0, 18, fill=_RED, outline="")
        self._ov_scan = self._ov_canvas.create_line(0, 0, 0, 18, fill=_CYAN, width=2)
        self._ov_pct = 0
        self._animate_overlay_scan()

    def _animate_overlay_scan(self):
        """Animate scan line on overlay progress bar."""
        if not hasattr(self, '_overlay') or self._overlay is None:
            return
        try:
            import math
            bar_w = 360
            scan_x = (self._ov_pct * bar_w) // 100
            offset = int(8 * math.sin(time.time() * 6))
            sx = max(0, min(bar_w, scan_x + offset))
            self._ov_canvas.coords(self._ov_scan, sx, 0, sx, 18)
            self._ov_anim_id = self._overlay.after(30, self._animate_overlay_scan)
        except Exception:
            pass

    def _update_apply_overlay(self, status=None, pct=None):
        """Thread-safe update of overlay status/progress."""
        def _do():
            if not hasattr(self, '_overlay') or self._overlay is None:
                return
            try:
                if status is not None:
                    self._ov_status.configure(text=status)
                if pct is not None:
                    self._ov_pct = pct
                    bar_w = int(360 * pct / 100)
                    self._ov_canvas.coords(self._ov_bar, 0, 0, bar_w, 18)
            except Exception:
                pass
        self.root.after(0, _do)

    def _close_apply_overlay(self):
        """Thread-safe destroy of overlay."""
        def _do():
            if hasattr(self, '_overlay') and self._overlay is not None:
                try:
                    if self._ov_anim_id:
                        self._overlay.after_cancel(self._ov_anim_id)
                    self._overlay.destroy()
                except Exception:
                    pass
                self._overlay = None
        self.root.after(0, _do)

    def __run_tweaks_inner(self, selected, to_restore):
        # Create restore point with overlay feedback
        self._update_apply_overlay(status="Creating system restore point...", pct=10)
        _rp_ok = False
        try:
            result = subprocess.run(
                'powershell -NoProfile -Command "Enable-ComputerRestore -Drive $env:SystemDrive\\; Checkpoint-Computer -Description \'Before_TheVault_Optimizer\' -RestorePointType \'MODIFY_SETTINGS\'"',
                shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=120, creationflags=0x08000000
            )
            _rp_ok = (result.returncode == 0)
        except Exception:
            pass
        if not _rp_ok:
            self.root.after(0, lambda: messagebox.showwarning(
                "Restore Point",
                "Could not create a System Restore point.\nSystem Restore may be disabled or the disk is full.\nProceeding without restore point.",
                parent=self.root))

        self._update_apply_overlay(status="Building tweak batch...", pct=60)

        applied_count = 0
        restored_count = 0

        # Build ONE SINGLE batch file with ALL commands
        _bat = os.path.join(os.environ.get("TEMP", r"C:\Windows\Temp"), "_vault_all_tweaks.bat")
        bat_lines = []
        bat_lines.append("@echo off")
        bat_lines.append("chcp 65001 >nul 2>&1")
        bat_lines.append(f"title {_t('bat_title')}")
        bat_lines.append("color 0A")
        bat_lines.append("echo.")
        bat_lines.append("echo  =====================================================")
        bat_lines.append(f"echo   {_t('bat_header')}")
        bat_lines.append("echo  =====================================================")
        bat_lines.append("echo.")

        # -- Apply selected tweaks --
        for _, tw in selected:
            safe = tw["name"].replace("&", "^&").replace('"', "").replace("'", "").replace("<", "^<").replace(">", "^>").replace("|", "^|")
            bat_lines.append(f"echo  [{_t('bat_applying')}] {safe}")
            bat_lines.append("echo  -----------------------------------------")
            for cmd in tw["cmds"]:
                safe_echo = cmd[:90].replace("%", "%%").replace("&", "^&").replace("<", "^<").replace(">", "^>").replace("|", "^|")
                bat_lines.append(f"echo  ^> {safe_echo}")
                bat_lines.append(f"{cmd} 2>nul")
                bat_lines.append(f"if %errorlevel% neq 0 echo  {_t('bat_warn')} %errorlevel%")
                applied_count += 1
            bat_lines.append(f"echo  {_t('bat_ok')}")
            bat_lines.append("echo.")

        # -- Restore deselected tweaks --
        if to_restore:
            bat_lines.append("color 0E")
        for tw in to_restore:
            safe = tw["name"].replace("&", "^&").replace('"', "").replace("'", "").replace("<", "^<").replace(">", "^>").replace("|", "^|")
            reverse_cmds = self._generate_reverse_cmds(tw)
            bat_lines.append(f"echo  [{_t('bat_restoring')}] {safe}")
            bat_lines.append("echo  -----------------------------------------")
            for cmd in reverse_cmds:
                safe_echo = cmd[:90].replace("%", "%%").replace("&", "^&").replace("<", "^<").replace(">", "^>").replace("|", "^|")
                bat_lines.append(f"echo  ^> {safe_echo}")
                bat_lines.append(f"{cmd} 2>nul")
                bat_lines.append(f"if %errorlevel% neq 0 echo  {_t('bat_warn')} %errorlevel%")
                restored_count += 1
            bat_lines.append(f"echo  {_t('bat_ok_restore')}")
            bat_lines.append("echo.")

        bat_lines.append("echo  =====================================================")
        bat_lines.append(f"echo   {_t('bat_complete', a=applied_count, r=restored_count)}")
        bat_lines.append("echo  =====================================================")
        bat_lines.append("echo.")
        bat_lines.append(f"echo  {_t('bat_press_key')}")
        bat_lines.append("pause >nul")

        # Write the single batch file
        with open(_bat, "w", encoding="utf-8") as _bf:
            _bf.write("\n".join(bat_lines))

        self._update_apply_overlay(status="Launching tweaks...", pct=95)
        self._close_apply_overlay()

        # Launch ONE single visible console window for everything
        _comspec = os.environ.get("COMSPEC", r"C:\Windows\System32\cmd.exe")
        try:
            subprocess.run([_comspec, "/c", _bat], timeout=3600, creationflags=subprocess.CREATE_NEW_CONSOLE)
        except Exception:
            pass
        # Individual [WARN] lines in the console window handle per-command errors.
        # The overall batch return code is unreliable (e.g. user closing the
        # console window returns STATUS_CONTROL_C_EXIT), so no popup here.

        # Update UI for applied tweaks (thread-safe via root.after)
        for _, tw in selected:
            def _mark_applied(n=tw["name"]):
                self.initially_applied.add(n)
                if n in self.tweak_applied_lbls:
                    self.tweak_applied_lbls[n].configure(text=_t("applied"))
            self.root.after(0, _mark_applied)

        # Update UI for restored tweaks (thread-safe via root.after)
        for tw in to_restore:
            def _mark_restored(n=tw["name"]):
                self.initially_applied.discard(n)
                if n in self.tweak_applied_lbls:
                    self.tweak_applied_lbls[n].configure(text="")
            self.root.after(0, _mark_restored)

        # Build result message
        parts = []
        if selected:
            parts.append(_t("done_applied", n=len(selected), c=applied_count))
        if to_restore:
            parts.append(_t("done_restored", n=len(to_restore), c=restored_count))
        result_msg = "\n".join(parts) + _t("done_restart")

        self.root.after(0, lambda: messagebox.showinfo(_t("done_title"), result_msg, parent=self.root))


# ════════════════════════════ Entry Point ═════════════════════════════
if __name__ == "__main__":
    if not is_admin():
        try:
            # Safely rebuild arguments to handle paths with spaces, and
            # determine if running as frozen executable or python script
            args_list = sys.argv[1:] if getattr(sys, 'frozen', False) else sys.argv
            args_str = " ".join(f'"{a}"' for a in args_list)
            
            # Try to re-run with admin privileges
            script_dir = os.path.dirname(os.path.abspath(sys.argv[0])) if sys.argv else None
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, args_str, script_dir, 1)
            sys.exit()  # Exit this non-admin process; the admin version will run separately
        except Exception as e:
            print(f"š  Admin elevation failed: {e}")
            print("š  Continuing without admin (some tweaks may not work).")
            # Fall through to start the app anyway

    _running_as_admin = is_admin()
    try:
        root = tk.Tk()
        app = OptimizerApp(root)
        if not _running_as_admin:
            root.after(1000, lambda: messagebox.showwarning(
                "Not Running as Admin",
                "This app is NOT running with administrator privileges.\n\n"
                "Most tweaks require admin access and will silently fail.\n"
                "Please restart as administrator for full functionality.",
                parent=root))
        root.mainloop()
    except Exception:
        import traceback
        log = os.path.join(os.path.dirname(os.path.abspath(__file__)), "crash.log")
        with open(log, "w", encoding="utf-8") as f:
            traceback.print_exc(file=f)
        raise



