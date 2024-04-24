from tkinter import *
from PIL import Image, ImageTk
import pieces



root = Tk()

frm = Frame(root, padx=100, pady=100)
frm.grid()
button_label = Label(frm, padx=10, pady=10)
button_label.grid(row=1)
chess_canvas = Canvas(frm, width=560, height=560,
                      bg="#C19A6B", highlightthickness=0)
chess_canvas.grid(row=2)


#ONLY USED TO INIT
white_pieces_list = [[ pieces.Pawn("white",i) for i in range(0,8)],pieces.Rook("white",0),pieces.Rook("white",7),pieces.Bishop("white",2),pieces.Bishop("white",5),pieces.Knight("white",1),pieces.Knight("white",6),pieces.King("white",4),pieces.Queen("white",3)]
white_deadpieces_list = []
black_pieces_list = [[pieces.Pawn("black", i) for i in range(0, 8)], pieces.Rook("black", 0), pieces.Rook("black", 7), pieces.Bishop(
    "black", 2), pieces.Bishop("black", 5), pieces.Knight("black", 1), pieces.Knight("black", 6), pieces.King("black", 4), pieces.Queen("black", 3)]
black_deadpieces_list = []


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
 
 # generate a hash with the initial chess pieces for each team with their actual coordinates
def generate_team_Hash(team):  
    team_hash= {}
    
    ##mieux le faire jsp comment
    
    if team=="white":
    
        for piece in white_pieces_list:
            if isinstance(piece, list):
                for sub_piece in piece:
                    team_hash[sub_piece] = str(
                        sub_piece.init_x) + str(sub_piece.init_y)
            else:
                team_hash[piece] = str(piece.init_x) + str(piece.init_y)
    else:
        for piece in black_pieces_list:
            if isinstance(piece, list):
                for sub_piece in piece:
                    team_hash[sub_piece] = str(
                        sub_piece.init_x) + str(sub_piece.init_y)
            else:
                team_hash[piece] = str(piece.init_x) + str(piece.init_y)
               
    return team_hash
    

white_pieces_hash = {}
black_pieces_hash = {}

#initializes the chessboard hash with all the pieces
def init_chessboard(chessboard_hash):
    global white_pieces_hash
    global black_pieces_hash
    white_pieces_hash = generate_team_Hash("white")
    white_deadpieces_list.clear()
    black_pieces_hash=generate_team_Hash("black")

    black_deadpieces_list.clear()
    
    #Basically comment ca fonctionne c<est que les pions cest une liste donc si cest une liste je fais uune autre boucle for si ce nest pas pion je ne fais aps de boucle for aussi simple que ca
    for piece in white_pieces_hash:
        if isinstance(piece, list):
            for sub_piece in piece:
                chessboard_hash[str(sub_piece.init_x) + str(sub_piece.init_y)] = sub_piece
        else:
            chessboard_hash[str(piece.init_x) + str(piece.init_y)] = piece
            
    for piece in black_pieces_hash:
        if isinstance(piece, list):
            for sub_piece in piece:
                chessboard_hash[str(sub_piece.init_x) + str(sub_piece.init_y)] = sub_piece
        else:
            chessboard_hash[str(piece.init_x) + str(piece.init_y)] = piece
         
#puts Coordinate (key) = None (key) and then update the chessboard_hash
def removepiece(piece: pieces.Pieces):
    if piece is not None:
        if (piece.getTeam() == "white"):
            white_pieces_hash[piece] = None

        else:
            black_pieces_hash[piece] = None
        update_chessboard()
       

blank = Image.open("./assets/blank.png")
blank_image = ImageTk.PhotoImage(blank)





chessboard=generate_chessboard_Hash()
init_chessboard(chessboard)


#clears the chessboard with none for all values (keys are coordinates), then places the peices that have coordinates on the chessboard matching the key from chessboard and pieces value's
def update_chessboard():
    global chessboard
    for key in chessboard.keys():
        chessboard[key]=None
    for piece in white_pieces_hash:
        if isinstance(piece, list):
            for sub_piece in piece:
                chessboard[str(sub_piece.init_x) +
                                str(sub_piece.init_y)] = sub_piece
        else:
            if white_pieces_hash[piece]!=None:
                chessboard[str(piece.init_x) + str(piece.init_y)] = piece

    for piece in black_pieces_hash:
        if isinstance(piece, list):
            for sub_piece in piece:
                chessboard[str(sub_piece.init_x) +
                                str(sub_piece.init_y)] = sub_piece
        else:
            if black_pieces_hash[piece] != None:
                chessboard[str(piece.init_x) + str(piece.init_y)] = piece

##game loop recursive
def update():
    update_board_ui()
    frm.after(100, update)




def update_board_ui():

    chess_canvas.delete("all")
    cell_size = 70  # Adjust this value as needed

    # Draw the cells
    for x in range(8):
        for y in range(8):
            color = "#C19A6B" if (x + y) % 2 == 0 else "#342214"  
            chess_canvas.create_rectangle(
                x * cell_size, y *
                cell_size, (x + 1) * cell_size, (y + 1) * cell_size,
                fill=color, outline="")

            # Draw the pieces
            piece = chessboard[str(x) + str(7-y)]
            if piece:
                image = piece.chess_photo
                chess_canvas.create_image(
                    x * cell_size + cell_size // 2, y * cell_size + cell_size // 2,
                    image=image)

    # Column labels
    for i, letter in enumerate("ABCDEFGH"):
        chess_canvas.create_text(
            i * cell_size + cell_size // 2, 8 * cell_size + cell_size // 2,
            text=letter, font=("BOLD", 12))

    # Row labels
    for i in range(8):
        chess_canvas.create_text(
            8 * cell_size + cell_size // 2, i * cell_size + cell_size // 2,
            text=str(8 - i), font=("BOLD", 12))

win=False
def set_win(value):
    global win
    global text
    win = value
    text= "game won"
    win_label.config(text=text)

##quand une piece mange un autre
spawn_window_button = Button(button_label,
                             text="Delete",
                             command=lambda: removepiece(chessboard["07"])).grid(column=0, row=0)

##Quand le roi est math 
spawn_window_button_win = Button(button_label,
                             text="Win",
                             command=lambda: set_win(True)).grid(column=1, row=0)


win_label= Label(button_label,text="Playing")
win_label.grid(column=2, row=0)


    





##commence la partie
update()
root.mainloop()



##click on a piece and shows with dots all the legal moves and being able to click there u wanna go and mvoes the piece

##make turns and write whose turn is it

