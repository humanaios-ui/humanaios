/**
 * HumanAIOS ACAT Module
 * Bundles ACAT protocol service, database layer, and orchestration
 */

import { Module } from '@nestjs/common';
import { ACATService } from './acat.service';
import { DatabaseModule } from '../database/database.module';
import { AssessmentsModule } from '../assessments/assessments.module';

@Module({
  imports: [DatabaseModule, AssessmentsModule],
  providers: [ACATService],
  exports: [ACATService],
})
export class ACATModule {}
