/**
 * HumanAIOS - The Operating System for Human-AI Workflows
 * Copyright (c) 2026 HumanAIOS
 * All rights reserved.
 */

import { Injectable, Inject, NotFoundException, BadRequestException } from '@nestjs/common';
import { Pool } from 'pg';
import { v4 as uuidv4 } from 'uuid';
import { Agent, AgentActivity, CreateAgentDto, CreateActivityDto } from './agent.entity';

@Injectable()
export class AgentsService {
  constructor(@Inject('DATABASE_POOL') private pool: Pool) {}

  async createAgent(orgId: string, createAgentDto: CreateAgentDto): Promise<Agent> {
    const { name, type, description, metadata } = createAgentDto;
    
    const query = `
      INSERT INTO agents (id, org_id, name, type, description, metadata, status, created_at, updated_at)
      VALUES ($1, $2, $3, $4, $5, $6, $7, NOW(), NOW())
      RETURNING *
    `;
    
    const values = [
      uuidv4(),
      orgId,
      name,
      type,
      description || null,
      metadata ? JSON.stringify(metadata) : null,
      'active'
    ];

    try {
      const result = await this.pool.query(query, values);
      return this.mapAgent(result.rows[0]);
    } catch (error) {
      throw new BadRequestException(`Failed to create agent: ${error.message}`);
    }
  }

  async findAllByOrg(orgId: string): Promise<Agent[]> {
    const query = `
      SELECT * FROM agents 
      WHERE org_id = $1 
      ORDER BY created_at DESC
    `;
    
    const result = await this.pool.query(query, [orgId]);
    return result.rows.map(row => this.mapAgent(row));
  }

  async findOne(agentId: string, orgId: string): Promise<Agent> {
    const query = `
      SELECT * FROM agents 
      WHERE id = $1 AND org_id = $2
    `;
    
    const result = await this.pool.query(query, [agentId, orgId]);
    
    if (result.rows.length === 0) {
      throw new NotFoundException(`Agent with ID ${agentId} not found`);
    }
    
    return this.mapAgent(result.rows[0]);
  }

  async createActivity(agentId: string, orgId: string, createActivityDto: CreateActivityDto): Promise<AgentActivity> {
    // First verify agent exists and belongs to org
    await this.findOne(agentId, orgId);

    const {
      activity_type,
      description,
      input_data,
      output_data,
      duration_ms,
      tokens_used,
      cost_usd,
      error_message,
      metadata
    } = createActivityDto;

    const query = `
      INSERT INTO agent_activities (
        id, agent_id, activity_type, description, input_data, output_data,
        duration_ms, tokens_used, cost_usd, error_message, metadata, created_at
      )
      VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, NOW())
      RETURNING *
    `;

    const values = [
      uuidv4(),
      agentId,
      activity_type,
      description,
      input_data ? JSON.stringify(input_data) : null,
      output_data ? JSON.stringify(output_data) : null,
      duration_ms || null,
      tokens_used || null,
      cost_usd || null,
      error_message || null,
      metadata ? JSON.stringify(metadata) : null
    ];

    try {
      const result = await this.pool.query(query, values);
      
      // Update agent's last_activity_at
      await this.pool.query(
        'UPDATE agents SET last_activity_at = NOW(), updated_at = NOW() WHERE id = $1',
        [agentId]
      );
      
      return this.mapActivity(result.rows[0]);
    } catch (error) {
      throw new BadRequestException(`Failed to create activity: ${error.message}`);
    }
  }

  async findActivities(
    agentId: string, 
    orgId: string,
    limit: number = 100,
    offset: number = 0
  ): Promise<AgentActivity[]> {
    // Verify agent exists and belongs to org
    await this.findOne(agentId, orgId);

    const query = `
      SELECT * FROM agent_activities 
      WHERE agent_id = $1 
      ORDER BY created_at DESC
      LIMIT $2 OFFSET $3
    `;

    const result = await this.pool.query(query, [agentId, limit, offset]);
    return result.rows.map(row => this.mapActivity(row));
  }

  private mapAgent(row: any): Agent {
    return {
      id: row.id,
      org_id: row.org_id,
      name: row.name,
      type: row.type,
      description: row.description,
      metadata: row.metadata,
      status: row.status,
      last_activity_at: row.last_activity_at,
      created_at: row.created_at,
      updated_at: row.updated_at
    };
  }

  private mapActivity(row: any): AgentActivity {
    return {
      id: row.id,
      agent_id: row.agent_id,
      activity_type: row.activity_type,
      description: row.description,
      input_data: row.input_data,
      output_data: row.output_data,
      duration_ms: row.duration_ms,
      tokens_used: row.tokens_used,
      cost_usd: row.cost_usd ? parseFloat(row.cost_usd) : null,
      error_message: row.error_message,
      metadata: row.metadata,
      created_at: row.created_at
    };
  }
}
