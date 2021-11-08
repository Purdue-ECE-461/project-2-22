import os
from google.cloud import storage


def upload_file(source_file_local, destination_bucket_gcp):
    os.system(f"gsutil cp {source_file_local} {destination_bucket_gcp}")

