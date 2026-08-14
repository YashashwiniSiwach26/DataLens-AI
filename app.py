import streamlit as st
import pandas as pd
import requests

st.set_page_config(
    page_title="DataLens AI",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 DataLens AI")

st.subheader(
    "Automated Machine Learning and Data Analysis Platform"
)

st.sidebar.title("DataLens AI")

st.sidebar.write(
    "Automated Machine Learning Platform "
    "for Dataset Analysis and Model Selection"
)

st.sidebar.write("Built with:")
st.sidebar.write("- Python")
st.sidebar.write("- Streamlit")
st.sidebar.write("- FastAPI")
st.sidebar.write("- Pandas")
st.sidebar.write("- Scikit-learn")


uploaded_file = st.file_uploader(
    "Upload your CSV dataset",
    type=["csv"]
)


if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

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

    st.header("Dataset Preview")

    st.dataframe(
        df,
        use_container_width=True
    )

    st.header("Missing Values")

    missing_values = df.isnull().sum()

    st.dataframe(
        missing_values
    )

    if st.button(
        "🚀 Analyze Dataset"
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

            if response.status_code != 200:

                st.error(
                    "FastAPI returned an error."
                )

                st.json(result)

            elif "error" in result:

                st.error(
                    result["error"]
                )

                st.json(result)

            else:

                st.success(
                    "Dataset analyzed successfully!"
                )

                st.header(
                    "Model Performance"
                )

                scores = result[
                    "model_scores"
                ]

                for model_name, score in scores.items():

                    st.write(
                        f"**{model_name}: {score}%**"
                    )

                    st.progress(
                        float(score) / 100
                    )

                st.header(
                    "Best Model"
                )

                st.success(
                    f"🏆 {result['best_model']}"
                )

                st.header(
                    "Dataset Information"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        "**Numerical Columns**"
                    )

                    st.write(
                        result[
                            "numerical_columns"
                        ]
                    )

                with col2:

                    st.write(
                        "**Categorical Columns**"
                    )

                    st.write(
                        result[
                            "categorical_columns"
                        ]
                    )

                st.write(
                    "**Target Column:**",
                    result["target_column"]
                )

                st.write(
                    "**Feature Columns:**",
                    result["feature_columns"]
                )

                st.header(
                    "Label Mapping"
                )

                st.json(
                    result["label_mapping"]
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Could not connect to FastAPI."
            )

            st.info(
                "Start FastAPI using:"
            )

            st.code(
                "uvicorn api.main:app --reload"
            )

        except Exception as e:

            st.error(
                f"Error: {str(e)}"
            )