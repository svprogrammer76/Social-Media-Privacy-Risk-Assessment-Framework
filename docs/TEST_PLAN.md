# Test plan and execution record

The automated suite is in `tests/test_assessment.py`. It includes over 30 test cases (including parameterized individual-field scenarios). Run `pytest -q` from the repository root after installing `requirements.txt`.

| ID | Scenario and synthetic input | Expected result | Actual result |
|---|---|---|---|
| T01 | Fully private answers | LOW; category scores near zero | Implemented; suite not executable in supplied runtime (Flask/pytest unavailable) |
| T02 | Fully exposed synthetic answers | HIGH or CRITICAL | Implemented; suite not executable in supplied runtime |
| T03 | Phone visibility YES | Personal-info exposure increases | Implemented; suite not executable in supplied runtime |
| T04 | Email visibility YES | Personal-info exposure increases | Implemented; suite not executable in supplied runtime |
| T05 | Full birthday visibility YES | Personal-info exposure increases | Implemented; suite not executable in supplied runtime |
| T06 | Public location YES | Location score increases | Implemented; suite not executable in supplied runtime |
| T07 | Real-time location YES | Finding and increased location risk | Implemented; suite not executable in supplied runtime |
| T08 | Travel plans YES | Location score increases | Implemented; suite not executable in supplied runtime |
| T09 | Workplace visibility YES | Personal-info score increases | Implemented; suite not executable in supplied runtime |
| T10 | Education visibility YES | Personal-info score increases | Implemented; suite not executable in supplied runtime |
| T11 | Public posts YES | Content score increases | Implemented; suite not executable in supplied runtime |
| T12 | Unknown requests OFTEN | Connection score increases | Implemented; suite not executable in supplied runtime |
| T13 | Tag review NO | Tagging finding appears | Implemented; suite not executable in supplied runtime |
| T14 | MFA NO | Account-security risk increases | Implemented; suite not executable in supplied runtime |
| T15 | Login alerts NO | Account-security risk increases | Implemented; suite not executable in supplied runtime |
| T16 | Password manager NO | Account-security risk increases | Implemented; suite not executable in supplied runtime |
| T17 | Third-party review NO | Third-party finding appears | Implemented; suite not executable in supplied runtime |
| T18 | Suspicious-message response OFTEN | Social-engineering score increases | Implemented; suite not executable in supplied runtime |
| T19 | Unexpected links OFTEN | Social-engineering score increases | Implemented; suite not executable in supplied runtime |
| T20 | Old posts review NO | Digital-footprint finding appears | Implemented; suite not executable in supplied runtime |
| T21 | Calculate all ten categories | All scores are within 0–100 | Implemented; suite not executable in supplied runtime |
| T22 | Default weighted scoring | Weighted score and level returned | Implemented; suite not executable in supplied runtime |
| T23 | Boundary score 20 | LOW | Implemented; suite not executable in supplied runtime |
| T24 | Boundary score 40 | MODERATE | Implemented; suite not executable in supplied runtime |
| T25 | Boundary score 70 | HIGH | Implemented; suite not executable in supplied runtime |
| T26 | Exposure-heavy answer set | Recommendations generated | Implemented; suite not executable in supplied runtime |
| T27 | Protective changes in simulator | Simulated score decreases; clearly labeled | Implemented; suite not executable in supplied runtime |
| T28 | Save assessment | Summary records can be read back | Implemented; suite not executable in supplied runtime |
| T29 | Inspect SQLite schema | No sensitive response columns/table | Implemented; suite not executable in supplied runtime |
| T30 | Generate report | HTML summary contains no questionnaire values | Implemented; suite not executable in supplied runtime |
| T31 | Unknown answer field | HTTP 400 / validation error | Implemented; suite not executable in supplied runtime |
| T32 | Invalid answer enum | HTTP 400 / validation error | Implemented; suite not executable in supplied runtime |
| T33 | Delete assessment | Summary and child rows removed | Implemented; suite not executable in supplied runtime |
| T34 | Report ID contains markup | HTML-escaped identifier; script not executed | Implemented; suite not executable in supplied runtime |
| T35 | Security response headers | `X-Frame-Options: DENY` and nosniff | Implemented; suite not executable in supplied runtime |

The runtime-independent source compilation (`compileall`) and direct scoring/data checks succeeded. Full actual pass/fail results require installing Flask, Flask-Limiter, and pytest in a Python environment with package access.
