###################################################################################################################################
# Monte-Carlo Method
###################################################################################################################################

import random
import copy

class Cell:
    
    # Initialization / variable: owner
    def __init__(self, owner = -1):
        self.owner = owner  # initialization to the value -1

    # Returns the value of owner of the cell
    def getOwner(self):
        return self.owner

    # Sets the value of owner of the cell and raises an error if it is invalid / variable: owner
    def setOwner(self, owner):
        try:
            self.owner = owner
            if owner not in [-1, 0, 1, 2]:
                raise ValueError("Invalid Value. It should be -1, 0, 1, 2")
        except ValueError as ex:
            print("Error",ex)


class Reversi2:

    # Initialization / variable: owner
    def __init__(self, pid = 0, size = 8):
        self.pid = pid
        self.size = size

    # Sets the value of pid (valid values 0 or 1) / variable: pid
    def setPid(self, pid):
        try:
            self.pid = pid
            if pid not in [0, 1]:
                raise ValueError("Invalid Value. It should be -0, 1")
        except ValueError as ex:
            print("Error", ex)

    # Returns the value of pid
    def getPid(self):
        return self.pid

    # Sets the size of the board (valid value is an even number) / variable: size
    def setBoardSize(self, size):
        try:
            self.size = size
            if size%2 != 0:
                raise ValueError("Invalid Value. It should be even number")
        except ValueError as ex:
            print("Error", ex)

    # Returns the string names of the players
    def getPlayerName(self):
        return "Player2"

    
    # Finds possible positions to place a piece and changes the owner attribute to 2 on the board
    # Basic Logic: For each of the player's pieces, scan in every direction and if you find
    # consecutive opponent's pieces followed by an empty space, then that empty space is a possible placement 
    # Variable: board  
    def findNeighbours(self, board):

        possible_spots = []   # List where potential placement coordinates will be stored (for the player)
        directions = [(0,1),(1,0),(-1,0),(0,-1),(1,-1),(-1,1),(1,1),(-1,-1)]   # Directional vectors
        player_spots = []    # List where the player's pieces will be stored

        # Add the player's pieces to player_spots
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j].owner == self.pid:
                    player_spots.append([i,j])

        # For each of the player's pieces and each direction, do the following:
        for i in range(len(player_spots)): 
            for j in range(len(directions)):
                row = (directions[j])[0]   # The first element of the j-th direction
                col = (directions[j])[1]   # The second element of the j-th direction
                
                # Inside the while loop, the first two conditions are for the index checks and the third is the key condition
                # that the next piece in the j direction should be of the opponent
                while (0 <= (player_spots[i])[0]+row < self.size) and (0 <= (player_spots[i])[1]+col < self.size) and (board[(player_spots[i])[0] + row][(player_spots[i])[1] + col].owner == 1 - self.pid):
                    # Update the row and col to check the next piece in the direction
                    row = row + (directions[j])[0]
                    col = col + (directions[j])[1]
                    # The first two conditions are for the indexes, and the third is if the next piece in the j direction is an empty space
                    # Then, the first empty space followed by consecutive opponent's pieces is a potential placement for the player
                    if (0 <= (player_spots[i])[0] + row < self.size) and (0 <= (player_spots[i])[1] + col < self.size) and (board[(player_spots[i])[0] + row][(player_spots[i])[1] + col].owner == -1):
                        possible_spots.append([row + (player_spots[i])[0], col + (player_spots[i])[1]])
                        
        # Update the board since the coordinates of possible spots are known
        for i in range(len(possible_spots)):
            board[((possible_spots[i])[0])][((possible_spots[i])[1])].owner = 2
        
        return board


    # Evaluates the best of the possible placement spots using the Pure Monte Carlo method where for each possible spot
    # x simulations of the game (with random moves) are run and the one giving the best average score is selected  
    # Variable: board / Uses the rand_simulate function
    def placeTile(self,board): 
        
        # Initialization
        player_turn = self.pid
        avg_score = 0   # Average score in the x rollouts run for each possible spot
        total_score = 0   # Counter for calculating avg_score
        best_score = -100   # Stores the best score here
        best_spot = None   # Stores the spot that gave the best score
        possible_spots = []   # List that will contain all the possible spots
        
        self.findNeighbours(board)   # Call findNeighbours to find the possible spots

         # Create possible_spots (because findNeighbours couldn't return it)
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j].owner == 2:
                    possible_spots.append([i,j])

        # If there are no possible spots              
        if len(possible_spots) == 0:
            return ()
        # If there are possible spots
        else:
            for i in range(len(possible_spots)):   # For each possible spot
                avg_score = 0
                total_score = 0
                for j in range(300):   # Define how many simulations/rollouts will be run
                    player_turn = self.pid   # In each iteration, set which player is playing
                    copy_board = copy.deepcopy(board)   # Use deepcopy so the values of copy_board change but not the original board
                    copy_board[((possible_spots[i])[0])][((possible_spots[i])[1])].owner = player_turn # Place the player's piece in the position being evaluated
                    # Update the cells that need to be changed
                    change_cells = self.findTakeOverCells([(possible_spots[i])[0], (possible_spots[i])[1]], copy_board) 
                    for k in range(len(change_cells)):
                        copy_board[(change_cells[k])[0]][(change_cells[k])[1]].owner = player_turn
                    player_turn = 1 - player_turn   # Switch player
                    # Run the simulation to the end (which runs first for the opponent)
                    score = self.rand_simulate(copy_board, player_turn)
                    total_score = total_score + score   # Update total_score with the score returned by rand_simulate
                
                # After all x rollouts, store the avg score for this specific spot
                avg_score = total_score / 100

                # If this specific spot had a better avg_score than the best_score, then it becomes the best spot
                if avg_score >= best_score:
                    best_score = avg_score
                    best_spot = possible_spots[i]

        best_spot_tuple = tuple(best_spot)   # Convert the list to a tuple

        return best_spot_tuple

     # The rand_simulate function plays the game until the end. It uses the random library.
    # The opponent plays first.
    # Variable: board, player / Uses the findNeighbours_pid and findTakeOverCells_pid functions
    def rand_simulate(self, board, player): 

        # Initialization
        copy_player = 1 - copy.deepcopy(player)   # Deepcopy so that copy_player remembers who the player is (for score evaluation), because player changes value often
        score = None   # The score (of the player) at the end of the game
        rand_spot = []   # List that contains the randomly selected position
        empty_cells = []
        print_board = []   # Board with owner values
        no_move = False   # Boolean that is True when both players cannot make a move

        # Initialize empty_cells which contains the coordinates of the empty spots
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j].owner == -1 or board[i][j].owner == 2:
                    empty_cells.append([i,j])
                    
        # While there are empty spots and at least one player can make a move, do the following:
        while (len(empty_cells) > 0) and (no_move == False):
               
            # Remove the owner = 2 values from the board so there is no overlap with previous iterations
            for i in range(self.size):
                for j in range(self.size):
                    if board[i][j].owner == 2:
                        board[i][j].owner = -1

            # Create and update possible_spots
            possible_spots = self.findNeighbours_pid(board,player)
  
            # If there are possible spots
            if len(possible_spots)>0:
                rand_spot=random.choice(possible_spots)   # Choose a random spot
                change_cells=self.findTakeOverCells_pid(board,rand_spot,player)   # Find the positions that need to be updated
                board[(rand_spot[0])][(rand_spot[1])].owner=player   # Place the player's piece in the random spot
                for i in range(len(change_cells)):  # Place the player's pieces in the positions that need to be changed
                    board[(change_cells[i])[0]][(change_cells[i])[1]].owner=player
                player=1-player   # Change player for the next iteration
                
            # If there are no possible spots for the player
            if len(possible_spots)==0:
                # If neither player has any possible spots, then no_move = True to exit the while loop (game over)
                if (len(self.findNeighbours_pid(board,0))==0) and (len(self.findNeighbours_pid(board,1))==0):    
                    no_move=True
                else:
                    player = 1 - player   # If only one player can't move, just change the playe
            
            # Update empty_cells for the termination condition
            for i in range(self.size):
                for j in range(self.size):
                    if board[i][j].owner==-1 or board[i][j].owner == 2:
                        empty_cells.append([i,j])

        # Calculate score in each simulation
        print_board = [[board[i][j].owner for i in range(self.size)] for j in range(self.size)]
        score = (sum(x.count(copy_player) for x in print_board)) - (sum(x.count(1-copy_player) for x in print_board))

        return score

    # Calls findNeighbours, which runs for player = self.pid from the argument, and returns the possible spots
    # Used in the update of the boolean no_move to check if both players have no move
    # Variable: board, player 
    def findNeighbours_pid(self,board,player):
        copy_pid = copy.deepcopy(self.pid)   # Deepcopy to keep the actual value of self.pid
        self.pid = player   # Set self.pid to the current player (for which player to run findNeighbours)
        possible_spots=[] 
        self.findNeighbours(board)
        # Construct the possible_spots list
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j].owner == 2:
                    possible_spots.append([i,j])
        self.pid = copy_pid   # Restore the original value of self.pid
        return possible_spots

    # Similar logic to the one above. Runs takeOverCells for player = self.pid
    # that we need to check each time. Variable: board, position, player
    def findTakeOverCells_pid(self, board, position, player):
        copy_pid = copy.deepcopy(self.pid) # To prevent changing the actual value of self.pid
        self.pid = player
        change_cells = self.findTakeOverCells(position, board)
        self.pid = copy_pid
        return change_cells

    # Finds the positions that need to change color if we place a piece in a specific position
    # Logic: Starts from the position where the piece will be placed and for each direction the loop will run entirely if it finds only opponent's pieces
    # and when moving in that direction it finds one of our own pieces, it will close the list of positions that need to be changed with extend.
    # No positions with owner = 2 or -1 should be between them. Variable: board
    def findTakeOverCells(self, position, board):

        if position == ():   # If there are no available positions to place, then no color changes
            return []
        else:
            row = position[0]   # unpacking
            col = position[1]   # unpacking
            takeOverCells = []  # List that contains the consecutive opponent's pieces that I find   
            changeCells = []    # It is the extend of the previous one. It also contains one piece of the player's color
            i = row
            j = col 
        
            # In each iteration, takeOverCells is reinitialized so there is no overlap with other iterations
            # The comments apply similarly to all the checks

            # Horizontal right check
            takeOverCells = []
            if col < 7:   # For bounds check
                for m in range(col + 1, self.size):
                    if board[i][m].getOwner() == -1: # If you find an empty space, stop
                        break
                    if board[i][m].getOwner() == 2: # If you find a possible spot, stop
                        break
                    if board[i][m].owner == 1 - self.pid: # If you find an opponent's piece, continue
                        takeOverCells.append([i, m])
                    # If you find your own piece (no gaps with owner -1 or 2 due to construction), close the list
                    if board[i][m].owner == self.pid: 
                        changeCells.extend(takeOverCells)
                        break

            # Horizontal left check
            takeOverCells = []
            if col > 0:   # For bounds check
                for m in range(col - 1, -1, -1):
                    if board[i][m].getOwner() == -1:
                        break
                    if board[i][m].getOwner() == 2:
                        break
                    if board[i][m].owner == 1 - self.pid:
                        takeOverCells.append([i,m])
                    if board[i][m].getOwner() == self.getPid():
                        changeCells.extend(takeOverCells)
                        break

            # Vertical top check
            takeOverCells = []
            if row > 0:   # For bounds check
                for n in range(row - 1, -1, -1):
                    if board[n][j].getOwner() == -1:
                        break
                    if board[n][j].getOwner() == 2:
                       break
                    if board[n][j].getOwner() == 1 - self.getPid():
                        takeOverCells.append([n,j])
                    if board[n][j].getOwner() == self.getPid():
                        changeCells.extend(takeOverCells)
                        break
        
            # Vertical bottom check
            takeOverCells = []
            if row < 7:   # For bounds check
                for n in range(row + 1, self.size):
                    if board[n][j].getOwner() == -1:
                        break
                    if board[n][j].getOwner() == 2:
                        break
                    if board[n][j].getOwner() == 1 - self.getPid():
                        takeOverCells.append([n,j])
                    if board[n][j].getOwner() == self.getPid():
                        changeCells.extend(takeOverCells)
                        break
             
            # Diagonal top-right check
            m1 = min(row, self.size - col - 1) # Για να ορίζονται οι συνθήκες στις if

            takeOverCells = []
            if m1 > 0:   # For bounds check
                for k in range(1, m1+1):
                    if board[i-k][j+k].getOwner() == -1:
                        break
                    if board[i-k][j+k].getOwner() == 2:
                        break 
                    if board[i-k][j+k].getOwner() == 1 - self.getPid():
                        takeOverCells.append([i-k,j+k])
                    if board[i-k][j+k].getOwner() ==  self.getPid():
                        changeCells.extend(takeOverCells)
                        break
        
            # Diagonal top-left check
            m2 = min(row, col)
        
            takeOverCells = []
            if m2 > 0:   # For bounds check
                for t in range(1, m2+1):
                    if board[i-t][j-t].getOwner() == -1:
                        break
                    if board[i-t][j-t].getOwner() == 2:
                        break
                    if board[i-t][j-t].getOwner() == 1 - self.getPid():
                        takeOverCells.append([i-t,j-t])
                    if board[i-t][j-t].getOwner() ==  self.getPid():
                        changeCells.extend(takeOverCells)
                        break
        
            # Diagonal bottom-right check
            m3 = min(self.size - row - 1, self.size - col - 1)

            takeOverCells = []
            if m3 > 0:   # For bounds check
                for r in range(1, m3+1):
                    if board[i+r][j+r].getOwner() == -1:
                         break
                    if board[i+r][j+r].getOwner() == 2:
                        break
                    if board[i+r][j+r].getOwner() == 1 - self.getPid():
                        takeOverCells.append([i+r,j+r])
                    if board[i+r][j+r].getOwner() ==  self.getPid():
                        changeCells.extend(takeOverCells)
                        break

            # Diagonal bottom-left check
            m4 = min(self.size - row - 1, col)

            takeOverCells = []
            if m4 > 0:   # For bounds check
                for s in range(1, m4+1):
                    if board[i+s][j-s].getOwner() == - 1:
                        break
                    if board[i+s][j-s].getOwner() == 2:
                        break
                    if board[i+s][j-s].getOwner() == 1 - self.getPid():
                        takeOverCells.append([i+s,j-s])
                    if board[i+s][j-s].getOwner() ==  self.getPid():
                        changeCells.extend(takeOverCells)
                        break
        
            # Convert to tuple
            changeCellsTuple = []
            for i in range(len(changeCells)):
                changeCellsTuple.append(tuple(changeCells[i]))
        
            return changeCellsTuple

    # Calls the other methods and applies the changes. Variable: board
    def applyChanges(self, board):
        spot = []
        
        spot = self.placeTile(board)   # Where will the player place their piece
        change_cells = self.findTakeOverCells(spot, board)   # Which cells need to change color

        if spot != ():   # If the player had a valid spot, update the board
            board[spot[0]][spot[1]].owner = self.pid
        
        if change_cells != []:   # If the player had a valid spot, update the board
            for i in range(len(change_cells)):
                board[(change_cells[i])[0]][(change_cells[i])[1]].owner = self.pid

        # Remove cells with owner 2 from the board
            for i in range(self.size):
                for j in range(self.size):
                    if board[i][j].owner==2:
                        board[i][j].owner=-1
        
        return board
                
