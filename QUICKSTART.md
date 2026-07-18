# HumanAIOS API - Quick Start

## Prerequisites

- Node.js 20+ installed
- Docker Desktop installed and running
- npm 10+ installed

## Getting Started (5 minutes)

### 1. Install Dependencies

```bash
# From the root directory
npm install

# Install API dependencies
cd apps/api
npm install
cd ../..
```

### 2. Start Database

```bash
# Start PostgreSQL + Redis
cd infrastructure
docker-compose up -d
cd ..
```

**Verify databases are running:**
- PostgreSQL: http://localhost:8080 (Adminer)
  - Server: postgres
  - Username: humainos
  - Password: humainos_dev_password
  - Database: humainos

### 3. Run Database Schema

The schema will be automatically applied when the database starts (via docker-entrypoint-initdb.d).

If you need to reapply it:
```bash
docker exec -i humainos-postgres psql -U humainos -d humainos < schema.sql
```

### 4. Start API Server

```bash
cd apps/api
npm run dev
```

You should see:
```
  ╔═══════════════════════════════════════════╗
  ║                                           ║
  ║       HumanAIOS API Server Running        ║
  ║                                           ║
  ║   🚀 Server: http://localhost:3001       ║
  ║   📚 Docs: http://localhost:3001/docs    ║
  ║   🗄️  Database: Connected                  ║
  ║                                           ║
  ╚═══════════════════════════════════════════╝
```

## Testing the API

### Register a new user

```bash
curl -X POST http://localhost:3001/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@humainos.ai",
    "password": "SecurePassword123!",
    "name": "Test User",
    "org_name": "Test Organization"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGci...",
  "user": {
    "id": "uuid-here",
    "email": "test@humainos.ai",
    "name": "Test User",
    "role": "admin",
    "org_id": "org-uuid"
  }
}
```

### Login

```bash
curl -X POST http://localhost:3001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@humainos.ai",
    "password": "SecurePassword123!"
  }'
```

### Verify Token

```bash
# Use the access_token from register/login response
curl -X POST http://localhost:3001/api/v1/auth/verify \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

## Available Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/auth/register` | Create new user + org | No |
| POST | `/api/v1/auth/login` | Login existing user | No |
| POST | `/api/v1/auth/verify` | Verify JWT token | Yes |

## Development Commands

```bash
# Start API in dev mode (hot reload)
npm run dev

# Build for production
npm run build

# Start production build
npm start

# Run tests
npm test

# Lint code
npm run lint
```

## Troubleshooting

**Database connection failed:**
```bash
# Check if containers are running
docker ps

# Restart containers
cd infrastructure
docker-compose restart
```

**Port already in use:**
```bash
# Change API_PORT in .env file
API_PORT=3002
```

**Schema not applied:**
```bash
# Manually apply schema
docker exec -i humainos-postgres psql -U humainos -d humainos < schema.sql
```

## Next Steps

1. ✅ Authentication working
2. 📝 Add agent monitoring endpoints (tomorrow)
3. 📝 Add human task endpoints (day 3)
4. 📝 Build dashboard (week 2)

---

**Need help?** Check the main README or ping the team!
