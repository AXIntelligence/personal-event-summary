# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal Event Summary is a system for capturing, processing, and summarizing personal events and activities. The project is in early development stage and focuses on building a robust event processing pipeline with comprehensive validation and testing.

## Development Workflow

### Planning & Design

```bash
# Create a new plan for a feature or task
/plan [description of what you want to build]

# Explore the codebase to understand current state
/explore

# Focus exploration on specific areas
/explore event processing and data models
```

### Implementation

```bash
# Implement a plan using TDD methodology
/implement ./plans/001-feature-name.md

# Run tests
pytest -v                                    # Run all tests
pytest --cov=src --cov-report=term-missing  # With coverage
```

## Architecture Summary

*To be defined as the project evolves*

### System Overview

The system will handle:
- Event capture from various sources
- Event processing and transformation
- Event aggregation and summarization
- Data persistence and retrieval

### File Structure

```
personal-event-summary/
├── src/                  # Source code
├── tests/                # Test files
├── plans/                # Implementation plans
├── analysis/             # Validation reports and research
├── requirements/         # Project requirements
├── .claude/              # Claude-specific configuration
│   └── commands/         # Custom Claude commands
└── docs/                 # Documentation
```

## Critical Lessons Learned

*This section will be updated as the project evolves*

## Development Standards

### Test-Driven Development (TDD)

1. **Write tests first** - All new code must have tests written before implementation
2. **Red-Green-Refactor** cycle:
   - Red: Write failing tests
   - Green: Write minimal code to pass
   - Refactor: Improve code quality

### Quality Metrics

- **Test Coverage**: Minimum 70% (target 80%)
- **Documentation**: All public interfaces documented
- **Validation**: All features empirically validated

### Planning Standards

- Use hypothesis-driven approach
- Define measurable success criteria
- Include empirical validation methods
- No human time estimates

### Documentation Requirements

- Update CLAUDE.md with lessons learned
- Create validation reports in `./analysis/`
- Keep plans/README.md index current
- Document architectural decisions

## Quick Troubleshooting

### Common Issues

**"Tests failing after changes"**
```bash
# Clear Python cache if using Python
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
pip install -e .  # Reinstall package
```

**"Need to understand current implementation"**
```bash
/explore  # Run exploration command
```

**"Want to add a new feature"**
```bash
/plan [feature description]  # Create plan first
# Review plan
/implement ./plans/NNN-feature.md  # Then implement
```

## Data Models

*To be defined based on requirements*

## Environment Configuration

**Required (.env):**
```bash
# Add environment variables as needed
```

## Security Considerations

- Input validation for all external data
- Secure storage of sensitive information
- Path traversal prevention
- API key protection

## Performance Guidelines

*To be defined based on requirements*

## Important Notes

### When Creating Plans
- Always validate assumptions empirically
- Store analysis artifacts in `./analysis/`
- Never include human time estimates
- Define clear success criteria

### When Implementing
- Follow TDD strictly
- Seek confirmation between phases
- Validate all outcomes empirically
- Update documentation

### When Exploring
- Validate claims with code inspection
- Note discrepancies between docs and reality
- Store findings in analysis directory

---

**Last Updated**: 2025-11-05
**Project Status**: Initial Setup
**Documentation Version**: 1.0