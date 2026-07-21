# ADR-0003

## Title

Holdings are Calculated

## Status

Accepted

## Context

The application needs to display current investment positions.

## Decision

No holdings table will exist.

HoldingService will calculate holdings from transactions.

## Consequences

- Simpler database
- Better consistency
- Read-only calculation engine
