import { Controller, Get, Post, Body, Param, Query } from '@nestjs/common';
import { AgentsService } from './agents.service';
import { CreateAgentDto, LogActivityDto } from './agent.entity';

@Controller('agents')
export class AgentsController {
  constructor(private agentsService: AgentsService) {}

  @Post()
  async createAgent(@Body() createAgentDto: CreateAgentDto) {
    return this.agentsService.createAgent(createAgentDto, 'test-user-id');
  }

  @Get()
  async getAgents() {
    return this.agentsService.getAgents('test-user-id');
  }

  @Get(':id')
  async getAgent(@Param('id') id: string) {
    return this.agentsService.getAgent(id, 'test-user-id');
  }

  @Post(':id/activities')
  async logActivity(
    @Param('id') agentId: string,
    @Body() logActivityDto: LogActivityDto
  ) {
    return this.agentsService.logActivity(agentId, logActivityDto);
  }

  @Get(':id/activities')
  async getActivities(
    @Param('id') agentId: string,
    @Query('limit') limit?: number,
    @Query('offset') offset?: number
  ) {
    return this.agentsService.getActivities(
      agentId,
      limit ? parseInt(limit.toString()) : 100,
      offset ? parseInt(offset.toString()) : 0
    );
  }
}
