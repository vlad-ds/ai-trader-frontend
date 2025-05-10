# Instructions for Creating and Pushing Daily Diary Entry

## Overview
These instructions will guide you through creating a daily diary markdown file and pushing it to the git repository. The diary file should follow the format: `default_YYYY-MM-DD.md`

## Prerequisites
- You already have the diary content to write
- You are working in the repository: `/Users/vladgheorghe/code/ai-trader-frontend`
- The diary files are stored in: `dashboard/data/diary/`

## Step-by-Step Instructions

### 1. Navigate to the repository
```bash
cd /Users/vladgheorghe/code/ai-trader-frontend
```

### 2. Create the diary file
Use the Write tool to create the markdown file with today's date:
```
Write tool:
- file_path: /Users/vladgheorghe/code/ai-trader-frontend/dashboard/data/diary/default_YYYY-MM-DD.md
- content: [Your diary content here]
```
Replace `YYYY-MM-DD` with the actual date (e.g., 2025-05-10).

### 3. Add the file to git
```bash
git add dashboard/data/diary/default_YYYY-MM-DD.md
```

### 4. Commit the file
```bash
git commit -m "Add diary entry for YYYY-MM-DD"
```

### 5. Check for remote updates
Before pushing, check if your local branch is behind the remote:
```bash
git fetch origin
git status
```

### 6. Handle any divergence
If your branch is both ahead and behind (diverged), use rebase to integrate changes:
```bash
git pull --rebase origin main
```

### 7. Push your changes
```bash
git push origin main
```

### 8. Verify the push
```bash
git status
```
You should see: "Your branch is up to date with 'origin/main'."

## Common Issues and Solutions

### Push fails with authentication error
- The git credentials may need refreshing
- Check the remote URL: `git remote -v`
- Verify user config: `git config --list | grep -E '(user.name|user.email)'`

### Push fails due to diverged branches
- This happens when remote has new commits
- Always use `git pull --rebase origin main` before pushing
- This preserves a linear history and avoids merge commits

### Push still fails after pull
- Use `git remote show origin` to check the remote status
- Try verbose output: `git push origin main --verbose`
- As a last resort, check network connectivity

## Notes
- Always use absolute paths when working with files
- The diary content should be a single paragraph of markdown
- Commit messages should follow the format: "Add diary entry for YYYY-MM-DD"
- If using Batch tool to run multiple commands, handle errors gracefully