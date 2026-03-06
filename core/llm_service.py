import google.generativeai as genai
import os
from typing import Dict, Any

class StrategicNarrativeService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None

    def _get_fallback_insights(self, match_score: float, missing_skills: list) -> Dict[str, Any]:
        """Generates simple, encouraging, and easy-to-understand feedback for internships."""
        safe_missing = missing_skills[:3] if missing_skills else []
        
        # 1. Generate a robust Strategic Narrative
        if match_score >= 80:
            if safe_missing:
                narrative = f"Great Fit ({match_score:.0f}%!)\n\nYour skills match very well with this internship. You already have a strong foundation, but learning a bit more about {', '.join(safe_missing)} will make your resume stand out even more."
                advice = f"Try to add any small projects or coursework related to {safe_missing[0]} to your resume."
            else:
                narrative = f"Perfect Fit ({match_score:.0f}%!)\n\nYour resume covers all the main requirements for this internship. You look like a great candidate!"
                advice = "Your skills match perfectly! Make sure your resume clearly highlights your best projects and what you learned from them."
        elif match_score >= 50:
            missing_str = ', '.join(safe_missing) if safe_missing else 'some key skills'
            narrative = f"Good Fit ({match_score:.0f}%)\n\nYou have many of the right skills for this role! However, since this internship asks for {missing_str}, spending some time learning these will help you a lot."
            advice = f"Consider doing a quick weekend project using {safe_missing[0] if safe_missing else 'the required tools'} and adding it to your resume."
        else:
            missing_str = ', '.join(safe_missing) if safe_missing else 'the main tools'
            narrative = f"Room to Grow ({match_score:.0f}%)\n\nThis internship wants experience with things like {missing_str}. Right now, your resume doesn't quite match, but that's okay! It just means you have some exciting things to learn."
            advice = f"Don't worry about the low score! Start by taking a beginner tutorial on {safe_missing[0] if safe_missing else 'the core skills'} and build a simple project to show you are eager to learn."

        # 2. Generate profound Interview Questions
        questions = []
        if len(safe_missing) >= 1:
            skill = safe_missing[0]
            questions.append(f"Have you ever used or learned about {skill}? If not, how would you go about learning it in your first week?")
        if len(safe_missing) >= 2:
            skill = safe_missing[1]
            questions.append(f"Tell me about a time you had to learn a new tool for a project. Could you do the same for {skill}?")
        
        # General profound questions to fill the gap
        if len(questions) < 3:
            questions.append("Can you tell me about a coding project you are really proud of?")
        if len(questions) < 3:
            questions.append("If you get stuck on a coding bug, what steps do you take to figure it out?")

        return {
            "status": "success",
            "raw_narrative": narrative,
            "interview_questions": questions[:3],
            "resume_advice": advice,
            "recommended_role": "Junior Machine Learning Engineer" if match_score >= 50 else "Data Analyst/Python Developer Intern"
        }

    async def generate_insights(self, resume_text: str, jd_text: str, match_score: float, missing_skills: list) -> Dict[str, Any]:
        """
        Generates structured qualitative insights using Google Gemini.
        """
        if not self.model:
            return self._get_fallback_insights(match_score, missing_skills)

        prompt = f"""
        As a helpful, encouraging mentor, analyze this internship match:
        Match Score: {match_score}%
        Missing Skills: {', '.join(missing_skills)}
        
        Resume: {resume_text[:2000]}
        JD: {jd_text[:2000]}
        
        IMPORTANT: Use very simple, easy-to-understand language. Avoid complex technical jargon. Ensure anyone (even non-technical users) can understand the feedback.
        
        Return ONLY a JSON object with these exact keys:
        - "raw_narrative": A simple 2-3 sentence summary telling them how well they fit and what they should learn.
        - "interview_questions": A list of 3 simple, encouraging interview questions to help them prepare (based on missing skills or their resume).
        - "resume_advice": One clear, actionable piece of simple advice to improve their resume for this exact role.
        - "recommended_role": A short 3-5 word job title that this resume is currently best suited for based on its main skills.
        """
        
        try:
            # Use async version of generate_content
            response = await self.model.generate_content_async(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    response_mime_type="application/json",
                )
            )
            
            import json
            data = json.loads(response.text)
            
            return {
                "status": "success",
                "raw_narrative": data.get("raw_narrative", ""),
                "interview_questions": data.get("interview_questions", []),
                "resume_advice": data.get("resume_advice", ""),
                "recommended_role": data.get("recommended_role", "Data/Software Intern")
            }
        except Exception as e:
            print(f"LLM Error: {str(e)}")
            fallback = self._get_fallback_insights(match_score, missing_skills)
            fallback["error"] = str(e)
            return fallback

narrative_service = StrategicNarrativeService()
