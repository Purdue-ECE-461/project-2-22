from Actions import Delete
from Actions import Upload


def update_file(bucket_name, object_name, content):
    Delete.delete_object(bucket_name, object_name + '.txt')
    Upload.upload_file(object_name, content, bucket_name)

