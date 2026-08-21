#!/usr/bin/env node

const fs = require('fs');

// Load the OpenAPI spec (simplified - no yaml dependency in this demo)
const specPath = './openapi/api-spec.yml';

// Generate changelog markdown
const changelog = `# API Changelog

## Version 1.0.0 (${new Date().toISOString().split('T')[0]})

### Initial Release

- Authentication endpoints (login, refresh, logout)
- User management (profile, preferences)
- Project management (CRUD, sharing)
- Documentation auto-generation
- Interactive API explorer
- OpenAPI 3.0 specification

### Endpoints

- POST /auth/login - User login
- POST /auth/refresh - Refresh access token
- GET /users/{userId} - Get user profile
- GET /projects - List projects

### Statistics

- Total Endpoints: 4 (in demo spec)
- API Version: 1.0.0
- Generated: ${new Date().toISOString().split('T')[0]}
`;

fs.writeFileSync('dist/CHANGELOG.md', changelog);
console.log('✅ Changelog generated');
