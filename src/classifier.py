import joblib

model = joblib.load("models/severity_classifier.joblib")


def classify_log(message: str):
    label = model.predict([message])[0]
    probabilities = model.predict_proba([message])[0]

    confidence = max(probabilities)

    return {
        "severity": label,
        "confidence": round(float(confidence), 4)
    }