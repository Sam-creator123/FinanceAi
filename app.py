from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename

# Simplified Flask app (no CORS). Frontend is served from this same app so cross-origin isn't needed.
# Serve static files from project root so existing structure (styles/, scripts/, etc.) works
app = Flask(__name__, static_folder='.', template_folder='templates')

# Import local analysis helpers
import backend as backend_helpers

# Upload folders
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_ROOT = os.path.join(BASE_DIR, 'backendd')
IMAGE_FOLDER = os.path.join(UPLOAD_ROOT, 'images')
VOICE_FOLDER = os.path.join(UPLOAD_ROOT, 'voices')

os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(VOICE_FOLDER, exist_ok=True)

ALLOWED_IMAGE_EXT = {'png', 'jpg', 'jpeg', 'webp'}
ALLOWED_VOICE_EXT = {'mp3', 'wav', 'ogg', 'm4a'}

def allowed_file(filename, allowed_exts):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_exts


@app.route('/upload/image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file part'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected image file'}), 400

    if not allowed_file(file.filename, ALLOWED_IMAGE_EXT):
        return jsonify({'error': 'Image file type not allowed'}), 400

    filename = secure_filename(file.filename)
    save_path = os.path.join(IMAGE_FOLDER, filename)
    file.save(save_path)
    return jsonify({'status': 'success', 'filename': filename}), 200


    if 'voice' not in request.files:
        return jsonify({'error': 'No voice file part'}), 400

    file = request.files['voice']
    if file.filename == '':
        return jsonify({'error': 'No selected voice file'}), 400

    if not allowed_file(file.filename, ALLOWED_VOICE_EXT):
        return jsonify({'error': 'Voice file type not allowed'}), 400


    filename = secure_filename(file.filename)
    save_path = os.path.join(VOICE_FOLDER, filename)
    file.save(save_path)
    return jsonify({'status': 'success', 'filename': filename}), 200


@app.route('/')
def index():
    # Render the Jinja template which references static assets via url_for('static', filename=...)
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """Simple analysis endpoint. Expects JSON with keys:
       {
         "image": "uploaded-image-filename.jpg",
         "voice": "uploaded-voice-filename.wav",
         "text": "optional raw text string"
       }
       Returns JSON with results for image, text and a placeholder voice result.
    """
    data = request.get_json(force=True)
    image_fname = data.get('image')
    voice_fname = data.get('voice')
    text_content = data.get('text', '')

    results = {'image': None, 'text': None, 'voice': None}

    # Image analysis
    try:
        if image_fname:
            image_path = os.path.join(IMAGE_FOLDER, secure_filename(image_fname))
            if os.path.exists(image_path):
                # backend_helpers.analyze_image returns a risk_level between 0 and 1
                risk = backend_helpers.analyze_image(image_path)
                confidence = int(round((1.0 - float(risk)) * 100))
                status = 'authentic' if confidence >= 80 else ('suspicious' if confidence >= 50 else 'fraudulent')
                results['image'] = {
                    'type': 'image',
                    'confidence': confidence,
                    'status': status,
                    'isAuthentic': status != 'fraudulent',
                    'indicators': [f'Image risk score: {risk}'],
                    'timestamp': None,
                }
    except Exception as e:
        results['image'] = {'type': 'image', 'confidence': 0, 'status': 'fraudulent', 'isAuthentic': False, 'indicators': [f'Error: {e}']}

    # Text analysis
    try:
        if text_content:
            text_score = backend_helpers.analyze_text(text_content)
            # analyze_text likely returns a fraud score (higher = more risky)
            confidence = int(round((1.0 - float(text_score)) * 100))
            status = 'authentic' if confidence >= 80 else ('suspicious' if confidence >= 50 else 'fraudulent')
            results['text'] = {
                'type': 'text',
                'confidence': confidence,
                'status': status,
                'isAuthentic': status != 'fraudulent',
                'indicators': [f'Text fraud score: {text_score}'],
                'timestamp': None,
            }
    except Exception as e:
        results['text'] = {'type': 'text', 'confidence': 0, 'status': 'fraudulent', 'isAuthentic': False, 'indicators': [f'Error: {e}']}

    # Voice: placeholder — for a simple backend we just acknowledge the file exists
    try:
        if voice_fname:
            voice_path = os.path.join(VOICE_FOLDER, secure_filename(voice_fname))
            if os.path.exists(voice_path):
                results['voice'] = {
                    'type': 'voice',
                    'confidence': 90,
                    'status': 'authentic',
                    'isAuthentic': True,
                    'indicators': ['Voice file received on server'],
                    'timestamp': None,
                }
            else:
                results['voice'] = {'type': 'voice', 'confidence': 0, 'status': 'fraudulent', 'isAuthentic': False, 'indicators': ['Voice file not found']}
    except Exception as e:
        results['voice'] = {'type': 'voice', 'confidence': 0, 'status': 'fraudulent', 'isAuthentic': False, 'indicators': [f'Error: {e}']}

    return jsonify(results)


if __name__ == '__main__':
    # Run on port 5000 by default
    app.run(host='0.0.0.0', port=5000, debug=True)
