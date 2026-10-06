import csv
import pytest
from backend.services.assessment_engine import QUESTIONS, CATEGORIES, calculate_category_scores, validate_responses
from backend.services.scoring_engine import calculate_privacy_risk, classify_risk
from backend.services.findings_engine import generate_privacy_findings
from backend.services.recommendation_engine import generate_recommendations
from backend.services.improvement_simulator import simulate_improvement

def safe(): return {q["field"]:("YES" if q["reverse"] else "NO") if q["kind"]=="boolean" else "NEVER" for q in QUESTIONS}
def exposed(): return {q["field"]:("NO" if q["reverse"] else "YES") if q["kind"]=="boolean" else "OFTEN" for q in QUESTIONS}

@pytest.mark.parametrize("field",["profile_public","phone_public","email_public","birthday_public","location_public","realtime_location","travel_plans_public","workplace_public","education_public","posts_public","unknown_connections","anyone_can_tag","mfa_enabled","login_alerts_enabled","password_manager","third_party_apps_reviewed","suspicious_dm_response","unexpected_links_clicked","old_posts_reviewed","privacy_settings_reviewed"])
def test_individual_response_changes_risk(field):
    base=safe(); changed=dict(base); changed[field]="NO" if field in {"mfa_enabled","login_alerts_enabled","password_manager","third_party_apps_reviewed","old_posts_reviewed","privacy_settings_reviewed"} else "OFTEN" if field=="unknown_connections" else "YES"
    assert calculate_privacy_risk(changed)["overall_score"] >= calculate_privacy_risk(base)["overall_score"]

def test_fully_private_profile_low(): assert calculate_privacy_risk(safe())["risk_level"]=="LOW"
def test_fully_public_synthetic_profile_high(): assert calculate_privacy_risk(exposed())["risk_level"] in {"HIGH","CRITICAL"}
def test_categories_all_present(): assert set(calculate_category_scores(safe()))==set(CATEGORIES)
def test_category_score_range(): assert all(0<=x<=100 for x in calculate_category_scores(exposed()).values())
def test_risk_boundaries(): assert [classify_risk(x) for x in [20,21,40,41,70,71]]==["LOW","MODERATE","MODERATE","HIGH","HIGH","CRITICAL"]
def test_score_boundary_20(): assert classify_risk(20)=="LOW"
def test_score_boundary_40(): assert classify_risk(40)=="MODERATE"
def test_score_boundary_70(): assert classify_risk(70)=="HIGH"
def test_custom_weights_validation():
    with pytest.raises(ValueError):calculate_privacy_risk(safe(),{"bad":1})
def test_recommendations_generated(): assert generate_recommendations(exposed(),calculate_privacy_risk(exposed()))
def test_simulator_reduces_risk():
    ans=exposed(); out=simulate_improvement(ans,{k:"NO" for k in ["phone_public","location_public","realtime_location","travel_plans_public"]}|{k:"YES" for k in ["mfa_enabled","tag_review_enabled","login_alerts_enabled","third_party_apps_reviewed"]}); assert out["risk_reduction"]>=0 and out["simulated_only"]
def test_bad_field_rejected():
    with pytest.raises(ValueError):validate_responses({"password":"example"})
def test_bad_enum_rejected():
    with pytest.raises(ValueError):validate_responses({"mfa_enabled":"MAYBE"})
def test_questions_exceed_40(): assert len(QUESTIONS)>=40

def test_api_assessment_and_report(client):
    r=client.post('/api/assessment',json={"responses":exposed()}); assert r.status_code==201
    aid=r.json["assessment_id"]; assert client.get(f'/report/{aid}').status_code==200
def test_api_validation(client): assert client.post('/api/assessment',json={"responses":{"password":"secret"}}).status_code==400
def test_database_does_not_store_responses(client):
    client.post('/api/assessment',json={"responses":{"phone_public":"YES","mfa_enabled":"NO"}})
    import backend.app as mod,sqlite3
    with sqlite3.connect(mod.DB_PATH) as db:
        tables={x[0] for x in db.execute("select name from sqlite_master where type='table'")}; cols={t:[x[1] for x in db.execute(f"pragma table_info({t})")] for t in tables}
    assert not any(x in " ".join(sum(cols.values(),[])).lower() for x in ["phone","email","password","address","location","birth_date","response"])
def test_get_saved_summary(client):
    r=client.post('/api/assessment',json={"responses":safe()}); assert client.get('/api/assessment/'+r.json['assessment_id']).status_code==200
def test_checklist_endpoint(client): assert len(client.get('/api/privacy-checklist').json["checklist"])>=15
def test_security_headers(client): assert client.get('/api/questions').headers.get('X-Frame-Options')=='DENY'
def test_delete_summary(client):
    r=client.post('/api/assessment',json={"responses":safe()}); aid=r.json['assessment_id']; assert client.delete('/api/assessment/'+aid).status_code==200
def test_dashboard_stats(client): assert client.get('/api/dashboard/stats').status_code==200
def test_frequency_validation():
    with pytest.raises(ValueError):validate_responses({"unknown_connections":"MAYBE"})
def test_report_does_not_include_sensitive_values(client):
    r=client.post('/api/assessment',json={"responses":{"phone_public":"YES"}}); report=client.get('/report/'+r.json['assessment_id']).get_data(as_text=True); assert "phone_public" not in report
def test_report_escapes_untrusted_assessment_id(client):
    import backend.app as mod,sqlite3
    from urllib.parse import quote
    hostile="<script>alert(1)</script>"
    with sqlite3.connect(mod.DB_PATH) as db: db.execute("INSERT INTO assessments VALUES (?,?,?,?)",(hostile,1,"LOW","today"))
    response=client.get('/report/'+quote(hostile,safe=''))
    assert response.status_code==200 and '&lt;script&gt;' in response.get_data(as_text=True)
def test_weights_sum_normalized(): assert calculate_privacy_risk(safe(),{k:2 for k in CATEGORIES})["overall_score"]<=20
def test_dataset_is_reproducible(tmp_path):
    from data.generate_dataset import generate
    p=generate(tmp_path/"a.csv",10,1); rows=list(csv.DictReader(p.open())); assert len(rows)==10 and rows[0]["profile_id"]=="SYN-0001"
