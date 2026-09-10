/**
 * SMCU Module
 * Bundles the SMCU telemetry service and contextual bandit router.
 */

import { Module } from '@nestjs/common';
import { SmcuTelemetryService } from './smcu-telemetry.service';
import { SmcuRouterService } from './smcu-router.service';
import { DatabaseModule } from '../database/database.module';

@Module({
  imports: [DatabaseModule],
  providers: [SmcuTelemetryService, SmcuRouterService],
  exports: [SmcuTelemetryService, SmcuRouterService],
})
export class SmcuModule {}
