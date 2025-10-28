# 🔌 API INTEGRATION GUIDE

## Connecting Your AI Model to the Frontend

This guide explains how to replace the mock analysis with your actual AI fraud detection model.

---

## 📋 Overview

Currently, the app uses **simulated analysis** (mock data). To connect your real AI model:

1. Deploy your AI model as a REST API
2. Update the configuration
3. Modify the API call function
4. Handle responses correctly

---

## 🏗️ Architecture

### Current Flow (Mock)
```
User Uploads Files → Frontend Validation → Mock Analysis → Display Results
```

### Production Flow (Real API)
```
User Uploads Files → Frontend Validation → Send to API → 
Your AI Model Processes → Receive Results → Display Results
```

---

## 🚀 Step-by-Step Integration

### Step 1: Prepare Your Backend API

Your AI model should expose a REST API endpoint that accepts file uploads.

**Example Backend Endpoint:**
```
POST https://your-api.com/api/analyze-claim
```

**Expected Request Format:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: Three files (voice, image, text)

**Example using Flask (Python):**
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/analyze-claim', methods=['POST'])
def analyze_claim():
    # Get uploaded files
    voice_file = request.files.get('voice')
    image_file = request.files.get('image')
    text_file = request.files.get('text')
    
    # Your AI model processing here
    voice_result = analyze_voice(voice_file)
    image_result = analyze_image(image_file)
    text_result = analyze_text(text_file)
    
    # Return results in expected format
    return jsonify({
        'voice': voice_result,
        'image': image_result,
        'text': text_result
    })
```

### Step 2: Update Configuration

Edit `config/app-config.js`:

```javascript
const APP_CONFIG = {
    api: {
        // Your actual API URL
        baseUrl: 'https://your-api.com',
        
        endpoints: {
            submitClaim: '/api/analyze-claim',
            // Add more endpoints if needed
        },
        
        // IMPORTANT: Set to false for production
        useMockAPI: false,
    },
    
    // ... rest of config
};
```

### Step 3: Modify API Call Function

Edit `scripts/analysis-simulator.js`, specifically the `callRealAPI()` function:

```javascript
async callRealAPI(type) {
    try {
        // Prepare form data
        const formData = new FormData();
        formData.append(type, this.uploadedFiles[type]);
        
        // Add authentication if needed
        const headers = {
            // Add your auth token
            // 'Authorization': 'Bearer YOUR_TOKEN',
        };
        
        // Make API call
        const response = await fetch(
            `${APP_CONFIG.api.baseUrl}${APP_CONFIG.api.endpoints.submitClaim}`,
            {
                method: 'POST',
                headers: headers,
                body: formData,
            }
        );
        
        // Check response
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        // Parse response
        const data = await response.json();
        
        // Validate response format
        return this.validateAPIResponse(data, type);
        
    } catch (error) {
        console.error('API call failed:', error);
        
        // Decide what to do on error:
        // Option 1: Show error to user
        alert('Analysis failed. Please try again.');
        
        // Option 2: Fall back to mock data (for development)
        // return this.generateMockResult(type);
        
        // Option 3: Return error result
        return {
            type,
            confidence: 0,
            status: 'error',
            isAuthentic: false,
            indicators: ['Analysis failed - please try again'],
            timestamp: new Date().toISOString(),
        };
    }
}
```

### Step 4: Define Expected Response Format

Your API should return JSON in this format for each analyzed file:

```javascript
{
    "type": "voice",  // "voice", "image", or "text"
    "confidence": 85,  // Number between 0-100
    "status": "authentic",  // "authentic", "suspicious", or "fraudulent"
    "isAuthentic": true,  // Boolean
    "indicators": [  // Array of strings
        "Natural speech patterns detected",
        "Consistent acoustic signatures",
        "No signs of voice synthesis"
    ],
    "timestamp": "2025-10-28T12:00:00Z"  // ISO format
}
```

### Step 5: Add Response Validation

Add this function to `scripts/analysis-simulator.js`:

```javascript
validateAPIResponse(data, type) {
    // Ensure required fields exist
    if (!data || typeof data !== 'object') {
        throw new Error('Invalid API response format');
    }
    
    // Set defaults for missing fields
    return {
        type: data.type || type,
        confidence: Math.min(100, Math.max(0, data.confidence || 0)),
        status: ['authentic', 'suspicious', 'fraudulent'].includes(data.status) 
            ? data.status 
            : 'fraudulent',
        isAuthentic: data.isAuthentic !== undefined 
            ? data.isAuthentic 
            : false,
        indicators: Array.isArray(data.indicators) 
            ? data.indicators 
            : ['No analysis details available'],
        timestamp: data.timestamp || new Date().toISOString(),
    };
}
```

---

## 🔐 Authentication

### Adding API Keys

**Option 1: In Headers**
```javascript
const headers = {
    'Authorization': 'Bearer YOUR_API_KEY',
    'X-API-Key': 'YOUR_API_KEY',
};
```

**Option 2: As Query Parameter**
```javascript
const url = `${baseUrl}${endpoint}?api_key=YOUR_API_KEY`;
```

**⚠️ Security Warning:** Never expose API keys in frontend code for production!

### Better Approach for Production

1. **Use a Backend Proxy:**
   - Frontend → Your Backend → AI Model
   - Your backend handles authentication securely

2. **Use User Authentication:**
   - User logs in → Gets session token
   - Token is sent with requests
   - Backend validates token

---

## 🔄 Alternative Integration Methods

### Method 1: Sequential Analysis (Current)

The frontend calls your API three times (once for each file type):
- Analyzes voice → If OK, analyzes image → If OK, analyzes text

**Pros:** Can stop early if fraud detected
**Cons:** Slower overall time

### Method 2: Parallel Analysis

Call API once with all three files, process simultaneously:

```javascript
async startAnalysis(files) {
    this.uploadedFiles = files;
    
    // Prepare all files
    const formData = new FormData();
    formData.append('voice', files.voice);
    formData.append('image', files.image);
    formData.append('text', files.text);
    
    // Single API call
    const response = await fetch(endpoint, {
        method: 'POST',
        body: formData
    });
    
    const results = await response.json();
    
    // Update UI with all results
    this.results = results;
    this.showResults();
}
```

**Pros:** Faster overall time
**Cons:** Processes everything even if early fraud detected

### Method 3: WebSocket for Real-time Updates

For longer processing times, use WebSocket to stream updates:

```javascript
const ws = new WebSocket('wss://your-api.com/analyze');

