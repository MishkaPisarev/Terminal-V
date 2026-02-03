# CRITICAL: GitHub Pages Still Showing README

## Problem
The site at `terminal.valkyrris.com` is showing the README file instead of the React app. This means GitHub Pages is serving from the **repository root** instead of the **built artifact**.

## Root Cause
GitHub Pages is configured to serve from a **branch** instead of **GitHub Actions**.

## IMMEDIATE FIX REQUIRED

### Step 1: Check GitHub Pages Source (MOST IMPORTANT)

1. Go to: **https://github.com/MishkaPisarev/Terminal-V/settings/pages**

2. Look at the **"Source"** section at the top

3. **If it says ANY of these, it's WRONG:**
   - ❌ "Deploy from a branch"
   - ❌ "main" / "root"
   - ❌ "Use a suggested workflow"

4. **It MUST say:**
   - ✅ "GitHub Actions" 
   - ✅ "Deployed via GitHub Actions"
   - ✅ Workflow name: "Deploy Terminal Web"

### Step 2: Change Source to GitHub Actions

**If Source is NOT "GitHub Actions":**

1. Click the dropdown next to "Source"
2. Select **"GitHub Actions"**
3. Click **"Save"**
4. Wait 1-2 minutes

### Step 3: Verify Workflow Ran

1. Go to: **https://github.com/MishkaPisarev/Terminal-V/actions**
2. Look for workflow: **"Deploy Terminal Web"**
3. **If no runs exist or last run failed:**
   - Click **"Run workflow"** (top right)
   - Select branch: `main`
   - Click **"Run workflow"**
   - Wait 2-3 minutes for completion

### Step 4: Check Deployment

1. Go to: **https://github.com/MishkaPisarev/Terminal-V/deployments**
2. Should see:
   - Environment: **"github-pages"**
   - Status: **"Active"**
   - URL: `https://terminal.valkyrris.com`

### Step 5: Test Site

1. **Wait 2-3 minutes** after deployment completes
2. **Hard refresh**: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
3. **Or use Incognito/Private mode**
4. Visit: **https://terminal.valkyrris.com**

**Expected:** React app with Dashboard
**If still README:** Source is still wrong - repeat Step 1-2

## Why This Happens

GitHub Pages has TWO deployment methods:

1. **Branch Deployment** (WRONG for us)
   - Serves files directly from repository
   - Shows README.md from root
   - No build process

2. **GitHub Actions** (CORRECT for us)
   - Builds the app first
   - Serves from built artifact (`apps/terminal-web/dist`)
   - Shows the React app

## Verification Checklist

- [ ] GitHub Pages Source = **"GitHub Actions"** (NOT "Deploy from a branch")
- [ ] Workflow "Deploy Terminal Web" exists and ran successfully
- [ ] Latest deployment shows "Active" status
- [ ] Site shows React app (NOT README)
- [ ] No 404 errors in browser console

## If Still Not Working

1. **Double-check Source setting** - this is the #1 cause
2. Check Actions logs for build errors
3. Verify artifact contains `index.html` in `apps/terminal-web/dist`
4. Clear browser cache completely
5. Try different browser/device

**The Source MUST be "GitHub Actions" - nothing else will work!**
