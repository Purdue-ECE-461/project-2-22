from google.cloud import storage


def upload_file(filename_to_gcp, encoded_zipfile_string, destination_bucket_gcp):
    # filename_to_gcp: the name of the file that is going to be in gcp
    client = storage.Client()
    bucket = client.get_bucket(destination_bucket_gcp)
    blob = bucket.blob(filename_to_gcp + ".txt")
    blob.upload_from_string(encoded_zipfile_string)
