import datetime
import json

from flask import Flask, render_template, request, url_for, make_response, Response, jsonify
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required

from firebase import firebase
from google.cloud import storage
from google.auth.transport import requests
from google.cloud import datastore
import google.oauth2.id_token
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from werkzeug.utils import redirect

import database_helper
import mainHelper
from flask_restful import Api, Resource, reqparse, abort
import os
import pymysql
from Actions import Decode, Delete, ResetDefault, Download, Upload, Update, Search

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ece-461-project-2-22-44eb5eb60671.json"

# firebase = firebase.FirebaseApplication('https://ece-461-project-2-22-default-rtdb.firebaseio.com/', None)
data = {
    'Name': 'Alia Ahmed'
}

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = str(os.urandom(48))
jwt = JWTManager(app)
firebase_request_adapter = requests.Request()

# random key is needed to keep the connection secure to the server
app.config['SECRET_KEY'] = 'os.urandom(48)'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
# db.init_app(app)
# db.create_all(app=app)

ROWS_PER_PAGE = 5
# Bucket name for GCP
MAIN_BUCKET_NAME = "acme_corporation_general"


@app.route("/token", methods=["POST"])
def create_token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    # Query your database for username and password
    # user = User.query.filter_by(username=username, password=password).first()
    # if user is None:
    # the user was not found on the database
    #    return jsonify({"msg": "Bad username or password"}), 401

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
    if os.environ.get('GAE_ENV') == 'standard' or True:
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(database_helper.db_connection_name)
        cnx = pymysql.connect(user=database_helper.db_user, password=database_helper.db_password,
                              unix_socket=unix_socket, db=database_helper.db_name)
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
    select = request.form.get('requestType')
    if select == "list":
        if id == "":
            return get_packages()
        else:
            return get_package_by_id(id)
        # get packages
    elif select == "upload":
        return post_package()
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
            return delete_all_packages()
        else:
            return delete_package_by_id(id)
        # delete stuff
    else:
        pass
        # error then, dont think this is possible though
    return "this is " + select + " and " + str(id)


@app.route('/packages', methods=['POST'])
def get_packages():
    try:
        offset = request.args.get('offset')
        print(offset)
        header = request.headers.get('Content-Type')
        print(header)

        d = (str(request.data.decode('utf-8')))
        print(d)
        data_list_dict = json.loads(d)
        print(data_list_dict)

        # returns list of dictionaries
        packages = database_helper.get_packages(data_list_dict, offset)

        # TODO: database fetching

        resp = Response(response=packages,
                        status=200,
                        mimetype="application/json")
    except Exception as e:
        print("yikes")
        print(str(e))
        resp = make_response({"code" : 500, "message" : "Unexpected Error"})
        resp.mimetype = 'application/json'

    return resp

    # return render_template('page.html', endpoint='GET: packages')


@app.route('/reset', methods=['DELETE'])
def delete_all_packages():
    # return 200 registry is reset
    # return 401 no permissions to reset the registry

    permission = True

    if permission:
        database_helper.delete_all_packages()
        status_code = 200
        # Cloud Storage: Reset bucket to default, empty all objects
        ResetDefault.reset_default(MAIN_BUCKET_NAME)
    else:
        status_code = 401

    resp = Response(status=status_code)

    return resp


@app.route('/package/<id>', methods=['GET'])
def get_package_by_id(id):
    print(id)

    # returns in the format Name Version Filename Url Content
    ret_data = database_helper.get_package_by_id(id)

    data = {
        "metadata": {
            "Name": ret_data['Name'],
            "Version": ret_data['Version'],
            "ID": str(id)
        },
        "data": {
            "Content": ret_data['Content'],
            "URL": ret_data['URL'],
            "JSProgram": "None"
        }
    }

    r = make_response(data)
    r.mimetype = 'application/json'

    # TODO: Use data for GCP

    render_template('page.html', endpoint=('GET: package/' + str(id)))
    return r


@app.route('/package/<id>', methods=['PUT'])
def update_package(id):
    # the name, version, and ID must match
    # the package contents will replace the previous contents
    print(id)

    print(request.data)

    root_parser = reqparse.RequestParser()
    root_parser.add_argument('metadata', type=dict)
    root_parser.add_argument('data', type=dict)

    message_parser = reqparse.RequestParser()
    message_parser.add_argument('Name', type=str, location=('metadata',), required=True)
    message_parser.add_argument('Version', type=str, location=('metadata',), required=True)
    message_parser.add_argument('ID', type=str, location=('metadata',), required=True)

    message_parser.add_argument('Content', type=str, location=('data',), required=False)
    message_parser.add_argument('URL', type=str, location=('data',), required=False)
    message_parser.add_argument('JSProgram', type=str, location=('data',), required=False)

    root_args = root_parser.parse_args()
    print(root_args)

    d = (str(request.data.decode('utf-8')))
    print(d)
    data_list_dict = json.loads(d)
    print(data_list_dict)

    # args = message_parser.parse_args(req=root_args)
    name = (data_list_dict['metadata']['Name'])
    version = (data_list_dict['metadata']['Version'])
    p_id = (data_list_dict['metadata']['ID'])
    url = (data_list_dict['data']['URL'])

    # Decode: Put the encoded string to a text file
    current_path = os.getcwd()
    encoded_text_file = (data_list_dict['data']['Content'])
    complete_text_file_path, output_filename_txt = Decode.string_to_text_file(
        encoded_text=encoded_text_file,
        text_file_folder_path=current_path,
        filename_original=name
    )

    if database_helper.get_package_by_id(p_id) is not None:
        database_helper.update_package(name, version, p_id, url, filename=complete_text_file_path)
        Update.update_file(
            bucket_name=MAIN_BUCKET_NAME,
            object_name=output_filename_txt,
            source_file_local=complete_text_file_path
        )
        status_code = 200
    else:
        status_code = 400

    # response 200 for success
    # response 400 for a malformed request: no such package

    return Response(status=status_code)


