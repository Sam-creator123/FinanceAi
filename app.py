from flask import Flask, request, jsonify, render_template, send_from_directory
import os
from werkzeug.utils import secure_filename
from backend import analyze_image, analyze_text, analyze_voice

app = Flask(__name__, 
            static_folder='static',
            static_url_path='/static',
            template_folder='templates')

# Configuration
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {
    'image': {'png', 'jpg', 'jpeg', 'webp'},
    'voice': {'mp3', 'wav', 'ogg', 'm4a'},
    'text': {'txt'}
}

def allowed_file(filename, file_type):
    if not filename:
        return False
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS[file_type]

@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/x-icon')

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Accepts multipart form data with:
    - image: image file (optional)
    - voice: audio file (optional)
    - text: text file or text content (optional)
    Returns analysis results as JSON
    """
    results = {}
    
    try:
        # Handle image
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file and image_file.filename != '':
                if not allowed_file(image_file.filename, 'image'):
                    results['image'] = {'error': 'Invalid file type for image'}
                else:
                    filename = secure_filename(image_file.filename)
                    img_path = os.path.join(UPLOAD_FOLDER, filename)
                    image_file.save(img_path)
                    
                    try:
                        risk_score = analyze_image(img_path)
                        confidence = int((1.0 - float(risk_score)) * 100)
                        results['image'] = {
                            'confidence': confidence,
                            'status': 'authentic' if confidence >= 70 else 'suspicious',
                            'risk_score': float(risk_score)
                        }
                    except Exception as e:
                        results['image'] = {'error': str(e), 'status': 'error'}
        
        # Handle text
        if 'text' in request.files:
            text_file = request.files['text']
            if text_file and text_file.filename != '':
                if not allowed_file(text_file.filename, 'text'):
                    results['text'] = {'error': 'Invalid file type for text'}
                else:
                    text_content = text_file.read().decode('utf-8')
                    
                    try:
                        fraud_score = analyze_text(text_content)
                        confidence = int((1.0 - float(fraud_score)) * 100)
                        results['text'] = {
                            'confidence': confidence,
                            'status': 'authentic' if confidence >= 70 else 'suspicious',
                            'fraud_score': float(fraud_score)
                        }
                    except Exception as e:
                        results['text'] = {'error': str(e), 'status': 'error'}
        
        # Handle voice
        if 'voice' in request.files:
            voice_file = request.files['voice']
            if voice_file and voice_file.filename != '':
                if not allowed_file(voice_file.filename, 'voice'):
                    results['voice'] = {'error': 'Invalid file type for voice'}
                else:
                    filename = secure_filename(voice_file.filename)
                    voice_path = os.path.join(UPLOAD_FOLDER, filename)
                    voice_file.save(voice_path)
                    
                    try:
                        match_result = analyze_voice(voice_path)
                        # Convert match_result to boolean if needed
                        if isinstance(match_result, str):
                            # Assuming analyze_voice returns string
                            confidence = 85  # Default confidence for voice match
                        else:
                            confidence = 85 if match_result else 30
                        
                        results['voice'] = {
                            'confidence': confidence,
                            'match': bool(match_result),
                            'status': 'authentic' if confidence >= 70 else 'suspicious'
                        }
                    except Exception as e:
                        results['voice'] = {'error': str(e), 'status': 'error'}
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)