"""
STUDENT GRADE AND ATTENDANCE ANALYZER
A beginner-friendly, menu-driven Python project.

Features:
1. Add a student
2. View all students
3. Update attendance
4. Add/update subject marks
5. View an individual student report
6. View class summary
7. Save data automatically in a JSON file

Only Python's built-in modules are used.
"""

import json
import os

DATA_FILE = "student_data.json"


def load_data():
    """Load saved student data from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read saved data. Starting with empty data.")
        return {}


def save_data(students):
    """Save all student data."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(students, file, indent=4)
    except OSError:
        print("Error: Data could not be saved.")


def get_percentage(obtained, maximum):
    if maximum <= 0:
        return 0
    return (obtained / maximum) * 100


def get_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "F"


def add_student(students):
    print("\n--- ADD STUDENT ---")
    roll_no = input("Enter roll number: ").strip()

    if not roll_no:
        print("Roll number cannot be empty.")
        return

    if roll_no in students:
        print("A student with this roll number already exists.")
        return

    name = input("Enter student name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    students[roll_no] = {
        "name": name,
        "classes_held": 0,
        "classes_attended": 0,
        "marks": {}
    }

    save_data(students)
    print("Student added successfully!")


def view_students(students):
    print("\n--- STUDENT LIST ---")

    if not students:
        print("No student records found.")
        return

    print(f"{'Roll No.':<12}{'Name':<25}{'Attendance':<15}{'Average':<12}")
    print("-" * 64)

    for roll_no, details in students.items():
        held = details["classes_held"]
        attended = details["classes_attended"]
        attendance = get_percentage(attended, held)

        marks = details["marks"]
        if marks:
            percentages = [
                get_percentage(item["obtained"], item["maximum"])
                for item in marks.values()
            ]
            average = sum(percentages) / len(percentages)
            average_text = f"{average:.2f}%"
        else:
            average_text = "N/A"

        print(f"{roll_no:<12}{details['name']:<25}"
              f"{attendance:.2f}%{'':<8}{average_text:<12}")


def update_attendance(students):
    print("\n--- UPDATE ATTENDANCE ---")
    roll_no = input("Enter student roll number: ").strip()

    if roll_no not in students:
        print("Student not found.")
        return

    try:
        held = int(input("Enter total classes held: "))
        attended = int(input("Enter classes attended: "))

        if held < 0 or attended < 0 or attended > held:
            print("Invalid values. Attended classes must be between 0 and total classes.")
            return

        students[roll_no]["classes_held"] = held
        students[roll_no]["classes_attended"] = attended
        save_data(students)
        print("Attendance updated successfully!")

    except ValueError:
        print("Please enter whole numbers only.")


def add_marks(students):
    print("\n--- ADD / UPDATE SUBJECT MARKS ---")
    roll_no = input("Enter student roll number: ").strip()

    if roll_no not in students:
        print("Student not found.")
        return

    subject = input("Enter subject name: ").strip()
    if not subject:
        print("Subject name cannot be empty.")
        return

    try:
        maximum = float(input("Enter maximum marks: "))
        obtained = float(input("Enter marks obtained: "))

        if maximum <= 0 or obtained < 0 or obtained > maximum:
            print("Invalid marks. Obtained marks must be between 0 and maximum marks.")
            return

        students[roll_no]["marks"][subject] = {
            "obtained": obtained,
            "maximum": maximum
        }

        save_data(students)
        print("Marks saved successfully!")

    except ValueError:
        print("Please enter valid numbers.")


def student_report(students):
    print("\n--- INDIVIDUAL STUDENT REPORT ---")
    roll_no = input("Enter student roll number: ").strip()

    if roll_no not in students:
        print("Student not found.")
        return

    details = students[roll_no]
    held = details["classes_held"]
    attended = details["classes_attended"]
    attendance = get_percentage(attended, held)

    print("\n" + "=" * 42)
    print("             STUDENT REPORT")
    print("=" * 42)
    print(f"Roll Number : {roll_no}")
    print(f"Name        : {details['name']}")
    print(f"Attendance  : {attended}/{held} classes ({attendance:.2f}%)")

    if held == 0:
        print("Attendance status: Not recorded")
    elif attendance >= 75:
        print("Attendance status: Eligible (75% or above)")
    else:
        print("Attendance status: Below 75%")

    print("\nSUBJECT-WISE PERFORMANCE")
    print("-" * 42)

    marks = details["marks"]
    if not marks:
        print("No marks have been entered.")
    else:
        percentages = []
        for subject, item in marks.items():
            percentage = get_percentage(item["obtained"], item["maximum"])
            percentages.append(percentage)
            grade = get_grade(percentage)
            print(f"{subject:<18} {item['obtained']:>6.1f}/{item['maximum']:<6.1f}"
                  f" {percentage:>6.2f}%  Grade: {grade}")

        average = sum(percentages) / len(percentages)
        print("-" * 42)
        print(f"Average Percentage: {average:.2f}%")
        print(f"Overall Grade     : {get_grade(average)}")

    print("=" * 42)


def class_summary(students):
    print("\n--- CLASS SUMMARY ---")

    if not students:
        print("No student records found.")
        return

    attendance_values = []
    grade_values = []
    low_attendance = []

    for roll_no, details in students.items():
        held = details["classes_held"]
        attended = details["classes_attended"]

        if held > 0:
            attendance = get_percentage(attended, held)
            attendance_values.append(attendance)
            if attendance < 75:
                low_attendance.append((roll_no, details["name"], attendance))

        marks = details["marks"]
        if marks:
            subject_percentages = [
                get_percentage(item["obtained"], item["maximum"])
                for item in marks.values()
            ]
            grade_values.append(sum(subject_percentages) / len(subject_percentages))

    print(f"Total students: {len(students)}")

    if attendance_values:
        print(f"Class average attendance: "
              f"{sum(attendance_values) / len(attendance_values):.2f}%")
    else:
        print("Class average attendance: Not available")

    if grade_values:
        print(f"Class average marks: "
              f"{sum(grade_values) / len(grade_values):.2f}%")
    else:
        print("Class average marks: Not available")

    print("\nStudents below 75% attendance:")
    if low_attendance:
        for roll_no, name, attendance in low_attendance:
            print(f"- {name} (Roll No. {roll_no}): {attendance:.2f}%")
    else:
        print("None")


def main():
    students = load_data()

    while True:
        print("\n" + "=" * 48)
        print("     STUDENT GRADE AND ATTENDANCE ANALYZER")
        print("=" * 48)
        print("1. Add student")
        print("2. View all students")
        print("3. Update attendance")
        print("4. Add or update subject marks")
        print("5. View student report")
        print("6. View class summary")
        print("7. Exit")
        print("-" * 48)

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_students(students)
        elif choice == "3":
            update_attendance(students)
        elif choice == "4":
            add_marks(students)
        elif choice == "5":
            student_report(students)
        elif choice == "6":
            class_summary(students)
        elif choice == "7":
            save_data(students)
            print("Thank you for using the Student Analyzer. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a number from 1 to 7.")


if __name__ == "__main__":
    main()
