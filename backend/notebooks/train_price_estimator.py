"""
Train Fair Price Estimator — RandomForest Regression
====================================================
Run: python train_price_estimator.py
"""

import os, random
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib

random.seed(42)
np.random.seed(42)

PRICE_RANGES = {
    0: (200, 800), 1: (150, 600), 2: (100, 400),
    3: (300, 1000), 4: (200, 600), 5: (300, 900), 6: (150, 700),
}
CATEGORY_NAMES = {
    0: 'Home Repair', 1: 'Education', 2: 'Delivery',
    3: 'Labour & Moving', 4: 'Cleaning', 5: 'Tech Help', 6: 'General',
}

records = []
for _ in range(500):
    cat = random.randint(0, 6)
    radius = round(random.uniform(1, 15), 1)
    base_min, base_max = PRICE_RANGES[cat]
    base_price = random.uniform(base_min, base_max)
    radius_factor = radius * random.uniform(5, 15)
    noise = random.gauss(0, 30)
    fair_price = max(50, round(base_price + radius_factor + noise))
    records.append({'category': cat, 'radius_km': radius, 'fair_price': fair_price})

df = pd.DataFrame(records)
print(f"Total samples: {len(df)}")
print(f"\nCategory distribution:\n{df['category'].value_counts().sort_index()}")
print(f"\nPrice stats:\n{df['fair_price'].describe()}")

X = df[['category', 'radius_km']]
y = df['fair_price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"\n{'='*60}")
print(f"MAE: Rs.{mae:.2f}  |  RMSE: Rs.{rmse:.2f}")
print(f"{'='*60}")
print(f"\nFeature Importances:")
for name, imp in zip(X.columns, model.feature_importances_):
    print(f"  {name}: {imp:.4f}")

model_dir = os.path.join(os.path.dirname(__file__), '..', 'ai', 'models')
os.makedirs(model_dir, exist_ok=True)
model_path = os.path.join(model_dir, 'price_estimator.pkl')
joblib.dump(model, model_path)
print(f"\nModel saved to: {model_path}")

print(f"\nSample Predictions:")
for cat, radius in [(0,3),(1,5),(2,2),(3,7),(4,4),(5,10),(6,5)]:
    pred = model.predict([[cat, radius]])[0]
    print(f"  {CATEGORY_NAMES[cat]} ({radius}km) -> Rs.{round(pred*0.85)}-Rs.{round(pred*1.15)}")
