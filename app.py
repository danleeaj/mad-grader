import streamlit as st
import main

with st.form("debate_form", border=False):

    context = st.text_input("Context", placeholder="Enter the body of your question here to improve grading accuracy. (Optional)")
    rubric_component = st.text_input("Rubric component", placeholder="Enter the grading rubric component here.")
    student_response = st.text_input("Student response", placeholder="Enter the student response you want to grade here.")

    submitted = st.form_submit_button(label="Submit", help="Click to query the API to initiate a multi-agent debate session.")

    if submitted:
        print("Submitted")
        history = main.debate(rubric_component, student_response, context)

        for round in history:
            st.write(round)