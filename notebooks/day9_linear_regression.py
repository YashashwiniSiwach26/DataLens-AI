import pandas as pd #read dataset
from sklearn.model_selection import train_test_split #split data sets into training and testing
from sklearn.linear_model import LinearRegression #creates model
from sklearn.metrics import mean_absolute_error #measures prediction error

data={
    "Hours":[2,3,4,5,6,7,8,9],
    "Marks":[35,45,55,65,75,82,90,95]
}
df=pd.DataFrame(data)
print(df)
X=df[["Hours"]] # Double brackets because scikit learn expects 2D input
y=df["Marks"]
X_train,X_test,y_train,y_test=train_test_split(
    X,y,test_size=0.2,random_state=42
)
model=LinearRegression()
model.fit(X_train,y_train)
prediction=model.predict(X_test)

print("Actual Marks")
print(y_test)
print()
print("Predicted Marks")
print(prediction)

error=mean_absolute_error(y_test,prediction)
print("Mean Absolute error",error)

new_hours=[[7.5]]
predicted_marks=model.predict(new_hours)
print("Predicted Marks:",predicted_marks)
