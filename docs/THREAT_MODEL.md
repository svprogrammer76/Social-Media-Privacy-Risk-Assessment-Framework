# Defensive threat model and risk matrix

Scope: a fictional user and local educational application. This is defensive analysis; no attack workflow is included.

| Asset | Threat | Exposure | Potential impact | Existing control | Recommended control |
|---|---|---|---|---|---|
| Account | Account takeover | Reused password or MFA absent | Loss of access, impersonation | Self-report scoring | Unique password, MFA, alerts, session review |
| Identity information | Impersonation | Public birthday, employer, school, family context | Fraudulent contact | Exposure categories | Reduce public fields; verify requests independently |
| Contact information | Phishing/unwanted contact | Public email or phone visibility | Spam, targeted scams | Asks visibility only | Restrict fields; use purpose-specific contact |
| Location privacy | Unwanted profiling | Live location, geotags, travel plans | Routine/absence exposure | Location prompts | Disable unnecessary geotags; delay posts; restrict audience |
| Private content | Unwanted disclosure | Broad audience, tags, old posts | Sensitive disclosure | Tag/history prompts | Enable tag review; review older content |
| Social relationships | Social engineering | Visible friend/follower context | Trusted-person impersonation | Connection hygiene prompts | Verify unknown requests; report suspicious contact |
| Assessment summary | Local unauthorized access | Shared device or exposed host | Score/finding disclosure | Localhost default; no raw answers | Restrict files, delete summaries, require auth before remote access |
| Synthetic dataset | Misinterpretation | Example data lacks context | False conclusions | Synthetic IDs | Label synthetic; do not claim population evidence |

## Illustrative risk matrix

| Scenario | Likelihood | Impact | Rationale |
|---|---|---|---|
| Public phone number | Medium | Medium | May increase unwanted contact; context varies. |
| Real-time location | Medium | High | Can reveal presence or routine. |
| MFA disabled | Medium | High | A stolen password has fewer barriers. |
| Old public posts | Medium | Medium | Earlier context may remain discoverable. |

Ratings are examples. Actual risk depends on context, platform, audience, and threat environment.
