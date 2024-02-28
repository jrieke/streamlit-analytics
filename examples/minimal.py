import platform
import streamlit as st
import streamlit_analytics

# Get the software versions
python_version = platform.python_version()
streamlit_version = st.__version__
streamlit_analytics_version = streamlit_analytics.__version__

# Print the versions
st.write(f"Python version: {python_version}")
st.write(f"Streamlit version: {streamlit_version}")
st.write(f"streamlit_analytics version: {streamlit_analytics_version}")

st.markdown("---")

with streamlit_analytics.track():
    st.text_input("Write your name")
    st.selectbox("Select your favorite", ["cat", "dog", "flower"])
    st.button("Click me")


st.title("A [link]()")
