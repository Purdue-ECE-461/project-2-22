import datetime
import json

from flask import Flask, render_template, request, url_for, make_response, Response, jsonify
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required

from werkzeug.utils import redirect

import database_helper
import mainHelper
from flask_restful import Api, Resource, reqparse, abort
import os
import pymysql
from Actions import Delete, ResetDefault, Upload, Update, Search
from Actions import Decode
from Actions import Download
import logging

DEST_FOLDER = 'downloaded_files'

app = Flask(__name__)

api = Api(app)

ROWS_PER_PAGE = 5
MAIN_BUCKET_NAME = "acme_corporation_general"


@app.route("/token", methods=["POST"])
def create_token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    # create a new token with the user id inside
    access_token = create_access_token(identity=username)
    return jsonify({"token": access_token, "user_id": username})


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user_id = get_jwt_identity()
    print(current_user_id)

    return jsonify({"id": current_user_id, "username": "test"}), 200


@app.route('/')
def root():
    print("Root Endpoint Reached")
    if os.environ.get('GAE_ENV') == 'standard' or True:
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(database_helper.db_connection_name)
        cnx = pymysql.connect(user=database_helper.db_user, password=database_helper.db_password,
                              unix_socket=unix_socket, db=database_helper.db_name)
        print("Root connected to database")
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        print(database_helper.db_user)
        cnx = pymysql.connect(user='proj-2-database-mysql', password='test1234',
                              host=host, db='demo')

    with cnx.cursor() as cursor:
        cursor.execute('SELECT demo_txt from demo_tbl;')
        result = cursor.fetchall()
        current_msg = result[0][0]
    cnx.close()

    print(str(current_msg))

    return render_template('index.html', times='1.0.0', endpoint=current_msg, user_data='1.0.0',
                           error_message='current_msg')


@app.route('/start', methods=['POST'])
def start():
    id = request.form['id']
    name = request.form['name']
    content = request.form['content']
    version = request.form['version']
    url = request.form['url']
    jsprogram = request.form['jsprogram']
    offset = request.form['offset']

    select = request.form.get('requestType')
    if select == "list":
        if id == "":
            if name == "":
                return get_packages(offset)
            else:
                return get_package_by_name(name)
        else:
            return get_package_by_id(id)  # WORKS CORRECTLY
        # get packages
    elif select == "upload":
        return post_package(name, content, version, url, jsprogram)  # DOES NOT WORK
        # upload stuff
    elif select == "update":
        return update_package(id)
        # update stuff
    elif select == "rate":
        if id == "":
            return "Invalid package Id"
        else:
            return rate_package_by_id(id)
        # rate stuff
    elif select == "delete":
        if id == "":
            if name == "":
                return delete_all_packages()
            else:
                return delete_package_by_name(name)
        else:
            return delete_package_by_id(id)
        # delete stuff
    else:
        pass
        # error then, dont think this is possible though
    return "this is " + select + " and " + str(id)


@app.route('/packages', methods=['POST'])
def get_packages(offset=None):
    print("GET PACKAGES START")
    try:
        if offset == None:
            offset = request.args.get('offset')
            print('Offset in get packages: ' + str(offset))
            header = request.headers.get('Content-Type')
            print(header)

        d = (str(request.data.decode('utf-8')))
        print('/packages POST data: ' + d)
        data_list_dict = json.loads(d)
        print('GET PACKAGES DATA: ' + str(data_list_dict))

        # returns list of dictionaries
        packages = database_helper.get_packages(data_list_dict, offset)

        resp = Response(response=packages,
                        status=200,
                        mimetype="application/json")
        print("GET PACKAGES END")
    except Exception as e:
        logging.error(str(e))
        print(str(e))
        resp = make_response({"code": 500, "message": "Unexpected Error in Get Packages (POST)"})
        resp.mimetype = 'application/json'

    return resp


