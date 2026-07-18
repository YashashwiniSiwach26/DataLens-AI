import pandas as pd
df=pd.read_csv("C:\\Users\\dev15\\Documents\\DataLens-AI\\datasets\\students.csv")
print(df)
df.info()
print(df.shape)
print(df.isnull().sum())
print(df.duplicated().sum())
#dropping the duplicates
df=df.drop_duplicates()
print(df.duplicated().sum())
#finding Missing Values and replacing them with mean
df['Age']=df['Age'].fillna(df['Age'].mean())
df['Marks']=df['Marks'].fillna(df['Marks'].mean())
#verfying the null values after replacing them with mean
print(df.isnull().sum())
#what is EDA? EDA stands for Exploratory Data Analysis. 
# It is an approach to analyze and summarize datasets to understand their main characteristics, often using visual methods.
#  EDA helps in identifying patterns, spotting anomalies, testing hypotheses, and checking assumptions with the help of summary statistics and graphical representations.
#why is data cleaning important? 
# Data cleaning is important because it ensures the accuracy, consistency, and reliability of data.
#  Clean data is essential for making informed decisions, building predictive models, and conducting meaningful analyses. 
# It helps in reducing errors, improving data quality, and enhancing the overall effectiveness of data-driven processes.

#why do we use drop_duplicates() in pandas?
# We use drop_duplicates() in pandas to remove duplicate rows from a DataFrame.


