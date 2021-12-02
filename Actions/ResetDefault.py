from Actions import Delete
from Actions import List


def reset_default(main_bucket):
    # Don't delete the bucket, but the objects in the bucket
    # Get list of buckets
    list_buckets = List.list_buckets()
    for bucket in list_buckets:
        bucket_name = bucket.name
        if bucket_name == main_bucket:
            list_objects_main_bucket = List.list_objects_in_bucket(bucket_name)
            for object_main in list_objects_main_bucket:
                object_main_name = object_main.name
                Delete.delete_object(bucket_name, object_main_name)
        else:
            Delete.delete_bucket(bucket_name)

    return
