import requests
from git import Repo
from zipfile import ZipFile
from Actions import Decode
import os
from os.path import basename
import shutil

APP_BASE_URL = r"https://ece-461-project-2-22.ue.r.appspot.com/"
# APP_BASE_URL = r'http://127.0.0.1:8080/'


# TESTING GET PACKAGES
# fully tested
def ping_get_packages(version, name, offset=0):
    payload = [{'Version': str(version), 'Name': str(name)}]

    r = requests.post(APP_BASE_URL + 'packages?offset=' + str(offset), json=payload)

    # add appropriate request body

    headers = r.headers
    status_code = r.status_code
    response = r.json()

    return headers, status_code, response


# TESTING DELETE ALL PACKAGES
# tested
def ping_reset():
    r = requests.delete(APP_BASE_URL + 'reset')

    headers = r.headers
    status_code = r.status_code

    return headers, status_code


# TESTING GET PACKAGE BY ID
# tested locally successfully
def ping_get_package_by_id(package_id):
    r = requests.get(APP_BASE_URL + 'package/' + str(package_id))

    headers = r.headers
    status_code = r.status_code
    response = r.json()

    return headers, status_code, response


# TEST UPDATE PACKAGE
# Tested locally successfully
def ping_update_package_by_id(package_name, package_version, package_id, package_url, package_content):
    payload = {'data':
                   {'URL': str(package_url), 'JSProgram': 'update_test', 'Content': str(package_content)},
               'metadata':
                   {'Name': str(package_name), 'Version': str(package_version), 'ID': str(package_id)}
               }
    r = requests.put(APP_BASE_URL + 'package/' + str(package_id), json=payload)

    headers = r.headers
    status_code = r.status_code

    return headers, status_code


def ping_update_package_no_content(package_name, package_version, package_id, package_url):
    payload = {'data':
                   {'URL': str(package_url), 'JSProgram': 'update_test'},
               'metadata':
                   {'Name': str(package_name), 'Version': str(package_version), 'ID': str(package_id)}
               }
    r = requests.put(APP_BASE_URL + 'package/' + str(package_id), json=payload)

    headers = r.headers
    status_code = r.status_code

    return headers, status_code


# TEST DELETE PACKAGE BY ID
# TESTED LOCALLY
def ping_delete_package_by_id(package_id):
    r = requests.delete(APP_BASE_URL + 'package/' + str(package_id))

    headers = r.headers
    status_code = r.status_code

    return headers, status_code


# TEST POST PACKAGE
# Tested
def ping_post_package(package_name, package_version, package_id, package_url, package_js, package_content):
    payload = {'data':
                   {'URL': str(package_url), 'JSProgram': str(package_js), 'Content': str(package_content)},
               'metadata':
                   {'Name': str(package_name), 'Version': str(package_version), 'ID': str(package_id)}
               }

    r = requests.post(APP_BASE_URL + 'package', json=payload)

    headers = r.headers
    status_code = r.status_code
    if status_code == 201:
        response = r.json()  # in dictionary form
    else:
        response = None

    return headers, status_code, response


# TEST POST PACKAGE
# Tested
def ping_post_package_no_content(package_name, package_version, package_id, package_url, package_js):
    payload = {'data':
                   {'URL': str(package_url), 'JSProgram': str(package_js)},
               'metadata':
                   {'Name': str(package_name), 'Version': str(package_version), 'ID': str(package_id)}
               }

    r = requests.post(APP_BASE_URL + 'package', json=payload)

    headers = r.headers
    status_code = r.status_code
    # response = r.json()  # in dictionary form

    return headers, status_code


# TEST RATE PACKAGE
# tested
def ping_rate_package_by_id(package_id):
    r = requests.get(APP_BASE_URL + 'package/' + str(package_id) + '/rate')

    headers = r.headers
    status_code = r.status_code
    if status_code != 200:
        response = None
    else:
        response = r.json()

    return headers, status_code, response


# TEST AUTHENTICATE
# todo implementation if time
def ping_authenticate(name, isAdmin, password):
    payload = {"User": {"name": str(name), "isAdmin": str(isAdmin)}, "Secret": {"password": str(password)}}

    r = requests.post(APP_BASE_URL + 'authenticate', json=payload)

    headers = r.headers
    status_code = r.status_code
    response = r.json()  # in dictionary form

    return headers, status_code, response


# tested
def ping_get_package_by_name(package_name):
    r = requests.get(APP_BASE_URL + 'package/byName/' + str(package_name))

    headers = r.headers
    status_code = r.status_code
    response = r.json()

    return headers, status_code, response


# tested
def ping_delete_package_by_name(package_name):
    r = requests.delete(APP_BASE_URL + 'package/byName/' + str(package_name))

    headers = r.headers
    status_code = r.status_code

    return headers, status_code


if __name__ == '__main__':
    # res = ping_get_packages('^1.0', 'Underscore')
    # res = ping_get_package_by_id(64)

    # p_id = (database_helper.get_package_id('Cloudy', '3.1.2', '67'))
    # print(ping_update_package_by_id('Express-Test', '5.0.0', '172', 'test.com', 'testing update'))

    # ping_post_package('Cloudier', '1.0.0', '78', 'https://github.com/cloudinary/cloudinary_npm', '',
    #                                      '')

    res = ping_post_package('Cloudier', '6.0.0', '78', 'https://github.com/cloudinary/cloudinary_npm', '',
                            None)
    print(res)
    p_id = res[2]['ID']

    # print(ping_get_package_by_id('211'))

    # print(ping_post_package('Cloudier', '3.0.0', '78', 'https://github.com/cloudinary/cloudinary_npm', '',
    #                         'hello'))

    # ping_delete_package_by_name('Cloudier')

