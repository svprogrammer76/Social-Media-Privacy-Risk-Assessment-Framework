"""Validation, feature extraction, and category scoring for self-reported data."""
from typing import Any

CATEGORIES = {
    "Profile Exposure": ["profile_public", "search_engine_visible", "followers_public", "friends_list_public", "discoverable"],
    "Personal Information": ["phone_public", "email_public", "birthday_public", "home_info_public", "workplace_public", "education_public", "relationship_public"],
    "Location Exposure": ["location_public", "realtime_location", "geotagging", "checkins_public", "home_location_clues", "work_location_clues", "travel_plans_public", "vacation_posts_live", "location_patterns_public"],
    "Content Exposure": ["posts_public", "photos_reviewed", "documents_visible", "family_info_in_posts"],
    "Connection Risk": ["unknown_connections", "follower_list_reviewed", "connection_requests_verified"],
    "Tagging Risk": ["anyone_can_tag", "tag_review_enabled", "auto_tagged_posts", "unknown_mentions_allowed"],
    "Account Security": ["mfa_enabled", "unique_password", "password_manager", "login_alerts_enabled", "recovery_reviewed", "sessions_reviewed", "unknown_devices_checked"],
    "Third-Party Apps": ["third_party_apps_reviewed", "unused_apps_removed", "permissions_minimized", "social_login_reviewed"],
    "Social Engineering": ["suspicious_dm_response", "unexpected_links_clicked", "verification_codes_shared", "personal_info_messaged", "impersonation_trusted", "giveaways_checked"],
    "Digital Footprint": ["old_posts_reviewed", "old_accounts_reviewed", "public_comments_reviewed", "profile_history_reviewed", "privacy_settings_reviewed"],
}

# Every field is categorical; never collect the underlying phone, address, password, or location.
QUESTIONS = []
def _q(field, category, prompt, kind="frequency", reverse=False):
    QUESTIONS.append({"field": field, "category": category, "prompt": prompt, "kind": kind, "reverse": reverse})

for item in [
 ("profile_public","Is your profile publicly visible?","boolean",False),
 ("search_engine_visible","Can search engines show your profile?","boolean",False),
 ("followers_public","Are your followers visible to everyone?","boolean",False),
 ("friends_list_public","Is your friends list visible publicly?","boolean",False),
 ("discoverable","Can anyone find your profile using your name?","boolean",False),
 ("phone_public","Is a phone number visible publicly? (Do not enter it.)","boolean",False),
 ("email_public","Is a personal email visible publicly? (Do not enter it.)","boolean",False),
 ("birthday_public","Is your full birth date publicly visible?","boolean",False),
 ("home_info_public","Do public posts reveal home-related information?","boolean",False),
 ("workplace_public","Is your workplace publicly visible?","boolean",False),
 ("education_public","Is your school or education publicly visible?","boolean",False),
 ("relationship_public","Are family or relationship details public?","boolean",False),
 ("location_public","Do you share location information publicly?","boolean",False),
 ("realtime_location","Do you broadcast your current location in real time?","boolean",False),
 ("geotagging","Are photo geotags enabled when posting?","boolean",False),
 ("checkins_public","Are location check-ins public?","boolean",False),
 ("home_location_clues","Could public content reveal where you live?","boolean",False),
 ("work_location_clues","Could public content reveal your regular work location?","boolean",False),
 ("travel_plans_public","Do you post travel plans before or during a trip?","boolean",False),
 ("vacation_posts_live","Do you post vacation photos while still there?","boolean",False),
 ("location_patterns_public","Could posts reveal repeated location patterns?","boolean",False),
 ("posts_public","Are your posts visible to everyone?","boolean",False),
 ("photos_reviewed","Do you check photos for badges, documents, screens, or clues?","boolean",True),
 ("documents_visible","Have public photos included documents or screens?","boolean",False),
 ("family_info_in_posts","Do public photos disclose family information?","boolean",False),
 ("unknown_connections","How often do you accept unknown connection requests?","frequency",False),
 ("follower_list_reviewed","Do you review your followers or friends?","boolean",True),
 ("connection_requests_verified","Do you verify unfamiliar requests?","boolean",True),
 ("anyone_can_tag","Can anyone tag you without approval?","boolean",False),
 ("tag_review_enabled","Is tag review enabled?","boolean",True),
 ("auto_tagged_posts","Do tagged posts appear automatically?","boolean",False),
 ("unknown_mentions_allowed","Can unknown accounts mention you?","boolean",False),
 ("mfa_enabled","Is multi-factor authentication enabled?","boolean",True),
 ("unique_password","Do you use a unique password for this account?","boolean",True),
 ("password_manager","Do you use a password manager?","boolean",True),
 ("login_alerts_enabled","Are login alerts enabled?","boolean",True),
 ("recovery_reviewed","Have you reviewed account recovery options?","boolean",True),
 ("sessions_reviewed","Do you review active sessions?","boolean",True),
 ("unknown_devices_checked","Do you check for unrecognized devices?","boolean",True),
 ("third_party_apps_reviewed","Have you reviewed connected third-party apps?","boolean",True),
 ("unused_apps_removed","Have you removed unused integrations?","boolean",True),
 ("permissions_minimized","Do connected apps have only needed permissions?","boolean",True),
 ("social_login_reviewed","Have you reviewed social sign-in connections?","boolean",True),
 ("suspicious_dm_response","How often do you respond to suspicious messages?","frequency",False),
 ("unexpected_links_clicked","How often do you click unexpected links?","frequency",False),
 ("verification_codes_shared","Have you shared a verification code with someone?","boolean",False),
 ("personal_info_messaged","Do you send personal information in messages?","boolean",False),
 ("impersonation_trusted","Have you trusted an account without verifying its identity?","boolean",False),
 ("giveaways_checked","Do you verify giveaways before engaging?","boolean",True),
 ("old_posts_reviewed","Have you reviewed older public posts?","boolean",True),
 ("old_accounts_reviewed","Have you reviewed unused/old accounts?","boolean",True),
 ("public_comments_reviewed","Have you reviewed old public comments?","boolean",True),
 ("profile_history_reviewed","Have you reviewed profile history?","boolean",True),
 ("privacy_settings_reviewed","Have you checked privacy settings in the last 6 months?","boolean",True),
]:
    field, prompt, kind, reverse = item
    cat = next(k for k, fields in CATEGORIES.items() if field in fields)
    _q(field, cat, prompt, kind, reverse)

