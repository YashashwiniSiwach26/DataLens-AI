from fastapi import FastAPI, UploadFile, File
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# Create FastAPI application
app = FastAPI()


# Home Endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to DataLens AI!"
    }


# About Endpoint
@app.get("/about")
def about():
    return {
        "project": "DataLens AI",
        "version": "1.0",
        "developer": "Yashashwini Siwach"
    }


# Health Check Endpoint
@app.get("/health")
def health():
    return {
        "status": "running"
    }


# Models Endpoint
@app.get("/models")
def models():
    return {
        "models": [
            "Logistic Regression",
            "Decision Tree",
            "Random Forest",
            "SVM",
            "KNN",
            "Naive Bayes"
        ]
    }
@app.post("/upload-dataset/")
def upload_dataset(file: UploadFile = File(...)):
    # Read the uploaded CSV file
    df = pd.read_csv(file.file)

    rows = int(df.shape[0])
    columns = int(df.shape[1])
    column_names = df.columns.tolist()

    missing_values = {
        col: int(val) for col, val in df.isnull().sum().items()
    }
    duplicate_rows = int(df.duplicated().sum())
    data_types = {col: str(dtype) for col, dtype in df.dtypes.items()}

    numerical_columns = list(df.select_dtypes(include=["number"]).columns)
    categorical_columns = list(df.select_dtypes(include=["object"]).columns)

    target_column = df.columns[-1]
    feature_columns = df.columns[:-1].tolist()
    label_encoders = {}
    for column in categorical_columns:
        encoder = LabelEncoder()
        df[column]=encoder.fit_transform(df[column])
        label_encoders[column] = encoder
        joblib.dump(label_encoders, "label_encoder.pkl")


    scaler = StandardScaler()
    if numerical_columns:
        df[numerical_columns] = scaler.fit_transform(df[numerical_columns])
        joblib.dump(scaler, "scaler.pkl")

    X=df[feature_columns]
    y=df[target_column]
    joblib.dump(feature_columns, "feature_columns.pkl")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    models={
        "Logistic Regression": LogisticRegression(),
        "Decision Tree": DecisionTreeClassifier(),
        "Random Forest": RandomForestClassifier(),
        "SVM": SVC(),
        "KNN": KNeighborsClassifier(n_neighbors=3),
        "Naive Bayes": GaussianNB()}
    scores={}
    for name,model in models.items():
        model.fit(X_train,y_train)
        predictions=model.predict(X_test)
        accuracy=accuracy_score(y_test,predictions)
        scores[name]=round(accuracy*100, 2)

    best_model_name=max(scores,key=scores.get)
    best_model=models[best_model_name]
    joblib.dump(best_model,"best_model.pkl")    
    return {
        "filename": file.filename,
        "rows": rows,
        "columns": columns,
        "column_names": column_names,
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "data_types": data_types,
        "numerical_columns": numerical_columns,
        "categorical_columns": categorical_columns,
        "feature_columns": feature_columns,
        "target_column": target_column,
        "preview": df.head().to_dict(orient="records"),
        "encoded_preview": df.head().to_dict(orient="records"),
        "label_mapping": label_encoders,
        "model_scores": scores,
        "best_model": best_model_name
    }

@app.post("/predict")
def predict(data:dict):
    model=joblib.load("best_model.pkl")
    input_data=pd.DataFrame([data])
    prediction=model.predict(input_data)
    return {"prediction": int(prediction[0])
        }

@app.post("/predict")
def predict(data: dict):
    model=joblib.load("best_model.pkl")
    scaler=joblib.load("scaler.pkl")
    label_encoders=joblib.load("label_encoder.pkl")
    feature_columns=joblib.load("feature_columns.pkl")
    input_df=pd.DataFrame([data])
    for column,encoder in label_encoders.items():
        input_df[column]=encoder.transform(input_df[column])
    if numerical_columns:
            input_df[numerical_columns]=scaler.transform(input_df[numerical_columns])
    input_df=input_df[feature_columns]
    prediction=model.predict(input_df)
    return {"prediction": int(prediction[0])} 