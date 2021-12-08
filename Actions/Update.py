from Actions import Delete
from Actions import Upload
# import Delete
# import Upload


def update_file(bucket_name, encoded_zipfile_string, filename_to_gcp):
    Delete.delete_object(bucket_name, filename_to_gcp)
    Upload.upload_file(filename_to_gcp, encoded_zipfile_string, bucket_name)
    return

