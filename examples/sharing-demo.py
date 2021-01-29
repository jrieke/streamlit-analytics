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
    st.text_input("Write something")
    st.button("Click me")

    st.write("")
    st.write("Add `?analytics=on` to the URL to see some action 👀")
