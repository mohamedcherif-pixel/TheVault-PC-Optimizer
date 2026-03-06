# Code Signing Setup (100% Free)

NormieTools uses **SignPath.io** to digitally sign both the portable EXE and the installer. This eliminates the Windows SmartScreen "Windows protected your PC" warning. **SignPath.io is free for open-source projects.**

## Why Code Signing?

Without a digital signature, Windows SmartScreen blocks every download with "Windows protected your PC". Signing the EXE with a trusted certificate eliminates this warning.

| Option | Cost | SmartScreen Trust |
|--------|------|-------------------|
| **SignPath.io** (current) | **$0** | Builds over ~30 days |
| Azure Trusted Signing | $9.99/month | Immediate |
| EV Code Signing | $300–500/year | Immediate |
| No signing | Free | ❌ Warning every time |

---

## Current Workflow: Manual Signing (Free)

The CI/CD pipeline builds unsigned binaries. After each release, sign them manually through SignPath:

### After Each Release:

1. Go to your [GitHub release](https://github.com/mohamedcherif-pixel/TheVault-PC-Optimizer/releases/latest)
2. Download `NormieTools.exe` and `NormieTools_Setup.exe`
3. Go to [SignPath.io](https://app.signpath.io) → your NormieTools project → **Submit signing request**
4. Upload `NormieTools.exe` → select your signing policy → Submit
5. Wait for signing to complete → download the signed EXE
6. Repeat for `NormieTools_Setup.exe`
7. Edit the GitHub release → delete the unsigned files → upload the signed versions
8. Update `CHECKSUMS.txt` with new SHA256 hashes of the signed files

### Verify the Signature:

Right-click the signed EXE → **Properties** → **Digital Signatures** tab → you should see a valid signature from "mohamed cherif".

---

## Automated Signing (After Foundation Approval)

To automate signing in CI/CD (no manual steps), apply for the **SignPath Foundation** plan:

1. Go to [about.signpath.io/open-source](https://about.signpath.io/open-source)
2. Submit `https://github.com/mohamedcherif-pixel/TheVault-PC-Optimizer`
3. Once approved, the Foundation plan unlocks **Trusted Build Systems** (GitHub Actions integration)
4. The `deploy.yml` workflow already has a placeholder for automated signing — just configure the secrets and it will sign automatically during CI

---

## SmartScreen Timeline

After signing:
- **Day 1**: SmartScreen may still warn (new publisher, no reputation yet)
- **Week 1–2**: Warning frequency decreases as downloads accumulate
- **Week 3–4**: Most users will no longer see the warning
- **After ~30 days**: SmartScreen fully trusts the signed binary

Each new signed release inherits reputation from the previous one.

---

## Accelerating SmartScreen Trust (Free)

1. **Submit to Microsoft for review**: [microsoft.com/en-us/wdsi/filesubmission](https://www.microsoft.com/en-us/wdsi/filesubmission) — submit your signed binary as "incorrectly detected"
2. **Submit to VirusTotal**: [virustotal.com](https://www.virustotal.com) — a clean scan from 70+ engines boosts SmartScreen confidence
3. **Consistent releases**: Regular signed releases from the same certificate build trust faster
