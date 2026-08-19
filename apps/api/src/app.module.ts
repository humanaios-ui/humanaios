import { Module } from '@nestjs/common';
import { AuthModule } from './auth/auth.module';
import { AgentsModule } from './agents/agents.module';
import { DatabaseModule } from './database/database.module';
import { AssessmentsModule } from './assessments/assessments.module';
import { ACATModule } from './acat/acat.module';
import { SmcuModule } from './smcu/smcu.module';

@Module({
  imports: [DatabaseModule, AuthModule, AgentsModule, ACATModule, AssessmentsModule, SmcuModule],
  controllers: [],
  providers: [],
})
export class AppModule {}
