import tkinter as tk

import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["PyChat"]
message_col = db["messages"]

root = tk.Tk()
root.title("Hangman")

myLabel1 = tk.Label(root, text="This is Hangman game:\n please enter a letter that you guess", justify="center")
myLabel1.grid(row=0, column=0, columnspan=6, pady=30, padx=50)

# -------------------------------------------------------

# Create an input field
entry = tk.Entry(root, width=60, justify="center")
entry.grid(row=1, column=0, columnspan=6, pady=5)



root.mainloop()
