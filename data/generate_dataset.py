"""Create 1,000+ fictional assessment rows. No real accounts or personal values."""
import csv, random, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from backend.services.assessment_engine import QUESTIONS
from backend.services.scoring_engine import calculate_privacy_risk

def generate(path=None, count=1000, seed=2026):
    rng=random.Random(seed); path=Path(path or Path(__file__).with_name("social_media_privacy_assessments.csv")); path.parent.mkdir(parents=True,exist_ok=True)
    fields=[q["field"] for q in QUESTIONS]
    with path.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=["profile_id",*fields,"risk_score","risk_level"]);writer.writeheader()
        for i in range(count):
            answers={}
            for q in QUESTIONS:
                field=q["field"]
                if q["kind"]=="frequency": answers[field]=rng.choice(["NEVER","SOMETIMES","OFTEN","NOT SURE"])
                else: answers[field]=rng.choice(["YES","NO","NOT SURE"])
            result=calculate_privacy_risk(answers)
            writer.writerow({"profile_id":f"SYN-{i+1:04}",**answers,"risk_score":result["overall_score"],"risk_level":result["risk_level"]})
    return path
if __name__=="__main__":
    count=int(sys.argv[1]) if len(sys.argv)>1 else 1000
    print(f"Generated {count} synthetic assessments at {generate(count=count)}")
