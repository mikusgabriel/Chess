
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

class Pawn(Pieces):
    def __init__(self, team,init_x):
        image = f"./assets/pawn_{team}.png"
        init_y = {"white": 1, "black": 6}[team]
        super().__init__(image, team, init_x, init_y)

class Knight(Pieces):
    def __init__(self, team,init_x):
        image = f"./assets/knight_{team}.png"
        init_y = {"white": 0, "black": 7}[team]
        super().__init__(image, team, init_x, init_y)

class Bishop(Pieces):
    def __init__(self, team,init_x):
        image = f"./assets/bishop_{team}.png"
        init_y = {"white": 0, "black": 7}[team]
        super().__init__(image, team, init_x, init_y)

class Rook(Pieces):
    def __init__(self, team,init_x):
        image = f"./assets/rook_{team}.png"
        init_y = {"white": 0, "black": 7}[team]
        super().__init__(image, team, init_x, init_y)

class Queen(Pieces):
    def __init__(self, team,init_x):
        image = f"./assets/queen_{team}.png"
        init_x = 3
        init_y = {"white": 0, "black": 7}[team]
        super().__init__(image, team, init_x, init_y)

class King(Pieces):
    def __init__(self, team,init_x):
        image = f"./assets/king_{team}.png"
        init_x = 4
        init_y = {"white": 0, "black": 7}[team]
        super().__init__(image, team, init_x, init_y)
