import base64
import os


def encode_zip(filename):
    with open(filename, "rb") as f:
        file_bytes = f.read()
        encoded = base64.b64encode(file_bytes)
        return encoded


def decode_base64(output_zip, string_to_decode):
    decoded = base64.b64decode(string_to_decode)
    with open(output_zip, 'wb') as f:
        f.write(decoded)


def string_to_text_file(encoded_text, text_file_folder_path):
    filename = "file_encoded_string.txt"
    file_path = os.path.join(text_file_folder_path, filename)
    with open(file_path, 'w') as f:
        f.write(encoded_text)
    return file_path


def text_file_to_string(text_file):
    with open(text_file, "rb") as f:
        string_to_zip = f.readlines()[0]
    return string_to_zip


if __name__ == "__main__":
    file_to_encode = "C:\\Users\\sguad\\A_Desktop\\College\\VIP\\Datasets\\Fiducial\\images.zip"
    file_to_decode = "C:\\Users\\sguad\\A_Desktop\\College\\VIP\\Datasets\\Fiducial\\images_1.zip"
    folder_dest_text = "C:\\Users\\sguad\\A_Desktop\\College\\VIP\\Datasets\\Fiducial"

    encoded_string = encode_zip(file_to_encode)
    file_text = string_to_text_file(encoded_string, folder_dest_text)
    string_encoded_from_text = text_file_to_string(file_text)
    if string_encoded_from_text == encoded_string:
        print("Great")
    else:
        print("Not Great")
    decode_base64(file_to_decode, string_encoded_from_text)