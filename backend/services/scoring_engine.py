"""Weighted risk score and classification."""
from .assessment_engine import calculate_category_scores
DEFAULT_WEIGHTS = {"Profile Exposure":.10,"Personal Information":.15,"Location Exposure":.15,"Content Exposure":.10,"Connection Risk":.10,"Tagging Risk":.05,"Account Security":.15,"Third-Party Apps":.05,"Social Engineering":.10,"Digital Footprint":.05}

def classify_risk(score: int) -> str:
    if score <= 20: return "LOW"
    if score <= 40: return "MODERATE"
    if score <= 70: return "HIGH"
    return "CRITICAL"

def calculate_privacy_risk(responses, weights=None):
    category_scores = calculate_category_scores(responses)
    weights = weights or DEFAULT_WEIGHTS
    if set(weights) != set(category_scores) or any(v < 0 for v in weights.values()) or sum(weights.values()) <= 0:
        raise ValueError("Weights must cover every category with nonnegative values and a positive total.")
    total = sum(category_scores[k] * v for k, v in weights.items()) / sum(weights.values())
    score = round(total)
    return {"overall_score": score, "risk_level": classify_risk(score), "category_scores": category_scores}
