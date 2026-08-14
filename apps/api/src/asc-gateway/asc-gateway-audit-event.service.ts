import { Injectable } from '@nestjs/common';
import { EventEmitter } from 'events';

/**
 * Audit Event Service — Event Streaming Pipeline
 * Manages real-time event emission for ASC_GATEWAY audit events
 *
 * Events stream from measurement engine → repository → subscribers (webhooks, dashboards, etc.)
 */

export type AuditEventType =
  | 'probeResultRecorded'
  | 'measurementWindowCompleted'
  | 'thresholdBreach'
  | 'degradationDetected'
  | 'deploymentRegistered'
  | 'infrastructureChanged'
  | 'notificationSent'
  | 'auditLogQueried';

export interface AuditEvent {
  eventType: AuditEventType;
  deploymentId: string;
  timestamp: Date;
  severity: 'info' | 'warn' | 'error';
  data: Record<string, unknown>;
  correlationId?: string; // For tracing across events
}

export interface EventSubscriber {
  id: string;
  eventType: AuditEventType | '*'; // '*' = subscribe to all
  handler: (event: AuditEvent) => Promise<void>;
  retryPolicy?: {
    maxRetries: number;
    backoffMs: number;
  };
}

@Injectable()
export class AscGatewayAuditEventService {
  private eventEmitter: EventEmitter;
  private subscribers: Map<string, EventSubscriber> = new Map();
  private eventLog: AuditEvent[] = [];
  private readonly MAX_LOG_SIZE = 10000; // Prevent unbounded memory growth

  constructor() {
    this.eventEmitter = new EventEmitter();
    this.eventEmitter.setMaxListeners(100); // Allow many subscribers
  }

  /**
   * Emit an audit event into the pipeline.
   * Events flow: measurement engine → this service → subscribers/webhooks/logs.
   */
  async emitEvent(event: AuditEvent): Promise<void> {
    // Ensure timestamp
    if (!event.timestamp) {
      event.timestamp = new Date();
    }

    // Log to in-memory event log (circular buffer)
    this.eventLog.push(event);
    if (this.eventLog.length > this.MAX_LOG_SIZE) {
      this.eventLog.shift(); // Remove oldest
    }

    // Emit to local subscribers (in-process)
    this.eventEmitter.emit(event.eventType, event);
    this.eventEmitter.emit('*', event); // Wildcard subscribers

    // Dispatch to external subscribers (webhooks, queues, etc.)
    await this.dispatchToSubscribers(event);
  }

  /**
   * Register a real-time event subscriber.
   */
  subscribe(subscriber: EventSubscriber): void {
    this.subscribers.set(subscriber.id, subscriber);

    // Attach handler to emitter
    const handler = async (event: AuditEvent) => {
      if (subscriber.eventType === '*' || subscriber.eventType === event.eventType) {
        await this.executeWithRetry(subscriber, event);
      }
    };

    this.eventEmitter.on(subscriber.eventType === '*' ? '*' : subscriber.eventType, handler);
  }

  /**
   * Unsubscribe from events.
   */
  unsubscribe(subscriberId: string): void {
    this.subscribers.delete(subscriberId);
  }

  /**
   * Get event stream for a deployment (query audit log).
   */
  getEventStream(deploymentId: string, eventType?: AuditEventType, limit: number = 100): AuditEvent[] {
    let events = this.eventLog.filter(e => e.deploymentId === deploymentId);

    if (eventType) {
      events = events.filter(e => e.eventType === eventType);
    }

    return events.slice(-limit); // Return last N
  }

  /**
   * Get event statistics for a deployment.
   */
  getEventStats(deploymentId: string): {
    totalEvents: number;
    eventsByType: Record<AuditEventType, number>;
    lastEventTime?: Date;
  } {
    const events = this.eventLog.filter(e => e.deploymentId === deploymentId);

    const stats: Record<AuditEventType, number> = {
      probeResultRecorded: 0,
      measurementWindowCompleted: 0,
      thresholdBreach: 0,
      degradationDetected: 0,
      deploymentRegistered: 0,
      infrastructureChanged: 0,
      notificationSent: 0,
      auditLogQueried: 0,
    };

    for (const event of events) {
      stats[event.eventType]++;
    }

    return {
      totalEvents: events.length,
      eventsByType: stats,
      lastEventTime: events[events.length - 1]?.timestamp,
    };
  }

  /**
   * Clear event log for a deployment (for testing/reset).
   */
  clearEventLog(deploymentId: string): number {
    const initialLength = this.eventLog.length;
    this.eventLog = this.eventLog.filter(e => e.deploymentId !== deploymentId);
    return initialLength - this.eventLog.length;
  }

  /**
   * Private: dispatch to external subscribers with retry logic.
   */
  private async dispatchToSubscribers(event: AuditEvent): Promise<void> {
    const promises: Promise<void>[] = [];

    for (const subscriber of this.subscribers.values()) {
      if (subscriber.eventType === '*' || subscriber.eventType === event.eventType) {
        promises.push(this.executeWithRetry(subscriber, event));
      }
    }

    // Fire and forget (non-blocking)
    Promise.all(promises).catch(err => {
      console.error('Subscriber dispatch error:', err);
    });
  }

  /**
   * Private: execute subscriber handler with retry logic.
   */
  private async executeWithRetry(
    subscriber: EventSubscriber,
    event: AuditEvent,
    attempt: number = 0
  ): Promise<void> {
    const maxRetries = subscriber.retryPolicy?.maxRetries ?? 3;
    const backoffMs = subscriber.retryPolicy?.backoffMs ?? 1000;

    try {
      await subscriber.handler(event);
    } catch (error) {
      if (attempt < maxRetries) {
        const delay = backoffMs * Math.pow(2, attempt); // Exponential backoff
        setTimeout(() => {
          this.executeWithRetry(subscriber, event, attempt + 1);
        }, delay);
      } else {
        console.error(
          `Subscriber ${subscriber.id} failed after ${maxRetries} retries:`,
          error
        );
      }
    }
  }
}
