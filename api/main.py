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
