import sqlite3
import semver


def version_check(package_list, version_range):
    '''test_range = '1.2.3-2.1.0'
    version = '3.2.1'
    ver = semver.parse('1.2.3-2.1.0')
    res = semver.compare(test_range, version)
    res = semver.match(version, '>3.0.0')
    res = semver.max_ver(test_range, '1.3.4')'''

    good_packages = []
    for package in package_list:
        if semver.match(package[1], version_range):
            good_packages.append(package)

    return good_packages


def initialize_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE packages (Name TEXT, Version TEXT, ID TEXT NOT NULL PRIMARY KEY, URL TEXT, Filename '
                 'TEXT)')
    print("Table created successfully")
    conn.close()


def post_package(name, version, p_id, url, filename):
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO packages (Name,Version,ID,URL,Filename) \
        VALUES(?, ?, ?, ?, ?)", (name, version, p_id, url, filename))

        con.commit()


def get_packages(data_dict, offset):
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        for d in data_dict:
            res = cur.execute("SELECT Name,Version,ID from packages WHERE Name='" + str(d['Name']) + "'")

            packages = []
            for row in res:
                packages.append(row)

            print(version_check(packages, d['Version']))


def get_all_packages():
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        res = cur.execute("SELECT Name,Version,ID from packages")

        packages = []
        for row in res:
            packages.append(row)

        print(packages)


def get_package_by_id(id):
    con = sqlite3.connect("database.db")

    cur = con.cursor()
    res = cur.execute("select Name,Version,Filename,URL from packages WHERE ID=" + str(id))

    variables = []
    for row in res:
        print(row)
        variables.append(row)

    data = {
        "Name": variables[0],
        "Version": variables[1],
        "Filename": variables[2],
        "URL": variables[3]
    }

    con.close()
    return data


def get_package_by_name(name):
    con = sqlite3.connect("database.db")

    cur = con.cursor()
    res = cur.execute("select Name,Version,Filename from packages WHERE Name=?", (name,))

    for row in res:
        print(row)

    con.close()


def update_package(name, version, p_id, url, filename):
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE packages SET URL = ?, Filename = ? \
        WHERE Name = ? AND Version = ? and ID = ?", (url, filename, name, version, p_id))

        con.commit()


def delete_all_packages():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("DELETE from packages")
    con.commit()
    con.close()


def delete_package_by_id(p_id):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("DELETE from packages where ID=?", str(p_id))
    con.commit()
    con.close()


if __name__ == '__main__':
    print(semver.SEMVER_SPEC_VERSION)

    '''import requests

    url = "http://127.0.0.1:8080/packages?offset=10"

    payload = "[\n  {\n    \"Version\": \"<=1.0.0\",\n    \"Name\": \"test2\"\n  },\n  {\n    \"Version\": \"<=1.3.0\",\n    \"Name\": \"test2\"\n  }\n]"
    headers = {
        'X-Authorization': 'bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)'''
