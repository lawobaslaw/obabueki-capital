# ADR 0001

## Decision

Use UUID primary keys.

## Status

Accepted

## Reason

UUIDs are globally unique, API-friendly, and suitable for distributed systems. They avoid exposing sequential IDs and provide flexibility if the application evolves into a multi-user SaaS platform.