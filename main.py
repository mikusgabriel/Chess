from tkinter import *
from PIL import Image, ImageTk
import pieces



root = Tk()
frm = Frame(root, padx=100,pady=100)
frm.grid()

team1_pieces = [[ pieces.Pawn("white",i) for i in range(0,8)],pieces.Rook("white",0),pieces.Rook("white",7),pieces.Bishop("white",2),pieces.Bishop("white",5),pieces.Knight("white",1),pieces.Knight("white",6),pieces.King("white",4),pieces.Queen("white",3)]
team1_deadpieces=[]
team2_pieces = [[ pieces.Pawn("black",i) for i in range(0,8)],pieces.Rook("black",0),pieces.Rook("black",7),pieces.Bishop("black",2),pieces.Bishop("black",5),pieces.Knight("black",1),pieces.Knight("black",6),pieces.King("black",4),pieces.Queen("black",3)]
team2_deadpieces = []


#generate a hash with the initial chess pieces
def generate_chessboard_Hash():
    chessboard_hash = {}
    columns=range(0,8)
    rows = range(0, 8)
    
    for column in columns:
        for row in rows:
            x = column
            y = row
            coordinate = str(x)+str(y)  #coordinate instead A1->00 ,  B2-> 11
            chessboard_hash[coordinate] = None
    return chessboard_hash
    
def init_chessboard(chessboard_hash):
    team1_pieces.append(team1_deadpieces)
    team1_deadpieces.clear()
    team2_pieces.append(team2_deadpieces)
    team2_deadpieces.clear()
    
    #Basically comment ca fonctionne c<est que les pions cest une liste donc si cest une liste je fais uune autre boucle for si ce nest pas pion je ne fais aps de boucle for aussi simple que ca
    for piece in team1_pieces:
        if isinstance(piece, list):
            for sub_piece in piece:
                chessboard_hash[str(sub_piece.init_x) + str(sub_piece.init_y)] = sub_piece
        else:
            chessboard_hash[str(piece.init_x) + str(piece.init_y)] = piece
            
    for piece in team2_pieces:
        if isinstance(piece, list):
            for sub_piece in piece:
                chessboard_hash[str(sub_piece.init_x) + str(sub_piece.init_y)] = sub_piece
        else:
            chessboard_hash[str(piece.init_x) + str(piece.init_y)] = piece


blank = Image.open("./assets/blank.png")
blank_image = ImageTk.PhotoImage(blank)





chessboard=generate_chessboard_Hash()
init_chessboard(chessboard)
print(chessboard)

#Column de 1 a 8
for i in range(8, 0, -1):
    Label(frm, text=str(i), font="BOLD", padx=5, pady=5).grid(column=0, row=8-i)

#Row de A a H
for i, letter in enumerate("ABCDEFGH"):
    Label(frm, text=letter, font="BOLD", padx=5, pady=5).grid(column=i+1, row=8)


#UPDATE DE CHESSBOARD     ----JE DOIS LE METTRE DANS UNE FONCTION ET CALL CA TOUT LES MOVES YK

for x in range (0,8):
    for y in range (7, -1, -1):
        color = "#342214" if (x + y) % 2 == 0 else "#C19A6B"
        if  chessboard[str(x)+str(y)]!=None:
            piece=chessboard[str(x)+str(y)]
            Label(frm,image=piece.chess_photo, background=color ,padx=10,pady=10).grid(column=x+1, row=7-y)
            
        else:
            Label(frm,image=blank_image, background=color,padx=10,pady=10).grid(column=x+1, row=7-y)
        
#SOIS BOUGER EN CLICKANT SOIT EN DRAG
          

root.mainloop()
