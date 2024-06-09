from tkinter import *
from PIL import Image, ImageTk
import pieces
import numpy as np



root = Tk(className="Chess")


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
        if current_team != chessboard[cell].team and not chessboard[cell].isTargeted:
            return False
    previous_piece = chessboard[last_cell] if last_cell is not None else None
    clicked_piece = chessboard[cell]
    
    # If a piece is already selected
    if previous_piece is not None:
        if isinstance(clicked_piece, pieces.Pieces):
            if isinstance(previous_piece, pieces.Pieces):
                
                if previous_piece.team != clicked_piece.team and clicked_piece.isTargeted:
                  
                    # If the clicked piece belongs to the opposing team, capture it
                    clicked_piece.setDead(True)
                    previous_piece.setSelected(False)
                    
                    #queen when pawn promotes
                    if isinstance(previous_piece,pieces.Pawn) and isLastRow(cell,previous_piece.team):
                        chessboard[cell] = pieces.Queen(previous_piece.team, cell[0],cell[1])
                    else:    
                        chessboard[cell] = previous_piece
                        
                    chessboard[last_cell] = None
                    removeAllTargeted()
                    switchTeam()

                            
                elif previous_piece != clicked_piece and previous_piece.team == clicked_piece.team:
                   
                    # If the clicked piece belongs to the same team but is different,
                    # switch selection to the new piece
                    previous_piece.setSelected(False)
                    clicked_piece.setSelected(True)
                    last_cell = cell

                    
                elif previous_piece == clicked_piece:
                    # If the clicked piece is the same one
                    previous_piece.setSelected(False)
                    removeAllTargeted()
                    last_cell=None
            
                    
              

                    
                    
                  
        else:
            if isMoveValid(previous_piece,last_cell,cell,False):
                if isinstance(previous_piece,pieces.King):
                   if isCellTargeted(previous_piece.team,getPositionAfterMove(previous_piece,cell),False):
                       return False
                 
                #queen when pawn promotes
                if isinstance(previous_piece,pieces.Pawn) and isLastRow(cell,previous_piece.team):
                
                    chessboard[cell] = pieces.Queen(previous_piece.team, cell[0],cell[1])
                else:    
                    chessboard[cell] = previous_piece
                    
                chessboard[last_cell] = None
                last_cell = cell
                if isinstance(previous_piece, pieces.Pawn):
                    previous_piece.setFirstMove()
                previous_piece.setSelected(False)
                removeAllTargeted()
                switchTeam()
            

    
    else:
        if isinstance(clicked_piece, pieces.Pieces):
            # Deselect the last selected piece if a new piece is clicked
            previous_piece=chessboard[cell]
            previous_piece.setSelected(True)
            last_cell = cell
    
def isLastRow(cell,team):
    if team=="white":
        if cell[1]=="7":
            return True
    else:
        if cell[1]=="0":
            return True
    return False        
    
    
def switchTeam():
    global current_team
    global last_cell
    
    if current_team == "white":
        current_team = "black"
    else:
        current_team = "white"
    isKingTargeted(current_team)
    removeAllTargeted()
    last_cell=None
    
    set_turn(current_team)

def getRecommandation(cell,recommendedMove,team):
    recommendation=""
    if team == "white":
        recommendation = str(int(cell) + recommendedMove)
    else:
        recommendation = str(int(cell) - recommendedMove)
    if len(recommendation) < 2:
        recommendation = f"0{recommendation}"
    return recommendation


def isMoveRecommendationValid(piece,recommendedMove,cell):
    recommendation = getRecommandation(cell,recommendedMove,piece.team)
    

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
            if isinstance(piece,pieces.Pawn):
                if recommendedMove != 1 and recommendedMove != 2 :
                    if chessboard[recommendation].team != piece.team:
                                chessboard[recommendation].setTargeted(True)
                                return chessboard[recommendation]
            else:
                if chessboard[recommendation].team != piece.team:
                    chessboard[recommendation].setTargeted(True)
                    return chessboard[recommendation]
                   
            return chessboard[recommendation]
    else:
        if isinstance(piece,pieces.Pawn):
            if recommendedMove == -9 or recommendedMove == 11:
                return False
    return True


