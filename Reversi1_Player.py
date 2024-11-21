###################################################################################################################################
# Deterministic Method
###################################################################################################################################
class Cell:
    def __init__(self, owner=-1):
        self.owner = owner  # 0=black, 1=white, -1=blank, 2=possible move

    def getOwner(self):
        return self.owner

    def setOwner(self, int):
        try:
            if int in [-1, 0, 1, 2]:
                self.owner = int
            else:
                raise ValueError("Οι τιμές πρέπει να είναι -1, 0, 1, 2")
        except ValueError as ve:
            print(ve)

class Reversi30:
    def __init__(self, pid=0, size=8):
        self.pid = pid      # 0=black, 1=white
        self.size = size    # even number, size of the board

    @staticmethod
    def getPlayerName():
        return "Player1"

    def setPid(self, int):
        try:
            if int in [0, 1]:
                self.pid = int
            else:
                raise ValueError("Οι παίχτες είναι δύο, 0 για μαύρα και 1 για άσπρα")
        except ValueError as ve:
            print(ve)

    def setBoardSize(self, int):
        try:
            if int % 2 == 0:
                self.size = int
            else:
                raise ValueError("Το ταμπλό πρέπει να είναι άρτιος αριθμός")
        except ValueError as ve:
            print(ve)

#    def setBoard(self, size=8):     # Δημιουργεί το αρχικό ταμπλό
#        board = []
#        for i in range(size):
#            row = [Cell() for j in range(size)]      # Έχω κάνει το ταμπλό λιστα απο Cells
#            board.append(row)
#        # Βάζω αρχικές θέσεις στο ταμπλό
#        board[3][3].setOwner(1)
#        board[4][4].setOwner(1)
#        board[3][4].setOwner(0)
#        board[4][3].setOwner(0)
#        return board

