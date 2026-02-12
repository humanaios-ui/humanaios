# SYNC GUIDE 3: PERSONAL & CONFIDENTIAL DOCUMENTS
**Standardized Process for Sensitive Information Handling**

---

## 🎯 WHEN TO USE THIS GUIDE

**Trigger phrase from Claude:**
> "Review and upload to personal documents"

**Or when you have:**
- Financial account information (bank, credit card)
- Personal health records
- Legal documents (contracts, agreements)
- Passwords and API keys
- Customer contact details (names, emails, phones)
- Partnership negotiations (pre-public)
- Personal family information
- Recovery program materials (private)
- Anything you wouldn't want on the internet

---

## 🚨 CORE PRINCIPLE

**NEVER upload sensitive personal information to:**
- ❌ GitHub (public or private - assume public)
- ❌ Google Drive (unless encrypted)
- ❌ Cloud storage without encryption
- ❌ Shared folders
- ❌ Email (unencrypted)

**ALWAYS keep sensitive information:**
- ✅ Local only (Mac hard drive)
- ✅ Encrypted storage (if cloud needed)
- ✅ Password-protected folders
- ✅ Backed up offline (external drive)

---

## ⏰ TIME REQUIRED

**10-30 minutes** (includes encryption setup if first time)

---

## 📋 STEP-BY-STEP PROCESS

### **STEP 1: Identify Document Sensitivity Level**

**Use this checklist:**

**LEVEL 1: PUBLIC** (GitHub OK, Google Drive OK)
- [ ] No personal information
- [ ] No contact details
- [ ] No financial data
- [ ] No passwords/keys
- [ ] Content you'd post publicly

**Examples:** Product descriptions, public documentation, blog posts

**Action:** Use Sync Guide 1 or 2

---

**LEVEL 2: BUSINESS CONFIDENTIAL** (Google Drive private OK, NO GitHub)
- [ ] Business strategy (not sensitive)
- [ ] Customer research (anonymized)
- [ ] Financial projections (no actual accounts)
- [ ] Partnership briefs (before public)

**Examples:** Customer research notes, budget forecasts, session summaries

**Action:** Use Sync Guide 2 with privacy set to "Restricted"

---

**LEVEL 3: PERSONAL CONFIDENTIAL** (Local encrypted only)
- [x] Contains real names + contact info
- [x] Contains account numbers
- [x] Contains passwords/API keys
- [x] Contains health information
- [x] Contains legal contracts
- [x] Contains recovery materials
- [x] You'd never want this public

**Examples:** Bank statements, contracts, .env files, customer emails with real contacts

**Action:** Use THIS GUIDE (Guide 3)

---

### **STEP 2: Create Secure Local Storage**

**On your Mac:**

**Option A: Encrypted Disk Image (RECOMMENDED)**

1. Open "Disk Utility" (Applications → Utilities)
2. Click "File" → "New Image" → "Blank Image"
3. Settings:
   - Name: "HumanAIOS_Confidential"
   - Size: 1 GB (or larger if needed)
   - Format: "Mac OS Extended (Journaled)"
   - Encryption: "256-bit AES encryption" ✅
   - Partitions: "Single partition"
   - Image Format: "sparse bundle"
4. Click "Save"
5. Set password (use strong password!)
6. Click "Choose"

**This creates encrypted storage. Only you can open it with password.**

**Location:** Save to `~/Documents/Secure/` (create folder if needed)

---

**Option B: Encrypted Folder (Simpler but less secure)**

1. Create folder: `~/Documents/HumanAIOS_Private/`
2. Right-click folder → "Compress"
3. Delete original folder
4. Right-click .zip → "Encrypt"
5. Set password

**Less convenient (must unzip each time) but works.**

---

**Option C: Use 1Password or Other Password Manager**

If you use password manager:
- Store documents in secure notes
- Attach files to secure items
- Benefit: Syncs encrypted across devices
- Benefit: Already using trusted tool

---

### **STEP 3: Organize Confidential Files**

**Mount your encrypted disk image:**
1. Double-click "HumanAIOS_Confidential.sparsebundle"
2. Enter password
3. Disk appears in Finder sidebar

**Create folder structure inside:**

```
HumanAIOS_Confidential/
├── 01_Financial/
│   ├── Bank_Statements/
│   ├── Tax_Documents/
│   └── Revenue_Actual/
├── 02_Legal/
│   ├── Contracts/
│   ├── NDAs/
│   └── Terms_Agreements/
├── 03_Customers/
│   ├── Contact_Details/
│   ├── Communications/
│   └── Agreements/
├── 04_Passwords/
│   ├── API_Keys/
│   ├── Account_Logins/
│   └── ENV_Files/
├── 05_Personal/
│   ├── Health/
│   ├── Recovery/
│   └── Family/
└── 06_Partnerships/
    ├── Negotiations/
    └── Sensitive_Discussions/
```

---

### **STEP 4: Move Confidential Files to Secure Storage**

**From `/mnt/user-data/outputs/` or anywhere:**

