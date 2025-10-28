## 🧩 FinanceAI — Intelligent Fraud & Risk Scoring for Financial Docs

### 🚀 Overview
FinanceAI verifies speaker identity, extracts text from financial documents, and computes a fraud/risk score by combining OCR, LLM analysis, and NLP signals. Designed for rapid triage of claims, invoices, and KYC artifacts.

### 💡 Inspiration
Manual fraud checks are slow and error-prone. FinanceAI accelerates trust decisions by blending voice verification with document risk analysis to flag suspicious submissions in seconds.

### ⚙️ Tech Stack
- **Python**: core runtime
- **EasyOCR**: document text extraction
- **Google Gemini (2.5 Flash)**: image + text risk analysis via JSON output
- **HuggingFace Transformers**: FinBERT sentiment, NER, zero-shot classification
- **Sentence-Transformers**: semantic consistency
- **SpeechBrain (ECAPA-TDNN)**: speaker embeddings for voice match
- **Librosa, noisereduce, SoundFile**: audio preprocessing
- **dotenv, requests, PIL**: utilities

### 🧠 Features
- **Speaker Verification**: Confirms if two voice samples match (ECAPA embeddings + cosine similarity)
- **OCR + Vision-Language Risking**: Extracts text and queries Gemini to return `{ summary, risk_level, explanation }`
- **Combined NLP Fraud Scoring**: Sentiment, NER, semantic consistency, and zero-shot fraud vs legal classification
- **Ensemble Decision**: Merges image risk and text risk into a single final score
- **CLI-First Workflow**: Run end-to-end checks via simple commands

### 🧰 Installation / Setup
Prereqs: Python 3.9–3.11, ffmpeg (recommended for audio), internet access.

1) Clone and create a virtual environment
```bash
git clone <your-repo-url>
cd FinanceAi
python -m venv .venv
./.venv/Scripts/activate  # Windows
```

2) Install dependencies
```bash
pip install --upgrade pip
pip install easyocr pillow python-dotenv requests sentence-transformers transformers torch soundfile librosa noisereduce speechbrain
```

3) Set environment variables
Create a `.env` file in project root:
```bash
echo GEMINI_API_KEY=YOUR_API_KEY_HERE > .env
```

### 🧪 How to Use
- **A) End-to-end pipeline (voice + image + text)**
```bash
python backend.py ayush.wav kshitijphone.wav sample2.png "Claim states minor damages but asks large payout"
```
Outputs voice match, image risk from Gemini, text fraud score, and an ensemble decision.

- **B) OCR + Gemini image risk (reference flow in main.py)**
Update `image_path` inside `main.py` or adjust as needed, then:
```bash
python main.py
```
Saves OCR text to `ocr_output.txt` and prints the Gemini JSON (summary, risk_level, explanation).

- **C) Text-only fraud analysis**
```bash
python combined_nlp_fraud_detector_fileinput_v2.py --text "Policyholder reports theft without police report; amounts inconsistent."

# Or analyze from file
python combined_nlp_fraud_detector_fileinput_v2.py --file path/to/claim.txt
```

- **D) Voice verification standalone**
```bash
python voice.py ayush.wav kshitijphone.wav
```

### 📈 Future Scope / Improvements
- Web dashboard with case history, audit logs, and explainability cards
- Fine-tuned fraud classifier on domain data (beyond zero-shot)
- Multi-language OCR and locale-aware checks
- Structured document parsing (key-value extraction, template matching)
- Confidence calibration and human-in-the-loop review tools


### 🏆 Acknowledgements / Hackathon
- Thanks to open-source contributors of EasyOCR, SpeechBrain, HuggingFace, and Sentence-Transformers.

---
Quick demo checklist for judges:
- Voice samples ready (WAV), one genuine and one comparison
- A sample financial document image (invoice/claim)
- GEMINI_API_KEY set in `.env`
- Run the end-to-end command under “How to Use (A)” and show the final ensemble decision