import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB 
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)
data={
    "Hours":[1,2,3,4,5,6,7,8,9,10,11,12],
    "Attendance":[60,65,68,70,75,80,82,85,90,92,95,98],
    "Pass":[0,0,0,0,1,1,1,1,1,1,1,1]
}
df=pd.DataFrame(data)
print(df)

X=df[["Hours","Attendance"]]
y=df["Pass"]
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)
model=GaussianNB()
model.fit(X_train,y_train)
predictions=model.predict(X_test)
accuracy=accuracy_score(y_test,predictions)
print("Accuracy:",accuracy)
cm=confusion_matrix(y_test,predictions)
print(classification_report(y_test,predictions))
prediction=model.predict([[6.5,84]])
print(prediction)
probablity=model.predict_proba([[6.5,84]])
print(probablity)
