
import tkinter as tk
from tkinter import messagebox
import random


class MathsQuiz:

    def __init__(self, root):
        self.root = root
        self.root.title("Maths Quiz")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        self.score = 0
        self.questionNumber = 0
        self.attempts = 0
        self.correctAnswer = 0

        self.minimum = 1
        self.maximum = 9

        self.displayMenu()

    # Display difficulty menu
    def displayMenu(self):
        self.clearWindow()

        title = tk.Label(
            self.root,
            text="MATHS QUIZ",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=20)

        menuLabel = tk.Label(
            self.root,
            text="DIFFICULTY LEVEL",
            font=("Arial", 14)
        )
        menuLabel.pack(pady=10)

        easyButton = tk.Button(
            self.root,
            text="1. Easy",
            width=20,
            command=lambda: self.startQuiz(1, 9)
        )
        easyButton.pack(pady=5)

        moderateButton = tk.Button(
            self.root,
            text="2. Moderate",
            width=20,
            command=lambda: self.startQuiz(10, 99)
        )
        moderateButton.pack(pady=5)

        advancedButton = tk.Button(
            self.root,
            text="3. Advanced",
            width=20,
            command=lambda: self.startQuiz(1000, 9999)
        )
        advancedButton.pack(pady=5)

    # Generate a random integer
    def randomInt(self, minimum, maximum):
        return random.randint(minimum, maximum)

    # Randomly decide the operation
    def decideOperation(self):
        operation = random.choice(["+", "-"])
        return operation

    # Start the quiz
    def startQuiz(self, minimum, maximum):
        self.minimum = minimum
        self.maximum = maximum

        self.score = 0
        self.questionNumber = 0

        self.clearWindow()
        self.displayProblem()

    # Display a question
    def displayProblem(self):
        self.clearWindow()

        if self.questionNumber == 10:
            self.displayResults()
            return

        self.attempts = 0

        self.number1 = self.randomInt(
            self.minimum, self.maximum
        )

        self.number2 = self.randomInt(
            self.minimum, self.maximum
        )

        self.operation = self.decideOperation()

        if self.operation == "+":
            self.correctAnswer = self.number1 + self.number2
        else:
            self.correctAnswer = self.number1 - self.number2

        questionLabel = tk.Label(
            self.root,
            text="Question " + str(self.questionNumber + 1) + " / 10",
            font=("Arial", 14)
        )
        questionLabel.pack(pady=15)

        scoreLabel = tk.Label(
            self.root,
            text="Score: " + str(self.score),
            font=("Arial", 12)
        )
        scoreLabel.pack()

        self.problemLabel = tk.Label(
            self.root,
            text=str(self.number1) + " " +
            self.operation + " " +
            str(self.number2) + " = ?",
            font=("Arial", 24, "bold")
        )
        self.problemLabel.pack(pady=20)

        self.answerEntry = tk.Entry(
            self.root,
            font=("Arial", 16),
            justify="center"
        )
        self.answerEntry.pack(pady=10)

        self.submitButton = tk.Button(
            self.root,
            text="Submit Answer",
            command=self.checkAnswer
        )
        self.submitButton.pack(pady=10)

        self.feedbackLabel = tk.Label(
            self.root,
            text="",
            font=("Arial", 12)
        )
        self.feedbackLabel.pack(pady=5)

    # Check whether the answer is correct
    def isCorrect(self, answer, correctAnswer):
        return answer == correctAnswer

    # Check the user's answer
    def checkAnswer(self):
        userInput = self.answerEntry.get()

        if userInput == "":
            messagebox.showwarning(
                "Missing Answer",
                "Please enter your answer."
            )
            return

        try:
            userAnswer = int(userInput)
        except ValueError:
            messagebox.showerror(
                "Invalid Answer",
                "Please enter a whole number."
            )
            return

        self.attempts += 1

        if self.isCorrect(userAnswer, self.correctAnswer):

            if self.attempts == 1:
                self.score += 10
                message = "Correct! You earned 10 points."
            else:
                self.score += 5
                message = "Correct on your second attempt! You earned 5 points."

            self.feedbackLabel.config(text=message)

            self.questionNumber += 1

            self.root.after(1200, self.displayProblem)

        else:

            if self.attempts == 1:
                self.feedbackLabel.config(
                    text="Incorrect! Try one more time."
                )

                self.answerEntry.delete(0, tk.END)

            else:
                self.feedbackLabel.config(
                    text="Incorrect! The answer was "
                    + str(self.correctAnswer)
                )

                self.questionNumber += 1

                self.root.after(1800, self.displayProblem)

    # Display final score and grade
    def displayResults(self):
        self.clearWindow()

        titleLabel = tk.Label(
            self.root,
            text="QUIZ RESULTS",
            font=("Arial", 20, "bold")
        )
        titleLabel.pack(pady=20)

        resultLabel = tk.Label(
            self.root,
            text="Your Score: " + str(self.score) + " / 100",
            font=("Arial", 16)
        )
        resultLabel.pack(pady=10)

        if self.score >= 90:
            grade = "A+"
        elif self.score >= 80:
            grade = "A"
        elif self.score >= 70:
            grade = "B"
        elif self.score >= 60:
            grade = "C"
        elif self.score >= 50:
            grade = "D"
        else:
            grade = "F"

        gradeLabel = tk.Label(
            self.root,
            text="Your Grade: " + grade,
            font=("Arial", 16)
        )
        gradeLabel.pack(pady=10)

        replayLabel = tk.Label(
            self.root,
            text="Would you like to play again?",
            font=("Arial", 12)
        )
        replayLabel.pack(pady=15)

        replayButton = tk.Button(
            self.root,
            text="Play Again",
            command=self.displayMenu
        )
        replayButton.pack(pady=5)

        quitButton = tk.Button(
            self.root,
            text="Quit",
            command=self.root.destroy
        )
        quitButton.pack(pady=5)

    # Clear the window
    def clearWindow(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# Main program
root = tk.Tk()
quiz = MathsQuiz(root)
root.mainloop()
