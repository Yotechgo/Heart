# train_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import resample
import pickle

# Load dataset
df = pd.read_csv("heart.csv")

# Separate classes
df_majority = df[df.target == 0]  # Low risk
df_minority = df[df.target == 1]  # High risk

# Oversample minority class to balance dataset
df_minority_upsampled = resample(
    df_minority, 
    replace=True,
    n_samples=len(df_majority),
    random_state=42
)

# Combine balanced dataset
df_balanced = pd.concat([df_majority, df_minority_upsampled])

# Features & target
X = df_balanced.drop("target", axis=1)
y = df_balanced["target"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train model
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=10,
    random_state=42
)
model.fit(X_train, y_train)

# Save trained model
with open("heart_disease_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved as heart_disease_model.pkl")
