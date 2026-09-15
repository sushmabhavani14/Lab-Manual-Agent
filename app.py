import streamlit as st
from google import genai
import os
import time

# -----------------------------
# Page settings
# -----------------------------

st.set_page_config(
    page_title="Lab Manual Agent",
    page_icon="🧪",
    layout="wide"
)

# -----------------------------
# Gemini client
# -----------------------------

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY is not configured.")
    st.stop()

client = genai.Client(api_key=api_key)

# -----------------------------
# Agent instructions
# -----------------------------

SYSTEM_PROMPT = """
You are an AI Lab Manual Agent for college students.

Your job is to explain laboratory experiments in simple,
beginner-friendly English.

For every experiment provide:

1. Experiment Title
2. Aim
3. Requirements
4. Theory
5. Algorithm / Procedure
6. Source Code
7. Explanation of the Code
8. Expected Output
9. Viva Questions and Answers
10. Common Errors
11. Conclusion

Rules:
- Use simple English.
- Explain difficult terms.
- Give beginner-friendly code.
- Do not use unnecessary advanced technologies.
- Give practical college-level explanations.
- Give at least 5 viva questions with answers.
- Format the answer clearly using headings.
"""

# -----------------------------
# User Interface
# -----------------------------

st.title("🧪 Lab Manual Agent")

st.write(
    "Your AI assistant for understanding laboratory experiments, "
    "code, output and viva questions."
)

st.divider()

subject = st.selectbox(
    "📚 Select Subject",
    [
        "Python",
        "C Programming",
        "Java",
        "Data Structures",
        "DBMS",
        "Machine Learning",
        "Data Mining",
        "Artificial Intelligence"
    ]
)

experiment = st.text_area(
    "🔬 Enter your experiment",
    placeholder="Example: Implement Linear Regression using Python",
    height=120
)

generate = st.button(
    "🚀 Generate Lab Manual",
    use_container_width=True
)

# -----------------------------
# Generate response
# -----------------------------

if generate:

    if not experiment.strip():

        st.warning("⚠️ Please enter an experiment.")

    else:

        # IMPORTANT:
        # prompt is created BEFORE it is sent to Gemini

        prompt = SYSTEM_PROMPT + f"""

Subject:
{subject}

Student's Experiment:
{experiment}

Generate the complete lab manual now.
"""

        with st.spinner("🤖 Preparing your lab manual..."):

            response = None

            for attempt in range(3):

                try:

                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=prompt
                    )

                    break

                except Exception as e:

                    if "503" in str(e) and attempt < 2:

                        time.sleep(5)

                    else:

                        st.error(
                            "⚠️ Gemini is temporarily unavailable. "
                            "Please try again after a few seconds."
                        )

                        break

        # -----------------------------
        # Display response
        # -----------------------------

        if response is not None:

            st.success("✅ Lab manual generated successfully!")

            st.divider()

            st.markdown(response.text)
