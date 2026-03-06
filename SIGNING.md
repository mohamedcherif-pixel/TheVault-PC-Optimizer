# Code Signing Setup

NormieTools uses **Azure Trusted Signing** (Microsoft's own code signing service) to digitally sign both the portable EXE and the installer. This eliminates the Windows SmartScreen "Windows protected your PC" warning.

## Why Azure Trusted Signing?

| Option | Cost | SmartScreen Trust | Notes |
|--------|------|-------------------|-------|
| **Azure Trusted Signing** | ~$9.99/month | **Immediate** | Microsoft's own PKI — trusted by SmartScreen instantly |
| EV Code Signing (DigiCert, Sectigo) | $300–500/year | Immediate | Hardware token required |
| OV Code Signing | $60–200/year | Gradual (30–90 days) | Builds reputation over time |
| SignPath.io Foundation | Free (open-source) | Gradual | Requires approval process |
| No signing | Free | ❌ None | SmartScreen warning every time |

Azure Trusted Signing is the best value because it's **Microsoft's own certificate authority** — SmartScreen trusts it immediately with no reputation-building period required.

---

## Setup Instructions (One-Time)

### Step 1: Create Azure Account

1. Go to [portal.azure.com](https://portal.azure.com)
2. Create a free Azure account (if you don't have one)
3. You'll need a pay-as-you-go subscription ($9.99/month for Trusted Signing)

### Step 2: Create a Trusted Signing Account

1. In Azure Portal, search for **"Trusted Signing"**
2. Click **Create** → fill in:
   - **Subscription**: your subscription
   - **Resource group**: create new (e.g., `normietools-signing`)
   - **Account name**: e.g., `normietools-signing`
   - **Region**: pick the closest (e.g., `East US`, `West Europe`)
   - **Pricing tier**: Basic ($9.99/month)
3. Click **Review + Create** → **Create**

### Step 3: Create a Certificate Profile

1. Open your Trusted Signing account in Azure Portal
2. Go to **Certificate profiles** → **+ Add**
3. Fill in:
   - **Profile name**: e.g., `normietools-public`
   - **Profile type**: **Public Trust** (this is what SmartScreen checks)
   - **Identity validation**: Complete the identity verification process
     - You'll need to verify your identity (individual or organization)
     - For individual: government-issued ID
     - For organization: business registration documents

### Step 4: Create a Service Principal (for GitHub Actions)

Run these commands in Azure CLI (or use Azure Cloud Shell):

```bash
# Create service principal
az ad sp create-for-rbac --name "normietools-ci-signing" --role "Trusted Signing Certificate Profile Signer" --scopes "/subscriptions/<your-sub-id>/resourceGroups/normietools-signing/providers/Microsoft.CodeSigning/codeSigningAccounts/normietools-signing"
```

This outputs:
```json
{
  "appId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",      ← AZURE_CLIENT_ID
  "password": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",        ← AZURE_CLIENT_SECRET
  "tenant": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"       ← AZURE_TENANT_ID
}
```

### Step 5: Add GitHub Secrets

Go to your GitHub repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add these 6 secrets:

| Secret Name | Value |
|-------------|-------|
| `AZURE_TENANT_ID` | Tenant ID from Step 4 |
| `AZURE_CLIENT_ID` | App ID from Step 4 |
| `AZURE_CLIENT_SECRET` | Password from Step 4 |
| `TRUSTED_SIGNING_ENDPOINT` | Your account's endpoint URL (e.g., `https://eus.codesigning.azure.net`) |
| `TRUSTED_SIGNING_ACCOUNT` | Your Trusted Signing account name (e.g., `normietools-signing`) |
| `TRUSTED_SIGNING_CERT_PROFILE` | Your certificate profile name (e.g., `normietools-public`) |

### Step 6: Push and Verify

Push any commit to `main`. The GitHub Actions workflow will:

1. Build `NormieTools.exe` with PyInstaller
2. **Sign** `NormieTools.exe` with Azure Trusted Signing
3. Build `NormieTools_Setup.exe` with Inno Setup
4. **Sign** `NormieTools_Setup.exe` with Azure Trusted Signing
5. Generate SHA256 checksums of the **signed** binaries
6. Create a GitHub Release with signed artifacts

### Step 7: Verify the Signature

After downloading a signed release, right-click the EXE → **Properties** → **Digital Signatures** tab. You should see a valid signature from Microsoft's Trusted Signing service.

---

## How It Works in CI/CD

The signing is handled by the [`azure/trusted-signing-action`](https://github.com/azure/trusted-signing-action) GitHub Action in `.github/workflows/deploy.yml`.

Key points:
- Signing is **conditional** — if the secrets aren't configured, the build still succeeds (just without signing)
- The EXE is signed **before** the installer is built, so the installer contains a signed EXE
- The installer itself is also signed **after** being built
- SHA256 timestamps ensure signatures remain valid even after the certificate expires

---

## Regional Endpoints

| Region | Endpoint URL |
|--------|-------------|
| East US | `https://eus.codesigning.azure.net` |
| West US | `https://wus.codesigning.azure.net` |
| West Central US | `https://wcus.codesigning.azure.net` |
| West US 2 | `https://wus2.codesigning.azure.net` |
| North Europe | `https://neu.codesigning.azure.net` |
| West Europe | `https://weu.codesigning.azure.net` |
| UK South | `https://uks.codesigning.azure.net` |

---

## Free Alternative: SignPath.io

If you prefer a free option, [SignPath.io](https://signpath.io) offers free code signing for open-source projects through their Foundation program:

1. Apply at [signpath.io/open-source](https://about.signpath.io/open-source)
2. Submit your GitHub repo for review
3. Once approved, integrate via their GitHub Action
4. Note: SmartScreen reputation builds gradually (~30–90 days) since it's not Microsoft's own PKI

---

## Troubleshooting

**"Signing step skipped"** — The Azure secrets aren't configured. Follow Steps 4–5 above.

**"Identity validation pending"** — Azure requires identity verification before issuing Public Trust certificates. Complete the verification in Azure Portal → Trusted Signing → Identity validations.

**"Certificate profile not found"** — Double-check `TRUSTED_SIGNING_CERT_PROFILE` matches the exact profile name in Azure Portal.

**SmartScreen still warns after signing** — Clear your browser's download cache and re-download. SmartScreen checks the Authenticode signature on first run — once signed, the warning should not appear.
