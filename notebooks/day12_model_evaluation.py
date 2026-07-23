import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import(
    accuracy_score,confusion_matrix,classification_report,precision_score,recall_score,f1_score
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
model=LogisticRegression()
model.fit(X_train,y_train)

predictions=model.predict(X_test)
accuracy=accuracy_score(y_test,predictions)
print("Accuracy",accuracy)
cm=confusion_matrix(y_test,predictions)
print("\nConfusion Matrix")
print(cm)
precision=precision_score(y_test,predictions)
print("Precision:",precision)
recall=recall_score(y_test,predictions)
print("Recall:",recall)
f1=f1_score(y_test,predictions)
print("F1 Score:",f1)

print("\nClassification Report")
print(classification_report(y_test,predictions))

#Accuracy=TP+TN/(TP+TN+FP+FN)
#Precision=TP/(TP+FP)
#Recall:TP+(TP+FN)
#F1_Score=2*(precision*Recall)/(Precision+Recall)