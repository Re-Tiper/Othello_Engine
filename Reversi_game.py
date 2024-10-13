# --- Replace X with the number of your team ---
import Reversi as RP  # ReversiX_Player
import Reversi26_Player as RP26
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

#Set board size
board_size = 8

# --- Set delay to a higher number if you want to have a bigger delay between the moves ---
delay = 2

#Initial board
board = [[RP.Cell(-1) for x in range(board_size)] for y in range(board_size)]
board[3][3], board[4][4], board[3][4], board[4][3] = RP.Cell(0), RP.Cell(0), RP.Cell(1), RP.Cell(1)
         
# Transform the board for the UI
print_board = [[board[x][y].getOwner() for y in range(board_size)] for x in range(board_size)]

# UI initialisation
cmap = colors.ListedColormap(['green', 'black', 'white'])
bounds = [-1.5, -0.5, 0.5, 1.5]
norm = colors.BoundaryNorm(bounds, cmap.N)

fig, ax = plt.subplots()
ax.imshow(print_board, cmap=cmap, norm=norm)

ax.grid(which='major', axis='both', linestyle='-', color='gray', linewidth=1.5)
ax.set_xticks(np.arange(-.5, board_size, 1));
ax.set_yticks(np.arange(-.5, board_size, 1));
ax.xaxis.set_tick_params(labelbottom=False)
ax.yaxis.set_tick_params(labelleft=False)
plt.title('Black: ' + str(sum(x.count(0) for x in print_board)) + '\nWhite: ' + str(sum(x.count(1) for x in print_board)),fontsize=14)
plt.show(block=False)
plt.pause(delay)

#Player 1 is black
player1 = RP.Reversi30(0, 8)  # --- Replace X with the number of your team ---
#Player 2 is white
player2 = RP26.Reversi26(1, 8)  # --- Replace X with the number of your team ---

#Initialisation 
player_turn = 1
empty_cells = sum(x.count(-1) for x in print_board)
no_move = False
no_move_before = False

#Play game
while empty_cells>0 & (not no_move):
    empty_cells_before = sum(x.count(-1) for x in print_board)
    
    if player_turn == 1:
        board = player1.applyChanges(board)
        player_turn = 2
    else:
        board = player2.applyChanges(board)
        player_turn = 1

    #Update UI
    print_board = [[board[x][y].getOwner() for y in range(board_size)] for x in range(board_size)]
    ax.imshow(print_board, cmap=cmap, norm=norm)
    plt.title('Black: ' + str(sum(x.count(0) for x in print_board)) + '\nWhite: ' + str(sum(x.count(1) for x in print_board)),fontsize=14)
    plt.show(block=False)
    plt.pause(delay)

    #Calculate the number of empty cells
    empty_cells = sum(x.count(-1) for x in print_board)

    #Identify if both players cannot make more moves
    no_move_current = not bool(empty_cells_before - empty_cells)
    no_move = no_move_before & no_move_current
    no_move_before = no_move_current
