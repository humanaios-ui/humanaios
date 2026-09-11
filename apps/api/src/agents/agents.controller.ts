import {
  Controller,
  Get,
  Post,
  Body,
  Param,
  Query,
  UseGuards,
  Request,
} from '@nestjs/common';
import { AgentsService } from './agents.service';
import { CreateAgentDto, CreateActivityDto } from './agent.entity';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';

@Controller('agents')
@UseGuards(JwtAuthGuard)
export class AgentsController {
  constructor(private readonly agentsService: AgentsService) {}

  @Post()
  async create(@Request() req, @Body() createAgentDto: CreateAgentDto) {
    return this.agentsService.createAgent(req.user.org_id, createAgentDto);
  }

  @Get()
  async findAll(@Request() req) {
    return this.agentsService.findAllByOrg(req.user.org_id);
  }

  @Get(':id')
  async findOne(@Request() req, @Param('id') id: string) {
    return this.agentsService.findOne(id, req.user.org_id);
  }

  @Post(':id/activities')
  async createActivity(
    @Request() req,
    @Param('id') agentId: string,
    @Body() createActivityDto: CreateActivityDto
  ) {
    return this.agentsService.createActivity(
      agentId,
      req.user.org_id,
      createActivityDto
    );
  }

  @Get(':id/activities')
  async findActivities(
    @Request() req,
    @Param('id') agentId: string,
    @Query('limit') limit?: string,
    @Query('offset') offset?: string
  ) {
    return this.agentsService.findActivities(
      agentId,
      req.user.org_id,
      limit ? parseInt(limit, 10) : 100,
      offset ? parseInt(offset, 10) : 0
    );
  }
}
