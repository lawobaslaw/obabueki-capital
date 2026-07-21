# ADR-0002

## Title

Transactions are the Source of Truth

## Status

Accepted

## Context

Investment holdings can either be stored directly or calculated from
historical transactions.

## Decision

Transactions are the only persisted financial records.

Holdings will always be calculated dynamically.

## Consequences

- No synchronization issues
- Complete audit trail
- Easier recalculation
- Supports future analytics
