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

# -------------------------------------------------------

# Create an input field
entry = tk.Entry(root, width=60, justify="center")
entry.grid(row=1, column=0, columnspan=6, pady=5)

# -------------------------------------------------------

word_list = ["apple", "banana", "cherry", "grape", "orange", "strawberry", "elephant", "giraffe", "tiger"]
random_word = random.choice(word_list)
word_length = len(random_word)
empty_word = ["_"] * word_length
print(random_word)

message_label = tk.Label(root, text="", font=("Arial", 12), fg="black")
message_label.grid(row=3, column=0, columnspan=6, pady=10)

word_display = tk.Label(root, text=" ".join(empty_word), font=("Arial", 12))
word_display.grid(row=4, column=0, columnspan=6, pady=10)

def send_letter():
    input_letter = entry.get().lower()
    message_col.insert_one({"text": input_letter})
    print(random_word)  # just for guiding in terminal to save time for coding
    entry.delete(0, tk.END)
    message_col.insert_one({"text": input_letter})

    if len(input_letter) != 1 or not input_letter.isalpha():
        message_label.config(text="Please type a single letter!", fg="orange")
        return

    if input_letter in random_word:

        for i, letter in enumerate(random_word):
            if letter == input_letter:
                empty_word[i] = letter # Replace the correct letter
        message_label.config(text="Correct guess!", fg="blue")
    else:
        message_label.config(text="Wrong guess!", fg="red")

    word_display.config(text=" ".join(empty_word))

    if "_" not in empty_word:
        message_label.config(text="You won!", fg="green")


send_button = tk.Button(root, text="Send", height=2, width=10, command=send_letter)
send_button.grid(row=2, column=0, pady=5, padx=3)

root.mainloop()