import requests

APP_BASE_URL = r"https://ece-461-project-2-22.ue.r.appspot.com/"

payload = {'key1': 'value1', 'key2': 'value2'}


def ping_get_package_by_id(package_id):
    r = requests.get(APP_BASE_URL + 'package/' + str(package_id))

    headers = r.headers
    status_code = r.status_code
    response = r.json()  # in dictionary form

    return headers, status_code, response


def ping_get_package_by_name(package_name):
    r = requests.get(APP_BASE_URL + 'package/byName/' + str(package_name))

    headers = r.headers
    status_code = r.status_code
    response = r.json()  # in dictionary form

    return headers, status_code, response


def ping_post_package(package_name, package_version, package_id, package_url, package_js, package_content):
    payload = {'data':
                   {'URL':package_url, 'JSProgram':package_js, 'Content':package_content},
                'metadata':
                    {'Name':package_name, 'Version':package_version,'ID':package_id}
                }
    r = requests.post(APP_BASE_URL + 'package', data=payload)

    headers = r.headers
    status_code = r.status_code
    #response = r.json()  # in dictionary form

    return headers, status_code


if __name__ == '__main__':
    res = ping_get_package_by_id(12)
    #res = ping_post_package(package_url="hi.com", package_content="hi", package_name="lol", package_id="lol", package_js="", package_version="1.0.0")
    print(res)
