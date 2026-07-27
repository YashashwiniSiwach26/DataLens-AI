import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score

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
model=DecisionTreeClassifier(random_state=42)
parameters={
    "max_depth":[2,3,4,5],
    "criterion":["gini",'entropy']
}
grid=GridSearchCV(
    estimator=model,
    param_grid=parameters,cv=5
)
grid.fit(X_train,y_train)
print("Best Parameters:")
print(grid.best_params_)
print("Best CV Score:")
print(grid.best_score_)
best_model=grid.best_estimator_
predictions=best_model.predict(X_test)
accuracy=accuracy_score(y_test,predictions)
print("Test Accuracy",accuracy)
