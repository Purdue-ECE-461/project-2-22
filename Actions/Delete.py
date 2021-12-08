import os
from google.cloud import storage


def delete_object_safe(bucket_name, object_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.delete()


def delete_object(bucket_name, object_name):
    os.system(f"gsutil rm gs://{bucket_name}/{object_name}")


def delete_bucket(bucket_name):
    os.system(f"gsutil rm -r gs://{bucket_name}")

