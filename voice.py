import torch
import noisereduce as nr
import numpy as np
import soundfile as sf
import librosa
import sys
from speechbrain.pretrained import EncoderClassifier

# -----------------------------------------------------
# MODEL: Robust speaker embedding (ECAPA-TDNN)
# -----------------------------------------------------
model = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb")

# -----------------------------------------------------
# Step 1: Load + clean audio
# -----------------------------------------------------
def load_and_clean(path):
    # Load WAV safely using soundfile (no torchaudio dependency)
    wav, sr = sf.read(path)
    if len(wav.shape) > 1:
        wav = wav.mean(axis=1)  # Convert to mono

    # Resample to 16 kHz
    if sr != 16000:
        wav = librosa.resample(wav, orig_sr=sr, target_sr=16000)
        sr = 16000

    # Denoise audio
    wav = nr.reduce_noise(y=wav, sr=sr)

    # --- Simple VAD: Remove silence based on RMS energy ---
    energy = librosa.feature.rms(y=wav)[0]
    threshold = 0.5 * np.mean(energy)
    frames = np.nonzero(energy > threshold)[0]
    if len(frames) > 0:
        t = librosa.frames_to_samples(frames, hop_length=512)
        start, end = max(0, t[0]), min(len(wav), t[-1])
        wav = wav[start:end]

    # Normalize loudness
    wav = wav / (np.max(np.abs(wav)) + 1e-6)

    # Convert to tensor
    return torch.tensor(wav).unsqueeze(0), sr

# -----------------------------------------------------
# Step 2: Extract embedding
# -----------------------------------------------------
def get_embedding(path):
    speech, sr = load_and_clean(path)
    emb = model.encode_batch(speech)
    emb = torch.nn.functional.normalize(emb, dim=-1)  # L2 normalize
    return emb.squeeze(0)

# -----------------------------------------------------
# Step 3: Cosine similarity
# -----------------------------------------------------
def cosine_sim(a, b):
    return torch.nn.functional.cosine_similarity(a, b).item()

# -----------------------------------------------------
# Step 4: Main check
# -----------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python voice.py <file1.wav> <file2.wav>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    emb1 = get_embedding(file1)
    emb2 = get_embedding(file2)

    sim = cosine_sim(emb1, emb2)
    print(f"\n🔊 Cosine similarity between '{file1}' and '{file2}': {sim:.4f}")

    # Interpret similarity score
    if sim > 0.55:
        print("✅ Likely the SAME speaker")
    elif sim > 0.5:
        print("🤔 Possibly same speaker (uncertain)")
    else:
        print("❌ Different speaker")


