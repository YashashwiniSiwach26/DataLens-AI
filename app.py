import streamlit as st
import pandas as pd
import requests
st.title("DataLens AI")
st.write("Automated Machine learning and Data Analysis Platform")
uploaded_file=st.file_uploader("Upload your CSV dataset",type=["csv"])
if uploaded_file is not None:
    df=pd.read_csv(uploaded_file)
    st.write("Dataset uploaded successfully!")
    st.dataframe(df)
    st.write("Rows:",df.shape[0])
    st.write("Columns",df.shape[1])
    st.header("Dataset Preview")
    st.dataframe(df.head())
    if st.button("Analyze Dataset"):
        files={
            "file":(uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
        response=requests.post("http://127.0.0.1.8000/upload-dataset/", files=files)
        if response.status_code==200:
            result=response.json()
            st.success("Dataset analyzed successfully!")
            st.subheader("Model Performance")
            st.json(result["model_performance"])
            st.success(f"Best Model: {result['best_model']}")
        else:
            st.error("Error analyzing dataset. Please try again.")
            
