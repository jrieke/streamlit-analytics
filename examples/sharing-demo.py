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
    streamlit_analytics.counts["widgets"] = {
        "Write your name": {
            " ": 44,
            "hello": 3,
            "HIIII its Marisa :) ": 1,
            "CATS CATS CATS are the wiiiiiiners ahahahahhahahaha ": 1,
            "What am I supposed to write here?": 1,
            "hello ": 1,
            "hello from Abhi": 1,
            "Never gonna ": 1,
            "Never gonna give you uuuuuppp !": 1,
            "Never gonna": 1,
            "Hey b": 1,
            "Ah I guess text input is saved when I select my favorite, though I did not press enter in the text_input": 1,
            "something": 1,
        },
        "Click me": 18,
        "Select your favorite": {"cat": 49, "dog": 5, "flower": 6},
    }
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
