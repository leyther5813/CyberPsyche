# CyberPsyche

### Cybersecurity Awareness & Decision-Training Platform

A research-oriented, full-stack platform for exploring security decision-making through simulated phishing and social-engineering scenarios.

<p align="center">
  <img src="https://img.shields.io/badge/Python-Backend-blue?logo=python" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/React-Frontend-61DAFB?logo=react" alt="React" />
  <img src="https://img.shields.io/badge/TypeScript-Type--Safe-3178C6?logo=typescript" alt="TypeScript" />
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite" alt="SQLite" />
  <img src="https://img.shields.io/badge/Tests-29%20passed-brightgreen" alt="29 backend tests passed during development" />
</p>

---

## Overview

CyberPsyche is a research-oriented cybersecurity awareness and decision-training platform designed to explore how people evaluate potentially suspicious messages, requests, and social-engineering situations.

The platform combines interactive security scenarios with a structured **Baseline → Retest → Transfer** workflow. It records decision-related metrics to support software validation and future research into cybersecurity decision-making.

The project brings together full-stack development, application security, structured study workflows, and responsible research documentation.

## Key Features

- **Structured study workflow** — Organizes activities into baseline, retest, and transfer phases.
- **Simulated security scenarios** — Presents phishing and social-engineering situations in a controlled environment.
- **Decision-related metrics** — Supports tracking measures such as decision quality and out-of-band verification.
- **Study session management** — Provides a guided workflow for completing study activities.
- **Research documentation** — Includes study protocol, ethics and consent considerations, and threat-model documentation.
- **Automated backend testing** — Uses `pytest` to validate backend functionality.
- **Production frontend build** — Uses Vite to build the React and TypeScript application.

## Technology Stack

| Layer | Technologies |
|---|---|
| Backend | Python, FastAPI |
| Frontend | React, TypeScript, Vite |
| Data storage | SQLite |
| Automated testing | pytest |
| Research resources | Study documentation and analysis tools |

## Project Architecture

```text
CyberPsyche/
├── analysis/    # Analysis resources and synthetic visualizations
├── backend/     # API, application services, scenarios, and tests
├── docs/        # Study protocol, ethics, consent, and threat model
├── frontend/    # React and TypeScript application
├── docker-compose.yml
├── .gitignore
├── AGENTS.md
└── README.md
```

## Getting Started

### Prerequisites

Install the following tools:

- Python
- Node.js and npm
- Git

Use versions compatible with the project's dependency and configuration files.

### 1. Clone the Repository

```bash
git clone https://github.com/leyther5813/CyberPsyche.git
cd CyberPsyche
```

### 2. Set Up the Backend

From the project root, create a Python virtual environment:

```powershell
cd backend
python -m venv .venv
```

Activate the virtual environment in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the backend dependencies:

```bash
python -m pip install -r requirements.txt
```

Configure the required environment variables and database settings according to the backend configuration and project documentation. Do not use development secrets in a production deployment.

Run the backend tests:

```bash
python -m pytest -q
```

Start the development API server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

- API base URL: `http://127.0.0.1:8000`
- Interactive API documentation: `http://127.0.0.1:8000/docs`

Keep the backend terminal running while using the application.

### 3. Set Up the Frontend

Open a **separate terminal** in the project root and navigate to the frontend directory:

```bash
cd frontend
npm ci
```

Start the frontend development server:

```bash
npm run dev
```

To create a production build:

```bash
npm run build
```

Use the local URL printed by Vite to open the frontend in your browser.

**Note:** The commands above describe the development workflow. Follow the repository's actual environment settings, dependency files, and configuration when running the application in another environment.

## Validation

During development, the following checks completed successfully:

- **Backend:** 29 automated tests passed.
- **Frontend:** The Vite production build completed successfully.

These results reflect software validation at the time of testing. They do not independently demonstrate improved cybersecurity behaviour, training effectiveness, or generalizability to a wider population.

## Research, Ethics & Responsible Use

CyberPsyche is designed to support controlled cybersecurity awareness activities and future research.

- Scenarios are simulated and intended for a controlled environment.
- Synthetic visualizations represent synthetic data, not observations from human participants.
- Any participant-based study should follow applicable ethics-review requirements, informed-consent procedures, privacy protections, and data-management practices.
- Research conclusions should be based on an appropriate study design and supporting evidence rather than software metrics alone.

## Security Considerations

- Never commit real credentials, access tokens, production secrets, local databases, or identifiable participant data.
- Use unique, sufficiently strong secrets and appropriate environment-specific settings for deployments.
- Review the application's security configuration and threat model before deployment.
- Treat the development configuration as a starting point, not a guarantee of production security.

## Current Status

**Status:** Under active development.

The platform's features, metrics, and study procedures may evolve as implementation and validation continue. This repository documents an ongoing software and research project; it does not claim that the platform has been deployed as a production service or that its training effectiveness has been experimentally established.

## Future Directions

Potential areas for further development include:

- Expanded scenario coverage and evaluation.
- Improved reporting and analysis of decision-related metrics.
- Additional testing and deployment hardening.
- Further validation of study procedures and research measures.

These are prospective directions, not claims of completed functionality.

## License

No open-source license has been selected for this repository. Unless a license is added, the code is not automatically granted open-source reuse permissions. Contact the copyright holder for permission to reuse or redistribute it.

---

**CyberPsyche** — Exploring cybersecurity decision-making through software, simulation, and responsible research.
