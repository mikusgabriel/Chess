from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk



root = Tk()
frm = ttk.Frame(root, padding=100)
frm.grid()
counter=0

chess_image = Image.open("./assets/Chess_bdt60.png")
chess_image2 = Image.open("./assets/Chess_kdt60.png")
chess_photo = ImageTk.PhotoImage(chess_image)
chess_photo2 = ImageTk.PhotoImage(chess_image2)

for x in range (0,8):
    counter+=1
    for y in range (0,8):
        counter+=1
        if counter%2==0:
            ttk.Label(frm, image=chess_photo, background="#C19A6B" ,padding=10).grid(column=x, row=y)
        else:
            ttk.Label(frm, image=chess_photo2, background="#342214" ,padding=10).grid(column=x, row=y)

          

            

root.mainloop()
