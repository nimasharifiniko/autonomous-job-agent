import os
import glob
import base64
import streamlit as st
from database import init_db, get_all_jobs
from pipeline import run_agent_pipeline

# Page Configuration
st.set_page_config(
    page_title="Autonomous AI Job Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Modern White & Royal Blue SaaS Styling
st.markdown("""
    <style>
    /* Global background tint */
    .stApp { background-color: #F8FAFC; }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] { background-color: #0F172A !important; }
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] p { color: #F8FAFC !important; }

    /* Fix Input Box Text Color inside Sidebar */
    section[data-testid="stSidebar"] div[data-baseweb="input"] input {
        color: #0F172A !important;
        background-color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    
    section[data-testid="stSidebar"] div[data-baseweb="input"] {
        background-color: #FFFFFF !important;
        border-radius: 8px !important;
    }

    /* Custom Profile Avatar */
    .avatar-container {
        display: flex;
        justify-content: center;
        margin: 10px 0 15px 0;
    }
    .avatar-img {
        width: 140px;
        height: 140px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #38BDF8;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5);
    }
    
    /* Text & Links */
    .profile-title { text-align: center; font-size: 1.3rem; font-weight: 800; margin-bottom: 2px; color: #FFFFFF !important; }
    .profile-subtitle { text-align: center; font-size: 0.9rem; color: #94A3B8 !important; margin-bottom: 15px; }
    .social-links { text-align: center; margin-bottom: 20px; }
    .social-links a {
        color: #38BDF8 !important;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 0 8px;
        transition: 0.2s;
    }
    .social-links a:hover { color: #FFFFFF !important; }

    /* Main Area Headers & Buttons */
    h1 { color: #0F172A !important; font-weight: 800 !important; }
    h3 { color: #1E3A8A !important; }
    div.stButton > button {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 0.6rem 1rem !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25) !important;
    }
    div.stButton > button:hover { background-color: #1D4ED8 !important; }

    /* Job Cards */
    div[data-testid="stExpander"] {
        border: 1px solid #CBD5E1 !important;
        border-radius: 12px !important;
        background-color: #FFFFFF !important;
        margin-bottom: 12px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    }
    div[data-testid="stMetric"] {
        background-color: #EFF6FF !important;
        padding: 10px 15px !important;
        border-radius: 10px !important;
        border: 1px solid #BFDBFE !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Database Table
init_db()

# Main Header
st.title("🤖 Autonomous AI Job Agent")
st.markdown("An intelligent dashboard that fetches live listings, matches skills using local LLMs (Ollama/Qwen 2.5), and writes customized cover letters.")
st.divider()

# ================= SIDEBAR PROFILE & CONTROLS =================


def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


profile_files = glob.glob("profile.*") + glob.glob("Profile.*")

if profile_files:
    img_base64 = get_base64_image(profile_files[0])
    st.sidebar.markdown(f'''
        <div class="avatar-container">
            <img src="data:image/png;base64,{img_base64}" class="avatar-img" />
        </div>
    ''', unsafe_allow_html=True)

st.sidebar.markdown(
    "<div class='profile-title'>Nima Sharifi Niko</div>", unsafe_allow_html=True)
st.sidebar.markdown(
    "<div class='profile-subtitle'>AI Automation Developer</div>", unsafe_allow_html=True)

# Social Links
st.sidebar.markdown("""
    <div class='social-links'>
        <a href="https://github.com/nimasharifiniko" target="_blank">🔗 GitHub</a> | 
        <a href="https://linkedin.com/in/nimasharifiniko" target="_blank">🔗 LinkedIn</a>
    </div>
""", unsafe_allow_html=True)

st.sidebar.divider()

st.sidebar.subheader("⚙️ Agent Controls")
search_term = st.sidebar.text_input(
    "Job Search Keyword", value="Python Developer")
results_count = st.sidebar.slider(
    "Number of Jobs to Fetch", min_value=1, max_value=10, value=3)
match_threshold = st.sidebar.slider(
    "Min Match Score for Cover Letter (%)", min_value=30, max_value=90, value=60)

run_button = st.sidebar.button(
    "🚀 Fetch & Process Jobs", use_container_width=True)

# ================= PIPELINE LOGIC =================
if run_button:
    with st.spinner("🤖 Fetching jobs from Adzuna & evaluating with local AI... Please wait."):
        run_agent_pipeline(
            search_term=search_term,
            results_count=results_count,
            match_threshold=match_threshold
        )
    st.success("✅ Job search and AI evaluation pipeline finished!")
    st.rerun()

# ================= DISPLAY JOBS =================
stored_jobs = get_all_jobs()

st.subheader(f"📋 Analyzed Job Opportunities ({len(stored_jobs)})")

if not stored_jobs:
    st.info("No job evaluations found in database yet. Click **'Fetch & Process Jobs'** in the sidebar to start!")
else:
    for job in stored_jobs:
        score = job.get("match_score", 0)
        badge_color = "🟢" if score >= 70 else ("🟡" if score >= 50 else "🔴")

        with st.expander(f"{badge_color} [{score}% Match] {job['title']} — {job['company']} ({job['location']})"):
            col1, col2 = st.columns([2.5, 1])

            with col1:
                st.markdown(f"**🏢 Company:** {job['company']}")
                st.markdown(f"**📍 Location:** {job['location']}")
                st.markdown(f"**💬 AI Analysis:** {job['summary_reason']}")
                st.markdown(
                    f"**🔗 Job Post:** [Apply / View Details]({job['redirect_url']})")

            with col2:
                st.metric("Match Score", f"{score}%")
                st.progress(score / 100.0)

            st.divider()

            skill_col1, skill_col2 = st.columns(2)
            with skill_col1:
                matching_skills = job.get("matching_skills", [])
                st.markdown("**✅ Matching Skills:**")
                if matching_skills:
                    st.write(", ".join(f"`{s}`" for s in matching_skills))
                else:
                    st.write("None detected")

            with skill_col2:
                missing_skills = job.get("missing_skills", [])
                st.markdown("**⚠️ Skill Gaps / Missing:**")
                if missing_skills:
                    st.write(", ".join(f"`{s}`" for s in missing_skills))
                else:
                    st.write("None detected")

            if job.get("cover_letter"):
                st.divider()
                st.markdown("### ✍️ AI-Generated Cover Letter")
                st.text_area(
                    label="Customized Application Cover Letter",
                    value=job["cover_letter"],
                    height=150,
                    key=f"cl_{job['job_id']}"
                )
