import streamlit as st
import streamlit_analytics

with streamlit_analytics.track(firestore_key_file="firestore-key.json"):
    st.title(
        "Demo app for [streamlit-analytics](https://github.com/jrieke/streamlit-analytics)"
    )
    st.text_input("Write a greeting")
    st.selectbox("Select your favorite", ["Cats", "Dogs", "Flowers"])
    st.button("Click me")

    st.write("")
    st.write(
        "If there's nothing below, add `?analytics=on` to the URL to see some real action 👀"
    )
