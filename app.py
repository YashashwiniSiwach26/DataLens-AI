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

    st.info(
        "The last column will be used as the target column."
    )

    st.write(
        "Target Column:",
        df.columns[-1]
    )

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

        try:

            response = requests.post(
                "http://127.0.0.1:8000/upload-dataset/",
                files=files
            )

            result = response.json()

            if "error" in result:

                st.error(
                    result["error"]
                )

                if "model_scores" in result:

                    st.subheader(
                        "Model Training Details"
                    )

                    for name, score in result[
                        "model_scores"
                    ].items():

                        st.write(
                            f"{name}: {score}"
                        )

            elif response.status_code == 200:

                st.success(
                    "Dataset analyzed successfully!"
                )

                st.header(
                    "Model Performance"
                )

                scores = result.get(
                    "model_scores",
                    {}
                )

                for model_name, score in scores.items():

                    st.write(
                        f"**{model_name}**"
                    )

                    if isinstance(
                        score,
                        (int, float)
                    ):

                        st.write(
                            f"Accuracy: {score}%"
                        )

                        st.progress(
                            min(
                                float(score) / 100,
                                1.0
                            )
                        )

                    else:

                        st.error(
                            str(score)
                        )

                if "best_model" in result:

                    st.success(
                        f"Best Model: "
                        f"{result['best_model']}"
                    )

                st.header(
                    "Analysis Summary"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Features",
                        len(
                            result[
                                "feature_columns"
                            ]
                        )
                    )

                with col2:

                    st.metric(
                        "Numerical Columns",
                        len(
                            result[
                                "numerical_columns"
                            ]
                        )
                    )

                with col3:

                    st.metric(
                        "Categorical Columns",
                        len(
                            result[
                                "categorical_columns"
                            ]
                        )
                    )

                st.write(
                    "Target Column:",
                    result[
                        "target_column"
                    ]
                )

            else:

                st.error(
                    "Backend error occurred."
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to FastAPI. "
                "Start the API using "
                "'uvicorn api.main:app --reload'."
            )