####################################################################
# WARNING: The main program is commented out

if __name__=='__main__':

    """
    WARNING!!!
    To run this as a fast working example of the code,
    in line 135 of the code set the rollouts to a small number, e.g. 3.
    It was not set to a small number by default.
    """
    
    # Define the two players
    a = Reversi26(1,8)
    b = Reversi26(0,8)
    empty_cells = []
    no_move = False
    
    # Define the initial board state
    board = [[Cell(-1) for x in range(a.size)] for y in range(a.size)]
    board[3][3], board[4][4], board[3][4], board[4][3]= Cell(0), Cell(0), Cell(1), Cell(1)

    # Player 0 goes first
    player = 0
                    
    # As long as there are empty cells and at least one player can make a move
    while no_move == False:
               
        if player == 0:
            # If player cannot make a move
            if b.placeTile(board) == ():
                print('----- Player 0 cannot play. Player 1 will play next -----')
                print()
            # If they can, first display available positions
            elif b.placeTile(board) != ():
                print('----- The possible moves for player 0 are as follows -----')
                print()
                b.findNeighbours(board)
                # Print the board with available moves
                for i in range(8):
                    for j in range(8):
                        print(board[i][j].owner, end='\t')
                    print()
                print()
                # Reset owner 2 back to -1 to run applyChanges correctly
                for i in range(8):
                    for j in range(8):
                        if board[i][j].owner == 2:
                            board[i][j].owner = -1
                            
                # Player 0 plays
                board = b.applyChanges(board)
                # Print the updated board
                print('----- Player 0 played. The updated board is -----')
                print()
                for i in range(8):
                    for j in range(8):
                        print(board[i][j].owner, end='\t')
                    print()
                print()

        if player == 1:
            # If player cannot make a move
            if a.placeTile(board) == ():
                print('----- Player 1 cannot play. Player 0 will play next -----')
                print()
            # If they can, first display available positions
            elif a.placeTile(board) != ():
                print('----- The possible moves for player 1 are as follows -----')
                print()
                a.findNeighbours(board)
                # Print the board
                for i in range(8):
                    for j in range(8):
                        print(board[i][j].owner, end='\t')
                    print()
                print()
                # Reset owner 2 back to -1 to run applyChanges correctly
                for i in range(8):
                    for j in range(8):
                        if board[i][j].owner == 2:
                            board[i][j].owner = -1

                # Player 1 plays
                board = a.applyChanges(board)
                # Print the updated board
                print('----- Player 1 played. The updated board is -----')
                print()
                for i in range(8):
                    for j in range(8):
                        print(board[i][j].owner, end='\t')
                    print()
                print()

        # Switch player
        player = 1 - player
        
        # Check if both players cannot play (game over)
        if a.placeTile(board) == () and b.placeTile(board) == ():
            mo_move = True
            break

    # Calculate final score
    print_board = [[board[i][j].owner for i in range(8)] for j in range(8)]
    white_score = (sum(x.count(1) for x in print_board))
    black_score = (sum(x.count(0) for x in print_board)) 
    print('Final score: Black:', black_score, 'White:', white_score)
