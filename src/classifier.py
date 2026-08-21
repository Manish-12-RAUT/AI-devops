import joblib


MODEL_PATH = "models/severity_classifier.joblib"


# Load trained model
model = joblib.load(MODEL_PATH)


def classify_log(message: str):
    """
    Classify a log message into:
    INFO, WARNING, ERROR, or CRITICAL.
    """

    prediction = model.predict([message])[0]

    probabilities = model.predict_proba([message])[0]

    class_probabilities = dict(
    zip(model.classes_, probabilities)
)

    confidence = max(probabilities)

    return {
    "message": message,
    "severity": prediction,
    "confidence": round(float(confidence), 4),
    "probabilities": {
        label: round(float(probability), 4)
        for label, probability in class_probabilities.items()
    }
}


# --------------------------------------------------
# Test the classifier
# --------------------------------------------------

if __name__ == "__main__":

    test_logs = [
        "User successfully logged in",
        "CPU usage has reached 95%",
        "Database connection timeout",
        "Production application has crashed",
    ]

    for log in test_logs:

        result = classify_log(log)

        print("\nLog:", result["message"])
        print("Severity:", result["severity"])
        print("Confidence:", result["confidence"])