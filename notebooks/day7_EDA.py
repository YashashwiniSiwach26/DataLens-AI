import pandas as pd
import matplotlib.pyplot as plt
df=pd.read_csv("C:\\Users\\dev15\\Documents\\DataLens-AI\\datasets\\students.csv")
#EDA is an approach to analyze and summarize datasets to understand their main characteristics, often using visual
print(df)
print(df.head())
print(df.tail())
print(df.describe())
print(df["Marks"].mean())
print(df["Marks"].median())
print(df["Department"].mode())
print(df["Marks"].max())
print(df["Marks"].min())
df["Department"].value_counts().plot(kind="bar")
#value_counts() is a method in pandas that returns a Series containing counts of unique values in a column.
#plot(kind="bar") is used to create a bar plot of the counts of unique values in the "Department" column.
plt.title("Department Distribution")
plt.xlabel("Department")
plt.ylabel("Count")
plt.show()
df["Marks"].plot(kind="hist", bins=5)
#hist() is a method in pandas that creates a histogram of the "Marks" column, with the specified number of bins (5 in this case).
#bins are the intervals that divide the range of values in the "Marks" column into equal parts for visualization.
plt.title("Marks Distribution")
plt.xlabel("Marks")
plt.ylabel("Frequency")
plt.show()

df.boxplot(column="Marks")
plt.title("Marks Boxplot")
plt.show()

print(df.corr(numeric_only=True))
#models that require scaling
#knn,logistic regression,neural networks,svm 
#usually not required in decision tree ,random forest,XGBoost