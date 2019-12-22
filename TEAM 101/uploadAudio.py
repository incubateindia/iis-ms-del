import os
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify

app = Flask(__name__)
app.config['FILE_UPLOADS']="./audio_uploads/"

@app.route('/audio', methods=['GET', 'POST'])
def upload_file():
    if request.method=='POST':
        if request.files:
            file = request.files['file']
            if file.filename=='':
                return "empty"
            if file: 
                filename = file.filename
                file.save(os.path.join(app.config['FILE_UPLOADS'],filename))
                print(filename)
                return "saved"
    return jsonify("waiting")