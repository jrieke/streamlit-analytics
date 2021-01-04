import streamlit as st
import streamlit_analytics
from datetime import datetime

with streamlit_analytics.track():
    st.title("Test app with all widgets")
    st.checkbox("checkbox")
    st.button("button")
    st.radio("radio", ("option 1", "option 2"))
    st.selectbox("selectbox", ("option 1", "option 2", "option 3"))
    st.multiselect("multiselect", ("option 1", "option 2"))
    st.slider("slider")
    st.select_slider("select_slider", ("option 1", "option 2"))
    st.text_input("text_input")
    st.number_input("number_input")
    st.text_area("text_area")
    st.date_input("date_input")
