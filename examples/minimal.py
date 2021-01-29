import streamlit as st
import streamlit_analytics

with streamlit_analytics.track():
    st.text_input("Write something")
    st.button("Click me")

    st.write("")
    st.write("Add `?analytics=on` to the URL to see some action 👀")
