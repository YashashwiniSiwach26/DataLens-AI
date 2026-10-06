import streamlit as st
import pandas as pd
import requests

st.set_page_config(
    page_title="DataLens-AI",
    page_icon="📊",
    layout="wide"
)

st.title("DataLens AI")

st.subheader(
    "Automated Machine Learning and Data Analysis Platform"
)

uploaded_file = st.file_uploader(
    "Upload your CSV dataset",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(
        uploaded_file
    )

    st.success(
        "Dataset uploaded successfully!"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Rows",
            df.shape[0]
        )

    with col2:
        st.metric(
            "Columns",
            df.shape[1]
        )

    with col3:
        st.metric(
            "Duplicate Rows",
            int(df.duplicated().sum())
        )

    st.subheader(
        "Dataset Preview"
    )

    st.dataframe(
        df.head(),
        use_container_width=True
    )

    st.subheader(
        "Data Types"
    )

    data_types = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str)
    })

    st.dataframe(
        data_types,
        use_container_width=True
    )

    st.subheader(
        "Missing Values"
    )

    missing_values = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isnull().sum().values
    })

    st.dataframe(
        missing_values,
        use_container_width=True
    )

    numerical_columns = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
            include=["object", "category"]
    ).columns.tolist()

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            "Numerical Columns"
        )

        st.write(
            numerical_columns
        )

    with col2:

        st.write(
            "Categorical Columns"
        )

        st.write(
            categorical_columns
        )

    target_column = st.selectbox(
        "Target column to predict",
        options=df.columns.tolist(),
        index=len(df.columns) - 1,
        help="Choose the outcome column. All remaining columns are used as features."
    )

    dataset_key = (uploaded_file.name, len(uploaded_file.getvalue()), target_column)
    if st.session_state.get("analysis_key") != dataset_key:
        st.session_state.pop("analysis_result", None)

    if st.button(
        "Analyze Dataset"
    ):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "text/csv"
            )
        }

        data = {"target_column": target_column}

        try:

            response = requests.post(
                "http://backend:8000/upload-dataset/",
                files=files,
                data=data,
                timeout=60
            )

            try:
                result = response.json()
            except ValueError:
                st.error("The backend returned an invalid response.")
                st.stop()

            if response.ok and "best_model" in result:
                st.session_state.analysis_result = result
                st.session_state.analysis_key = dataset_key
            else:
                st.error(result.get("detail", result.get("error", "Backend error occurred.")))

        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to FastAPI. "
                "Start the API using "
                "'uvicorn api.main:app --reload'."
            )

    result = st.session_state.get("analysis_result")
    if result:
            st.success("Dataset analyzed successfully!")
            st.header("Model Performance")
            for model_name, score in result.get("model_scores", {}).items():
                if isinstance(score, (int, float)):
                    st.write(f"**{model_name}**: {score}%")
                    st.progress(min(float(score) / 100, 1.0))
                else:
                    st.warning(f"{model_name}: {score}")
    
            st.success(f"Best Model: {result['best_model']}")
            st.info(f"Prediction target: {result['target_column']}")
    
            col1, col2, col3 = st.columns(3)
            col1.metric("Features", len(result["feature_columns"]))
            col2.metric("Numerical Columns", len(result["numerical_columns"]))
            col3.metric("Categorical Columns", len(result["categorical_columns"]))
    
            st.subheader(f"Predict {result['target_column']}")
            with st.form("prediction_form"):
                prediction_input = {}
                for column in result["feature_columns"]:
                    if pd.api.types.is_numeric_dtype(df[column]):
                        default = float(df[column].median()) if df[column].notna().any() else 0.0
                        prediction_input[column] = st.number_input(column, value=default)
                    else:
                        choices = sorted(df[column].dropna().astype(str).unique().tolist())
                        if choices:
                            prediction_input[column] = st.selectbox(column, choices)
    
                predict_clicked = st.form_submit_button("Predict", type="primary")
    
            if predict_clicked:
                try:
                    prediction_response = requests.post(
                        "http://backend:8000/predict",
                        json=prediction_input,
                        timeout=30
                    )
                    prediction_result = prediction_response.json()
                    if prediction_response.ok:
                        st.success(f"Predicted {result['target_column']}: {prediction_result['prediction']}")
                    else:
                        st.error(prediction_result.get("detail", "Prediction failed."))
                except (requests.exceptions.RequestException, ValueError) as error:
                    st.error(f"Prediction request failed: {error}")

