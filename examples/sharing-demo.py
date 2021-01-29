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
    name = st.text_input("Write your name")
    fav = st.selectbox("Select your favorite", ["cat", "dog", "flower"])
    clicked = st.button("Click me")
    if clicked:
        st.write(
            f"Hello {name}, here's a {fav} for you: :{fav.replace('flower', 'sunflower')}:"
        )

    st.write("")
    st.write(
        "...and now add `?analytics=on` to the URL to see the analytics dashboard 👀"
    )
