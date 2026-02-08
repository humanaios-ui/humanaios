/**
 * HumanAIOS - The Operating System for Human-AI Workflows
 * Copyright (c) 2026 HumanAIOS
 * All rights reserved.
 */

import {
  Controller,
  Get,
  Post,
  Body,
  Param,
  Query,
  UseGuards,
  Request
} from '@nestjs/common';
import { AgentsService } from './agents.service';
import { CreateAgentDto, CreateActivityDto } from './agent.entity';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';

@Controller('api/v1/agents')
@UseGuards(JwtAuthGuard)
export class AgentsController {
  constructor(private readonly agentsService: AgentsService) {}

  @Post()
  async create(@Request() req, @Body() createAgentDto: CreateAgentDto) {
    const orgId = req.user.org_id;
    return this.agentsService.createAgent(orgId, createAgentDto);
  }

  @Get()
  async findAll(@Request() req) {
    const orgId = req.user.org_id;
    return this.agentsService.findAllByOrg(orgId);
  }

  @Get(':id')
  async findOne(@Request() req, @Param('id') id: string) {
    const orgId = req.user.org_id;
    return this.agentsService.findOne(id, orgId);
  }

  @Post(':id/activities')
  async createActivity(
    @Request() req,
    @Param('id') agentId: string,
    @Body() createActivityDto: CreateActivityDto
  ) {
    const orgId = req.user.org_id;
    return this.agentsService.createActivity(agentId, orgId, createActivityDto);
  }

  @Get(':id/activities')
  async findActivities(
    @Request() req,
    @Param('id') agentId: string,
    @Query('limit') limit?: string,
    @Query('offset') offset?: string
  ) {
    const orgId = req.user.org_id;
    return this.agentsService.findActivities(
      agentId,
      orgId,
      limit ? parseInt(limit) : 100,
      offset ? parseInt(offset) : 0
    );
  }
}
