import sqlite3
import json
import os
import pymysql
import semver

from Actions import Search

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

ROWS_PER_PAGE = 5


def mysql_close(cnx):
    cnx.close()


def mysql_connect():
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        cnx = pymysql.connect(user='proj-2-database-mysql', password='test1234',
                              host=host, db='demo')

    '''with cnx.cursor() as cursor:
        cursor.execute('SELECT demo_txt from demo_tbl;')
        result = cursor.fetchall()
        current_msg = result[0][0]'''

    return cnx


def version_check(package_list, version_range):
    '''test_range = '1.2.3-2.1.0'
    version = '3.2.1'
    ver = semver.parse('1.2.3-2.1.0')
    res = semver.compare(test_range, version)
    res = semver.match(version, '>3.0.0')
    res = semver.max_ver(test_range, '1.3.4')'''

    start_range = ''
    end_range = ''

    if version_range.count('.') == 1:
        version_range = version_range + '.0'
    elif version_range.count('.') == 0:
        version_range = version_range + '.0.0'

    if '!' not in str(version_range) and '>' not in str(version_range) and '<' not in str(version_range) \
            and '~' not in str(version_range) and '^' not in str(version_range) and '-' not in str(version_range):
        version_range = '==' + version_range
        start_range = version_range
        end_range = version_range
    elif '~' in version_range:
        start_range = '>=' + str(version_range[1:])
        split = version_range.split('.')
        end_range = '<' + split[0][1:] + '.' + str(int(split[1]) + 1) + '.0'
    elif '^' in version_range:
        start_range = '>=' + str(version_range[1:])
        split = version_range.split('.')
        end_range = '<' + str(int(split[0][1:]) + 1) + '.0.0'
    elif '-' in version_range:
        split = version_range.split('-')
        start_range = '>=' + split[0].strip()
        end_range = '<=' + split[1].strip()

    good_packages = []
    for package in package_list:
        print(version_range)
        if semver.match(package[1], start_range) and semver.match(package[1], end_range):
            good_packages.append(package)

    return good_packages


def initialize_db():
    conn = mysql_connect()
    conn.execute('CREATE TABLE packages (internal_id INT NOT NULL AUTO_INCREMENT, Name TEXT, Version TEXT, ID TEXT NOT '
                 'NULL, URL TEXT, Filename '
                 'TEXT, PRIMARY KEY (internal_id))')
    print("Table created successfully")
    mysql_close(conn)


def init_package_history_table():
    conn = mysql_connect()
    cur = conn.cursor()
    cur.execute("create table package_history(user_name TEXT,user_isAdmin CHAR(1),change_date TIMESTAMP NOT NULL "
                "DEFAULT CURRENT_TIMESTAMP,package_name TEXT,package_version VARCHAR(255),package_id TEXT,"
                "action VARCHAR(50));")
    mysql_close(conn)


def insert_package_history(package_name, package_version, package_id, action, user_name=None, user_isAdmin=0):
    conn = mysql_connect()
    cur = conn.cursor()

    cur.execute("INSERT INTO package_history (user_name, user_isAdmin, package_name, package_version, package_id, "
                "action) "
                "VALUES (%s, %s, %s, %s, %s, %s);",
                (str(user_name), str(user_isAdmin), str(package_name), str(package_version), str(package_id),
                 str(action),))
    conn.commit()
    mysql_close(conn)


def get_package_history(name):
    con = mysql_connect()
    cur = con.cursor()

    cur.execute("SELECT * FROM package_history WHERE package_name=%s", (str(name),))

    ret_val = cur.fetchall()

    mysql_close(con)

    return ret_val


def get_name_version_from_id(p_id):
    con = mysql_connect()
    cur = con.cursor()

    cur.execute("SELECT Name, Version FROM packages WHERE INTERNAL_ID=" + str(p_id))

    ret_val = cur.fetchall()

    mysql_close(con)

    return ret_val[0]


def post_package(name, version, p_id, url, filename):
    con = mysql_connect()
    cur = con.cursor()
    cur.execute("INSERT INTO packages (Name,Version,ID,URL,Filename) VALUES (%s, %s, %s, %s, %s);",
                (str(name), str(version), str(p_id), str(url), str(filename),))

    insert_package_history(name, version, get_auto_increment() - 1, 'CREATE')

    con.commit()
    mysql_close(con)


