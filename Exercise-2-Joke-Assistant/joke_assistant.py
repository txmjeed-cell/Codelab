
import tkinter as tk
from tkinter import messagebox
import random


# Store the selected joke's punchline
currentPunchline = ""


# Read jokes from the text file
def loadJokes():
    jokes = []

    try:
        file = open("randomJokes.txt", "r")

        for line in file:
            line = line.strip()

            if line != "":
                jokes.append(line)

        file.close()

    except FileNotFoundError:
        messagebox.showerror(
            "File Error",
            "randomJokes.txt was not found."
        )

    return jokes


# Select and display a random joke
def tellJoke():
    global currentPunchline

    if len(jokes) == 0:
        messagebox.showwarning(
            "No Jokes",
            "There are no jokes available."
        )
        return

    selectedJoke = random.choice(jokes)

    # Remove the dash at the beginning if present
    if selectedJoke.startswith("-"):
        selectedJoke = selectedJoke[1:].strip()

    # Separate the setup and punchline
    if "?" in selectedJoke:
        setup, currentPunchline = selectedJoke.split("?", 1)

        setupLabel.config(
            text=setup.strip() + "?"
        )

        punchlineLabel.config(text="")

    else:
        setupLabel.config(
            text="This joke has an invalid format."
        )

        currentPunchline = ""


# Display the punchline
def showPunchline():
    if currentPunchline != "":
        punchlineLabel.config(
            text=currentPunchline.strip()
        )
    else:
        messagebox.showinfo(
            "No Punchline",
            "Please select a joke first."
        )


# Select another joke
def nextJoke():
    tellJoke()


# Close the application
def quitApp():
    root.destroy()


# Load jokes from the file
jokes = loadJokes()


# Create the main window
root = tk.Tk()
root.title("Alexa Tell Me a Joke")
root.geometry("550x400")
root.resizable(False, False)


# Application title
titleLabel = tk.Label(
    root,
    text="Alexa Tell Me a Joke",
    font=("Arial", 20, "bold")
)
titleLabel.pack(pady=20)


# Joke setup
setupLabel = tk.Label(
    root,
    text="Click the button to hear a joke!",
    font=("Arial", 14),
    wraplength=450
)
setupLabel.pack(pady=20)


# Punchline
punchlineLabel = tk.Label(
    root,
    text="",
    font=("Arial", 14, "italic"),
    wraplength=450
)
punchlineLabel.pack(pady=15)


# Tell a joke button
tellButton = tk.Button(
    root,
    text="Alexa tell me a Joke",
    width=25,
    command=tellJoke
)
tellButton.pack(pady=5)


# Show punchline button
punchlineButton = tk.Button(
    root,
    text="Show Punchline",
    width=25,
    command=showPunchline
)
punchlineButton.pack(pady=5)


# Next joke button
nextButton = tk.Button(
    root,
    text="Next Joke",
    width=25,
    command=nextJoke
)
nextButton.pack(pady=5)


# Quit button
quitButton = tk.Button(
    root,
    text="Quit",
    width=25,
    command=quitApp
)
quitButton.pack(pady=5)


# Start the application
root.mainloop()
