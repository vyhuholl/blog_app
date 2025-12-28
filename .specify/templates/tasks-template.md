# Task Breakdown Template

**Constitution Version**: 1.0.0

---

## Feature/Epic Name
[Name from specification or plan]

---

## Task Categorization

Tasks are categorized by constitutional principle to ensure balanced attention to quality, testing, UX, and performance.

---

## Code Quality Tasks

### [Task ID-001]: [Task Name]
**Description**: [What needs to be done]

**Acceptance Criteria**:
- [ ] [Specific, testable criterion]
- [ ] Code passes linting (zero errors/warnings)
- [ ] Cyclomatic complexity < 20
- [ ] Code reviewed and approved
- [ ] No dead code or commented-out blocks

**Estimated Effort**: [Hours/Story Points]

**Dependencies**: [Other task IDs]

---

### [Task ID-002]: [Task Name]
[Repeat structure for each code quality task]

---

## Testing Tasks

### [Task ID-101]: [Task Name]
**Description**: [What needs to be tested]

**Test Coverage**:
- Unit Tests: [Scope]
- Integration Tests: [Scope]
- Edge Cases: [List specific cases]

**Acceptance Criteria**:
- [ ] Tests written and passing
- [ ] Coverage ≥ 80% for business logic
- [ ] All edge cases covered
- [ ] Tests run in CI/CD
- [ ] No flaky tests

**Estimated Effort**: [Hours/Story Points]

**Dependencies**: [Other task IDs]

---

### [Task ID-102]: [Task Name]
[Repeat structure for each testing task]

---

## User Experience Tasks

### [Task ID-201]: [Task Name]
**Description**: [UX component or flow to implement]

**Design Requirements**:
- Design System Components: [List]
- Accessibility: [Specific requirements]
- Responsive Breakpoints: [Mobile/Tablet/Desktop]
- User Feedback: [Loading/Error/Success states]

**Acceptance Criteria**:
- [ ] Follows design system patterns
- [ ] WCAG 2.1 AA compliant
- [ ] Keyboard navigable
- [ ] Screen reader compatible
- [ ] Responsive across viewports
- [ ] User feedback implemented

**Estimated Effort**: [Hours/Story Points]

**Dependencies**: [Other task IDs]

---

### [Task ID-202]: [Task Name]
[Repeat structure for each UX task]

---

## Performance Tasks

### [Task ID-301]: [Task Name]
**Description**: [Performance optimization or requirement]

**Performance Targets**:
- FCP: < 1.5s
- LCP: < 2.5s
- TTI: < 3.5s
- API Response: < 200ms (p95)
- Bundle Size: [Specific limit]
- Database: [Query optimization requirements]

**Acceptance Criteria**:
- [ ] Performance metrics meet targets
- [ ] Lighthouse score ≥ 90
- [ ] Bundle size within budget
- [ ] Database queries optimized
- [ ] Performance tests passing
- [ ] Monitoring configured

**Estimated Effort**: [Hours/Story Points]

**Dependencies**: [Other task IDs]

---

### [Task ID-302]: [Task Name]
[Repeat structure for each performance task]

---

## Infrastructure & DevOps Tasks

### [Task ID-401]: [Task Name]
**Description**: [Infrastructure or CI/CD work]

**Acceptance Criteria**:
- [ ] [Specific criterion]
- [ ] Integrates with CI/CD pipeline
- [ ] Supports quality gates (linting, testing, performance)
- [ ] Documented and reproducible

**Estimated Effort**: [Hours/Story Points]

**Dependencies**: [Other task IDs]

---

## Documentation Tasks

### [Task ID-501]: [Task Name]
**Description**: [Documentation to create or update]

**Scope**:
- [ ] Inline code comments
- [ ] API documentation
- [ ] User guides
- [ ] Architecture decision records
- [ ] Design system updates

**Acceptance Criteria**:
- [ ] Documentation accurate and complete
- [ ] Examples provided where applicable
- [ ] Reviewed for clarity

**Estimated Effort**: [Hours/Story Points]

**Dependencies**: [Other task IDs]

---

## Task Summary

### By Constitutional Principle
- **Code Quality Tasks**: [Count] ([Total estimated effort])
- **Testing Tasks**: [Count] ([Total estimated effort])
- **User Experience Tasks**: [Count] ([Total estimated effort])
- **Performance Tasks**: [Count] ([Total estimated effort])
- **Infrastructure Tasks**: [Count] ([Total estimated effort])
- **Documentation Tasks**: [Count] ([Total estimated effort])

**Total Tasks**: [Count]
**Total Estimated Effort**: [Hours/Story Points]

---

## Task Dependency Graph

```
[Visual representation or text list of task dependencies]

Example:
Task-001 (Code Quality: Setup)
  └─> Task-101 (Testing: Unit tests for setup)
  └─> Task-201 (UX: Component implementation)
      └─> Task-202 (UX: Accessibility audit)
      └─> Task-301 (Performance: Bundle optimization)
```

---

## Sprint/Iteration Planning

### Iteration 1
- Tasks: [Task IDs]
- Focus: [Primary constitutional principle]
- Quality Gates: [Required gates]

### Iteration 2
- Tasks: [Task IDs]
- Focus: [Primary constitutional principle]
- Quality Gates: [Required gates]

---

## Constitutional Compliance Checklist

Before marking feature complete, validate all tasks meet constitutional standards:

- [ ] **Code Quality**: All code reviewed, linted, maintainable
- [ ] **Testing Standards**: ≥ 80% coverage, all tests passing, no flaky tests
- [ ] **User Experience Consistency**: Design system followed, WCAG AA compliant, responsive
- [ ] **Performance Requirements**: All metrics within targets, performance budget respected

---

## Notes

[Any additional context, blockers, or considerations]
