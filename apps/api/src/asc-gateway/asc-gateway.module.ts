import { Module } from '@nestjs/common';
import { AscGatewayService } from './asc-gateway.service';
import { AscGatewayRepository } from './asc-gateway.repository';

/**
 * ASC_GATEWAY Module
 * Provides runtime auditing for deployed AI assistants (measurement engine + log-only persistence).
 * Integrates with Supabase for audit logging and compliance.
 */
@Module({
  providers: [AscGatewayRepository, AscGatewayService],
  exports: [AscGatewayService],
})
export class AscGatewayModule {}