def get_packages(data_dict, offset):
    con = mysql_connect()

    if offset is None:
        offset = 1

    print(offset)
    offset = int(offset)

    cur = con.cursor()
    valid_packages = []
    for d in data_dict:
        cur.execute("SELECT Name,Version,INTERNAL_ID from packages WHERE Name=%s", (d['Name'],))

        packages = []
        for row in cur.fetchall():
            packages.append(row)

        for package in (version_check(packages, d['Version'])):
            j_pack = {'Name': package[0], 'Version': package[1], 'ID': package[2]}
            if j_pack not in valid_packages:
                valid_packages.append(j_pack)

    if len(valid_packages) > ROWS_PER_PAGE:
        valid_packages = valid_packages[(offset - 1) * ROWS_PER_PAGE: (
            offset * ROWS_PER_PAGE if len(valid_packages) >= offset * ROWS_PER_PAGE else len(valid_packages))]

    mysql_close(con)

    return json.dumps(valid_packages)


def get_all_packages():
    con = mysql_connect()
    cur = con.cursor()
    cur.execute("SELECT Name,Version,INTERNAL_ID,URL,Filename from packages")

    packages = []
    for row in cur.fetchall():
        packages.append(row)

    print(packages)
    mysql_close(con)
    return packages


def get_all_package_history():
    con = mysql_connect()
    cur = con.cursor()
    cur.execute("SELECT * from package_history")

    packages = []
    for row in cur.fetchall():
        packages.append(row)

    print(packages)
    mysql_close(con)
    return packages


def get_package_by_id(p_id):
    con = mysql_connect()
    cur = con.cursor()
    cur.execute("select Name,Version,Filename,URL from packages WHERE INTERNAL_ID=" + str(p_id))
    mysql_close(con)

    variables = []
    for row in cur.fetchall():
        variables.append(row)

    print(len(variables))

    if len(variables) > 0:
        data = {
            "Name": variables[0][0],
            "Version": variables[0][1],
            "Filename": variables[0][2],
            "URL": variables[0][3],
            "Content": variables[0][2]  # needs to be decoded
        }
        insert_package_history(data["Name"], data["Version"], p_id, 'DOWNLOAD')
    else:
        data = None

    return data


def get_package_by_name(name):
    con = mysql_connect()
    cur = con.cursor()
    cur.execute("select Name,Version,Filename from packages WHERE Name=%s", (name,))
    mysql_close(con)

    ret_val = []

    for row in cur.fetchall():
        print(row)
        ret_val.append(row)

    return ret_val


def get_package_by_name_history(name):
    con = mysql_connect()
    cur = con.cursor()
    cur.execute("select * from package_history WHERE package_name=%s", (str(name),))
    mysql_close(con)

    ret_val = []

    for row in cur.fetchall():
        ret_val.append(row)

    return ret_val


def update_package(name, version, p_id, url, filename):
    con = mysql_connect()
    cur = con.cursor()
    cur.execute("UPDATE packages SET URL = %s, Filename = %s \
        WHERE Name = %s AND Version = %s and INTERNAL_ID = %s", (url, filename, name, version, p_id,))
    insert_package_history(str(name), str(version), str(p_id), 'UPDATE', 'None', 0)
    con.commit()
    mysql_close(con)


def delete_all_packages():
    con = mysql_connect()
    cur = con.cursor()
    cur.execute("DELETE from packages")
    cur.execute("DELETE from package_history")
    con.commit()
    mysql_close(con)


def delete_package_by_id(p_id):

    name, version = get_name_version_from_id(p_id)

    con = mysql_connect()
    cur = con.cursor()
    cur.execute("SELECT Filename from packages where INTERNAL_ID=" + str(p_id))
    res = cur.fetchall()
    cur.execute("DELETE from packages where INTERNAL_ID=" + str(p_id))
    con.commit()
    mysql_close(con)

    insert_package_history(str(name), str(version), str(p_id), 'DELETE', 'None', 0)

    if len(res) > 0:
        return res[0][0]
    else:
        return None


def delete_package_by_name(name):
    insert_package_history(str(name), str('ALL'), str('ALL'), 'DELETE', 'None', 0)

    con = mysql_connect()
    cur = con.cursor()
    cur.execute("DELETE from packages where NAME=%s", str(name))
    con.commit()
    mysql_close(con)