@app.route('/reset', methods=['DELETE'])
def delete_all_packages():
    print('/reset')
    try:
        permission = True

        if permission:
            database_helper.delete_all_packages()
            status_code = 200
            # Cloud Storage: Reset bucket to default, empty all objects
            ResetDefault.reset_default(MAIN_BUCKET_NAME)
            print("reset success")
        else:
            status_code = 401

        resp = Response(status=status_code)
    except Exception as e:
        logging.error(str(e))
        resp = make_response({"code": 500, "message": "Unexpected Error in Delete all packages"})
        resp.mimetype = 'application/json'

    return resp


@app.route('/package/<id>', methods=['GET'])
def get_package_by_id(id):
    print('get package by ID endpoint; package_id: ' + str(id))

    # returns in the format Name Version Filename Url Content
    if id.isdigit():
        ret_data = database_helper.get_package_by_id(id)
    else:
        print("Id is not an integer")
        return Response(status=400)

    if ret_data is None:
        print("ret data is none")
        return Response(status=400)

    print("GET PACKAGE BY ID DATA: " + str(ret_data))

    # take ret_data[content] with the bucket path and put that into a text file
    # read in that text file and assign that to a content variable

    try:
        print(str(ret_data['Filename']))
        if ret_data['Filename'] is None or ret_data['Filename'] == 'None':
            lines = []
        else:
            lines = Download.download_text(filename_to_gcp=ret_data['Filename'],
                                           destination_bucket_gcp=MAIN_BUCKET_NAME)

        print(lines)
        data = {
            "metadata": {
                "Name": ret_data['Name'],
                "Version": ret_data['Version'],
                "ID": str(id)
            },
            "data": {
                "Content": str(lines),
                "URL": ret_data['URL'],
                "JSProgram": "None"
            }
        }

        r = make_response(data)
        r.mimetype = 'application/json'
    except Exception as e:
        logging.error(str(e))
        print(str(e))
        r = make_response({"code": 500, "message": "Unexpected Error in get package by id"})
        r.mimetype = 'application/json'

    render_template('page.html', endpoint=('GET: package/' + str(id)))
    return r


@app.route('/package/<id>', methods=['PUT'])
def update_package(id):
    # the name, version, and ID must match
    # the package contents will replace the previous contents
    print("Update Package; ID: " + str(id))

    if not id.isdigit():
        return Response(status=403)

    try:
        d = (str(request.data.decode('utf-8')))
        print('Update Package Data: ' + d)
        data_list_dict = json.loads(d)

        # args = message_parser.parse_args(req=root_args)
        name = (data_list_dict['metadata']['Name'])
        version = (data_list_dict['metadata']['Version'])
        p_id = (data_list_dict['metadata']['ID'])

        if 'Content' in data_list_dict['data']:
            if str(data_list_dict['data']['content']).lower != 'null' and str(data_list_dict['data']['content']).lower != 'none':
                content_found = True
            else:
                content_found = False
        else:
            content_found = False

        if content_found:
            print('Content found')
            if database_helper.package_exists(name, version, id):
                database_helper.update_package(name, version, p_id, database_helper.get_url_from_id(p_id),
                                               database_helper.get_filename_from_id(p_id))
                Update.update_file(
                    bucket_name=MAIN_BUCKET_NAME,
                    object_name=database_helper.get_filename_from_id(p_id)[:-4],
                    content=data_list_dict['data']['Content']
                )
                status_code = 200
            else:
                print("Package does not exist")
                status_code = 403
        elif 'URL' in data_list_dict['data']:
            print('URL found')
            if database_helper.package_exists(name, version, id):
                database_helper.update_package(name, version, p_id, data_list_dict['data']['URL'],
                                               database_helper.get_filename_from_id(p_id))
                status_code = 200
            else:
                print("Package does not exist")
                status_code = 403
    except Exception as e:
        logging.error(str(e))
        print(str(e))
        status_code = 500

    return Response(status=status_code)