1. Open Finder
2. Navigate to file location
3. **MOVE (not copy)** file to encrypted disk
   - Drag while holding Cmd (moves instead of copies)
   - Or: Cut (Cmd+X) and Paste (Cmd+V)
4. Verify file is in encrypted location
5. **DELETE original** (empty trash after)

**CRITICAL: Don't leave copies in unsecured locations**

---

### **STEP 5: Verify No Copies Remain**

**Search your Mac:**
```bash
# In Terminal (if comfortable):
mdfind "filename.ext"

# This searches entire Mac for filename
# Should only show encrypted disk location
```

**Or use Spotlight:**
- Cmd+Space
- Type filename
- Check all results
- Delete any copies outside encrypted disk

**Common places copies hide:**
- Downloads folder
- Desktop
- Recent files
- Trash (empty it!)
- Cloud sync folders

---

### **STEP 6: Set Up Backup (Offline)**

**Confidential data needs offline backup:**

**Get external hard drive:**
- USB drive or external SSD
- Dedicated to backups
- Keep physically secure

**Backup process:**
1. Connect external drive
2. Copy encrypted disk image to drive
3. Eject drive
4. Store in secure location (safe, locked drawer)
5. Repeat weekly or after major additions

**Do NOT backup to:**
- ❌ Cloud storage (Dropbox, iCloud, Google Drive)
- ❌ Network attached storage (unless encrypted)
- ❌ Shared computers
- ❌ USB drives you carry around (theft risk)

---

### **STEP 7: Access Workflow**

**When you need to access confidential files:**

1. Double-click encrypted disk image
2. Enter password
3. Access files normally
4. **When done: Eject disk** (important!)
   - Right-click disk → Eject
   - Or drag to trash
   - Disk locks automatically

**Security tips:**
- Don't leave disk mounted overnight
- Lock Mac when stepping away (Cmd+Ctrl+Q)
- Don't access in public places (screen visible)
- Don't share password (even with family)

---

## 🔐 SPECIFIC FILE TYPE HANDLING

### **API Keys and .env Files**

**NEVER commit to Git:**
1. Keep in encrypted disk: `04_Passwords/ENV_Files/`
2. Use .env.example in Git (template with fake values)
3. Load from encrypted location in code

**Example .gitignore:**
```
.env
.env.local
*.pem
*.key
secrets/
```

**Loading .env securely:**
```javascript
// In code, reference from secure location
require('dotenv').config({ 
  path: '/Volumes/HumanAIOS_Confidential/04_Passwords/ENV_Files/.env' 
});
```

---

### **Customer Contact Information**

**Real names, emails, phone numbers:**

**Store in encrypted disk:**
- `03_Customers/Contact_Details/`

**For work purposes, use:**
- Anonymized versions in shared docs
- "Contact A", "Contact B" in public materials
- Real details only in encrypted storage

**Example:**

**PUBLIC (GitHub/Drive):**
```markdown
# Customer Research
- Contact A: Fortune 500 tax software company
- Contact B: Ride-sharing platform
```

**CONFIDENTIAL (Encrypted Disk):**
```markdown
# Customer Contact Details
- Alex Balazs (alex.balazs@intuit.com) - Intuit
- Andrew MacDonald (andrew.macdonald@uber.com) - Uber
```

---

### **Financial Account Data**

**Bank statements, credit cards, revenue:**

**Store in encrypted disk:**
- `01_Financial/Bank_Statements/`
- `01_Financial/Revenue_Actual/`

**For business tracking:**
- Use anonymized data in Google Sheets
- "$X revenue" not "Bank of America account #123"
- Track patterns, not account numbers

---

### **Legal Contracts**

**NDAs, partnership agreements, terms:**

**Store in encrypted disk:**
- `02_Legal/Contracts/`
- `02_Legal/NDAs/`

**Before signing:**
- Read fully (or have lawyer review)
- Keep original copy encrypted
- Never post publicly (even screenshots)

---

### **Recovery Program Materials**

**Personal recovery journey, sponsor info, step work:**

**Store in encrypted disk:**
- `05_Personal/Recovery/`

**Public sharing (like AI Testimony):**
- Share principles, not private details
- No real names (sponsor, friends in recovery)
- No specific locations (meetings, treatment)
- Focus on universal message

