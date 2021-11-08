import os


def delete_object(bucket_name, object_name):
    os.system(f"gsutil rm gs://{bucket_name}/{object_name}")


def delete_bucket(bucket_name):
    os.system(f"gsutil rm -r gs://{bucket_name}")

