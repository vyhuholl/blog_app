---
description: Create or update the project constitution from interactive or provided principle inputs, ensuring all dependent templates stay in sync.
handoffs: 
  - label: Build Specification
    agent: speckit.specify
    prompt: Implement the feature specification based on the updated constitution. I want to build...
---

# Constitution Command

This command manages the project constitution at `.specify/memory/constitution.md`.

## Purpose

The constitution is the foundational document that establishes non-negotiable principles for the project. All specifications, plans, and tasks MUST align with constitutional principles.

## Execution Flow

1. **Load Existing Constitution**: Read `.specify/memory/constitution.md` and identify all placeholder tokens
2. **Collect Values**: Derive values from user input, repository context, or existing documentation
3. **Draft Updated Constitution**: Replace placeholders with concrete, testable principles
4. **Propagate Changes**: Update all dependent templates to reflect constitutional amendments
5. **Generate Sync Report**: Document version changes, modified principles, and affected templates
6. **Validate**: Ensure no unexplained placeholders remain and all formatting is correct
7. **Write Constitution**: Save the updated constitution file
8. **Output Summary**: Provide version bump rationale and follow-up actions

## Constitutional Principles

The blog_app constitution focuses on four core principles:

1. **Code Quality**: Maintainable, clean, and reviewed code
2. **Testing Standards**: Comprehensive and automated testing
3. **User Experience Consistency**: Coherent, accessible, and delightful interfaces
4. **Performance Requirements**: Fast, efficient, and scalable operations

## Template Dependencies

When updating the constitution, the following templates MUST be checked for consistency:

- `.specify/templates/spec-template.md`: Specification structure and constitutional alignment section
- `.specify/templates/plan-template.md`: Implementation phases and quality gates
- `.specify/templates/tasks-template.md`: Task categorization by constitutional principle
- `.specify/templates/commands/*.md`: Command documentation and constitutional references

## Versioning Rules

Constitution versions follow semantic versioning:

- **MAJOR**: Removal or fundamental redefinition of core principles (backward incompatible)
- **MINOR**: Addition of new principles or material expansion of existing principles
- **PATCH**: Clarifications, wording improvements, non-semantic refinements

## Usage Examples

### Create Initial Constitution
```
/speckit.constitution Create principles focused on code quality, testing standards, user experience consistency, and performance requirements
```

### Add New Principle
```
/speckit.constitution Add security principle requiring encryption at rest and in transit
```

### Refine Existing Principle
```
/speckit.constitution Update testing standards to include E2E testing requirements
```

## Output

The command produces:

1. **Updated Constitution File**: `.specify/memory/constitution.md` with all placeholders replaced
2. **Sync Impact Report**: HTML comment at top of constitution documenting changes
3. **Summary**: Version bump rationale, affected files, and suggested commit message

## Validation Checklist

Before finalizing the constitution update:

- [ ] No unexplained bracket tokens remain
- [ ] Version line matches sync report
- [ ] Dates in ISO format (YYYY-MM-DD)
- [ ] Principles are declarative and testable
- [ ] All dependent templates reviewed and updated
- [ ] Governance section includes amendment process
- [ ] Rationale provided for each principle

## Notes

- The constitution is living documentation and should evolve with the project
- All team members can propose amendments
- Constitutional compliance is validated at code review and in CI/CD pipelines

