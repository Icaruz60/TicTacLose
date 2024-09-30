#w0780459
#Coded by Gerrit Visser

import random
import pygame
from time import sleep

def play_game(a):
    pygame.init() #initialize pygame and display
    pygame.display.init()
    global MovesMadeCount
    MovesMadeCount = 0
    PlayerMoveMade = a
    # Screen setup
    window_size = 500 #define window size
    window = pygame.display.set_mode((window_size, window_size), vsync=1)
    #Load and scale gridsprite
    background = pygame.image.load("C:\\Users\\busin\\OneDrive\\Dokumente\\TicTacToe\\Resources\\tttgrid.png").convert()
    background = pygame.transform.scale(background, window.get_size())

    # Load and scale X and O Sprites
    redx = pygame.image.load("C:\\Users\\busin\\OneDrive\\Dokumente\\TicTacToe\\Resources\\tttx.png").convert_alpha()
    redx = pygame.transform.scale(redx, (131, 131))

    blueo = pygame.image.load("C:\\Users\\busin\\OneDrive\\Dokumente\\TicTacToe\\Resources\\ttto.png").convert_alpha()
    blueo = pygame.transform.scale(blueo, (131, 131))
    # Load, scale, and position Win Message Sprites
    RedWon = pygame.image.load("C:\\Users\\busin\\OneDrive\\Dokumente\\TicTacToe\\Resources\\RedWon.png")
    RedWon = pygame.transform.scale(RedWon,(450,65))

    BlueWon = pygame.image.load("C:\\Users\\busin\\OneDrive\\Dokumente\\TicTacToe\\Resources\\BlueWon.png")
    BlueWon = pygame.transform.scale(BlueWon,(450,65))

    # Define coordinates for each field (top-left corner of each cell)
    field_coords = [
        (26.31, 26.31), (184.17, 26.31), (342.03, 26.31),
        (26.31, 184.17), (184.17, 184.17), (342.03, 184.17),
        (26.31, 342.03), (184.17, 342.03), (342.03, 342.03)
    ]

    # Track the state of the board
    board = [None, None, None, None, None, None, None, None, None] #array that hold the values of the moves

    def get_square(pos): # check if player has clicked into a field
        x, y = pos
        for field in range(9):
             field_x, field_y = field_coords[field]
             # Check if the click is inside the boundaries of the current field
             if field_x <= x <= field_x + 131 and field_y <= y <= field_y + 131:  # Assuming field size is 131x131
                 return field
        return None

    def detectwin():
        #check if redwon
        if board[0] == "X" and board[1] == "X" and board[2] == "X" or board[3] == "X" and board[4] == "X" and board[
            5] == "X" or board[6] == "X" and board[7] == "X" and board[8] == "X" or board[0] == "X" and board[
            3] == "X" and board[6] == "X" or board[1] == "X" and board[4] == "X" and board[7] == "X" or board[
            2] == "X" and board[5] == "X" and board[8] == "X" or board[0] == "X" and board[4] == "X" and board[
            8] == "X" or board[2] == "X" and board[4] == "X" and board[6] == "X":
            print("RED WON") # console prints redwon for development purposes only
            window.blit(RedWon, (25, 220)) #display the redwon message
            pygame.display.update() #update display
            gameover() #trigger the gameover
        #check if Blue Won
        elif board[0] == "O" and board[1] == "O" and board[2] == "O" or board[3] == "O" and board[4] == "O" and board[
            5] == "O" or board[6] == "O" and board[7] == "O" and board[8] == "O" or board[0] == "O" and board[
            3] == "O" and board[6] == "O" or board[1] == "O" and board[4] == "O" and board[7] == "O" or board[
            2] == "O" and board[5] == "O" and board[8] == "O" or board[0] == "O" and board[4] == "O" and board[
            8] == "O" or board[2] == "O" and board[4] == "O" and board[6] == "O":
            print("Blue WON") # console prints bluewon for development purposes only
            window.blit(BlueWon, (25, 220)) #display the bluewon message
            pygame.display.update() #update display
            gameover() #trigger the gameover

    def gameover():
        sleep(2) #wait 2 seconds
        play_game(False) #resets game

    def fullboard():
        global MovesMadeCount
        if (MovesMadeCount == 9): #check if the board is full and if so reset the game
            sleep(1)
            if(a == True):
                play_game(False)
            elif(a == False):
                play_game(True)

    def drawboard():
        window.fill((0, 0, 0))  # whites out screen
        window.blit(background, (0, 0))  # displays grid

        # displays Xs and Os played
        for field in range(9):
            field_x, field_y = field_coords[field]
            if board[field] == "X":
                window.blit(redx, (field_x, field_y))
            elif board[field] == "O":
                window.blit(blueo, (field_x, field_y))
        pygame.display.update()  # update game display

    def minimax(board, depth, is_maximizing):
        #evaluate the board
        score = evaluate(board)
        if score != 0 or is_full(board):
            return score

        if is_maximizing: #maximizing algorithm
            best_score = -float('inf') #start off with small number
            for i in range(9): #check for each field
                if board[i] is None:
                    board[i] = "O"  # Bot is "O"
                    score = minimax(board, depth + 1, False) #recursive function checking for best move
                    board[i] = None  # Undo move
                    best_score = max(score, best_score) #returns best move
            return best_score#returns best move
        else: #minimizing algorithm
            best_score = float('inf')
            for i in range(9):#check for each field
                if board[i] is None:
                    board[i] = "X"  # Player is "X"
                    score = minimax(board, depth + 1, True)#recursive function checking for best move
                    board[i] = None  # Undo move
                    best_score = min(score, best_score)#returns best move
            return best_score#returns best move

    def evaluate(board):
        #Evaluates the current board state. Returns 1 if bot wins, -1 if player wins, and 0 if tie.
        win_conditions = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)  # Diagonals
        ]
        for condition in win_conditions:
            a, b, c = condition
            if board[a] == board[b] == board[c] and board[a] is not None:
                if board[a] == "O":
                    return 1  # Bot wins
                elif board[a] == "X":
                    return -1  # Player wins
        return 0  # Tie or unfinished

    def is_full(board):
        #Checks if the board is full (tie).
        return all(field is not None for field in board)

    def best_move():
        #Determines the best move for the bot using the minimax algorithm.
        best_score = -float('inf')
        move = None
        for i in range(9):
            if board[i] is None:
                board[i] = "O"  # Assume bot makes the move
                score = minimax(board, 0, False)
                board[i] = None  # Undo move
                if score > best_score: #check for best possible move
                    best_score = score
                    move = i
        return move

    def botmove():
        move = best_move()  # Get the optimal move from Minimax
        if move is not None:
            board[move] = "O"  # Place O at optimal move

    running = True #running loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #quit game if windows X icon has been clicked
                running = False
            #check if players have clicked into a field
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                field = get_square(mouse_pos)

                # Check if the click is inside the grid and the square is empty
                if field is not None and board[field] is None:
                    board[field] = "X"  # Place current player's mark
                    print(board) #shows board state in console (for development purposes)
                    MovesMadeCount += 1 # Additional move has been made
                    PlayerMoveMade = True





        drawboard()

        detectwin() #detect if a player won
        pygame.display.update() #update game display

        fullboard()

        if(PlayerMoveMade == True):
            botmove()
            MovesMadeCount += 1
            PlayerMoveMade = False

    pygame.quit()

play_game(False)