import { NestFactory } from '@nestjs/core';
import { ValidationPipe } from '@nestjs/common';
import { AppModule } from './app.module';
import helmet from 'helmet';
import compression from 'compression';
import * as dotenv from 'dotenv';

dotenv.config();

async function bootstrap() {
  const app = await NestFactory.create(AppModule, {
    logger: ['error', 'warn', 'log', 'debug'],
  });

  // Security
  app.use(helmet());
  app.use(compression());

  // CORS
  app.enableCors({
    origin: process.env.CORS_ORIGIN || 'http://localhost:3000',
    credentials: true,
  });

  // Validation
  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,
      forbidNonWhitelisted: true,
      transform: true,
    })
  );

  // Global prefix
  app.setGlobalPrefix('api/v1');

  const port = process.env.API_PORT || 3001;
  await app.listen(port);

  console.log(`
  ╔═══════════════════════════════════════════╗
  ║                                           ║
  ║       HumanAIOS API Server Running        ║
  ║                                           ║
  ║   🚀 Server: http://localhost:${port}       ║
  ║   📚 Docs: http://localhost:${port}/docs    ║
  ║   🗄️  Database: Connected                  ║
  ║                                           ║
  ╚═══════════════════════════════════════════╝
  `);
}

bootstrap();
