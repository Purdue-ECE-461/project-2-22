from Actions import Delete
from Actions import List


def reset_default(main_bucket):
    list_objects_main_bucket = List.list_objects_in_bucket(main_bucket)
    for object_main in list_objects_main_bucket:
        object_main_name = object_main.name
        Delete.delete_object_safe(main_bucket, object_main_name)

    return
