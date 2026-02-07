/**
 * HumanAIOS - The Operating System for Human-AI Workflows
 * Copyright (c) 2026 HumanAIOS
 * All rights reserved.
 */

import { Module } from '@nestjs/common';
import { AgentsController } from './agents.controller';
import { AgentsService } from './agents.service';
import { DatabaseModule } from '../database/database.module';

@Module({
  imports: [DatabaseModule],
  controllers: [AgentsController],
  providers: [AgentsService],
  exports: [AgentsService]
})
export class AgentsModule {}
