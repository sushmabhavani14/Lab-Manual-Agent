import streamlit as st
from google import genai
import os

st.set_page_config(
    page_title="Lab Manual Agent",
    page_icon="🧪",
    layout="wide"
)

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

SYSTEM_PROMPT = """
You are an AI Lab Manual Agent for college students.

Explain laboratory experiments in simple English.

For every experiment provide:

1. Experiment Title
2. Aim
3. Requirements
4. Theory
5. Algorithm / Procedure
6. Source Code
7. Explanation of Code
8. Expected Output
9. Viva Questions and Answers
10. Common Errors
11. Conclusion

Use beginner-friendly explanations and code.
Give at least 5 viva questions with answers.
"""

st.title("🧪 Lab Manual Agent")
st.write("Your AI assistant for laboratory experiments")

subject = st.selectbox(
    "Select Subject",
    [
        "Python",
        "Java",
        "C Programming",
        "Data Structures",
        "DBMS",
        "Machine Learning",
        "Data Mining"
    ]
)

experiment = st.text_area(
    "Enter your experiment",
    placeholder="Example: Implement Linear Regression using Python"
)

if st.button("🚀 Generate Lab Manual"):

    if experiment.strip():

        with st.spinner("Generating your lab manual..."):

            prompt = SYSTEM_PROMPT + f"""

Subject: {subject}

Experiment:
{experiment}
"""

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

        st.markdown(response.text)

    else:
        st.warning("Please enter an experiment.")
