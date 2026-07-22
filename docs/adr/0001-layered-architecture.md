# ADR-0001

## Title

Layered Architecture

## Status

Accepted

## Context

The application requires clear separation between HTTP handling,
business logic and persistence.

## Decision

The project will use:

API
↓

Service

↓

Repository

↓

Model

## Consequences

- Easier testing
- Better maintainability
- Clear separation of concerns
- Simple dependency injection
