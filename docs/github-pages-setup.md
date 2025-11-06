# GitHub Pages Setup Instructions

This document provides step-by-step instructions for configuring GitHub Pages to deploy the Personal Event Summary system.

## Prerequisites

- Repository must be pushed to GitHub
- GitHub Actions workflows must be present in `.github/workflows/`
- You must have admin access to the repository

## Configuration Steps

### 1. Navigate to Repository Settings

1. Go to your repository on GitHub
2. Click on **Settings** (top navigation bar)
3. In the left sidebar, click on **Pages**

### 2. Configure Source

Under "Build and deployment":

1. **Source**: Select "GitHub Actions"
   - This enables deployment via the `.github/workflows/deploy.yml` workflow
   - Do NOT select "Deploy from a branch" - we're using Actions

### 3. Verify Workflow Permissions

1. In repository Settings, go to **Actions** → **General**
2. Scroll to "Workflow permissions"
3. Ensure **"Read and write permissions"** is selected
4. Check **"Allow GitHub Actions to create and approve pull requests"** (optional but recommended)
5. Click **Save**

### 4. Initial Deployment

Once configured:

1. Push changes to the `main` branch
2. Go to **Actions** tab in your repository
3. You should see the "Deploy to GitHub Pages" workflow running
4. Wait for it to complete (usually 1-2 minutes)

### 5. Verify Deployment

After the workflow completes:

1. Go back to **Settings** → **Pages**
2. You should see a message: "Your site is live at `https://<username>.github.io/<repository>/`"
3. Click the URL to verify your site is accessible

## Expected Site Structure

Your deployed site will have the following structure:

```
https://<username>.github.io/<repository>/
├── attendees/
│   ├── 1001/
│   │   └── index.html          # Accessible at /attendees/1001/
│   ├── 1002/
│   │   └── index.html          # Accessible at /attendees/1002/
│   └── ...
├── static/
│   ├── css/
│   │   └── styles.css
│   └── images/
│       ├── event-logo.png
│       └── favicon.png
├── 404.html                    # Custom 404 page
└── .nojekyll                   # Disables Jekyll processing
```

## Testing Your Deployment

### Test Clean URLs

Visit these URLs to verify clean URL routing:
- `https://<username>.github.io/<repository>/attendees/1001/` ✓ Should work
- `https://<username>.github.io/<repository>/attendees/1001` ✓ Should redirect
- `https://<username>.github.io/<repository>/attendees/1001/index.html` ✓ Should work

### Test 404 Page

Visit a non-existent page to verify custom 404:
- `https://<username>.github.io/<repository>/nonexistent-page`

### Test Static Assets

Verify CSS and images load:
- `https://<username>.github.io/<repository>/static/css/styles.css`

## Troubleshooting

### Site Not Deploying

**Symptom**: Workflow runs but site doesn't update

**Solutions**:
1. Check workflow logs in Actions tab for errors
2. Verify Pages is set to "GitHub Actions" not "Deploy from a branch"
3. Ensure workflow has write permissions (see Step 3 above)
4. Check if there's a `CNAME` file interfering (delete if not using custom domain)

### 404 Errors on All Pages

**Symptom**: Only 404 page shows, all other pages return 404

**Solutions**:
1. Verify `.nojekyll` file exists in dist/ directory
2. Check deploy workflow includes: `touch dist/.nojekyll`
3. Ensure workflow uploads from `./dist` directory

### CSS Not Loading

**Symptom**: Pages load but are unstyled

**Solutions**:
1. Check browser console for CSS 404 errors
2. Verify `static/css/styles.css` is in the uploaded artifact
3. Check HTML links use absolute paths: `/static/css/styles.css` not `../static/css/styles.css`
4. Clear browser cache and hard refresh (Ctrl+Shift+R or Cmd+Shift+R)

### Permission Errors

**Symptom**: Workflow fails with permission errors

**Solutions**:
1. Go to Settings → Actions → General
2. Set Workflow permissions to "Read and write permissions"
3. Re-run the workflow

## Automatic Updates

Once configured, your site automatically updates when:
- You push commits to the `main` branch
- The deploy workflow completes successfully

Typical deployment time: **1-2 minutes** from push to live site

## Manual Deployment Trigger

You can manually trigger a deployment:

1. Go to **Actions** tab
2. Select "Deploy to GitHub Pages" workflow
3. Click **Run workflow**
4. Select branch (usually `main`)
5. Click **Run workflow** button

## Custom Domain (Optional)

To use a custom domain:

1. In Settings → Pages, under "Custom domain"
2. Enter your domain name (e.g., `events.example.com`)
3. Click **Save**
4. Configure DNS records with your domain provider:
   - Type: `CNAME`
   - Name: `events` (or `@` for apex domain)
   - Value: `<username>.github.io`
5. Wait for DNS propagation (up to 48 hours, usually faster)

## Security: HTTPS

GitHub Pages automatically provides HTTPS for:
- `*.github.io` domains (default)
- Custom domains (after DNS verification)

**Enforce HTTPS**:
1. In Settings → Pages
2. Check **"Enforce HTTPS"**
3. Recommended for all production sites

## Monitoring

### Check Deployment Status

View deployment history:
1. Go to **Actions** tab
2. Click on "Deploy to GitHub Pages" workflow
3. View all previous runs and their status

### View Build Logs

If deployment fails:
1. Click on the failed workflow run
2. Click on the failed job
3. Expand steps to see detailed logs
4. Common issues are shown in the verification step

## Next Steps

After configuration:
1. Test all attendee pages
2. Verify responsive design on mobile devices
3. Test custom 404 page
4. Share URLs with stakeholders
5. Add build status badges to README (see Phase 6.4)

## Support

For issues not covered here:
- Check [GitHub Pages documentation](https://docs.github.com/en/pages)
- Review workflow logs in Actions tab
- Inspect browser console for client-side errors
