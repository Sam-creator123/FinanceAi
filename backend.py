import subprocess
import json
import sys
import os
from combined_nlp_fraud_detector_fileinput_v2 import CombinedNLPAnalyzer
import voice
import easyocr
import base64
import requests
from dotenv import load_dotenv

def check_voice_match(file1, file2, threshold=0.55):
    emb1 = voice.get_embedding(file1)
    emb2 = voice.get_embedding(file2)
    sim = voice.cosine_sim(emb1, emb2)
    print(f"[VOICE MATCH] Cosine similarity: {sim:.4f}")
    return sim >= threshold

'''def analyze_image(image_path):
    """Use the same logic as main.py to get Gemini risk score."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("❌ Gemini API key missing in .env")

    reader = easyocr.Reader(['en'], gpu=False)
    results = reader.readtext(image_path)
    full_text = "\n".join([d[1] for d in results])

    with open(image_path, "rb") as img_file:
        image_base64 = base64.b64encode(img_file.read()).decode("utf-8")

    prompt = (
        "You are an AI risk assessment assistant for financial documents. "
        "Return a JSON with a 'risk_level' between 0 and 1.\n\n"
        f"OCR Extracted Text:\n{full_text}"
    )

    body = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": "image/png", "data": image_base64}},
                ],
            }
        ]
    }

    endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    headers = {"Content-Type": "application/json", "x-goog-api-key": api_key}

    resp = requests.post(endpoint, headers=headers, data=json.dumps(body))
    if resp.status_code != 200:
        print(f"Gemini error: {resp.status_code}")
        return 0.0

    raw_output = resp.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
    
    try:
        data = json.loads(raw_output)
        risk_level = float(data.get("risk_level", 0))
    except Exception:
        print("⚠️ Gemini output not valid JSON. Default risk=0.0")
        risk_level = 0.0
    print(f"[IMAGE RISK] Risk level from Gemini: {risk_level}")
    return risk_level
'''
import re
import json
import requests
import base64
import easyocr
import os
from dotenv import load_dotenv

def analyze_image(image_path):
    """Perform OCR + Gemini analysis and extract a clean risk_level."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("❌ Gemini API key missing in .env")

    reader = easyocr.Reader(['en'], gpu=False)
    results = reader.readtext(image_path)
    full_text = "\n".join([d[1] for d in results])

    with open(image_path, "rb") as img_file:
        image_base64 = base64.b64encode(img_file.read()).decode("utf-8")

    prompt = (
        "You are an AI risk assessment assistant for financial documents. "
        "Return a JSON with keys 'summary', 'risk_level', and 'explanation'. "
        "Risk_level should be a number between 0 and 1.\n\n"
        f"OCR Extracted Text:\n{full_text}"
    )

    endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    headers = {"Content-Type": "application/json", "x-goog-api-key": api_key}
    body = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": "image/png", "data": image_base64}},
                ],
            }
        ]
    }

    resp = requests.post(endpoint, headers=headers, data=json.dumps(body))
    if resp.status_code != 200:
        print(f"❌ Gemini error: {resp.status_code}")
        print(resp.text)
        return 0.0

    # Extract model output
    raw_output = resp.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
    print("\n[RAW GEMINI OUTPUT]")
    print(raw_output)

    # ---- FIX: Clean Markdown-wrapped JSON ----
    # Example problematic output: ```json {...} ```
    json_pattern = r"\{[\s\S]*\}"
    match = re.search(json_pattern, raw_output)
    if match:
        json_str = match.group(0)
    else:
        json_str = raw_output.strip()

    try:
        data = json.loads(json_str)
        risk_level = float(data.get("risk_level", 0))
        print(f"[IMAGE RISK] Extracted risk level: {risk_level}")
        return risk_level
    except Exception as e:
        print(f"⚠️ Could not parse Gemini JSON: {e}")
        print("Returning default risk = 0.0")
        return 0.0

def analyze_text(text):
    analyzer = CombinedNLPAnalyzer()
    result = analyzer.analyze_text(text)
    print(f"[TEXT FRAUD SCORE] Combined NLP score: {result['combined_score']}")
    return result["combined_score"]

def main():
    if len(sys.argv) != 5:
        print("Usage: python fraud_pipeline.py <voice1.wav> <voice2.wav> <image_path> <text>")
        sys.exit(1)

    voice1, voice2, image_path, text = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

    # Step 1: Voice verification
    print("🔊 Checking if the two voices match...")
    if not check_voice_match(voice1, voice2):
        print("❌ Voice not matched.")
        return

    print("✅ Voice matched. Proceeding with image and text analysis...")

    # Step 2: Image risk analysis
    image_risk = analyze_image(image_path)

    # Step 3: Text fraud analysis
    text_risk = analyze_text(text)

    # Step 4: Ensemble risk score
    final_score = (image_risk + text_risk) / 2
    label = "RISK" if final_score > 0.6 else "NOT RISK"

    print("\n========== FINAL REPORT ==========")
    print(f"Voice match: ✅")
    print(f"Image risk score: {image_risk:.3f}")
    print(f"Text fraud score: {text_risk:.3f}")
    print(f"Final Ensemble Score: {final_score:.3f}")
    print(f"🧾 Decision: {label}")
    print("==================================")

if __name__ == "__main__":
    main()
