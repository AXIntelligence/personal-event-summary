# Personal Event Summary

A system for capturing, processing, and summarizing personal events and activities.

## Project Status

🚧 **Early Development** - Setting up project infrastructure and development workflow

## Overview

Personal Event Summary aims to provide a comprehensive solution for tracking and analyzing personal events, activities, and patterns over time. The system will capture events from various sources, process them intelligently, and provide meaningful summaries and insights.

## Development Workflow

This project uses a hypothesis-driven development approach with empirical validation:

### 1. Planning
```bash
# Create a new implementation plan
/plan [feature description]
```

### 2. Implementation
```bash
# Implement a plan using TDD
/implement ./plans/001-feature-name.md
```

### 3. Exploration
```bash
# Explore and understand the codebase
/explore
```

## Project Structure

```
personal-event-summary/
├── src/                  # Source code
├── tests/                # Test files
├── plans/                # Implementation plans
│   └── README.md        # Plan index and guidelines
├── analysis/            # Validation reports and research
├── requirements/        # Project requirements
├── .claude/             # Claude Code configuration
│   └── commands/        # Custom commands
├── docs/                # Documentation
└── CLAUDE.md           # Claude Code guidance
```

## Getting Started

*Setup instructions will be added as the project develops*

## Features

*Planned features (to be implemented):*
- Event capture from multiple sources
- Event processing and transformation
- Event aggregation and analysis
- Summary generation
- Data persistence
- Query and retrieval capabilities

## Testing

```bash
# Run tests (once implemented)
pytest -v

# Run with coverage
pytest --cov=src --cov-report=term-missing
```

## Documentation

- [CLAUDE.md](CLAUDE.md) - Development guidance for Claude Code
- [plans/README.md](plans/README.md) - Planning and implementation guide
- [Analysis Reports](analysis/) - Validation and research documents

## Quality Standards

- **Test Coverage**: Minimum 70% (target 80%)
- **TDD**: All code written test-first
- **Validation**: Empirical validation of all features
- **Documentation**: Comprehensive and up-to-date

## Contributing

This project follows a structured development workflow:
1. Create a plan using `/plan`
2. Review and approve the plan
3. Implement using `/implement` with TDD
4. Validate all success criteria
5. Update documentation

## License

*To be determined*

---

**Last Updated**: 2025-11-05
**Version**: 0.0.1 (Initial Setup)