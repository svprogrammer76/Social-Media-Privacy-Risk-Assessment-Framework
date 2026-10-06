"""Flask application. Assessment answers are processed in memory and never persisted."""
import json, os, sqlite3, uuid
from datetime import datetime, timezone
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory, make_response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from backend.services.assessment_engine import QUESTIONS, validate_responses
from backend.services.scoring_engine import calculate_privacy_risk
from backend.services.findings_engine import generate_privacy_findings
from backend.services.recommendation_engine import generate_recommendations
from backend.services.improvement_simulator import simulate_improvement

ROOT=Path(__file__).resolve().parents[1]
app=Flask(__name__, static_folder="../frontend", static_url_path="")
app.config["MAX_CONTENT_LENGTH"]=64*1024
limiter=Limiter(get_remote_address,app=app,default_limits=["120 per hour"])
DB_PATH=Path(os.environ.get("ASSESSMENT_DB",ROOT/"data"/"assessments.sqlite3"))

def init_db():
    DB_PATH.parent.mkdir(parents=True,exist_ok=True)
    with sqlite3.connect(DB_PATH) as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS assessments (assessment_id TEXT PRIMARY KEY, overall_score INTEGER NOT NULL, risk_level TEXT NOT NULL, created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS category_scores (assessment_id TEXT NOT NULL, category TEXT NOT NULL, score INTEGER NOT NULL, PRIMARY KEY(assessment_id,category), FOREIGN KEY(assessment_id) REFERENCES assessments(assessment_id) ON DELETE CASCADE);
        CREATE TABLE IF NOT EXISTS findings (assessment_id TEXT NOT NULL, category TEXT NOT NULL, finding_type TEXT NOT NULL, severity TEXT NOT NULL, description TEXT NOT NULL, FOREIGN KEY(assessment_id) REFERENCES assessments(assessment_id) ON DELETE CASCADE);
        """)

def save_summary(result, findings):
    # Strict allowlist: responses and personal data are never written.
    aid=str(uuid.uuid4()); created=datetime.now(timezone.utc).isoformat()
    with sqlite3.connect(DB_PATH) as db:
        db.execute("INSERT INTO assessments VALUES (?,?,?,?)",(aid,result["overall_score"],result["risk_level"],created))
        db.executemany("INSERT INTO category_scores VALUES (?,?,?)",[(aid,k,v) for k,v in result["category_scores"].items()])
        db.executemany("INSERT INTO findings VALUES (?,?,?,?,?)",[(aid,f["category"],f["field"],f["severity"],f["description"]) for f in findings])
    return aid,created

@app.after_request
def security_headers(response):
    response.headers["X-Content-Type-Options"]="nosniff"; response.headers["X-Frame-Options"]="DENY"; response.headers["Referrer-Policy"]="no-referrer"; response.headers["Content-Security-Policy"]="default-src 'self'; script-src 'self' https://cdn.jsdelivr.net; style-src 'self'; img-src 'self' data:; connect-src 'self'"
    return response

@app.get("/")
def home(): return send_from_directory(app.static_folder,"index.html")
@app.get("/api/privacy-checklist")
def checklist(): return jsonify({"checklist":["Review profile visibility","Hide unnecessary contact information","Review birth-date visibility","Review location sharing","Avoid unnecessary real-time location posts","Review tagging permissions","Review followers/friends","Verify unfamiliar requests","Enable MFA","Enable login alerts","Review active sessions","Review connected apps","Remove unused integrations","Review old public posts","Review photo privacy","Be cautious with unexpected links","Never share verification codes","Review privacy settings periodically"]})
@app.get("/api/questions")
def questions(): return jsonify({"questions":QUESTIONS})
@app.post("/api/assessment")
@limiter.limit("20 per hour")
def assessment():
    try:
        payload=request.get_json(force=True); responses=validate_responses(payload.get("responses",payload))
        result=calculate_privacy_risk(responses); findings=generate_privacy_findings(responses,result); recs=generate_recommendations(responses,result)
        aid,created=save_summary(result,findings)
        return jsonify({"assessment_id":aid,"created_at":created,**result,"findings":findings,"recommendations":recs,"privacy_note":"Only risk summary, category scores, and finding types are retained; questionnaire responses are discarded."}),201
    except (ValueError,TypeError,AttributeError) as e: return jsonify({"error":str(e)}),400
@app.get("/api/assessment/<assessment_id>")
def get_assessment(assessment_id):
    with sqlite3.connect(DB_PATH) as db:
        row=db.execute("SELECT overall_score,risk_level,created_at FROM assessments WHERE assessment_id=?",(assessment_id,)).fetchone()
        if not row:return jsonify({"error":"Assessment not found"}),404
        cats=db.execute("SELECT category,score FROM category_scores WHERE assessment_id=?",(assessment_id,)).fetchall()
        findings=db.execute("SELECT category,finding_type,severity,description FROM findings WHERE assessment_id=?",(assessment_id,)).fetchall()
    return jsonify({"assessment_id":assessment_id,"overall_score":row[0],"risk_level":row[1],"created_at":row[2],"category_scores":dict(cats),"findings":[{"category":x[0],"field":x[1],"severity":x[2],"description":x[3]} for x in findings]})
@app.get("/api/assessment/<assessment_id>/recommendations")
def assessment_recommendations(assessment_id):
    from backend.services.recommendation_engine import TEXT
    with sqlite3.connect(DB_PATH) as db:
        exists=db.execute("SELECT 1 FROM assessments WHERE assessment_id=?",(assessment_id,)).fetchone()
        rows=db.execute("SELECT finding_type,severity,description FROM findings WHERE assessment_id=?",(assessment_id,)).fetchall()
    if not exists:return jsonify({"error":"Assessment not found"}),404
    recommendations=[]
    for field,severity,description in rows:
        priority="IMMEDIATE" if field in {"verification_codes_shared","realtime_location","mfa_enabled"} else "IMPORTANT" if severity=="HIGH" else "GOOD PRACTICE"
        recommendations.append({"field":field,"risk":description,"priority":priority,"recommendation":TEXT.get(field,"Review this setting and reduce unnecessary public exposure.")})
    return jsonify({"recommendations":recommendations,"note":"Generated from stored finding types; original responses are intentionally not retained."})
@app.post("/api/assessment/simulate-improvement")
def simulate():
    try:
        p=request.get_json(force=True); result=simulate_improvement(validate_responses(p.get("responses",{})),validate_responses(p.get("changes",{})))
        return jsonify(result)
    except (ValueError,TypeError,AttributeError) as e:return jsonify({"error":str(e)}),400
@app.get("/api/dashboard/stats")
def stats():
    with sqlite3.connect(DB_PATH) as db:
        n,avg=db.execute("SELECT COUNT(*),COALESCE(AVG(overall_score),0) FROM assessments").fetchone()
        levels=dict(db.execute("SELECT risk_level,COUNT(*) FROM assessments GROUP BY risk_level").fetchall())
        cats=dict(db.execute("SELECT category,ROUND(AVG(score)) FROM category_scores GROUP BY category").fetchall())
        tops=db.execute("SELECT finding_type,COUNT(*) c FROM findings GROUP BY finding_type ORDER BY c DESC LIMIT 5").fetchall()
    return jsonify({"assessments":n,"average_risk":round(avg),"risk_distribution":levels,"category_averages":cats,"top_findings":[{"type":x,"count":y} for x,y in tops],"data_scope":"Aggregates include only assessments submitted to this local demo instance."})
@app.delete("/api/assessment/<assessment_id>")
def delete_assessment(assessment_id):
    with sqlite3.connect(DB_PATH) as db:
        db.execute("DELETE FROM category_scores WHERE assessment_id=?",(assessment_id,))
        db.execute("DELETE FROM findings WHERE assessment_id=?",(assessment_id,))
        cur=db.execute("DELETE FROM assessments WHERE assessment_id=?",(assessment_id,))
    return (jsonify({"deleted":True}),200) if cur.rowcount else (jsonify({"error":"Assessment not found"}),404)
@app.get("/report/<assessment_id>")
def report(assessment_id):
    with sqlite3.connect(DB_PATH) as db:
        row=db.execute("SELECT overall_score,risk_level,created_at FROM assessments WHERE assessment_id=?",(assessment_id,)).fetchone()
        cats=db.execute("SELECT category,score FROM category_scores WHERE assessment_id=?",(assessment_id,)).fetchall()
        fs=db.execute("SELECT category,severity,description FROM findings WHERE assessment_id=?",(assessment_id,)).fetchall()
    if not row:return "Assessment not found",404
    # All dynamic text is escaped by JSON encoding and rendered as text client-side in UI; HTML report uses escaped values.
    from html import escape
    body=f"<h1>Privacy Risk Assessment</h1><p>ID: {escape(assessment_id)}</p><p>Date: {escape(row[2])}</p><h2>{row[0]}/100 — {escape(row[1])}</h2><h3>Category scores</h3><ul>"+"".join(f"<li>{escape(c)}: {s}/100</li>" for c,s in cats)+"</ul><h3>Findings</h3><ul>"+"".join(f"<li>{escape(sev)} — {escape(desc)}</li>" for _,sev,desc in fs)+"</ul><p>Educational framework, not a guarantee of safety. This report contains no questionnaire answers.</p>"
    return make_response("<!doctype html><meta charset='utf-8'><title>Privacy Assessment Report</title><style>body{font:16px system-ui;max-width:850px;margin:3rem auto;padding:1rem;color:#182435}li{margin:.5rem}</style>"+body)

if __name__=="__main__":
    init_db(); app.run(host="127.0.0.1",port=int(os.environ.get("PORT","5000")),debug=False)
