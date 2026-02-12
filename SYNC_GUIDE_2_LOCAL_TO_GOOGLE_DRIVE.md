# SYNC GUIDE 2: LOCAL → GOOGLE DRIVE
**Standardized Process for Cloud Document Storage**

---

## 🎯 WHEN TO USE THIS GUIDE

**Trigger phrase from Claude:**
> "Review and upload to Google Drive"

**Or when you have:**
- Business documents (.md, .pdf, .docx)
- Financial tracking spreadsheets (.csv, .xlsx)
- Customer research and outreach materials
- Partnership documentation
- Session summaries and logs
- Any non-code business files

---

## ⏰ TIME REQUIRED

**5-20 minutes** (depends on number of files and internet speed)

---

## 📋 STEP-BY-STEP PROCESS

### **STEP 1: Organize Files Locally First**

**Before uploading, make sure files are in logical groups:**

```
/mnt/user-data/outputs/
├── [Files to upload to 01_Business_Development/]
├── [Files to upload to 02_Partnerships/]
├── [Files to upload to 03_Financial/]
├── [Files to upload to 04_Daily_Logs/]
└── [Files to upload to 05_Product_Documentation/]
```

**Ask yourself:**
- Where does this file belong?
- Is this the final version?
- Does the filename make sense?
- Is it duplicate of something already uploaded?

---

### **STEP 2: Open Google Drive**

**In browser:**
1. Go to: https://drive.google.com
2. Sign in (if needed)
3. Navigate to: HumanAIOS folder
4. Verify you see your folder structure

**Expected structure:**
```
HumanAIOS/
├── 01_Business_Development/
│   ├── Customer_Research/
│   ├── Outreach_Emails/
│   └── Contacts/
├── 02_Partnerships/
│   └── Zach_Raymond/
├── 03_Financial/
│   ├── Budget_Tracking/
│   └── Guides/
├── 04_Daily_Logs/
│   └── 2026-02/
└── 05_Product_Documentation/
```

**If folders missing:** Create them first (see Step 3)

---

### **STEP 3: Create New Folders (If Needed)**

**To create folder:**
1. Click "+ New" button (top left)
2. Select "New folder"
3. Name it clearly (e.g., "06_Social_Media")
4. Press Enter

**Folder naming conventions:**
- ✅ Start with number for ordering (01_, 02_, 03_)
- ✅ Use underscores not spaces (01_Business not "01 Business")
- ✅ Descriptive names (Customer_Research not CR)
- ✅ Consistent capitalization (Title_Case)

---

### **STEP 4: Navigate to Target Folder**

**Click through to where file belongs:**

Example: Uploading customer email
- Click: `01_Business_Development`
- Click: `Outreach_Emails`
- You're now in the right place

**Verify you're in correct folder:**
- Check breadcrumb at top
- Should show: HumanAIOS > 01_Business_Development > Outreach_Emails

---

### **STEP 5: Upload Files**

### **Method A: Drag and Drop (Fastest)**

1. Open Finder window side-by-side with browser
2. Navigate to: `/mnt/user-data/outputs/`
3. Select files to upload
4. Drag them into Google Drive window
5. Wait for upload (green checkmarks appear)

### **Method B: File Upload Button**

1. Click "+ New" button
2. Select "File upload"
3. Navigate to `/mnt/user-data/outputs/`
4. Select files (Cmd+Click for multiple)
5. Click "Open"
6. Wait for upload

### **Method C: Folder Upload (For Many Files)**

1. Click "+ New" button
2. Select "Folder upload"
3. Select entire folder
4. All files upload maintaining structure

**Choose method based on:**
- Few files (1-5): Method A or B
- Many files (5+): Method C
- Preserving structure: Method C

---

### **STEP 6: Verify Upload Success**

**Check each file:**
- [ ] Green checkmark appears (upload complete)
- [ ] File appears in correct folder
- [ ] Filename is correct
- [ ] File can be opened (double-click to verify)
- [ ] No error messages

