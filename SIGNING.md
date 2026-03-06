# Code Signing Setup (100% Free)

NormieTools uses **SignPath.io Foundation** to digitally sign both the portable EXE and the installer. This eliminates the Windows SmartScreen "Windows protected your PC" warning. **SignPath.io Foundation is 100% free for open-source projects.**

## Why SignPath.io Foundation?

| Option | Cost | SmartScreen Trust | Notes |
|--------|------|-------------------|-------|
| **SignPath.io Foundation** | **$0 (free)** | Builds over ~30 days | Free for open-source, trusted CA certificate |
| Azure Trusted Signing | $9.99/month | Immediate | Microsoft's own PKI |
| EV Code Signing (DigiCert, Sectigo) | $300–500/year | Immediate | Hardware token required |
| No signing | Free | ❌ None | SmartScreen warning every time |

SignPath.io Foundation provides **free Authenticode code signing** for open-source projects using a trusted CA certificate. After a few releases, SmartScreen builds trust and stops showing warnings.

---

## Setup Instructions (One-Time, ~15 minutes)

### Step 1: Apply to SignPath Foundation

1. Go to [about.signpath.io/open-source](https://about.signpath.io/open-source)
2. Click **"Submit your project"**
3. Fill in:
   - **GitHub repository URL**: `https://github.com/mohamedcherif-pixel/TheVault-PC-Optimizer`
   - **Project description**: "Free, open-source Windows optimizer with 174 system tweaks and 173 tool installs"
   - **License**: MIT
4. Submit and wait for approval (typically 1–5 business days)

### Step 2: Configure Your SignPath Project

Once approved, log in to [app.signpath.io](https://app.signpath.io):

1. **Create a project** named `normietools`
2. **Create an artifact configuration** named `initial`:
   - Add a signing directive for PE files (`.exe`)
3. **Create a signing policy** named `release-signing`:
   - Set the certificate to the one provided by SignPath Foundation
   - Configure it to trigger on GitHub Actions

### Step 3: Get Your API Token

1. In SignPath dashboard, go to **Users & Teams** → **CI Tokens**
2. Create a new CI token for GitHub Actions
3. Copy the token value

### Step 4: Add GitHub Secrets & Variables

Go to your GitHub repo → **Settings** → **Secrets and variables** → **Actions**

Add one **secret**:

| Type | Name | Value |
|------|------|-------|
| Secret | `SIGNPATH_API_TOKEN` | Your CI token from Step 3 |

Add one **variable** (not secret):

| Type | Name | Value |
|------|------|-------|
| Variable | `SIGNPATH_ORG_ID` | Your SignPath organization ID (from dashboard URL) |

### Step 5: Push and Verify

Push any commit to `main`. The GitHub Actions workflow will:

1. Build `NormieTools.exe` with PyInstaller
2. Build `NormieTools_Setup.exe` with Inno Setup
3. Upload both binaries to SignPath for signing
4. Wait for SignPath to sign them
5. Replace unsigned binaries with signed ones
6. Generate SHA256 checksums of the **signed** binaries
7. Create a GitHub Release with signed artifacts

### Step 6: Verify the Signature

After downloading a signed release, right-click the EXE → **Properties** → **Digital Signatures** tab. You should see a valid Authenticode signature.

---

## How It Works in CI/CD

The signing is handled by the [`signpath/github-action-submit-signing-request`](https://github.com/signpath/github-action-submit-signing-request) GitHub Action in `.github/workflows/deploy.yml`.

Key points:
- Signing is **conditional** — if the secrets aren't configured, the build still succeeds (just without signing)
- Both the EXE and the installer are uploaded together and signed in one request
- Signed binaries replace the unsigned ones before checksum generation and release upload
- RFC 3161 timestamps ensure signatures remain valid even after the certificate expires

---

## SmartScreen Timeline

After signing:
- **Day 1**: SmartScreen may still warn (new publisher, no reputation yet)
- **Week 1–2**: Warning frequency decreases as downloads accumulate
- **Week 3–4**: Most users will no longer see the warning
- **After ~30 days**: SmartScreen fully trusts the signed binary

Each new signed release inherits reputation from the previous one, so the warning only appears briefly (if at all) on the very first signed releases.

---

## Accelerating SmartScreen Trust (Free)

To speed up reputation building, you can also:

1. **Submit your signed EXE to Microsoft for review**: Go to [microsoft.com/en-us/wdsi/filesubmission](https://www.microsoft.com/en-us/wdsi/filesubmission) and submit your binary as "incorrectly detected" software
2. **Submit to VirusTotal**: Upload to [virustotal.com](https://www.virustotal.com) — a clean scan from 70+ engines boosts SmartScreen confidence
3. **Consistent releases**: Regular signed releases from the same publisher certificate build trust faster

---

## Paid Alternative: Azure Trusted Signing

If you want **immediate** SmartScreen trust (day 1, zero waiting), consider Azure Trusted Signing ($9.99/month). It's Microsoft's own PKI, so SmartScreen trusts it instantly. See the [Azure Trusted Signing docs](https://learn.microsoft.com/en-us/azure/trusted-signing/) for setup.

---

## Troubleshooting

**"Signing step skipped"** — The `SIGNPATH_ORG_ID` variable or `SIGNPATH_API_TOKEN` secret isn't configured. Follow Steps 3–4 above.

**"Signing request denied"** — Your SignPath Foundation application may not be approved yet, or the signing policy isn't configured correctly. Check your SignPath dashboard.

**"Artifact configuration not found"** — Make sure your artifact configuration is named `initial` (matching deploy.yml) and contains a PE signing directive.

**SmartScreen still warns after signing** — This is normal for the first few releases. Submit the binary to Microsoft for review (see above) to accelerate trust building.
