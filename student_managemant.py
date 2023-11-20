import json

class StudentManagementApp:
    def __init__(self):
        self.students = []
        self.file_path = "students.txt"
        self.load_data()

    def load_data(self):
        try:
            with open(self.file_path, "r") as file:
                self.students = json.load(file)
        except FileNotFoundError:
            with open(self.file_path, "w") as file:
                json.dump([], file)

    def save_data(self):
        with open(self.file_path, "w") as file:
            json.dump(self.students, file)

    def show_all_students(self):
        if not self.students:
            print("No students in the database.")
            return

        for student in self.students:
            self.display_student_info(student)

    def filter_students(self, criteria):
        filtered_students = [student for student in self.students if student.get("Class") == criteria]
        if not filtered_students:
            print(f"No students found in class {criteria}.")
            return

        for student in filtered_students:
            self.display_student_info(student)

    def search_student(self, query):
        matching_students = [student for student in self.students if
                             query.lower() in student.get("Full Name").lower() or
                             query.lower() == str(student.get("Roll Number")).lower()]
        if not matching_students:
            print("No matching students found.")
            return

        for student in matching_students:
            self.display_student_info(student)

    def update_student(self, roll_number, new_data):
        for student in self.students:
            if student.get("Roll Number") == roll_number:
                student.update(new_data)
                print("Student record updated successfully.")
                self.save_data()
                return
        print("Student not found.")

    def delete_student(self, roll_number):
        for student in self.students:
            if student.get("Roll Number") == roll_number:
                self.students.remove(student)
                print("Student record deleted successfully.")
                self.save_data()
                return
        print("Student not found.")

    def add_student(self):
        new_student = {
            "Full Name": input("Enter Full Name: "),
            "Age": input("Enter Age: "),
            "Date of Birth": input("Enter Date of Birth: "),
            "Class": input("Enter Class: "),
            "Subjects List": input("Enter Subjects List (comma-separated): ").split(","),
            "Marks": {},
        }

        total_marks = 0
        for subject in new_student["Subjects List"]:
            marks = int(input(f"Enter marks for {subject}: "))
            new_student["Marks"][subject] = marks
            total_marks += marks

        new_student["Percentage"] = total_marks / len(new_student["Subjects List"])
        new_student["Grade"] = self.calculate_grade(new_student["Percentage"])

        #  unique Roll Number
        new_student["Roll Number"] = len(self.students) + 1

        self.students.append(new_student)
        print("Student added successfully.")
        self.save_data()

    def calculate_grade(self, percentage):
        if percentage >= 90:
            return "A+"
        elif 80 <= percentage < 90:
            return "A"
        elif 70 <= percentage < 80:
            return "B"
        elif 60 <= percentage < 70:
            return "C"
        elif 50 <= percentage < 60:
            return "D"
        else:
            return "F"

    def calculate_average_marks(self, roll_number):
        for student in self.students:
            if student.get("Roll Number") == roll_number:
                marks = student.get("Marks")
                average_marks = sum(marks.values()) / len(marks)
                print(f"\nAverage Marks for {student.get('Full Name')}: {average_marks:.2f}")
                return
        print("Student not found.")

    def display_student_info(self, student):
        print("\nStudent Information:")
        for key, value in student.items():
            if key == "Marks":
                print("Marks:")
                for subject, marks in value.items():
                    print(f"  {subject}: {marks}")
            else:
                print(f"{key}: {value}")

    def run(self):
        while True:
            print("\nOptions:")
            print("1. Show all Students")
            print("2. Filter Students based on criteria")
            print("3. Search for a Student")
            print("4. Update a Student's Record")
            print("5. Delete a Student")
            print("6. Add a new Student")
            print("7. Calculate Average Marks of a Student")
            print("8. Exit")

            choice = input("Enter your choice (1-8): ")

            if choice == "1":
                self.show_all_students()
            elif choice == "2":
                criteria = input("Enter criteria (Class): ")
                self.filter_students(criteria)
            elif choice == "3":
                query = input("Enter student name or roll number: ")
                self.search_student(query)
            elif choice == "4":
                roll_number = input("Enter the Roll Number of the student to update: ")
                new_data = {
                    "Age": input("Enter new age: "),
                    "Class": input("Enter new class: "),
                }
                self.update_student(roll_number, new_data)
            elif choice == "5":
                roll_number = input("Enter the Roll Number of the student to delete: ")
                self.delete_student(roll_number)
            elif choice == "6":
                self.add_student()
            elif choice == "7":
                roll_number = input("Enter the Roll Number of the student to calculate average marks: ")
                self.calculate_average_marks(roll_number)
            elif choice == "8":
                print("Exiting the Student Management Application.")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 8.")

if __name__ == "__main__":
    app = StudentManagementApp()
    app.run()
7