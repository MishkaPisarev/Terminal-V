# Fix GitHub Pages Showing README Instead of App

## Problem
When visiting `terminal.valkyrris.com`, you see the repository README instead of the React app.

## Solution

### Step 1: Verify GitHub Pages Settings

1. Go to: https://github.com/MishkaPisarev/Terminal-V/settings/pages
2. **Source**: Must be set to **"GitHub Actions"** (NOT "Deploy from a branch")
3. **Custom domain**: Should be `terminal.valkyrris.com`
4. **Enforce HTTPS**: Should be enabled

### Step 2: Check Deployment Workflow

1. Go to: https://github.com/MishkaPisarev/Terminal-V/actions
2. Look for "Deploy Terminal Web" workflow
3. If it hasn't run, click "Run workflow" → "Run workflow" to trigger it manually
4. Wait for the workflow to complete (both "Build Terminal Web" and "Deploy to GitHub Pages" jobs)

### Step 3: Verify CNAME File

The CNAME file has been added to `apps/terminal-web/public/CNAME` and will be copied to `dist/` during build.

### Step 4: Check Deployment Status

1. Go to: https://github.com/MishkaPisarev/Terminal-V/deployments
2. You should see a successful deployment with the custom domain

### Step 5: Clear Browser Cache

After deployment completes:
- Clear browser cache or use incognito mode
- Visit `terminal.valkyrris.com` again

## What Was Fixed

1. ✅ Added `CNAME` file to `apps/terminal-web/public/` (will be copied to dist during build)
2. ✅ Updated workflow to trigger on all pushes to `main` (removed path filters)
3. ✅ Added `workflow_dispatch` to allow manual triggering

## If Still Not Working

1. Check GitHub Actions logs for errors
2. Verify the build artifact contains `index.html` in `apps/terminal-web/dist/`
3. Make sure DNS CNAME record points to `mishkapisarev.github.io`
4. Wait 5-10 minutes for DNS propagation
