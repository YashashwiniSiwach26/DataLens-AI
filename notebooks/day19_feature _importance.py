import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

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
model=RandomForestClassifier(
    random_state=42
)
model.fit(X_train,y_train)
importance=model.feature_importances_
print(importance)

importance_df=pd.DataFrame({
    "Feature":X.columns,
    "Importance":importance
})
print(importance_df)
importance_df=importance_df.sort_values(
    by='Importance',ascending=False
)
print(importance_df)
plt.figure(figsize=(6,4))
plt.bar(
    importance_df['Feature'],
    importance_df['Importance']
)
plt.title("Feature Importance")
plt.xlabel("Features")
plt.ylabel("Importance")
plt.show()