**Common upload issues:**
- File too large (>15GB on free account)
- Internet connection dropped
- File name has special characters (?, *, :)
- Duplicate filename (Drive will rename)

---

### **STEP 7: Convert CSVs to Google Sheets (If Applicable)**

**For financial tracking files (.csv):**

1. Find the CSV file in Google Drive
2. Right-click on it
3. Select "Open with" → "Google Sheets"
4. File opens as spreadsheet
5. Click "File" → "Save as Google Sheets"
6. Now it's a live spreadsheet (auto-saves)

**Which files to convert:**
- ✅ budget_summary.csv → Budget Summary
- ✅ transaction_log.csv → Transactions
- ✅ revenue_tracker.csv → Revenue Pipeline
- ✅ runway_calculator.csv → Runway Calculator

**Which files to keep as CSV:**
- ✅ One-time exports
- ✅ Backup copies
- ✅ Data for import elsewhere

---

### **STEP 8: Set Sharing/Privacy Settings**

**For entire HumanAIOS folder:**

1. Right-click "HumanAIOS" folder
2. Click "Share"
3. Check current setting

**Should be:** "Restricted" (only you have access)

**If not:**
1. Click "Change to restricted"
2. Remove any other people
3. Click "Done"

**For specific files you want to share:**

1. Right-click specific file
2. Click "Share"
3. Add person's email
4. Choose permission level:
   - Viewer (can see, can't edit)
   - Commenter (can comment)
   - Editor (can edit)
5. Click "Send"

**NEVER share:**
- ❌ Financial data
- ❌ Customer contact details
- ❌ Partnership negotiations
- ❌ Personal information
- ❌ Sensitive research

**OK to share (with permission):**
- ✅ Public documentation
- ✅ Finalized outreach emails (templates)
- ✅ Non-sensitive process docs

---

### **STEP 9: Organize and Clean Up**

**After uploading:**

**Rename if needed:**
- Right-click file → Rename
- Follow naming convention
- Be descriptive

**Move if in wrong place:**
- Click and drag to correct folder
- Or: Right-click → Move to

**Delete duplicates:**
- If you uploaded same file twice
- Right-click → Remove
- Confirm deletion

**Add to folders (not move):**
- Right-click file
- Hold Shift
- Click "Add to"
- File now appears in multiple folders (same file, not copy)

---

### **STEP 10: Verify Final Structure**

**Navigate back to HumanAIOS root:**

**Check:**
- [ ] All new files in correct folders
- [ ] No files in root (everything categorized)
- [ ] Folder structure makes sense
- [ ] Privacy set to Restricted
- [ ] CSVs converted to Sheets (if needed)

**Your structure should look clean and organized.**

---

## 📊 FOLDER ORGANIZATION GUIDE

### **01_Business_Development/**
- Customer research files
- Outreach email templates
- Contact information
- Market analysis

### **02_Partnerships/**
- Partnership briefs
- Call notes
- Proposals
- Agreements

### **03_Financial/**
- Budget tracking (Sheets)
- Financial reports
- Revenue forecasts
- Runway calculations

### **04_Daily_Logs/**
- Session summaries
- Progress tracking
- Decision logs
- Weekly reviews

### **05_Product_Documentation/**
- Product descriptions
- Technical docs
- API documentation
- Feature specs

### **06_Social_Media/** (if needed)
- Post drafts
- Content calendar
- Engagement tracking

### **07_Legal/** (if needed)
- Contracts
- Terms of service
- Privacy policy
- Compliance docs

---

## 🔄 HANDLING COMMON SCENARIOS

### **Scenario 1: File Already Exists**

**Google Drive will:**
- Create copy with "(1)" appended
- Example: "EMAIL_INTUIT.md" becomes "EMAIL_INTUIT (1).md"

**What to do:**
1. Compare the two versions
2. Keep the newest/best one
3. Delete the old one
4. Rename if needed (remove the "(1)")

---

### **Scenario 2: Upload Failed**

**Symptoms:**
- Upload stuck at 99%
- Error message appears
- File doesn't show up

**Solutions:**
1. Refresh the page
2. Try uploading again
3. Check internet connection
4. Try smaller batch (fewer files)
5. Check file size (under 15GB)
6. Check filename (no special characters)

---

### **Scenario 3: Can't Find Uploaded File**

**Search for it:**
1. Click search bar (top)
2. Type filename
3. Check if it's in different folder
4. Check if upload actually completed

**Filter by upload date:**
1. Sort by "Last modified"
2. Look for today's uploads

---

### **Scenario 4: Need to Download Files Back**

**Single file:**
1. Right-click file
2. Select "Download"
3. File saves to Downloads folder

**Multiple files:**
1. Select files (Cmd+Click)
2. Right-click
3. Select "Download"
4. Downloads as .zip file

**Entire folder:**
1. Right-click folder
2. Select "Download"
3. Downloads as .zip (preserves structure)

---

## 💡 PRO TIPS

### **Tip 1: Star Important Files**

- Right-click file → Add star
- Access quickly via "Starred" in left sidebar
- Use for files you reference often

### **Tip 2: Use Colors for Folders**

- Right-click folder
- Select color
- Visual organization
- Example: Red = urgent, Blue = archive

### **Tip 3: Create Shortcuts**

- Right-click file
- "Add shortcut to Drive"
- File appears in multiple places (still one file)
- Useful for cross-category files

### **Tip 4: Use Google Drive Desktop App**

- Download: https://www.google.com/drive/download/
- Syncs folder to Mac
- Drag/drop from Finder
- Auto-uploads in background
- Access offline

### **Tip 5: Enable Offline Access**

- Click Settings (gear icon)
- Turn on "Offline"
- Access files without internet
- Changes sync when online

---

## 🚨 COMMON MISTAKES TO AVOID

**Don't:**
- ❌ Upload same file multiple times (creates duplicates)
- ❌ Leave files in root folder (unorganized)
- ❌ Use cryptic filenames ("doc1.md")
- ❌ Share entire folder publicly
- ❌ Forget to convert CSVs to Sheets (can't edit otherwise)
- ❌ Upload sensitive data to shared folders
- ❌ Delete local copies before verifying upload

**Do:**
- ✅ Organize into folders before uploading
- ✅ Use descriptive filenames
- ✅ Verify uploads completed
- ✅ Check privacy settings
- ✅ Keep local backups
- ✅ Clean up duplicates regularly

---

## 📞 WHEN TO ASK CLAUDE FOR HELP

**Ask before proceeding if:**
- ⚠️ Upload keeps failing
- ⚠️ Not sure which folder file belongs in
- ⚠️ File contains sensitive data (privacy check)
- ⚠️ Need to share file but unsure if safe
- ⚠️ Can't find uploaded file
- ⚠️ Storage quota full

**Claude will:**
- Help troubleshoot upload issues
- Suggest proper folder organization
- Verify privacy settings
- Create new folder structure if needed
- Guide through sharing safely

---

## ✅ SUCCESS METRICS

**You've successfully synced when:**
- ✅ All files uploaded (green checkmarks)
- ✅ Files in correct folders
- ✅ Privacy set appropriately
- ✅ CSVs converted to Sheets (if financial)
- ✅ No duplicates
- ✅ Structure is organized
- ✅ You can find files easily

---

## 🎯 REMEMBER

**Google Drive is for:**
- Business documents
- Collaboration (when appropriate)
- Cloud backup
- Easy access across devices

**Google Drive is NOT for:**
- Code (use GitHub)
- Large video files (use Vimeo/YouTube)
- Highly sensitive secrets (use 1Password/encrypted storage)

**Keep it organized. Keep it private. Keep it clean.** ✅

---

**Last Updated:** February 12, 2026  
**Version:** 1.0  
**Status:** Standardized Process Active
