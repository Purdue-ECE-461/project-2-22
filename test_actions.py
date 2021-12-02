from Actions import Decode
from Actions import Download
from Actions import Upload
import random
import string
import os

BUCKET = 'acme_corporation_general'
download_file = 'test_data.txt.txt'
DEST_FOLDER = 'downloaded_files'

def test_download_and_read():
    Download.download_file(bucket=BUCKET, file_to_download=download_file, destination_folder_local=DEST_FOLDER)
    # read in text file
    with open(DEST_FOLDER + '/' + download_file) as f:
        lines = f.readlines()

    if len(lines) == 1:
        assert lines[0] == 'hi my name is alia and i put myself in dumb situation xoxo dummy'
    else:
        assert False


def test_upload_download():
    # make a string
    letters = string.ascii_letters
    upload_str = (''.join(random.choice(letters) for i in range(100)))
    # upload a file
    current_path = os.getcwd()
    encoded_text_file = upload_str
    complete_zip_file_path = Decode.string_to_text_file(encoded_text=encoded_text_file,
                                                        text_file_folder_path=current_path, upload_str[0] + 'test_upload')
    print("saved")
    Upload.upload_file(upload_str[0] + 'test_upload.txt', BUCKET)
    print("uploaded")
    # download the data
    Download.download_file(bucket=BUCKET, file_to_download=upload_str[0] + 'test_upload.txt', destination_folder_local=DEST_FOLDER)
    # read in text file
    with open(DEST_FOLDER + '/' + upload_str[0] + 'test_upload.txt') as f:
        lines = f.readlines()
    # verify that it's the same data
    print(lines)

    assert (lines[0] == upload_str)

if __name__ == '__main__':
    # make a string
    letters = string.ascii_letters
    upload_str = (''.join(random.choice(letters) for i in range(100)))
    # upload a file
    current_path = os.getcwd()
    encoded_text_file = upload_str
    complete_zip_file_path = Decode.string_to_text_file(encoded_text=encoded_text_file,
                                                        text_file_folder_path=current_path,
                                                        filename=upload_str[0] + 'test_upload.txt')
    print("saved")
    Upload.upload_file(upload_str[0] + 'test_upload.txt', BUCKET)
    print("uploaded")
    # download the data
    Download.download_file(bucket=BUCKET, file_to_download=upload_str[0] + 'test_upload.txt',
                           destination_folder_local=DEST_FOLDER)
    # read in text file
    with open(DEST_FOLDER + '/' + upload_str[0] + 'test_upload.txt') as f:
        lines = f.readlines()
    # verify that it's the same data
    print(lines)

    print (lines[0] == upload_str)


