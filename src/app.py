from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)

# app = CORS(app)

# Set the upload folder
UPLOAD_FOLDER = './songs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html', message=None)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return render_template('index.html', message='No file part')

    file = request.files['file']

    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return render_template('index.html', message='No selected file')

    # Check if the file has an allowed extension
    allowed_extensions = {'mp3', 'wav'}
    if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return render_template('index.html', message='Invalid file type. Allowed types: mp3, wav')

    # Save the file to the upload folder
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

    return render_template('index.html', message='File uploaded successfully')

if __name__ == '__main__':
    app.run(debug=True, port=8000)