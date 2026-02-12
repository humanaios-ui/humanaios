# AUTH SYSTEM - INSTALLATION & SETUP GUIDE
**Time to complete:** 60-90 minutes  
**Difficulty:** Intermediate  
**Status:** Ready to implement

---

## 📦 STEP 1: COPY FILES TO YOUR PROJECT (5 min)

### **Option A: Manual Copy**

1. **Download all files** from `/home/claude/auth-system/`
2. **Copy to your HumanAIOS project:**
   ```
   your-project/
   ├── config/
   │   └── database.js
   ├── middleware/
   │   └── authMiddleware.js
   ├── models/
   │   └── User.js
   ├── routes/
   │   └── authRoutes.js
   ├── controllers/
   │   └── authController.js
   ├── utils/
   │   ├── emailService.js
   │   └── tokenService.js
   ├── .env.example
   ├── package.json
   └── server.js
   ```

### **Option B: Use Provided Files**

All files are ready in `/home/claude/auth-system/` directory.

---

## 🔧 STEP 2: INSTALL DEPENDENCIES (5 min)

```bash
# Navigate to auth-system directory
cd /home/claude/auth-system

# Install all dependencies
npm install

# This installs:
# - express (web framework)
# - pg (PostgreSQL client)
# - bcrypt (password hashing)
# - jsonwebtoken (JWT tokens)
# - dotenv (environment variables)
# - express-rate-limit (rate limiting)
# - express-validator (input validation)
# - nodemailer (email sending)
# - uuid (unique IDs)
# - helmet (security headers)
# - cors (cross-origin requests)
```

---

## 🗄️ STEP 3: DATABASE SETUP (10 min)

### **Install PostgreSQL** (if not already installed)

**Mac:**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Ubuntu/Linux:**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### **Create Database**

```bash
# Connect to PostgreSQL
psql postgres

# Create database and user
CREATE DATABASE humanaios;
CREATE USER humanaios_user WITH ENCRYPTED PASSWORD 'your_secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE humanaios TO humanaios_user;

# Exit psql
\q
```

### **Alternative: Use Existing Database**

If you already have a database, just note the connection details for `.env` file.

---

## ⚙️ STEP 4: CONFIGURE ENVIRONMENT (10 min)

### **Create .env file**

```bash
# Copy example file
cp .env.example .env

# Edit with your settings
nano .env  # or use your preferred editor
```

### **Required Configuration:**

```env
# Server
NODE_ENV=development
PORT=3000

# Database - UPDATE THESE
DATABASE_URL=postgresql://humanaios_user:your_secure_password_here@localhost:5432/humanaios
DB_HOST=localhost
DB_PORT=5432
DB_NAME=humanaios
DB_USER=humanaios_user
DB_PASSWORD=your_secure_password_here

# JWT Secrets - GENERATE RANDOM STRINGS
JWT_ACCESS_SECRET=generate-random-64-char-string-here
JWT_REFRESH_SECRET=generate-different-random-64-char-string-here
JWT_ACCESS_EXPIRATION=15m
JWT_REFRESH_EXPIRATION=7d

# Password Reset
PASSWORD_RESET_EXPIRATION=1h
PASSWORD_RESET_SECRET=another-random-64-char-string

# Email (Optional - for password reset)
EMAIL_SERVICE=sendgrid
EMAIL_FROM=noreply@humanaios.com
SENDGRID_API_KEY=your-sendgrid-key-here

# Frontend URL
FRONTEND_URL=http://localhost:3001

# Rate Limiting
MAX_LOGIN_ATTEMPTS=5
LOGIN_ATTEMPT_WINDOW=15m
```

### **Generate Secure Secrets:**

```bash
# Generate random secrets (run 3 times for 3 different secrets)
node -e "console.log(require('crypto').randomBytes(64).toString('hex'))"
```

Copy each output into your `.env` file for the JWT secrets.

---

## 📧 STEP 5: EMAIL SETUP (Optional - 10 min)

### **Option A: SendGrid (Recommended)**

1. Sign up at https://sendgrid.com (free tier: 100 emails/day)
2. Create API key
3. Add to `.env`:
   ```env
   SENDGRID_API_KEY=SG.xxxxxxxxxxxxx
   ```

### **Option B: Gmail SMTP**

```env
EMAIL_SERVICE=gmail
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-specific-password
```

### **Option C: Skip Email (Testing)**

Password reset won't work, but registration/login will.

---

## 🚀 STEP 6: START THE SERVER (2 min)