@app.route('/package/<id>', methods=['DELETE'])
def delete_package_by_id(id):
    print(id)
    print('Delete package by ID: ' + str(id))

    if id.isdigit():
        filename = database_helper.delete_package_by_id(id)
    else:
        print("id not found or not a digit")
        return Response(status=400)

    try:
        if filename is not None:
            Delete.delete_object_safe(
                bucket_name=MAIN_BUCKET_NAME,
                object_name=filename
            )
            status_code = 200
        else:
            status_code = 400
    except Exception as e:
        logging.error(str(e))
        print(str(e))
        status_code = 500

    return Response(status=status_code)


@app.route('/package', methods=['POST'])
def post_package(name=None, content=None, version=None, url=None, jsprogram=None):
    print('Enter Post Package Endpoint')

    # these variables are None if the requests are done via postman, they are not None if done by front end
    if name is None:
        header = request.headers.get('X-Authorization')
        print(header)

    if name is None:
        d = (str(request.data.decode('utf-8')))
        data_list_dict = json.loads(d)

    int_id = database_helper.get_auto_increment()
    print("Internal ID (auto increment): " + str(int_id))

    try:
        if 'data' not in data_list_dict:
            print("provided json has no data")
            return Response(status=400)

        if 'URL' not in data_list_dict['data'] and 'Content' not in data_list_dict['data']:
            print('Provided JSON has no URL or Content')
            return Response(status=400)
    except Exception as e:
        print(str(e))
        return Response(status=400)

    if 'Content' in data_list_dict['data']:
        content = (data_list_dict['data']['Content'])
    else:
        print("Provided JSON has no content")
        content = 'None'

    if 'URL' in data_list_dict['data']:
        print("Provided JSON has no URL")
        url = (data_list_dict['data']['URL'])
    else:
        url = ""

    frontEnd = 1
    if name is None:
        name = (data_list_dict['metadata']['Name'])
        version = (data_list_dict['metadata']['Version'])
        p_id = (data_list_dict['metadata']['ID'])
        frontEnd = 0

    ingestion = 1
    for key, value in data_list_dict['data'].items():
        if key == 'Content':
            ingestion = 0

    if ingestion == 0:

        if frontEnd == 0:
            if 'Content' in data_list_dict['data']:
                content = (data_list_dict['data']['Content'])
            else:
                content = 'None'

        encoded_text_to_gcp = str(content)

        print(database_helper.is_unique_package(name, version, p_id))
        if database_helper.is_unique_package(name, version, p_id):
            # Cloud Storage: Uploading file to GCP.
            if content != 'None':
                database_helper.post_package(name, version, p_id, url, (name + str(int_id) + ".txt"))
                Upload.upload_file(
                    filename_to_gcp=(name + str(int_id)),
                    encoded_zipfile_string=encoded_text_to_gcp,
                    destination_bucket_gcp=MAIN_BUCKET_NAME
                )
            else:
                database_helper.post_package(name, version, p_id, url, None)

            status_code = 201
        else:
            status_code = 403
    else:
        if database_helper.is_unique_package(name, version, p_id):
            print("ingesting")
            scores = mainHelper.rate(url)
            print(scores)
            ingestible = 1
            for key, value in scores.items():
                print(str(key) + ': ' + str(value))
                if value < 0.5:
                    ingestible = 0
            if ingestible == 1:
                conn = database_helper.mysql_connect()
                if database_helper.is_unique_package(name, version, p_id):
                    database_helper.post_package(name, version, p_id, url, None)
                    status_code = 201
                else:
                    status_code = 405
                    print("Package was not ingestible")
                    print("Package URL: " + str(url))
                database_helper.mysql_close(conn)
            else:
                status_code = 405
        else:
            status_code = 403

    if status_code != 201:
        return Response(status=status_code)

    data = {"Name": name, "Version": version, "ID": int_id}
    r = make_response(data)
    r.mimetype = 'application/json'
    r.status_code = status_code

    return r


