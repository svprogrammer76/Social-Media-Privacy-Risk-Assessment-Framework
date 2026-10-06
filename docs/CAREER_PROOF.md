# Career and interview proof

## Resume bullets

- Built a privacy-focused cybersecurity assessment framework in Python and Flask, mapping 55 self-reported controls into ten explainable risk categories and a configurable 0–100 score.
- Implemented privacy-by-design data handling with validation, summary-only SQLite storage, deletion, rate limits, response headers, and a reproducible 1,000-record synthetic dataset.
- Delivered a dashboard, personalized recommendations, printable reports, improvement simulator, threat model, and automated tests for security awareness and GRC review.

## Two-line project description

A defensive privacy-risk framework scoring social-media exposure, account security, social-engineering awareness, and digital-footprint practices from voluntary categorical responses.
Built with Python, Flask, SQLite, HTML/CSS/JavaScript, and synthetic data; includes findings, recommendations, analytics, and a what-if simulator.

## LinkedIn project description

Designed and implemented a defensive educational application for reviewing social-media privacy practices without accessing or scraping accounts. The Python/Flask application processes 55 categorical self-reported questions across profile exposure, personal information, location, content, connections, tagging, account security, third-party apps, social engineering, and digital footprint. It generates configurable category and overall scores, prioritized recommendations, local analytics, a printable report, and improvement simulation. Privacy-by-design controls include data minimization, no contact values/passwords/exact locations, summary-only storage, deletion, validation, and synthetic data generation. Demonstrates cybersecurity, privacy risk assessment, digital-footprint analysis, Python, analytics, security awareness, and GRC fundamentals.

## Technical skills

Cybersecurity; privacy risk assessment; privacy by design; digital-footprint analysis; social-engineering awareness; risk scoring; Python; Flask APIs; SQLite; input validation; analytics; synthetic data; HTML/CSS/JavaScript; Chart.js; pytest; threat modeling; GRC; Git/GitHub.

## GitHub description

Privacy-focused cybersecurity framework for assessing social-media exposure, account-security practices, social-engineering risk, digital-footprint risk, and personalized privacy improvements using synthetic/self-reported data.

## Interview preparation — 10 questions and answers

1. **Explain your project.** — I built a defensive privacy assessment tool. It asks categorical questions about settings and habits, validates answers, scores ten categories, and provides findings, recommendations, a dashboard, and a what-if simulation. It never logs into or scrapes an account and does not ask for actual personal values.
2. **What is privacy versus security?** — Privacy concerns how information is collected, shared, exposed, and used. Security protects accounts and information from unauthorized access. A strong password can protect an account while public details still create privacy exposure.
3. **What is a digital footprint?** — It is information associated with online activity. An active footprint is deliberately shared content; a passive footprint can be generated or collected in a service context. My tool assesses self-reported practices, not actual profiles.
4. **How can oversharing relate to social engineering?** — Public work, school, travel, or family context can make impersonation more believable. The tool flags exposure and recommends verification but does not create attack messages.
5. **How does risk scoring work?** — Answers map to normalized exposure features, are averaged by category, then combined with configurable weights. Higher scores mean higher assessed exposure. Weights and bands are educational, not calibrated predictions.
6. **How did you apply data minimization?** — The questionnaire asks whether information is visible, never the value itself. Responses are used for feedback and discarded; only a score summary, category scores, and finding types are persisted.
7. **Why recommend MFA?** — MFA adds a verification factor, so a password alone may not be enough to sign in. I assess whether it is reported enabled while treating account security as related to, but distinct from, privacy.
8. **What is third-party app risk?** — Connected apps may retain permissions no longer needed. Least privilege means reviewing integrations and revoking unused or excessive access. The tool never connects to those apps.
9. **How does the project follow Privacy by Design?** — It minimizes inputs, limits purpose, defaults to no raw-answer retention, explains stored fields, supports deletion, and avoids credentials and platform access.
10. **How did you test it?** — Automated tests cover score bands, category bounds, validation, safer/riskier profiles, simulation, API behavior, report output, deletion, headers, and schema checks that ensure sensitive response fields are not stored.
