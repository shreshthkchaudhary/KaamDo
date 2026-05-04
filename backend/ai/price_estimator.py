"""Fair Price Estimator — RandomForest regression model.

Predicts a fair price range for a task based on category and radius.
"""

import os
import joblib
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'price_estimator.pkl')

# Category encoding map (must match the one used during training)
CATEGORY_MAP = {
    'Home Repair': 0,
    'Education': 1,
    'Delivery': 2,
    'Labour & Moving': 3,
    'Cleaning': 4,
    'Tech Help': 5,
    'General': 6,
}

# Fallback average prices per category (₹)
FALLBACK_PRICES = {
    'Home Repair': 450,
    'Education': 350,
    'Delivery': 200,
    'Labour & Moving': 600,
    'Cleaning': 300,
    'Tech Help': 500,
    'General': 400,
}

_model = None


def _load_model():
    global _model
    if _model is None:
        if os.path.exists(MODEL_PATH):
            _model = joblib.load(MODEL_PATH)
        else:
            _model = None
    return _model


def estimate_price(category: str, radius_km: float = 5.0) -> dict:
    """Return min and max estimated price for a task.

    Falls back to hard-coded averages if model isn't trained yet.
    """
    model = _load_model()

    if model is not None:
        cat_encoded = CATEGORY_MAP.get(category, 6)
        features = np.array([[cat_encoded, radius_km]])
        predicted = float(model.predict(features)[0])
    else:
        # Fallback heuristic
        base = FALLBACK_PRICES.get(category, 400)
        # Larger radius → slightly higher price (travel cost)
        predicted = base + (radius_km - 5) * 10

    min_price = max(50, round(predicted * 0.85))
    max_price = round(predicted * 1.15)

    return {
        'min_price': min_price,
        'max_price': max_price,
        'estimated': round(predicted)
    }
