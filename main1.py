import json
from abc import ABC,abstractmethod
from pathlib import Path 

database = "school_data.json"
data = {"students" : [], "teachers" : []}

if Path(database).exists():
    with open(database,'r') as f:
        content = f.read()
        if content:
            data = json.loads(content)

def save():
    with open(database,"w") as f:
        json.dump(data,f,indent=4)


class Persons(ABC):

    @abstractmethod
    def get_roles(self):
        pass 

    @abstractmethod
    def register(self):
        pass 

    @abstractmethod
    def show_details(self):
        pass
    
    @staticmethod
    def validate_email(email):
        if "@" in email and "." in email:
            return True 
        else:
            return False 

class Student(Persons):

    def get_roles(self):
        return "student"
    
    def register(self):
        name = input("tell your name :- ")
        age = int(input("tell your age :- "))
        email = input("tell your mail :- ")
        roll_no = input("tell your roll number :- ")
    
        if not Persons.validate_email(email):
            print("invalid Email ")
            return

        for i in data['students']:
            if i['roll_no'] == roll_no:
                print("student already exist")
                return 
        
        data['students'].append({
            "name" : name, 
            "age" : age,
            "email" : email,
            "roll_no":roll_no,
            "grades" : {}
        })

        save()
        print(f"Student {name} registered")

    def show_details(self):
        roll_no = input("roll no :- ")
        for s in data['students']:
            if s['roll_no'] == roll_no:
                grades = s['grades']
                avg = sum(grades.values()) / len(grades) if grades else 0

                print(f"\n  Name    : {s['name']}")
                print(f"  Roll no : {s['roll_no']}")
                print(f"  Grades  : {grades}")
                print(f"  Average : {avg:.1f}")
                return




    def add_grade(self):
        roll_no = input("tell the roll number :- ")
        subject = input("Subject : ")
        marks = float(input("Marks : "))

        for i in data['students']:
            if i["roll_no"] == roll_no:
                i['grades'][subject] = marks
                save()
                print("grade added successfully")
                return 
        print("student not found")




class Teacher(Persons):
    def get_roles(self):
        return "Teacher"
    
    def register(self):
        name = input("tell your name :- ")
        age = int(input("tell your age :- "))
        email = input("tell your mail :- ")
        subject = input("subject : ")
        emp_id = input("tell your emp_id number :- ")

        if not Persons.validate_email(email):
            print("invalid Email ")
            return

        for i in data['teachers']:
            if i['emp_id'] == emp_id:
                print("Teacher already exist")
                return 
        
        data['teachers'].append({
            "name" : name, 
            "age" : age,
            "email" : email,
            "subject" : subject,
            "emp_id":emp_id,
        })
        save()
        print(f"Teacher {name} registerd")

    def show_details(self):
        emp_id = input("Employee ID: ")

        for t in data["teachers"]:
            if t["emp_id"] == emp_id:
                print(f"\n  Name    : {t['name']}")
                print(f"  Subject : {t['subject']}")
                print(f"  Emp ID  : {t['emp_id']}")
                return
        print("Teacher not found.")

        

stud = Student()
tech = Teacher()
print("press 1  to register a student")
print("press 2  to register a teacher")
print("press 3  to add grades")
print("press 4  to show a student detail")
print("press 5  to show a teacher detail")


choice = int(input("please tell your choice :- "))

if choice == 1:
    stud.register()

elif choice == 2:
    tech.register()

elif choice == 3:
    stud.add_grade()

elif choice == 4:
    stud.show_details()

elif choice == 5:
    tech.show_details()
