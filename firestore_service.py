import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import random
import argparse
import os

def initialize_firestore(service_account_path):
    """
    Initializes the Firebase Admin SDK.
    """
    if not os.path.exists(service_account_path):
        raise FileNotFoundError(f"Service account key not found at: {service_account_path}")
    
    try:
        cred = credentials.Certificate(service_account_path)
        firebase_admin.initialize_app(cred)
        print("Firebase Admin SDK initialized successfully.")
    except Exception as e:
        print(f"Error initializing Firebase Admin SDK: {e}")
        exit()

def generate_document_data(index):
    """
    Generates a dictionary representing a single Firestore document.
    """
    return {
        "document_id": f"doc_{index}",
        "timestamp": firestore.SERVER_TIMESTAMP,
        "random_number": random.randint(1, 100000),
        "description": f"This is document number {index} generated on {datetime.datetime.now().isoformat()}.",
        "status": random.choice(["active", "inactive", "pending"]),
        "tags": random.sample(["tagA", "tagB", "tagC", "tagD", "tagE"], random.randint(1, 3)),
        "nested_data": {
            "key1": "valueA",
            "key2": random.uniform(0, 1),
            "key3": ["item1", "item2"]
        }
    }

def write_documents_to_firestore(num_documents, collection_name="test_documents"):
    """
    Writes a specified number of documents to a Firestore collection.
    """
    db = firestore.client()
    batch = db.batch()
    
    print(f"\nStarting to write {num_documents} documents to collection '{collection_name}'...")
    start_time = datetime.datetime.now()
    
    for i in range(1, num_documents + 1):
        doc_data = generate_document_data(i)
        doc_ref = db.collection(collection_name).document()
        batch.set(doc_ref, doc_data)
        
        if i % 500 == 0:  # Commit every 500 documents (Firestore batch limit is 500)
            try:
                batch.commit()
                print(f"  Committed {i} documents...")
                batch = db.batch() # Start a new batch
            except Exception as e:
                print(f"Error committing batch at document {i}: {e}")
                # You might want to implement retry logic here
                batch = db.batch() # Try to continue with a new batch to avoid stalling
                
    # Commit any remaining documents in the last batch
    try:
        batch.commit()
        print(f"  Committed final batch.")
    except Exception as e:
        print(f"Error committing final batch: {e}")

    end_time = datetime.datetime.now()
    duration = end_time - start_time
    print(f"\nFinished writing {num_documents} documents.")
    print(f"Total time taken: {duration}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Write documents to Firestore.")
    parser.add_argument(
        "--docs", 
        type=int, 
        default=5000, 
        choices=[5000, 60000],
        help="Number of documents to write (5000 or 60000). Defaults to 5000."
    )
    parser.add_argument(
        "--collection", 
        type=str, 
        default="test_documents", 
        help="Name of the Firestore collection. Defaults to 'test_documents'."
    )
    parser.add_argument(
        "--service-account-path", 
        type=str, 
        default="path/to/your/serviceAccountKey.json", # <--- CHANGE THIS PATH
        help="Path to your Firestore service account key JSON file."
    )

    args = parser.parse_args()

    # --- IMPORTANT: CHANGE THIS PATH TO YOUR SERVICE ACCOUNT KEY ---
    # For example: service_account_key_path = "my-project-12345-firebase-adminsdk-xxxxx-xxxxxxxxxx.json"
    service_account_key_path = args.service_account_path 
    # ---------------------------------------------------------------

    initialize_firestore(service_account_key_path)
    write_documents_to_firestore(args.docs, args.collection)
