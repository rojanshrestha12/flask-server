from flask import Flask, request, jsonify
import os
from datetime import datetime
import cloudinary
import cloudinary.uploader
from werkzeug.utils import secure_filename
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure upload folder - use absolute path for Render
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    logger.info(f"Created upload folder at: {UPLOAD_FOLDER}")

# Cloudinary configuration
cloudinary.config(
    cloud_name = "dvv568z7k",
    api_key = "159433497574657", 
    api_secret = "EjV1qwN2sd7SHTr9pHr-ah7rueo"
)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        logger.info("=== New Upload Request ===")
        logger.info(f"Request method: {request.method}")
        logger.info(f"Request headers: {dict(request.headers)}")
        logger.info(f"Request files: {request.files}")
        logger.info(f"Request form: {request.form}")
        logger.info(f"Request data: {request.data}")
        
        if 'file' not in request.files:
            logger.error("No file part in request")
            return jsonify({'error': 'No file part in request'}), 400
        
        file = request.files['file']
        if file.filename == '':
            logger.error("No selected file")
            return jsonify({'error': 'No selected file'}), 400
        
        if file:
            # Save file locally
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            
            logger.info(f"Attempting to save file to: {filepath}")
            file.save(filepath)
            logger.info(f"File saved successfully at: {filepath}")
            
            try:
                logger.info("Attempting to upload to Cloudinary as raw file...")
                # Upload to Cloudinary as raw file
                result = cloudinary.uploader.upload(
                    filepath,
                    resource_type="raw",  # Specify raw upload for .txt files
                    public_id=f"raw_uploads/{filename}",  # Organize in a specific folder
                    overwrite=True,  # Overwrite if file exists
                    resource_options={
                        "access_mode": "public"  # Make it publicly accessible
                    }
                )
                cloudinary_url = result['secure_url']
                logger.info(f"File uploaded to Cloudinary: {cloudinary_url}")
                
                # Clean up local file after successful upload
                try:
                    os.remove(filepath)
                    logger.info(f"Local file removed: {filepath}")
                except Exception as e:
                    logger.warning(f"Failed to remove local file: {str(e)}")
                
                # Return both local and cloudinary URLs
                return jsonify({
                    'message': 'File uploaded successfully',
                    'cloudinary_url': cloudinary_url,
                    'public_id': result.get('public_id'),
                    'resource_type': result.get('resource_type')
                })
            except Exception as e:
                logger.error(f"Cloudinary upload failed: {str(e)}")
                # Clean up local file if upload fails
                try:
                    os.remove(filepath)
                    logger.info(f"Local file removed after failed upload: {filepath}")
                except Exception as cleanup_error:
                    logger.warning(f"Failed to remove local file after failed upload: {str(cleanup_error)}")
                return jsonify({'error': f'Cloudinary upload failed: {str(e)}'}), 500
            
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

# Health check endpoint for Render
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    # Get port from environment variable (Render sets this)
    port = int(os.environ.get('PORT', 6000))
    logger.info(f"Server starting on port {port}")
    logger.info(f"Upload folder: {UPLOAD_FOLDER}")
    app.run(host='0.0.0.0', port=port, debug=False) 