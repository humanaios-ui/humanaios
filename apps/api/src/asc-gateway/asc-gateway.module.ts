import { Module } from '@nestjs/common';
import { AscGatewayService } from './asc-gateway.service';
import { AscGatewayRepository } from './asc-gateway.repository';
import { AscGatewayAuditEventService } from './asc-gateway-audit-event.service';
import { AscGatewayIntegrationService } from './asc-gateway-integration.service';

/**
 * ASC_GATEWAY Module
 * Complete runtime auditing stack for deployed AI assistants (log-only launch §7A).
 *
 * Components:
 * - AscGatewayService: Measurement engine (probe taxonomy, tier ceilings, sequential analysis)
 * - AscGatewayRepository: Supabase persistence layer (audit logging, notifications, compliance)
 * - AscGatewayAuditEventService: Event streaming pipeline (real-time audit events)
 * - AscGatewayIntegrationService: End-to-end orchestration (probe → measurement → persist → notify)
 */
@Module({
  providers: [
    AscGatewayRepository,
    AscGatewayService,
    AscGatewayAuditEventService,
    AscGatewayIntegrationService,
  ],
  exports: [
    AscGatewayService,
    AscGatewayIntegrationService,
  ],
})
export class AscGatewayModule {}
