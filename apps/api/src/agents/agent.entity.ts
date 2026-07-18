/**
 * HumanAIOS - The Operating System for Human-AI Workflows
 * Copyright (c) 2026 HumanAIOS
 * All rights reserved.
 */

export interface Agent {
  id: string;
  org_id: string;
  name: string;
  type: 'mcp' | 'langchain' | 'crewai' | 'custom';
  description?: string;
  metadata?: Record<string, any>;
  status: 'active' | 'inactive' | 'error';
  last_activity_at?: Date;
  created_at: Date;
  updated_at: Date;
}

export interface AgentActivity {
  id: string;
  agent_id: string;
  activity_type: 'tool_call' | 'completion' | 'error' | 'custom';
  description: string;
  input_data?: Record<string, any>;
  output_data?: Record<string, any>;
  duration_ms?: number;
  tokens_used?: number;
  cost_usd?: number;
  error_message?: string;
  metadata?: Record<string, any>;
  created_at: Date;
}

export interface CreateAgentDto {
  name: string;
  type: 'mcp' | 'langchain' | 'crewai' | 'custom';
  description?: string;
  metadata?: Record<string, any>;
}

export interface CreateActivityDto {
  activity_type: 'tool_call' | 'completion' | 'error' | 'custom';
  description: string;
  input_data?: Record<string, any>;
  output_data?: Record<string, any>;
  duration_ms?: number;
  tokens_used?: number;
  cost_usd?: number;
  error_message?: string;
  metadata?: Record<string, any>;
}
