# app.py - InterviewMate (Midnight Blue, Neon Cyan, Hybrid tone)
import streamlit as st
import os, json, requests
from dotenv import load_dotenv
from typing import List

# Try modern OpenAI client, fall back to openai
try:
    from openai import OpenAI
    OPENAI_CLIENT_AVAILABLE = True
except Exception:
    import openai
    OPENAI_CLIENT_AVAILABLE = False

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

if OPENAI_CLIENT_AVAILABLE:
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    openai.api_key = OPENAI_API_KEY


# ------------------------
# Page config + CSS
# ------------------------
st.set_page_config(page_title="InterviewMate", page_icon="🤖", layout="wide")
st.markdown(
    """
    <style>
      .stApp { background: linear-gradient(180deg, #030517 0%, #071032 45%, #0b1736 100%); color: #e6eef8; }
      .chat-wrap { max-width: 980px; margin: 0 auto; padding: 18px 12px 80px 12px; }
      .messages { max-height: 68vh; overflow-y: auto; padding: 12px; }
      .assistant {
        background: linear-gradient(180deg, rgba(0,230,255,0.06), rgba(0,200,255,0.04));
        color: #dff8ff; padding:14px; border-radius:12px;
        border-left: 3px solid rgba(0,230,255,0.18); margin: 10px 0;
        width: fit-content; max-width: 78%; box-shadow: 0 8px 30px rgba(0,200,255,0.03);
      }
      .user {
        background: linear-gradient(180deg,#071033,#061226); color: #bfe6ff;
        padding:12px; border-radius:12px; margin: 10px 0; margin-left: auto;
        width: fit-content; max-width: 78%; box-shadow: 0 8px 30px rgba(2,6,23,0.6);
      }
      .role-card { background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
                   border: 1px solid rgba(0,230,255,0.06);
                   padding:10px; border-radius:10px; margin-bottom:8px;}
      .role-title { color:#9ff; font-weight:700; }
      .role-desc { color:#a9dbe6; font-size:13px; margin-top:6px; }
      .domain-banner { background: linear-gradient(90deg, rgba(0,12,30,0.6), rgba(0,20,40,0.55));
                        padding:8px; border-radius:8px; border:1px solid rgba(0,230,255,0.04); margin-bottom:10px;
                        color: #bfefff; }
      .muted { color:#9fb3c4; font-size:13px; }
      .typing { color:#8fdbe8; font-style:italic; margin:6px 0; }
      .btn {
        background: linear-gradient(90deg, #00e6ff, #00c8ff);
        color: #001b22; padding:8px 12px; border-radius:8px; font-weight:600;
      }
      .footer { color:#8fb3c4; text-align:center; margin-top:18px; font-size:13px; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------------
# Session state
# ------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_domain" not in st.session_state:
    st.session_state.last_domain = ""
if "suggested_roles" not in st.session_state:
    st.session_state.suggested_roles = []
if "selected_role" not in st.session_state:
    st.session_state.selected_role = None
if "roadmap_md" not in st.session_state:
    st.session_state.roadmap_md = None
if "study_resources" not in st.session_state:
    st.session_state.study_resources = None
if "jobs" not in st.session_state:
    st.session_state.jobs = []
if "domain_history" not in st.session_state:
    st.session_state.domain_history = []
if "pending_message" not in st.session_state:
    st.session_state.pending_message = ""


# ------------------------
# Helpers
# ------------------------
def call_gpt(messages: List[dict], model="gpt-4o-mini", max_tokens=800, temperature=0.25):
    if not OPENAI_API_KEY:
        return "⚠️ OpenAI API key missing."
    try:
        if OPENAI_CLIENT_AVAILABLE:
            resp = client.chat.completions.create(
                model=model, messages=messages, max_tokens=max_tokens, temperature=temperature
            )
            return resp.choices[0].message.content
        else:
            resp = openai.ChatCompletion.create(
                model=model, messages=messages, max_tokens=max_tokens, temperature=temperature
            )
            return resp.choices[0].message["content"]
    except Exception as e:
        return f"⚠️ AI error: {e}"


def is_domain_like(text: str) -> bool:
    t = text.strip().lower()
    greetings = ["hi", "hey", "hello", "yo", "sup", "good morning", "good evening", "thank you", "thanks"]
    if any(g == t or g in t for g in greetings):
        return False

    domain_keywords = [
        "data", "ai", "machine learning", "ml", "developer", "software", "engineer", "analyst",
        "cyber", "security", "cloud", "devops", "tester", "qa", "android", "mobile", "web",
        "frontend", "backend", "design", "ui", "ux"
    ]

    t = t.replace("domain", "").replace("field", "").replace("job", "").strip()
    for k in domain_keywords:
        if k in t:
            return True
    return False


def extract_domain(text: str) -> str:
    text = text.lower().strip()

    domain_map = {
        "data": "data",
        "machine learning": "ai",
        "ml": "ai",
        "artificial intelligence": "ai",
        "ai": "ai",
        "frontend": "web",
        "backend": "web",
        "web": "web",
        "developer": "web",
        "cloud": "cloud",
        "aws": "cloud",
        "azure": "cloud",
        "devops": "cloud",
        "cyber": "security",
        "security": "security",
        "tester": "tester",
        "qa": "tester",
        "testing": "tester",
        "commerce": "business",
        "finance": "business",
        "business": "business",
        "marketing": "business",
        "sales": "business",
        "design": "design",
        "ui": "design",
        "ux": "design",
    }

    found = None
    for word, mapped in domain_map.items():
        if word in text:
            found = mapped
    return found if found else ""


def get_domains_from_skills(text: str) -> list:
    t = text.lower()
    mapping = {
        "html": "web", "css": "web", "javascript": "web", "react": "web", "angular": "web",
        "java": "backend", "spring": "backend",
        "python": "data", "sql": "data", "pandas": "data", "excel": "data", "tableau": "data",
        "power bi": "data", "aws": "cloud", "azure": "cloud",
        "docker": "devops", "kubernetes": "devops", "testing": "tester",
        "selenium": "tester", "cyber": "security", "network": "security",
        "machine learning": "ai", "deep learning": "ai", "nlp": "ai"
    }

    found_domains = set()
    for skill, domain in mapping.items():
        if skill in t:
            found_domains.add(domain)
    return list(found_domains)


def fetch_roles_for_domain(domain: str) -> List[dict]:
    fallback_roles = {
        "data": [
            {"title": "Data Analyst", "desc": "Turns raw data into business insights."},
            {"title": "Data Scientist", "desc": "Applies ML and stats to uncover trends."},
            {"title": "Data Engineer", "desc": "Builds and manages data pipelines."},
            {"title": "BI Analyst", "desc": "Creates dashboards and visualization reports."},
            {"title": "ML Engineer", "desc": "Develops models that make predictions."}
        ],
        "web": [
            {"title": "Frontend Developer", "desc": "Builds responsive and modern UIs."},
            {"title": "Backend Developer", "desc": "Develops and maintains APIs."},
            {"title": "Full Stack Developer", "desc": "Works across front and back end."},
            {"title": "UI/UX Designer", "desc": "Designs beautiful user experiences."},
            {"title": "Web Tester", "desc": "Ensures web apps work flawlessly."}
        ],
        "cloud": [
            {"title": "Cloud Engineer", "desc": "Manages cloud infrastructure."},
            {"title": "DevOps Engineer", "desc": "Automates CI/CD pipelines."},
            {"title": "Cloud Architect", "desc": "Designs scalable systems."},
            {"title": "Cloud Security Engineer", "desc": "Secures cloud environments."},
            {"title": "SRE", "desc": "Ensures system reliability and uptime."}
        ],
        "ai": [
            {"title": "AI Engineer", "desc": "Builds and deploys AI-driven systems."},
            {"title": "ML Researcher", "desc": "Develops machine learning algorithms."},
            {"title": "NLP Engineer", "desc": "Works with text and language data."},
            {"title": "CV Engineer", "desc": "Focuses on image/video recognition."},
            {"title": "AI Product Manager", "desc": "Bridges AI tech with product vision."}
        ]
    }

    return fallback_roles.get(domain.lower(), fallback_roles["data"])


def generate_roadmap(role: str, domain: str):
    prompt = f"As InterviewMate, make a 4-week roadmap for '{role}' in '{domain}'. Include weekly goals and learning resources."
    return call_gpt([{"role": "user", "content": prompt}], max_tokens=1000)


def fetch_jobs_for_role(role: str):
    if not RAPIDAPI_KEY:
        return [
            {"title": "Data Analyst", "company": "Contoso Analytics", "city": "Bangalore", "apply": "https://example.com"},
            {"title": "Data Engineer", "company": "Atlas Systems", "city": "Pune", "apply": "https://example.com"},
        ]
    try:
        url = "https://jsearch.p.rapidapi.com/search"
        headers = {"X-RapidAPI-Key": RAPIDAPI_KEY, "X-RapidAPI-Host": "jsearch.p.rapidapi.com"}
        params = {"query": f"{role} in India", "num_pages": "1"}
        r = requests.get(url, headers=headers, params=params, timeout=8)
        data = r.json().get("data", [])
        return [{"title": j.get("job_title", "Job"), "company": j.get("employer_name", "Company"),
                 "city": j.get("job_city", ""), "apply": j.get("job_apply_link", "")} for j in data]
    except Exception as e:
        print("Job fetch error:", e)
        return []


# ------------------------
# Chat Logic (fixed)
# ------------------------
def append_user(msg_text: str):
    st.session_state.chat_history.append({"role": "user", "content": msg_text})
    text = msg_text.lower()

    # Detect skill-based intent
    skill_domains = get_domains_from_skills(text)
    if skill_domains:
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "Nice skillset! 😎 Based on what you mentioned, here are some domains you could explore 👇"
        })
        all_roles = []
        for d in skill_domains:
            roles = fetch_roles_for_domain(d)
            all_roles.extend(roles[:3])
            if d not in st.session_state.domain_history:
                st.session_state.domain_history.append(d)
        st.session_state.suggested_roles = all_roles
        st.session_state.pending_message = ""
        st.rerun()

    # --- Domain switch handling ---
    if is_domain_like(text):
        domain = extract_domain(text)
        st.session_state.last_domain = domain

        # Clear previous role suggestions
        st.session_state.suggested_roles = []

        roles = fetch_roles_for_domain(domain)
        if roles:
            st.session_state.suggested_roles = roles
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": f"✅ Got it! Switching gears to **{domain.capitalize()}** — here are some top roles you can explore 👇"
            })
        else:
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": f"Sure! Let’s explore the **{domain.capitalize()}** field and its opportunities."
            })

        if domain not in st.session_state.domain_history:
            st.session_state.domain_history.append(domain)

        # Reset other state fields
        st.session_state.selected_role = None
        st.session_state.roadmap_md = None
        st.session_state.study_resources = None
        st.session_state.jobs = []

        # Force rerun
        st.session_state.pending_message = ""
        st.rerun()

    # Default conversation
    else:
        context = [{"role": "system", "content": "You are InterviewMate — a friendly, career-focused mentor."}]
        for m in st.session_state.chat_history[-8:]:
            context.append({"role": m["role"], "content": m["content"]})
        context.append({"role": "user", "content": msg_text})
        reply = call_gpt(context, max_tokens=600)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.session_state.pending_message = ""


# ------------------------
# UI Layout (stable)
# ------------------------
left_col, right_col = st.columns([3, 1])

# Sidebar – Jobs + Domains
with right_col:
    st.markdown("## 💼 Live Jobs")
    if st.session_state.selected_role:
        jobs = st.session_state.jobs or fetch_jobs_for_role(st.session_state.selected_role)
        for i, j in enumerate(jobs[:8], 1):
            st.markdown(f"**{i}. {j['title']}** — {j['company']} • {j['city']}")
            if j.get("apply"):
                st.markdown(f"<a href='{j['apply']}' target='_blank' class='muted'>Apply</a>", unsafe_allow_html=True)
    else:
        st.write("Choose a role to see jobs here.")
    if st.button("Refresh Jobs"):
        if st.session_state.selected_role:
            st.session_state.jobs = fetch_jobs_for_role(st.session_state.selected_role)
            st.rerun()

    st.write("---")
    st.markdown("## 📂 Domains explored")
    for d in reversed(st.session_state.domain_history):
        if st.button(d):
            st.session_state.last_domain = d
            st.session_state.suggested_roles = fetch_roles_for_domain(d)
            st.session_state.selected_role = None
            st.rerun()

# Chat area
with left_col:
    st.markdown("<div class='chat-wrap'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#9fffefff'>InterviewMate — your AI mentor</h2>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='messages'>", unsafe_allow_html=True)
        for m in st.session_state.chat_history:
            bubble = "assistant" if m["role"] == "assistant" else "user"
            st.markdown(f"<div class='{bubble}'>{m['content']}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Handle pending message safely
    if st.session_state.pending_message:
        msg = st.session_state.pending_message
        st.session_state.pending_message = ""
        append_user(msg)
        st.rerun()

    # Suggested roles UI
    if st.session_state.suggested_roles and not st.session_state.selected_role:
        st.markdown("**Suggested roles:**")
        cols = st.columns(3)
        for i, r in enumerate(st.session_state.suggested_roles):
            with cols[i % 3]:
                st.markdown(
                    f"<div class='role-card'><div class='role-title'>{r['title']}</div><div class='role-desc'>{r['desc']}</div></div>",
                    unsafe_allow_html=True,
                )
                if st.button(f"Choose {r['title']}", key=f"choose_{i}"):
                    st.session_state.selected_role = r["title"]
                    with st.spinner("InterviewMate is preparing your roadmap..."):
                        st.session_state.roadmap_md = generate_roadmap(
                            r["title"], st.session_state.last_domain
                        )
                        st.session_state.study_resources = call_gpt(
                            [
                                {
                                    "role": "user",
                                    "content": f"List top resources for {r['title']} in {st.session_state.last_domain}",
                                }
                            ],
                            max_tokens=400,
                        )
                        st.session_state.jobs = fetch_jobs_for_role(r["title"])
                    st.rerun()

    # Chat input
    prompt = st.chat_input("Talk to InterviewMate...")
    if prompt:
        st.session_state.pending_message = prompt
        st.rerun()

    # Roadmap display
    if st.session_state.roadmap_md:
        st.markdown("---")
        st.markdown("### 🗺 4-week Roadmap")
        rd = st.session_state.roadmap_md
        for w in range(1, 5):
            marker = f"Week {w}"
            if marker in rd:
                start = rd.find(marker)
                end = rd.find(f"Week {w+1}", start) if f"Week {w+1}" in rd else len(rd)
                with st.expander(f"Week {w}"):
                    st.markdown(rd[start:end])
        with st.expander("📚 Study Resources"):
            st.markdown(st.session_state.study_resources or "No study resources found.")

st.markdown("<div class='footer'>Built with ❤️ — InterviewMate • Hybrid mentor (Smart + Chill)</div>", unsafe_allow_html=True)
