import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
data = pd.read_csv("data/fatigue_data.csv")

# Features and target
X = data.drop("fatigue_level", axis=1)
y = data["fatigue_level"]

# Encode target labels
encoder = LabelEncoder()
y = encoder.fit_transform(y)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model and encoder
joblib.dump(model, "model/fatigue_model.pkl")
joblib.dump(encoder, "model/label_encoder.pkl")

print("Model trained and saved successfully!")
