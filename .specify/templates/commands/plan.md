---
description: Create implementation plans with phased approach and constitutional quality gates.
handoffs: 
  - label: Generate Task Breakdown
    agent: speckit.tasks
    prompt: Break this plan down into specific actionable tasks
  - label: Refine Specification
    agent: speckit.specify
    prompt: Update the specification based on planning insights
---

# Plan Command

This command creates detailed implementation plans with quality gates aligned to constitutional principles.

## Purpose

Generate phased implementation plans that ensure:
- Code quality maintained throughout development
- Testing integrated at every phase
- UX consistency enforced from design to deployment
- Performance targets monitored and validated

## Execution Flow

1. **Load Specification**: Read feature specification or gather requirements
2. **Define Phases**: Break implementation into logical, manageable phases
3. **Create Quality Gates**: Define constitutional compliance checks for each phase
4. **Map Dependencies**: Identify external, team, and infrastructure dependencies
5. **Risk Mitigation**: Document risks with mitigation and contingency plans
6. **Testing Strategy**: Define unit, integration, performance, and accessibility testing approach
7. **Rollout Plan**: Specify deployment strategy with monitoring and rollback procedures
8. **Generate Plan**: Write plan using template at `.specify/templates/plan-template.md`

## Constitutional Quality Gates

Every phase MUST pass these quality gates before proceeding:

### Code Quality Gate
- [ ] Code passes linter (zero errors, zero warnings)
- [ ] Cyclomatic complexity < 20 per function
- [ ] No code duplication (DRY principle)
- [ ] Peer review completed with approval

### Testing Gate
- [ ] Unit tests written and passing (≥ 80% coverage)
- [ ] Integration tests cover critical workflows
- [ ] All tests pass in CI/CD
- [ ] No flaky tests

### UX Gate
- [ ] Follows design system components and patterns
- [ ] Passes accessibility audit (WCAG 2.1 AA)
- [ ] Responsive across mobile/tablet/desktop
- [ ] User feedback implemented (loading, errors, success)

### Performance Gate
- [ ] FCP < 1.5s, LCP < 2.5s, TTI < 3.5s
- [ ] API responses < 200ms (p95)
- [ ] Bundle size within budget
- [ ] Database queries optimized (no N+1)

## Implementation Phases

Plans typically include:

1. **Foundation Phase**: Setup, infrastructure, core architecture
2. **Development Phase**: Feature implementation with continuous testing
3. **Integration Phase**: End-to-end testing and performance optimization
4. **Deployment Phase**: Staging validation, production rollout, monitoring

Each phase includes:
- Objective and deliverables
- Tasks mapped to constitutional principles
- Exit criteria
- Quality gate validation

## Testing Strategy

Plans MUST define:

- **Unit Testing**: Scope, coverage targets, testing framework
- **Integration Testing**: End-to-end workflows and scenarios
- **Performance Testing**: Metrics (FCP, LCP, TTI, API response times) and tools
- **Accessibility Testing**: WCAG compliance validation tools and process

## Rollout and Monitoring

Plans MUST include:

- Deployment strategy (feature flags, staging validation)
- Performance monitoring instrumentation
- Error tracking and alerting
- Rollback plan and procedures

## Usage Examples

### Create Implementation Plan
```
/speckit.plan Create implementation plan for user authentication system
```

### Plan with Time Constraints
```
/speckit.plan Plan blog post CRUD API implementation with 2-week timeline
```

### Plan for Performance-Critical Feature
```
/speckit.plan Plan real-time notification system with sub-100ms latency requirement
```

## Output

The command produces:

1. **Implementation Plan**: Phased plan in `.specify/plans/[feature-name].md`
2. **Quality Gates**: Constitutional compliance checkpoints for each phase
3. **Testing Strategy**: Comprehensive testing approach
4. **Risk Assessment**: Identified risks with mitigation strategies

## Validation Checklist

Before finalizing the plan:

- [ ] Constitution check completed (all four principles addressed)
- [ ] Phases have clear objectives and exit criteria
- [ ] Quality gates defined for each phase
- [ ] Dependencies identified (external, team, infrastructure)
- [ ] Testing strategy covers unit, integration, performance, accessibility
- [ ] Rollout plan includes monitoring and rollback procedures
- [ ] Documentation requirements specified
- [ ] Post-implementation review criteria defined

## Handoff Notes

After generating a plan:

- Use `/speckit.tasks` to break down phases into specific tasks
- Share plan with team for review and timeline validation
- Update specification if planning reveals scope changes

