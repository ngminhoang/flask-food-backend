import requests
from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
from services.DetectImageService import analyze_image
import os

analyze_bp = Blueprint('analyze', __name__)

@analyze_bp.route('/api/analyze', methods=['POST'])
def analyze():
    # Get the API key from config
    api_key = current_app.config['API_KEY']

    # Check if an image file is included in the request
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    # Get the image from the request
    image = request.files['image']
    filename = secure_filename(image.filename)

    # Set up the temporary directory from config
    tmp_dir = current_app.config['TMP_DIR']
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    image_path = os.path.join(tmp_dir, filename)
    image.save(image_path)

    # Call the analyze_image function
    try:
        result = analyze_image(api_key, image_path)
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Optionally, remove the image after processing if not needed
        if os.path.exists(image_path):
            os.remove(image_path)
