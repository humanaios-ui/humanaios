const jwt = require('jsonwebtoken');
const { v4: uuidv4 } = require('uuid');

class TokenService {
  constructor(dbQuery, config = {}) {
    this.query = dbQuery; // Dependency injection: database query function
    this.config = {
      accessSecret: config.accessSecret || process.env.JWT_ACCESS_SECRET,
      refreshSecret: config.refreshSecret || process.env.JWT_REFRESH_SECRET,
      accessExpiration: config.accessExpiration || process.env.JWT_ACCESS_EXPIRATION || '15m',
      refreshExpiration: config.refreshExpiration || process.env.JWT_REFRESH_EXPIRATION || '7d',
    };
  }

  generateAccessToken(userId, email, role) {
    return jwt.sign(
      { userId, email, role },
      this.config.accessSecret,
      { expiresIn: this.config.accessExpiration }
    );
  }

  async generateRefreshToken(userId) {
    const token = jwt.sign(
      { userId, tokenId: uuidv4() },
      this.config.refreshSecret,
      { expiresIn: this.config.refreshExpiration }
    );

    const expiresAt = new Date();
    expiresAt.setDate(expiresAt.getDate() + 7);

    await this.query(
      'INSERT INTO refresh_tokens (user_id, token, expires_at) VALUES ($1, $2, $3)',
      [userId, token, expiresAt]
    );

    return token;
  }

  verifyAccessToken(token) {
    try {
      return jwt.verify(token, this.config.accessSecret);
    } catch (error) {
      throw new Error('Invalid or expired access token');
    }
  }

  async verifyRefreshToken(token) {
    try {
      const payload = jwt.verify(token, this.config.refreshSecret);
      const result = await this.query(
        'SELECT * FROM refresh_tokens WHERE token = $1 AND expires_at > NOW()',
        [token]
      );
      if (result.rows.length === 0) {
        throw new Error('Invalid or expired refresh token');
      }
      return payload;
    } catch (error) {
      throw new Error('Invalid or expired refresh token');
    }
  }

  async revokeRefreshToken(token) {
    await this.query('DELETE FROM refresh_tokens WHERE token = $1', [token]);
  }

  async revokeAllUserTokens(userId) {
    await this.query('DELETE FROM refresh_tokens WHERE user_id = $1', [userId]);
  }

  async cleanupExpiredTokens() {
    await this.query('DELETE FROM refresh_tokens WHERE expires_at < NOW()');
    await this.query('DELETE FROM password_reset_tokens WHERE expires_at < NOW()');
  }

  async generatePasswordResetToken(userId) {
    const token = uuidv4();
    const expiresAt = new Date();
    expiresAt.setHours(expiresAt.getHours() + 1);

    await this.query(
      'INSERT INTO password_reset_tokens (user_id, token, expires_at) VALUES ($1, $2, $3)',
      [userId, token, expiresAt]
    );

    return token;
  }

  async verifyPasswordResetToken(token) {
    const result = await this.query(
      `SELECT * FROM password_reset_tokens
       WHERE token = $1 AND expires_at > NOW() AND used = false`,
      [token]
    );

    if (result.rows.length === 0) {
      throw new Error('Invalid or expired password reset token');
    }

    return result.rows[0];
  }

  async markPasswordResetTokenAsUsed(token) {
    await this.query(
      'UPDATE password_reset_tokens SET used = true WHERE token = $1',
      [token]
    );
  }
}

module.exports = TokenService;
