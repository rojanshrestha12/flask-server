from flask import Flask, request
from datetime import datetime
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create folder if it doesn't exist

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part in request', 400

    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file', 400

    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    
    file.save(file_path)

    print(f"✅ File saved to {file_path}")
    return 'File received and saved', 200


@app.route('/files', methods=['GET'])
def list_files():
    try:
        files = os.listdir(UPLOAD_FOLDER)
        return '<br>'.join(files)
    except Exception as e:
        return f"Error reading upload folder: {e}", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
