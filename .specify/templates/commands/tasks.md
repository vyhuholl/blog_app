---
description: Break down specifications or plans into categorized, actionable tasks aligned with constitutional principles.
handoffs: 
  - label: Create Specification
    agent: speckit.specify
    prompt: Create a detailed specification for this work
  - label: Refine Implementation Plan
    agent: speckit.plan
    prompt: Update the implementation plan based on task breakdown insights
---

# Tasks Command

This command breaks down features into specific, actionable tasks categorized by constitutional principle.

## Purpose

Generate organized task lists that ensure balanced attention to:
- Code Quality
- Testing Standards
- User Experience Consistency
- Performance Requirements

## Execution Flow

1. **Load Context**: Read specification or plan, or gather requirements from user input
2. **Identify Work Items**: Break down feature into discrete, achievable tasks
3. **Categorize by Principle**: Group tasks by constitutional principle (Code Quality, Testing, UX, Performance)
4. **Define Acceptance Criteria**: Create specific, testable criteria for each task
5. **Estimate Effort**: Provide hour or story point estimates
6. **Map Dependencies**: Identify task dependencies and sequencing
7. **Plan Iterations**: Organize tasks into sprints or iterations
8. **Generate Task Breakdown**: Write tasks using template at `.specify/templates/tasks-template.md`

## Task Categories

Tasks are organized by constitutional principle:

### Code Quality Tasks (ID: 001-099)
Tasks related to:
- Code implementation following linting standards
- Refactoring for maintainability
- Code review and documentation
- Technical debt resolution

**Acceptance Criteria Include**:
- Code passes linting (zero errors/warnings)
- Cyclomatic complexity < 20
- Code reviewed and approved
- No dead code or commented-out blocks

### Testing Tasks (ID: 101-199)
Tasks related to:
- Unit test development
- Integration test scenarios
- Edge case coverage
- Test automation in CI/CD

**Acceptance Criteria Include**:
- Tests written and passing
- Coverage ≥ 80% for business logic
- All edge cases covered
- No flaky tests

### User Experience Tasks (ID: 201-299)
Tasks related to:
- UI component implementation
- Design system alignment
- Accessibility compliance
- Responsive design

**Acceptance Criteria Include**:
- Follows design system patterns
- WCAG 2.1 AA compliant
- Keyboard navigable and screen reader compatible
- Responsive across viewports

### Performance Tasks (ID: 301-399)
Tasks related to:
- Performance optimization
- Bundle size management
- Database query optimization
- Performance monitoring setup

**Acceptance Criteria Include**:
- Performance metrics meet constitutional targets
- Lighthouse score ≥ 90
- Bundle size within budget
- Database queries optimized

### Infrastructure Tasks (ID: 401-499)
Tasks related to:
- CI/CD pipeline setup
- Development environment configuration
- Deployment automation
- Monitoring and alerting

### Documentation Tasks (ID: 501-599)
Tasks related to:
- Inline code documentation
- API documentation
- User guides
- Architecture decision records

## Task Structure

Each task includes:

- **Task ID**: Unique identifier with category-based numbering
- **Task Name**: Clear, action-oriented description
- **Description**: What needs to be done
- **Acceptance Criteria**: Specific, testable checkpoints including constitutional compliance
- **Estimated Effort**: Hours or story points
- **Dependencies**: Other task IDs that must complete first

## Usage Examples

### Break Down Specification
```
/speckit.tasks Break down the user authentication specification into tasks
```

### Generate Sprint Tasks
```
/speckit.tasks Create tasks for blog post management API (Sprint 1 focus)
```

### Task List with Estimates
```
/speckit.tasks Generate estimated tasks for responsive blog card component
```

## Output

The command produces:

1. **Task Breakdown Document**: Categorized tasks in `.specify/tasks/[feature-name].md`
2. **Task Summary**: Count and effort by constitutional principle
3. **Dependency Graph**: Visual or text representation of task dependencies
4. **Iteration Planning**: Tasks organized into sprints or iterations
5. **Constitutional Compliance Checklist**: Final validation criteria

## Validation Checklist

Before finalizing task breakdown:

- [ ] All tasks have clear, action-oriented names
- [ ] Tasks categorized by appropriate constitutional principle
- [ ] Acceptance criteria are specific and testable
- [ ] Constitutional compliance checks included in acceptance criteria
- [ ] Effort estimates provided
- [ ] Dependencies identified and documented
- [ ] Tasks balanced across principles (not overweighted in one category)
- [ ] Total effort estimate reasonable and validated

## Iteration Planning

Task breakdowns include sprint/iteration recommendations:

- **Iteration 1**: Foundation and core functionality (typically Code Quality + Testing focus)
- **Iteration 2**: User-facing features (typically UX + Testing focus)
- **Iteration 3**: Optimization and polish (typically Performance + all principles)

Each iteration should validate relevant constitutional quality gates.

## Constitutional Compliance

The task breakdown MUST include a final compliance checklist:

- [ ] **Code Quality**: All code reviewed, linted, maintainable
- [ ] **Testing Standards**: ≥ 80% coverage, all tests passing, no flaky tests
- [ ] **User Experience Consistency**: Design system followed, WCAG AA compliant, responsive
- [ ] **Performance Requirements**: All metrics within targets, performance budget respected

## Handoff Notes

After generating tasks:

- Use tasks to populate project management tools (Jira, Linear, GitHub Issues)
- Review effort estimates with team for validation
- Adjust iteration planning based on team capacity
- Track progress against constitutional compliance checklist

