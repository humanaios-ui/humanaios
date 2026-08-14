/**
 * HumanAIOS Assessments Module
 * Orchestrates assessment API, job queue, and result persistence
 */

import { Module, OnApplicationShutdown, forwardRef } from '@nestjs/common';
import { AssessmentsService } from './assessments.service';
import { AssessmentsController } from './assessments.controller';
import { AssessmentsRepository } from './assessments.repository';
import { ACATModule } from '../acat/acat.module';
import { DatabaseModule } from '../database/database.module';

@Module({
  imports: [DatabaseModule, forwardRef(() => ACATModule)],
  providers: [AssessmentsService, AssessmentsRepository],
  controllers: [AssessmentsController],
  exports: [AssessmentsService, AssessmentsRepository],
})
export class AssessmentsModule implements OnApplicationShutdown {
  constructor(private assessmentsService: AssessmentsService) {}

  onApplicationShutdown(signal?: string) {
    this.assessmentsService.cleanupAllTimeouts();
  }
}
