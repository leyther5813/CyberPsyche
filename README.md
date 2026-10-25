\# CyberPsyche



\*\*A Research-Oriented Cybersecurity Awareness and Decision-Training Platform\*\*



CyberPsyche is a full-stack platform designed to explore how people make security decisions when faced with simulated phishing and social-engineering scenarios. It provides structured study phases and decision-related metrics to support cybersecurity awareness training and future research.



\## Key Features



\- \*\*Structured study workflow:\*\* Baseline, retest, and transfer phases.

\- \*\*Interactive security scenarios:\*\* Simulated situations designed to encourage careful evaluation of potentially suspicious messages and requests.

\- \*\*Decision-related metrics:\*\* Tracks measures such as decision quality and out-of-band verification.

\- \*\*Study session management:\*\* Supports progression through a guided training workflow.

\- \*\*Research-oriented design:\*\* Includes study protocol, ethics and consent documentation, and a threat model.



\## Technology Stack



\- \*\*Backend:\*\* Python, FastAPI

\- \*\*Frontend:\*\* React, TypeScript, Vite

\- \*\*Data storage:\*\* SQLite

\- \*\*Testing:\*\* pytest and frontend production builds



\## Project Structure



\- `backend/` — API, application services, scenarios, and automated tests

\- `frontend/` — React and TypeScript user interface

\- `docs/` — Study protocol, ethics and consent, and threat-model documentation

\- `analysis/` — Analysis resources and synthetic validation visualizations



\## Local Development



\### Backend



1\. Navigate to the backend directory.

2\. Create and activate a Python virtual environment.

3\. Install the dependencies listed in the project's dependency files.

4\. Configure appropriate local environment variables and a development database.

5\. Start the FastAPI application using the project's configured entry point.



Run the automated tests from the backend directory:



```bash

python -m pytest -q

```



\### Frontend



1\. Navigate to `frontend/`.

2\. Install the dependencies using the package lockfile.

3\. Start the development server using the project's npm scripts.



Create a production build with:



```bash

npm run build

```



Consult the project configuration and dependency files for the exact setup requirements.



\## Validation



During development, the backend test suite completed with \*\*29 passing tests\*\*, and the frontend production build completed successfully.



These results demonstrate software validation at that point in development. They do not establish that the platform improves cybersecurity behaviour or that its research findings generalize to a wider population.



\## Research and Responsible Use



CyberPsyche is intended for controlled cybersecurity awareness training and research. Its scenarios are simulations, not live phishing campaigns.



The included synthetic validation visualizations should be interpreted as synthetic data, not as evidence from human participants. Any future participant study should follow the applicable ethics-review, informed-consent, privacy, and data-management requirements.



\## Security Notes



\- Never commit real credentials, access tokens, production secrets, local databases, or identifiable participant data.

\- Use strong, unique secrets and appropriate security settings for any deployment.

\- Review the study documentation and threat model before deploying the application or conducting research.



\## Project Status



This is a developing research-oriented software project. Features, study procedures, and metrics may evolve as validation continues.



\## License



No open-source license has been selected yet. All rights remain with the copyright holder unless a license is added.
