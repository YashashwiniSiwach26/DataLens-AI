import pandas as pd
import matplotlib.py as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

data={
    "Hours":[2,3,4,5,6,7,8,9],
    "Marks":[35,45,55,65,75,82,90,95]
}
df=pd.DataFrame(data)
X=df[["Hours"]]
y=df["Marks"]

model=LinearRegression()
model.fit(X,y)

predictions=model.predict(X)
print("Actual Marks")
print(y)
print("Predicted Marks")
print(predictions)

mse=mean_absolute_error(y,predictions)
print("Mean Squared Error",mse)

plt.scatter(df["Hours"],df["Marks"],label="Actual Data")
plt.plot(df["Hours"],predictions,color="red",label="Best fit line")
plt.title("Linear Regression")
plt.xlabel("Hours Studied")
plt.ylabel("Marks")
plt.legend()
plt.show()

print("Slope:",model.coef_[0])
print("Intercept",model.intercept_)