ws.onmessage = (event) => {
    const update = JSON.parse(event.data);
    
    if (update.stage === 'voice') {
        this.updateVoiceProgress(update.progress);
    }
    // ... handle other stages
};
```

---

## 🧪 Testing Your Integration

### Test Checklist

- [ ] API endpoint is accessible from frontend
- [ ] CORS is properly configured on backend
- [ ] File upload size limits match on both ends
- [ ] Authentication works correctly
- [ ] Response format matches expected structure
- [ ] Error handling works (try invalid files)
- [ ] Loading indicators show during processing
- [ ] Results display correctly
- [ ] Download report works

### Test with Mock First

Keep `useMockAPI: true` while developing, then switch to `false` when ready.

---

## 🐛 Common Issues & Solutions

### Issue: CORS Error
```
Access to fetch has been blocked by CORS policy
```

**Solution:** Enable CORS on your backend:

Python (Flask):
```python
from flask_cors import CORS
CORS(app)
```

Node.js (Express):
```javascript
const cors = require('cors');
app.use(cors());
```

### Issue: File Too Large
```
Request Entity Too Large (413)
```

**Solution:** Increase upload limit on backend:

Express:
```javascript
app.use(express.json({ limit: '10mb' }));
```

### Issue: Timeout
```
Network request failed
```

**Solution:** Increase timeout:
```javascript
const controller = new AbortController();
const timeout = setTimeout(() => controller.abort(), 30000); // 30 seconds

fetch(url, { 
    signal: controller.signal,
    // ... other options
});
```

---

## 📊 Response Time Optimization

### Frontend Loading States

The app shows loading animations. Customize timing in `config/app-config.js`:

```javascript
analysis: {
    voiceAnalysisTime: 3000,  // Adjust to match your API
    imageAnalysisTime: 3500,
    textAnalysisTime: 3000,
}
```

### Show Real Progress

Update the messages array to match your API's processing stages:

```javascript
messages: {
    voice: [
        'Uploading voice sample...',
        'Running voice analysis model...',
        'Analyzing acoustic features...',
        'Detecting anomalies...',
        'Generating results...'
    ],
    // ... other types
}
```

---

## 🔧 Advanced Customization

### Add Progress Callback

Modify `callRealAPI` to support progress:

```javascript
async callRealAPI(type, progressCallback) {
    const formData = new FormData();
    formData.append(type, this.uploadedFiles[type]);
    
    const xhr = new XMLHttpRequest();
    
    // Track upload progress
    xhr.upload.addEventListener('progress', (e) => {
        if (e.lengthComputable) {
            const percentComplete = (e.loaded / e.total) * 100;
            progressCallback(percentComplete);
        }
    });
    
    // Make request
    return new Promise((resolve, reject) => {
        xhr.open('POST', url);
        xhr.onload = () => resolve(JSON.parse(xhr.response));
        xhr.onerror = () => reject(new Error('Upload failed'));
        xhr.send(formData);
    });
}
```

### Add Retry Logic

```javascript
async callRealAPIWithRetry(type, maxRetries = 3) {
    for (let i = 0; i < maxRetries; i++) {
        try {
            return await this.callRealAPI(type);
        } catch (error) {
            if (i === maxRetries - 1) throw error;
            await this.delay(1000 * (i + 1)); // Exponential backoff
        }
    }
}
```

---

## 📝 Deployment Checklist

Before deploying to production:

- [ ] Set `useMockAPI: false`
- [ ] Configure proper authentication
- [ ] Set up HTTPS for API calls
- [ ] Add error tracking (e.g., Sentry)
- [ ] Add analytics (e.g., Google Analytics)
- [ ] Test with real files at scale
- [ ] Set up proper logging
- [ ] Configure rate limiting
- [ ] Add input sanitization
- [ ] Implement proper CORS
- [ ] Add request validation
- [ ] Set up monitoring

---

## 🎯 Example: Complete Integration

Here's a complete example using a Python backend:

**Backend (Flask):**
```python
from flask import Flask, request, jsonify
from flask_cors import CORS
import your_ai_model

app = Flask(__name__)
CORS(app)

@app.route('/api/analyze-claim', methods=['POST'])
def analyze():
    voice = request.files['voice']
    image = request.files['image']
    text = request.files['text']
    
    # Your AI model
    results = your_ai_model.analyze_all(voice, image, text)
    
    return jsonify(results)
```

**Frontend (config):**
```javascript
const APP_CONFIG = {
    api: {
        baseUrl: 'https://your-api.com',
        endpoints: {
            submitClaim: '/api/analyze-claim',
        },
        useMockAPI: false,
    },
};
```

That's it! Your frontend will now use your real AI model. 🎉

---

## 📚 Additional Resources

- MDN Web Docs: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
- REST API Best Practices: https://restfulapi.net/
- CORS Documentation: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS

**Happy Integrating! 🚀**
