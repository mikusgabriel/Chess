from tkinter import *
from PIL import Image, ImageTk
import pieces
import numpy as np



root = Tk()

frm = Frame(root, padx=100, pady=100)
frm.grid()
button_label = Label(frm, padx=10, pady=10)
button_label.grid(row=1)
chess_canvas = Canvas(frm, width=560, height=560,
                      bg="#C19A6B", highlightthickness=0)
chess_canvas.grid(row=2)


def getCellfromCoord(x, y):
    number_cellx = str(int(np.floor(x/cell_size)))
    number_celly = str(int(7-np.floor(y/cell_size)))
    return (number_cellx+number_celly)


def getCordfromCell(cell):
    if cell[0]== '-':
        return (-1,-1)
    elif len(cell)==2:
        x = (int(cell[0])*cell_size) +cell_size/2
        y = 7*cell_size-(int(cell[1])*cell_size) + cell_size/2
    else:
        x = cell_size/2
        y = 7*cell_size-(int(cell[0])*cell_size) + cell_size/2
        
    return (x,y)

#you get the cell coordinate from click then based on the cell you setSelect the piece on the cell and you deselect the last piece using pass_selected (you store the last cell)
#just need to add que tu peux juste selectionner les joueur de ta team
last_cell=None
current_team="white"
played=False

def move(event):
    global last_cell
    
    cell=getCellfromCoord(event.x, event.y)
    if isinstance(chessboard[cell],pieces.Pieces):
        if current_team != chessboard[cell].team:
            print("youhou")
            return False
    selected_piece = chessboard[last_cell] if last_cell is not None else None
    clicked_piece = chessboard[cell]
    
    # If a piece is already selected
    if selected_piece is not None:
        if isinstance(clicked_piece, pieces.Pieces):
            if isinstance(selected_piece, pieces.Pieces):
                print(f"Selected team:{selected_piece.team} --- Clicked Team:{clicked_piece.team} ---- is targeted?? {clicked_piece.isTargeted}")
                if selected_piece.team != clicked_piece.team and clicked_piece.isTargeted:
                    print("wallahi")
                    # If the clicked piece belongs to the opposing team, capture it
                    clicked_piece.setDead(True)
                    selected_piece.setSelected(False)
                    chessboard[cell] = selected_piece
                    chessboard[last_cell] = None
                    removeAllTargeted()
                    switchTeam()

                            
                elif selected_piece != clicked_piece and selected_piece.team == clicked_piece.team:
                    print("same")
                    # If the clicked piece belongs to the same team but is different,
                    # switch selection to the new piece
                    selected_piece.setSelected(False)
                    clicked_piece.setSelected(True)
                    last_cell = cell

                    
                elif selected_piece == clicked_piece:
                    # If the clicked piece is the same one
                    selected_piece.setSelected(False)
                    removeAllTargeted()
                    last_cell=None
            
                    
              

                    
                    
                  
        else:
            if isMoveValid(chessboard[last_cell],last_cell,cell):
                chessboard[cell] = chessboard[last_cell]
                chessboard[last_cell] = None
                last_cell = cell
                if isinstance(selected_piece, pieces.Pawn):
                    selected_piece.setFirstMove()
                selected_piece.setSelected(False)
                removeAllTargeted()
                switchTeam()

    
    else:
        if isinstance(clicked_piece, pieces.Pieces):
            # Deselect the last selected piece if a new piece is clicked
            selected_piece=chessboard[cell]
            selected_piece.setSelected(True)
            last_cell = cell
        
    
def switchTeam():
    global current_team
    global last_cell
    
    if current_team == "white":
        current_team = "black"
    else:
        current_team = "white"
    last_cell=None
    print(current_team)
    set_turn(current_team)


