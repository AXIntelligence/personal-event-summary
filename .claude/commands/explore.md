---
description: Deep dive into repository architecture, design, workflows, and evolution
---

Explore this repository to understand its architecture, design, and expected workflows.

## Usage

```bash
# Standard exploration (covers all areas)
/explore

# With additional focus areas
/explore data models and event processing
/explore integration patterns and APIs
/explore validation logic and data quality
```

## Standard Exploration Strategy

1. **Architecture & Design**: Pay specific attention to all README.md files
   - IGNORE all contents of ./examples unless explicitly instructed to
   - IGNORE all contents of ./analysis as those are ephemeral

Your goal is to learn about:
   - System architecture
   - Design patterns
   - Expected workflows
   - Component relationships

2. **Project Evolution**: Examine plans in ./plans/* to understand:
   - How the project has evolved over time
   - Implementation decisions and rationale
   - Historical context for current design

3. **Requirements & Goals**: Study ./requirements/* to understand:
   - Project goals
   - Success criteria
   - Feature requirements

4. **Assumption Formation**: As you explore, form assumptions about:
   - System capabilities
   - Design tradeoffs
   - Implementation patterns
   - Quality standards

5. **Validation**: Use subagents to research and validate any assumptions or questions that arise during exploration.
   - CRITICAL: YOU MUST validate assumptions about plan implementation success, don't trust plan status

## Additional Focus Areas

If additional focus areas are specified as arguments to this command, pay extra attention to those specific topics while still covering the standard exploration strategy. Examples of focus areas:

- **Event Processing**: Event capture, transformation, aggregation patterns
- **Data Models**: Schema design, data relationships, storage patterns
- **Testing**: Test coverage, testing patterns, test infrastructure
- **Error Handling**: Error propagation, validation, edge cases
- **Performance**: Optimization strategies, bottlenecks, concurrency
- **Data Flow**: Data transformations, state management, persistence
- **Validation**: Quality checks, validation logic, acceptance criteria
- **Integration**: External dependencies, API interactions, tool integrations
- **Configuration**: Settings, environment variables, feature flags

## Empirical Validation

When exploring:
- Always verify claims with actual code inspection
- Run tests if they exist to validate assumptions
- Check for inconsistencies between documentation and implementation
- Note any gaps in testing or validation

## Output Format

Once exploration is complete, provide a comprehensive summary organized by:

1. **Project Overview**
   - Purpose and goals
   - Current state
   - Key components

2. **Architecture Analysis**
   - System design
   - Data flow
   - Integration points

3. **Implementation Status**
   - Completed features
   - Work in progress
   - Gaps or missing pieces

4. **Quality Assessment**
   - Test coverage
   - Documentation completeness
   - Code quality observations

5. **Recommendations**
   - Next steps
   - Improvement opportunities
   - Risk areas

## Important Notes

- Store detailed exploration findings in `./analysis/exploration-report-[date].md`
- Be empirical - validate all assumptions with evidence
- Focus on understanding the "why" behind design decisions
- Note any discrepancies between documentation and reality

Once exploration is complete, provide a comprehensive summary and wait for further instructions.