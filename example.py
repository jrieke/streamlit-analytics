import streamlit as st
import streamlit_analytics

with streamlit_analytics.track():
    st.title("Just a small test app")
    text = st.text_input("Enter some text")
    selected = st.selectbox("Select an option", ("option 1", "option 2", "option 3"))
    st.checkbox("Check this")
    st.checkbox("...or this")
    st.radio("Select one radio", ("radio 1", "radio 2"))
    st.multiselect("Select multiple", ("multiselect 1", "multiselect 2"))
    st.slider("Slide along")
    clicked = st.button("Click me")