def isMoveValid(piece,init_cell,clicked_cell,isProtecting):
    if str(init_cell)==str(clicked_cell):
        return False
    validMoves=[]
    piecesProtected=[]
    for recommendedMove in piece.getAttackMoves():
            if isinstance(recommendedMove, list):
                for sub_recommendedMove in recommendedMove:
                    if isMoveRecommendationValid(piece, sub_recommendedMove, init_cell) is True:
                        validMoves.append(sub_recommendedMove)
                        
                            
                    #si une piece est retournee then la liste de recommandation break
                    elif isinstance(isMoveRecommendationValid(piece, sub_recommendedMove, init_cell),pieces.Pieces):
                        if piece.team!=isMoveRecommendationValid(piece, sub_recommendedMove, init_cell).team:
                            validMoves.append(sub_recommendedMove)
                        elif isProtecting:
                            piecesProtected.append(sub_recommendedMove)                            
                        break
                    else:
                        break
                
            elif isMoveRecommendationValid(piece, recommendedMove,init_cell) is True:
                    validMoves.append(recommendedMove)
            elif isinstance(isMoveRecommendationValid(piece, recommendedMove, init_cell),pieces.Pieces):
                        if piece.team!=isMoveRecommendationValid(piece, recommendedMove, init_cell).team:
                            validMoves.append(recommendedMove)
                        
                        elif isProtecting:
                            piecesProtected.append(recommendedMove)      
    if isinstance(piece, pieces.Pawn):
       
        for recommendedMove in piece.getPossibleMoves():
            if isMoveRecommendationValid(piece, recommendedMove, init_cell):
                validMoves.append(recommendedMove)
            else:
                break
    if not isProtecting:  
        for move in validMoves:
            print(str(clicked_cell),getRecommandation(init_cell,move,piece.team))
            if str(clicked_cell)== getRecommandation(init_cell,move,piece.team):
                return True
    else:
        for move in  piecesProtected: 
            if  str(clicked_cell) == getRecommandation(init_cell,move,piece.team):
                
                return True
    return False                   
                    


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
            4, fill="white")

def removeAllTargeted():
    for key in chessboard:
        if isinstance(chessboard[key], pieces.Pieces) and chessboard[key].isTargeted == True:
            chessboard[key].setTargeted(False)
            
def isKingTargeted(team):
    for cell in chessboard.keys():
        piece=chessboard[cell]
        if isinstance(piece,pieces.King) and piece.team==team:  
            if isCellTargeted(team,cell,False):
                if setKingEchec(piece):
                    gameOver()

def isPieceTargeted(piece,team):
    if  isCellTargeted(team,getPiecePosition(piece),False):
        return True   
                    
#IL FAUT JUSTE FIX CA
def isCellTargeted(team,cell,isCheckingProtected):
    for key in chessboard.keys():
        piece=chessboard[key]
        if isinstance(piece,pieces.Pieces):
           
            if piece.team != team:
                
                if isCheckingProtected:
                    if isMoveValid(piece,key,cell,True):
                        return piece
                else:
                    if isMoveValid(piece,key,cell,False):
                        return piece
                   
    return False
    
