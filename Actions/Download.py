import os
from google.cloud import storage


def download_file(bucket, file_to_download, destination_folder_local):
    os.system(f"gsutil -m cp -r gs://{bucket}/{file_to_download} {destination_folder_local}")


def download_bucket(source_bucket_gcp, destination_folder_local):
    os.system(f"gsutil -m cp -r {source_bucket_gcp} {destination_folder_local}")
