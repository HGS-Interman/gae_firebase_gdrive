from __future__ import print_function
from flask import Flask, request, make_response, jsonify
import os.path
import werkzeug
import datetime
import mimetypes

# Google Drive
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.http import MediaFileUpload

# firebase
import firebase_admin
from firebase_admin import firestore


TMP_FOLDER = '/tmp/'
app = Flask(__name__)

@app.route('/', methods=['POST'])
def upload_multipart():
    '''ファイルアップロード'''
    app.logger.debug('upload_multipart')
    if 'uploadFile' not in request.files:
        make_response(jsonify({'result':'uploadFileが必要です'}))
    app.logger.debug(f'request.files:{request.files}')
    upload_file = request.files['uploadFile']
    folder_id = '1Y8EKzqUJIx467rTh0f8zaw9O_fP_kExL'
    
    fileName = upload_file.filename
    if '' == fileName:
        make_response(jsonify({'result':'filenameが空です。filenameを指定してください。'}))

    saveFileName = werkzeug.utils.secure_filename(fileName)
    temp_filepath = os.path.join(TMP_FOLDER, saveFileName)
    upload_file.save(temp_filepath)

    drive_file = upload_google_drive_upload(temp_filepath, folder_id)

    firebase_data = {'filename':fileName, 'drive_file':drive_file, 'timestamp':datetime.datetime.now().isoformat(), 'result':'upload ok'}

    add_firestore('file_upload', fileName, firebase_data)

    return make_response(jsonify(firebase_data))


@app.route('/', methods=['GET'])
def show_upload_form():
    html =  '<html><body><form method="post" action="/" enctype="multipart/form-data">'\
            '<h2>Googleドライブにアップロードします</h2>'\
            '<p>Google Drive Folder ID: 1Y8EKzqUJIx467rTh0f8zaw9O_fP_kExL'\
            '<p>Upload File: '\
            '<input type="file" name="uploadFile"></p>'\
            '<p></p><input type="submit" value="アップロード">'\
            '</body></html>'
    
    return html


def upload_google_drive_upload(filepath, parents_folder_id=None):
    '''GoogleDriveにアップロードする'''
    # mimetypeを取得
    file_basename = os.path.basename(filepath)
    mimetype = mimetypes.guess_type(file_basename)[0]
    if parents_folder_id:
        file_metadata = {'name': file_basename,'mimetype': mimetype, 'parents':[parents_folder_id] }
    else:
        file_metadata = {'name': file_basename,'mimetype': mimetype}
    
    creds = Credentials.from_service_account_file('drive_service_account.json')
    drive_service = build('drive', 'v3', credentials=creds)
    media = MediaFileUpload(filepath, mimetype = mimetype)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    return file


def add_firestore(collection, document, data):
    # credentialsの作成
    cred = firebase_admin.credentials.Certificate("firebase_service_account.json")
    # firebase_admin初期化
    firebase_admin.initialize_app(cred)
    # firebase client
    db = firestore.client()

    # firestoreに追加
    doc_ref = db.collection(collection).document(document)
    doc_ref.set(data)


# main
if __name__ == "__main__":
    print(app.url_map)
    app.run(host='localhost', port=8000, debug=True)