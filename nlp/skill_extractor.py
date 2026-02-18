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
    
    skills = []
    with open(SKILL_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # Ignore comments and empty lines
            if line and not line.startswith("#"):
                skills.append(line.lower())
    return skills

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

    # Create a regex pattern to match skills with word boundaries
    # We escape the skill to handle special characters, and use \b for boundaries
    # However, some skills might contain special characters that \b doesn't work well with (e.g., C++),
    # so we need a more robust approach or just stick to \b for now as a significant improvement.
    # For "C++", \b matches the start but not necessarily the end if followed by space.
    # Let's use a robust pattern: (?<!\w)skill(?!\w) roughly.
    
    import re
    
    for skill in SKILLS:
        # Escape skill for regex safety
        skill_pattern = re.escape(skill)
        
        # Use lookbehind and lookahead to ensure we are not inside a word
        # This is equivalent to \b but safer for some edge cases where \b might not behave as expected with non-alphanumerics
        # But for 'C++', \bC\+\+\b might fail because + is not a word character.
        # Let's try to be smart. If skill starts/ends with word char, use \b.
        
        pattern = r""
        
        # Start boundary
        if skill[0].isalnum() or skill[0] == '_':
            pattern += r"\b"
        
        pattern += skill_pattern
        
        # End boundary - C++ is a common issue. '+' is not alnum.
        # If the skill ends with a symbol, we might just want to ensure it's not followed by a word char immediately?
        # Or just rely on space/punctuation.
        if skill[-1].isalnum() or skill[-1] == '_':
            pattern += r"\b"
            
        # Compile and search
        if re.search(pattern, text, re.IGNORECASE):
            found_skills.append(skill)

    return sorted(set(found_skills))
