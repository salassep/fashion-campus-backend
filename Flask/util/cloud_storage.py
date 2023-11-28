import os
from google.cloud import storage
from dotenv import load_dotenv

def get_bucket():
    load_dotenv()
    client = storage.Client.from_service_account_json(os.getenv("GCS_CREDENTIALS"))
    bucket = client.get_bucket(os.getenv("GCS_BUCKET"))
    return bucket