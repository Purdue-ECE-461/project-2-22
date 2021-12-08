import os
from Actions import ActionHelper
from Actions import Search
from google.cloud import storage


def download_file(bucket, file_to_download, destination_folder_local):
    if ActionHelper.check_folder_path(destination_folder_local):
        os.system(f"gsutil -m cp -r gs://{bucket}/{file_to_download} {destination_folder_local}")
    else:
        print("Folder path does not exists in local machine")


def download_text(filename_to_gcp, destination_bucket_gcp):
    # filename_to_gcp: the name of the file that is in gcp
    client = storage.Client()
    bucket = client.get_bucket(destination_bucket_gcp)
    # Should check if the file is there or not
    if Search.find_object(destination_bucket_gcp, filename_to_gcp):
        blob = bucket.blob(filename_to_gcp)
        return blob.download_as_text()
    else:
        return "Message from Download.py: File wasn't found in GCP"


def download_bucket(source_bucket_gcp, destination_folder_local):
    if ActionHelper.check_folder_path(destination_folder_local):
        os.system(f"gsutil -m cp -r {source_bucket_gcp} {destination_folder_local}")
    else:
        print("Folder path does not exists in local machine")

