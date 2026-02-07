# GitHub Setup Instructions

## Option 1: Automated Script (Recommended)

```bash
cd humainos
./setup-git.sh
```

That's it! The script handles everything.

---

## Option 2: Manual Steps

If you prefer to do it manually or the script doesn't work:

### 1. Navigate to Project Directory
```bash
cd humainos
```

### 2. Initialize Git Repository
```bash
git init
```

### 3. Add All Files
```bash
git add .
```

### 4. Create Initial Commit
```bash
git commit -m "Initial commit: HumanAIOS authentication system

✅ Complete authentication system with JWT
✅ User registration and login endpoints  
✅ PostgreSQL + TimescaleDB database schema
✅ Redis integration
✅ Docker development environment
✅ Multi-tenant organization support
✅ Production-ready security

Ready for Day 2: Agent monitoring endpoints"
```

### 5. Rename Branch to Main
```bash
git branch -M main
```

### 6. Add GitHub Remote
```bash
git remote add origin git@github.com:humainos/humainos.git
```

### 7. Push to GitHub
```bash
git push -u origin main
```

---

## Verification

After pushing, verify everything worked:

1. **Visit GitHub**: https://github.com/humainos/humainos
2. **Check files**: You should see all project files
3. **Check README**: Should display the project overview

---

## Post-Push Setup

### Make Repository Private

1. Go to: https://github.com/humainos/humainos/settings
2. Scroll to "Danger Zone"
3. Click "Change visibility"
4. Select "Make private"
5. Confirm

### Add Repository Description

1. Go to repository home
2. Click ⚙️ next to "About"
3. Add description: "The Operating System for Human-AI Workflows"
4. Add website: https://humainos.ai
5. Add topics: `ai`, `agents`, `monitoring`, `orchestration`, `typescript`, `nestjs`
6. Save

### Set Up Branch Protection (Optional but Recommended)

1. Settings → Branches
2. Add rule for `main` branch
3. Enable:
   - ✅ Require pull request reviews before merging
   - ✅ Require status checks to pass
4. Save

---

## Troubleshooting

### Permission Denied (SSH Key Issues)

If you get "Permission denied (publickey)":

1. **Check if you have an SSH key:**
   ```bash
   ls -la ~/.ssh
   ```

2. **If no SSH key, create one:**
   ```bash
   ssh-keygen -t ed25519 -C "aioshuman@gmail.com"
   ```

3. **Add SSH key to GitHub:**
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
   Copy output and add to: https://github.com/settings/keys

4. **Try pushing again:**
   ```bash
   git push -u origin main
   ```

### Alternative: Use HTTPS Instead

If SSH continues to have issues:

```bash
git remote remove origin
git remote add origin https://github.com/humainos/humainos.git
git push -u origin main
```

You'll be prompted for your GitHub username and Personal Access Token.

### Already Pushed?

If you already pushed and need to force update:

```bash
git push -f origin main
```

⚠️ **Warning**: Only use `-f` if you're sure you want to overwrite remote changes.

---

## Next Steps After Push

Once successfully pushed:

1. ✅ Clone on another machine to verify
2. ✅ Set up GitHub Actions (later)
3. ✅ Invite collaborators
4. ✅ Create project board for issue tracking

---

**Ready?** Run `./setup-git.sh` or follow the manual steps above! 🚀
