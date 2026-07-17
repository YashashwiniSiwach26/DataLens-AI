import pandas as pd
print("====== Pandas Basics =======")
student={
    "Name":["yasha","yuvi","sneha","priya"],
    "Age":[20,21,22,23],
    "Marks":[70,80,82,91]   
}
df=pd.DataFrame(student)
print("DataFrame:\n",df)
print("\nShape:", df.shape)
print("\nColumns:", df.columns)
print("\nInfo:")
print(df.info())
print("\nDescription:")
print(df.describe())
print("\nMarks:")
print(df["Marks"])
print("\nFirst Row:")
print(df.iloc[0])
df["Passed"]=["Yes","Yes","Yes","Yes"]
print(df)
df.to_csv("student.csv",index=False)
data={
    "Name":["yasha","yuvi","sneha","priya"],
    "Branch":["CSE","ECE","MECH","CIVIL"],
    "Semester":[3,4,5,6],
    "CGPA":[8.5,8.0,7.5,9.0],
    "City":["Bangalore","Hyderabad","Chennai","Mumbai"]
}
df_data=pd.DataFrame(data)
print("\nShape of df_data:", df_data.shape)
print("\nDataFrame df_data:\n", df_data)
print("\nCGPA:")
print(df_data["CGPA"])
df_data["Placement_Ready"]=["Yes","Yes","Yes","Yes"]
df_data.to_csv("my_profile.csv",index=False)
#pandas is used for data analysis and manipulation. It provides data structures like Series and DataFrame to work with structured data.
