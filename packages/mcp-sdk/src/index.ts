/**
 * HumanAIOS MCP SDK
 * Connect AI agents to human workers via Model Context Protocol
 */

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

export class HumanAIOSClient {
  private apiKey: string;
  private baseUrl: string;

  constructor(config: { apiKey: string; baseUrl?: string }) {
    this.apiKey = config.apiKey;
    this.baseUrl = config.baseUrl || 'https://api.humanaios.com';
  }

  /**
   * Create a task that requires human assistance
   */
  async createTask(task: Omit<HumanTask, 'id' | 'status' | 'createdAt'>): Promise<HumanTask> {
    // TODO: Implement API call
    throw new Error('Not implemented - connect to HumanAIOS API');
  }

  /**
   * Get task status
   */
  async getTask(taskId: string): Promise<HumanTask> {
    // TODO: Implement API call
    throw new Error('Not implemented');
  }

  /**
   * Find available workers for a task
   */
  async findWorkers(criteria: {
    skills?: string[];
    location?: { lat: number; lng: number; radius: number };
    minRating?: number;
  }): Promise<HumanWorker[]> {
    // TODO: Implement API call
    throw new Error('Not implemented');
  }

  /**
   * Assign task to a worker
   */
  async assignTask(taskId: string, workerId: string): Promise<HumanTask> {
    // TODO: Implement API call
    throw new Error('Not implemented');
  }

  /**
   * Get task result when completed
   */
  async getTaskResult(taskId: string): Promise<TaskResult> {
    // TODO: Implement API call
    throw new Error('Not implemented');
  }
}

export default HumanAIOSClient;
