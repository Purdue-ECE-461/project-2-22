from google.cloud import storage


def upload_file(filename_to_gcp, encoded_zipfile_string, destination_bucket_gcp):
    # filename_to_gcp: the name of the file that is going to be in gcp
    client = storage.Client()
    bucket = client.get_bucket(destination_bucket_gcp)
    if len(filename_to_gcp.split(".")) == 1:
        filename_to_gcp = filename_to_gcp + ".txt"
    blob = bucket.blob(filename_to_gcp + ".txt")
    blob.upload_from_string(encoded_zipfile_string)


# def upload_file(source_file_local, destination_bucket_gcp):
#     destination_bucket_gcp = f'gs://' + str(destination_bucket_gcp)
#     if ActionHelper.check_file(source_file_local):
#         os.system(f"gsutil cp {source_file_local} {destination_bucket_gcp}")
#     else:
#         print("File path doesn't exists")

