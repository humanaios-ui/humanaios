const bcrypt = require('bcrypt');
const { query } = require('../config/database');

class User {
  static async create({ email, password, firstName, lastName, role = 'user' }) {
    const passwordHash = await bcrypt.hash(password, 12);
    const result = await query(
      `INSERT INTO users (email, password_hash, first_name, last_name, role)
       VALUES ($1, $2, $3, $4, $5)
       RETURNING id, email, first_name, last_name, role, is_verified, created_at`,
      [email.toLowerCase(), passwordHash, firstName, lastName, role]
    );
    return result.rows[0];
  }

  static async findByEmail(email) {
    const result = await query(
      'SELECT * FROM users WHERE email = $1',
      [email.toLowerCase()]
    );
    return result.rows[0];
  }

  static async findById(id) {
    const result = await query(
      'SELECT id, email, first_name, last_name, role, is_verified, is_active, created_at FROM users WHERE id = $1',
      [id]
    );
    return result.rows[0];
  }

  static async verifyPassword(plainPassword, passwordHash) {
    return await bcrypt.compare(plainPassword, passwordHash);
  }

  static async updatePassword(userId, newPassword) {
    const passwordHash = await bcrypt.hash(newPassword, 12);
    await query(
      'UPDATE users SET password_hash = $1, updated_at = CURRENT_TIMESTAMP WHERE id = $2',
      [passwordHash, userId]
    );
  }

  static async incrementLoginAttempts(email) {
    await query(
      `UPDATE users 
       SET login_attempts = login_attempts + 1,
           locked_until = CASE 
             WHEN login_attempts + 1 >= 5 THEN CURRENT_TIMESTAMP + INTERVAL '15 minutes'
             ELSE locked_until
           END
       WHERE email = $1`,
      [email.toLowerCase()]
    );
  }

  static async resetLoginAttempts(email) {
    await query(
      'UPDATE users SET login_attempts = 0, locked_until = NULL WHERE email = $1',
      [email.toLowerCase()]
    );
  }

  static async isAccountLocked(email) {
    const result = await query(
      'SELECT locked_until FROM users WHERE email = $1',
      [email.toLowerCase()]
    );
    if (!result.rows[0]) return false;
    const lockedUntil = result.rows[0].locked_until;
    if (!lockedUntil) return false;
    return new Date(lockedUntil) > new Date();
  }

  static async updateProfile(userId, { firstName, lastName }) {
    const result = await query(
      `UPDATE users 
       SET first_name = $1, last_name = $2, updated_at = CURRENT_TIMESTAMP
       WHERE id = $3
       RETURNING id, email, first_name, last_name, role`,
      [firstName, lastName, userId]
    );
    return result.rows[0];
  }
}

module.exports = User;
