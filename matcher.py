import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
model_name = os.getenv("AI_MODEL_NAME", "qwen2.5-coder:7b")

client = OpenAI(
    base_url=base_url,
    api_key="ollama"
)


def load_user_profile():
    """Loads user profile from profile.json file."""
    try:
        with open("profile.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Warning: Could not load profile.json: {e}")
        return {}


MATCH_SYSTEM_PROMPT = """
You are an expert AI Technical Recruiter. Your task is to evaluate how well a candidate's profile matches a given Job Description.

Compare the provided Candidate Profile against the Job Description.

Return ONLY a valid JSON object with the following exact structure (no markdown backticks, no extra text):
{
    "match_score": 85,
    "summary_reason": "Brief 1-2 sentence explanation of why this score was assigned.",
    "matching_skills": ["Python", "SQLite"],
    "missing_skills": ["AWS", "Docker"]
}

Guidelines for match_score (0 to 100):
- 80-100: Strong match with core skills (Python, AI, Backend, Automation).
- 50-79: Moderate match (some transferable skills, missing key requirements).
- 0-49: Weak match (irrelevant domain, wrong tech stack).
"""


def evaluate_job_match(job_title: str, job_description: str) -> dict:
    """
    Evaluates job match percentage and reasoning using local LLM.
    """
    profile = load_user_profile()

    user_prompt = f"""
    CANDIDATE PROFILE:
    {json.dumps(profile, indent=2)}

    JOB TITLE: {job_title}
    JOB DESCRIPTION: {job_description}
    """

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": MATCH_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1
        )

        raw_content = response.choices[0].message.content.strip()

        # Clean markdown code blocks if model includes them
        if raw_content.startswith("```json"):
            raw_content = raw_content[7:]
        if raw_content.startswith("```"):
            raw_content = raw_content[3:]
        if raw_content.endswith("```"):
            raw_content = raw_content[:-3]

        result = json.loads(raw_content.strip())
        return result

    except json.JSONDecodeError:
        print("⚠️ Failed to parse LLM response as JSON. Returning fallback.")
        return {
            "match_score": 0,
            "summary_reason": "Parsing error from AI model.",
            "matching_skills": [],
            "missing_skills": []
        }
    except Exception as e:
        print(f"❌ Matcher error: {e}")
        return {
            "match_score": 0,
            "summary_reason": f"System error: {str(e)}",
            "matching_skills": [],
            "missing_skills": []
        }


# Self-testing script
if __name__ == "__main__":
    print("🧠 Testing AI Matcher Engine with local Ollama...\n")

    test_title = "Senior Python Developer - FastAPI & AI"
    test_desc = "We are seeking a Python Engineer skilled in REST APIs, Local LLMs, SQLite, and automation tools."

    print(f"Testing Job: {test_title}")
    match_result = evaluate_job_match(test_title, test_desc)

    print("\n📊 AI Match Result:")
    print(json.dumps(match_result, indent=2))
