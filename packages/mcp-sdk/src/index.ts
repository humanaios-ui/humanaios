/**
 * HumanAIOS MCP SDK
 * Connect AI agents to human workers via Model Context Protocol
 */

import { APIClient, APIError } from './api-client';

export { APIError };

export interface HumanTask {
  id: string;
  agentId: string;
  title: string;
  description: string;
  skillsRequired: string[];
  estimatedDuration?: number;
  budget?: number;
  location?: {
    lat: number;
    lng: number;
    address?: string;
  };
  status: 'pending' | 'assigned' | 'in_progress' | 'completed' | 'failed';
  createdAt: Date;
  completedAt?: Date;
}

export interface HumanWorker {
  id: string;
  name: string;
  skills: string[];
  location?: {
    lat: number;
    lng: number;
  };
  availability: 'available' | 'busy' | 'offline';
  rating?: number;
  hourlyRate?: number;
}

export interface TaskResult {
  taskId: string;
  workerId: string;
  status: 'completed' | 'failed';
  result?: any;
  evidence?: {
    photos?: string[];
    notes?: string;
    timestamp: Date;
  };
  cost?: number;
}

export interface Agent {
  id: string;
  name: string;
  type: string;
  description?: string;
  status: string;
  created_at: string;
}

export interface Activity {
  id: string;
  agent_id: string;
  activity_type: string;
  description?: string;
  metadata?: any;
  created_at: string;
}

export interface HumanAIOSConfig {
  apiKey?: string;
  baseUrl?: string;
  timeout?: number;
}

export class HumanAIOSClient {
  private client: APIClient;
  private userId: string = 'sdk-user'; // Will be from auth token later

  constructor(config: HumanAIOSConfig = {}) {
    this.client = new APIClient({
      baseUrl: config.baseUrl || 'http://localhost:3001/api/v1',
      apiKey: config.apiKey,
      timeout: config.timeout,
    });
  }

  /**
   * AGENT MANAGEMENT
   */

  /**
   * Create a new AI agent
   */
  async createAgent(agent: {
    name: string;
    type: string;
    description?: string;
  }): Promise<Agent> {
    return this.client.post<Agent>('/agents', {
      ...agent,
      user_id: this.userId,
    });
  }

  /**
   * Get all agents
   */
  async getAgents(): Promise<Agent[]> {
    return this.client.get<Agent[]>('/agents');
  }

  /**
   * Get a specific agent by ID
   */
  async getAgent(agentId: string): Promise<Agent> {
    return this.client.get<Agent>(`/agents/${agentId}`);
  }

  /**
   * ACTIVITY LOGGING
   */

  /**
   * Log an activity for an agent
   */
  async logActivity(
    agentId: string,
    activity: {
      activity_type: string;
      description?: string;
      metadata?: any;
    }
  ): Promise<Activity> {
    return this.client.post<Activity>(
      `/agents/${agentId}/activities`,
      activity
    );
  }

  /**
   * Get activities for an agent
   */
  async getActivities(
    agentId: string,
    options: {
      limit?: number;
      offset?: number;
    } = {}
  ): Promise<Activity[]> {
    const params = new URLSearchParams();
    if (options.limit) params.set('limit', options.limit.toString());
    if (options.offset) params.set('offset', options.offset.toString());
    
    const query = params.toString();
    const path = `/agents/${agentId}/activities${query ? '?' + query : ''}`;
    
    return this.client.get<Activity[]>(path);
  }

  /**
   * HUMAN TASK MANAGEMENT (Future - RentAHuman Integration)
   */

  /**
   * Create a task that requires human assistance
   */
  async createTask(task: Omit<HumanTask, 'id' | 'status' | 'createdAt'>): Promise<HumanTask> {
    // TODO: Implement when RentAHuman integration is ready
    throw new Error('Task creation via RentAHuman not yet implemented');
  }

  /**
   * Get task status
   */
  async getTask(taskId: string): Promise<HumanTask> {
    // TODO: Implement when RentAHuman integration is ready
    throw new Error('Task retrieval not yet implemented');
  }

  /**
   * Find available workers for a task
   */
  async findWorkers(criteria: {
    skills?: string[];
    location?: { lat: number; lng: number; radius: number };
    minRating?: number;
  }): Promise<HumanWorker[]> {
    // TODO: Implement when RentAHuman integration is ready
    throw new Error('Worker search not yet implemented');
  }

  /**
   * Assign task to a worker
   */
  async assignTask(taskId: string, workerId: string): Promise<HumanTask> {
    // TODO: Implement when RentAHuman integration is ready
    throw new Error('Task assignment not yet implemented');
  }

  /**
   * Get task result when completed
   */
  async getTaskResult(taskId: string): Promise<TaskResult> {
    // TODO: Implement when RentAHuman integration is ready
    throw new Error('Task result retrieval not yet implemented');
  }
}

export default HumanAIOSClient;
