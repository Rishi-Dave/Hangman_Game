#importing libraries
import requests
import random
from tkinter import *
from PIL import ImageTk, Image

#getting words from https://www.mit.edu/~ecprice/wordlist.10000, 
# This is a file with a large list of words
word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

#gets the words from the site in a variable
word_list = requests.get(word_site)
#creates a list from the words on the wesbite
words = word_list.content.splitlines()

#reshapes words to only contain words with between 4 and 6 letters
i = 0
while i < (len(words)):
    if i<0:
        i = 0
    if len(words[i])<4 or len(words[i])>6:
        words.remove(words[i])
        i-= 1
    i+=1
#tkinter loading
app = Tk()
app.title("Hangman Game")
app.geometry('600x600')



#hangman images used from https://commons.wikimedia.org
hang0 = Image.open("hangmanImg/Hangman-0.png")
img0 = ImageTk.PhotoImage(hang0)
hang1 = Image.open("hangmanImg/Hangman-1.png")
img1 = ImageTk.PhotoImage(hang1)
hang2 = Image.open("hangmanImg/Hangman-2.png")
img2 = ImageTk.PhotoImage(hang2)
hang3 = Image.open("hangmanImg/Hangman-3.png")
img3 = ImageTk.PhotoImage(hang3)
hang4 = Image.open("hangmanImg/Hangman-4.png")
img4 = ImageTk.PhotoImage(hang4)
hang5 = Image.open("hangmanImg/Hangman-5.png")
img5 = ImageTk.PhotoImage(hang5)
hang6 = Image.open("hangmanImg/Hangman-6.png")
img6 = ImageTk.PhotoImage(hang6)
hang7 = Image.open("hangmanImg/Hangman-7.png")
img7 = ImageTk.PhotoImage(hang7)
hang8 = Image.open("hangmanImg/Hangman-8.png")
img8 = ImageTk.PhotoImage(hang8)
hang9 = Image.open("hangmanImg/Hangman-9.png")
img9 = ImageTk.PhotoImage(hang9)
imgs = [img0, img1, img2, img3, img4, img5, img6, img7, img8, img9]

#variables that I will use
incorrect_inputs = 0 #number of times you guess wrong
hangman_img = Label(app, image=imgs[incorrect_inputs]) #shows the hangman depending on the number of wrong guesses
hiddenText = [] #shows the amount of hidden letters left
label2 = Label(app, text = hiddenText, font=("Arial", 25)) #displays messages
letters = [["a", "b", "c", "d"], ["e", "f", "g", "h"], ["i", "j", "k", "l"], ["m", "n", "o", "p"], ["q", "r", "s", "t"], ["u", "v", "w", "x"], ["y", "z"]] #list of letters
board = [[],[],[],[],[],[],[]] #list of buttons(to be filled later)
word = "" #word to guess
#abstraction for a button to make initializing them easier
#button class inspired by buttons class in tiktactoe game on https://www.codespeedy.com/tic-tac-toe-gui-in-python-using-tkinter/
def button(frame, text):
    b = Button(frame, state = NORMAL, text = text, width = 25, height = 25, bg = "white", relief = GROOVE, bd = 5, font=('Arial', 25))
    return b
#function that choosing a random word from list
def chooseWord():
    global hiddenText
    global word
    word = str(words[random.randint(0, len(words))])
    word = word.replace("b'", "")
    word = word.replace("'", "")
    for i in word:
        hiddenText.append("_ ")
    label2["text"] = "".join(hiddenText)
#resets the game and chooses a new word
def reset():
    global hiddenText
    global incorrect_inputs
    for i in range(0,7):
        for j in range(0,len(letters[i])):
            board[i].append(button(app, letters[i][j]))
            board[i][j].config(state = NORMAL)
    hiddenText = []
    incorrect_inputs = 0
    hangman_img["image"] = imgs[incorrect_inputs]
    label3["text"] = ""
    chooseWord()
#checks if the letter guessed is in the word
#if it is, then show where it is in string hidden word, if all letters are found then you win
#if not, then increase the amount of body parts of the hangman, if all parts are shown then you lose
def guess(row, col):
    global hiddenText
    global incorrect_inputs
    board[row][col].config(state = DISABLED, disabledforeground= "black")
    if board[row][col]["text"] not in word:
        incorrect_inputs += 1
        hangman_img["image"] = imgs[incorrect_inputs]
    else:
        for i in range(len(word)):
            if board[row][col]["text"] == word[i]:
                hiddenText[i] = word[i]
            
    label2["text"] = "".join(hiddenText)
    checkWinLoss()
def checkWinLoss():
    if word == label2["text"]:
        for i in range(0,7):
            for j in range(0,len(letters[i])):
                board[i][j].config(state = DISABLED, disabledforeground= "black")
        label3["text"] = "You win good job!"
    if incorrect_inputs == 9:
        for i in range(0,7):
            for j in range(0,len(letters[i])):
                board[i][j].config(state = DISABLED, disabledforeground= "black")
        label3["text"] = "You lose!"
        label2["text"] = word
#button to reset(play another game with a different word)
paB = button(app, "Play Again")
paB.config(command = reset, width = 150, font = 50)
#setting positions of the objects
paB.grid(row = 6, column = 0)
hangman_img.grid(row = 0, column = 0)
label3 = Label(app)
label3.grid(row = 7, column = 0)
chooseWord()
label2.grid(row = 1, column = 0)

#loop to set the letter buttons in list board and assign them with the command guess
#loop to display buttons from tiktactoe game by https://www.codespeedy.com/tic-tac-toe-gui-in-python-using-tkinter/
for i in range(0,7):
    app.rowconfigure(i +2, weight=1)
    for j in range(0,len(letters[i])):
        app.columnconfigure(j+2, weight=1)
        board[i].append(button(app, letters[i][j]))
        board[i][j].config(command= lambda row=i,col=j:guess(row,col))
        board[i][j].grid(row = i +2, column = j+2, sticky = 'news')
app.mainloop()