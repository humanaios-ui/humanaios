/**
 * HumanAIOS ACAT Module
 * Bundles ACAT protocol service, database layer, and orchestration
 */

import { Module, forwardRef } from '@nestjs/common';
import { ACATService } from './acat.service';
import { ACATPromptTemplateService } from './acat-prompt-templates';
import { ACATSystemClient } from './acat-system-client';
import { ACATFlagDetector } from './acat-flag-detector';
import { DatabaseModule } from '../database/database.module';
import { AssessmentsModule } from '../assessments/assessments.module';

@Module({
  imports: [DatabaseModule, forwardRef(() => AssessmentsModule)],
  providers: [ACATService, ACATPromptTemplateService, ACATSystemClient, ACATFlagDetector],
  exports: [ACATService, ACATPromptTemplateService, ACATSystemClient, ACATFlagDetector],
})
export class ACATModule {}
