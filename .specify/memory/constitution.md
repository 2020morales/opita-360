<!--
Sync Impact Report:
- Version change: unversioned scaffold -> 1.0.0
- Modified principles: none (initial project constitution)
- Added sections: Core Principles, Technology and Data Constraints, Development Workflow
- Removed sections: none
- Follow-up TODOs: Confirm and replace TODO(RATIFICATION_DATE) with the formal adoption date.
-->

# OPITA 360 Constitution

## Core Principles

### I. User-Visible Quality and Accessibility

User-facing behavior MUST remain usable with keyboard navigation, clear feedback, and
accessible visual states. Destination filters, recommendations, and API fallback behavior
MUST preserve the existing demo experience when the API is unavailable. Frontend changes
MUST be implemented with React and Vite patterns already present in the project.

### II. Stable API Contracts

Backend behavior MUST remain compatible with FastAPI/Pydantic contracts and the public routes
`GET /`, `GET /api/destinations`, `GET /api/destinations/{destination_id}`, and
`POST /api/recommendations`. Optional municipality and budget behavior MUST be validated
without changing the established first-stop-over-budget contract. API and UI changes MUST
remain traceable through request, response, and test behavior.

### III. Test-First and Evidence-Based Delivery (NON-NEGOTIABLE)

Feature work MUST begin from approved acceptance criteria and executable cases. Tests MUST
fail for missing behavior before implementation, then pass after implementation. Delivery
MUST use real verification results; builds and syntax checks do not substitute for functional
tests. New evidence MUST include the command, output, date, and isolated destination for
verification artifacts that prohibit overwriting existing files.

### IV. Integration and Regression Integrity

Changes MUST preserve existing behavior across frontend, backend, filters, accessibility,
and API/demo recovery paths. Integration work MUST be limited to work authorized by the
current feature plan and MAY NOT publish, merge, or alter protected historical branches or
pull requests without explicit human approval. PostgreSQL schema preparation MUST NOT be
presented as implemented persistence.

### V. Small, Traceable, and Reviewable Changes

Implementation MUST use the smallest coherent change that satisfies approved scope. Python
MUST use snake_case, React state and catalog data MUST remain unmutated, and JavaScript
filter logic MUST remain in focused pure functions. Every criterion SHOULD map to an
`AC-NN` case and every test case SHOULD map to `TC-spec-NN` evidence with a complete
requirement-to-test trace.

## Technology and Data Constraints

OPITA 360 MUST remain a React/Vite and FastAPI monorepo using in-memory destination and
recommendation data unless persistence is explicitly approved. Local development MUST target
the existing API port 8000 and frontend port 5173. PostgreSQL support MUST remain limited to
`database/schema.sql` until real persistence is implemented and verified. Secrets, account
names, and local machine paths MUST NOT appear in project reports.

The project SHOULD support Python 3.10 or newer and Node.js 22.12 or newer. Dependency changes
MUST be limited to approved manifests and lockfiles, and networked package installation
requires separate authorization when the environment needs it.

## Development Workflow

Feature work MUST follow specification, plan, tasks, and executable cases before implementation.
The human operator MUST approve scope and implementation plans. Protected Taller 4, Taller 5,
its PDF and historical evidence, and original agent/skill content MUST NOT be modified during
Taller 6 except through explicitly authorized corrective work.

Before completion, applicable verification MUST include the relevant unit suites, frontend
tests and build, harness validation, and harness checks for the affected scope. Reviews MUST
distinguish executed facts from pending or historical claims, and MUST NOT represent docente
certification or approval as accredited without direct evidence.

Commits, pushes, merges, and pull requests require explicit human authorization. Completion
MUST include a concise review of changed behavior, validation results, and unresolved risks.

## Governance

This constitution supersedes ad hoc project practices for governance, verification, and
protected-work handling. Amendments MUST be proposed, reviewed, and approved by the human
project owner, documented in the Sync Impact Report, and accompanied by a migration plan when
governance or principle changes affect existing work.

Version changes MUST follow semantic versioning: MAJOR for incompatible governance or principle
redefinitions/removals, MINOR for a new or materially expanded principle or section, and PATCH
for clarification or non-semantic refinement. Compliance MUST be reviewed at feature planning,
implementation review, and final verification.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): Confirm the formal adoption date | **Last Amended**: 2026-11-24
