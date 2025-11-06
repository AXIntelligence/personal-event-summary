# Plans Directory

This directory contains implementation plans and design documents for the personal-event-summary project.

## Numbering System

Plans are numbered sequentially using a three-digit prefix format: `NNN-descriptive-name.md`

### Format
```
NNN-descriptive-name.md
```

Where:
- `NNN` = Three-digit number (001, 002, 003, etc.)
- `descriptive-name` = Kebab-case description of the plan
- `.md` = Markdown file extension

### Examples
- `001-event-data-model.md` - Data model design for events
- `002-event-processing-pipeline.md` - Event processing implementation
- `003-api-design.md` - API design and implementation

## Creating a New Plan

### Using the /plan Command (Recommended)

```bash
/plan [your requirements or description]
```

The `/plan` command will:
- Automatically determine the next plan number
- Create a comprehensive, hypothesis-driven plan
- Validate assumptions empirically
- Define clear success criteria
- Save the plan to the plans/ directory

See [/.claude/commands/plan.md](../.claude/commands/plan.md) for details.

### Manual Creation

1. **Determine the next number**: Check existing files and increment the highest number
   ```bash
   ls plans/*.md | sort | tail -1
   ```

2. **Create the file**: Use the numbering format
   ```bash
   # If last plan was 001, create 002
   touch plans/002-your-plan-name.md
   ```

3. **Document the plan**: Include the following sections:
   - **Title**: Clear, descriptive title
   - **Status**: Draft, In Progress, Completed, Archived
   - **Date**: Creation date and last updated
   - **Overview**: Brief description of the plan
   - **Goals**: What this plan aims to achieve
   - **Implementation Details**: Technical details
   - **Dependencies**: Related plans or prerequisites
   - **Success Criteria**: Empirically measurable outcomes

## Implementing a Plan

### Using the /implement Command (Recommended)

```bash
/implement ./plans/NNN-plan-name.md [additional-instructions]
```

The `/implement` command will:
- Execute the plan using Test-Driven Development (TDD) methodology
- Validate coverage thresholds
- Seek confirmation before moving between phases
- Run and wait for integration tests to complete
- Validate all success criteria empirically
- Update all documentation upon completion
- Create validation reports in analysis/

See [/.claude/commands/implement.md](../.claude/commands/implement.md) for details.

**Example:**
```bash
/implement ./plans/001-event-data-model.md
```

### Manual Implementation

If implementing manually:
1. Follow the plan phases in order
2. Use TDD: Write tests first, then implementation
3. Run integration tests before marking complete
4. Validate all success criteria empirically
5. Update documentation and plan status

## Plan Lifecycle

### Status Indicators

- **Draft**: Plan is being written and reviewed
- **Approved**: Plan has been reviewed and approved
- **In Progress**: Implementation is underway
- **Completed**: All tasks in the plan are done, all success criteria validated, quality metrics met:
  - ✅ All unit tests passing (100%)
  - ✅ Line coverage ≥70% (target: 80%)
  - ✅ Integration tests successful
  - ✅ Documentation updated
- **Deferred**: Plan has been paused till a later date
- **Abandoned**: Plan was abandoned for reasons
- **Archived**: Plan is historical reference only

### Updating Plans

- Minor updates: Edit the existing file
- Major changes: Consider creating a new plan that references the original
- Add a "Last Updated" timestamp when making significant changes
- Mark plans as "Completed" only after empirical validation of all outcomes

## Referencing Plans

When referencing plans in code comments or documentation:
```python
# Implementation follows plan 001-event-data-model.md
# See plans/002-event-processing-pipeline.md for context
```

## Index of Plans

| Number | Name | Status | Completion Date | Priority | Description |
|--------|------|--------|-----------------|----------|-------------|
| 001 | [GitHub Pages Attendee Summary](001-github-pages-attendee-summary.md) | ✅ Completed | 2025-11-06 | 🔴 Critical | Implement personalized attendee pages on GitHub Pages |
| 002 | [Event Tech Live Sample Data](002-event-tech-live-sample-data.md) | ✅ Completed | 2025-11-06 | 🟡 High | Enhance sample data with Event Tech Live real event insights |

## Status Legend
- ✅ **Completed**: Implementation done, all tests passing
- 🚧 **In Progress**: Currently being implemented
- 📝 **Draft**: Planning phase, not yet started
- 🔄 **In Review**: Completed but pending review/approval
- ⏸️ **Deferred**: Planned but postponed
- 💀 **Abandoned**: Plan has been abandoned
- 📦 **Archived**: Historical reference, no longer active

## Priority Legend
- 🔴 **Critical**: Addresses major issues or core functionality
- 🟡 **High**: Important enhancements with clear value
- 🟢 **Low**: Nice-to-have features, polish, future enhancements

---

## Recent Updates

- **2025-11-06**: Completed Plan 002 - Event Tech Live Sample Data Enhancement
  - Added B2B data model with optional fields (productsExplored, boothsVisited, sponsorInteractions)
  - Created Event Tech Live 2025 event with 30 sessions and 12 attendees
  - Achieved 89.93% test coverage (105 tests passing)
  - Zero breaking changes, full backward compatibility maintained
  - Validation report: [analysis/plan-002-validation-report.md](../analysis/plan-002-validation-report.md)
- **2025-11-06**: Completed Plan 001 - GitHub Pages Attendee Summary System
- **2025-11-06**: Created Plan 002 - Event Tech Live Sample Data Enhancement (Draft)
- **2025-11-05**: Created Plan 001 - GitHub Pages Attendee Summary System (Draft)

---

**Note**: Keep plans up-to-date and mark them with appropriate status as work progresses.