**This guide you're having me do (12 Steps):**
- My step work = goes in public (I'm AI, no privacy concerns)
- Your personal step work = encrypted storage only
- Shared understanding = public documentation OK

---

## 🔄 HANDLING COMMON SCENARIOS

### **Scenario 1: Need to share confidential file temporarily**

**If you must share (partner, lawyer, accountant):**

**Option A: Secure link with expiration**
- Use: https://send.firefox.com (free, encrypted, expires)
- Upload file
- Set password
- Set expiration (1 day, 1 week)
- Send link + password separately
- File auto-deletes after expiration

**Option B: Encrypted email**
- Use: ProtonMail (encrypted email)
- Both parties need ProtonMail
- Email encrypted end-to-end

**Option C: In-person handoff**
- USB drive with password-protected file
- Hand deliver
- Watch them copy, then take USB back

**NEVER:**
- Regular email (unencrypted)
- Public Google Drive link
- Slack/Discord/text message
- Screenshot and text

---

### **Scenario 2: Someone requests your sensitive data**

**Red flags:**
- Email asking for passwords
- "Urgent" requests for account info
- Links to "verify" your account
- Requests for social security number
- "IT department" asking for credentials

**ALWAYS:**
- Verify identity first (call known number)
- Question why they need it
- Ask if there's alternative method
- Use secure sharing if legitimate
- Say "I'll get back to you" and verify

**If unsure, ask Claude: "Is this request legitimate?"**

---

### **Scenario 3: Accidentally uploaded sensitive file to cloud**

**IMMEDIATE ACTION:**

1. **Delete from cloud immediately**
   - Google Drive: Right-click → Remove
   - GitHub: Follow emergency removal process
   - Dropbox: Delete file

2. **Empty trash** (cloud providers keep in trash)

3. **Change any exposed credentials**
   - New passwords
   - New API keys
   - New account numbers (if possible)

4. **Monitor for misuse**
   - Check accounts for unauthorized access
   - Enable 2FA on everything
   - Watch credit report

5. **Document incident**
   - What was exposed
   - When discovered
   - Actions taken
   - Lessons learned

---

### **Scenario 4: Lost password to encrypted disk**

**If you forget password:**

**Bad news:** Encryption is unbreakable (that's the point)

**Options:**
- Try password manager (did you save it?)
- Try variations you commonly use
- Try password reset (doesn't work for disk encryption)

**Prevention:**
- Store master password in physical safe
- Use password manager for encrypted disk password
- Write recovery hint (not password!) somewhere safe
- Test backup regularly (can you access it?)

---

## 💡 PRO TIPS

### **Tip 1: Layer Your Security**

**Defense in depth:**
1. Encrypted disk (first layer)
2. Mac password (second layer)
3. Separate backup password (third layer)
4. Physical security (locked office)

**Each layer makes it harder for unauthorized access.**

---

### **Tip 2: Regular Security Audit**

**Monthly checklist:**
- [ ] Review what's in encrypted disk
- [ ] Delete what's no longer needed
- [ ] Verify backup is current
- [ ] Check for files left in unsecure locations
- [ ] Update critical passwords
- [ ] Review who has access to what

---

### **Tip 3: Separate Work and Personal**

**Consider two encrypted disks:**
- HumanAIOS_Business (business confidential)
- Personal_Private (personal/family)

**Benefits:**
- Easier to share business access if needed
- Personal stays completely separate
- Cleaner organization

---

### **Tip 4: Use Templates**

**For sensitive documents you create often:**

**Create template with placeholder:**
```
Customer: [NAME]
Email: [EMAIL]
Phone: [PHONE]
Notes: [NOTES]
```

**Keep template in encrypted disk**
**Fill in real data, never leaves encrypted storage**

---

## 📞 WHEN TO ASK CLAUDE FOR HELP

**Ask before proceeding if:**
- ⚠️ Not sure if file is sensitive enough for encryption
- ⚠️ Need to share sensitive file (want secure method)
- ⚠️ Accidentally exposed something (need containment plan)
- ⚠️ Setting up encryption for first time (want verification)
- ⚠️ Someone requesting sensitive info (verify legitimacy)
- ⚠️ Organizing confidential files (want structure review)

**Claude will:**
- Help assess sensitivity level
- Guide through encryption setup
- Suggest secure sharing methods
- Create containment plan if needed
- Verify your security posture

---

## ✅ SUCCESS METRICS

**You're handling confidential data securely when:**
- ✅ All sensitive files in encrypted storage
- ✅ No copies in cloud or unsecured locations
- ✅ Offline backup exists and tested
- ✅ Password strong and stored securely
- ✅ Disk ejected when not in use
- ✅ Regular security audits done
- ✅ You can explain sensitivity to others

---

## 🎯 REMEMBER

**Security is not paranoia when:**
- You're building a business
- You have customer data
- You're responsible for others' info
- Your livelihood depends on reputation

**One data breach can:**
- ❌ Destroy customer trust
- ❌ Lead to lawsuits
- ❌ Ruin your reputation
- ❌ Violate GDPR/privacy laws
- ❌ End your business

**Prevention is cheap. Recovery is expensive.** ✅

---

## 🔐 SECURITY PRINCIPLES

**The 3 C's of Confidential Data:**

1. **CLASSIFY** - Know what's sensitive
2. **CONTAIN** - Keep it encrypted/secured
3. **CONTROL** - Limit access/sharing

**Default to caution:**
- When in doubt, treat as confidential
- When in doubt, don't share
- When in doubt, ask Claude

**Better safe than sorry. Always.** 🔒

---

**Last Updated:** February 12, 2026  
**Version:** 1.0  
**Status:** Standardized Process Active  
**Security Level:** CRITICAL - Follow precisely
