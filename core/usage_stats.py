import json
import os
from datetime import datetime

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STATS_FILE = BASE_DIR / "data" / "usage_stats.json"

def get_stats():
    if not os.path.exists(STATS_FILE):
        return {"total_analyses": 0, "last_analysis": None, "skill_counts": {}}
    with open(STATS_FILE, "r") as f:
        return json.load(f)

def update_stats(found_skills):
    stats = get_stats()
    stats["total_analyses"] += 1
    stats["last_analysis"] = datetime.now().isoformat()
    
    skill_counts = stats.get("skill_counts", {})
    for skill in found_skills:
        skill_counts[skill] = skill_counts.get(skill, 0) + 1
    stats["skill_counts"] = skill_counts
    
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=4)
