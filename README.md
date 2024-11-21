# Reversi_Player
Algorithms for reversi/othello. One deterministic and one using Monte Carlo simulations. <br>
The algorithm uses Monte Carlo Tree Search (MCTS) in a simplified form. The Monte Carlo simulations are used to estimate the value of a move by simulating random future plays and determining which move has the best expected outcome based on random sampling. <br>
By running many random simulations and averaging the results, the algorithm can approximate the "value" of a move without needing a perfect lookahead strategy like minimax.
