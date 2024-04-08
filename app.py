import streamlit as st
import main

st.header("Welcome to :blue[_mad-debate_]", divider="rainbow")
st.markdown(''':blue[mad-debate] (working title) is an automatic grading program that utilizes multi-agent debate to ensure consistency and accuracy in delivering verdicts on whether a rubric component is satisfied.
            ''')

with st.form("debate_form", border=False):

    context = st.text_input("Context", placeholder="Enter the body of your question here to improve grading accuracy. (Optional)", help="The user can optionally enter the body of the question for the program to use as a reference when grading the response. This is particularly useful for conditional rubric components, such as 'no irrelevant information'. The program will use the context as a reference to determine whether the response is relevant to the question.")
    rubric_component = st.text_input("Rubric component", placeholder="Enter the grading rubric component here.", help="The rubric component is what the response will be graded off of. If the rubric component is satisfied by the response, then 'true' is returned, else, 'false' is returned.")
    student_response = st.text_input("Student response", placeholder="Enter the student response you want to grade here.", help="The student response is where the response to be graded is entered.")
    
    submitted = st.form_submit_button(label="Submit", help="Click to query the API to initiate a multi-agent debate session.")

    if submitted:
        print("Submitted")
        history = main.debate(rubric_component, student_response, context)

        for round in history:
            st.write(round)
    
