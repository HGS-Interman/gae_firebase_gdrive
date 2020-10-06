# gae_firebase_gdrive
google app engineでfirebaseとgoogle driveを動かす

---
## Google Drive認証情報の準備
1. Google Drive APIを有効化する
2. サービスアカウントを作成する
3. 認証情報をダウンロードする(JSON)
4. フォルダにコピーする　"drive_service_account.json"
---
## Firebase認証情報の準備
1. Firebase Admin サービスアカウントを作成する
2. 認証情報をダウンロードする(JSON)
3. フォルダにコピーする　"firebase_service_account.json"

---
## ローカルで動作確認
```
pip install -r requirements.txt
python3 main.py
```
---
## GAEにdeployする
```
git clone https://github.com/HGS-Interman/gae_firebase_gdrive.git
cd gae_firebase_gdrive
gcloud app deploy
gcloud app browse
```
