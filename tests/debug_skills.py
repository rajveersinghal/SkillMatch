import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nlp.skill_extractor import SKILLS, extract_skills

def debug_skills():
    print(f"Total skills loaded: {len(SKILLS)}")
    print("First 10 skills:")
    print(SKILLS[:10])
    
    # Check for specific artifacts
    artifacts = [s for s in SKILLS if s.startswith("#") or "role" in s]
    if artifacts:
        print("\nFound artifacts (headers/comments) in SKILLS:")
        for a in artifacts:
            print(f"- '{a}'")
    else:
        print("\nNo artifacts found in SKILLS.")

    # Test extraction again with a broader text to see if it matches headers
    text = "I am a Data Scientist with Python skills."
    extracted = extract_skills(text)
    print(f"\nExtracted from '{text}': {extracted}")

if __name__ == "__main__":
    debug_skills()
