/**
 * ACAT System Communication Client
 * Calls external AI systems (HTTP APIs, local models, MCP)
 */

import { Injectable, Logger, BadRequestException } from '@nestjs/common';
import axios, { AxiosInstance, AxiosError } from 'axios';

interface SystemConfig {
  type: 'http-api' | 'local-model' | 'mcp';
  endpoint?: string;
  model?: string;
  api_key?: string;
  timeout_ms?: number;
}

interface SystemResponse {
  text: string;
  model: string;
  duration_ms: number;
  tokens_used?: number;
}

@Injectable()
export class ACATSystemClient {
  private readonly logger = new Logger(ACATSystemClient.name);
  private httpClient: AxiosInstance;

  constructor() {
    this.httpClient = axios.create({
      timeout: 30000,
      headers: {
        'User-Agent': 'HumanAIOS ACAT/5.0',
      },
    });
  }

  /**
   * Send prompt to AI system, get response
   * Supports HTTP APIs (OpenAI, Anthropic, etc.)
   */
  async callSystem(config: SystemConfig, prompt: string): Promise<SystemResponse> {
    const startTime = Date.now();

    try {
      if (config.type === 'http-api') {
        return await this.callHTTPAPI(config, prompt);
      } else if (config.type === 'local-model') {
        return await this.callLocalModel(config, prompt);
      } else if (config.type === 'mcp') {
        return await this.callMCP(config, prompt);
      } else {
        throw new BadRequestException(`Unknown system type: ${config.type}`);
      }
    } catch (error) {
      this.logger.error(
        `System call failed [${config.model || config.endpoint}]: ${error.message}`
      );
      throw error;
    }
  }

  /**
   * Call HTTP-based API (OpenAI, Anthropic, generic)
   */
  private async callHTTPAPI(config: SystemConfig, prompt: string): Promise<SystemResponse> {
    const startTime = Date.now();

    // Detect provider from endpoint
    const provider = this.detectProvider(config.endpoint);

    let response;

    if (provider === 'openai') {
      response = await this.callOpenAI(config, prompt);
    } else if (provider === 'anthropic') {
      response = await this.callAnthropicAPI(config, prompt);
    } else {
      // Generic HTTP endpoint
      response = await this.httpClient.post(config.endpoint, {
        prompt,
        model: config.model,
      });
    }

    const text = this.extractTextFromResponse(response.data, provider);

    return {
      text,
      model: config.model || 'unknown',
      duration_ms: Date.now() - startTime,
      tokens_used: response.data.usage?.total_tokens,
    };
  }

  /**
   * Call OpenAI API (GPT-4, GPT-3.5, etc.)
   */
  private async callOpenAI(config: SystemConfig, prompt: string): Promise<any> {
    return this.httpClient.post(config.endpoint || 'https://api.openai.com/v1/chat/completions', {
      model: config.model || 'gpt-4',
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.7,
      max_tokens: 2000,
    });
  }

  /**
   * Call Anthropic API (Claude)
   */
  private async callAnthropicAPI(config: SystemConfig, prompt: string): Promise<any> {
    return this.httpClient.post(
      config.endpoint || 'https://api.anthropic.com/v1/messages',
      {
        model: config.model || 'claude-3-sonnet-20240229',
        max_tokens: 2000,
        messages: [{ role: 'user', content: prompt }],
      },
      {
        headers: {
          'x-api-key': config.api_key || process.env.ANTHROPIC_API_KEY,
        },
      }
    );
  }

  /**
   * Call local model (Ollama, LM Studio, etc.)
   */
  private async callLocalModel(config: SystemConfig, prompt: string): Promise<SystemResponse> {
    const startTime = Date.now();

    const response = await this.httpClient.post(config.endpoint || 'http://localhost:11434/api/generate', {
      model: config.model,
      prompt,
      stream: false,
    });

    return {
      text: response.data.response,
      model: config.model,
      duration_ms: Date.now() - startTime,
    };
  }

  /**
   * Call MCP (Model Context Protocol) server
   */
  private async callMCP(config: SystemConfig, prompt: string): Promise<SystemResponse> {
    // MCP integration placeholder
    // Real implementation depends on MCP server setup
    throw new BadRequestException('MCP integration not yet implemented');
  }

  /**
   * Detect provider from endpoint URL
   */
  private detectProvider(endpoint: string): string {
    if (!endpoint) return 'generic';

    try {
      const host = new URL(endpoint).hostname.toLowerCase();

      if (host === 'openai.com' || host.endsWith('.openai.com')) return 'openai';
      if (host === 'anthropic.com' || host.endsWith('.anthropic.com')) return 'anthropic';
      if (host === 'localhost' || host === '127.0.0.1') return 'local';
    } catch {
      return 'generic';
    }

    return 'generic';
  }

  /**
   * Extract text from provider-specific response format
   */
  private extractTextFromResponse(data: any, provider: string): string {
    if (provider === 'openai') {
      return data.choices?.[0]?.message?.content || '';
    } else if (provider === 'anthropic') {
      return data.content?.[0]?.text || '';
    } else if (provider === 'local') {
      return data.response || '';
    }
    // Generic: assume 'text' or 'content' field
    return data.text || data.content || JSON.stringify(data);
  }
}