#    def printBoard(self, board):    # Μετατρέπει το ταμπλό σε λίστα με int με την συνάρτηση getOwner
#        print("   0 1 2 3 4 5 6 7")
#        print("  -----------------")
#        for i in range(self.size):
#            print("{:d} |".format(i), end="")     # end="" ώστε να παραμείνει στην ίδια γραμμή
#            for j in range(self.size):
#                owner = board[i][j].getOwner()
#                if owner == -1:
#                    print("-", end=" ")
#                else:
#                    print(owner, end=" ")
#            print("|")
#        print("  -----------------")

    def findNeighbours(self, board):
        find_cells = []
        for i in range(self.size):      # Διαδικασία που βρίσκει τα μάυρα ή άσπρα Cells του board ανάλογα με την τιμή pid
            for j in range(self.size):
                if board[i][j].getOwner() == self.pid:
                    find_cells.append((i,j))

        dir = [(0,-1), (0,1), (1,0), (-1,0), (1,-1), (1, 1), (-1, -1), (-1, 1)] # up, down, right, left, upright, downright, upleft, downleft
        for x, y in dir:
            for i, j in find_cells:
                i += x
                j += y
                while i >= 0 and i < self.size and j >= 0 and j < self.size and board[i][j].getOwner() == 1 - self.pid: # Ψάχνει μαύρα αν pid=1 (άσπρο)
                    i += x                                                                                              # Ψάχνει άσπρα αν pid=0 (μαύρο)
                    j += y
                    if i < 0 or i >= self.size or j < 0 or j >= self.size:  # Θέλουμε οι τιμές να παραμένουν μέσα στο ταμπλό που ορίζει η instance var size
                        break;
                    if board[i][j].getOwner() == -1:
                        board[i][j].setOwner(2)
                    elif board[i][j].getOwner() == self.pid or board[i][j].getOwner() == 2:
                        break;
        return board

    def placeTile(self, board):
        board = self.findNeighbours(board)
        moves = []
        best_move = None

        for i in range(self.size):      # Διαδικασία που βρίσκει τις πιθανές κινήσεις του board δηλαδή pid=2
            for j in range(self.size):
                if board[i][j].getOwner() == 2:
                    moves.append((i,j))

        if len(moves) == 0:        # Αν δεν υπάρχουν κινήσεις τότε επιστρέφει την κενή πλειάδα
            return best_move

        for move in moves:         # Αν μια από τις γωνίες είναι δυνατή κίνηση τότε απευθείας επιλέγεται
            if move in [(0,0), (0,7), (7,0), (7,7)]:
                return move

        best_score = -1
        dir = [(0, -1), (0, 1), (1, 0), (-1, 0), (1, -1), (1, 1), (-1, -1), (-1, 1)]
        for move in moves:
            score = 0           # Ο αριθμός των cell του αντιπάλου που βρίσκονται ανάμεσα στα cell του παίχτη (προς όλες τις κατευθύνσεις)
            for x, y in dir:
                i, j = move
                score_add = 0       # Ορίζω score_add που μετρά το score της κάθε κατεύθυνσης
                i += x
                j += y
                while i >= 0 and i < self.size and j >= 0 and j < self.size and board[i][j].getOwner() == 1 - self.pid:
                    i += x
                    j += y
                    score_add += 1
                    if i < 0 or i >= self.size or j < 0 or j >= self.size:
                        break;
                    if board[i][j].getOwner() == -1 or board[i][j].getOwner() == 2:
                        break;
                    elif board[i][j].getOwner() == self.pid:
                        score += score_add                      # Προσθέτω την τιμή της score_add στην score μόνο όταν μια διαδρομή καταλήγει σε cell του παίχτη
            if score > best_score:      # Με αυτον τον τρόπο αν υπάρχουν παραπάνω απο μία κινήσεις που εξασφαλίζουν μέγιστο score
                best_score = score      # θα διαλέξει την πρώτη που βρήκε
                best_move = move
        return best_move #, best_score, moves

    def findTakeOverCells(self, board, row, col):
        # board = self.findNeighbours(board) Δεν χρειάζονται οι δυνατές κινήσεις σε αυτή την μέθοδο
        take_over_cells = []
        dir = [(0, -1), (0, 1), (1, 0), (-1, 0), (1, -1), (1, 1), (-1, -1), (-1, 1)]
        for x, y in dir:
            i, j = row, col
            i += x
            j += y
            cells_to_take_over = []     # Λίστα που κρατά τις συντ/νες των cells του αντιπάλου για take over προς κάθε κατεύθυνση
            while i >= 0 and i < self.size and j >= 0 and j < self.size and board[i][j].getOwner() == 1 - self.pid:
                cells_to_take_over.append((i, j))
                i += x
                j += y
                if i < 0 or i >= self.size or j < 0 or j >= self.size:
                    break;
                if board[i][j].getOwner() == -1: # or board[i][j].getOwner() == 2:
                    break;
                elif board[i][j].getOwner() == self.pid:        # Αν ο αλγόριθμος καταλήξει σε cell του παίχτη τότε μόνο προστίθεται
                    take_over_cells += cells_to_take_over       # η cells_to_take_over στην take_over_cells, αλλιώς συνεχίζει στον
                    break;                                      # έλεγχο των υπολοίπων κατευθύνσεων
        return list(set(take_over_cells))   # Το γράφω έτσι ώστε να εξαφανίζονται τα duplicates (εμφανίστηκαν σε κάποια παραδείγματα)

    def applyChanges(self, board):
        board = self.findNeighbours(board)              # Παίρνουμε το board απο την findNeighbours ώστε να χρησιμοποιήσουμε
        best_move = self.placeTile(board)               # την placeTile (χρειάζεται τις δυνατές κινήσεις ώστε να τις αξιολογήσει).

        if best_move is None:                           # Αν δεν υπάρχει κίνηση τότε απλα θα μετατρέπει     (Αχρείαστο αφού αν best_move=None τότε δεν υπάρχουν cells με owner 2)
#           for i in range(self.size):                  # τα cells του board που έχουν τιμή 2 σε τιμή -1.
#               for j in range(self.size):
#                   if board[i][j].getOwner() == 2:
#                       board[i][j].setOwner(-1)
            return board
        else:
            i, j = best_move
            take_over_cells = self.findTakeOverCells(board, row=i, col=j)
            board[i][j].setOwner(self.pid)              # Βάζει το cell του παίχτη στην βέλτιστη θέση

            for cell in take_over_cells:                # Παίρνει τα cells του αντιπάλου
                i, j = cell
                board[i][j].setOwner(self.pid)

            for i in range(self.size):                  # Μετατρέπει τα cells του board που έχουν τιμή 2 σε τιμή -1
                for j in range(self.size):
                    if board[i][j].getOwner() == 2:
                        board[i][j].setOwner(-1)
            return board

