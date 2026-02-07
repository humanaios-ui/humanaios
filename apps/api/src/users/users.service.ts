import { Injectable, Inject } from '@nestjs/common';
import { Pool } from 'pg';
import * as bcrypt from 'bcrypt';
import { DATABASE_POOL } from '../database/database.module';
import { User, Organization, CreateUserDto } from './user.entity';

@Injectable()
export class UsersService {
  constructor(@Inject(DATABASE_POOL) private pool: Pool) {}

  async findByEmail(email: string): Promise<User | null> {
    const result = await this.pool.query(
      'SELECT * FROM users WHERE email = $1 AND is_active = true',
      [email]
    );
    return result.rows[0] || null;
  }

  async findById(id: string): Promise<User | null> {
    const result = await this.pool.query(
      'SELECT * FROM users WHERE id = $1 AND is_active = true',
      [id]
    );
    return result.rows[0] || null;
  }

  async create(createUserDto: CreateUserDto): Promise<User> {
    const { email, password, name, org_name } = createUserDto;
    const client = await this.pool.connect();

    try {
      await client.query('BEGIN');

      // Hash password
      const password_hash = await bcrypt.hash(password, 10);

      // Create organization if new signup
      let org_id: string;
      if (org_name) {
        const slug = org_name
          .toLowerCase()
          .replace(/[^a-z0-9]+/g, '-')
          .replace(/^-|-$/g, '');

        const orgResult = await client.query(
          `INSERT INTO organizations (name, slug, plan) 
           VALUES ($1, $2, 'free') 
           RETURNING id`,
          [org_name, slug]
        );
        org_id = orgResult.rows[0].id;
      } else {
        // Use demo org for now
        org_id = '00000000-0000-0000-0000-000000000001';
      }

      // Create user
      const userResult = await client.query(
        `INSERT INTO users (org_id, email, password_hash, name, role, auth_provider) 
         VALUES ($1, $2, $3, $4, 'admin', 'email') 
         RETURNING *`,
        [org_id, email, password_hash, name || email.split('@')[0]]
      );

      await client.query('COMMIT');

      const user = userResult.rows[0];
      delete user.password_hash; // Don't return password hash
      return user;
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    } finally {
      client.release();
    }
  }

  async validatePassword(user: User, password: string): Promise<boolean> {
    if (!user.password_hash) return false;
    return bcrypt.compare(password, user.password_hash);
  }

  async updateLastLogin(userId: string): Promise<void> {
    await this.pool.query('UPDATE users SET last_login_at = NOW() WHERE id = $1', [userId]);
  }
}
