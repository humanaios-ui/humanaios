const jwt = require('jsonwebtoken');
const { v4: uuidv4 } = require('uuid');
const { query } = require('../config/database');

class TokenService {
  static generateAccessToken(userId, email, role) {
    return jwt.sign(
      { userId, email, role },
      process.env.JWT_ACCESS_SECRET,
      { expiresIn: process.env.JWT_ACCESS_EXPIRATION || '15m' }
    );
  }

  static async generateRefreshToken(userId) {
    const token = jwt.sign(
      { userId, tokenId: uuidv4() },
      process.env.JWT_REFRESH_SECRET,
      { expiresIn: process.env.JWT_REFRESH_EXPIRATION || '7d' }
    );

    const expiresAt = new Date();
    expiresAt.setDate(expiresAt.getDate() + 7);

    await query(
      'INSERT INTO refresh_tokens (user_id, token, expires_at) VALUES ($1, $2, $3)',
      [userId, token, expiresAt]
    );

    return token;
  }

  static verifyAccessToken(token) {
    try {
      return jwt.verify(token, process.env.JWT_ACCESS_SECRET);
    } catch (error) {
      throw new Error('Invalid or expired access token');
    }
  }

  static async verifyRefreshToken(token) {
    try {
      const payload = jwt.verify(token, process.env.JWT_REFRESH_SECRET);
      const result = await query(
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

  static async revokeRefreshToken(token) {
    await query('DELETE FROM refresh_tokens WHERE token = $1', [token]);
  }

  static async revokeAllUserTokens(userId) {
    await query('DELETE FROM refresh_tokens WHERE user_id = $1', [userId]);
  }

  static async cleanupExpiredTokens() {
    await query('DELETE FROM refresh_tokens WHERE expires_at < NOW()');
    await query('DELETE FROM password_reset_tokens WHERE expires_at < NOW()');
  }

  static async generatePasswordResetToken(userId) {
    const token = uuidv4();
    const expiresAt = new Date();
    expiresAt.setHours(expiresAt.getHours() + 1);

    await query(
      'INSERT INTO password_reset_tokens (user_id, token, expires_at) VALUES ($1, $2, $3)',
      [userId, token, expiresAt]
    );

    return token;
  }

  static async verifyPasswordResetToken(token) {
    const result = await query(
      `SELECT * FROM password_reset_tokens 
       WHERE token = $1 AND expires_at > NOW() AND used = false`,
      [token]
    );

    if (result.rows.length === 0) {
      throw new Error('Invalid or expired password reset token');
    }

    return result.rows[0];
  }

  static async markPasswordResetTokenAsUsed(token) {
    await query(
      'UPDATE password_reset_tokens SET used = true WHERE token = $1',
      [token]
    );
  }
}

module.exports = TokenService;
