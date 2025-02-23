import tkinter as tk

import pymongo
import random
import string

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["Hangman"]
message_col = db["messages"]

root = tk.Tk()
root.title("Hangman")

myLabel1 = tk.Label(root, text="This is Hangman game:\n please enter a letter that you guess", justify="center")
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

# -------------------------------------------------------
#Alphabet letters
alphabet_letters = string.ascii_lowercase

def send_letter():
    global empty_word

    #Create an input field
    input_letter = entry.get().lower()
    message_col.insert_one({"text": input_letter})
    print(random_word)  # just for guiding to save time for coding
    entry.delete(0, tk.END)

    #if the letter is more than one letter or is not alphabet
    if len(input_letter) > 1 or not input_letter.isalpha():
        message = tk.Label(root, text="Please type a single letter")
        message.grid(row=5, column=5, pady=10)
        return

    correct_guess = False

    ## Check all letters
    for c, letter in enumerate(random_word):

        if input_letter == letter:
            empty_word[c] = letter # Replace the correct letter
            correct_guess = True

        # Display updated word
        myLabel3 = tk.Label(root, text=" ".join(empty_word), font=("Arial", 12))
        myLabel3.grid(row=5, column=0, columnspan=6, pady=10)

        if correct_guess:
            message = tk.Label(root, text="Correct guess", fg="green")
        else:
            message = tk.Label(root, text="Wrong guess", fg="red")
        message.grid(row=5, column=5, pady=10)

        # Check if user win
        if "_" not in empty_word:
            win_message = tk.Label(root, text="You won!", fg="blue", font=("Arial", 14))
            win_message.grid(row=6, column=0, columnspan=6, pady=10)


messages_label = tk.Label(root, text="Messages:\n", justify="left")
messages_label.grid()

send_button = tk.Button(root, text="send", height=2, width=5, command=send_letter)
send_button.grid(pady=5, padx=3)

root.mainloop()

