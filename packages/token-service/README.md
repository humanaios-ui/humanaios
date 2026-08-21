# @humanaios/token-service

JWT token service module for HumanAIOS with refresh token and password reset token management.

## Installation

```bash
npm install @humanaios/token-service
```

## Configuration

Set environment variables:
- `JWT_ACCESS_SECRET` - Secret for signing access tokens
- `JWT_REFRESH_SECRET` - Secret for signing refresh tokens
- `JWT_ACCESS_EXPIRATION` - Access token expiration (default: 15m)
- `JWT_REFRESH_EXPIRATION` - Refresh token expiration (default: 7d)

Or pass config object to constructor.

## Initialization

Requires database query function for token storage:

```javascript
const TokenService = require('@humanaios/token-service');
const { query } = require('./config/database');

const tokenService = new TokenService(query, {
  accessSecret: process.env.JWT_ACCESS_SECRET,
  refreshSecret: process.env.JWT_REFRESH_SECRET,
});
```

## API

### generateAccessToken(userId, email, role)

Generate a new access token.

**Parameters:**
- `userId` (string) - User ID
- `email` (string) - User email
- `role` (string) - User role

**Returns:** string (JWT token)

### async generateRefreshToken(userId)

Generate and store a refresh token.

**Parameters:**
- `userId` (string) - User ID

**Returns:** Promise<string> (JWT token)

### verifyAccessToken(token)

Verify and decode an access token.

**Parameters:**
- `token` (string) - JWT token

**Returns:** object (decoded token payload)

**Throws:** Error if token is invalid or expired

### async verifyRefreshToken(token)

Verify and validate a refresh token from storage.

**Parameters:**
- `token` (string) - JWT token

**Returns:** Promise<object> (decoded token payload)

### async revokeRefreshToken(token)

Revoke a single refresh token.

**Parameters:**
- `token` (string) - JWT token

**Returns:** Promise<void>

### async revokeAllUserTokens(userId)

Revoke all refresh tokens for a user.

**Parameters:**
- `userId` (string) - User ID

**Returns:** Promise<void>

### async cleanupExpiredTokens()

Delete expired refresh and password reset tokens from storage.

**Returns:** Promise<void>

### async generatePasswordResetToken(userId)

Generate and store a password reset token.

**Parameters:**
- `userId` (string) - User ID

**Returns:** Promise<string> (reset token)

### async verifyPasswordResetToken(token)

Verify a password reset token.

**Parameters:**
- `token` (string) - Reset token

**Returns:** Promise<object> (token record from database)

### async markPasswordResetTokenAsUsed(token)

Mark a password reset token as used.

**Parameters:**
- `token` (string) - Reset token

**Returns:** Promise<void>

## Dependencies

- jsonwebtoken ^9.0.0 - JWT signing and verification
- uuid ^9.0.0 - Token ID generation

## Database Schema

Requires these tables:

```sql
CREATE TABLE refresh_tokens (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR NOT NULL,
  token VARCHAR NOT NULL UNIQUE,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE password_reset_tokens (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR NOT NULL,
  token VARCHAR NOT NULL UNIQUE,
  expires_at TIMESTAMP NOT NULL,
  used BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW()
);
```

## License

MIT
