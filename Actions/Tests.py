import pytest
import Create, Delete, Upload, Download, List, Rate, ResetDefault, Update, Search


# Create bucket Testing
def test_create_bucket(bucket):
    Create.create_bucket(bucket)


def test_upload_file(bucket, filename):
    Upload.upload_file(filename, f"gs://{bucket}")
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


def test_download(bucket, filename_gcp, folder_dest_local):
    Download.download_file(bucket, filename_gcp, folder_dest_local)


def test_update(bucket_name, object_name, source_file_local):
    Update.update_file(bucket_name, object_name, source_file_local)


def test_reset_default(main_bucket):
    ResetDefault.reset_default(main_bucket)


def run_test():
    # Missing testing: Rate
    # Need to do error handling later. Make sure that this is what we are using

    bucket_name = "bucket_testing_sguada1"
    file = "/proj2_code_github/project-2-22/TestHelperFiles/images.zip"
    file_update = "/proj2_code_github/project-2-22/TestHelperFiles/images1.zip"
    local_folder = "C:/Users/sguad/A_Desktop/College/ECE_461/Project2/proj2_code_github" \
                   "/project-2-22/TestHelperFiles/"
    # test_create_bucket(bucket_name)
    # test_list_buckets()
    # test_upload_file(bucket_name, file)
    # test_list_objects(bucket_name)
    # test_download(bucket_name, "images.zip", local_folder)
    # test_update(bucket_name, "images.zip", file_update)
    # test_delete_object(bucket_name, "images.zip")
    # test_delete_bucket(bucket_name)
    # test_list_buckets()
    # test_reset_default("main_bucket")
