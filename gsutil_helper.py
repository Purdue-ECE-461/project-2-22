import os
import pathlib
from google.cloud import storage
from zipfile36 import ZipFile, ZipInfo
import io

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:/Users/sguad/A_Desktop/College/ECE_461/" \
                                               "Project2/proj2_code_github/project-2-22/Credentials/" \
                                               "prime-micron-330718-02ad6bc9672b.json"


# client = storage.Client()
# test_bucket_name = "fiducial_marker_buck"
# bucket = client.get_bucket(test_bucket_name)
# blobs = bucket.list_blobs()
# print(blobs)

# Download folder
# os.system("gsutil -m cp -r gs://fiducial_marker_bucket/images.zip C:/Users/sguad/A_Desktop/College/VIP/Datasets/")

# Using gsutil is more efficient and have more commands than storage library

def create_bucket(bucket_name, storage_class="STANDARD", bucket_location="US-EAST1", project_id="ece-461-project-2-22"):
    os.system(f"gsutil mb -p {project_id} -c {storage_class} -l {bucket_location} gs://{bucket_name}")


def upload_zip(source_file_local, dest_bucket_gcp):
    os.system(f"gsutil -m cp -r {source_file_local} {dest_bucket_gcp}")


def download_zip(source_file_object, dest_folder_local):
    os.system(f"gsutil -m cp -r {source_file_object} {dest_folder_local}")


def delete_object(bucket_name, object_name):
    os.system(f"gsutil rm gs://{bucket_name}/{object_name}")


def delete_bucket(bucket_name):
    os.system(f"gsutil rm gs://{bucket_name}")


def list_buckets():
    os.system("gsutil ls")


def list_objects_in_bucket(bucket_name):
    os.system(f"gsutil ls -r gs://{bucket_name}")


def label_bucket(key, value, bucket_name):
    os.system(f"gsutil label ch -l {key}:{value} gs://{bucket_name}")


if __name__ == '__main__':
    print("start")
    source_file = "C:/Users/sguad/A_Desktop/College/ECE_461/Project2/" \
                  "proj2_code_github/project-2-22/Gsutil_Testing/images.zip"
    dest_folder = 'C:/Users/sguad/A_Desktop/College/ECE_461/Project2/proj2_code_github/project-2-22/Gsutil_Testing'
    # dest_bucket = gs://fiducial_marker_bucket
    bucket_name = "testing_gsutil_myproj"

    # Testing
    # create_bucket("testing_gsutil_myproj", project_id="prime-micron-330718")
    # upload_zip(source_file, dest_bucket_gcp=f"gs://{bucket_name}")
    # download_zip(f"gs://{bucket_name}/images.zip", dest_folder)
    # delete_object(bucket_name, "images.zip")
    list_objects_in_bucket(bucket_name)

    # Notes: use gsutil for commands, use storage to check commands occurred.
    # Think to look for: how to get the json file, authorization for different buckets/objects
    print("end")
