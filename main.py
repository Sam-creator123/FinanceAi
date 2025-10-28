# import easyocr
# from PIL import Image

# # Install: pip install easyocr
# reader = easyocr.Reader(['en'], gpu=False)  # Set gpu=True if you have CUDA
# image_path = "sample2.png"

# # Read text from image
# results = reader.readtext(image_path)

# # Print all detected text
# print("Detected text:")
# for detection in results:
#     bbox, text, confidence = detection
#     print(f"Text: {text}, Confidence: {confidence:.2f}")

# # Get all text as a single string
# full_text = '\n'.join([detection[1] for detection in results])
# print("\nFull recognized text:")
# print(full_text)

# import easyocr
# from PIL import Image

# # Initialize EasyOCR reader
# reader = easyocr.Reader(['en'], gpu=False)  # Set gpu=True if you have CUDA
# image_path = "sample2.png"

# # Read text from image
# results = reader.readtext(image_path)

# # Print all detected text
# print("Detected text:")
# for detection in results:
#     bbox, text, confidence = detection
#     print(f"Text: {text}, Confidence: {confidence:.2f}")

# # Combine all detected text into one string
# full_text = '\n'.join([detection[1] for detection in results])

# # Print the final recognized text
# print("\nFull recognized text:")
# print(full_text)

# # Save the recognized text to a file
# output_file = "ocr_output.txt"
# with open(output_file, "w", encoding="utf-8") as f:
#     f.write(full_text)

# print(f"\n✅ OCR output saved to '{output_file}'")

import easyocr
from PIL import Image
import requests
import json
import base64
import os
from dotenv import load_dotenv

# --------------------------------------------------------------------
# Step 0: Load Gemini API key securely
# --------------------------------------------------------------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ Gemini API key not found. Please set GEMINI_API_KEY in .env file or environment.")

# --------------------------------------------------------------------
# Step 1: OCR extraction using EasyOCR
# --------------------------------------------------------------------
reader = easyocr.Reader(['en'], gpu=False)
image_path = "fab2lab.jpg" 
results = reader.readtext(image_path)

# Combine the OCR text
full_text = "\n".join([detection[1] for detection in results])

# Save OCR text to file
output_txt = "ocr_output.txt"
with open(output_txt, "w", encoding="utf-8") as f:
    f.write(full_text)

print(f"✅ OCR completed. Extracted text saved to '{output_txt}'.")

# --------------------------------------------------------------------
# Step 2: Convert image to Base64 for Gemini API
# --------------------------------------------------------------------
with open(image_path, "rb") as img_file:
    image_base64 = base64.b64encode(img_file.read()).decode("utf-8")

# --------------------------------------------------------------------
# Step 3: Define prompt for risk analysis
# --------------------------------------------------------------------
prompt = (
    "You are an AI risk assessment assistant for financial institutions. "
    "You will receive an image of a financial document and its OCR text. "
    "Analyze both and determine the potential fraud or compliance risk score as a number between 0 and 1: "
     "0 means no risk, 1 means high risk.\n\n"
    "Base this on red flags like altered signatures, mismatched amounts, fake logos, missing authorization, etc.\n\n"
    "Provide the output strictly in JSON format as follows:\n\n"
    "{\n"
    '  "summary": "short one-sentence summary",\n'
    '  "risk_level": "A number between 0 and 1",\n'
    '  "explanation": "2-3 sentence explanation for the decision"\n'
    "}\n\n"
    f"OCR Extracted Text:\n{full_text}"
)

# --------------------------------------------------------------------
# Step 4: Prepare Gemini API request (latest endpoint + model)
# --------------------------------------------------------------------
endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

headers = {
    "Content-Type": "application/json",
    "x-goog-api-key": api_key
}

body = {
    "contents": [
        {
            "role": "user",
            "parts": [
                {"text": prompt},
                {
                    "inline_data": {
                        "mime_type": "image/png",
                        "data": image_base64
                    }
                }
            ]
        }
    ]
}

# --------------------------------------------------------------------
# Step 5: Make request to Gemini API
# --------------------------------------------------------------------
response = requests.post(endpoint, headers=headers, data=json.dumps(body))

if response.status_code != 200:
    print(f"❌ ERROR: {response.status_code}")
    print(response.text)
    exit(1)

resp_json = response.json()
generated = resp_json.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")

print("\n=== Gemini Risk Assessment Output ===")
print(generated)

# --------------------------------------------------------------------
# Step 6: Parse and save structured JSON output
# --------------------------------------------------------------------
try:
    risk_data = json.loads(generated)
    print("\n✅ Parsed Response:")
    print(f"Summary: {risk_data.get('summary')}")
    print(f"Risk Level: {risk_data.get('risk_level')}")
    print(f"Explanation: {risk_data.get('explanation')}")

    # Save to file for audit logging
    with open("risk_assessment.json", "w", encoding="utf-8") as f:
        json.dump(risk_data, f, indent=4)

    print("\n💾 Saved structured output to 'risk_a  ssessment.json'.")

except json.JSONDecodeError:
    print("\n⚠️ Model did not return valid JSON. Here’s the raw output instead:")
    print(generated)    