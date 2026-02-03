# Troubleshooting: GitHub Pages Shows README Instead of App

## Problem
Visiting `terminal.valkyrris.com` shows the repository README instead of the React application.

## Root Cause
GitHub Pages is configured to serve from a **branch** instead of **GitHub Actions**.

## Solution Steps

### Step 1: Change GitHub Pages Source (CRITICAL)

1. Go to: **https://github.com/MishkaPisarev/Terminal-V/settings/pages**

2. Under **"Source"**, you'll see one of these:
   - ❌ **"Deploy from a branch"** (WRONG - this is why you see README)
   - ✅ **"GitHub Actions"** (CORRECT)

3. If it says "Deploy from a branch":
   - Click the dropdown
   - Select **"GitHub Actions"**
   - Click **"Save"**

4. Verify:
   - Source should now say: **"GitHub Actions"**
   - Custom domain: `terminal.valkyrris.com`
   - Enforce HTTPS: ✓ (enabled)

### Step 2: Verify Deployment Workflow Ran

1. Go to: **https://github.com/MishkaPisarev/Terminal-V/actions**

2. Look for workflow: **"Deploy Terminal Web"**

3. Check the latest run:
   - Should have ✅ green checkmarks
   - Both jobs should be successful:
     - ✅ "Build Terminal Web"
     - ✅ "Deploy to GitHub Pages"

4. If workflow hasn't run or failed:
   - Click **"Run workflow"** → **"Run workflow"** (top right)
   - Wait for it to complete (2-3 minutes)

### Step 3: Check Deployment Status

1. Go to: **https://github.com/MishkaPisarev/Terminal-V/deployments**

2. You should see:
   - Latest deployment with status: **"Active"**
   - Environment: **"github-pages"**
   - Custom domain: `terminal.valkyrris.com`

### Step 4: Verify Build Output

The workflow should build and upload:
- **Path**: `apps/terminal-web/dist`
- **Contents**: Should include `index.html`, `assets/`, and `CNAME`

### Step 5: Clear Cache and Test

1. **Wait 2-3 minutes** after deployment completes
2. **Clear browser cache** or use **Incognito/Private mode**
3. Visit: **https://terminal.valkyrris.com**

## Common Issues

### Issue 1: "Source" is still "Deploy from a branch"
**Fix**: You must manually change it to "GitHub Actions" in Settings → Pages

### Issue 2: Workflow not running
**Fix**: 
- Check if workflow file exists: `.github/workflows/deploy-frontend.yml`
- Manually trigger: Actions → "Deploy Terminal Web" → "Run workflow"

### Issue 3: Build fails
**Fix**: 
- Check Actions logs for errors
- Common issues:
  - Missing dependencies (run `pnpm install` locally first)
  - TypeScript errors (fix in code)
  - Missing UI Kit build (should build automatically)

### Issue 4: 404 after deployment
**Fix**:
- Verify CNAME file exists in `apps/terminal-web/public/CNAME`
- Check DNS: `nslookup terminal.valkyrris.com` should point to `mishkapisarev.github.io`
- Wait 5-10 minutes for DNS propagation

## Verification Checklist

- [ ] GitHub Pages Source = **"GitHub Actions"** (NOT "Deploy from a branch")
- [ ] Custom domain = `terminal.valkyrris.com`
- [ ] Enforce HTTPS = Enabled
- [ ] Deployment workflow ran successfully
- [ ] Latest deployment shows "Active" status
- [ ] CNAME file exists in `apps/terminal-web/public/CNAME`
- [ ] DNS CNAME record points to `mishkapisarev.github.io`
- [ ] Browser cache cleared
- [ ] Tested in incognito mode

## Still Not Working?

1. Check GitHub Actions logs for specific errors
2. Verify the build artifact contains `index.html`:
   - Go to Actions → Latest run → "Build Terminal Web" → "Upload artifact"
   - Should see `index.html` in the artifact
3. Check repository settings:
   - Settings → Pages → should show "Your site is live at terminal.valkyrris.com"
4. Contact GitHub Support if deployment shows as active but site doesn't load
