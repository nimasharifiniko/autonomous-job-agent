# 🤖 Autonomous AI Job Application Agent

An intelligent, privacy-first job searching and application system. It fetches real-time job listings, evaluates compatibility against candidate profiles using a local LLM, and automatically generates tailored cover letters — presented in a clean, executive Streamlit dashboard.

---

## 📌 The Problem
Searching for international software engineering roles is exhausting and time-consuming:
- **Time Drain**: Reading hundreds of job descriptions manually to find relevant roles wastes hours daily.
- **Generic Applications**: Sending standardized resumes and cover letters leads to low callback rates.
- **Privacy & Cost**: Relying on expensive or data-leaking cloud APIs for personal career data is unideal for engineering professionals.

---

## 💡 The Solution
**Autonomous AI Job Agent** automates the entire job evaluation pipeline locally:
1. **Real-Time Job Fetching**: Pulls live tech vacancies from Adzuna API based on search terms and target regions.
2. **Local AI Compatibility Matcher**: Runs job descriptions against a structured `profile.json` using a local LLM (`qwen2.5-coder:7b` via Ollama) to output a 0-100% compatibility score, skill gap analysis, and reasoning.
3. **Automated Cover Letter Writer**: For high-matching opportunities (e.g., >60%), generates a customized 3-4 sentence cover letter targeting the company's specific stack.
4. **Data Persistence**: Stores all evaluated jobs in SQLite to prevent redundant API calls and model executions.
5. **Interactive UI**: Displays opportunities in a modern white-and-navy Streamlit dashboard.

---

## 🏗️ System Architecture
[ Adzuna Job API ]
│
▼
[ job_fetcher.py ] ──► Extracts Live Job Listings
│
▼
[ matcher.py ] ◄────► [ profile.json ]
│ │
│ Evaluates Compatibility via Local Ollama LLM
│ │
├─── IF Match Score < Threshold ──► Save to DB (No Cover Letter)
│
└─── IF Match Score >= Threshold
│
▼
[ writer.py ] ──► Generate Targeted Cover Letter via AI
│
▼
[ database.py ] ──► Store in SQLite (jobs.db)
│
▼
[ app.py ] ──► Streamlit Web Dashboard

text


---

## 🛠️ Tech Stack & Tools

| Component | Technology | Description |
|---|---|---|
| **Language** | Python 3.10+ | Core application runtime |
| **User Interface** | Streamlit | Executive web dashboard with custom CSS styling |
| **API Integration** | Adzuna REST API | Real-time job vacancy data fetching |
| **AI / LLM Engine** | Ollama (`qwen2.5-coder:7b`) | Privacy-first local LLM inference |
| **Client SDK** | OpenAI Python SDK | Standardized interface to local Ollama API |
| **Database** | SQLite3 | Embedded database for job evaluations & cover letters |
| **Config** | python-dotenv | Secure API key & environment variable management |

---

## 🚀 Quick Start & Installation

### Prerequisites
- Python 3.10 or higher
- [Ollama](https://ollama.com/) installed and running locally

### 1. Clone & Environment Setup

```bash
# Clone the repository
git clone https://github.com/nimasharifiniko/autonomous-job-agent.git
cd autonomous-job-agent

# Create and activate virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install requests python-dotenv openai streamlit
2. Pull Local LLM Model
Make sure Ollama is active, then pull the model:

Bash

ollama pull qwen2.5-coder:7b
3. Environment Variables
Create a .env file in the root directory:

env

ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_APP_KEY=your_adzuna_app_key
ADZUNA_COUNTRY=gb
OLLAMA_BASE_URL=http://localhost:11434/v1
AI_MODEL_NAME=qwen2.5-coder:7b
4. Run the Application
Bash

streamlit run app.py
👤 Author
Developed by Nima Sharifi Niko as part of an advanced AI Automation Engineering portfolio.

GitHub: github.com/nimasharifiniko
LinkedIn: linkedin.com/in/nimasharifiniko