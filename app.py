
import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Education System",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- MODERN BLUE UI ----------------
st.markdown("""
<style>

<style>
/* Dark navy and royal blue theme */

.stApp {
    background: #0b1220;
    color: #e5edff;
}

[data-testid="stHeader"] {
    background: #0b1220;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #101a35 0%, #142b59 100%);
    border-right: 1px solid #263c68;
}

[data-testid="stSidebar"] * {
    color: #e5edff !important;
}

.main .block-container {
    max-width: 1120px;
    padding: 2rem 2rem 4rem;
}

h1, h2, h3 {
    color: #8db8ff !important;
}

p, label, .stMarkdown {
    color: #d5e1f7;
}

/* Hero banner */
.hero {
    background: linear-gradient(125deg, #142c62, #174ea6, #5136a8);
    padding: 32px;
    border: 1px solid #34599a;
    border-radius: 22px;
    color: #ffffff;
    margin-bottom: 26px;
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.22);
}

.hero h1, .hero p {
    color: #ffffff !important;
}

/* Input fields */
.stTextInput input,
.stTextArea textarea {
    background: #141f35 !important;
    color: #f1f5ff !important;
    border: 1px solid #33496f !important;
    border-radius: 12px !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #6098ff !important;
    box-shadow: 0 0 0 2px #1d3d73 !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #94a8c8 !important;
}

/* Buttons */
.stButton > button,
.stDownloadButton > button {
    background: linear-gradient(100deg, #2164d8, #6045d5);
    color: #ffffff !important;
    border: 1px solid #4779d9;
    border-radius: 12px;
    min-height: 45px;
    font-weight: 600;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: linear-gradient(100deg, #347cf2, #7659ef);
    border-color: #8db8ff;
}

/* Chat messages */
div[data-testid="stChatMessage"] {
    background: #111d33;
    border: 1px solid #293e61;
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 12px;
}

/* Chat input */
div[data-testid="stChatInput"] {
    background: #141f35;
    border: 1px solid #3a5480;
    border-radius: 16px;
}

div[data-testid="stChatInput"] textarea {
    color: #ffffff !important;
}

/* Alerts and separators */
div[data-testid="stAlert"] {
    background: #152744;
    border-radius: 12px;
}

hr {
    border-color: #2b3d60 !important;
}

[data-testid="stSidebar"] hr {
    border-color: #3a4f75 !important;
}

/* Footer */
.footer {
    text-align: center;
    color: #8da4c8;
    padding: 20px 0;
    font-size: 13px;
}

@media (max-width: 768px) {
    .main .block-container {
        padding: 1rem 1rem 3rem;
    }

    .hero {
        padding: 22px;
        border-radius: 16px;
    }
}
</style>

</style>
""", unsafe_allow_html=True)

# ---------------- GEMINI API ----------------
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    st.error(
        "Gemini API key is missing. Please add GEMINI_API_KEY "
        "to your .env file or Streamlit Secrets."
    )
    st.stop()

client = genai.Client(api_key=api_key)

# ---------------- AI SYSTEM PROMPT ----------------
SYSTEM_PROMPT = """
You are Smart Education System's AI Lesson Assistant.

ROLE:
Help teachers create effective lessons and explain educational
topics in a clear, detailed, practical and engaging way.

ANSWER QUALITY:
- Use simple, clear English.
- Start with a direct answer or easy definition.
- Explain concepts step by step, from basic to advanced.
- Use clear headings, numbered steps and bullet points.
- Include relevant real-life and classroom examples.
- Explain difficult terms in simple language.
- Adapt the explanation to the given class or grade.
- Include practical applications when useful.
- Avoid unnecessary repetition and complicated wording.
- Never invent facts; acknowledge uncertainty.
- Answer all parts of the user's question.
- Keep simple answers concise and complex answers detailed.
- Use tables only when they genuinely improve understanding.

FOR LESSON PLANNING, INCLUDE:
1. Lesson Title
2. Learning Objectives
3. Required Materials
4. Introduction
5. Empathize
6. Define
7. Ideate
8. Prototype
9. Test
10. Step-by-Step Teaching Procedure
11. Group Activity
12. Worksheet or Practice Questions
13. Assessment
14. Expected Learning Outcomes
15. Homework or Extension Activity

FOR GENERAL EDUCATIONAL QUESTIONS, USE WHEN RELEVANT:
1. Simple Definition
2. Detailed Explanation
3. Step-by-Step Breakdown
4. Real-Life Examples
5. Practical Applications
6. Summary
7. Practice Questions

DESIGN THINKING:
Explain Empathize, Define, Ideate, Prototype and Test when
relevant to the question or classroom activity.

TEACHING STYLE:
Be patient, encouraging and helpful.
Make activities practical for teachers and students.
Ask a short clarifying question if essential information is missing.
Politely redirect unrelated questions toward educational topics.
"""

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("# 📘 Smart Education")
    st.markdown("### AI Lesson Assistant")
    st.markdown("---")

    page = st.radio(
        "Navigation",
        ["🏠 Lesson Planner", "💬 AI Chat Assistant"],
        label_visibility="visible"
    )

    st.markdown("---")
    st.markdown("**Your teaching workspace**")
    st.caption("Plan lessons. Explore ideas. Inspire learning.")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.caption("Powered by Gemini AI")

