from flask import Flask, request, jsonify
import os
from datetime import datetime
import cloudinary
import cloudinary.uploader
from werkzeug.utils import secure_filename

app = Flask(__name__)  # Initialize Flask app with the correct __name__

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)  # Create uploads folder if it doesn't exist

# Cloudinary configuration - fill in your details
cloudinary.config(
    cloud_name="dvv568z7k",
    api_key="159433497574657",
    api_secret="EjV1qwN2sd7SHTr9pHr-ah7rueo"
)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    # If no file is selected
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        # Secure the filename to avoid directory traversal attacks
        filename = secure_filename(file.filename)  
        # Add timestamp to filename to avoid collisions
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)  # Save file locally

        # Upload the saved file to Cloudinary as raw file
        try:
            result = cloudinary.uploader.upload(filepath, resource_type='raw')
            cloudinary_url = result['secure_url']
            return jsonify({
                'message': 'File uploaded successfully',
                'local_path': filepath,
                'cloudinary_url': cloudinary_url
            }), 200
        except Exception as e:
            # Return error if upload to Cloudinary fails
            return jsonify({'error': f'Cloudinary upload failed: {str(e)}'}), 500

    # Catch all unknown errors
    return jsonify({'error': 'Unknown error'}), 500


if __name__ == '__main__':
    # Run Flask app on all IP addresses on port 5000 with debug mode on
    app.run(host='0.0.0.0', port=5000, debug=True)
