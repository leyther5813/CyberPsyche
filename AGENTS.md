# CYBERPSYCHE — PROJECT CONSTITUTION

CyberPsyche is a research-oriented cybersecurity application.

Official title:
A Decision-Process Laboratory for Social-Engineering Resilience

The official CyberPsyche specification supplied by the project owner is the
SOURCE OF TRUTH.

NON-NEGOTIABLE RULES

1. Never change the research objective without explicit approval.
2. Never replace the decision-process focus with a generic phishing-awareness app.
3. Never turn CyberPsyche into a generic quiz application.
4. Never turn CyberPsyche into a generic chatbot or AI social-engineering roleplay system.
5. Never allow the LLM to determine scenario ground truth.
6. Ground truth must remain schema-controlled.
7. Behavioural scoring must remain rule-based.
8. Never diagnose personality, psychological disorders, or mental health conditions.
9. Never collect real passwords, OTPs, bank information, credentials, or private messages.
10. Never use real malicious links, payloads, or credential harvesting.
11. Never expose scenario ground truth, evidence signals, or safe actions before the user's decision.
12. Scenarios must support malicious, genuine, and ambiguous truth classes.
13. The system must measure both under-caution and over-caution.
14. The system must include baseline → intervention → retest → transfer.
15. Transfer must involve changed context and/or channel while preserving the underlying manipulation mechanism.
16. The application must measure behaviour, not merely click/no-click.
17. AI is permitted for controlled wording generation and approved feedback assistance only.
18. AI-generated scenario wording must be schema-constrained and human-reviewed before study use.
19. Do not introduce future/out-of-scope features unless explicitly approved.
20. Do not fabricate research results, participant numbers, effect sizes, or evaluation results.
21. All security controls specified in THREAT_MODEL.md must be implemented before production/demo release.
22. Every major implementation decision must remain consistent with PROJECT_SPEC.md.

PRODUCT DESIGN

CyberPsyche should feel like a professional cybersecurity research laboratory.

Visual direction:
- Primary visual identity: blue.
- Secondary palette: light blue / blue-gray.
- Small sunflower-yellow accent is permitted.
- Sunflower motif must remain subtle and secondary.
- Clean, modern, accessible interface.
- Research-lab/product aesthetic.
- No hacker aesthetic.
- No Matrix aesthetic.
- No excessive neon.
- No skulls or stereotypical cyber imagery.
- No childish gamification aesthetic.

ENGINEERING PRINCIPLES

- TypeScript frontend.
- React/Next.js frontend.
- FastAPI backend.
- PostgreSQL database.
- SQLAlchemy/Alembic.
- Pydantic validation.
- Docker Compose.
- pytest.
- pandas/scipy/statsmodels/matplotlib for analysis.
- Secure-by-default implementation.
- Server-side scoring.
- Strong authentication.
- RBAC.
- Audit logging.
- Parameterized queries/ORM.
- Input validation.
- XSS protection.
- CSP.
- HSTS.
- Appropriate CSRF protection if cookie-based sessions are used.
- Rate limiting.
- Minimal data collection.
- Pseudonymous research exports.

DEVELOPMENT BEHAVIOUR

Before implementing a major feature:
1. inspect the specification;
2. explain the implementation plan;
3. identify affected components;
4. implement;
5. run tests;
6. run the application;
7. verify through the browser where appropriate;
8. report what changed and what remains.

Do not silently change architecture or research methodology.