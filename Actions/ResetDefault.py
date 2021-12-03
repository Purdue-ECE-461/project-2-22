import Delete
import List


def reset_default(main_bucket):
    # Don't delete the bucket, but the objects in the bucket
    # Get list of buckets

    list_objects_main_bucket = List.list_objects_in_bucket(main_bucket)
    for object_main in list_objects_main_bucket:
        object_main_name = object_main.name
        Delete.delete_object(main_bucket, object_main_name)

    return
