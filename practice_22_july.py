
import json
import os
from datetime import datetime

class Student:
    def __init__(self, student_id, name, age, email, grades=None):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.email = email
        self.grades = grades if grades else {}
        self.enrollment_date = datetime.now().strftime("%Y-%m-%d")
    
    def add_grade(self, subject, grade):
        if 0 <= grade <= 100:
            self.grades[subject] = grade
            return True
        return False
    
    def get_average(self):
        if not self.grades:
            return 0
        return sum(self.grades.values()) / len(self.grades)
    
    def get_letter_grade(self):
        avg = self.get_average()
        if avg >= 90: return 'A'
        elif avg >= 80: return 'B'
        elif avg >= 70: return 'C'
        elif avg >= 60: return 'D'
        else: return 'F'
    
    def __str__(self):
        return f"ID: {self.student_id}, Name: {self.name}, Average: {self.get_average():.2f}"

class StudentManager:
    def __init__(self, filename="students.json"):
        self.students = {}
        self.filename = filename
        self.load_data()
    
    def add_student(self, student):
        self.students[student.student_id] = student
        print(f"Student {student.name} added successfully!")
    
    def remove_student(self, student_id):
        if student_id in self.students:
            removed = self.students.pop(student_id)
            print(f"Student {removed.name} removed successfully!")
            return True
        print("Student not found!")
        return False
    
    def find_student(self, student_id):
        return self.students.get(student_id, None)
    
    def get_top_students(self, n=5):
        sorted_students = sorted(
            self.students.values(),
            key=lambda x: x.get_average(),
            reverse=True
        )
        return sorted_students[:n]
    
    def get_students_by_grade(self, letter_grade):
        return [s for s in self.students.values() if s.get_letter_grade() == letter_grade]
    
    def save_data(self):
        try:
            data = {}
            for sid, student in self.students.items():
                data[sid] = {
                    'name': student.name,
                    'age': student.age,
                    'email': student.email,
                    'grades': student.grades,
                    'enrollment_date': student.enrollment_date
                }
            
            with open(self.filename, 'w') as file:
                json.dump(data, file, indent=2)
            print("Data saved successfully!")
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    data = json.load(file)
                    
                for sid, info in data.items():
                    student = Student(
                        sid, info['name'], info['age'], 
                        info['email'], info['grades']
                    )
                    student.enrollment_date = info['enrollment_date']
                    self.students[sid] = student
                print("Data loaded successfully!")
            except Exception as e:
                print(f"Error loading data: {e}")

def generate_student_report(manager):
    print("\n" + "="*50)
    print("STUDENT MANAGEMENT SYSTEM REPORT")
    print("="*50)
    
    total_students = len(manager.students)
    print(f"Total Students: {total_students}")
    
    if total_students == 0:
        print("No students in the system.")
        return

    all_averages = [s.get_average() for s in manager.students.values() if s.get_average() > 0]
    if all_averages:
        overall_avg = sum(all_averages) / len(all_averages)
        print(f"Overall Class Average: {overall_avg:.2f}")
    
    grade_counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
    for student in manager.students.values():
        grade_counts[student.get_letter_grade()] += 1
    
    print("\nGrade Distribution:")
    for grade, count in grade_counts.items():
        print(f"  {grade}: {count} students")
    
    print("\nTop 3 Students:")
    top_students = manager.get_top_students(3)
    for i, student in enumerate(top_students, 1):
        print(f"  {i}. {student}")

def main():
    manager = StudentManager()
    
    # Sample data creation
    sample_students = [
        Student("S001", "Alice Johnson", 20, "alice@email.com", {"Math": 95, "Science": 88, "English": 92}),
        Student("S002", "Bob Smith", 19, "bob@email.com", {"Math": 78, "Science": 85, "English": 80}),
        Student("S003", "Charlie Brown", 21, "charlie@email.com", {"Math": 92, "Science": 96, "English": 89}),
        Student("S004", "Diana Prince", 20, "diana@email.com", {"Math": 67, "Science": 72, "English": 75}),
        Student("S005", "Eve Wilson", 22, "eve@email.com", {"Math": 45, "Science": 50, "English": 48})
    ]
    
    # Add sample students
    for student in sample_students:
        manager.add_student(student)
    
    # Demonstrate various operations
    print("\nDemonstrating search functionality:")
    found_student = manager.find_student("S001")
    if found_student:
        print(f"Found: {found_student}")
    
    print("\nStudents with grade 'A':")
    a_students = manager.get_students_by_grade('A')
    for student in a_students:
        print(f"  {student}")
    
    # Generate report
    generate_student_report(manager)
    
    # Save data
    manager.save_data()

if __name__ == "__main__":
    main()