# ---------------- HERO ----------------
st.markdown("""
<div class="hero">
    <h1>📘 Smart Education System</h1>
    <p>
        Your AI-powered teaching partner for creative lessons,
        classroom activities and better learning experiences.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- LESSON PLANNER ----------------
if page == "🏠 Lesson Planner":

    st.markdown("## ✨ Create Your Lesson")
    st.write(
        "Fill in the details below to generate a structured, "
        "classroom-ready lesson plan."
    )

    with st.container(border=True):
        subject = st.text_input(
            "📚 Subject",
            placeholder="e.g. Science, Mathematics, English"
        )

        grade = st.text_input(
            "🎓 Class / Grade",
            placeholder="e.g. Class 8"
        )

        topic = st.text_input(
            "📌 Lesson Topic",
            placeholder="e.g. Water Conservation"
        )

        objective = st.text_area(
            "🎯 Learning Objective (optional)",
            placeholder="What should students learn from this lesson?",
            height=110
        )

        generate = st.button(
            "✨ Generate Lesson Plan",
            use_container_width=True
        )

    if generate:
        if not subject.strip() or not grade.strip() or not topic.strip():
            st.warning(
                "Please enter the Subject, Class/Grade and Topic."
            )
        else:
            lesson_request = f"""
Create a complete, practical classroom lesson plan.

Subject: {subject}
Class/Grade: {grade}
Topic: {topic}
Learning Objective: {objective.strip() or "Create a suitable objective."}

Explain the lesson in simple English, with clear headings
and practical examples suitable for this grade.

Include:
1. Lesson Title
2. Learning Objectives
3. Required Materials
4. Introduction
5. Empathize
6. Define
7. Ideate
8. Prototype
9. Test
10. Step-by-Step Teaching Procedure
11. Group Activity
12. Worksheet or Practice Questions
13. Assessment
14. Expected Learning Outcomes
15. Homework or Extension Activity

Make the lesson easy for a teacher to conduct.
Include suggested timings when useful.
"""

            with st.spinner("🤖 Creating your lesson plan..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-3.5-flash-lite",
                        contents=lesson_request,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_PROMPT,
                            temperature=0.5
                        )
                    )

                    answer = response.text

                    if not answer:
                        st.error(
                            "The AI returned an empty response. Please try again."
                        )
                    else:
                        st.session_state.messages.extend([
                            {
                                "role": "user",
                                "content": lesson_request
                            },
                            {
                                "role": "assistant",
                                "content": answer
                            }
                        ])

                        st.success("Your lesson plan is ready!")

                        st.markdown("### 📖 Your Generated Lesson")
                        st.markdown(answer)

                        st.download_button(
                            "⬇️ Download Lesson Plan",
                            data=answer,
                            file_name="lesson_plan.txt",
                            mime="text/plain",
                            use_container_width=True
                        )

                except Exception as e:
                    st.error(
                        "Unable to generate the lesson. Check your "
                        "API key, model availability and internet connection."
                    )
                    st.error(f"Technical details: {e}")

# ---------------- AI CHAT ASSISTANT ----------------
elif page == "💬 AI Chat Assistant":

    st.markdown("## 💬 AI Chat Assistant")
    st.write(
        "Ask educational questions, request examples or improve "
        "your lesson plans with follow-up questions."
    )

    if not st.session_state.messages:
        st.info(
            "👋 Welcome! Try asking: "
            "\"Explain Design Thinking with a classroom example.\""
        )

        st.markdown("### Suggested questions")

        suggestions = [
            "Explain Design Thinking in simple English",
            "Create a science activity for Class 8",
            "Make a worksheet on water conservation"
        ]

        for suggestion in suggestions:
            if st.button(suggestion, use_container_width=True):
                st.session_state.pending_question = suggestion
                st.rerun()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    typed_question = st.chat_input(
        "Ask an educational question..."
    )

    pending_question = st.session_state.pop(
        "pending_question", None
    )

    user_question = typed_question or pending_question

    if user_question:
        st.session_state.messages.append({
            "role": "user",
            "content": user_question
        })

        with st.chat_message("user"):
            st.markdown(user_question)

        conversation = []

        for message in st.session_state.messages:
            role = (
                "Teacher"
                if message["role"] == "user"
                else "Assistant"
            )
            conversation.append(
                f"{role}: {message['content']}"
            )

        full_prompt = "\n\n".join(conversation)

        with st.chat_message("assistant"):
            with st.spinner("🤖 Preparing a clear explanation..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-3.5-flash-lite",
                        contents=full_prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_PROMPT,
                            temperature=0.5
                        )
                    )

                    answer = response.text

                    if not answer:
                        st.error(
                            "The AI returned an empty response. Please try again."
                        )
                    else:
                        st.markdown(answer)

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": answer
                        })

                except Exception as e:
                    st.error(
                        "Unable to contact Gemini. Please check your "
                        "API key, model availability and internet connection."
                    )
                    st.error(f"Technical details: {e}")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("""
<div class="footer">
    📘 Smart Education System · AI-powered learning and lesson planning
</div>
""", unsafe_allow_html=True)
