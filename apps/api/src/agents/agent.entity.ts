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
  status: 'active' | 'inactive' | 'error';
  metadata?: Record<string, any>;
  created_at: Date;
  updated_at: Date;
  last_active_at?: Date;
}

export interface CreateAgentDto {
  name: string;
  type: 'mcp' | 'langchain' | 'crewai' | 'custom';
  description?: string;
  metadata?: Record<string, any>;
}

export interface UpdateAgentDto {
  name?: string;
  description?: string;
  status?: 'active' | 'inactive' | 'error';
  metadata?: Record<string, any>;
}

export interface AgentActivity {
  id: string;
  agent_id: string;
  org_id: string;
  activity_type: 'tool_call' | 'llm_request' | 'task_complete' | 'error' | 'custom';
  description: string;
  input_data?: Record<string, any>;
  output_data?: Record<string, any>;
  tokens_used?: number;
  cost_usd?: number;
  duration_ms?: number;
  status: 'success' | 'failed' | 'pending';
  error_message?: string;
  metadata?: Record<string, any>;
  created_at: Date;
}

export interface CreateActivityDto {
  activity_type: 'tool_call' | 'llm_request' | 'task_complete' | 'error' | 'custom';
  description: string;
  input_data?: Record<string, any>;
  output_data?: Record<string, any>;
  tokens_used?: number;
  cost_usd?: number;
  duration_ms?: number;
  status?: 'success' | 'failed' | 'pending';
  error_message?: string;
  metadata?: Record<string, any>;
}
