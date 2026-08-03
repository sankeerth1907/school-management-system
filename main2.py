import json
from abc import ABC, abstractmethod
from pathlib import Path

database = "school.json"
data = {
    "student": [],
    "teacher": []
}

if Path(database).exists():
    with open(database, "r") as file:
        content = file.read()
        if content:
            data = json.loads(content)


def save_database():
    with open(database, "w") as file:
        json.dump(data, file, indent=4)


class person(ABC):
    @abstractmethod
    def get_roles(self):
        pass

    def register(self):
        pass

    def show_details(self):
        pass

    @staticmethod
    def validate_email(email):
        if "@" in email and "." in email:
            return True
        else:
            return False


class student(person):
    def get_roles(self):
        return "student"

    def register(self):
        name = input("Enter student name: ")
        rollno = input("Enter student roll no: ")
        email = input("Enter student email: ")

        if not student.validate_email(email):
            print("Invalid email")
            return

        for i in data["student"]:
            if i["rollno"] == rollno:
                print("student already exists")
                return

        data["student"].append({
            "name": name,
            "rollno": rollno,
            "email": email,
            "grades": {}
        })
        save_database()

        print(f"Student {name} registered")

    def show_details(self):
        rollno = input("Enter student roll no: ")
        for s in data["student"]:
            if s["rollno"] == rollno:
                grades = s["grades"]
                print("Name:", s["name"])
                print("Rollno:", s["rollno"])
                print("Email:", s["email"])
                print("Grades:", grades)
                if grades:
                    avg = sum(grades.values()) / len(grades)
                    print("Average:", avg)
                else:
                    print("Average: no grades yet")
                return
        print("Rollno not found")

    def add_grades(self):
        rollno = input("Enter student roll no: ")
        subject = input("Enter subject: ")
        grade = input("Enter grade: ")

        try:
            grade = float(grade)
        except ValueError:
            print("Grade must be a number")
            return

        for s in data["student"]:
            if s["rollno"] == rollno:
                s["grades"][subject] = grade
                save_database()
                print("Grades added")
                return
        print("Rollno not found")

    def delete_student(self):
        rollno = input("Enter student roll no to delete: ")
        for s in data["student"]:
            if s["rollno"] == rollno:
                confirm = input(f"Are you sure you want to delete {s['name']} ({rollno})? (y/n): ")
                if confirm.lower() == "y":
                    data["student"].remove(s)
                    save_database()
                    print("Student deleted")
                else:
                    print("Delete cancelled")
                return
        print("Rollno not found")

    def show_all_students(self):
        for s in data["student"]:
            grades = s["grades"]
            print(f"Name: {s['name']}")
            print(f"Roll No: {s['rollno']}")
            print(f"Email: {s['email']}")
            print(f"Grades: {grades}")
            if grades:
                avg = sum(grades.values()) / len(grades)
                print(f"Average: {avg}")
            else:
                print("No grades yet")


class teacher(person):
    def get_roles(self):
        return "teacher"

    def register(self):
        name = input("Enter teacher name: ")
        email = input("Enter teacher email: ")
        subject = input("Enter subject: ")
        empid = input("Enter employee id: ")

        if not teacher.validate_email(email):
            print("Invalid email")
            return

        for i in data["teacher"]:
            if i["empid"] == empid:
                print("Teacher already exists")
                return

        data["teacher"].append({
            "name": name,
            "email": email,
            "subject": subject,
            "empid": empid
        })
        save_database()
        print(f"Teacher {name} registered")

    def show_details(self):
        empid = input("Enter teacher id: ")
        for i in data["teacher"]:
            if i["empid"] == empid:
                print("Name:", i["name"])
                print("Email:", i["email"])
                print("Subject:", i["subject"])
                print("Employee id:", i["empid"])
                return
        print("Employee id not found")

    def delete_teacher(self):
        empid = input("Enter teacher employee id to delete: ")
        for i in data["teacher"]:
            if i["empid"] == empid:
                confirm = input(f"Are you sure you want to delete {i['name']} ({empid})? (y/n): ")
                if confirm.lower() == "y":
                    data["teacher"].remove(i)
                    save_database()
                    print("Teacher deleted")
                else:
                    print("Delete cancelled")
                return
        print("Employee id not found")

    def show_all_teachers():
        for t in data["teacher"]:
            print(f"Name: {t['name']}")
            print(f"Email: {t['email']}")
            print(f"Subject: {t['subject']}")
            print(f"Employee ID: {t['empid']}")

teach = teacher()
stud = student()
print("press 1 to register student")
print("press 2 to register teacher")
print("press 3 to add grades")
print("press 4 to view student details")
print("press 5 to view teacher details")
print("press 6 to view all students")
print("press 7 to view all teachers")
print("press 8 to delete a student")
print("press 9 to delete a teacher")

try:
    choice = int(input("Enter your choice: "))
except ValueError:
    choice = -1

if choice == 1:
    stud.register()
elif choice == 2:
    teach.register()
elif choice == 3:
    stud.add_grades()
elif choice == 4:
    stud.show_details()
elif choice == 5:
    teach.show_details()
elif choice == 6:
    stud.show_all_students()
elif choice == 7:
    teach.show_all_teachers()
elif choice == 8:
    stud.delete_student()
elif choice == 9:
    teach.delete_teacher()
else:
    print("Invalid choice")