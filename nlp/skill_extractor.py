import os
from pathlib import Path

# Use absolute path relative to this file to locate skills_list.txt
# This ensures it works regardless of where the script is called from
BASE_DIR = Path(__file__).resolve().parent.parent
SKILL_FILE = BASE_DIR / "data" / "skills_list.txt"

def load_skills():
    """Lods skills from the skills_list.txt file."""
    if not SKILL_FILE.exists():
        print(f"Warning: Skill file not found at {SKILL_FILE}")
        return []
    
    with open(SKILL_FILE, "r", encoding="utf-8") as f:
        # Read lines, strip whitespace, and convert to lowercase
        return [skill.strip().lower() for skill in f.readlines() if skill.strip()]

# Load skills only once when module is imported
SKILLS = load_skills()

def extract_skills(text: str) -> list[str]:
    """
    Extracts skills present in the given text using dictionary matching.
    Input text should ideally be processed/cleaned, but the logic handles basics.
    """
    if not text or not isinstance(text, str):
        return []
        
    text = text.lower()
    found_skills = []

    for skill in SKILLS:
        # Basic substring consistency check
        # Note: This might match 'java' in 'javascript', but for now it's simple dictionary matching
        # A more robust approach would be token-based or regex with word boundaries,
        # but per Phase 3 requirements, we stick to simple matching first.
        
        # Improvement: Check for exact word matches for short skills to avoid false positives (e.g. "go" in "good")
        # For this phase, we'll stick to the requested logic but maybe add simple boundary checks if needed later.
        if skill in text:
            found_skills.append(skill)

    return sorted(set(found_skills))
