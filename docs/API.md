# REST API guide

All requests run against the local Flask server. JSON requests are limited to 64 KB and assessment creation is rate-limited. Authentication is not implemented because this is a localhost student demo. Do not expose it publicly without authentication, authorization, HTTPS, and a deployment security review.

| Method and path | Purpose |
|---|---|
| `GET /api/questions` | Questionnaire schema and accepted answers |
| `POST /api/assessment` | Score answers, return findings/recommendations, save summary only |
| `GET /api/assessment/{id}` | Read summary, categories, findings |
| `GET /api/assessment/{id}/recommendations` | Explain that personal recommendations cannot be reconstructed after answer disposal |
| `POST /api/assessment/simulate-improvement` | Rescore hypothetical changes without saving |
| `GET /api/dashboard/stats` | Local aggregate counts and averages |
| `GET /api/privacy-checklist` | Printable checklist |
| `DELETE /api/assessment/{id}` | Delete summary and associated rows |
| `GET /report/{id}` | Summary-only HTML report |

Example: `{"responses":{"profile_public":"YES","phone_public":"NO","mfa_enabled":"YES"}}`. Unanswered fields are uncertain. Invalid fields or choices return HTTP 400; unknown IDs return 404. SQL is parameterized and report values escaped.

## Database

`assessments(assessment_id, overall_score, risk_level, created_at)`

`category_scores(assessment_id, category, score)`

`findings(assessment_id, category, finding_type, severity, description)`

No questionnaire-answer table exists. Summary data is local and deletable. Personalized recommendation reconstruction is intentionally unavailable after request completion.
