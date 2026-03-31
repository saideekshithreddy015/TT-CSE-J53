import json
import os

def get_icon(category):
    icons = {
        "agriculture": "🌾", "education": "📚", "health": "🏥",
        "women": "👩", "employment": "💼", "housing": "🏠",
        "senior": "👴", "sc": "🌟", "st": "🌟", "disability": "♿",
        "youth": "🏃", "sports": "🏅", "finance": "💰",
        "social": "🤝", "skill": "🛠️", "infrastructure": "🏗️",
        "digital": "💻", "environment": "🌿", "water": "💧",
        "energy": "⚡", "transport": "🚌", "food": "🍚"
    }
    cat = str(category).lower()
    for key, icon in icons.items():
        if key in cat:
            return icon
    return "📋"

def fetch():
    print("📦 Loading dataset via Hugging Face datasets library...")
    try:
        from datasets import load_dataset
        ds = load_dataset("shrijayan/gov_myscheme", split="train")
        print(f"✅ Loaded {len(ds)} schemes!")

        schemes = []
        for i, row in enumerate(ds):
            scheme = {
                "id": i + 1,
                "name": str(row.get("Scheme Name", row.get("name", f"Scheme {i+1}")))[:150],
                "category": str(row.get("Category", row.get("category", "General")))[:50],
                "description": str(row.get("Description", row.get("description", "Government scheme.")))[:300],
                "benefit": str(row.get("Benefits", row.get("Benefit", row.get("benefit", "Government benefit"))))[:200],
                "eligibility": {},
                "apply_link": str(row.get("Official Link", row.get("apply_link", "https://myscheme.gov.in")))[:200],
                "icon": get_icon(row.get("Category", "General"))
            }
            schemes.append(scheme)

        return schemes

    except Exception as e:
        print(f"❌ Error: {e}")
        return []

if __name__ == "__main__":
    schemes = fetch()
    if schemes:
        with open("schemes_data.json", "w", encoding="utf-8") as f:
            json.dump(schemes, f, ensure_ascii=False, indent=2)
        print(f"\n🎉 Saved {len(schemes)} schemes to schemes_data.json!")
    else:
        print("\n⚠️ Could not fetch. Check internet connection.")