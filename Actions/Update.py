import os
from google.cloud import storage


def update_file(bucket_name, object_name, source_file_local):
    # Might need to add a way to look for a file similar to this one just in case
    delete_object(bucket_name, object_name)
    upload_file(source_file_local, bucket_name)
    return


def upload_file(source_file_local, destination_bucket_gcp):
    os.system(f"gsutil cp {source_file_local} gs://{destination_bucket_gcp}/")


def delete_object(bucket_name, object_name):
    os.system(f"gsutil rm gs://{bucket_name}/{object_name}")
