import streamlit as st
import main

st.header("Welcome to :blue[_mad-grader_]", divider="rainbow")
st.markdown(''':blue[mad-grader] (working title) is an automatic grading program that utilizes multi-agent debate to ensure consistency and accuracy in delivering verdicts on whether a rubric component is satisfied.
            \nThis is a demonstration of the multi-agent debate technology it utlizes. Specifically, the graders use OpenAI's GPT 3.5 and Anthropic's Claude 3 Haiku models, while the evaluator uses the same as the latter. We're currently working on implementing more models, such as Google's Gemini, as well as experimenting with locally-run LLMs for lower cost.
            ''')

st.divider()
st.caption('Developed by An Jie Lee, 2024 // [Github](https://github.com/danleeaj)')
