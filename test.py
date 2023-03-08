import streamlit as st
import streamlit_analytics
import os

with streamlit_analytics.track(firestore_collection_name="data", streamlit_secrets_firestore_key="firebase", firestore_project_name=os.environ["CURRI_FIREBASE_PROJECT_NAME"]):
    st.text_input("Write something")
    st.button("Click me")
