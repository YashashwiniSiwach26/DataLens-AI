import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

data={
    "Hours":[1,2,3,4,5,6,7,8,9,10],
    "Pass":[0,0,0,0,1,1,1,1,1,1]
}
df=pd.DataFrame(data)
print(df)
X=df[["Hours"]]
y=df["Pass"]
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)

model=LogisticRegression()
model.fit(X_train,y_train)

predictions=model.predict(X_test)

accuracy=accuracy_score(y_test,predictions)
print("Accuracy:",accuracy)

cm=confusion_matrix(y_test,predictions)
print(cm)

prediction=model.predict([[5.5]])
print(prediction)

probabality=model.predict_proba([[5.5]])
print(probabality)
