import os

ECE_PROJECT_ID = "ece-461-project-2-22"
TESTING_PROJECT_ID = "prime-micron-330718"


def create_bucket(bucket_name, storage_class="STANDARD", bucket_location="US-EAST1", project_id=TESTING_PROJECT_ID):
    os.system(f"gsutil mb -p {project_id} -c {storage_class} -l {bucket_location} gs://{bucket_name}")
