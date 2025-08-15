from cotizador.db import get_db

# Use a fixed, known ID for the single company configuration document
CONFIG_DOCUMENT_ID = "main_config"

def get_company_config():
    """
    Retrieves the company configuration document from Firestore.
    If it doesn't exist, it returns an empty dictionary.
    """
    db = get_db()
    if not db:
        return {}
    try:
        doc_ref = db.collection('empresa').document(CONFIG_DOCUMENT_ID)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            # The document doesn't exist yet, return a default structure
            return {}
    except Exception as e:
        print(f"An error occurred while fetching company config: {e}")
        return {}

def update_company_config(data):
    """
    Updates the company configuration document in Firestore.
    It uses `set` with `merge=True` to create the document if it doesn't exist,
    or update it if it does.
    """
    db = get_db()
    if not db:
        return None
    try:
        doc_ref = db.collection('empresa').document(CONFIG_DOCUMENT_ID)
        doc_ref.set(data, merge=True)
        # Return the updated data by fetching it again
        updated_doc = doc_ref.get()
        return updated_doc.to_dict()
    except Exception as e:
        print(f"An error occurred while updating company config: {e}")
        return None
