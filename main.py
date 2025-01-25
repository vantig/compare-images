from flask import Flask, request, jsonify
from PIL import Image
import imagehash
import base64
from io import BytesIO

base64_image = "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"
base64_image2 = "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"

app = Flask(__name__)


@app.route('/api/compare-image', methods=['POST'])
def hash_image():
    try:
        # Get JSON payload
        data = request.json
        if not data or 'base64_image' not in data:
            return jsonify({"error": "Missing 'base64_image' in request"}), 400

        # Decode the base64 image
        base64_image2 = data['base64_image']

        # Decode the base64 string into bytes
        image_data = base64.b64decode(base64_image)
        image_data2 = base64.b64decode(base64_image2)

        # Create a BytesIO object from the bytes
        image_bytes = BytesIO(image_data)
        image_bytes2 = BytesIO(image_data2)
        image1 = Image.open(image_bytes)
        image2 = Image.open(image_bytes2)

        hash1 = imagehash.average_hash(image1)
        hash2 = imagehash.average_hash(image2)
        print(hash1 - hash2)

        return jsonify({"isEqual": hash1 - hash2 < 4}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500