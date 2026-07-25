import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import(
    accuracy_score,
    confusion_matrix,
    classification_report
)
data={
    "Hours":[1,2,3,4,5,6,7,8,9,10,11,12],
    "Pass":[0,0,0,0,1,1,1,1,1,1,1,1]
}
df=pd.DataFrame(data)
print(df)

X=df[["Hours"]]
y=df["Pass"]
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)
#model=SVC(kernel="linear",
#         C=1,
#         random_state=42)
model=SVC(kernel="rbf",
          C=10,
          random_state=42)
model.fit(X_train,y_train)
predictions=model.predict(X_test)
accuracy=accuracy_score(y_test,predictions)
print("Accuracy",accuracy)
cm=confusion_matrix(y_test,predictions)
print("\nConfusion Matrix")
print(cm)
print("\nClassification Report")
print(classification_report(y_test,predictions))
#prediction=model.predict([[6.5]])
prediction=model.predict([[8.5]])
print("Prediction:",prediction)
importance=model.feature_importances_
print("Feature Importance:",importance)
