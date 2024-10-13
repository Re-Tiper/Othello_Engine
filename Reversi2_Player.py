###################################################################################################################################
# Monte-Carlo Method
###################################################################################################################################

# Δημιουργία παίκτη του παιχνιδιού Reversi

import random
import copy

class Cell:
    
    # Αρχικοποίηση / μεταβλητή: owner
    def __init__(self, owner = -1):
        self.owner = owner  # αρχικοποίηση στην τιμή -1

    # Επιστρέφει την τιμή owner του κελιού 
    def getOwner(self):
        return self.owner

    # Ορίζει την τιμή owner του κελιού και εμφανίζει error αν είναι μη επιτρεπτή / μεταβλητή: owner
    def setOwner(self, owner):
        try:
            self.owner = owner
            if owner not in [-1, 0, 1, 2]:
                raise ValueError("Invalid Value. It should be -1, 0, 1, 2")
        except ValueError as ex:
            print("Error",ex)


class Reversi26:

    # Αρχικοποίηση / μεταβλητή: owner
    def __init__(self, pid = 0, size = 8):
        self.pid = pid
        self.size = size

    # Ορίζει (επιτρεπτή τιμή 0 ή 1) την τιμή pid / μεταβλητή: pid
    def setPid(self, pid):
        try:
            self.pid = pid
            if pid not in [0, 1]:
                raise ValueError("Invalid Value. It should be -0, 1")
        except ValueError as ex:
            print("Error", ex)

    # Επιστρέφει την τιμή pid
    def getPid(self):
        return self.pid

    # Ορίζει (επιτρεπτή τιμή πολλ. 2) το μέγεθος του board / μεταβλητή: size
    def setBoardSize(self, size):
        try:
            self.size = size
            if size%2 != 0:
                raise ValueError("Invalid Value. It should be even number")
        except ValueError as ex:
            print("Error", ex)

    # Επιστρέφει σε string τα ονόματα των φοιτητών
    def getPlayerName(self):
        return "Prevezas_Christos, Tziortzis_Alexandros, Tsaousi_Rebekka"

    
    # Εύρεση πιθανών θέσεων τοποθέτησης πιονιού και αλλαγή του owner attribute σε 2 στο board
    # Βασική Λογική: για κάθε πιόνι του παίκτη σκάναρε προς κάθε κατεύθυνση και αν βρίσκεις
    # συνεχόμενα πιόνια του αντιπάλου και μετά κενή θέση, τότε αυτή η κένη θέση είναι πιθανή θέση 
    # Mεταβλητή: board  
    def findNeighbours(self, board):

        possible_spots = []   # Λίστα όπου θα μπουν οι συντ. που είναι πιθανές θέσεις τοποθέτησης (του παίκτη)
        directions = [(0,1),(1,0),(-1,0),(0,-1),(1,-1),(-1,1),(1,1),(-1,-1)]   # Οι ως διανύσματα κατευθύνσεις
        player_spots = []   # Λίστα όπου θα μπουν τα πιόνια του παίκτη

        # Βάζω τα πιόνια του παίκτη στην player_spots
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j].owner == self.pid:
                    player_spots.append([i,j])

        # Για κάθε πιόνι του παίκτη και για κάθε κετεύθυνση κάνε:
        for i in range(len(player_spots)): 
            for j in range(len(directions)):
                row = (directions[j])[0]   # Το 1ο στοιχείο της j-οστής κατεύθυνσης
                col = (directions[j])[1]   # Το 2ο στοιχείο της j-οστής κατεύθυνσης
                
                # Μέσα στη while οι δύο πρώτες συνθήκες είναι για να ορίζονται τα indexes και η τρίτη είναι η βασική συνθήκη
                # δηλαδή το επόμενο πιόνι προς τη j κατεύθυνση να είναι του αντιπάλου
                while (0 <= (player_spots[i])[0]+row < self.size) and (0 <= (player_spots[i])[1]+col < self.size) and (board[(player_spots[i])[0] + row][(player_spots[i])[1] + col].owner == 1 - self.pid):
                    # Τα ενημερώνω ώστε στην επόμενη επανάληψη να ελέγξω το επόμενο πιόνι στην j κατεύθυνση
                    row = row + (directions[j])[0]
                    col = col + (directions[j])[1]
                    # Οι δύο πρώτες συνθήκες είναι για τα indexes και η 3η είναι αν το επόμενο πιόνι στην j κατεύθυνση είναι κενή θέση
                    # Τότε, η πρώτη κενή θέση που ακολουθείται από συνεχόμενα πιόνια του αντιπάλου είναι πιθανή θέση τοποθέτησης για τον παίκτη
                    if (0 <= (player_spots[i])[0] + row < self.size) and (0 <= (player_spots[i])[1] + col < self.size) and (board[(player_spots[i])[0] + row][(player_spots[i])[1] + col].owner == -1):
                        possible_spots.append([row + (player_spots[i])[0], col + (player_spots[i])[1]])
                        
        # Ενημερώνω το board αφού οι συντ. των πιθανών θέσεων είναι γνωστές
        for i in range(len(possible_spots)):
            board[((possible_spots[i])[0])][((possible_spots[i])[1])].owner = 2
        
        return board


    # Αξιολόγηση της καλύτερης από της πιθανές θέσεις τοποθέτησης με την μέθοδο Pure Monte Carlo όπου για κάθε πιθανή θέση
    # τρέχουν x simulations του παιχνιδιού (με random τρόπο) και επιλέγεται αυτό που δίνει το καλύτερο μέσο score  
    # Μεταβλητή: board / Χρησιμοπεί τη συνάρτηση rand_simulate
    def placeTile(self,board): 
        
        # Αρχικοποίηση
        player_turn = self.pid
        avg_score = 0   # Μέσο score στα x rollouts που έτρεξαν για κάθε πιθανή θέση
        total_score = 0   # Μετρητής για τον υπολογισμό του avg_score
        best_score = -100   # Εδώ αποθηκεύεται το καλύτερο score
        best_spot = None   # Εδώ αποθηκεύεται η θέση που έδωσε το καλύτερο score
        possible_spots = []   # Λίστα που θα περιέχει όλες τις πιθανές θέσεις
        
        self.findNeighbours(board)   # Καλώ την findNeighbours για να βρει τις πιθανές θέσεις

        # Δημιουργία possible_spots (γιατι δεν μπορούσε να το επιστρέφει η findNeighbours)
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j].owner == 2:
                    possible_spots.append([i,j])

        # Αν δεν υπάρχει πιθανή θέση τότε       
        if len(possible_spots) == 0:
            return ()
        # Αν υπάρχει πιθανή θέση τότε
        else:
            for i in range(len(possible_spots)):   # Για κάθε πιθανή θέση
                avg_score = 0
                total_score = 0
                for j in range(300):   # Ορίζω πόσα simulations/rollouts θα γίνουν
                    player_turn = self.pid   # Σε κάθε επανάληψη ορίζω ποιος είναι ο παίκτης
                    copy_board=copy.deepcopy(board)   # Χρησιμοποιώ την deepcopy ώστε να αλλάζουν οι τιμές του copy_board αλλά όχι του αρχικού board
                    copy_board[((possible_spots[i])[0])][((possible_spots[i])[1])].owner = player_turn # Βάζω πιόνι του παίκτη στο θέση για την οποία τρέχει η for
                    # Ενημερώνω τα cells που πρέπει να αλλάξουν
                    change_cells = self.findTakeOverCells([(possible_spots[i])[0], (possible_spots[i])[1]], copy_board) 
                    for k in range(len(change_cells)):
                        copy_board[(change_cells[k])[0]][(change_cells[k])[1]].owner=player_turn
                    player_turn = 1 - player_turn   # Αλλαγή παίκτη
                    # Τρέχω το simulation ως το τέλος (η οποία τρέχει πρώτη φορά για τον αντίπαλο)
                    score = self.rand_simulate(copy_board, player_turn)
                    total_score = total_score + score   # Ενημέρωση του total_score με το score που επέστρεψε η rand_simulate
                
                # Αφού ολοκληρωθούν τα x rollouts κρατάω το avg score για την συγκεκριμένη θέση
                avg_score=total_score/100

                # Αν η συγκεκριμένη θέση είχε καλύτερο avg_score από το best_score τότε αυτή γίνεται η καλύτερη
                if avg_score >= best_score:
                    best_score = avg_score
                    best_spot = possible_spots[i]

        best_spot_tuple = tuple(best_spot)   # Μετατροπή της λίστας σε πλειάδα

        return best_spot_tuple

    # Η rand_simulate παίζει το παιχνίδι ως το τέλος. Χρησιμοποιεί την βιβλιοθήκη random.
    # Πρώτος παίζει ο αντίπαλος.
    # Μεταβλητή: board, player / Χρησιμοποιεί τις findNeighbours_pid και findTakeOverCells_pid
    def rand_simulate(self, board, player): 

        # Αρχικοποίηση
        copy_player = 1 - copy.deepcopy(player)   # Deepcopy ώστε η copy_player να θυμάται ποιος είναι ο παίκτης (για το score evaluation), γιατί η player αλάζει τιμή συχνά
        score = None   # To score (του παίκτη) στο τέλος του παιχνιδιού
        rand_spot = []   # Λίστα που περιέχει την θέση που επιλέγεται τυχαία από τις πιθανές θέσεις
        empty_cells = []
        print_board = []   # Board με τις τιμές owner
        no_move = False   # Boolean που είναι True όταν και οι 2 παίκτες δεν μπορούν να κάνουν κίνηση

        # Αρχικοποίηση empty_cells που περιέχει τις συντ. των κενών θέσεων
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j].owner == -1 or board[i][j].owner == 2:
                    empty_cells.append([i,j])
                    
        # Όσο υπάρχουν κενές θέσεις και τουλάχιστον ένας παίκτης μπορεί να παίξει κάνε:
        while (len(empty_cells) > 0) and (no_move == False):
               
            # Αφαίρεση των owner = 2 values απο το board για να μην υπαρχει επικάλυψη με προηγούμενες επαναλήψεις 
            for i in range(self.size):
                for j in range(self.size):
                    if board[i][j].owner == 2:
                        board[i][j].owner = -1

            # Δημιουργία και ενημέρωση possible_spots
            possible_spots = self.findNeighbours_pid(board,player)
  
            # Αν υπάρχουν πιθανές θέσεις
            if len(possible_spots)>0:
                rand_spot=random.choice(possible_spots)   # Επίλεξε μία τυχαία θέση
                change_cells=self.findTakeOverCells_pid(board,rand_spot,player)   # Βρίσκω ποιες θέσεις πρέπει να ενημερωθούν
                board[(rand_spot[0])][(rand_spot[1])].owner=player   # Βάλε πιόνι του player στην τυχαία θέση
                for i in range(len(change_cells)):  # Βάλε πιόνι του player στις θέσεις που πρέπει να αλλάξουν
                    board[(change_cells[i])[0]][(change_cells[i])[1]].owner=player
                player=1-player   # Αλλαγή παίκτη για την επόμενη επανάληψη
            # Αν δεν υπάρχουν πιθανές θέσεις για τον player
            if len(possible_spots)==0:
                # Αν και οι δύο δεν έχουν πιθανές θέσεις τότε no_move = True για να βγεί από τη while (game over)
                if (len(self.findNeighbours_pid(board,0))==0) and (len(self.findNeighbours_pid(board,1))==0):    
                    no_move=True
                else:
                    player = 1 - player   # Αν μόνο ο ένας δεν μπορεί να παίξει τότε απλά αλάζει ο παίκτης
            
            # Ενημέρωση empty_cells για την τερματική συνθήκη
            for i in range(self.size):
                for j in range(self.size):
                    if board[i][j].owner==-1 or board[i][j].owner == 2:
                        empty_cells.append([i,j])

        # Υπολογισμός score σε κάθε simulation
        print_board = [[board[i][j].owner for i in range(self.size)] for j in range(self.size)]
        score = (sum(x.count(copy_player) for x in print_board)) - (sum(x.count(1-copy_player) for x in print_board))

        return score

    # Καλεί την findNeighbours  η οποία τρέχει για το player = self.pid του ορίσματος και επιστρέφει τις πιθανές θέσεις
    # Την χρησιμοποίησα στην ενημέρωση της boolean no_move για να δω αν και οι δύο παίκτες δεν έχουν κίνηση
    # Μεταβλητή: board, player 
    def findNeighbours_pid(self,board,player):
        copy_pid = copy.deepcopy(self.pid)   # Deepcopy ώστε να κρατήσω την πραγματική τιμή του self.pid
        self.pid = player   # Ορίζω τιμή στο self.pid (=για ποιον παίκτη θα τρέξει η findNeighbours)
        possible_spots=[] 
        self.findNeighbours(board)
        # Κατασκευή του possible_spots
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j].owner == 2:
                    possible_spots.append([i,j])
        self.pid = copy_pid   # Επαναφέρω την πραγματική τιμή του self.pid
        return possible_spots

    # Όμοια λογική με την από πάνω. Τρέχει την takeOverCells  για το payer = self.pid
    # που θέλουμε κάθε φορά. Μεταβλητή: board, position, player
    def findTakeOverCells_pid(self, board, position, player):
        copy_pid = copy.deepcopy(self.pid) # Για να μην αλλάξει η πραγματική τιμή του self.pid
        self.pid = player
        change_cells = self.findTakeOverCells(position, board)
        self.pid = copy_pid
        return change_cells

    # Βρίσκει τις θέσεις που πρέπει να αλλάξουν χρώμα αν βάλουμε πιόνι σε συγκεκριμένη θέση
    # Λογική: ξεκινά από τη θέση που θα μπει το πιόνι και για κάθε κατεύθυνση η for θα τρέξει ολόκληρη αν βρει μόνο πιόνια του αντιπάλου
    # και όταν κινούμενη στην εκάστοτε κατέυθυνση βρει δικό μας πιόνι θα κλείσει την λίστα με τις θέσεις που πρέπει να αλλάξουν χρώμα
    # με την extend. Δεν πρέπει να παρεμβάλλονται θέσεις με owner = 2 ή -1. Μεταβλητή: board
    def findTakeOverCells(self, position, board):

        if position == ():   # Aν δεν υπάρχουν διάθεσιμες θέσεις τοποθέτησης τότε δεν αλλάζει κανένα χρώμα
            return []
        else:
            row = position[0]   # unpacking
            col = position[1]   # unpacking
            takeOverCells = []   # Λίστα που περιέχει τα συνεχόμενα πιόνια του αντιπάλου που βρίσκω    
            changeCells = []   # Είναι η extend της προηγούμενης. Περιέχει έξτρα και ένα πιόνι με το χρώμα του παίκτη
            i = row
            j = col 
        
            # Σε κάθε επανάληψη η takeOverCells αρχικοποιείται για να μην υπάρχει επικάλυψη με άλλες επαναλήψεις
            # Τα σχόλια ισχύουν αντίστοιχα για όλους τους ελέγχους

            #Οριζόντιος δεξιά έλεγχος
            takeOverCells = []
            if col < 7:   #Για να ορίζεται ο έλεγχος
                for m in range(col + 1, self.size):
                    if board[i][m].getOwner() == -1: # Αν βρείς κενή θέση μην συνεχίσεις άλλο
                        break
                    if board[i][m].getOwner() == 2: # Αν βρείς πιθανή θέση μην συνεχίσεις άλλο
                        break
                    if board[i][m].owner == 1-self.pid: # Αν βρείς πιόνι του αντιπάλου συνέχισε
                        takeOverCells.append([i,m])
                    # Αν βρείς δικό σου πιόνι (δεν θα παρεμβάλλονται owner -1 ή 2 λόγω κατασκευής) κλείσε την λίστα 
                    if board[i][m].owner == self.pid: 
                        changeCells.extend(takeOverCells)
                        break

            #Οριζόντιος αριστερά έλεγχος
            takeOverCells = []
            if col > 0:   #Για να ορίζεται ο έλεγχος
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

            #Κάθετος πάνω έλεγχος
            takeOverCells = []
            if row > 0:   #Για να ορίζεται ο έλεγχος
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
        
            #Κάθετος κάτω έλεγχος
            takeOverCells = []
            if row < 7:   #Για να ορίζεται ο έλεγχος
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
             
            #Διαγώνια πάνω δεξιά έλεγχος
            m1 = min(row, self.size - col - 1) # Για να ορίζονται οι συνθήκες στις if

            takeOverCells = []
            if m1 > 0:   # Για να ορίζεται ο έλεγχος
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
        
            #Διαγώνια πάνω αριστερά έλεγχος
            m2 = min(row, col)
        
            takeOverCells = []
            if m2 > 0:   # Για να ορίζεται ο έλεγχος 
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
        
            #Διαγώνια κάτω δεξιά έλεγχος
            m3 = min(self.size - row - 1, self.size - col - 1)

            takeOverCells = []
            if m3 > 0:   # Για να ορίζεται ο έλεγχος
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

            #Διαγώνια κάτω αριστερά έλεγχος
            m4 = min(self.size - row - 1, col)

            takeOverCells = []
            if m4 > 0:   # Για να ορίζεται ο έλεγχος 
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
        
            #Μετατροπή σε πλειάδα
            changeCellsTuple = []
            for i in range(len(changeCells)):
                changeCellsTuple.append(tuple(changeCells[i]))
        
            return changeCellsTuple

    # Καλεί τις άλλες και εφαρμόζει τις αλλαγές. Μεταβλητή: board
    def applyChanges(self, board):
        spot = []
        
        spot = self.placeTile(board)   # Που θα βάλει ο παίκτης
        change_cells = self.findTakeOverCells(spot, board)   # Ποια κελιά πρέπει να αλλάξουν χρώμα

        if spot != ():   # Αν ο παίκτης είχε διαθέσιμη θέση ενημερώνω το board
            board[spot[0]][spot[1]].owner = self.pid
        
        if change_cells != []:   # Αν ο παίκτης είχε διαθέσιμη θέση ενημερώνω το board
            for i in range(len(change_cells)):
                board[(change_cells[i])[0]][(change_cells[i])[1]].owner = self.pid

        # Αφαίρεση των cell με owner 2 από το board
            for i in range(self.size):
                for j in range(self.size):
                    if board[i][j].owner==2:
                        board[i][j].owner=-1
        
        return board
                
