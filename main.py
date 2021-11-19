import datetime
from Actions import Create, Upload, Download

from flask import Flask, render_template, request
#from firebase import firebase
#from google.cloud import storage
from google.auth.transport import requests
#from google.cloud import datastore
import google.oauth2.id_token

import os

import mainHelper

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ece-461-project-2-22-44eb5eb60671.json"

#firebase = firebase.FirebaseApplication('https://ece-461-project-2-22-default-rtdb.firebaseio.com/', None)
data = {
    'Name' : 'Alia Ahmed'
}
#result = firebase.post('ece-461-project-2-22-default-rtdb/User', data)
#print(result)
#result = firebase.get('ece-461-project-2-22-default-rtdb/User', '')
#print(result)
#firebase.put('ece-461-project-2-22-default-rtdb/User/-MnxvizzcJgrLFXzUMsE', 'Name', 'rania')
#firebase.delete('ece-461-project-2-22-default-rtdb/User/', '-MnxvizzcJgrLFXzUMsE''')
#print("deleted")

#client = storage.Client()
#bucket = client.get_bucket('staging.ece-461-project-2-22.appspot.com')
#imageBlob = bucket.blob("/")
#imagePath = "IMG_3047.JPG"
#imageBlob = bucket.blob("IMG_3047")
#imageBlob.upload_from_filename(imagePath)

app = Flask(__name__)
firebase_request_adapter = requests.Request()


@app.route('/')
def root():
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
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

    return render_template('index.html', times=dummy_times, endpoint='root', user_data=claims, error_message=error_message)

@app.route('/start', methods=['POST'])
def start():
    id = request.form['id']
    name = request.form['name']
    url = request.form['url']
    content = request.form['content']
    select = request.form.get('requestType')
    if select == "list":
        if id == "":
            return get_packages()
        else:
            return get_package_by_id(id)
        #get packages
    elif select == "upload":
        return post_package(content)
        #upload stuff
    elif select == "update":
        return update_package(id)
        #update stuff
    elif select == "rate":
        if id == "":
            return "Invalid package Id"
        else:
            return rate_package_by_id(id)
        #rate stuff
    elif select == "delete":
        if id == "":
            return delete_all_packages()
        else:
            return delete_package_by_id(id)
        #delete stuff
    else:
        pass
        #error then, dont think this is possible though
    return "this is " + select + " and " + str(id)

@app.route('/packages', methods=['GET'])
def get_packages():
    return render_template('page.html', endpoint='GET: packages')


@app.route('/reset', methods=['DELETE'])
def delete_all_packages():
    return render_template('page.html', endpoint='DELETE: reset')


@app.route('/package/<id>', methods=['GET'])
def get_package_by_id(id):
    return render_template('page.html', endpoint=('GET: package/' + str(id)))


@app.route('/package/<id>', methods=['PUT'])
def update_package(id):
    return render_template('page.html', endpoint=('PUT: package/' + str(id)))


@app.route('/package/<id>', methods=['DELETE'])
def delete_package_by_id(id):
    return render_template('page.html', endpoint=('DELETE: package/' + str(id)))


@app.route('/package', methods=['POST'])
def post_package(content=None):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/Users/justinlukowski/Downloads" \
                                            "ece-461-project-2-22-441ab13258f1.json"


    bucketName = "test_justin_139pm"
    fileName = content

    #print("create")
    #Create.create_bucket(bucketName)
    print("upload")
    Upload.upload_file(input, f"gs://{bucketName}")

    return render_template('page.html', endpoint='POST: package')


@app.route('/package/<id>/rate', methods=['GET'])
def rate_package_by_id(id):
    bucket = "test_justin_139pm"
    filename_gcp = "encoded-20211117185003.txt"
    folder_dest_local = "/Users/justinlukowski/Documents/461/project-2-22/justintest"

    print("download")
    Download.download_file(bucket, filename_gcp, folder_dest_local)

    print("rank - main")
    mainHelper.rank("/Users/justinlukowski/Documents/461/project-2-22/justintest/encoded-20211117185003.txt")

    return render_template('page.html', endpoint=('GET: package/' + str(id)) + '/rate')


@app.route('/authenticate', methods=['PUT'])
def authenticate():
    return render_template('page.html', endpoint='GET: authenticate')


@app.route('/package/byName/{name}', methods=['GET'])
def get_package_by_name(name):
    return render_template('page.html', endpoint=('GET: package/byName/' + str(name)))


@app.route('/package/byName/{name}', methods=['DELETE'])
def delete_package_by_name(name):
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
