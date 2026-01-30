# Train a text classifier that predicts `relation_type` from `text`.

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


def main() -> None:
    # Paths
    project_root = Path(__file__).resolve().parents[1]
    data_path = project_root / "data" / "training_data.csv"
    model_dir = project_root / "model"
    model_path = model_dir / "model.pkl"

    # 1) Load data
    df = pd.read_csv(data_path)

    # 2) Split into X (text) and y (relation_type)
    X = df["text"].astype(str).fillna("")
    y = df["relation_type"].astype(str)

    # Create a train/test split. We try to stratify (keep class proportions similar)
    # when possible, but fall back if any class is too small.
    stratify = y
    if y.value_counts().min() < 2:
        stratify = None

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=stratify,
    )

    # 3) Build model
    #
    # TF-IDF (Term Frequency–Inverse Document Frequency) converts raw text into numbers
    # by giving each word (or n-gram) a weight:
    # - higher if it appears often in a specific document (term frequency),
    # - lower if it appears in many documents (inverse document frequency),
    # so common words like "the" matter less and more distinctive terms matter more.
    #
    # Logistic Regression is a linear classifier that learns weights for these TF-IDF
    # features and outputs probabilities over classes. The predicted class is typically
    # the one with the highest probability.
    model: Pipeline = Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer()),
            ("clf", LogisticRegression(max_iter=1000, class_weight="balanced")),
        ]
    )

    # 4) Train model
    #
    # "Training" means fitting the model's parameters (the learned weights) using the
    # training data so that its predictions match the true labels as closely as possible.
    model.fit(X_train, y_train)

    # 5) Print accuracy
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {acc:.4f}  (test size: {len(y_test)})")

    # 6) Save full pipeline (vectorizer + classifier) in one file for app
    model_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)
    print(f"Saved model to: {model_path}")
    print("Model training done successfully.")


if __name__ == "__main__":
    main()

