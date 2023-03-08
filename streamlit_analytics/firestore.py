from google.cloud import firestore
from google.oauth2 import service_account
import streamlit as st
import json


def load(counts, service_account_json, collection_name, streamlit_secrets_firestore_key, firestore_project_name):
    """Load count data from firestore into `counts`."""
    if streamlit_secrets_firestore_key is not None:
        # Following along here https://blog.streamlit.io/streamlit-firestore-continued/#part-4-securely-deploying-on-streamlit-sharing for deploying to Streamlit Cloud with Firestore
        key_dict = json.loads(st.secrets[streamlit_secrets_firestore_key])
        creds = service_account.Credentials.from_service_account_info(key_dict)
        db = firestore.Client(
            credentials=creds, project=firestore_project_name)
        col = db.collection(collection_name)
        firestore_counts = col.document("counts").get().to_dict()
    else:
        db = firestore.Client.from_service_account_json(service_account_json)
        col = db.collection(collection_name)
        firestore_counts = col.document("counts").get().to_dict()

    # Update all fields in counts that appear in both counts and firestore_counts.
    if firestore_counts is not None:
        for key in firestore_counts:
            if key in counts:
                counts[key] = firestore_counts[key]


def save(counts, service_account_json, collection_name, streamlit_secrets_firestore_key, firestore_project_name):
    """Save count data from `counts` to firestore."""
    if streamlit_secrets_firestore_key is not None:
        # Following along here https://blog.streamlit.io/streamlit-firestore-continued/#part-4-securely-deploying-on-streamlit-sharing for deploying to Streamlit Cloud with Firestore
        key_dict = json.loads(st.secrets[streamlit_secrets_firestore_key])
        creds = service_account.Credentials.from_service_account_info(key_dict)
        db = firestore.Client(
            credentials=creds, project=firestore_project_name)
        col = db.collection(collection_name)
    else:
        db = firestore.Client.from_service_account_json(service_account_json)
    col = db.collection(collection_name)
    doc = col.document("counts")
    doc.set(counts)  # creates if doesn't exist
