import streamlit as st
import main

st.header("Welcome to :blue[_mad-grader_]", divider="rainbow")
st.markdown(''':blue[mad-grader] (working title) is an automatic grading program that utilizes multi-agent debate to ensure consistency and accuracy in delivering verdicts on whether a rubric component is satisfied.
            \nThis is a demonstration of the multi-agent debate technology it utlizes. Specifically, the graders use OpenAI's GPT 3.5 and Anthropic's Claude 3 Haiku models, while the evaluator uses the same as the latter. We're currently working on implementing more models, such as Google's Gemini, as well as experimenting with locally-run LLMs for lower cost.
            ''')

with st.form("debate_form", border=False):

    context = st.text_input("Context", placeholder="Enter the body of your question here to improve grading accuracy. (Optional)", help="The user can optionally enter the body of the question for the program to use as a reference when grading the response. This is particularly useful for conditional rubric components, such as 'no irrelevant information'. The program will use the context as a reference to determine whether the response is relevant to the question.")
    rubric_component = st.text_input("Rubric component", placeholder="Enter the grading rubric component here.", help="The rubric component is what the response will be graded off of. If the rubric component is satisfied by the response, then 'true' is returned, else, 'false' is returned.")
    student_response = st.text_input("Student response", placeholder="Enter the student response you want to grade here.", help="The student response is where the response to be graded is entered.")
    
    submitted = st.form_submit_button(label="Submit", help="Click to query the API to initiate a multi-agent debate session.")

    if submitted:

        history = main.debate(rubric_component, student_response, context)

        if not history:
            st.error('Error: No history was provided. Please let the developer know and try again in 5 minutes.', icon="🚨")

        for count, round in enumerate(history):
            st.subheader(f"Round {count + 1}", divider="gray")

            st.markdown(f'''Evaluation: The graders {':green[do]' if round['Evaluator']['gradersAgree'] else ':red[do not]'} agree. The consensus reached is {round['Evaluator']['consensusEvaluation']}.
                        ''')

            st.write(round)
    

st.divider()
st.caption('Developed by An Jie Lee, 2024 // [Github](https://github.com/danleeaj)')
