"""Task Classifier — TF-IDF + Logistic Regression pipeline.

Classifies task descriptions into categories:
Home Repair, Education, Delivery, Labour & Moving, Cleaning, Tech Help, General
"""

import os
import joblib

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'classifier.pkl')

# In-memory cache so we don't reload from disk on every request
_model = None


def _load_model():
    global _model
    if _model is None:
        if os.path.exists(MODEL_PATH):
            _model = joblib.load(MODEL_PATH)
        else:
            _model = None
    return _model


def classify_task(description: str) -> dict:
    """Classify a task description and return predicted category + confidence.

    Falls back to a keyword-based heuristic if the trained model isn't present.
    """
    model = _load_model()

    if model is not None:
        category = model.predict([description])[0]
        confidence = float(model.predict_proba([description]).max())
        return {
            'category': category,
            'confidence': round(confidence * 100, 1)
        }

    # ── Fallback heuristic when no .pkl is available ──
    desc = description.lower()
    categories = {
        'Home Repair': ['repair', 'fix', 'plumb', 'electric', 'wire', 'leak',
                        'tap', 'fan', 'pipe', 'paint', 'door', 'window',
                        'carpenter', 'wall'],
        'Education': ['tutor', 'teach', 'learn', 'math', 'science', 'exam',
                      'homework', 'class', 'study', 'school', 'college',
                      'assignment', 'coach', 'lesson'],
        'Delivery': ['deliver', 'pickup', 'courier', 'parcel', 'package',
                     'send', 'drop', 'transport', 'shipping', 'mail'],
        'Labour & Moving': ['move', 'shift', 'lift', 'furniture', 'heavy',
                            'carry', 'load', 'unload', 'packing', 'labour',
                            'labor', 'relocat'],
        'Cleaning': ['clean', 'wash', 'sweep', 'mop', 'dust', 'laundry',
                     'iron', 'scrub', 'vacuum', 'tidy', 'sanitiz'],
        'Tech Help': ['computer', 'laptop', 'phone', 'software', 'install',
                      'wifi', 'internet', 'printer', 'format', 'virus',
                      'app', 'website', 'code', 'program', 'tech'],
    }

    best_cat = 'General'
    best_score = 0
    for cat, keywords in categories.items():
        score = sum(1 for kw in keywords if kw in desc)
        if score > best_score:
            best_score = score
            best_cat = cat

    confidence = min(40 + best_score * 15, 95) if best_score > 0 else 30
    return {'category': best_cat, 'confidence': float(confidence)}
