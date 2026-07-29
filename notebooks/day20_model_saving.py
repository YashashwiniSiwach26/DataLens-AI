import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# Step 1: Create Dataset


data = {
    "Hours": [1,2,3,4,5,6,7,8,9,10,11,12],
    "Attendance": [60,65,68,70,75,80,82,85,90,92,95,98],
    "Pass": [0,0,0,0,1,1,1,1,1,1,1,1]
}

df = pd.DataFrame(data)

print("Dataset")
print(df)

# Step 2: Features and Target


X = df[["Hours", "Attendance"]]
y = df["Pass"]

# Step 3: Split Dataset


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Step 4: Feature Scaling

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Step 5: Train Random Forest


model = RandomForestClassifier(random_state=42)

model.fit(X_train, y_train)

print("\nModel Trained Successfully")

# Step 6: Save Model


joblib.dump(model, "saved_models/random_forest_model.pkl")

print("Random Forest Model Saved")

# Step 7: Save Scaler


joblib.dump(scaler, "saved_models/scaler.pkl")

print("Scaler Saved")

# Step 8: Load Model


loaded_model = joblib.load(
    "saved_models/random_forest_model.pkl"
)

print("Model Loaded Successfully")

# Step 9: Load Scaler


loaded_scaler = joblib.load(
    "saved_models/scaler.pkl"
)

print("Scaler Loaded Successfully")

# Step 10: Predict New Student


new_student = [[6.5, 84]]

new_student_scaled = loaded_scaler.transform(new_student)

prediction = loaded_model.predict(new_student_scaled)

# Step 11: Display Result

if prediction[0] == 1:
    print("\nPrediction : PASS")
else:
    print("\nPrediction : FAIL")