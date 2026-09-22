import sqlite3
import os
import json

DB_PATH = "jobs.db"


def get_connection():
    """Establish connection to SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn


def init_db():
    """Initialize database tables if they do not exist."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                job_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                company TEXT,
                location TEXT,
                description TEXT,
                redirect_url TEXT,
                match_score INTEGER,
                summary_reason TEXT,
                matching_skills TEXT,
                missing_skills TEXT,
                cover_letter TEXT,
                status TEXT DEFAULT 'New',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    print("[Database] Schema initialized successfully.")


def job_exists(job_id: str) -> bool:
    """Check if a job ID already exists in database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM jobs WHERE job_id = ?", (job_id,))
        return cursor.fetchone() is not None


def save_job_record(job_dict: dict, match_dict: dict, cover_letter: str = ""):
    """Save or replace a full job application evaluation record."""
    job_id = str(job_dict.get("id"))

    matching_skills_str = json.dumps(match_dict.get("matching_skills", []))
    missing_skills_str = json.dumps(match_dict.get("missing_skills", []))

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO jobs (
                job_id, title, company, location, description, redirect_url,
                match_score, summary_reason, matching_skills, missing_skills,
                cover_letter, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'New')
        """, (
            job_id,
            job_dict.get("title"),
            job_dict.get("company"),
            job_dict.get("location"),
            job_dict.get("description"),
            job_dict.get("redirect_url"),
            match_dict.get("match_score", 0),
            match_dict.get("summary_reason", ""),
            matching_skills_str,
            missing_skills_str,
            cover_letter
        ))
        conn.commit()


def get_all_jobs():
    """Fetch all stored job evaluations sorted by highest match score."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM jobs ORDER BY match_score DESC, created_at DESC
        """)
        rows = cursor.fetchall()

        results = []
        for row in rows:
            item = dict(row)
            item["matching_skills"] = json.loads(
                item["matching_skills"]) if item["matching_skills"] else []
            item["missing_skills"] = json.loads(
                item["missing_skills"]) if item["missing_skills"] else []
            results.append(item)

        return results


# Self-testing script
if __name__ == "__main__":
    init_db()

    test_job = {
        "id": "test_12345",
        "title": "Python AI Engineer",
        "company": "Tech Corp",
        "location": "London",
        "description": "Looking for Python AI devs.",
        "redirect_url": "https://example.com"
    }

    test_match = {
        "match_score": 92,
        "summary_reason": "Great fit for Python and AI automation.",
        "matching_skills": ["Python", "AI"],
        "missing_skills": []
    }

    test_letter = "Dear Tech Corp, I am excited to apply..."

    save_job_record(test_job, test_match, test_letter)
    print(f"✅ Saved test record. Exists check: {job_exists('test_12345')}")

    all_records = get_all_jobs()
    print(f"📊 Total jobs stored in DB: {len(all_records)}")
