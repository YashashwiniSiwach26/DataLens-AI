from fastapi import FastAPI, UploadFile, File
import pandas as pd

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

    rows, columns = df.shape
    column_names = df.columns.tolist()

    missing_values = df.isnull().sum().to_dict()
    duplicate_rows = df.duplicated().sum()
    data_types = df.dtypes.to_dict()

    numerical_columns = list(df.select_dtypes(include=["number"]).columns)
    categorical_columns = list(df.select_dtypes(include=["object"]).columns)

    target_column = df.columns[-1]
    feature_columns = df.columns[:-1].tolist()

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
        "preview": df.head().to_dict(orient="records")
    }

