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

**Important:** Each phase should result in at least ONE commit of working, tested code.

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

**Step 2.5: Commit Phase Work**

After completing TDD implementation for this phase:

```
a. Review Changes
   - Run `git status` to see modified files
   - Run `git diff` to review changes
   - Ensure all tests pass

b. Stage and Commit
   - Use `/commit` command to create atomic commit
   - Commit message should:
     * Use conventional format: `<emoji> <type>: <description>`
     * Describe WHAT changed and WHY
     * Reference plan/phase number
     * Be imperative mood ("add" not "added")

   Example: ✨ feat(types): add optional B2B fields for Event Tech Live data

c. Commit Granularity Guidelines
   - ✅ Commit after completing a logical unit (phase or major step)
   - ✅ Include tests with implementation in same commit
   - ✅ Keep commits focused (ideally 5-15 files)
   - ❌ Never commit broken/failing tests
   - ❌ Don't bundle unrelated changes

d. For Large Phases
   - Consider breaking into multiple commits if phase touches 20+ files
   - Commit after each major component within the phase
   - Each commit should leave codebase in working state
```

**Step 3: Phase Validation**
- Run all tests for this phase
- Verify phase-specific success criteria
- Create validation report in `./analysis/`

**Step 3.5: END-TO-END VALIDATION (For Integration Phases)**

**CRITICAL**: If this phase involves integrating multiple systems/languages (e.g., Python→TypeScript, API→Database), you MUST run the actual end-to-end pipeline with REAL data:

```
a. Check Environment Setup
   - Verify all required environment variables (.env file)
   - Verify all required API keys/secrets are configured
   - Verify all dependencies are installed

b. Run Actual System A
   - Execute the REAL CLI command (not just unit tests)
   - Verify it produces actual output files/data
   - Check the output matches expected schema

c. Run Actual System B with System A's Output
   - Use the REAL output from System A (not mock data)
   - Verify System B successfully consumes it
   - Verify end result is correct

d. Document the Validation
   - Save command outputs to validation report
   - Include file sizes, timing, error messages
   - Prove the pipeline actually works

e. Fix Any Runtime Bugs
   - Environment issues (missing keys)
   - Integration bugs (wrong method calls)
   - Schema mismatches (field names, types)
   - Performance issues with real data
```

**Red Flags - You're NOT Validating Properly:**
- ❌ "I created sample JSON to test with"
- ❌ "All unit tests pass" (but never ran CLI)
- ❌ "Schema looks compatible" (but never tried real data)
- ❌ "Should work" (but never executed end-to-end)

**Validation is NOT complete until:**
- ✅ System A ran and created actual output file
- ✅ System B successfully consumed that actual file
- ✅ End result verified to be correct
- ✅ All runtime bugs discovered and fixed

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

3. **Update Documentation and Commit**
   - Update README.md with new features/usage
   - Update CLAUDE.md with lessons learned
   - Update architecture documentation
   - Update plan status to "Completed"
   - **COMMIT documentation changes:**
     ```
     📝 docs: complete Plan NNN implementation documentation

     - Update README with new features
     - Add lessons learned to CLAUDE.md
     - Mark Plan NNN as completed
     - Add validation report to analysis/
     ```

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

### Commit Quality

**Conventional Format:**
- `<emoji> <type>(scope): <description>` (use `/commit` command)
- Types: feat, fix, docs, test, refactor, chore, ci, build
- Imperative mood: "add" not "added"
- Subject line < 72 characters

**Atomicity:**
- One logical change per commit
- Commits should be revertable without side effects
- Each commit leaves codebase in working, tested state

**When to Commit:**
- ✅ After each phase completion
- ✅ After major component within large phases
- ✅ After GREEN + REFACTOR in TDD cycle
- ❌ Never during RED phase (broken tests)
- ❌ Never commit untested code

**Size Guidelines:**
- Small: 5-15 files (ideal for most features)
- Medium: 15-30 files (acceptable for complex features)
- Large: 30+ files (split into multiple commits if possible)

**What to Include:**
- Implementation + tests together
- Related documentation updates
- Required configuration changes
- Nothing unrelated to the change

**Tools:**
- Use `/commit` command for consistent formatting
- Command handles splitting suggestions
- Follows conventional commits automatically

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

## Example: Commit Workflow for Multi-Phase Implementation

**Scenario:** Implementing Plan 002 (7 phases)

```
Phase 1: Data Model Enhancement
├─ Write type tests → Implement types → Tests pass
├─ Write template tests → Update templates → Tests pass
└─ COMMIT: "✨ feat(types): add optional B2B fields with backward compatibility"

Phase 2: Event Configuration
├─ Create event-tech-live-2025.json
├─ Add tests for event loading
└─ COMMIT: "✨ feat(data): add Event Tech Live 2025 configuration"

Phase 3: Session Generation (LARGE - split into 2 commits)
├─ Create session data structure
├─ COMMIT: "✨ feat(data): add 30 Event Tech Live session topics"
├─ Map sessions to tracks and speakers
└─ COMMIT: "✨ feat(data): map sessions to tracks with real company speakers"

[Phases 4-6: Similar pattern]

Phase 7: Testing & Validation
├─ Run all tests, fix issues
├─ COMMIT: "✅ test: validate all Plan 002 success criteria"
├─ Update documentation
└─ COMMIT: "📝 docs: complete Plan 002 implementation documentation"
```

**Result:** 8-9 atomic commits instead of 1 massive commit

**Benefits:**
- Easier code review (each commit is focused)
- Safe reverts (can undo specific phases)
- Clear history (understand evolution)
- Effective git bisect (find bug introduction)

## Important Reminders

- **Always write tests first** - No exceptions to TDD
- **Seek confirmation between phases** - Never skip ahead
- **Validate empirically** - Trust but verify
- **Document everything** - Especially deviations and decisions
- **Store artifacts** - Save all validation reports to `./analysis/`
- **Commit at phase boundaries** - Each phase = at least one commit
- **Keep commits atomic** - One logical change per commit
- **Include tests with code** - Tests and implementation together
- **Use `/commit` command** - Ensures consistent formatting

---

**Remember:** Quality over speed. A properly tested and validated implementation is worth the extra effort.