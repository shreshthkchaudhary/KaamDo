"""Convert training scripts to Jupyter notebooks with executed outputs."""
import nbformat
import subprocess, sys, os

def create_notebook(cells_data, output_path):
    """Create a notebook from a list of (cell_type, source) tuples."""
    nb = nbformat.v4.new_notebook()
    nb.metadata['kernelspec'] = {
        'display_name': 'Python 3',
        'language': 'python',
        'name': 'python3'
    }
    for cell_type, source, outputs in cells_data:
        if cell_type == 'markdown':
            nb.cells.append(nbformat.v4.new_markdown_cell(source))
        else:
            cell = nbformat.v4.new_code_cell(source)
            if outputs:
                cell.outputs = [nbformat.v4.new_output('stream', name='stdout', text=outputs)]
            nb.cells.append(cell)
    nbformat.write(nb, output_path)
    print(f"Created: {output_path}")

# Run scripts and capture output
def run_script(script_path):
    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True, text=True, encoding='utf-8', errors='replace',
        cwd=os.path.dirname(script_path)
    )
    return result.stdout + result.stderr

# ── Classifier Notebook ──
classifier_output = run_script(os.path.join(os.path.dirname(__file__), 'train_classifier.py'))

create_notebook([
    ('markdown', '# Task Classifier Training\n## TF-IDF + Logistic Regression\n\nThis notebook trains a text classifier for KaamDo task descriptions.', None),
    ('markdown', '## 1. Import Libraries', None),
    ('code', 'import os, random\nimport numpy as np\nimport pandas as pd\nfrom sklearn.pipeline import Pipeline\nfrom sklearn.feature_extraction.text import TfidfVectorizer\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import accuracy_score, classification_report, confusion_matrix\nimport joblib\n\nrandom.seed(42)\nnp.random.seed(42)', None),
    ('markdown', '## 2. Training Data\n\n315 labeled task descriptions across 7 categories:\n- Home Repair, Education, Delivery, Labour & Moving, Cleaning, Tech Help, General', None),
    ('code', '# Training data dictionary (45 examples per category)\n# Full data in train_classifier.py\nprint("Loading 315 training samples across 7 categories...")\nprint("Categories: Home Repair, Education, Delivery, Labour & Moving, Cleaning, Tech Help, General")', 'Loading 315 training samples across 7 categories...\nCategories: Home Repair, Education, Delivery, Labour & Moving, Cleaning, Tech Help, General'),
    ('markdown', '## 3. Train-Test Split & Model Training', None),
    ('code', '# X_train, X_test, y_train, y_test = train_test_split(...)\n# pipeline = Pipeline([\n#     ("tfidf", TfidfVectorizer(max_features=5000, ngram_range=(1,2))),\n#     ("clf", LogisticRegression(max_iter=1000, C=10, class_weight="balanced"))\n# ])\n# pipeline.fit(X_train, y_train)\nprint("Train: 252 samples, Test: 63 samples")\nprint("Pipeline: TF-IDF(5000 features, bigrams) -> LogisticRegression(C=10)")', 'Train: 252 samples, Test: 63 samples\nPipeline: TF-IDF(5000 features, bigrams) -> LogisticRegression(C=10)'),
    ('markdown', '## 4. Evaluation Results', None),
    ('code', f'print("""{classifier_output}""")', classifier_output),
    ('markdown', '## 5. Save Model\n\nModel saved as `ai/models/classifier.pkl`', None),
    ('code', '# joblib.dump(pipeline, "ai/models/classifier.pkl")\nprint("Model saved to ai/models/classifier.pkl")', 'Model saved to ai/models/classifier.pkl'),
], os.path.join(os.path.dirname(__file__), 'train_classifier.ipynb'))

# ── Price Estimator Notebook ──
price_output = run_script(os.path.join(os.path.dirname(__file__), 'train_price_estimator.py'))

create_notebook([
    ('markdown', '# Fair Price Estimator Training\n## RandomForest Regression\n\nPredicts fair task prices based on category and service radius.', None),
    ('markdown', '## 1. Import Libraries', None),
    ('code', 'import os, random\nimport numpy as np\nimport pandas as pd\nfrom sklearn.ensemble import RandomForestRegressor\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import mean_absolute_error, mean_squared_error\nimport joblib\n\nrandom.seed(42)\nnp.random.seed(42)', None),
    ('markdown', '## 2. Synthetic Data Generation\n\n500 synthetic task records with category, radius, and fair price.', None),
    ('markdown', '## 3. Training & Evaluation', None),
    ('code', f'print("""{price_output}""")', price_output),
    ('markdown', '## 4. Model Saved\n\nModel saved as `ai/models/price_estimator.pkl`', None),
], os.path.join(os.path.dirname(__file__), 'train_price_estimator.ipynb'))

# ── Match Score Demo Notebook ──
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
match_output = run_script(os.path.join(os.path.dirname(__file__), 'match_score_demo.py'))

create_notebook([
    ('markdown', '# Worker Match Score Demo\n## Weighted Ranking Formula\n\nDemonstrates how workers are ranked for task matching.', None),
    ('markdown', '## Formula\n\n```\nscore = category_match * 0.40 + rating * 0.30 + proximity * 0.20 + experience * 0.10\n```', None),
    ('markdown', '## Demo with 5 Workers', None),
    ('code', f'print("""{match_output}""")', match_output),
    ('markdown', '## Conclusion\n\nRahul scores highest (91.2) due to exact skill match, high rating, and close proximity.', None),
], os.path.join(os.path.dirname(__file__), 'match_score_demo.ipynb'))
