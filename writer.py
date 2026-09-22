import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client for local Ollama
base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
model_name = os.getenv("AI_MODEL_NAME", "qwen2.5-coder:7b")

client = OpenAI(
    base_url=base_url,
    api_key="ollama"
)


def load_user_profile():
    """Loads candidate profile from profile.json file."""
    try:
        with open("profile.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Warning] Could not load profile.json: {e}")
        return {}


COVER_LETTER_SYSTEM_PROMPT = """
You are an expert career coach and technical copywriter. Your goal is to write a highly compelling, short, and customized Cover Letter for a candidate applying to a specific job position.

Guidelines for the Cover Letter:
- Keep it extremely concise: Exactly 3 to 4 sentences (1 paragraph).
- Do NOT use generic buzzwords or corporate fluff.
- Directly highlight the candidate's core skills that match the job requirements.
- Show enthusiasm and focus on how the candidate can add business value to the company.
- Professional, modern, and direct tone.
"""


def generate_cover_letter(job_title: str, company: str, job_description: str, matching_skills: list) -> str:
    """
    Generates a personalized cover letter using local LLM.
    """
    profile = load_user_profile()

    skills_str = ", ".join(
        matching_skills) if matching_skills else "Python, AI Automation, Backend Engineering"

    user_prompt = f"""
    CANDIDATE NAME: {profile.get('full_name', 'Nima Sharifi Niko')}
    TARGET ROLE: {profile.get('target_role', 'Python AI Automation Developer')}
    SUMMARY: {profile.get('experience_summary', '')}
    KEY MATCHING SKILLS: {skills_str}

    TARGET JOB DETAILS:
    - Company: {company}
    - Job Title: {job_title}
    - Job Description: {job_description}

    Write a 3-4 sentence customized cover letter.
    """

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": COVER_LETTER_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"[Error] Failed to generate cover letter: {e}")
        return f"Dear Hiring Team at {company}, I am excited to apply for the {job_title} position. With my background in {skills_str}, I am confident in my ability to deliver immediate value to your engineering team. I look forward to connecting."


# Self-testing script
if __name__ == "__main__":
    print("✍️ Testing AI Cover Letter Writer Engine...\n")

    test_title = "Python Developer - Problem Solver"
    test_company = "Client Server"
    test_desc = "Looking for a technologist Python Developer who enjoys problem solving, working with SQLite, and building backend software systems."
    test_skills = ["Python", "SQLite", "Backend Engineering"]

    print(f"Company: {test_company}")
    print(f"Role: {test_title}")
    print("\n--- Generated Cover Letter ---")

    cover_letter = generate_cover_letter(
        test_title, test_company, test_desc, test_skills)
    print(cover_letter)
    print("------------------------------\n")
