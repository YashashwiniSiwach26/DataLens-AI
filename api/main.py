from fastapi import FastAPI #import fastapi framework
app=FastAPI() 
@app.get("/")
def home():
    return {
        "message":"Welcome to DataLens AI!"
    }
@app.get("/about")
def about():
    return{
        "project": "DataLens AI",
        "version":"1.0",
        "developer":"Yashashwini Siwach"
    }
@app.get("/health")
def health():
    return {
        "status":"running"
    }
@app.get("/models")
def models():
    return {
        "models":[
            "Logistic Regression",
            "Decision Tree",
            "Random Forest",
            "SVM",
            "KNN",
            "Naive Bayes"
        ]
    }
from fastapi import FastAPI, UploadFile, File
app=FastAPI()
@app.post("/upload-dataset/")
def upload_dataset(file:UploadFile=File(...)):
    return{
        "filename":file.filename
    }
#difference between post and get method is that post method is used to send data to the server and get method is used to retrieve data from the server.
#endpoints are the URLs that are used to access the resources on the server. 
#how do endpoints work? Endpoints work by defining a specific URL path and the HTTP method (GET, POST, etc.) that will be used to access that path. When a request is made to the endpoint, the server processes the request and returns a response based on the defined logic in the corresponding function.
#def upload_dataset(file:UploadFile=File(..)):
#  return{
#       "filename":file.filename
#   } this code is used to upload a dataset file to the server. The file is received as an UploadFile object, and the filename is returned in the response.
#difference in frontend and backend is that frontend is the part of the application that the user interacts with, while backend is the part of the application that handles the logic, database interactions, and server-side processing. The frontend is responsible for presenting data to the user and collecting user input, while the backend processes that input and returns the appropriate response.
#fastapi is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints. It is designed to be easy to use and to provide automatic interactive API documentation. FastAPI is built on top of Starlette for the web parts and Pydantic for the data parts. It allows developers to create APIs quickly and efficiently, with features like automatic validation, serialization, and documentation generation.
#functionalities of fastapi are:
#1. FastAPI is fast: It is one of the fastest Python frameworks available, thanks to its asynchronous capabilities and efficient design.
#2. Easy to use: FastAPI is designed to be easy to use and intuitive, with automatic validation and serialization of request and response data.
#3. Automatic documentation: FastAPI automatically generates interactive API documentation using Swagger UI and ReDoc   
#more function like get and post are available in fastapi like put, delete, patch, options, head, trace. These methods correspond to the standard HTTP methods and can be used to define endpoints for different types of requests. Each method serves a specific purpose in RESTful API design, allowing developers to create a comprehensive and well-structured API. 
from fastapi import FastAPI, UploadFile, File
import pandas as pd

app=FastAPI()
@app.post("/upload-dataset/")
def upload_dataset(file:UploadFile=File(...)):
    # Read the uploaded file into a pandas DataFrame
    #preview the first five rows of the dataset and return it as a dictionary  bcoz the data is in tabular format and we can use pandas to read the data and return it as a dictionary.
    df = pd.read_csv(file.file)
    print(df)
    return {
        "filename": file.filename,#file.filename is used to get the name of the file that is uploaded. this helps in identifying the file and also in saving the file with the same name. if it was file.file, it would return the file object instead of the filename.
        "preview":df.head().to_dict(orient="records")
        
    }
@app.post("/upload-dataset/")
def upload_dataset(file:UploadFile=File(...)):
    # Read the uploaded file into a pandas DataFrame
    df = pd.read_csv(file.file)
    rows,columans=df.shape
    column_name=df.columns.tolist()
    missing_values=df.isnull().sum().to_dict()#why is dict used here? because it is used to convert the series object to a dictionary object. this helps in returning the missing values in a key-value pair format. ex: {'column1': 0, 'column2': 5, 'column3': 2}
    duplicate_rows=df.duplicated().sum()#why is sum used here? because it is used to count the number of duplicate rows in the dataset. this helps in identifying the number of duplicate rows in the dataset.
    data_types=df.dtypes.to_dict()#why is dict used here? because it is used to convert the series object to a dictionary object. this helps in returning the data types of each column in a key-value pair format. ex: {'column1': 'int64', 'column2': 'float64', 'column3': 'object'}
    
    # Preview the first five rows of the dataset and return it as a dictionary
    return {
        "filename": file.filename,
        "row":rows,
        "columns":columans,
        "missing_value":missing_values,
        "duplicate_rows":duplicate_rows,
        "data_types":data_types,

        "preview": df.head().to_dict(orient="records")
    }
