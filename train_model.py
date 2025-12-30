import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os

# Ensure model directory exists
os.makedirs("model", exist_ok=True)

# Load dataset
data = pd.read_csv("data/fatigue_data.csv")

# Features and target
X = data.drop("fatigue_level", axis=1)
y = data["fatigue_level"]

# Encode labels
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# Train model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(
    y_test, y_pred, target_names=encoder.classes_
)
conf_matrix = confusion_matrix(y_test, y_pred)

# Save model & encoder
joblib.dump(model, "model/fatigue_model.pkl")
joblib.dump(encoder, "model/label_encoder.pkl")

# Save evaluation results
with open("model/evaluation_report.txt", "w") as f:
    f.write(f"Accuracy: {accuracy:.2f}\n\n")
    f.write("Classification Report:\n")
    f.write(report)
    f.write("\nConfusion Matrix:\n")
    f.write(str(conf_matrix))
    
    
# Save feature importance
feature_importance = pd.DataFrame({
    "feature": X.columns,
    "importance": model.feature_importances_
})

feature_importance.to_csv("model/feature_importance.csv", index=False)


# Print results
print("✅ Model trained successfully")
print(f"📊 Accuracy: {accuracy:.2f}")
print("\n📄 Classification Report:")
print(report)
print("🔢 Confusion Matrix:")
print(conf_matrix)


