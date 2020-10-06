# Google Drive
from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.http import MediaFileUpload

# firebase
import firebase_admin
from firebase_admin import firestore


from flask import Flask


app = Flask(__name__)
os.chdir(os.path.dirname(os.path.abspath(__file__)))


@app.route('/')
def hello():
    return 'hello test'


@app.route('/drive')
def drive():
    # サービスアカウントのcredentialsを作成
    creds = Credentials.from_service_account_file('drive_service_account.json')

    # Google Drive API v3 
    drive_service = build('drive', 'v3', credentials=creds)
    # メタデータを設定
    file_metadata = {'name': 'hoge.txt','mimetype': 'text/html', 'parents':['******************'] }

    # アップロード用のローカルファイルを設定
    media = MediaFileUpload('hoge.txt', mimetype = 'text/html')

    # アップロード実行
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()

    # ファイルのリストを表示
    results = drive_service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()

    items = results.get('files', [])

    if not items:
        res = 'No files found.'
    else:
        res ='Files:'
        for item in items:
            res = res + (u'{0} ({1}), '.format(item['name'], item['id']))

    res = res + '\r\n' + (f'upload File ID: {file.get("id")}')
    return res

@app.route('/firebase')
def firebase():
    '''firebaseの動作確認
    '''
    # credentialsの作成
    cred = firebase_admin.credentials.Certificate("firebase_service_account.json")
    # firebase_admin初期化
    firebase_admin.initialize_app(cred)
    # firebase client
    db = firestore.client()

    # firestoreに追加
    doc_ref = db.collection(u'users').document(u'alovelace')
    doc_ref.set({
        u'first': u'Ada',
        u'last': u'Lovelace',
        u'born': 1815
    })

    return 'ok'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
