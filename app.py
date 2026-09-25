import os
import streamlit as st

from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Lesson Assistant",
    page_icon="📚",
    layout="centered"
)

# Get API key from .env or Streamlit Secrets
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = None

# Check API key
if not api_key:
    st.error("Gemini API key is missing.")
    st.stop()

# Create Gemini client
client = genai.Client(api_key=api_key)

# System prompt
SYSTEM_PROMPT = """
You are AI Lesson Assistant, an AI assistant for school teachers.

Your purpose is to help teachers create creative, practical and
step-by-step classroom activities using Design Thinking.

You must focus on:
- Lesson planning
- Creative classroom activities
- Design Thinking
- Student teamwork
- Problem solving
- Worksheets
- Real-world classroom problems

When creating a lesson, include:

1. Learning Objective
2. Activity Name
3. Empathize
4. Define
5. Ideate
6. Prototype
7. Test
8. Group Activity
9. Worksheet/Task
10. Expected Learning Outcome

Use simple English and make activities suitable for the given class.

If the user asks something unrelated to education or lesson planning,
politely redirect them toward lesson planning and classroom activities.
"""

# App title
st.title("📚 AI Lesson Assistant")

st.caption(
    "Smart Education System – AI-powered support for creative classroom activities"
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.header("⚙️ Controls")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    st.write("**Project:** Smart Education System")
    st.write("**Module:** AI Lesson Assistant")

# Lesson details
st.subheader("Create a Lesson")

subject = st.text_input(
    "📖 Subject",
    placeholder="Example: Science"
)

grade = st.text_input(
    "🎓 Class / Grade",
    placeholder="Example: Class 8"
)

topic = st.text_input(
    "📌 Topic",
    placeholder="Example: Water Conservation"
)

objective = st.text_area(
    "🎯 Learning Objective",
    placeholder="Example: Students will understand the importance of saving water."
)

# Generate lesson
if st.button("✨ Generate Lesson", use_container_width=True):

    if not subject or not grade or not topic:
        st.warning("Please enter Subject, Class/Grade and Topic.")

    else:
        lesson_request = f"""
Create a complete creative classroom lesson.

Subject: {subject}
Class/Grade: {grade}
Topic: {topic}
Learning Objective: {objective if objective else "Create a suitable learning objective."}

Use the following structure:

1. Learning Objective
2. Activity Name
3. Empathize
4. Define
5. Ideate
6. Prototype
7. Test
8. Group Activity
9. Worksheet/Task
10. Expected Learning Outcome

Make it practical and easy for a teacher to conduct in a classroom.
"""

        with st.spinner("🤖 Creating your lesson..."):

            try:
                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=lesson_request,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT
                    )
                )

                answer = response.text

                st.session_state.messages.append({
                    "role": "user",
                    "content": lesson_request
                })

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

                st.success("Lesson generated successfully!")

            except Exception as e:
                st.error(
                    "Sorry, I could not generate the lesson. "
                    "Please check your Gemini API key and internet connection."
                )
                st.error(f"Error: {e}")

# Display chat history
for message in st.session_state.messages:

    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["content"])

    elif message["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(message["content"])

# Follow-up chat
user_question = st.chat_input(
    "Ask the AI Lesson Assistant a follow-up question..."
)

if user_question:

    with st.chat_message("user"):
        st.write(user_question)

    # Build conversation
    conversation = []

    for message in st.session_state.messages:
        conversation.append(
            f"{message['role']}: {message['content']}"
        )

    conversation.append(f"user: {user_question}")

    full_prompt = "\n\n".join(conversation)

    with st.chat_message("assistant"):

        with st.spinner("🤖 Thinking..."):

            try:
                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT
                    )
                )

                answer = response.text

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "user",
                    "content": user_question
                })

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error(
                    "Sorry, something went wrong while contacting Gemini."
                )
                st.error(f"Error: {e}")