```bash
# Development mode (auto-restart on changes)
npm run dev

# Or production mode
npm start
```

### **Expected Output:**

```
✅ Database connected successfully
✅ Database tables initialized successfully

╔════════════════════════════════════════╗
║   🚀 HumanAIOS Auth Server Running    ║
║                                        ║
║   Port: 3000                           ║
║   Environment: development             ║
║   Database: Connected ✅               ║
║                                        ║
║   API Endpoints:                       ║
║   POST /api/auth/register              ║
║   POST /api/auth/login                 ║
║   POST /api/auth/refresh-token         ║
║   POST /api/auth/logout                ║
║   POST /api/auth/request-password-reset║
║   POST /api/auth/reset-password        ║
║   GET  /api/auth/profile               ║
║   PUT  /api/auth/profile               ║
║                                        ║
║   Health: http://localhost:3000/health ║
╚════════════════════════════════════════╝
```

---

## ✅ STEP 7: TEST THE ENDPOINTS (20 min)

### **Test 1: Health Check**

```bash
curl http://localhost:3000/health
```

**Expected:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-11T18:00:00.000Z",
  "uptime": 5.123
}
```

---

### **Test 2: Register New User**

```bash
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "carly@humanaios.com",
    "password": "SecurePass123",
    "firstName": "Carly",
    "lastName": "Anderson"
  }'
```

**Expected:**
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user": {
      "id": "uuid-here",
      "email": "carly@humanaios.com",
      "firstName": "Carly",
      "lastName": "Anderson",
      "role": "user"
    },
    "accessToken": "eyJhbGciOiJIUzI1NiIs...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIs..."
  }
}
```

**Save the accessToken** - you'll need it for next tests!

---

### **Test 3: Login**

```bash
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "carly@humanaios.com",
    "password": "SecurePass123"
  }'
```

**Expected:** Same response as registration with new tokens.

---

### **Test 4: Get Profile (Protected Route)**

```bash
# Replace YOUR_ACCESS_TOKEN with token from register/login
curl -X GET http://localhost:3000/api/auth/profile \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Expected:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid-here",
      "email": "carly@humanaios.com",
      "firstName": "Carly",
      "lastName": "Anderson",
      "role": "user",
      "isVerified": false,
      "createdAt": "2026-02-11T18:00:00.000Z"
    }
  }
}
```

---

### **Test 5: Update Profile**

```bash
curl -X PUT http://localhost:3000/api/auth/profile \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Carly",
    "lastName": "Anderson-Updated"
  }'
```

---

### **Test 6: Request Password Reset**

```bash
curl -X POST http://localhost:3000/api/auth/request-password-reset \
  -H "Content-Type: application/json" \
  -d '{
    "email": "carly@humanaios.com"
  }'
```

**Expected:**
```json
{
  "success": true,
  "message": "If that email exists, a password reset link has been sent"
}
```

**Check email** for reset link (if email configured).

---

### **Test 7: Refresh Token**

```bash
# Replace YOUR_REFRESH_TOKEN with refreshToken from login
curl -X POST http://localhost:3000/api/auth/refresh-token \
  -H "Content-Type: application/json" \
  -d '{
    "refreshToken": "YOUR_REFRESH_TOKEN"
  }'
```

**Expected:**
```json
{
  "success": true,
  "data": {
    "accessToken": "new-access-token-here"
  }
}
```

---

### **Test 8: Logout**

```bash
curl -X POST http://localhost:3000/api/auth/logout \
  -H "Content-Type: application/json" \
  -d '{
    "refreshToken": "YOUR_REFRESH_TOKEN"
  }'
```

---

## 🧪 AUTOMATED TESTING (Optional - 15 min)

### **Create test file:**

```bash
npm install --save-dev jest supertest
```

Create `tests/auth.test.js`:

```javascript
const request = require('supertest');
const app = require('../server');

describe('Auth Endpoints', () => {
  let accessToken;
  let refreshToken;
  const testUser = {
    email: 'test@example.com',
    password: 'TestPass123',
    firstName: 'Test',
    lastName: 'User',
  };

  test('POST /api/auth/register - should register new user', async () => {
    const res = await request(app)
      .post('/api/auth/register')
      .send(testUser);
    
    expect(res.statusCode).toBe(201);
    expect(res.body.success).toBe(true);
    expect(res.body.data.user.email).toBe(testUser.email);
    
    accessToken = res.body.data.accessToken;
    refreshToken = res.body.data.refreshToken;
  });

  test('POST /api/auth/login - should login user', async () => {
    const res = await request(app)
      .post('/api/auth/login')
      .send({
        email: testUser.email,
        password: testUser.password,
      });
    
    expect(res.statusCode).toBe(200);
    expect(res.body.success).toBe(true);
  });

  test('GET /api/auth/profile - should get user profile', async () => {
    const res = await request(app)
      .get('/api/auth/profile')
      .set('Authorization', `Bearer ${accessToken}`);
    
    expect(res.statusCode).toBe(200);
    expect(res.body.data.user.email).toBe(testUser.email);
  });

  test('POST /api/auth/refresh-token - should refresh token', async () => {
    const res = await request(app)
      .post('/api/auth/refresh-token')
      .send({ refreshToken });
    
    expect(res.statusCode).toBe(200);
    expect(res.body.data.accessToken).toBeDefined();
  });
});
```

### **Run tests:**

```bash
npm test
```

---

## 📊 DATABASE VERIFICATION (5 min)

### **Check created tables:**

```bash
psql humanaios

# List tables
\dt

# Should show:
# - users
# - refresh_tokens
# - password_reset_tokens

# View users
SELECT id, email, first_name, last_name, role, created_at FROM users;

# Exit
\q
```

---

## 🎯 SUCCESS CHECKLIST

After setup, verify:

- [ ] ✅ Server starts without errors
- [ ] ✅ Database tables created
- [ ] ✅ Health endpoint responds
- [ ] ✅ Can register new user
- [ ] ✅ Can login with credentials
- [ ] ✅ Can access protected routes with token
- [ ] ✅ Can refresh access token
- [ ] ✅ Can logout (revoke refresh token)
- [ ] ✅ Can request password reset
- [ ] ✅ Rate limiting works (try 6+ login attempts)

**If all checked:** Auth system is COMPLETE! ✅

---

## 🔒 SECURITY FEATURES INCLUDED

✅ **Password Security:**
- Bcrypt hashing with salt rounds = 12
- Minimum 8 characters, uppercase, lowercase, number required
- Passwords never stored in plain text

✅ **Token Security:**
- Access tokens: Short-lived (15 min)
- Refresh tokens: Long-lived (7 days), stored in database
- Refresh token rotation on use
- All user tokens revoked on password reset

✅ **Account Protection:**
- Rate limiting (5 login attempts per 15 min)
- Account lockout after failed attempts (15 min)
- Password reset tokens expire in 1 hour
- One-time use reset tokens

✅ **Request Security:**
- Helmet.js security headers
- CORS protection
- Input validation (express-validator)
- SQL injection prevention (parameterized queries)
- XSS protection

---

## 🚨 TROUBLESHOOTING

### **Error: "Database connection failed"**

```bash
# Check PostgreSQL is running
brew services list  # Mac
sudo systemctl status postgresql  # Linux

# Check connection details in .env match database
```

### **Error: "EADDRINUSE - Port 3000 already in use"**

```bash
# Find and kill process
lsof -ti:3000 | xargs kill -9

# Or use different port in .env
PORT=3001
```

### **Error: "Invalid JWT secret"**

```bash
# Regenerate secrets
node -e "console.log(require('crypto').randomBytes(64).toString('hex'))"

# Update in .env
```

### **Email not sending**

- Check SENDGRID_API_KEY is correct
- Verify sender email is verified in SendGrid
- Check spam folder
- For testing: Comment out email lines, focus on core auth

---

## 📝 NEXT STEPS AFTER AUTH COMPLETE

1. **Integrate with Frontend:**
   - Create login/register forms
   - Store tokens in localStorage/sessionStorage
   - Add Authorization header to API requests
   - Handle token refresh

2. **Add MCP Integration:**
   - Use auth middleware to protect MCP endpoints
   - Authenticate AI agent requests
   - Authorize based on user role

3. **Deploy to Production:**
   - Use environment variables for secrets
   - Enable HTTPS
   - Configure production database
   - Set up email service (SendGrid production)

---

## ✅ COMPLETION TIME ESTIMATE

**Actual implementation time:**
- Setup & install: 20 min
- Database config: 10 min
- Environment config: 10 min
- Testing: 20 min
- Debugging: 10-20 min (if issues)

**Total: 70-90 minutes** ✅

---

**Auth system code is ready to implement!** 🚀

**All files provided. Start with Step 1 and work through sequentially.**

**Questions? Need debugging help? Just ask!**
