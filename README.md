# Social Media Privacy Risk Assessment Framework

A defensive cybersecurity project that evaluates social-media privacy practices from voluntary categorical answers. It does not access or scrape social-media accounts and never asks for actual phone numbers, emails, addresses, birth dates, passwords, verification codes, exact locations, or private messages.

> This project is designed for defensive cybersecurity and privacy education. It uses synthetic or voluntarily provided assessment responses and does not scrape, track, or profile real social-media users.

## Overview

The application asks 54 questions across ten categories, calculates category and overall risk scores, and provides findings, recommendations, an improvement simulator, dashboard, printable HTML report, REST API, and summary-only SQLite storage. A seeded generator creates 1,000 fictional assessment records.

## Privacy vs security

Privacy concerns how information is collected, shared, exposed, and used. Security protects accounts and information against unauthorized access or misuse. Strong authentication does not prevent a public profile from exposing too much information.

## Risk categories and scoring

Profile Exposure, Personal Information, Location Exposure, Content Exposure, Connection Risk, Tagging Risk, Account Security, Third-Party Apps, Social Engineering, and Digital Footprint.

Scores range from 0 (lower assessed risk) to 100 (higher assessed risk). Default weights, in category order, are 10%, 15%, 15%, 10%, 10%, 5%, 15%, 5%, 10%, and 5%. Levels: LOW (0–20), MODERATE (21–40), HIGH (41–70), CRITICAL (71–100). These are educational assumptions, not calibrated predictions or guarantees of safety.

## Features

- 54-question self-reported assessment and ten category scores.
- Findings, prioritized recommendations, and hypothetical improvement simulation.
- Browser dashboard, category charts, printable checklist, and HTML report.
- Flask REST API and SQLite database that stores summaries only.
- Input validation, request-size cap, rate limiting, security response headers, and deletion endpoint.
- Reproducible synthetic dataset generator (1,000 records by default).

## Architecture

```text
User → Questionnaire → Validation → Feature Extraction
     → Category Analysis → Weighted Score → Findings
     → Recommendations → Dashboard / HTML Report
```

Answers are processed for feedback and discarded. Stored data is limited to assessment ID, overall score, risk level, category scores, finding types, and timestamp.

## Technology stack

Python, Flask, SQLite, HTML, CSS, JavaScript, Chart.js, and pytest. This beginner-friendly stack is intended for a local student demonstration, not a production service.

## Project structure

```text
.
├── backend/app.py
├── backend/services/                 # validation, scoring, findings, recommendations, simulator
├── data/                             # synthetic CSV and generator
├── docs/                             # API, report, threat model, test plan, career proof
├── frontend/                         # HTML, CSS, JavaScript dashboard
├── tests/
├── requirements.txt
└── README.md
```

## Installation and local execution

Requires Python 3.10+ and package access to install dependencies.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python data/generate_dataset.py
python -m backend.app
```

Open <http://127.0.0.1:5000>, complete the questionnaire, review the category analysis and recommendations, try the improvement simulator, then open or print the report. On macOS/Linux, activate with `source .venv/bin/activate`.

## API

See [docs/API.md](docs/API.md). Main endpoints include `GET /api/questions`, `POST /api/assessment`, `POST /api/assessment/simulate-improvement`, `GET /api/dashboard/stats`, `GET /api/privacy-checklist`, and `DELETE /api/assessment/{id}`.

## Synthetic dataset

The checked-in CSV contains 1,000 fictional rows. Regenerate it with `python data/generate_dataset.py`; pass a row count such as `python data/generate_dataset.py 2500` to generate more. Synthetic data is demonstration material, not population evidence.

## Testing

```powershell
pytest -q
```

The suite covers scenarios, score boundaries, validation, recommendations, simulation, API behavior, deletion, reports, headers, and database schema. See [docs/TEST_PLAN.md](docs/TEST_PLAN.md). Flask, Flask-Limiter, and pytest must be installed first.

## Security and privacy

The app binds to localhost by default and has no user accounts or authentication. Do not expose it publicly without a security review, authentication, authorization, HTTPS, session protections, and operational safeguards. Do not enter real sensitive values. Local summary records can be deleted through the API.

The demo loads Chart.js from a CDN. For offline use, vendor and pin the chart library locally. The dashboard aggregates assessments submitted to the local instance and does not import the synthetic CSV.

## Privacy by Design

- **Data minimization:** asks whether practices apply, not the sensitive values themselves.
- **Purpose limitation:** assessment feedback and local demo aggregates.
- **Least privilege:** no platform credentials or account access.
- **Privacy by default:** raw answers are not stored.
- **Transparency and user control:** stored fields are documented and summaries can be deleted.
- **Retention limitation:** remove local database files when no longer needed.
- **Secure processing:** validation, parameterized SQL, request limits, and security headers.

## Limitations and future improvements

Self-reported answers may be incomplete. Weights are educational assumptions, not empirically calibrated. Platform settings change; this framework does not inspect real accounts, posts, photos, or EXIF metadata. It is not compliance certification or a compromise prediction.

Defensive future work could include platform-specific checklists, organizational policies, awareness quizzes, maturity scoring, family/teen education, enterprise training, GRC reporting, anonymous trends, better calibration, localization, accessibility, comparison over time, secure client-side assessment, and local-only mode. Do not add invasive monitoring or scraping.

## Documentation and career proof

- [Project report](docs/PROJECT_REPORT.md)
- [Threat model and risk matrix](docs/THREAT_MODEL.md)
- [API guide](docs/API.md)
- [Test plan](docs/TEST_PLAN.md)
- [Screenshot checklist](docs/SCREENSHOTS.md)
- [Resume, LinkedIn, skills, and interview preparation](docs/CAREER_PROOF.md)

## GitHub repository

Suggested name: `Social-Media-Privacy-Risk-Assessment`.

Description: “Privacy-focused cybersecurity framework for assessing social-media exposure, account-security practices, social-engineering risk, digital-footprint risk, and personalized privacy improvements using synthetic/self-reported data.”

Suggested topics: `cybersecurity`, `privacy`, `social-media-privacy`, `privacy-risk`, `security-awareness`, `python`, `flask`, `digital-footprint`, `risk-assessment`, `grc`, `privacy-by-design`, `defensive-security`.

```bash
git init
git add .
git commit -m "Initialize social media privacy risk assessment"
git branch -M main
git remote add origin <repository-url>
git push -u origin main
```

## Ethical disclaimer

For defensive cybersecurity and privacy education only. Use synthetic or voluntarily provided responses. Do not scrape profiles, bypass privacy settings, enumerate accounts, track people, or request passwords or unnecessary sensitive information. The score is guidance, not a guarantee of safety.
