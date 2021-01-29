"""This demo is run through Streamlit Sharing."""

# Install streamlit-analytics here because it's not included in requirements.txt.
import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit_analytics"])

import streamlit as st
import streamlit_analytics

with streamlit_analytics.track():
    st.text_input("Write something")
    st.button("Click me")

    st.write("")
    st.write("Add `?analytics=on` to the URL to see some action 👀")
