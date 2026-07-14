# 0002. Domain Model Hierarchy

* Status: Proposed
* Date: 2026-07-13

## Context and Problem Statement
We need to establish a consistent hierarchy for our core domain entities (`User`, `Portfolio`, `Account`) so the system naturally reflects real-world financial ownership and grouping. 

## Decision
We have organized the application's domain model in a strict hierarchical structure:
`User` $\downarrow$ `Portfolio` $\downarrow$ `Account`

This nested relationship models ownership and containment as follows:
- **Users** can own multiple **portfolios**.
- **Portfolios** can contain multiple **accounts**.
- **Accounts** hold **assets** (which will be introduced in a future domain layer).

## Rationale
This structural organization provides several key benefits:
1. **Logical Segregation**: By placing Portfolios below Users, users with diverse financial goals or strategies can easily separate their investments.
2. **Granular Grouping**: Grouping Accounts under Portfolios allows for distinct financial reporting, performance tracking, and boundary enforcement at the portfolio level.
3. **Foundation for Asset Management**: Anchoring assets at the `Account` level maps perfectly to standard real-world banking and brokerage models, making it easier to integrate with third-party financial data providers.

## Consequences

### Positive
- A clear, unidirectional data flow that simplifies querying and permissions (e.g., fetching all assets belonging to a specific user or portfolio).
- The domain model is highly intuitive and scalable for adding future features like reporting or aggregated metrics.

### Negative
- Deeper entity hierarchies require more complex navigation when performing cross-cutting operations (e.g., retrieving all assets across *all* accounts for a user). 
- Operations mutating deeply nested entities will require strict transaction boundaries to ensure data consistency.