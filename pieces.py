
#eventually cut the big one into smaller pieces :)

from PIL import Image, ImageTk

class Pieces():
    def __init__(self, image, team, init_x, init_y):
        self.team = team
        chess_image = Image.open(image)
        self.chess_photo = ImageTk.PhotoImage(chess_image)
        self.init_x = init_x
        self.init_y = init_y
        self.x=self.init_x
        self.y=self.init_y
        self.isSelected=False
        self.isTargeted=False
        self.isDead=False
    
    def setSelected(self,bool):
        self.isSelected=bool

    def setTargeted(self,bool):
        self.isTargeted = bool
        
    def setDead(self, bool):
        self.isDead = bool
        
class Pawn(Pieces):
    def __init__(self, team,init_x):
        image = f"./assets/pawn_{team}.png"
        init_y = {"white": 1, "black": 6}[team]
        self.firstMove=True
        self.canAttack = False
        self.possibleMoves=[]

       
        
        super().__init__(image, team, init_x, init_y)
        
    def setFirstMove(self):
        self.firstMove=False
    
    def getPossibleMoves(self):
        if self.firstMove:
            self.possible_moves = [1, 2]
        else:
            self.possible_moves = [1]
        return self.possible_moves   

    def getAttackMoves(self):
        return [11, -9]
class Knight(Pieces):
    def __init__(self, team,init_x):
        image = f"./assets/knight_{team}.png"
        init_y = {"white": 0, "black": 7}[team]
        self.possibleAttack_Moves = [12, 21, 19, -12, 8, -21, -19, -8]
        super().__init__(image, team, init_x, init_y)
        
    def getAttackMoves(self):
        return self.possibleAttack_Moves
    
class Bishop(Pieces):
    def __init__(self, team,init_x):
        image = f"./assets/bishop_{team}.png"
        init_y = {"white": 0, "black": 7}[team]
        self.possibleAttack_Moves = [[11, 22, 33, 44, 55, 66, 77], [-11, -22, -33, -44, -55, -66,
                              -77], [-9, -18, -27, -36, -45, -54, -63], [9, 18, 27, 36, 45, 54, 63]]
        super().__init__(image, team, init_x, init_y)
        
    def getAttackMoves(self):
        return self.possibleAttack_Moves
    
class Rook(Pieces):
    def __init__(self, team,init_x):
        image = f"./assets/rook_{team}.png"
        init_y = {"white": 0, "black": 7}[team]
        self.possibleAttack_Moves = [[1, 2, 3, 4, 5, 6, 7], [10, 20, 30, 40, 50, 60,
                              70],[ -1, -2, -3, -4, -5, -6, -7],[ -10, -20, -30, -40, -50, -60, -70]]

        
        super().__init__(image, team, init_x, init_y)
        
    def getAttackMoves(self):
        return self.possibleAttack_Moves
       

class Queen(Pieces):
    def __init__(self, team,init_x):
        image = f"./assets/queen_{team}.png"
        init_x = 3
        init_y = {"white": 0, "black": 7}[team]
        #en rajouter
        self.possibleAttack_Moves = [[11, 22, 33, 44, 55, 66, 77], [-11, -22, -33, -44, -55, -66,
                              -77], [-9, -18, -27, -36, -45, -54, -63], [9, 18, 27, 36, 45, 54, 63], [1, 2, 3, 4, 5, 6, 7], [-1, -2, -3, -4, -5, -6, -7], [10, 20, 30, 40, 50, 60, 70], [-10, -20, -30, -40, -50, -60, -70]]
        super().__init__(image, team, init_x, init_y)
        
    def getAttackMoves(self):
        return self.possibleAttack_Moves
    
class King(Pieces):
    def __init__(self, team,init_x):
        image = f"./assets/king_{team}.png"
        init_x = 4
        init_y = {"white": 0, "black": 7}[team]
        self.possibleAttack_Moves = [11, -11, -9, 9, 1, -1, 10, -10]
        super().__init__(image, team, init_x, init_y)
        
    def getAttackMoves(self):
        return self.possibleAttack_Moves
