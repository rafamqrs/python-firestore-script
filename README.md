# Firestore Document Generator

---

This Python script provides a simple yet effective way to populate your Firestore database with a specified number of documents. It's ideal for testing, development, or generating sample data.

## Features

* **Flexible Document Count:** Easily write either **5,000** or **60,000** documents.
* **Customizable Collection Name:** Specify the Firestore collection where documents will be stored.
* **Batch Writing:** Uses Firestore's batching capabilities for efficient bulk inserts, adhering to the 500-document batch limit.
* **Realistic Data Generation:** Each document includes various data types like timestamps, numbers, strings, arrays, and nested objects.
* **Progress Tracking:** Provides real-time updates on document writing progress.
* **Command-Line Interface:** Use arguments to configure the number of documents and collection name.

---

## Prerequisites

Before running this script, ensure you have the following:

1.  **Google Cloud Project:** A Google Cloud project with **Firestore enabled**.
2.  **Service Account Key:** Download your **service account key** (a JSON file) from the Google Cloud Console.
    * Go to "IAM & Admin" > "Service Accounts."
    * Create a new service account or select an existing one.
    * Under "Keys," click "Add Key" > "Create new key" > "JSON."
    * Save this JSON file securely.
3.  **Python 3.x:** Make sure you have Python installed.
4.  **Firebase Admin SDK:** Install the necessary Python library:
    ```bash
    pip install firebase-admin
    ```

---

## Installation

1.  **Clone this repository** (or copy the script directly).
2.  **Place your service account key** in the same directory as the script, or note its full path.

---

## Usage

1.  **Update Service Account Path:** Open the `firestore_writer.py` file and locate the line:
    ```python
    service_account_key_path = "path/to/your/serviceAccountKey.json" # <--- CHANGE THIS PATH
    ```
    Replace `"path/to/your/serviceAccountKey.json"` with the actual path to your downloaded JSON service account key. For example:
    ```python
    service_account_key_path = "my-project-12345-firebase-adminsdk-xxxxx-xxxxxxxxxx.json"
    ```

2.  **Run the script from your terminal:**

    * **Write 5,000 documents (default):**
        ```bash
        python firestore_writer.py
        ```

    * **Write 60,000 documents:**
        ```bash
        python firestore_writer.py --docs 60000
        ```

    * **Specify a custom collection name (e.g., `my_test_data`):**
        ```bash
        python firestore_writer.py --collection my_test_data
        ```

    * **Combine options (e.g., 60,000 documents in `large_dataset` collection):**
        ```bash
        python firestore_writer.py --docs 60000 --collection large_dataset
        ```

    * **Explicitly provide the service account path (if it's not in the same directory):**
        ```bash
        python firestore_writer.py --service-account-path /Users/youruser/keys/my-project-key.json --docs 60000
        ```

The script will output progress messages and the total time taken to write the documents.

---

## Document Structure

Each generated document will have a structure similar to this:

```json
{
  "document_id": "doc_1",
  "timestamp": "2024-01-01T12:00:00Z" (Firestore Server Timestamp),
  "random_number": 12345,
  "description": "This is document number 1 generated on 2024-01-01T12:00:00.000000.",
  "status": "active", // or "inactive", "pending"
  "tags": ["tagA", "tagC"],
  "nested_data": {
    "key1": "valueA",
    "key2": 0.54321,
    "key3": ["item1", "item2"]
  }
}
