import { Module } from '@nestjs/common';
import { AscGatewayService } from './asc-gateway.service';
import { AscGatewayRepository } from './asc-gateway.repository';
import { AscGatewayAuditEventService } from './asc-gateway-audit-event.service';
import { AscGatewayIntegrationService } from './asc-gateway-integration.service';
import { AscGatewayCryptographicLedgerService } from './asc-gateway-cryptographic-ledger.service';
import { AscGatewayNotificationPayloadService } from './asc-gateway-notification-payload.service';

/**
 * ASC_GATEWAY Module — Complete Log-Only Auditing Stack (§7A)
 *
 * Components:
 * - AscGatewayService: Measurement engine (probe taxonomy, tier ceilings, sequential analysis)
 * - AscGatewayRepository: Supabase persistence layer (audit logging, notifications, compliance)
 * - AscGatewayAuditEventService: Event streaming pipeline (real-time audit events)
 * - AscGatewayIntegrationService: End-to-end orchestration (probe → measurement → persist → notify)
 * - AscGatewayCryptographicLedgerService: Immutable audit trail (hash chain, integrity verification)
 * - AscGatewayNotificationPayloadService: Art. 15 compliance notifications (transparency to deployers)
 *
 * Full stack ready for production deployment with log-only enforcement.
 */
@Module({
  providers: [
    AscGatewayRepository,
    AscGatewayService,
    AscGatewayAuditEventService,
    AscGatewayIntegrationService,
    AscGatewayCryptographicLedgerService,
    AscGatewayNotificationPayloadService,
  ],
  exports: [
    AscGatewayService,
    AscGatewayIntegrationService,
    AscGatewayCryptographicLedgerService,
    AscGatewayNotificationPayloadService,
  ],
})
export class AscGatewayModule {}
