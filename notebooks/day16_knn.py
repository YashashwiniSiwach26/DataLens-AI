import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)
data={
    "Hours":[1,2,3,4,5,6,7,8,9,10,11,12],
    "Attendance":[60,65,68,70,75,80,90,92,95,98],
    "Pass":[0,0,0,0,1,1,1,1,1,1,1,1]
}
df=pd.DataFrame(data)
print(df)

X=df[["Hours","Attendance"]]
y=df["Pass"]
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)
scaler=StandardScaler()
X_train=scalar.fit_transform(X_train)
X_test=scaler.transform(X_test)
model=KNeighborsClassifier(n_neighbors=3)
model.fit(X_train,y_train)
predictions=model.predict(X_test)
accuracy=accuracy_score(y_test,predictions)
print("Accuracy:",accuracy)
cm=confusion_matrix(y_test,predictions)
print(classification_report(y_test,predictions))
new_student=scaler.transform([[6.5,84]])
prediction=model.predict(new_student)
print(prediction)