##COMPLETE CETTE FUNCTION QUI CHECK SI UNE RECOMMENDATION EST VALIDE DANS LE CHESSBOARD(SI A LEXTERIEUR DU CHESSBOARD SUR UNE PIECE)
#HAVE TO FIX
def isMoveRecommendationValid(piece,recommendedMove,cell):
    
    recommendation = ""
    if piece.team == "white":
        recommendation = str(int(cell) + recommendedMove)
    else:
        recommendation = str(int(cell) - recommendedMove)
    if len(recommendation) < 2:
        recommendation = f"0{recommendation}"

    # Get the coordinates of the target cell
    cord = getCordfromCell(recommendation)

    # Get the canvas dimensions
    canvas_width = chess_canvas.winfo_width()
    canvas_height = chess_canvas.winfo_height()
    
   

    # Check if the target cell coordinates are within the canvas bounds
    if cord[0] < 0 or cord[0] > canvas_width or cord[1] < 0 or cord[1] > canvas_height:
        return False

                
    if chessboard[recommendation]:
        if isinstance(chessboard[recommendation],pieces.Pieces):
            if chessboard[recommendation].team != piece.team:
                chessboard[recommendation].setTargeted(True)
        
                   
            return False
    else:
        if isinstance(piece,pieces.Pawn):
            if recommendedMove == -9 or recommendedMove == 11:
                return False
    return True

# COMPLETE CETTE FUNCTION QUI RETURN LES ENNEMIS (CELLS) QUI SONT TARGETTED PAR UN PION SELECTIONNER (JUST NEED TO MATCH DE CELLS)
def isMoveValid(piece,init_cell,clicked_cell):
    validMoves=[]
    for recommendedMove in piece.getAttackMoves():
            if isinstance(recommendedMove, list):
                for sub_recommendedMove in recommendedMove:
                    if isMoveRecommendationValid(piece, sub_recommendedMove, init_cell):
                        validMoves.append(sub_recommendedMove)
                    else:
                        break
                
            elif isMoveRecommendationValid(piece, recommendedMove,init_cell):
                
                    validMoves.append(recommendedMove)
       
    if isinstance(piece, pieces.Pawn):
        print("pawn")
        for recommendedMove in piece.getPossibleMoves():
            if isMoveRecommendationValid(piece, recommendedMove, init_cell):
                validMoves.append(recommendedMove)
            else:
                break
      
    for move in validMoves:
        if piece.team == "white":
            if clicked_cell == str(int(init_cell) + move):
                return True

        else:
            if clicked_cell == str(int(init_cell) - move ):
                return True
    return False                   
                    
                    
                    
def ennemiesTargeted(recommendedMoves):
    
    return True

# HAVE TO FIX
def drawRecommendation(piece,cell,recommendedMove):
    if piece.team == "white":
        target_cell = int(cell) + recommendedMove
        target_cord = getCordfromCell(str(target_cell))
        chess_canvas.create_circle(
            target_cord[0],
            target_cord[1],
            4, fill="white")
    else:
        target_cell = int(cell) - recommendedMove
        target_cord = getCordfromCell(str(target_cell))
        chess_canvas.create_circle(
            target_cord[0],
            target_cord[1],
            4, fill="blue")

def removeAllTargeted():
    for key in chessboard:
        if isinstance(chessboard[key], pieces.Pieces) and chessboard[key].isTargeted == True:
            chessboard[key].setTargeted(False)

def showMoves(cell, piece):
    if isinstance(piece,pieces.Pieces):
        #remove all targeted highlight
        removeAllTargeted()
        
        for recommendedMove in piece.getAttackMoves():
            if isinstance(recommendedMove, list):
                for sub_recommendedMove in recommendedMove:
                    if isMoveRecommendationValid(piece, sub_recommendedMove, cell):
                        drawRecommendation(piece,cell,sub_recommendedMove)
                    else:
                        if not isinstance(piece,pieces.Pawn):
                            print("true")
                            break
                            
                           
                            
            elif isMoveRecommendationValid(piece,recommendedMove,cell):
                drawRecommendation(piece,cell,recommendedMove)
    if isinstance (piece,pieces.Pawn):
        for recommendedMove in piece.getPossibleMoves():
            if isMoveRecommendationValid(piece, recommendedMove, cell):
                drawRecommendation(piece, cell, recommendedMove)
            else:
                break
            
