import { Module, Global } from '@nestjs/common';
import { Pool } from 'pg';
import { createClient } from 'redis';

export const DATABASE_POOL = 'DATABASE_POOL';
export const REDIS_CLIENT = 'REDIS_CLIENT';

@Global()
@Module({
  providers: [
    {
      provide: DATABASE_POOL,
      useFactory: () => {
        const pool = new Pool({
          connectionString: process.env.DATABASE_URL,
          max: 20,
          idleTimeoutMillis: 30000,
          connectionTimeoutMillis: 2000,
        });

        pool.on('error', (err) => {
          console.error('Unexpected database error:', err);
        });

        return pool;
      },
    },
    {
      provide: REDIS_CLIENT,
      useFactory: async () => {
        const client = createClient({
          url: process.env.REDIS_URL,
        });

        client.on('error', (err) => console.error('Redis Client Error', err));
        await client.connect();

        return client;
      },
    },
  ],
  exports: [DATABASE_POOL, REDIS_CLIENT],
})
export class DatabaseModule {}
