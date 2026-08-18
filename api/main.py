from fastapi import FastAPI, UploadFile, File
import pandas as pd
import numpy as np
import joblib

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Welcome to DataLens AI"
    }

@app.get("/about")
def about():
    return {
        "project": "DataLens AI",
        "version": "1.0",
        "type": "General Purpose Classification"
    }

@app.get("/health")
def health():
    return {
        "status": "running"
    }

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

    df = pd.read_csv(file.file)

    if df.empty:
        return {
            "error": "Dataset is empty."
        }

    if df.shape[1] < 2:
        return {
            "error": "Dataset must contain at least one feature and one target column."
        }

    rows = int(df.shape[0])
    columns = int(df.shape[1])

    column_names = df.columns.tolist()

    missing_values = {
        col: int(value)
        for col, value in df.isnull().sum().items()
    }

    duplicate_rows = int(df.duplicated().sum())

    data_types = {
        col: str(dtype)
        for col, dtype in df.dtypes.items()
    }

    target_column = df.columns[-1]

    feature_columns = df.columns[:-1].tolist()

    numerical_columns = df[feature_columns].select_dtypes(
        include=["number"]
    ).columns.tolist()

    categorical_columns = df[feature_columns].select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    df = df.dropna()

    if df.empty:
        return {
            "error": "No data remains after removing missing values."
        }

    label_encoders = {}

    for column in categorical_columns:

        encoder = LabelEncoder()

        df[column] = encoder.fit_transform(
            df[column].astype(str)
        )

        label_encoders[column] = encoder

    if df[target_column].dtype == "object" or str(df[target_column].dtype) == "category":

        target_encoder = LabelEncoder()

        df[target_column] = target_encoder.fit_transform(
            df[target_column].astype(str)
        )

        joblib.dump(
            target_encoder,
            "target_encoder.pkl"
        )

    else:

        target_encoder = None

    scaler = StandardScaler()

    if numerical_columns:

        df[numerical_columns] = scaler.fit_transform(
            df[numerical_columns]
        )

    joblib.dump(
        scaler,
        "scaler.pkl"
    )

    joblib.dump(
        label_encoders,
        "label_encoder.pkl"
    )

    joblib.dump(
        numerical_columns,
        "numerical_columns.pkl"
    )

    joblib.dump(
        categorical_columns,
        "categorical_columns.pkl"
    )

    joblib.dump(
        feature_columns,
        "feature_columns.pkl"
    )

    joblib.dump(
        target_column,
        "target_column.pkl"
    )

    X = df[feature_columns]

    y = df[target_column]

    if y.nunique() < 2:

        return {
            "error": "Target column must contain at least two classes."
        }

    if len(df) < 10:

        return {
            "error": "Dataset is too small. Use at least 10 rows."
        }

    try:

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
            stratify=y
        )

    except ValueError:

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "Random Forest": RandomForestClassifier(random_state=42),
        "SVM": SVC(),
        "KNN": KNeighborsClassifier(n_neighbors=3),
        "Naive Bayes": GaussianNB()
    }

    scores = {}

    trained_models = {}

    for name, model in models.items():

        try:

            model.fit(
                X_train,
                y_train
            )

            predictions = model.predict(
                X_test
            )

            accuracy = accuracy_score(
                y_test,
                predictions
            )

            scores[name] = round(
                float(accuracy * 100),
                2
            )

            trained_models[name] = model

        except Exception as error:

            scores[name] = f"Error: {str(error)}"

    valid_scores = {
        name: score
        for name, score in scores.items()
        if isinstance(score, (int, float))
    }

    if not valid_scores:

        return {
            "error": "None of the models could be trained.",
            "model_scores": scores
        }

    best_model_name = max(
        valid_scores,
        key=valid_scores.get
    )

    best_model = trained_models[
        best_model_name
    ]

    joblib.dump(
        best_model,
        "best_model.pkl"
    )

    preview = df.head().replace(
        {np.nan: None}
    ).to_dict(
        orient="records"
    )

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
        "preview": preview,
        "model_scores": scores,
        "best_model": best_model_name
    }


@app.post("/predict")
def predict(data: dict):

    model = joblib.load(
        "best_model.pkl"
    )

    scaler = joblib.load(
        "scaler.pkl"
    )

    label_encoders = joblib.load(
        "label_encoder.pkl"
    )

    numerical_columns = joblib.load(
        "numerical_columns.pkl"
    )

    feature_columns = joblib.load(
        "feature_columns.pkl"
    )

    input_df = pd.DataFrame(
        [data]
    )

    for column, encoder in label_encoders.items():

        if column in input_df.columns:

            input_df[column] = encoder.transform(
                input_df[column].astype(str)
            )

    if numerical_columns:

        input_df[numerical_columns] = scaler.transform(
            input_df[numerical_columns]
        )

    input_df = input_df[
        feature_columns
    ]

    prediction = model.predict(
        input_df
    )

    result = prediction[0]

    if isinstance(result, np.integer):

        result = int(result)

    return {
        "prediction": result
    }