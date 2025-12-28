---
description: Generate detailed feature specifications aligned with constitutional principles.
handoffs: 
  - label: Create Implementation Plan
    agent: speckit.plan
    prompt: Create an implementation plan for this specification
  - label: Break Down Into Tasks
    agent: speckit.tasks
    prompt: Break this specification down into actionable tasks
---

# Specify Command

This command generates comprehensive feature specifications that align with the project constitution.

## Purpose

Create detailed, testable specifications that explicitly map to constitutional principles:
- Code Quality
- Testing Standards
- User Experience Consistency
- Performance Requirements

## Execution Flow

1. **Gather Requirements**: Collect feature requirements from user input or discovery process
2. **Constitutional Mapping**: Explicitly map feature to relevant constitutional principles
3. **Define Scope**: Establish in-scope, out-of-scope boundaries and dependencies
4. **Set Quality Standards**: Define code quality, testing, UX, and performance targets
5. **Create Acceptance Criteria**: Include both functional validation and constitutional compliance checks
6. **Risk Assessment**: Identify technical, UX, and performance risks with mitigation strategies
7. **Generate Specification**: Write specification using template at `.specify/templates/spec-template.md`

## Constitutional Alignment

Every specification MUST include:

### Code Quality Standards
- Linting configuration and complexity targets
- Documentation requirements
- Code review process

### Testing Requirements
- Unit test coverage targets (≥ 80%)
- Integration test scenarios
- Performance benchmarks

### UX Standards
- Design system component usage
- Accessibility compliance (WCAG 2.1 AA)
- Responsive design requirements
- User feedback mechanisms

### Performance Targets
- FCP < 1.5s, LCP < 2.5s, TTI < 3.5s
- API response times < 200ms (p95)
- Bundle size constraints
- Database optimization requirements

## Template Structure

Specifications follow this structure:

1. **Feature Overview**: Name, description, constitutional alignment
2. **Requirements**: Functional and non-functional requirements by principle
3. **Scope**: In/out of scope, dependencies
4. **Technical Approach**: Architecture, technology stack, data model
5. **Acceptance Criteria**: Functional validation and constitutional compliance
6. **Risk Assessment**: Identified risks and mitigation strategies
7. **Success Metrics**: Functional, quality, and performance targets

## Usage Examples

### Create Feature Specification
```
/speckit.specify Create a user authentication system with email and password
```

### Generate API Specification
```
/speckit.specify Design a RESTful API for blog post management (CRUD operations)
```

### Specify UI Component
```
/speckit.specify Build a responsive blog post card component with accessibility support
```

## Output

The command produces:

1. **Specification Document**: Detailed feature spec in `.specify/specs/[feature-name].md`
2. **Constitutional Mapping**: Explicit alignment with all four principles
3. **Acceptance Criteria**: Testable criteria including constitutional compliance checks

## Validation Checklist

Before finalizing the specification:

- [ ] Constitutional alignment explicitly documented for all four principles
- [ ] Functional requirements are specific and testable
- [ ] Non-functional requirements include quality, testing, UX, and performance targets
- [ ] Acceptance criteria include constitutional compliance validation
- [ ] Risk assessment covers technical, UX, and performance concerns
- [ ] Success metrics are measurable and aligned with constitution
- [ ] Dependencies and scope are clearly defined

## Handoff Notes

After generating a specification:

- Use `/speckit.plan` to create an implementation plan
- Use `/speckit.tasks` to break down into actionable tasks
- Share specification with stakeholders for review and approval

