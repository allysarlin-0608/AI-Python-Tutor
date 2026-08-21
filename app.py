import streamlit as st

st.title("AI Python Tutor")

st.write("Ask a question about Python.")

question = st.text_input("Your question")

if st.button("Ask"):
    if question:
        st.write("You asked:", question)
    else:
        st.error("Please enter a question.")