#math doent work
def setKingEchec(king):
    piece_attaquante= isCellTargeted(king.team,getPiecePosition(king),False) 
    
    for move in king.getAttackMoves():
        #si le king peut bouger
      
        if isMoveRecommendationValid(king, move, getPiecePosition(king)):
            #si cest une piece
            if isinstance(isMoveRecommendationValid(king,move,getPiecePosition(king)),pieces.Pieces):
                if king.team!=isMoveRecommendationValid(king,move,getPiecePosition(king)).team:
                   
                   #si la piece nest pas proteger
                    if not isCellTargeted(king.team,getPositionAfterMove(king,move),True):  
                        print("peux manger avec roi")  
                        return False
                    
            #si cest une cell               
            else:
                #si l'endroit ou le king veut bouger nest pas attaque
                if isCellTargeted(king.team,getPositionAfterMove(king,move),False)==False:
                    print("peut bouger")
                    return False
                
    #si la piece attaquante peut etre mangee            
    for key in chessboard.keys():
        piece=chessboard[key]
        if isinstance(piece,pieces.Pieces) and not isinstance(piece,pieces.King):
            print("eee")
            if piece.team != getOppositeTeam(king.team):
                if isMoveValid(piece,key,getPiecePosition(piece_attaquante),False):
                    print("peut manger")
                    return False
   
   
         
    #si la trajectoire de l<attauqe peut etre bloquer                     
        

    return True

def checkMath():
    new_chessboard= chessboard
    
    
def getOppositeTeam(team):
    if team=="white":
        return "black"
    else:
        return "white"
    
    
def getPiecePosition(piece):
    for key in chessboard.keys():
        if chessboard[key] == piece:
            return key
        
def gameOver():
    print("gameover")
    pass

def getPositionAfterMove(piece,move):
    move=int(move)
    init_cell=int(getPiecePosition(piece))
    if piece.team == "white":
        return init_cell + move
    else:
        return init_cell - move
    
        
    
       
def showMoves(cell, piece):
    if isinstance(piece,pieces.Pieces):
        #remove all targeted highlight
        removeAllTargeted()
        
        for recommendedMove in piece.getAttackMoves():
            if isinstance(recommendedMove, list):
                for sub_recommendedMove in recommendedMove:
                    if isMoveRecommendationValid(piece, sub_recommendedMove, cell) is True:
                        drawRecommendation(piece,cell,sub_recommendedMove)
                        
                    #si une piece est retournee then la liste de recommandation break
                    elif isinstance(isMoveRecommendationValid(piece, sub_recommendedMove, cell),pieces.Pieces):
                        drawRecommendation(piece,cell,sub_recommendedMove)
                        break
                    else:
                        if not isinstance(piece,pieces.Pawn):
                            
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
white_pieces_list = [[ pieces.Pawn("white",i) for i in range(0,8)],pieces.Rook("white",0),pieces.Rook("white",7),pieces.Bishop("white",2),pieces.Bishop("white",5),pieces.Knight("white",1),pieces.Knight("white",6),pieces.King("white",4),pieces.Queen("white",3,0)]
white_deadpieces_list = []
black_pieces_list = [[pieces.Pawn("black", i) for i in range(0, 8)], pieces.Rook("black", 0), pieces.Rook("black", 7), pieces.Bishop(
    "black", 2), pieces.Bishop("black", 5), pieces.Knight("black", 1), pieces.Knight("black", 6), pieces.King("black", 4), pieces.Queen("black", 3,7)]
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
    
     # Draw the cells
    for x in range(8):
        for y in range(8):
            color = "#C19A6B" if (x + y) % 2 == 0 else "#342214"
            chess_canvas.create_square(x, y, color)
     # Draw the moves
    for x in range(8):
        for y in range(8):
            piece = chessboard[str(x) + str(7-y)]
            cell = str(x) + str(7-y)
            if isinstance(piece,pieces.Pieces):
                if piece is not None:
                    if piece.isSelected == True:
                        showMoves(cell,piece)
    # Draw the pieces
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

def set_turn(value):
    turn_label.config(text=f"{value}'s turn")
    


turn = 0
turn_label = Label(button_label, text="Turn")
turn_label.grid(column=3, row=0)
    




##commence la partie
update()
root.mainloop()




#roques, echec, math, en passant
