import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import accuracy_score
from sklearn.tree import plot_tree

import matplotlib.pyplot as plt

data={
    "Hours":[1,2,3,4,5,6,7,8,9,10],
    "Pass":[0,0,0,0,1,1,1,1,1,1]
}
df=pd.DataFrame(data)
print(df)
X=df[["Hours"]]
y=df["Pass"]
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)
model=DecisionTreeClassifier(
    criterion="gini",max_depth=2,random_state=42
)
model.fit(X_train,y_train)
predictions=model.predict(X_test)
accuracy=accuracy_score(y_test,predictions)
print("Accuracy",accuracy)

plt.figure(figsize=(8,6))
plot_tree(
    model,feature_names=["Hours"],class_names=["True","False"],filled=True
)
plt.show()

prediction=model.predict([[6]])
print(prediction)