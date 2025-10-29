from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Dict, Optional
import os
from werkzeug.utils import secure_filename
# from backend import analyze_image
# Temporary mock functions for testing
def analyze_image(path):
    return 0.2  # 20% risk score

def analyze_text(content):
    return 0.15  # 15% fraud score

def analyze_voice(path):
    return True  # voice match

app = FastAPI(
    title="InsureGuard AI",
    description="AI-Powered Insurance Fraud Detection",
    version="1.0.0"
)

# Static files and templates configuration
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

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

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Serve the main application page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/favicon.ico')
async def favicon():
    """Serve favicon"""
    return FileResponse('static/favicon.ico')

@app.post('/analyze')
async def analyze(
    image: Optional[UploadFile] = File(None),
    voice: Optional[UploadFile] = File(None),
    text: Optional[UploadFile] = File(None)
):
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
        if image and image.filename:
            if not allowed_file(image.filename, 'image'):
                results['image'] = {'error': 'Invalid file type for image'}
            else:
                filename = secure_filename(image.filename)
                img_path = os.path.join(UPLOAD_FOLDER, filename)
                content = await image.read()
                with open(img_path, "wb") as buffer:
                    buffer.write(content)
                
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
        if text and text.filename:
            if not allowed_file(text.filename, 'text'):
                results['text'] = {'error': 'Invalid file type for text'}
            else:
                content = await text.read()
                text_content = content.decode('utf-8')
                
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
        if voice and voice.filename:
            if not allowed_file(voice.filename, 'voice'):
                results['voice'] = {'error': 'Invalid file type for voice'}
            else:
                filename = secure_filename(voice.filename)
                voice_path = os.path.join(UPLOAD_FOLDER, filename)
                content = await voice.read()
                with open(voice_path, "wb") as buffer:
                    buffer.write(content)
                
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
        raise HTTPException(status_code=500, detail=str(e))
    
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)