import pandas  as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
df=pd.read_csv("C:\\Users\\dev15\\Documents\\DataLens-AI\\datasets\\students.csv")
print(df)
encoder=LabelEncoder()
df["Depatment_Label"]=encoder.fit_transform(df["Department"])
encoded=pd.get_dummies(df["Department"])
print(encoded)
df=pd.concat([df,encoded],axis=1)
scaler=StandardScaler()
df["Age_scaled"]=scaler.fit_transform(df[["Age"]])
print(df[["Age","Age_scaled"]])
minmax=MinMaxScaler()
df["Marks_scaled"]=minmax.fit_transform(df[["Marks"]])
print(df[["Marks","Marks_scaled"]])
df.to_csv("datasets/preprocessed_students.csv",index=False)
df["City"]=["Delhi","Mumbai","Noida","Chennai"]
