"""
Combined NLP Analysis Pipeline (Insurance Fraud Detection v2)
-------------------------------------------------------------
- Accepts .txt file (--file) or direct text (--text)
- Performs Sentiment, Entity Recognition, Semantic, and Fraud/Legal Classification
- Uses contextual zero-shot classification between only 'fraud' and 'legal'
"""

import argparse
import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from sentence_transformers import SentenceTransformer, util
import numpy as np
import warnings
from typing import List, Dict

warnings.filterwarnings("ignore")

class CombinedNLPAnalyzer:
    def __init__(self,
                 sentiment_weight=0.35,
                 entity_weight=0.25,
                 semantic_weight=0.20,
                 fraud_weight=0.20,
                 finbert_model="yiyanghkust/finbert-tone",
                 ner_model="dslim/bert-base-NER",
                 zero_shot_model="facebook/bart-large-mnli",
                 sentence_transformer="sentence-transformers/all-mpnet-base-v2",
                 fraud_labels=None):
        """
        Initialize the combined NLP analyzer with models and weights.
        """
        total = sentiment_weight + entity_weight + semantic_weight + fraud_weight
        if not np.isclose(total, 1.0):
            raise ValueError("Weights must sum to 1.0")

        self.weights = dict(
            sentiment=sentiment_weight,
            entity=entity_weight,
            semantic=semantic_weight,
            fraud=fraud_weight
        )

        # Only two labels now: fraud and legal (phrased for better zero-shot performance)
        self.fraud_labels = fraud_labels or [
            "fraudulent insurance claim",
            "legitimate insurance claim"
        ]

        print("Loading models... this may take a few minutes.")
        self.sentiment_tokenizer = AutoTokenizer.from_pretrained(finbert_model)
        self.sentiment_model = AutoModelForSequenceClassification.from_pretrained(finbert_model)
        self.ner_pipeline = pipeline("ner", model=ner_model, aggregation_strategy="simple")
        self.semantic_model = SentenceTransformer(sentence_transformer)
        self.zero_shot = pipeline("zero-shot-classification", model=zero_shot_model)
        print("✅ All models loaded successfully!\n")

    # ---------- SENTIMENT ----------
    def analyze_sentiment(self, text: str):
        inputs = self.sentiment_tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            out = self.sentiment_model(**inputs)
            probs = torch.nn.functional.softmax(out.logits, dim=-1)[0].tolist()
        labels = ["neutral", "positive", "negative"]
        d = dict(zip(labels, probs))
        dom = max(d, key=d.get)
        conf = d[dom]
        return {
            "scores": d,
            "dominant": dom,
            "confidence": conf,
            "weighted_score": conf * self.weights["sentiment"]
        }

    # ---------- ENTITY RECOGNITION ----------
    def extract_entities(self, text: str):
        ents = self.ner_pipeline(text)
        ent_dict = {}
        for e in ents:
            ent_dict.setdefault(e["entity_group"], []).append({"text": e["word"], "score": e["score"]})
        avg_conf = np.mean([e["score"] for e in ents]) if ents else 0
        return {
            "entities": ent_dict,
            "count": len(ents),
            "avg_confidence": float(avg_conf),
            "weighted_score": float(avg_conf) * self.weights["entity"]
        }

    # ---------- SEMANTIC ANALYSIS ----------
    def analyze_semantic(self, texts: List[str]):
        if len(texts) < 2:
            return {"consistency_score": 1.0,
                    "weighted_score": 1.0 * self.weights["semantic"]}
        emb = self.semantic_model.encode(texts, convert_to_tensor=True)
        sims = util.cos_sim(emb, emb).cpu().numpy()
        mask = ~np.eye(len(texts), dtype=bool)
        avg = float(sims[mask].mean())
        return {"consistency_score": avg,
                "weighted_score": avg * self.weights["semantic"]}

    # ---------- FRAUD CLASSIFICATION ----------
    def analyze_fraud(self, text: str):
        # Add contextual prefix for better understanding
        contextual_text = (
            "This text is an insurance claim description. "
            "Determine if it is fraudulent or legitimate:\n" + text
        )

        res = self.zero_shot(contextual_text, candidate_labels=self.fraud_labels)
        labels, scores = res["labels"], res["scores"]
        d = dict(zip(labels, scores))

        # Extract probabilities for our two labels
        fraud_p = d.get("fraudulent insurance claim", 0)
        legal_p = d.get("legitimate insurance claim", 0)

        # Decide final classification
        if fraud_p >= legal_p:
            lab, conf = "fraud", fraud_p
        else:
            lab, conf = "legal", legal_p

        return {
            "label_scores": d,
            "chosen_label": lab,
            "classification_confidence": float(conf),
            "weighted_score": float(conf) * self.weights["fraud"]
        }

    # ---------- COMPLETE TEXT ANALYSIS ----------
    def analyze_text(self, text: str):
        s = self.analyze_sentiment(text)
        e = self.extract_entities(text)
        sem = {"consistency_score": 1.0, "weighted_score": 1.0 * self.weights["semantic"]}
        f = self.analyze_fraud(text)
        combined = s["weighted_score"] + e["weighted_score"] + sem["weighted_score"] + f["weighted_score"]
        return dict(
            text=text,
            sentiment=s,
            entities=e,
            semantic=sem,
            fraud_classification=f,
            combined_score=float(combined),
            weights_used=self.weights
        )

# ---------- UTILS ----------
def read_text_file(path: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def print_summary(res: Dict):
    print("\n========== RESULT SUMMARY ==========")
    print(f"Combined Score: {res['combined_score']:.4f}")
    f = res["fraud_classification"]
    print(f"Fraud/Legal Label: {f['chosen_label']} (confidence: {f['classification_confidence']:.3f})")
    s = res["sentiment"]
    print(f"Sentiment: {s['dominant']} (confidence: {s['confidence']:.3f})")
    print(f"Entities found: {res['entities']['count']}")
    print("====================================\n")

# ---------- MAIN EXECUTION ----------
def main():
    parser = argparse.ArgumentParser(description="Combined NLP Analyzer (Fraud vs Legal) with file or text input")
    parser.add_argument("--file", "-f", type=str, help="Path to a .txt file containing insurance claim text")
    parser.add_argument("--text", "-t", type=str, help="Direct text string to analyze")
    args, unknown = parser.parse_known_args()

    analyzer = CombinedNLPAnalyzer()

    if args.file:
        text = read_text_file(args.file)
        print(f"\n Loaded text from {args.file} ({len(text.split())} words). Running analysis...\n")
        res = analyzer.analyze_text(text)
        print_summary(res)
    elif args.text:
        res = analyzer.analyze_text(args.text)
        print_summary(res)
    else:
        print(" Please provide either --file <path> or --text <string> to analyze.")

if __name__ == "__main__":
    main()