# # create an instance of the Reversi30 class with size 8
# game = Reversi30(0,8)
# # get the starting board
# board = game.setBoard()
# # print the starting board
# print("Starting board:")
# game.printBoard(board)
# # find the neighbors of each cell on the board
# print("Possible moves:")
# board = game.findNeighbours(board)
# game.printBoard(board)
# # place a tile on the board using the algorithm
# best_move = game.placeTile(board)
# # apply the changes to the board
# board = game.applyChanges(board)
# # print the board after the tile has been placed and changes have been made
# print("Board after placing tile and applying changes:")
# game.printBoard(board)

# print('\n\n')

# # create an instance of the Reversi30 class with size 8
# game = Reversi30(1,8)
# # create an example board
# exboard = game.setBoard()
# exboard[3][3].setOwner(0)
# exboard[4][4].setOwner(0)
# exboard[3][5].setOwner(0)
# exboard[2][4].setOwner(0)
# exboard[5][3].setOwner(0)
# exboard[5][4].setOwner(1)
# exboard[5][5].setOwner(1)
# exboard[5][6].setOwner(1)
# exboard[2][0].setOwner(1)
# exboard[2][1].setOwner(1)
# exboard[2][2].setOwner(1)
# exboard[2][3].setOwner(1)
# exboard[1][3].setOwner(1)
# exboard[0][3].setOwner(1)
# exboard[3][2].setOwner(1)
# exboard[4][2].setOwner(1)
# print("Example board:")
# game.printBoard(exboard)
# # find the neighbors of each cell on the board
# print("Possible moves for player {:d}:".format(game.pid))
# exboard = game.findNeighbours(exboard)
# game.printBoard(exboard)
# # place a tile on the board using the algorithm
# best_move = game.placeTile(exboard)
# print("Best Move:", best_move)
# # find the take over cells
# take_over_cells = game.findTakeOverCells(exboard, best_move[0], best_move[1])
# print("Cells to take over:", take_over_cells)
# # apply the changes to the board
# exboard = game.applyChanges(exboard)
# # print the board after the tile has been placed and changes have been made
# print("Board after placing tile and applying changes:")
# game.printBoard(exboard)

# print('\n\n')

# # create an instance of the Reversi30 class with size 8
# game = Reversi30(1,8)
# # create an example board
# exboard1 = game.setBoard()
# exboard1[3][3].setOwner(0)
# exboard1[5][3].setOwner(0)
# exboard1[1][3].setOwner(0)
# exboard1[3][5].setOwner(0)#
# exboard1[2][0].setOwner(1)
# exboard1[2][4].setOwner(1)
# exboard1[2][1].setOwner(1)
# exboard1[2][2].setOwner(1)
# exboard1[2][3].setOwner(1)
# exboard1[3][2].setOwner(1)
# exboard1[3][4].setOwner(1)
# exboard1[4][2].setOwner(1)
# exboard1[4][4].setOwner(1)
# exboard1[5][4].setOwner(1)
# exboard1[5][5].setOwner(1)
# exboard1[5][6].setOwner(1)
# print("Example board:")
# game.printBoard(exboard1)
# # find the neighbors of each cell on the board
# print("Possible moves for player {:d}:".format(game.pid))
# exboard1 = game.findNeighbours(exboard1)
# game.printBoard(exboard1)
# # place a tile on the board using the algorithm
# best_move = game.placeTile(exboard1)
# print("Best Move:", best_move)
# # find the take over cells
# take_over_cells = game.findTakeOverCells(exboard1, best_move[0], best_move[1])
# print("Cells to take over:", take_over_cells)
# # apply the changes to the board
# exboard = game.applyChanges(exboard1)
# # print the board after the tile has been placed and changes have been made
# print("Board after placing tile and applying changes:")
# game.printBoard(exboard1)

# print('\n\n')

