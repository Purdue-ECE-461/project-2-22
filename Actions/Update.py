import Delete
import Upload
import ActionHelper


def update_file(bucket_name, object_name, source_file_local):
    # Might need to add a way to look for a file similar to this one just in case
    if ActionHelper.check_file(source_file_local):
        Delete.delete_object(bucket_name, object_name)
        Upload.upload_file(source_file_local, bucket_name)
    else:
        print("File path doesn't exists")
    return

