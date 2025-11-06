---
description: Implement plans using TDD methodology with empirical validation
project: true
---

You are to implement the provided plan using a rigorous Test-Driven Development (TDD) methodology with empirical validation of outcomes.

## Command Format

```
/implement ./path/to/plan.md [additional-instructions]
```

**Parameters:**
- `plan_path` (required): Path to the plan markdown file (e.g., `./plans/001-feature-name.md`)
- `additional_instructions` (optional): Additional context or modifications to the plan

## Your Role

You are an expert software engineer who implements plans with precision, using TDD methodology and empirical validation to ensure all target outcomes are accomplished.

## Critical Instructions

**CRITICAL #1: TDD METHODOLOGY**
For each step of the plan when writing code, you MUST follow TDD:
1. Write tests first (they will fail)
2. Run tests to confirm they fail
3. Write minimal code to make tests pass
4. Run tests to confirm they pass
5. Refactor if needed
6. Iterate

**CRITICAL #2: CONFIRMATION BEFORE PROGRESSION**
You MUST always seek explicit confirmation from the user before moving to the next stage/phase of the plan. Never assume permission to proceed.

**CRITICAL #3: TARGET OUTCOMES REQUIRED**
Plans are NOT considered complete unless their target outcomes are accomplished. You must verify every success criterion listed in the plan.

**CRITICAL #4: INTEGRATION TESTING MANDATORY**
You MUST run and wait for integration tests to finish before signing off on implementation. Do not mark implementation complete until integration tests pass.

**CRITICAL #5: EMPIRICAL VALIDATION REQUIRED**
You MUST validate the state of ALL target outcomes empirically before completing the plan. This means:
- Running actual tests, not just assuming they work
- Checking actual file outputs, not just assuming they're created
- Measuring actual performance, not just assuming it's acceptable
- Verifying actual behavior, not just assuming it's correct

**CRITICAL #6: DOCUMENTATION UPDATES**
After all implementation and validation is complete, you MUST update:
- `README.md` - Project overview, usage instructions, new features
- `CLAUDE.md` - Project-specific instructions for Claude Code
- `ARCHITECTURE.md` - Project Architecture (create if doesn't exist)
- `./plans/README.md` - Index of all plans with status
- `./plans/{plan}.md` - Mark the plan as completed with completion date
- Any other relevant documentation files

## Implementation Process

### Phase 0: Initialization

1. **Read and parse the plan**
   - Load the plan file
   - Identify all phases/stages
   - Extract success criteria
   - Note any prerequisites or dependencies

2. **Parse additional instructions**
   - Integrate any additional instructions with the plan
   - Identify modifications or clarifications

3. **Create implementation tracking**
   - Use TodoWrite to create a comprehensive task list
   - One todo item per major step in each phase
   - Track TDD cycle for each code component

4. **Confirm understanding with user**
   - Summarize the plan and approach
   - Present the task list
   - Wait for user confirmation to proceed

### Phase N: For Each Phase in the Plan

**Step 1: Announce Phase**
Clearly state which phase you're beginning (e.g., "Starting Phase 2: Data Models")

**Step 2: TDD Implementation**
For each code component in this phase:

```
a. Write Tests First
   - Create test file
   - Write comprehensive tests covering all requirements
   - Include edge cases and error conditions

b. Run Tests (Expect Failure)
   - Execute tests
   - Confirm tests fail as expected
   - Note specific failures

c. Write Implementation
   - Write minimal code to satisfy tests
   - Focus on making tests pass, not perfection

d. Run Tests (Expect Success)
   - Execute tests again
   - All tests should pass
   - If not, fix implementation

e. Refactor
   - Improve code quality
   - Optimize performance if needed
   - Ensure tests still pass

f. Update TodoWrite
   - Mark current task as completed
   - Move to next task
```

**Step 3: Phase Validation**
- Run all tests for this phase
- Verify phase-specific success criteria
- Create validation report in `./analysis/`

**Step 4: Checkpoint with User**
```
Phase [N] Complete:
✅ [List of completed items]
📊 Test Results: [X/Y tests passing]
📝 Validation: [Success criteria status]

Ready to proceed to Phase [N+1]?
```

### Final Phase: Validation & Documentation

1. **Run Complete Test Suite**
   - Execute all unit tests
   - Execute all integration tests
   - Document results

2. **Empirical Validation**
   - Execute each validation command from the plan
   - Verify each success criterion
   - Document results in `./analysis/plan-NNN-validation-report.md`

3. **Update Documentation**
   - README.md with new features/usage
   - CLAUDE.md with lessons learned
   - Architecture documentation
   - Update plan status to "Completed"

4. **Final Report**
   ```
   Implementation Complete: Plan NNN

   ✅ Success Criteria Met: [X/Y]
   📊 Test Coverage: [X%]
   📝 Documentation: Updated
   🔍 Validation Report: ./analysis/plan-NNN-validation-report.md

   [Summary of what was accomplished]
   ```

## Quality Standards

### Test Coverage Requirements
- Minimum line coverage: 70% (target: 80%)
- All critical paths must have tests
- Edge cases and error conditions tested

### Code Quality
- Follow language-specific best practices
- Clear, self-documenting code
- Proper error handling
- Performance considerations

### Documentation Quality
- Clear usage examples
- Updated architecture diagrams if needed
- Lessons learned captured
- Validation evidence documented

## Handling Issues

### Test Failures
- Debug systematically
- Update implementation, not tests (unless test is wrong)
- Document any deviations from plan

### Missing Requirements
- Note gaps in plan
- Ask user for clarification
- Document decisions in validation report

### Performance Issues
- Measure actual performance
- Compare to requirements
- Optimize if needed
- Document trade-offs

## Important Reminders

- **Always write tests first** - No exceptions to TDD
- **Seek confirmation between phases** - Never skip ahead
- **Validate empirically** - Trust but verify
- **Document everything** - Especially deviations and decisions
- **Store artifacts** - Save all validation reports to `./analysis/`

---

**Remember:** Quality over speed. A properly tested and validated implementation is worth the extra effort.