# # create an instance of the Reversi30 class with size 8, Test: Corner Move
# game = Reversi30(1,8)
# # create an example board
# exboard = game.setBoard()
# exboard[3][3].setOwner(1)
# exboard[3][4].setOwner(0)
# exboard[4][3].setOwner(0)
# exboard[4][4].setOwner(1)
# exboard[4][5].setOwner(0)
# exboard[5][1].setOwner(1)
# exboard[5][2].setOwner(1)
# exboard[5][3].setOwner(1)
# exboard[5][4].setOwner(1)
# exboard[5][5].setOwner(1)
# exboard[6][1].setOwner(0)
# exboard[6][3].setOwner(0)
# print("Example board:")
# game.printBoard(exboard)
# # find the neighbors of each cell on the board
# print("Possible moves for player {:d}:".format(game.pid))
# exboard = game.findNeighbours(exboard)
# game.printBoard(exboard)
# # place a tile on the board using the algorithm
# best_move = game.placeTile(exboard)
# print("Best Move:", best_move)
# # find the take over cells
# take_over_cells = game.findTakeOverCells(exboard, best_move[0], best_move[1])
# print("Cells to take over:", take_over_cells)
# # apply the changes to the board
# exboard = game.applyChanges(exboard)
# # print the board after the tile has been placed and changes have been made
# print("Board after placing tile and applying changes:")
# game.printBoard(exboard)

# print('\n\n')

# # create an instance of the Reversi30 class with size 8, Test: No move
# game = Reversi30(1,8)
# # create an example board
# exboard = game.setBoard()
# for i in range(0,8):
#     exboard[i][7].setOwner(0)
# for i in range(0,4):
#     exboard[0][i].setOwner(0)
# exboard[0][5].setOwner(1)
# exboard[0][6].setOwner(0)
# for i in range(0,5):
#     exboard[1][i].setOwner(1)
# exboard[1][5].setOwner(0)
# exboard[1][6].setOwner(0)
# exboard[1][7].setOwner(0)
# exboard[2][0].setOwner(0)
# exboard[2][1].setOwner(1)
# exboard[2][2].setOwner(1)
# exboard[2][3].setOwner(1)
# exboard[2][4].setOwner(0)
# exboard[2][5].setOwner(1)
# exboard[2][6].setOwner(0)
# exboard[3][0].setOwner(0)
# exboard[3][1].setOwner(0)
# exboard[3][2].setOwner(1)
# exboard[3][3].setOwner(0)
# exboard[3][4].setOwner(1)
# exboard[3][5].setOwner(1)
# exboard[3][6].setOwner(1)
# exboard[4][0].setOwner(0)
# exboard[4][1].setOwner(1)
# exboard[4][2].setOwner(0)
# exboard[4][3].setOwner(0)
# exboard[4][4].setOwner(1)
# exboard[4][5].setOwner(1)
# exboard[4][6].setOwner(0)
# for i in range(0,4):
#     exboard[5][i].setOwner(0)
# for i in range(0,3):
#     exboard[6][i].setOwner(0)
# for i in range(0,7):
#     exboard[7][i].setOwner(0)
# for i in range(0,3):
#     exboard[6][4+i].setOwner(1)
# exboard[5][6].setOwner(0)
# exboard[5][5].setOwner(0)
# exboard[5][4].setOwner(0)
# exboard[6][3].setOwner(1)
# print("Example board:")
# game.printBoard(exboard)
# # find the neighbors of each cell on the board
# print("Possible moves for player {:d}:".format(game.pid))
# exboard = game.findNeighbours(exboard)
# game.printBoard(exboard)
# # place a tile on the board using the algorithm
# best_move = game.placeTile(exboard)
# print("Best Move:", best_move)
# # find the take over cells
# if best_move == None:
#     # apply the changes to the board
#     exboard = game.applyChanges(exboard)
#     take_over_cells = []
# else:
#     take_over_cells = game.findTakeOverCells(exboard, best_move[0], best_move[1])
#     # apply the changes to the board
#     exboard = game.applyChanges(exboard)
# print("Cells to take over:", take_over_cells)
# # print the board after the tile has been placed and changes have been made
# print("Board after placing tile and applying changes:")
# game.printBoard(exboard)
