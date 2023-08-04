from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

next_word = {}


def next_card():
    global next_word, flip_timer
    window.after_cancel(flip_timer)
    next_word = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=next_word["French"], fill="black")
    canvas.itemconfig(card_image, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=next_word["English"], fill="white")
    canvas.itemconfig(card_image, image=card_back_img)


def delete_card():
    to_learn.remove(next_word)
    print(len(to_learn))
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


window = Tk()
window.title("Flash Card")
window.config(padx=30, pady=30, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_image = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 260, text="", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)

no_img = PhotoImage(file="images/wrong.png")
no_btn = Button(image=no_img, highlightthickness=0, command=next_card)
no_btn.grid(row=1, column=0)
yes_img = PhotoImage(file="images/right.png")
yes_btn = Button(image=yes_img, highlightthickness=0, command=delete_card)
yes_btn.grid(row=1, column=1)

next_card()

window.mainloop()
