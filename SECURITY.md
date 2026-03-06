# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.1.x   | Yes       |
| < 1.1   | No        |

## What This App Does (Transparency)

This application:
- **Modifies Windows registry keys** using `reg add` commands
- **Configures Windows services** using `sc config` / `sc stop`
- **Adjusts network settings** using `netsh`
- **Modifies boot configuration** using `bcdedit`
- **Installs software** using `winget install` (Microsoft's official package manager)
- **Requires Administrator privileges** to apply system tweaks

This application does **NOT**:
- Collect or transmit personal data automatically
- Install drivers or kernel-level components
- Modify UEFI/BIOS settings
- Run cryptocurrency miners or ads
- Bundle third-party software

**Network activity** (user-initiated only):
- **Update checks**: Connects to GitHub API to check for new releases
- **Tool installs**: Uses `winget` (Microsoft's package manager) to download tools
- **Feedback**: If you submit feedback, it is sent via email API to the developer
- **AI Assistant**: If you use the AI chat, your messages are sent to third-party AI providers (Groq, Gemini, Cerebras, Cohere)

## Verifying Downloads

Every GitHub release includes a `CHECKSUMS.txt` file with SHA256 hashes. Verify with:

```powershell
(Get-FileHash .\NormieTools.exe -Algorithm SHA256).Hash
```

Compare the output with the hash published in the release.

## Reporting a Vulnerability

If you find a security issue, please report it responsibly:

1. **Email**: mohamedcherif.dev@outlook.com
2. **GitHub Issues**: For non-sensitive issues, open an [issue](https://github.com/mohamedcherif-pixel/TheVault-PC-Optimizer/issues)

Please include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact

## Source Code Audit

The entire application is a single Python file (`main.py`). You can read every line of code before running it. All registry keys, service names, and commands are visible in plaintext.
