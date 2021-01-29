"""This demo is run through Streamlit Sharing."""

import streamlit as st

try:
    import streamlit_analytics
except ImportError:
    # Install streamlit-analytics on first run (not included in requirements.txt).
    import subprocess
    import sys

    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "streamlit_analytics"]
    )
    import streamlit_analytics

with streamlit_analytics.track():
    st.title(
        "Demo app for [streamlit-analytics](https://github.com/jrieke/streamlit-analytics)"
    )
    st.text_input("Write a greeting")
    st.selectbox("Select your favorite", ["Cats", "Dogs", "Flowers"])
    st.button("Click me")

    st.write("")
    st.write("If there's nothing below, add `?analytics=on` to the URL to see the analytics dashboard 👀")