BOOL_FIELDS = {q["field"] for q in QUESTIONS if q["kind"] == "boolean"}
FREQ_FIELDS = {q["field"] for q in QUESTIONS if q["kind"] == "frequency"}
TRUE = {True, "YES", "TRUE", "1", 1}
FALSE = {False, "NO", "FALSE", "0", 0}
FREQUENCY = {"NEVER": 0, "NOT SURE": 1, "SOMETIMES": 2, "OFTEN": 3, "ALWAYS": 3}

def validate_responses(data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(data, dict): raise ValueError("Responses must be a JSON object.")
    unknown = set(data) - BOOL_FIELDS - FREQ_FIELDS
    if unknown: raise ValueError("Unknown response fields: " + ", ".join(sorted(unknown)))
    clean = {}
    for key, value in data.items():
        if key in BOOL_FIELDS:
            if value in TRUE: clean[key] = True
            elif value in FALSE: clean[key] = False
            elif isinstance(value, str) and value.upper() == "NOT SURE": clean[key] = None
            else: raise ValueError(f"{key} must be YES, NO, or NOT SURE.")
        else:
            if not isinstance(value, str) or value.upper() not in FREQUENCY: raise ValueError(f"{key} must be NEVER, SOMETIMES, OFTEN, or NOT SURE.")
            clean[key] = FREQUENCY[value.upper()]
    return clean

def extract_privacy_features(responses: dict[str, Any]) -> dict[str, float]:
    clean = validate_responses(responses)
    result = {}
    for q in QUESTIONS:
        key = q["field"]
        if key not in clean: result[key] = 0.5; continue
        val = clean[key]
        if q["kind"] == "frequency": result[key] = val / 3
        elif val is None: result[key] = 0.5
        else: result[key] = (0 if val else 1) if q["reverse"] else (1 if val else 0)
    return result

def calculate_category_scores(responses: dict[str, Any]) -> dict[str, int]:
    features = extract_privacy_features(responses)
    return {category: round(100 * sum(features[f] for f in fields) / len(fields)) for category, fields in CATEGORIES.items()}
