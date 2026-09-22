import os
from job_fetcher import fetch_jobs
from matcher import evaluate_job_match
from writer import generate_cover_letter
from database import init_db, job_exists, save_job_record, get_all_jobs


def run_agent_pipeline(search_term="Python Developer", results_count=3, match_threshold=60):
    """
    Executes the full autonomous job agent pipeline:
    Fetch -> Check DB -> AI Match -> Generate Cover Letter -> Store in SQLite.
    """
    # Ensure database table exists
    init_db()

    print(f"\n🚀 Running Autonomous Job Agent Pipeline...")
    print(
        f"🔍 Search Term: '{search_term}' | Fetch Limit: {results_count} | Match Threshold: {match_threshold}%\n")

    # Step 1: Fetch raw job listings from API
    raw_jobs = fetch_jobs(search_term=search_term,
                          results_per_page=results_count)

    if not raw_jobs:
        print("[Warning] No job listings returned from API.")
        return []

    processed_count = 0

    for idx, job in enumerate(raw_jobs, start=1):
        job_id = job.get("id")
        title = job.get("title")
        company = job.get("company")

        print(f"[{idx}/{len(raw_jobs)}] Job: {title} @ {company}")

        # Step 2: Avoid redundant processing if job exists in DB
        if job_exists(job_id):
            print(
                f" ⏭️ Job ID [{job_id}] already in database. Skipping redundant LLM evaluation.\n")
            continue

        # Step 3: Run AI Match Evaluation
        print(" 🤖 Evaluating match with local AI...")
        match_res = evaluate_job_match(title, job.get("description", ""))
        score = match_res.get("match_score", 0)

        # Step 4: Generate Cover Letter if score meets threshold
        cover_letter = ""
        if score >= match_threshold:
            print(
                f" 🎯 High match score ({score}%)! Generating customized Cover Letter...")
            cover_letter = generate_cover_letter(
                job_title=title,
                company=company,
                job_description=job.get("description", ""),
                matching_skills=match_res.get("matching_skills", [])
            )
        else:
            print(
                f" ℹ️ Match score ({score}%) below threshold ({match_threshold}%). Skipping cover letter.")

        # Step 5: Save evaluation record to SQLite DB
        save_job_record(job, match_res, cover_letter)
        print(" 💾 Saved record to SQLite database.\n")
        processed_count += 1

    print(
        f"✅ Pipeline complete! Processed {processed_count} new job listing(s).")
    return get_all_jobs()


# Independent testing
if __name__ == "__main__":
    all_stored_jobs = run_agent_pipeline(
        search_term="Python Developer", results_count=3, match_threshold=60)

    print(f"\n📊 Total Stored Jobs in SQLite DB: {len(all_stored_jobs)}")
    for j in all_stored_jobs:
        print(f"- [{j['match_score']}%] {j['title']} at {j['company']} (Cover Letter Generated: {bool(j['cover_letter'])})")
