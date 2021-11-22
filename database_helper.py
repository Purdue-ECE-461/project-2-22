import sqlite3
import semver
import json


def version_check(package_list, version_range):
    '''test_range = '1.2.3-2.1.0'
    version = '3.2.1'
    ver = semver.parse('1.2.3-2.1.0')
    res = semver.compare(test_range, version)
    res = semver.match(version, '>3.0.0')
    res = semver.max_ver(test_range, '1.3.4')'''

    if '<' and '>' and '!' not in version_range:
        version_range = '==' + version_range

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
        valid_packages = []
        for d in data_dict:
            res = cur.execute("SELECT Name,Version,ID from packages WHERE Name='" + str(d['Name']) + "'")

            packages = []
            for row in res:
                packages.append(row)

            for package in (version_check(packages, d['Version'])):
                j_pack = {'Name': package[0], 'Version': package[1], 'ID': package[2]}
                if j_pack not in valid_packages:
                    valid_packages.append(j_pack)

    return json.dumps(valid_packages)


def get_all_packages():
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        res = cur.execute("SELECT Name,Version,ID,URL,Filename from packages")

        packages = []
        for row in res:
            packages.append(row)

        print(packages)


def get_package_by_id(id):
    con = sqlite3.connect("database.db")

    cur = con.cursor()
    res = cur.execute("select Name,Version,Filename from packages WHERE ID=" + str(id))

    ret_val = None
    for row in res:
        ret_val = row

    con.close()

    return ret_val


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
    # print(semver.SEMVER_SPEC_VERSION)

    import requests

    url = "http://127.0.0.1:8080/package"

    payload = "{\n    \"metadata\": {\n        \"Name\": \"test2\",\n        \"Version\": \"1.3.0\",\n        \"ID\": \"7\"\n    },\n    \"data\": {\n        \"Content\": \"hi\",\n        \"URL\": \"https://github.com/jashkenas/underscore\",\n        \"JSProgram\": \"if (process.argv.length === 7) {\\nconsole.log('Success')\\nprocess.exit(0)\\n} else {\\nconsole.log('Failed')\\nprocess.exit(1)\\n}\\n\"\n    }\n}"
    headers = {
        'X-Authorization': 'bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

    print(semver.cmp('>=2.0.0', '2.0.0'))

    version_range = '2.0.0'

    if '<' and '>' and '!' not in version_range:
        version_range = '==' + version_range

    print(version_range)

    print(semver.match('2.0.0', '==1.2.3-2.1.0'))

    get_all_packages()

