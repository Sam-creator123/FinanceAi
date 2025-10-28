"""
run_donut_inference_local_parquet.py
------------------------------------
Runs OCR-free document understanding using Donut (naver-clova-ix/donut-base)
on a locally downloaded Sujet Finance Vision 10k parquet dataset.
"""

"""
run_donut_inference_local_parquet_fixed.py
------------------------------------------
Handles parquet datasets where images may be:
 - stored as binary bytes
 - Hugging Face Image objects
 - URLs or local paths

Runs Donut OCR-free extraction and saves results.
"""

import base64
import io
from datasets import load_dataset
from PIL import Image
from transformers import pipeline

# --- Load the local parquet dataset ---
dataset = load_dataset(
    "parquet",
    data_files=r"C:\donut\dataset\train-00000-of-00003.parquet"
)["train"]

print("✅ Dataset loaded! Columns:", dataset.column_names)

# --- Select one sample ---
sample = dataset[0]
print("Sample keys:", sample.keys())

# --- Locate the image field ---
# Usually it's under something like 'image', 'img', or a dict with {'bytes': base64_string}
image = None

for key, value in sample.items():
    if isinstance(value, dict):
        if "bytes" in value:  # e.g., {'bytes': '...base64...'}
            img_bytes = base64.b64decode(value["bytes"])
            image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
            print(f"🖼️ Loaded image from key '{key}' (base64 bytes)")
            break
    elif isinstance(value, str) and value.strip().startswith("/9j/"):  # raw base64 JPEG header
        img_bytes = base64.b64decode(value)
        image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        print(f"🖼️ Loaded image from key '{key}' (raw base64 string)")
        break

if image is None:
    raise ValueError("❌ Could not locate base64 image field. Check printed keys and sample structure.")

# --- Display image ---
image.show()

# --- Load Donut model ---
print("\n🤖 Loading Donut model...")
pipe = pipeline("image-to-text", model="naver-clova-ix/donut-base")
print("✅ Donut loaded!")

# --- Run inference ---
result = pipe(image)
print("\n📄 Donut Output:\n", result[0]["generated_text"])