####################################################################
# ΠΡΟΣΟΧΗ: Το main πρόγραμμα είναι commented out

# Κυρίως πρόγραμμα
if __name__=='__main__':

    """
    ΠΡΟΣΟΧΗ!!!
    Για να τρέξει γρήγορα αυτό το παράδειγμα καλής λειτουργίας του κώδικα
    στην γραμμή 135 του κώδικα ορίστε τα rollouts σε κάποιον μικρό αριθμό πχ 3.
    Δεν μπήκε μικρό νούμερο by default ώστε να μην χρειαστεί να το αλλάξουμε στο τουρνουά.
    """
    
    # Ορισμός των δύο παικτών
    a = Reversi26(1,8)
    b = Reversi26(0,8)
    empty_cells = []
    no_move = False
    
    # Ορισμός αρχικής καταστάσης board
    board = [[Cell(-1) for x in range(a.size)] for y in range(a.size)]
    board[3][3], board[4][4], board[3][4], board[4][3]= Cell(0), Cell(0), Cell(1), Cell(1)

    # Πρώτος θα παίξει ο παίκτης 0
    player = 0
                    
    # Όσο υπάρχουν κενά κελιά και πιθανές κινήσεις για τουλάχιστον έναν παίκτη παίζε
    while no_move == False:
               
        if player == 0:
            # Αν ο παίκτης δεν μπορεί να παίξει
            if b.placeTile(board) == ():
                print('----- Ο παίκτης 0 δεν μπορεί να παίξει. Θα παίξει ο 1 -----')
                print()
            # Αν μπορεί πρώτα εμφανίζω τις διαθέσιμες θέσεις
            elif b.placeTile(board) != ():
                print('----- Οι πιθανές θέσεις του παίκτη 0 είναι οι ακόλουθες -----')
                print()
                b.findNeighbours(board)
                # Tυπώνω το board με τις διαθέσιμες θέσεις
                for i in range(8):
                    for j in range(8):
                        print(board[i][j].owner, end='\t')
                    print()
                print()
                # Αφαιρώ ξανά τα owner 2 για να τρέξει σωστά η applyChanges
                for i in range(8):
                    for j in range(8):
                        if board[i][j].owner==2:
                            board[i][j].owner=-1
                            
                # Παίζει ο παίκτης 0
                board = b.applyChanges(board)
                # Τυπώνω το board
                print('----- Έπαιξε ο παίκτης 0. Το ενημερωμένο board είναι -----')
                print()
                for i in range(8):
                    for j in range(8):
                        print(board[i][j].owner, end='\t')
                    print()
                print()

        if player == 1:
            # Αν ο παίκτης δεν μπορεί να παίξει
            if a.placeTile(board) == ():
                print('----- Ο παίκτης 1 δεν μπορεί να παίξει. Θα παίξει ο 0 -----')
                print()
            # Αν μπορεί πρώτα εμφανίζω τις διαθέσιμες θέσεις
            elif a.placeTile(board) != ():
                print('----- Οι πιθανές θέσεις του παίκτη 1 είναι οι ακόλουθες -----')
                print()
                a.findNeighbours(board)
                # Tυπώνω το board
                for i in range(8):
                    for j in range(8):
                        print(board[i][j].owner, end='\t')
                    print()
                print()
                # Αφαιρώ ξανά τα owner 2 για να τρέξει σωστά η applyChanges
                for i in range(8):
                    for j in range(8):
                        if board[i][j].owner==2:
                            board[i][j].owner=-1

                # Pαίζει ο παίκτης 1
                board = a.applyChanges(board)
                # Τυπώνω το board
                print('----- Έπαιξε ο παίκτης 0. Το ενημερωμένο board είναι -----')
                print()
                for i in range(8):
                    for j in range(8):
                        print(board[i][j].owner, end='\t')
                    print()
                print()

        # Αλλαγή παίκτη
        player = 1 - player
        
        # Έλεγχος αν και οι δύο παίκτες δεν μπορούν να παίξουν (game over) 
        if a.placeTile(board) == () and b.placeTile(board) == ():
            mo_move = True
            break

    # Υπολογισμός τελικού score
    print_board = [[board[i][j].owner for i in range(8)] for j in range(8)]
    white_score = (sum(x.count(1) for x in print_board))
    black_score = (sum(x.count(0) for x in print_board)) 
    print('Τελικό score: Μαύρος:',black_score,'Λευκός:',white_score)
