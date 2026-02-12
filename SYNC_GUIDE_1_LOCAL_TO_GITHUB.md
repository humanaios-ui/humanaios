# SYNC GUIDE 1: LOCAL → GITHUB
**Standardized Process for Repository Updates**

---

## 🎯 WHEN TO USE THIS GUIDE

**Trigger phrase from Claude:**
> "Review and upload to GitHub"

**Or when you have:**
- New documentation files (.md)
- Updated code files
- New features or fixes
- Strategic documents to make public

---

## ⏰ TIME REQUIRED

**5-15 minutes** (depends on number of files)

---

## 📋 STEP-BY-STEP PROCESS

### **STEP 1: Navigate to Repository**
```bash
cd ~/Desktop/humanaios
```

**Verify you're in the right place:**
```bash
pwd
# Should show: /Users/andersonfamily/Desktop/humanaios
```

---

### **STEP 2: Check Current Status**
```bash
git status
```

**What you'll see:**
- Modified files (files you changed)
- Untracked files (new files to add)
- Deleted files (files removed)

**Read this output carefully.** This tells you what's about to be synced.

---

### **STEP 3: Review Files Before Adding**

**Look at what's changed:**
```bash
git diff README.md
# (Replace README.md with any modified file you want to review)
```

**Check new files exist:**
```bash
ls -la [filename]
```

**CRITICAL: Make sure no sensitive data is being committed**
- ❌ NO .env files (actual secrets)
- ❌ NO API keys
- ❌ NO passwords
- ❌ NO customer contact details
- ❌ NO financial account numbers
- ✅ YES to .env.example (template with fake values)
- ✅ YES to documentation
- ✅ YES to code without secrets

---

### **STEP 4: Stage Files**

**Option A: Add specific files (RECOMMENDED)**
```bash
# Add each file individually
git add filename1.md
git add filename2.md
git add docs/filename3.md
```

**Option B: Add all new/modified files**
```bash
git add .
```

**Option C: Add all including deletions**
```bash
git add -A
```

**After staging, verify:**
```bash
git status
# Check that ONLY the files you want are "staged for commit"
```

---

### **STEP 5: Commit with Meaningful Message**

**Format:**
```bash
git commit -m "Day [X]: [Brief summary]

- [Specific change 1]
- [Specific change 2]  
- [Specific change 3]

[Optional: Impact or next steps]"
```

**Example:**
```bash
git commit -m "Day 7: Product descriptions complete

- Added AI Agent technical documentation
- Added Layman's product description
- Converted language to accessibility
- Cleaned up redundant files

Ready for developer outreach"
```

**Good commit messages:**
- ✅ Start with "Day X:" for chronological tracking
- ✅ List specific changes (bullet points)
- ✅ Explain WHY if not obvious
- ✅ Keep under 300 characters total

**Bad commit messages:**
- ❌ "updates"
- ❌ "stuff"
- ❌ "misc changes"
- ❌ No description at all

---

### **STEP 6: Push to GitHub**

```bash
git push origin main
```

**What happens:**
- Your local changes upload to GitHub
- Repository updates publicly (if public repo)
- Changes visible at: https://github.com/humanaios-ui/humanaios

**If you see an error:**
- "rejected" → Someone else pushed, need to pull first
- "authentication failed" → GitHub credentials issue
- "connection refused" → Internet connection issue

---

### **STEP 7: Verify on GitHub**

**Open browser:**
1. Go to: https://github.com/humanaios-ui/humanaios
2. Check: Files you committed are visible
3. Click: Latest commit message appears
4. Verify: Changes look correct

**✅ DONE!**

---

## 🔄 HANDLING COMMON SCENARIOS

### **Scenario 1: You forgot to add a file**

```bash
# Add the forgotten file
git add forgotten-file.md

# Amend the last commit (don't create new commit)
git commit --amend --no-edit

# Force push (only if you haven't shared this commit yet)
git push origin main --force
```

---

### **Scenario 2: You added the wrong file**

**Before commit:**
```bash
# Unstage the file
git reset HEAD wrong-file.md

# Now commit without it
git commit -m "Your message"
```

**After commit but before push:**
```bash
# Remove from last commit
git reset --soft HEAD~1

# File is now unstaged, remove it from staging
git reset HEAD wrong-file.md

# Commit again
git commit -m "Your message"
```

---

### **Scenario 3: Merge conflicts**

```bash
# Pull latest changes
git pull origin main

# If conflicts, git will tell you which files
# Open each conflicted file, look for:
<<<<<<< HEAD
Your changes
=======
Their changes
>>>>>>> branch-name

# Decide which to keep, remove the markers
# Then:
git add [resolved-file]
git commit -m "Resolved merge conflict"
git push origin main
```

---

### **Scenario 4: Need to undo last commit**

**Undo commit but keep changes:**
```bash
git reset --soft HEAD~1
# Your files stay modified, commit is undone
```

**Undo commit and changes:**
```bash
git reset --hard HEAD~1
# WARNING: This deletes your changes!
```

---

## 📊 VERIFICATION CHECKLIST

After every sync, verify:

- [ ] `git status` shows "nothing to commit, working tree clean"
- [ ] Files visible on GitHub web interface
- [ ] Commit message is clear and descriptive
- [ ] No sensitive data was committed
- [ ] README.md still accurate
- [ ] Links in docs still work

---

## 🚨 EMERGENCY: Committed Sensitive Data

**If you accidentally committed passwords, API keys, or secrets:**

**IMMEDIATE ACTION:**

1. **Rotate/change the exposed secret immediately**
   - New API key
   - New password
   - New token

2. **Remove from Git history** (complex, ask Claude for help)

3. **Force push cleaned history**

**PREVENTION:**
- Always check `git status` before committing
- Never commit .env files (use .env.example instead)
- Use .gitignore properly
- When in doubt, ask Claude first

---

## 💡 PRO TIPS

**Commit often:**
- Small commits are better than large ones
- Easier to track what changed
- Easier to undo if needed

**Pull before you push:**
```bash
git pull origin main  # Get latest changes
git push origin main  # Push your changes
```

**Check your .gitignore:**
```bash
cat .gitignore
# Make sure it includes:
# .env
# node_modules/
# *.log
# .DS_Store
```

**Use branches for experiments:**
```bash
git checkout -b experiment-feature
# Make changes, test
# If good: merge to main
# If bad: delete branch
```

---

## 📞 WHEN TO ASK CLAUDE FOR HELP

**Ask before proceeding if:**
- ⚠️ You see merge conflicts
- ⚠️ Git gives an error you don't understand
- ⚠️ You think you committed sensitive data
- ⚠️ You want to undo multiple commits
- ⚠️ You're not sure if files should be public

**Claude will:**
- Walk you through step-by-step
- Explain what each command does
- Help verify no sensitive data exposed
- Create custom commands for your situation

---

## ✅ SUCCESS METRICS

**You've successfully synced when:**
- ✅ Local and GitHub match
- ✅ No unstaged changes
- ✅ Commit message is clear
- ✅ Files visible on GitHub
- ✅ No sensitive data exposed
- ✅ You can explain what changed and why

---

## 🎯 REMEMBER

**Git sync is about:**
- Communication (commit messages)
- Safety (no sensitive data)
- History (tracking changes)
- Collaboration (sharing progress)

**Take your time. Double-check. Ask questions.**

**Better to take 15 minutes and do it right than 5 minutes and expose secrets.** ✅

---

**Last Updated:** February 12, 2026  
**Version:** 1.0  
**Status:** Standardized Process Active
