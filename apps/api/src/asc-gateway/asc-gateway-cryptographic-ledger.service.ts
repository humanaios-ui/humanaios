import { Injectable } from '@nestjs/common';
import * as crypto from 'crypto';

/**
 * Cryptographic Ledger Service (Task 2.4)
 * Append-only, hash-chained audit trail for compliance
 *
 * Implements immutable ledger per §7A: every audit event is cryptographically signed.
 * Chain verification ensures tamper-detection.
 */

export interface LedgerEntry {
  entryId: string; // UUID
  sequenceNumber: number; // Immutable counter
  timestamp: Date;
  eventHash: string; // SHA256 of the event
  previousHash: string; // Link to prior entry (chain)
  data: {
    eventType: string;
    deploymentId: string;
    severity: string;
    [key: string]: unknown;
  };
  signature: string; // HMAC signature of this entry
}

export interface LedgerVerification {
  isValid: boolean;
  integrityViolations: string[];
  chainBroken: boolean;
  lastValidEntry?: number;
}

@Injectable()
export class AscGatewayCryptographicLedgerService {
  private ledger: LedgerEntry[] = [];
  private signingKey: string; // In production, load from secure store
  private lastHash: string = '';
  private entryCounter: number = 0;

  constructor() {
    // In production: load from environment/vault
    this.signingKey = process.env.LEDGER_SIGNING_KEY || 'default-key-change-in-production';
  }

  /**
   * Append an event to the cryptographic ledger.
   * Returns immutable ledger entry with chain verification.
   */
  appendEntry(event: {
    eventType: string;
    deploymentId: string;
    severity: string;
    [key: string]: unknown;
  }): LedgerEntry {
    const entryId = this.generateUUID();
    const timestamp = new Date();
    const sequenceNumber = ++this.entryCounter;

    // Hash the event data
    const eventHash = this.hashData(JSON.stringify(event));

    // Link to previous entry (chain)
    const previousHash = this.lastHash;

    // Construct the entry
    const entry: Omit<LedgerEntry, 'signature'> = {
      entryId,
      sequenceNumber,
      timestamp,
      eventHash,
      previousHash,
      data: event,
    };

    // Sign the entry
    const signature = this.signEntry(entry);

    const ledgerEntry: LedgerEntry = { ...entry, signature };

    // Append to ledger
    this.ledger.push(ledgerEntry);
    this.lastHash = this.hashEntry(ledgerEntry);

    return ledgerEntry;
  }

  /**
   * Retrieve a ledger entry by ID or sequence number.
   */
  getEntry(entryIdOrSequence: string | number): LedgerEntry | undefined {
    if (typeof entryIdOrSequence === 'number') {
      return this.ledger.find(e => e.sequenceNumber === entryIdOrSequence);
    }
    return this.ledger.find(e => e.entryId === entryIdOrSequence);
  }

  /**
   * Get all ledger entries (for compliance export).
   */
  getAllEntries(): LedgerEntry[] {
    return [...this.ledger]; // Return copy to prevent mutation
  }

  /**
   * Verify cryptographic integrity of the entire ledger.
   */
  verifyLedgerIntegrity(): LedgerVerification {
    const violations: string[] = [];
    let chainBroken = false;
    let lastValidEntry: number | undefined;

    for (let i = 0; i < this.ledger.length; i++) {
      const entry = this.ledger[i];

      // 1. Verify sequence number
      if (entry.sequenceNumber !== i + 1) {
        violations.push(`Entry ${i}: sequence number mismatch (expected ${i + 1}, got ${entry.sequenceNumber})`);
      }

      // 2. Verify signature
      const expectedSignature = this.signEntry({
        entryId: entry.entryId,
        sequenceNumber: entry.sequenceNumber,
        timestamp: entry.timestamp,
        eventHash: entry.eventHash,
        previousHash: entry.previousHash,
        data: entry.data,
      });

      if (entry.signature !== expectedSignature) {
        violations.push(`Entry ${i}: signature verification failed`);
      }

      // 3. Verify chain link
      if (i === 0) {
        // First entry should link to empty hash
        if (entry.previousHash !== '') {
          violations.push(`Entry 0: previousHash should be empty (got ${entry.previousHash})`);
        }
      } else {
        // Verify link to previous entry
        const previousEntry = this.ledger[i - 1];
        const expectedPreviousHash = this.hashEntry(previousEntry);

        if (entry.previousHash !== expectedPreviousHash) {
          violations.push(`Entry ${i}: chain link broken (previousHash mismatch)`);
          chainBroken = true;
        }
      }

      if (violations.length === 0) {
        lastValidEntry = i + 1;
      }
    }

    return {
      isValid: violations.length === 0,
      integrityViolations: violations,
      chainBroken,
      lastValidEntry,
    };
  }

  /**
   * Export ledger for compliance (e.g., regulatory audits).
   */
  exportForCompliance(deploymentId?: string): {
    exportedAt: Date;
    entryCount: number;
    ledgerHash: string;
    verification: LedgerVerification;
    entries: LedgerEntry[];
  } {
    let entries = this.ledger;

    if (deploymentId) {
      entries = entries.filter(e => e.data.deploymentId === deploymentId);
    }

    return {
      exportedAt: new Date(),
      entryCount: entries.length,
      ledgerHash: this.hashData(JSON.stringify(entries)),
      verification: this.verifyLedgerIntegrity(),
      entries,
    };
  }

  /**
   * Private: Generate UUID for ledger entry.
   */
  private generateUUID(): string {
    return crypto.randomUUID();
  }

  /**
   * Private: Hash event data using SHA256.
   */
  private hashData(data: string): string {
    return crypto.createHash('sha256').update(data).digest('hex');
  }

  /**
   * Private: Hash a ledger entry (for chain verification).
   */
  private hashEntry(entry: Omit<LedgerEntry, 'signature'>): string {
    const data = JSON.stringify({
      entryId: entry.entryId,
      sequenceNumber: entry.sequenceNumber,
      timestamp: entry.timestamp,
      eventHash: entry.eventHash,
      previousHash: entry.previousHash,
    });
    return this.hashData(data);
  }

  /**
   * Private: Sign a ledger entry using HMAC.
   */
  private signEntry(entry: Omit<LedgerEntry, 'signature'>): string {
    const data = JSON.stringify({
      entryId: entry.entryId,
      sequenceNumber: entry.sequenceNumber,
      timestamp: entry.timestamp,
      eventHash: entry.eventHash,
      previousHash: entry.previousHash,
      data: entry.data,
    });

    return crypto
      .createHmac('sha256', this.signingKey)
      .update(data)
      .digest('hex');
  }
}
