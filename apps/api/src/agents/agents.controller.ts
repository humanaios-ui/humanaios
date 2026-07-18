import { Controller, Get, Post, Body, Param, Query } from '@nestjs/common';
import { CreateAgentDto, LogActivityDto } from './agent.entity';

@Controller('agents')
export class AgentsController {
  constructor() {}

  @Post()
  async createAgent(@Body() createAgentDto: CreateAgentDto) {
    // Bypass service - return mock for SDK testing
    return {
      id: 'agent-' + Date.now(),
      name: createAgentDto.name,
      type: createAgentDto.type,
      description: createAgentDto.description,
      status: 'active',
      created_at: new Date().toISOString(),
      user_id: 'test-user-id',
    };
  }

  @Get()
  async getAgents() {
    return [];
  }

  @Get(':id')
  async getAgent(@Param('id') id: string) {
    return {
      id: id,
      name: 'Mock Agent',
      type: 'test',
      status: 'active',
      created_at: new Date().toISOString(),
    };
  }

  @Post(':id/activities')
  async logActivity(
    @Param('id') agentId: string,
    @Body() logActivityDto: LogActivityDto
  ) {
    return {
      id: 'activity-' + Date.now(),
      agent_id: agentId,
      activity_type: logActivityDto.activity_type,
      description: logActivityDto.description,
      metadata: logActivityDto.metadata,
      created_at: new Date().toISOString(),
    };
  }

  @Get(':id/activities')
  async getActivities(
    @Param('id') agentId: string,
    @Query('limit') limit?: number,
    @Query('offset') offset?: number
  ) {
    return [];
  }
}
