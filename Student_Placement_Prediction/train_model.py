import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# ---------------- LOAD DATA ----------------
df = pd.read_csv("data/placement_dataset.csv")

# ---------------- CLEAN DATA ----------------
df = df.drop("sl_no", axis=1)

# Fill missing salary values
df["salary"] = df["salary"].fillna(0)

# ---------------- ENCODING ----------------
cat_cols = [
    "gender",
    "ssc_b",
    "hsc_b",
    "hsc_s",
    "degree_t",
    "workex",
    "specialisation"
]

for col in cat_cols:
    df[col] = df[col].astype("category").cat.codes

# Target encoding
df["status"] = df["status"].map({"Not Placed": 0, "Placed": 1})

# ---------------- FEATURES & TARGET ----------------
X = df.drop("status", axis=1)
y = df["status"]

# ---------------- TRAIN TEST SPLIT ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------- MODEL ----------------
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# ---------------- EVALUATION ----------------
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print("Accuracy:", round(acc * 100, 2), "%")

# ---------------- SAVE MODEL ----------------
joblib.dump(model, "models/placement_model.pkl")

print("Model saved successfully 🚀")