
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os


# Student class
class Student:

    def __init__(self, code, name, course1, course2, course3, exam):
        self.code = code
        self.name = name
        self.course1 = course1
        self.course2 = course2
        self.course3 = course3
        self.exam = exam

    # Calculate coursework total
    def courseworkTotal(self):
        return self.course1 + self.course2 + self.course3

    # Calculate overall percentage
    def percentage(self):
        total = self.courseworkTotal() + self.exam
        return (total / 160) * 100

    # Calculate grade
    def grade(self):
        percentage = self.percentage()

        if percentage >= 70:
            return "A"
        elif percentage >= 60:
            return "B"
        elif percentage >= 50:
            return "C"
        elif percentage >= 40:
            return "D"
        else:
            return "F"


# Student Manager class
class StudentManager:

    def __init__(self, root):

        self.root = root
        self.root.title("Student Manager")
        self.root.geometry("1100x650")

        self.fileName = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "studentMarks.txt"
        )

        self.students = []

        self.loadStudents()

        # Application title
        title = tk.Label(
            root,
            text="STUDENT MANAGEMENT SYSTEM",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=15)

        # Menu frame
        menuFrame = tk.Frame(root)
        menuFrame.pack(pady=10)

        # Menu buttons
        buttons = [
            ("1. View All Students", self.viewAll),
            ("2. View Individual", self.viewIndividual),
            ("3. Highest Score", self.highestStudent),
            ("4. Lowest Score", self.lowestStudent),
            ("5. Sort Ascending", self.sortAscending),
            ("6. Sort Descending", self.sortDescending),
            ("7. Add Student", self.addStudent),
            ("8. Delete Student", self.deleteStudent),
            ("9. Update Student", self.updateStudent)
        ]

        for i, (text, command) in enumerate(buttons):
            button = tk.Button(
                menuFrame,
                text=text,
                width=18,
                command=command
            )
            button.grid(
                row=i // 3,
                column=i % 3,
                padx=5,
                pady=5
            )

        # Student records table
        columns = (
            "Code", "Name", "Coursework",
            "Exam", "Percentage", "Grade"
        )

        self.table = ttk.Treeview(
            root,
            columns=columns,
            show="headings",
            height=15
        )

        for column in columns:
            self.table.heading(column, text=column)
            self.table.column(column, width=145, anchor="center")

        self.table.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        # Summary label
        self.summaryLabel = tk.Label(
            root,
            text="Student records loaded",
            font=("Arial", 12, "bold")
        )
        self.summaryLabel.pack(pady=10)

        self.viewAll()

    # Load student records from file
    def loadStudents(self):

        self.students = []

        try:
            file = open(self.fileName, "r")

            lines = file.readlines()
            file.close()

            expectedCount = int(lines[0].strip())

            for line in lines[1:]:

                data = line.strip().split(",")

                if len(data) == 6:

                    student = Student(
                        int(data[0]),
                        data[1],
                        int(data[2]),
                        int(data[3]),
                        int(data[4]),
                        int(data[5])
                    )

                    self.students.append(student)

            if len(self.students) != expectedCount:
                messagebox.showwarning(
                    "File Warning",
                    "The number of records does not match the first line."
                )

        except FileNotFoundError:
            messagebox.showerror(
                "File Error",
                "studentMarks.txt was not found."
            )

        except (ValueError, IndexError):
            messagebox.showerror(
                "File Error",
                "The student file contains invalid data."
            )

    # Save records to file
    def saveStudents(self):

        file = open(self.fileName, "w")

        file.write(str(len(self.students)) + "\n")

        for student in self.students:

            record = (
                str(student.code) + "," +
                student.name + "," +
                str(student.course1) + "," +
                str(student.course2) + "," +
                str(student.course3) + "," +
                str(student.exam) + "\n"
            )

            file.write(record)

        file.close()

    # Display student information in the table
    def displayStudent(self, student):

        self.table.insert(
            "",
            "end",
            values=(
                student.code,
                student.name,
                student.courseworkTotal(),
                student.exam,
                round(student.percentage(), 2),
                student.grade()
            )
        )

    # Clear the table
    def clearTable(self):

        for item in self.table.get_children():
            self.table.delete(item)

    # Display all students
    def viewAll(self):

        self.clearTable()

        if len(self.students) == 0:
            self.summaryLabel.config(
                text="No student records available."
            )
            return

        totalPercentage = 0

        for student in self.students:
            self.displayStudent(student)
            totalPercentage += student.percentage()

        average = totalPercentage / len(self.students)

        self.summaryLabel.config(
            text="Total Students: " + str(len(self.students)) +
            " | Average Percentage: " + str(round(average, 2)) + "%"
        )

    # Find student using student code
    def findStudent(self, code):

        for student in self.students:

            if student.code == code:
                return student

        return None

    # View individual student
    def viewIndividual(self):

        code = simpledialog.askinteger(
            "Find Student",
            "Enter student code:"
        )

        if code is None:
            return

        student = self.findStudent(code)

        if student is None:
            messagebox.showerror(
                "Not Found",
                "Student not found."
            )
            return

        self.clearTable()
        self.displayStudent(student)

        self.summaryLabel.config(
            text="Individual student record: " + student.name
        )

    # Find student with highest score
    def highestStudent(self):

        if len(self.students) == 0:
            messagebox.showwarning("Warning", "No students available.")
            return

        highest = max(
            self.students,
            key=lambda student: student.percentage()
        )

        self.clearTable()
        self.displayStudent(highest)

        self.summaryLabel.config(
            text="Highest Scoring Student: " + highest.name
        )

    # Find student with lowest score
    def lowestStudent(self):

        if len(self.students) == 0:
            messagebox.showwarning("Warning", "No students available.")
            return

        lowest = min(
            self.students,
            key=lambda student: student.percentage()
        )

        self.clearTable()
        self.displayStudent(lowest)

        self.summaryLabel.config(
            text="Lowest Scoring Student: " + lowest.name
        )

    # Sort students in ascending order
    def sortAscending(self):

        self.students.sort(
            key=lambda student: student.percentage()
        )

        self.viewAll()

    # Sort students in descending order
    def sortDescending(self):

        self.students.sort(
            key=lambda student: student.percentage(),
            reverse=True
        )

        self.viewAll()

    # Validate a new or updated student mark
    def validMarks(self, course1, course2, course3, exam):

        if not all(
            0 <= mark <= 20
            for mark in [course1, course2, course3]
        ):
            return False

        if not 0 <= exam <= 100:
            return False

        return True

    # Add a new student
    def addStudent(self):

        code = simpledialog.askinteger(
            "Add Student",
            "Enter student code:"
        )

        if code is None:
            return

        if not 1000 <= code <= 9999:
            messagebox.showerror(
                "Invalid Code",
                "Student code must contain 4 digits."
            )
            return

        if self.findStudent(code) is not None:
            messagebox.showerror(
                "Duplicate Code",
                "This student code already exists."
            )
            return

        name = simpledialog.askstring(
            "Add Student",
            "Enter student name:"
        )

        if name is None:
            return

        name = name.strip()

        if name == "" or "," in name:
            messagebox.showerror(
                "Invalid Name",
                "Please enter a valid student name."
            )
            return

        course1 = simpledialog.askinteger(
            "Add Student", "Enter course 1 mark (0-20):"
        )

        if course1 is None:
            return

        course2 = simpledialog.askinteger(
            "Add Student", "Enter course 2 mark (0-20):"
        )

        if course2 is None:
            return

        course3 = simpledialog.askinteger(
            "Add Student", "Enter course 3 mark (0-20):"
        )

        if course3 is None:
            return

        exam = simpledialog.askinteger(
            "Add Student", "Enter examination mark (0-100):"
        )

        if exam is None:
            return

        if not self.validMarks(course1, course2, course3, exam):
            messagebox.showerror(
                "Invalid Marks",
                "Course marks must be 0-20 and exam must be 0-100."
            )
            return

        student = Student(
            code, name, course1, course2, course3, exam
        )

        self.students.append(student)

        self.saveStudents()
        self.viewAll()

        messagebox.showinfo(
            "Success",
            "Student added successfully."
        )

    # Delete a student
    def deleteStudent(self):

        code = simpledialog.askinteger(
            "Delete Student",
            "Enter student code to delete:"
        )

        if code is None:
            return

        student = self.findStudent(code)

        if student is None:
            messagebox.showerror(
                "Not Found",
                "Student not found."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Delete " + student.name + "?"
        )

        if confirm:
            self.students.remove(student)

            self.saveStudents()
            self.viewAll()

            messagebox.showinfo(
                "Success",
                "Student deleted successfully."
            )

    # Update student information
    def updateStudent(self):

        code = simpledialog.askinteger(
            "Update Student",
            "Enter student code to update:"
        )

        if code is None:
            return

        student = self.findStudent(code)

        if student is None:
            messagebox.showerror(
                "Not Found",
                "Student not found."
            )
            return

        name = simpledialog.askstring(
            "Update Student",
            "Enter new name:",
            initialvalue=student.name
        )

        if name is None:
            return

        name = name.strip()

        if name == "" or "," in name:
            messagebox.showerror(
                "Invalid Name",
                "Please enter a valid name."
            )
            return

        course1 = simpledialog.askinteger(
            "Update Student",
            "Enter course 1 mark:",
            initialvalue=student.course1,
            minvalue=0,
            maxvalue=20
        )

        if course1 is None:
            return

        course2 = simpledialog.askinteger(
            "Update Student",
            "Enter course 2 mark:",
            initialvalue=student.course2,
            minvalue=0,
            maxvalue=20
        )

        if course2 is None:
            return

        course3 = simpledialog.askinteger(
            "Update Student",
            "Enter course 3 mark:",
            initialvalue=student.course3,
            minvalue=0,
            maxvalue=20
        )

        if course3 is None:
            return

        exam = simpledialog.askinteger(
            "Update Student",
            "Enter examination mark:",
            initialvalue=student.exam,
            minvalue=0,
            maxvalue=100
        )

        if exam is None:
            return

        if not self.validMarks(course1, course2, course3, exam):
            messagebox.showerror(
                "Invalid Marks",
                "Please enter valid marks."
            )
            return

        student.name = name
        student.course1 = course1
        student.course2 = course2
        student.course3 = course3
        student.exam = exam

        self.saveStudents()
        self.viewAll()

        messagebox.showinfo(
            "Success",
            "Student record updated successfully."
        )


# Main program
root = tk.Tk()

app = StudentManager(root)

root.mainloop()
