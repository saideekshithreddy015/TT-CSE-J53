from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.schemes import match_schemes, schemes as local_schemes
import json, os

app = FastAPI(title="Govt Scheme Recommender")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load schemes — use fetched data if available, else use local
def load_schemes():
    if os.path.exists("schemes_data.json"):
        with open("schemes_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            print(f"✅ Loaded {len(data)} schemes from schemes_data.json")
            return data
    print(f"⚠️  Using {len(local_schemes)} local schemes")
    return local_schemes

all_schemes = load_schemes()

class UserProfile(BaseModel):
    age: int
    gender: str
    annual_income: int
    occupation: str
    category: str

def smart_match(profile: UserProfile):
    matched = []
    for scheme in all_schemes:
        e = scheme.get("eligibility", {})
        if "min_age"    in e and profile.age < e["min_age"]:                continue
        if "max_age"    in e and profile.age > e["max_age"]:                continue
        if "max_income" in e and profile.annual_income > e["max_income"]:   continue
        if "gender"     in e and profile.gender.lower() not in e["gender"]: continue
        if "occupation" in e and profile.occupation.lower() not in e["occupation"]: continue
        if "category"   in e and profile.category.upper() not in e["category"]:    continue
        matched.append(scheme)
    return matched

@app.post("/recommend")
def recommend(profile: UserProfile):
    results = smart_match(profile)
    return {"total": len(results), "schemes": results}

@app.get("/")
def root():
    return {"message": f"Govt Scheme Recommender — {len(all_schemes)} schemes loaded"}
