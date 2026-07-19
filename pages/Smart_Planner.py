import streamlit as st

st.title("Smart Planner")
st.write("Plan your week ahead with AI-assisted scheduling.")
date = st.date_input("Select Date")
plan = st.text_input("Enter your primary goal for the day")
if st.button("Generate Plan"):
    st.success(f"Plan for {date} created! Goal: {plan}")
