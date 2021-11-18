import datetime

from flask import Flask, render_template, request, url_for, make_response, Response, jsonify
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required

from firebase import firebase
from google.cloud import storage
from google.auth.transport import requests
from google.cloud import datastore
import google.oauth2.id_token
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from werkzeug.utils import redirect

from database_helper import *
from flask_restful import Api, Resource, reqparse, abort
import os

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ece-461-project-2-22-44eb5eb60671.json"

# firebase = firebase.FirebaseApplication('https://ece-461-project-2-22-default-rtdb.firebaseio.com/', None)
data = {
    'Name': 'Alia Ahmed'
}
# result = firebase.post('ece-461-project-2-22-default-rtdb/User', data)
# print(result)
# result = firebase.get('ece-461-project-2-22-default-rtdb/User', '')
# print(result)
# firebase.put('ece-461-project-2-22-default-rtdb/User/-MnxvizzcJgrLFXzUMsE', 'Name', 'rania')
# firebase.delete('ece-461-project-2-22-default-rtdb/User/', '-MnxvizzcJgrLFXzUMsE''')
# print("deleted")

# client = storage.Client()
# bucket = client.get_bucket('staging.ece-461-project-2-22.appspot.com')
# imageBlob = bucket.blob("/")
# imagePath = "IMG_3047.JPG"
# imageBlob = bucket.blob("IMG_3047")
# imageBlob.upload_from_filename(imagePath)

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = str(os.urandom(48))
jwt = JWTManager(app)
firebase_request_adapter = requests.Request()

# random key is needed to keep the connection secure to the server
app.config['SECRET_KEY'] = 'os.urandom(48)'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db.init_app(app)
db.create_all(app=app)

ROWS_PER_PAGE = 5


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
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
    if current_user.is_authenticated:
        print("Current user is authenticated")
    else:
        print("Current user is not authenticated")

    dummy_times = [datetime.datetime(2018, 1, 1, 10, 0, 0),
                   datetime.datetime(2018, 1, 2, 10, 30, 0),
                   datetime.datetime(2018, 1, 3, 11, 0, 0),
                   ]

    # Verify Firebase auth.
    id_token = request.cookies.get("token")
    error_message = None
    claims = None

    if id_token:
        try:
            # Verify the token against the Firebase Auth API. This example
            # verifies the token on each page load. For improved performance,
            # some applications may wish to cache results in an encrypted
            # session store (see for instance
            # http://flask.pocoo.org/docs/1.0/quickstart/#sessions).
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)
        except ValueError as exc:
            # This will be raised if the token is expired or any other
            # verification checks fail.
            error_message = str(exc)

        # Record and fetch the recent times a logged-in user has accessed
        # the site. This is currently shared amongst all users, but will be
        # individualized in a following step.

    print(claims)

    return render_template('index.html', times=dummy_times, endpoint='root', user_data=claims,
                           error_message=error_message)


@app.route('/packages', methods=['GET'])
def get_packages():
    offset = request.args.get('offset')
    print(offset)
    header = request.headers.get('Content-Type')
    print(header)

    message_parser = reqparse.RequestParser()
    message_parser.add_argument('Version', type=str)
    message_parser.add_argument('Name', type=str)
    args = message_parser.parse_args()

    print(args['Version'])
    print(args['Name'])

    #TODO: database fetching

    data = '''[{"id": 1,
            "name": "Zaza",
            "tag": "cat"},
            {"id": 1,
             "name": "Zaza",
             "tag": "cat"}
            ]'''

    resp = Response(response=data,
                    status=200,
                    mimetype="application/json")

    return resp

    # return render_template('page.html', endpoint='GET: packages')


@app.route('/reset', methods=['DELETE'])
def delete_all_packages():
    # return 200 registry is reset
    # return 401 no permissions to reset the registry
    return render_template('page.html', endpoint='DELETE: reset')


@app.route('/package/<id>', methods=['GET'])
def get_package_by_id(id):
    print(id)
    data = {
        "metadata": {
            "Name": "string",
            "Version": "1.2.3",
            "ID": "string"
        },
        "data": {
            "Content": "string",
            "URL": "string",
            "JSProgram": "string"
        }
    }

    r = make_response(data)
    r.mimetype = 'application/json'

    render_template('page.html', endpoint=('GET: package/' + str(id)))
    return r


@app.route('/package/<id>', methods=['PUT'])
def update_package(id):
    # the name, version, and ID must match
    # the package contents will replace the previous contents
    print(id)

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
    args = message_parser.parse_args(req=root_args)
    print(args['Name'])
    print(args['Version'])
    print(args['ID'])

    # response 200 for success
    # response 400 for a malformed request: no such package

    return render_template('page.html', endpoint=('PUT: package/' + str(id)))


@app.route('/package/<id>', methods=['DELETE'])
def delete_package_by_id(id):
    print(id)
    # response 200 for success
    # response 400 for a malformed request: no such package
    return render_template('page.html', endpoint=('DELETE: package/' + str(id)))


@app.route('/package', methods=['POST'])
def post_package():
    header = request.headers.get('X-Authorization')
    print(header)

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
    args = message_parser.parse_args(req=root_args)
    print(args['Name'])
    print(args['Version'])
    print(args['ID'])

    # if package exists already: return 403 code
    # status_code = flask.Response(status=201)

    # if malformed request

    data = {"Name": "string", "Version": "1.2.3", "ID": "test"}
    r = make_response(data)
    r.mimetype = 'application/json'
    return r
    # response = Response(response=data, status=201, mimetype='application/json')


@app.route('/package/<id>/rate', methods=['GET'])
def rate_package_by_id(id):
    print(id)
    #if successful rating
    data = {
          "BusFactor": 0,
          "Correctness": 0,
          "RampUp": 0,
          "ResponsiveMaintainer": 0,
          "LicenseScore": 0,
          "GoodPinningPractice": 0
        }
    r = make_response(data)
    r.mimetype = 'application/json'
    # return 400 for no such package; return 500 for failure in rating
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

    data = {
              "id": 1,
              "name": "Zaza",
              "tag": "cat"
            }
    r = make_response(data)
    r.mimetype = 'application/json'
    # return 400 for no such package; return 500 for failure in rating
    render_template('page.html', endpoint=('GET: package/byName/' + str(name)))
    return r


@app.route('/package/byName/<name>', methods=['DELETE'])
def delete_package_by_name(name):
    print(name)
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
