import requests

APP_BASE_URL = r"https://ece-461-project-2-22.ue.r.appspot.com/"


# TESTING GET PACKAGES
def ping_get_packages(version, name, offset=0):
    payload = [{'Version': str(version), 'Name': str(name)}]

    r = requests.post(APP_BASE_URL + 'packages?offset=' + str(offset), json=payload)

    # add appropriate request body

    headers = r.headers
    status_code = r.status_code
    response = r.json()

    return headers, status_code, response


# TESTING DELETE ALL PACKAGES
def ping_reset():
    r = requests.delete(APP_BASE_URL + 'reset')

    headers = r.headers
    status_code = r.status_code
    response = r.json()

    return headers, status_code, response


# TESTING GET PACKAGE BY ID
def ping_get_package_by_id(package_id):
    r = requests.get(APP_BASE_URL + 'package/' + str(package_id))

    headers = r.headers
    status_code = r.status_code
    response = r.json()

    return headers, status_code, response


# TEST UPDATE PACKAGE
def ping_update_package_by_id(package_id):
    r = requests.put(APP_BASE_URL + 'package/' + str(package_id))

    headers = r.headers
    status_code = r.status_code
    response = r.json()

    return headers, status_code, response


# TEST DELETE PACKAGE BY ID
def ping_delete_package_by_id(package_id):
    r = requests.delete(APP_BASE_URL + 'package/' + str(package_id))

    headers = r.headers
    status_code = r.status_code
    response = r.json()

    return headers, status_code, response


# TEST POST PACKAGE
def ping_post_package(package_name, package_version, package_id, package_url, package_js, package_content):
    payload = {'data':
                   {'URL': str(package_url), 'JSProgram': str(package_js), 'Content': str(package_content)},
               'metadata':
                   {'Name': str(package_name), 'Version': str(package_version), 'ID': str(package_id)}
               }

    r = requests.post(APP_BASE_URL + 'package', json=payload)

    headers = r.headers
    status_code = r.status_code
    response = r.json()  # in dictionary form

    return headers, status_code, response


# TEST RATE PACKAGE
def ping_rate_package_by_id(package_id):
    r = requests.get(APP_BASE_URL + 'package/' + str(package_id) + '/rate')

    headers = r.headers
    status_code = r.status_code
    response = r.json()

    return headers, status_code, response


# TEST AUTHENTICATE
def ping_authenticate(name, isAdmin, password):
    payload = {"User": {"name": str(name), "isAdmin": str(isAdmin)}, "Secret": {"password": str(password)}}

    r = requests.post(APP_BASE_URL + 'authenticate', json=payload)

    headers = r.headers
    status_code = r.status_code
    response = r.json()  # in dictionary form

    return headers, status_code, response


def ping_get_package_by_name(package_name):
    r = requests.get(APP_BASE_URL + 'package/byName/' + str(package_name))

    headers = r.headers
    status_code = r.status_code
    response = r.apparent_encoding

    return headers, status_code, response


def ping_delete_package_by_name(package_name):
    r = requests.delete(APP_BASE_URL + 'package/byName/' + str(package_name))

    headers = r.headers
    status_code = r.status_code
    response = r.apparent_encoding

    return headers, status_code, response


if __name__ == '__main__':
    res = ping_get_packages('^1.0', 'Underscore')
    # res = ping_get_package_by_id('lol')
    # res = ping_post_package(package_url="hi.com", package_content="hi", package_name="lol", package_id="lol",
    #                        package_js="", package_version="1.0.0")
    print(res)
