import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report


DATASET_PATH = "data/raw/logs.csv"
MODEL_PATH = "models/severity_classifier.joblib"


# --------------------------------------------------
# 1. Load dataset
# --------------------------------------------------

df = pd.read_csv(DATASET_PATH)

print(f"Loaded {len(df)} log records")


# --------------------------------------------------
# 2. Prepare input and labels
# --------------------------------------------------

X = df["message"]
y = df["label"]


# --------------------------------------------------
# 3. Split dataset
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print(f"Training records: {len(X_train)}")
print(f"Testing records: {len(X_test)}")


# --------------------------------------------------
# 4. Create ML pipeline
# --------------------------------------------------

model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            min_df=1
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000
        )
    )
])


# --------------------------------------------------
# 5. Train model
# --------------------------------------------------

print("\nTraining model...")

model.fit(X_train, y_train)

print("Training completed.")


# --------------------------------------------------
# 6. Evaluate model
# --------------------------------------------------

predictions = model.predict(X_test)

print("\nModel Evaluation:")
print("-----------------")

print(
    classification_report(
        y_test,
        predictions
    )
)


# --------------------------------------------------
# 7. Save model
# --------------------------------------------------

joblib.dump(model, MODEL_PATH)

print(f"\nModel saved to: {MODEL_PATH}")