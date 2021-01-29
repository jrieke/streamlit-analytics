import streamlit as st
import streamlit_analytics


with streamlit_analytics.track():  # firestore_key_file="firestore-key.json"):

    streamlit_analytics.counts["widgets"] = {"Write your name": {"foo": 1}}
    st.text_input("Write your name")
    st.selectbox("Select your favorite", ["cat", "dog", "flower"])
    st.button("Click me")

