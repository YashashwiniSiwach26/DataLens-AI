print("=" * 50)
print("🚀 Welcome to DataLens AI")
print("Building ML" )
print("=" * 50)
name="Yashashwini"
age=20
cgpa=8.81
print("\nUser Information:")
print(f"name: {name}, age: {age}, cgpa: {cgpa}")
skills=["Python","Machine Learning","Git","Data Analysis"]
languages=["Python","C++","C","Java"]
print("\nskills:")
for skill in skills:
    print(f"skill:{skill}")
print("\nlanguages:")
for language in languages:
    print(f"language:{language}")
student={"name":name,"age":age,"cgpa":cgpa}
print("\nStudent Information:")
print(f"name:{student['name']},age:{student['age']},cgpa:{student['cgpa']}")
def greet():
    print("Welcome to my project!")
greet()
if age>=18:
    print(f"hello{name},you are elgible to use the platform")
else:
    print(f"Sorry{name},you are not elgible to use the platform")
skill=["Python","Machine Learning","Git","Data Analysis"]
print("\nSkills:")
for s in skill:
    print(f"skill:{s}")
with open ("notes.txt","w") as file:
    file.write(f"User:{name}\n")
    file.write(f"Age:{age}\n")
    file.write(f"CGPA:{cgpa}\n")
    file.write("Stay tuned for more updates!\n")



