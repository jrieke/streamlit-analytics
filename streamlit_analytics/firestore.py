from google.cloud import firestore


def load(counts, service_account_json, collection_name):
    """Load count data from firestore into `counts`."""

    # Retrieve data from firestore.
    db = firestore.Client.from_service_account_json(service_account_json)
    col = db.collection(collection_name)
    firestore_counts = col.document("counts").get().to_dict()

    # Update all fields in counts that appear in both counts and firestore_counts.
    if firestore_counts is not None:
        for key in firestore_counts:
            if key in counts:
                counts[key] = firestore_counts[key]


def save(counts, service_account_json, collection_name):
    """Save count data from `counts` to firestore."""
    db = firestore.Client.from_service_account_json(service_account_json)
    col = db.collection(collection_name)
    doc = col.document("counts")
    doc.set(counts)  # creates if doesn't exist
