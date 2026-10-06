# Project Report: Social Media Privacy Risk Assessment Framework

## Abstract

This defensive educational framework accepts categorical self-reported practices, extracts features, calculates ten category scores and a weighted overall score, explains findings, recommends mitigations, and simulates hypothetical setting changes. A dashboard, summary-only SQLite storage, HTML report, and synthetic data generator demonstrate an end-to-end privacy engineering workflow without inspecting social-media accounts or requiring sensitive values.

## Introduction and problem statement

People may have secure authentication while publicly revealing contact, relationship, work, education, historical, or location context. That context can increase unwanted profiling, impersonation, or social-engineering exposure. The project turns a privacy checklist into understandable feedback without inspecting a real profile.

## Objectives

Assess ten exposure categories; explain findings; offer defensive recommendations; demonstrate possible effects of settings changes; produce 1,000 synthetic records; provide dashboard/report; minimize retained information.

## Social media privacy, digital footprint, privacy vs security

Privacy concerns collection, sharing, exposure, and use of personal information. Security protects accounts, systems, and information against unauthorized access or misuse. Strong security does not automatically make a profile private. An active digital footprint is content deliberately shared; a passive footprint is information generated or collected during service use depending on context. This project evaluates self-reported practices only. Location disclosures, public profile fields, and older posts can create contextual exposure.

## Method and architecture

The browser renders 55 categorical questions; Flask validates input; feature extraction maps answers to normalized values; category analyzers calculate ten 0–100 scores; weighted scoring calculates overall risk; findings and recommendations explain actions. Flask stores only a summary, dashboard aggregates local summaries, and reports omit raw answers. A seeded generator creates fictitious records.

## Risk scoring

Weights: profile 10%, personal information 15%, location 15%, content 10%, connections 10%, tagging 5%, account security 15%, third-party apps 5%, social engineering 10%, digital footprint 5%. Bands: 0–20 LOW, 21–40 MODERATE, 41–70 HIGH, 71–100 CRITICAL. These are educational assumptions requiring validation before professional use. Scores do not predict compromise.

## Industry relevance

The work demonstrates cybersecurity awareness, privacy engineering, analytics, application security fundamentals, and GRC concepts relevant to cybersecurity analyst, privacy analyst/engineer, GRC analyst, SOC analyst, consultant, IAM analyst, and security-awareness roles.

## Findings, recommendations, simulator

Findings derive from self-reported settings. Recommendations prioritize immediate, important, and good-practice changes. The simulator copies answers and recalculates; it does not change platform settings or claim real-world risk reduction.

## Results

The interface produces an overall score, risk band, category chart, findings, recommendations, dashboard, and printable report. Run `python data/generate_dataset.py` for 1,000 synthetic rows. Output depends on responses and weights.

## Privacy by Design

Data minimization: categorical answers only, then discarded. Purpose limitation: assessment feedback and local demo aggregates. Least privilege: no account credentials or platform access. Privacy by default: no raw-answer persistence. Transparency and control: disclose stored fields and allow deletion. Retention limitation: operators should periodically remove local SQLite data. Secure processing: validation, parameterized SQL, request size/rate limits, and security response headers.

## Testing and security testing

Automated tests cover scoring, boundaries, validation, recommendations, simulation, API, report, database schema, and deletion. Run `pytest -q`. Manual review before remote use should add and verify authentication, authorization, HTTPS, session protections, output encoding, rate controls, secret management, and deletion/backups. No user accounts or sessions exist. The demo loads Chart.js and fonts from CDNs; self-host pinned assets for fully offline use.

## Limitations

Self-report may be incomplete. Weights are not empirically calibrated and do not account for individual threat models. Platform controls change. This tool does not inspect photos, EXIF, posts, or account settings. It is not compliance certification or compromise prediction. Summary-only storage prevents reconstruction of personalized recommendations. Dashboard aggregates only the local instance; synthetic CSVs are not imported automatically.

## Future scope

Platform-specific checklists, configurable organizational policies, awareness quizzes, maturity scoring, family/teen education, enterprise training, GRC reports, anonymous trend analysis, calibrated models, localization, accessibility, trend comparison, secure client-side assessment, and local-only mode. Keep changes consent-based and defensive; no invasive monitoring or scraping.

## Conclusion and learning outcomes

The project demonstrates a useful awareness workflow shaped by privacy-by-design. It translates voluntary categorical answers into explainable risk areas while avoiding collection of sensitive values. Skills include Python/Flask, API design, feature engineering, scoring, SQLite, analytics, synthetic data, testing, threat modeling, and Git documentation.