@app.route('/package/<id>', methods=['DELETE'])
def delete_package_by_id(id):
    print(id)
    database_helper.delete_package_by_id(id)
    # TODO: Need name of the package for GCP
    # response 200 for success
    # response 400 for a malformed request: no such package
    return render_template('page.html', endpoint=('DELETE: package/' + str(id)))


@app.route('/package', methods=['POST'])
def post_package():
    header = request.headers.get('X-Authorization')
    print(header)

    d = (str(request.data.decode('utf-8')))
    print(d)
    data_list_dict = json.loads(d)
    print(data_list_dict)

    # args = message_parser.parse_args(req=root_args)
    name = (data_list_dict['metadata']['Name'])
    version = (data_list_dict['metadata']['Version'])
    p_id = (data_list_dict['metadata']['ID'])
    url = (data_list_dict['data']['URL'])

    # if package exists already: return 403 code
    # status_code = flask.Response(status=201)

    ingestion = 1
    for key, value in data_list_dict['data'].items():
        if key == 'Content':
            ingestion = 0

    if ingestion == 0: #upload content string
        current_path = os.getcwd()
        encoded_text_file = (data_list_dict['data']['Content'])
        complete_zip_file_path = Decode.string_to_text_file(encoded_text=encoded_text_file,
                                                            text_file_folder_path=current_path)

        # todo link the filename field to the bucket/filename
        # todo add a column in the database for permissions/security

        # Decode.py: Encoded string to text file
        current_path = os.getcwd()
        encoded_text_file = (data_list_dict['data']['Content'])
        complete_text_file_path, output_filename_txt = Decode.string_to_text_file(
            encoded_text=encoded_text_file,
            text_file_folder_path=current_path,
            filename_original=name
        )

        conn = database_helper.mysql_connect()
        if database_helper.get_package_by_id(p_id) is None:
            database_helper.post_package(name, version, p_id, url, complete_zip_file_path)
            # Cloud Storage: Uploading file to GCP.
            Upload.upload_file(
                source_file_local=complete_text_file_path,
                destination_bucket_gcp=MAIN_BUCKET_NAME,
            )
            status_code = 201
        else:
            status_code = 403
        database_helper.mysql_close(conn)
    else:
        scores = mainHelper.rate(url)
        ingestible = 1
        for key, value in scores.items():
            if value < 0.5:
                ingestible = 0
        if ingestible == 1:
            conn = database_helper.mysql_connect()
            if database_helper.get_package_by_id(p_id) is None:
                database_helper.post_package(name, version, p_id, url, None)
                status_code = 201
            else:
                status_code = 403 #todo: need value to be changed?
            database_helper.mysql_close(conn)
        else:
            status_code = 403 #todo: need value to be changed?


    # if malformed request

    data = {"Name": name, "Version": version, "ID": p_id}
    r = make_response(data)
    r.mimetype = 'application/json'
    r.status_code = status_code

    # Remove file when successfully uploaded
    if ingestion == 0:
        os.remove(complete_text_file_path)

    return r
    # response = Response(response=data, status=201, mimetype='application/json')


@app.route('/package/<id>/rate', methods=['GET'])
def rate_package_by_id(id):
    # print(id)
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
    variables = database_helper.get_package_by_id(id)
    if variables['URL'] == "":  # no URL, get from package.json
        # TODO: file = decode(variables['Filename'] ---> Santiago's code
        # It should be something like
        jsonFile = mainHelper.getPackageJson("output_file.zip")  # TODO: change input to file
        if jsonFile != None:
            url = mainHelper.getURL(jsonFile)
            data = mainHelper.rate(url)
    else:  # use URL
        data = mainHelper.rate(variables['URL'])

    r = make_response(data)
    r.mimetype = 'application/json'
    # TODO: return 400 for no such package; return 500 for failure in rating
    return r

    # return render_template('page.html', endpoint=('GET: package/' + str(id)) + '/rate')


@app.route('/authenticate', methods=['PUT'])
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
    print(name)
    # on success return package history
    # on no such package return 400
    # on error default

    database_helper.get_package_by_name(name)

    # Download file from GCP
    filename_in_gcp = Search.find_object(MAIN_BUCKET_NAME, name)
    if filename_in_gcp is not None:
        current_path = os.getcwd()
        Download.download_file(
            bucket=MAIN_BUCKET_NAME,
            file_to_download=filename_in_gcp,
            destination_folder_local=current_path  # Where to download?
        )
    else:
        print("File not found on GCP")

    r = make_response(data)
    r.mimetype = 'application/json'
    # return 400 for no such package; return 500 for failure in rating
    render_template('page.html', endpoint=('GET: package/byName/' + str(name)))
    return r


@app.route('/package/byName/<name>', methods=['DELETE'])
def delete_package_by_name(name):
    print(name)
    database_helper.delete_package_by_name(name)
    # Delete file from GCP
    filename_in_gcp = Search.find_object(MAIN_BUCKET_NAME, name)
    if filename_in_gcp is not None:
        Delete.delete_object(
            bucket_name=MAIN_BUCKET_NAME,
            object_name=filename_in_gcp
        )
    else:
        print("File not found on GCP")
    # return 400 for no such package; return 200 for success
    return render_template('page.html', endpoint=('DELETE: package/byName/' + str(name)))


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
