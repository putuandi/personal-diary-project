import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template( 'index.html' )

@app.route("/diary/delete", methods=["POST"])
def delete():
    title_delete = request.form['delete_title']
    db.diary.delete_one({'title' : title_delete})
    return jsonify({'msg': 'delete done!'})

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({}, {'_id':False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')
    
    today = datetime.now();
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    time_upload = today.strftime('%Y.%m.%d')
    
    if 'file_give' not in request.files:
        filename = 'static/default-image.jpg'
    else:
        file = request.files['file_give']
        extension = file.filename.split('.')[-1]
        filename = f'static/post-{mytime}.{extension}'
        file.save(filename)
    
    if 'image_profile_give' not in request.files:
        filename_profile = 'static/default-profile.jpg'
    else:
        image_profile = request.files['image_profile_give']
        extension_profile = image_profile.filename.split('.')[-1]
        filename_profile = f'static/profile-{mytime}.{extension_profile}'
        image_profile.save(filename_profile)
    
    doc = {
        'file': filename,
        'image_profile': filename_profile,
        'title': title_receive,
        'content' : content_receive,
        'time_upload': time_upload
    }
    db.diary.insert_one(doc)
    return jsonify({'msg': 'data was saved!'})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)