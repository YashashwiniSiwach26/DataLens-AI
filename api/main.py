from fastapi import FastAPI, UploadFile, File
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder

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
        label_encoders[column] = list(encoder.classes_)


    scaler = StandardScaler()
    if numerical_columns:
        df[numerical_columns] = scaler.fit_transform(df[numerical_columns])

    

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
        "label_mapping": label_encoders
    }