chess_canvas.bind("<Button-1>", move)

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
         
#puts piece setdead=true and Coordinate (key) = None (value) and then update the chessboard_hash
def removepiece(piece: pieces.Pieces):
    if piece is not None:
        piece.setDead(True)

        if (piece.team == "white"):
            white_pieces_hash[piece] = None

        else:
            black_pieces_hash[piece] = None
        update_chessboard()
       

blank = Image.open("./assets/blank.png")
blank_image = ImageTk.PhotoImage(blank)





chessboard=generate_chessboard_Hash()
init_chessboard(chessboard)

#checks if a piece is dead and if it is puts none as a value to remove it
def update_chessboard():
    for key in chessboard.keys():
        if chessboard[key] is not None:
            if chessboard[key].isDead == True:
                chessboard[key]=None
                
            
    # for piece in white_pieces_hash:
    #     if isinstance(piece, list):
    #         for sub_piece in piece:
    #             chessboard[str(sub_piece.init_x) +
    #                             str(sub_piece.init_y)] = sub_piece
    #     else:
    #         if white_pieces_hash[piece]!=None:
    #             chessboard[str(piece.init_x) + str(piece.init_y)] = piece
            
               
    # for piece in black_pieces_hash:
    #     if isinstance(piece, list):
    #         for sub_piece in piece:
    #             chessboard[str(sub_piece.init_x) +
    #                             str(sub_piece.init_y)] = sub_piece
    #     else:
    #         if black_pieces_hash[piece] != None:
    #             chessboard[str(piece.init_x) + str(piece.init_y)] = piece

##game loop recursive
def update():
    update_board_ui()
    frm.after(100, update)
    

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle


def _draw_cell(self, x, y,color):
    return self.create_rectangle(
        x * cell_size, y *
        cell_size, (x + 1) * cell_size, (y + 1) * cell_size,
        fill=color, outline="")
Canvas.create_square = _draw_cell

cell_size = 70

# HAVE TO FIX
def update_board_ui():
    chess_canvas.delete("all")
    cell_size = 70  # Adjust this value as needed
    for x in range(8):
        for y in range(8):
            color = "#C19A6B" if (x + y) % 2 == 0 else "#342214"
            chess_canvas.create_square(x, y, color)
    # Draw the cells
    for x in range(8):
        for y in range(8):
            piece = chessboard[str(x) + str(7-y)]
            cell = str(x) + str(7-y)
            # if type(piece) is pieces.Rook or pieces.Bishop or pieces.Pawn or pieces.King or pieces.Queen :
            if isinstance(piece,pieces.Pieces):
                if piece is not None:
                    if piece.isSelected == True:
                        color = "#FFFF00"
                        chess_canvas.create_square(x, y, color)
                        showMoves(cell,piece)
                        
                    if piece.isTargeted == True:
                        color = "#FF7F7F"
                        chess_canvas.create_square(x, y, color)
        
          
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
def set_win():
    global win
    global text
    text= "game won"
    win_label.config(text=text)

def set_turn(value):
    turn_label.config(text=value)
    

##quand une piece mange un autre
spawn_window_button = Button(button_label,
                             text="Delete",
                             command=lambda: removepiece(chessboard["31"])).grid(column=0, row=0)

##Quand le roi est math 
spawn_window_button_win = Button(button_label,
                             text="Win",
                             command=lambda: set_win()).grid(column=1, row=0)


win_label= Label(button_label,text="Playing")
win_label.grid(column=2, row=0)

turn = 0
turn_label = Label(button_label, text="Turn")
turn_label.grid(column=3, row=0)
    




##commence la partie
update()
root.mainloop()



##almost works cause only thing left is cant attack

#roques, echec, math

#maybe afficher les pieces sur le coter quand ils meurts

##make turns and write whose turn is it


