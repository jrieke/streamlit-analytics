import streamlit as st
import streamlit_analytics

with streamlit_analytics.track():
    st.title("Test app with all widgets")
    selected = st.selectbox("Select an option", ("option 1", "option 2", "option 3"))
    st.checkbox("Check this")
    st.checkbox("...or this")
    st.radio("Select one radio", ("radio 1", "radio 2"))
    st.multiselect("Select multiple", ("multiselect 1", "multiselect 2"))
    st.slider("Slide along")
    st.select_slider("Select slider", ("option 1", "option 2"))
    st.text_input("Enter some text")
    st.number_input("Input a number")
    st.text_area("text_area")
    clicked = st.button("Click me")
