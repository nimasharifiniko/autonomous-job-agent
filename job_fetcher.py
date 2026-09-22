import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")
ADZUNA_COUNTRY = os.getenv("ADZUNA_COUNTRY", "gb")  # Default to UK (gb)


def fetch_jobs(search_term="Python Developer", results_per_page=5, page=1):
    """
    Fetches job listings from Adzuna API based on search term and country code.
    Returns a list of structured job dictionaries.
    """
    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
        raise ValueError(
            "❌ Missing ADZUNA_APP_ID or ADZUNA_APP_KEY in .env file.")

    url = f"https://api.adzuna.com/v1/api/jobs/{ADZUNA_COUNTRY}/search/{page}"

    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": results_per_page,
        "what": search_term,
        "content-type": "application/json"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        raw_results = data.get("results", [])
        clean_jobs = []

        for job in raw_results:
            clean_jobs.append({
                "id": str(job.get("id", "")),
                "title": job.get("title", "N/A"),
                "company": job.get("company", {}).get("display_name", "Unknown Company"),
                "location": job.get("location", {}).get("display_name", "Remote / Unknown"),
                "description": job.get("description", "No description provided."),
                "redirect_url": job.get("redirect_url", ""),
                "created": job.get("created", "")
            })

        return clean_jobs

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching jobs from Adzuna API: {e}")
        return []


# Self-testing block
if __name__ == "__main__":
    print("🔍 Testing Job Fetcher Module with keyword: 'Python Developer'...")
    jobs = fetch_jobs("Python Developer", results_per_page=3)

    print(f"\n✅ Successfully fetched {len(jobs)} job(s):\n")
    for idx, j in enumerate(jobs, start=1):
        print(f"--- Job #{idx} ---")
        print(f"📌 Title: {j['title']}")
        print(f"🏢 Company: {j['company']}")
        print(f"📍 Location: {j['location']}")
        print(f"📝 Description Snippet: {j['description'][:150]}...")
        print(f"🔗 URL: {j['redirect_url']}")
        print("-" * 40 + "\n")
