import os
from Actions import ActionHelper


def upload_file(source_file_local, destination_bucket_gcp):
    if ActionHelper.check_file(source_file_local):
        os.system(f"gsutil cp {source_file_local} {destination_bucket_gcp}")
    else:
        print("File path doesn't exists")

