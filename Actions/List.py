from google.cloud import storage


def list_buckets():
    client = storage.Client()
    all_buckets = list(client.list_buckets())
    return all_buckets


def list_objects_in_bucket(bucket_name):
    client = storage.Client()
    all_blobs = list(client.list_blobs(bucket_name))
    return all_blobs
