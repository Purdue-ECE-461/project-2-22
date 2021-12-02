import os
from Actions import ActionHelper


def download_file(bucket, file_to_download, destination_folder_local):
    if ActionHelper.check_folder_path(destination_folder_local):
        os.system(f"gsutil -m cp -r gs://{bucket}/{file_to_download} {destination_folder_local}")
    else:
        print("Folder path does not exists in local machine")


def download_bucket(source_bucket_gcp, destination_folder_local):
    if ActionHelper.check_folder_path(destination_folder_local):
        os.system(f"gsutil -m cp -r {source_bucket_gcp} {destination_folder_local}")
    else:
        print("Folder path does not exists in local machine")

