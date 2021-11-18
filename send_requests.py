import requests

APP_BASE_URL = r"https://ece-461-project-2-22.ue.r.appspot.com/"

payload = {'key1': 'value1', 'key2': 'value2'}


def ping_get_package_by_id(package_id):
    r = requests.get(APP_BASE_URL + 'package/' + str(package_id))

    headers = r.headers
    status_code = r.status_code
    response = r.json()  # in dictionary form

    return headers, status_code, response


if __name__ == '__main__':
    res = ping_get_package_by_id(12)
    print(res)