@app.route('/package/<id>/rate', methods=['GET'])
def rate_package_by_id(id):
    print("Rate package by ID: " + str(id))
    # if successful rating
    data = {
        "BusFactor": 0,
        "Correctness": 0,
        "RampUp": 0,
        "ResponsiveMaintainer": 0,
        "LicenseScore": 0,
        "GoodPinningPractice": 0
    }

    # get package variables

    if id.isdigit():
        variables = database_helper.get_package_by_id(id)
    else:
        return Response(status=400)

    if variables is None:
        return Response(status=400)

    status_code = 200

    # no URL, get from package.json
    if variables['URL'] == "":
        print("filename: " + str(variables['Filename']))
        print("No URL uploaded, getting repository from package.json")
        content_string = Download.download_text(variables['Filename'], MAIN_BUCKET_NAME)
        print("content string found")
        Decode.decode_base64("/tmp/output.zip", content_string)
        print("decoded")
        jsonFile = mainHelper.getPackageJson("/tmp/output.zip")
        if jsonFile is not None:
            url = mainHelper.getURL('/tmp/' + jsonFile)
            print("Rate package by ID: URL from JSON file: " + str(url))
            if url is not None:
                data = mainHelper.rate(url)
    else:
        try:
            data = mainHelper.rate(variables['URL'])
            status_code = 200
        except Exception as e:
            logging.error(str(e))
            print(str(e))
            return Response(status=500)

    r = make_response(data)
    r.status_code = status_code
    r.mimetype = 'application/json'
    return r


@app.route('/authenticate_test', methods=['PUT'])
def authenticate():
    root_parser = reqparse.RequestParser()
    root_parser.add_argument('User', type=dict)
    root_parser.add_argument('Secret', type=dict)

    message_parser = reqparse.RequestParser()
    message_parser.add_argument('name', type=str, location=('User',))
    message_parser.add_argument('isAdmin', type=str, location=('User',))
    message_parser.add_argument('password', type=str, location=('Secret',))
    root_args = root_parser.parse_args()
    args = message_parser.parse_args(req=root_args)
    print(args['name'])
    print(args['isAdmin'])
    print(args['password'])
    return redirect(url_for('/', endpoint='GET: authenticate'))


@app.route('/package/byName/<name>', methods=['GET'])
def get_package_by_name(name):
    print("GET PACKAGE HISTORY BY NAME: " + str(name))

    database_helper.get_package_by_name(name)
    data = database_helper.get_package_by_name_history(name)

    if len(data) == 0:
        print("Name not found")
        return Response(status=400)
    print("PACKAGE HISTORY DATA: " + str(data))
    data_list = []
    for d in data:
        new_dict = {'User': {
            'Name': 'No User',
            'isAdmin': 'N/A'
        },
            'Date': str(d[2]),
            'PackageMetadata': {
                'Name': d[3],
                'Version': d[4],
                'ID': d[5]
            },
            'Action': d[6]}
        data_list.append(new_dict)
    r = json.dumps(data_list)
    return Response(response=r,
                    status=200,
                    mimetype="application/json")


@app.route('/package/byName/<name>', methods=['DELETE'])
def delete_package_by_name(name):
    print("Delete package by name: " + str(name))
    if len(database_helper.get_package_by_name(name)) == 0:
        return Response(status=400)
    filenames = database_helper.get_file_names(name)

    filenames = [fname for fname in filenames if str(fname) != 'None']

    print("FILENAMES TO DELETE: " + str(filenames))

    database_helper.delete_package_by_name(name)
    status_code = 200
    try:
        if len(filenames) > 0:
            for fname in filenames:
                print("FILENAME: " + str(fname))
                filename_in_gcp = Search.find_object(MAIN_BUCKET_NAME, fname)
                print("FOUND FILENAME IN GCP" + str(filename_in_gcp.name))
                if filename_in_gcp:
                    Delete.delete_object_safe(
                        bucket_name=MAIN_BUCKET_NAME,
                        object_name=fname
                    )
            status_code = 200
    except Exception as e:
        logging.error(str(e))
        print(str(e))
        status_code = 500

    # return 400 for no such package; return 200 for success
    return Response(status=status_code)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