def get_filename_from_id(pid):
    con = mysql_connect()
    cur = con.cursor()
    cur.execute("SELECT Filename from packages where INTERNAL_ID=" + str(pid))
    ret_val = cur.fetchall()
    mysql_close(con)
    return ret_val[0][0]


def get_url_from_id(pid):
    con = mysql_connect()
    cur = con.cursor()
    cur.execute("SELECT URL from packages where INTERNAL_ID=" + str(pid))
    ret_val = cur.fetchall()
    mysql_close(con)
    return ret_val[0][0]


def get_last_id():
    con = mysql_connect()
    cur = con.cursor()
    cur.execute("SELECT MAX(INTERNAL_ID) from packages;")
    ret_val = cur.fetchall()
    mysql_close(con)
    return ret_val[0][0]


def is_unique_package(package_name, package_version, package_id):
    con = mysql_connect()
    cur = con.cursor()
    cur.execute("SELECT * from packages WHERE Name=%s AND Version=%s", (str(package_name), str(package_version)))
    ret_val = cur.fetchall()
    mysql_close(con)

    if len(ret_val) > 0:
        return False
    else:
        return True


def package_exists(package_name, package_version, package_id):
    con = mysql_connect()
    cur = con.cursor()
    cur.execute("SELECT * from packages WHERE Name=%s AND Version=%s AND INTERNAL_ID=" + str(package_id), (str(package_name), str(package_version)))
    ret_val = cur.fetchall()
    mysql_close(con)

    if len(ret_val) > 0:
        return True
    else:
        return False


def get_package_id(package_name, package_version, package_id):
    con = mysql_connect()
    cur = con.cursor()
    cur.execute("SELECT INTERNAL_ID from packages WHERE Name=%s AND Version=%s AND ID=%s", (str(package_name), str(package_version), str(package_id)))
    ret_val = cur.fetchall()
    mysql_close(con)

    if len(ret_val) > 0:
        return ret_val[0][0]
    else:
        return None


def get_auto_increment():
    con = mysql_connect()
    cur = con.cursor()
    cur.execute("SELECT AUTO_INCREMENT FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'demo' AND TABLE_NAME = "
                "'packages';")
    ret_val = cur.fetchall()
    mysql_close(con)

    return ret_val[0][0]


def get_file_names(package_name):
    con = mysql_connect()
    cur = con.cursor()
    cur.execute("SELECT Filename FROM packages where Name=%s;", str(package_name))
    res = cur.fetchall()
    mysql_close(con)
    ret_val = []
    for file in res:
        ret_val.append(file[0])
    return ret_val




if __name__ == '__main__':
    # init_package_history_table()
    # insert_package_history('testpackage', '1.1.1', '4', 'CREATE', 'Alia', 0)
    # print(is_unique_package('testagain', '1.0.0', 'lolx'))
    # print(get_package_by_id(67))
    # print(get_all_packages())
    # print(semver.SEMVER_SPEC_VERSION)

    # delete_package_by_name('testing_offsets')
    # print(is_unique_package('test_rate', '1.0.0', '78'))

    # print(get_name_version_from_id(98))

    '''import requests

    url = "http://127.0.0.1:8080/package"

    payload = "{\n    \"metadata\": {\n        \"Name\": \"test2\",\n        \"Version\": \"1.3.0\",\n        \"ID\": \"8\"\n    },\n    \"data\": {\n        \"Content\": \"hi\",\n        \"URL\": \"https://github.com/jashkenas/underscore\",\n        \"JSProgram\": \"if (process.argv.length === 7) {\\nconsole.log('Success')\\nprocess.exit(0)\\n} else {\\nconsole.log('Failed')\\nprocess.exit(1)\\n}\\n\"\n    }\n}"
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

    get_all_packages()'''

    '''offset = 2
    p = [1, 1, 3, 3, 4, 5, 3, 2, 7, 2, 4, 2, 4, 5, 3, 2, 2, 3, 4, 5, 2, 4, 2, 5, 2]
    if len(p) > 10:
        valid_packages = p[(offset - 1) * 10: (offset * 10 if len(p) >= offset * 10 else len(p))]

    print(valid_packages)'''

    Search.find_object('acme_corporation_general', 'Cloudier')
