"""Generate concise, non-sensitive findings from response flags."""
from .assessment_engine import QUESTIONS, validate_responses

MESSAGES = {
 "phone_public":"Contact information is reported publicly visible.","email_public":"A personal email is reported publicly visible.","birthday_public":"A full birth date is reported publicly visible.","realtime_location":"Real-time location sharing is reported.","travel_plans_public":"Travel plans are shared before/during travel.","mfa_enabled":"Multi-factor authentication is not enabled.","tag_review_enabled":"Tag review is disabled.","third_party_apps_reviewed":"Connected applications have not been reviewed.","verification_codes_shared":"Verification codes have been shared in response to a prompt.","old_posts_reviewed":"Older public posts have not been reviewed.","unknown_connections":"Unknown connection requests are often accepted.","posts_public":"Posts are reported publicly visible.","password_manager":"A password manager is not reported in use.","login_alerts_enabled":"Login alerts are disabled.","geotagging":"Photo geotagging is enabled.","privacy_settings_reviewed":"Privacy settings have not been reviewed recently.",
}
def generate_privacy_findings(responses, scores):
    clean = validate_responses(responses); findings=[]
    for field, message in MESSAGES.items():
        val=clean.get(field)
        risk = (val is False) if field in {"mfa_enabled","tag_review_enabled","third_party_apps_reviewed","old_posts_reviewed","password_manager","login_alerts_enabled","privacy_settings_reviewed"} else (val is True)
        if field == "unknown_connections": risk = val is not None and val >= 2
        if risk: findings.append({"field":field,"category":next(q["category"] for q in QUESTIONS if q["field"]==field),"severity":"HIGH" if field in {"realtime_location","mfa_enabled","verification_codes_shared"} else "MODERATE","description":message})
    findings.sort(key=lambda f: (f["severity"] != "HIGH", -scores["category_scores"].get(f["category"],0)))
    return findings
