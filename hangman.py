import tkinter as tk
import pymongo
import random

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["PyChat"]
message_col = db["messages"]

try:
    client.admin.command('ping')
    print("MongoDB connection successful!")
except Exception as e:
    print("MongoDB connection failed:", e)

root = tk.Tk()
root.title("Hangman game")

myLabel1 = tk.Label(root, text="This is Hangman game:\nPlease enter a letter that you guess", justify="center")
myLabel1.grid(row=0, column=0, columnspan=6, pady=30, padx=50)

entry = tk.Entry(root, width=60, justify="center")
entry.grid(row=1, column=0, columnspan=6, pady=5)

word_categories = {"animals": ["lion", "elephant", "tiger", "giraffe", "wolf", "penguin", "eagle"],
                   "fruits_vegetables": ["apple", "orange", "watermelon", "banana", "carrot", "pineapple", "cucumber"],
                   "countries": ["sweden", "france", "canada", "japan", "germany", "brazil", "italy"],
                   "colors": ["red", "blue", "green", "yellow", "purple", "black", "white"],
                   "professions": ["doctor", "engineer", "teacher", "artist", "pilot", "chef", "firefighter"],
                   "sports": ["football", "basketball", "tennis", "volleyball", "baseball", "cricket", "hockey"],
                   "technology": ["computer", "internet", "software", "database", "python", "javascript", "algorithm"]
                   }

random_category = random.choice(list(word_categories.keys()))
random_word = random.choice(word_categories[random_category])

word_length = len(random_word)
empty_word = ["_"] * word_length
print(random_word)
message_label = tk.Label(root, text="", font=("Arial", 14), fg="black")
message_label.grid(row=3, column=0, columnspan=6, pady=10)

word_display = tk.Label(root, text=" ".join(empty_word), font=("MV Boli", 16), fg="Purple")
word_display.grid(row=5, column=0, columnspan=6, pady=10)

category_label = tk.Label(root, text="Category: " + random_category, font=("MV Boli", 16), fg="Purple")
category_label.grid(row=4, column=0, columnspan=6, pady=30, padx=50)


# Hangman Canvas
canvas = tk.Canvas(root, width=200, height=250)
canvas.grid(row=6, column=0, columnspan=6, pady=20)

# Draw Hangman Base
canvas.create_line(50, 200, 150, 200, width=3) # Base
canvas.create_line(100, 200, 100, 50, width=3) # Pole
canvas.create_line(100, 50, 150, 50, width=3) # Top Bar
canvas.create_line(150, 50, 150, 70, width=3) # Rope

# Hangman parts
hangman_parts = [
    canvas.create_oval(135, 70, 165, 100, width=3, state='hidden'), # Head
    canvas.create_line(150, 100, 150, 150, width=3, state='hidden'), # Body
    canvas.create_line(150, 110, 130, 130, width=3, state='hidden'), # Left Arm
    canvas.create_line(150, 110, 170, 130, width=3, state='hidden'), # Right Arm
    canvas.create_line(150, 150, 130, 180, width=3, state='hidden'), # Left Leg
    canvas.create_line(150, 150, 170, 180, width=3, state='hidden') # Right Leg
]

wrong_guesses = 0

def send_letter():
    global wrong_guesses
    input_letter = entry.get().lower()
    entry.delete(0, tk.END)  # Clear entry field
    message_col.insert_one({"text": input_letter})  # Save to database

    if len(input_letter) != 1 or not input_letter.isalpha():
        message_label.config(text="Please type a single letter!", fg="gray")
        return

    if input_letter in random_word:
        for i, letter in enumerate(random_word):
            if letter == input_letter:
                empty_word[i] = letter
        message_label.config(text="Correct guess!", fg="gray")
    else:
        wrong_guesses += 1
        message_label.config(text="Wrong guess!", fg="gray")

        if wrong_guesses <= 6:
            canvas.itemconfig(hangman_parts[wrong_guesses - 1], state='normal')

    word_display.config(text=" ".join(empty_word))

    if "_" not in empty_word:
        message_label.config(text="You won!", fg="gray")

    if wrong_guesses == 6:
        message_label.config(text=f"Game Over! The word was '{random_word}'", fg="black")

send_button = tk.Button(root, text="Send", height=2, width=10, command=send_letter)
send_button.grid(row=2, column=0, pady=5, padx=3)

root.mainloop()