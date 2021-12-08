import pytest
from Actions import Create, Delete, Upload, Download, List, ResetDefault, Update, Search
# import Update, Decode
# import Download


def test_create_bucket(bucket):
    Create.create_bucket(bucket)


def test_upload_file(bucket, filename):
    Upload.upload_file(filename, bucket)
    return


def test_list_buckets():
    bucket_list = List.list_buckets()
    print(bucket_list)


def test_list_objects(bucket):
    object_list = List.list_objects_in_bucket(bucket)
    print(object_list)


def test_delete_object(bucket, object_name):
    Delete.delete_object(bucket, object_name)


def test_delete_bucket(bucket):
    Delete.delete_bucket(bucket)


def test_download(downloading_textfile, destination_bucket_gcp):
    Download.download_text(downloading_textfile, destination_bucket_gcp)


def test_update(bucket_name, encoded_zipfile_string, filename_to_gcp):
    Update.update_file(bucket_name, encoded_zipfile_string, filename_to_gcp)


def test_reset_default(main_bucket):
    ResetDefault.reset_default(main_bucket)


def run_test():
    # Missing testing: Rate
    # Need to do error handling later. Make sure that this is what we are using

    MAIN_BUCKET_NAME = "acme_corporation_general"
    file = "/proj2_code_github/project-2-22/TestHelperFiles/images.zip"
    file_update = "/proj2_code_github/project-2-22/TestHelperFiles/images1.zip"
    local_folder = "C:/Users/sguad/A_Desktop/College/ECE_461/Project2/proj2_code_github" \
                   "/project-2-22/TestHelperFiles/"

    file_to_encode = "C:\\Users\\sguad\\Downloads\\express-master.zip"
    file_to_decode = "C:\\Users\\sguad\\Downloads\\expressjs_decoded.zip"
    folder_dest_text = "C:\\Users\\sguad\\Downloads"
    file_to_update_with = "C:\\Users\\sguad\\Downloads\\test_update.zip"

    # test_create_bucket(bucket_name)
    # test_list_buckets()
    # test_upload_file(bucket_name, file)
    # test_list_objects(bucket_name)
    # test_download("expressjs.txt", MAIN_BUCKET_NAME)
    # string_to_update = Decode.encode_zip(file_to_update_with)
    # print(string_to_update)
    # test_update(bucket_name=MAIN_BUCKET_NAME,
    #             encoded_zipfile_string=string_to_update,
    #             filename_to_gcp="expressjs")
    # test_delete_object(bucket_name, "images.zip")
    # test_delete_bucket(bucket_name)
    # test_list_buckets()
    # test_reset_default("main_bucket")