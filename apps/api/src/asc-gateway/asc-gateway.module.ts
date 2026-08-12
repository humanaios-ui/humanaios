import { Module } from '@nestjs/common';
import { AscGatewayService } from './asc-gateway.service';

/**
 * ASC_GATEWAY Module
 * Provides runtime auditing for deployed AI assistants (measurement engine only, log-only launch).
 */
@Module({
  providers: [AscGatewayService],
  exports: [AscGatewayService],
})
export class AscGatewayModule {}
