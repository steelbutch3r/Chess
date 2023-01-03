import numpy as np

# GLOBAL VARIABLES
ROWS = 8
COLUMNS = 8

WHITE_COLOR = (255,255,255)
BLACK_COLOR = (0,0,0)
RED_COLOR = (255,0,0)
BLACK_PIECE = (165,42,42)
WHITE_PIECE = (245,245,220)


FREE = []
CURRENT_WHITE = []
CURRENT_BLACK = []
turn = 0

castlew = [0, 0, 0]
castleb = [0, 0, 0]


# White pieces: 1= pawn, 2 = rook, 3 = knight, 4 = bishop, 5 = queen, 6 = king
WHITE = [1,2,3,4,5,6]
WHITE_BACK_ROW = [2,3,4,6,5,4,3,2]
WHITE_FRONT_ROW = [1,1,1,1,1,1,1,1]

# Black pieces: 7 = pawn, 8 = rook, 9 = knight, 10 = bishop, 11 = queen, 12 = king
BLACK = [7,8,9,10,11,12]
BLACK_BACK_ROW = [8,9,10,12,11,10,9,8]
BLACK_FRONT_ROW = [7,7,7,7,7,7,7,7]

# All pieces
ALL_PIECES = [WHITE, BLACK]
ALL_NAMES = [['Pawn', 'Rook', 'Knight', 'Bishop', 'Queen', 'King'],['Pawn', 'Rook', 'Knight', 'Bishop', 'Queen', 'King']]


class Piece(object):
    def __init__(self, x, y, piece_id, team):
        self.x = x
        self.y = y
        self.piece_id = piece_id
        self.team = team
        self.name = ALL_NAMES[team][ALL_PIECES[team].index(piece_id)]



######################################## ALWAYS USED

def create_board():
    board = np.zeros((ROWS, COLUMNS))
    for i in range(ROWS):
        if i == 0:
            board[i] = WHITE_BACK_ROW
        elif i == 1:
            board[i] = WHITE_FRONT_ROW
        elif i == 6:
            board[i] = BLACK_FRONT_ROW
        elif i == 7:
            board[i] = BLACK_BACK_ROW

    return board


def free_space(board):
    for i in range(ROWS):
        for j in range(COLUMNS):
            if board[i][j] == 0:
                FREE.append((j,i))
    return FREE


def white_occupied(board, WHITE):
    for i in range(ROWS):
        for j in range(COLUMNS):
            if board[i][j] in WHITE:
                CURRENT_WHITE.append((j,i))
                Piece(j, i, int(board[i][j]), 0)

    return CURRENT_WHITE, Piece


def black_occupied(board, BLACK):
    for i in range(ROWS):
        for j in range(COLUMNS):
            if board[i][j] in BLACK:
                CURRENT_BLACK.append((j,i))
                Piece(j, i, int(board[i][j]), 1)
    
    return CURRENT_BLACK, Piece


def determine_piece_id(x, y, board):
    piece_id = int(board[y][x])

    return piece_id


def list_of_moves(piece):
    POSSIBLE_MOVES = []
    POSSIBLE_ATTACKS = []

    if piece.name == 'Pawn':
        if piece.team == 0 and not at_bottom_edge(piece):
            pawn_one = (piece.x, piece.y + 1)
            POSSIBLE_MOVES.append(pawn_one)

            if piece.y == 1:
                pawn_two = (piece.x, piece.y + 2)
                POSSIBLE_MOVES.append(pawn_two)

            if (piece.x-1, piece.y+1) in CURRENT_BLACK:
                pawn_attack_one = (piece.x-1, piece.y+1)
                POSSIBLE_ATTACKS.append(pawn_attack_one)

            if (piece.x+1, piece.y+1) in CURRENT_BLACK:
                pawn_attack_two = (piece.x+1, piece.y+1)
                POSSIBLE_ATTACKS.append(pawn_attack_two)

            return POSSIBLE_MOVES, POSSIBLE_ATTACKS

        
        elif piece.team == 1 and not at_top_edge(piece):
            pawn_one = (piece.x, piece.y - 1)
            POSSIBLE_MOVES.append(pawn_one)

            if piece.y == 6:
                pawn_two = (piece.x, piece.y - 2)
                POSSIBLE_MOVES.append(pawn_two)

            if (piece.x-1, piece.y-1) in CURRENT_WHITE:
                pawn_attack_one = (piece.x-1, piece.y-1)
                POSSIBLE_ATTACKS.append(pawn_attack_one)

            if (piece.x+1, piece.y-1) in CURRENT_WHITE:
                pawn_attack_two = (piece.x+1, piece.y-1)
                POSSIBLE_ATTACKS.append(pawn_attack_two)


            return POSSIBLE_MOVES, POSSIBLE_ATTACKS


    if piece.name == 'Rook':
        north = piece.y + 1
        south = ROWS - piece.y
        west = piece.x + 1
        east = COLUMNS - piece.x
        north_moves = []
        south_moves = []
        west_moves = []
        east_moves = []

        for i in range(1, north):
            move = (piece.x, piece.y-i)
            POSSIBLE_MOVES.append(move)
            north_moves.append(move)

        for i in range(1, south):
            move = (piece.x, piece.y+i)
            POSSIBLE_MOVES.append(move)
            south_moves.append(move)

        for i in range(1, west):
            move = (piece.x-i, piece.y)
            POSSIBLE_MOVES.append(move)
            west_moves.append(move)

        for i in range(1, east):
            move = (piece.x+i, piece.y)
            POSSIBLE_MOVES.append(move)
            east_moves.append(move)

        return north_moves, south_moves, west_moves, east_moves

    if piece.name == 'Knight':
        list = [[1, 2], [-1, 2], [-1, -2], [1, -2], [2, 1], [-2, 1], [-2, -1], [2, -1]]
        for i in list:
            x_movement = piece.x + int(i[0])
            y_movement = piece.y + int(i[1])
            move = (x_movement, y_movement)
            if x_movement >= 0 and x_movement <= 7 and y_movement >= 0 and y_movement <= 7:
                POSSIBLE_MOVES.append(move)
        
        return POSSIBLE_MOVES

    if piece.name == 'Bishop':
        LR = []
        UR = []
        LL = []
        UL = []
        # Lower right diagonal
        for i in range(1, ROWS):
            move = (piece.x + i, piece.y + i)
            POSSIBLE_MOVES.append(move)
            if piece.x + i > 7 or piece.y + i > 7:
                break
            LR.append(move)

        # Upper right diagonal
        for i in range(1, ROWS):
            move = (piece.x + i, piece.y - i)
            POSSIBLE_MOVES.append(move)
            if piece.x + i > 7 or piece.y - i < 0:
                break
            UR.append(move)

        # Lower left diagonal
        for i in range(1, ROWS):
            move = (piece.x - i, piece.y + i)
            POSSIBLE_MOVES.append(move)
            if piece.x - i < 0 or piece.y + i > 7:
                break
            LL.append(move)

        # Upper left diagonal
        for i in range(1, ROWS):
            move = (piece.x - i, piece.y - i)
            POSSIBLE_MOVES.append(move)

            if piece.x - i < 0 or piece.y - i < 0:
                break
            UL.append(move)

        return LR, UR, LL, UL


    if piece.name == 'Queen':
        # Diagonals
        LR = []
        UR = []
        LL = []
        UL = []
        # Lower right diagonal
        for i in range(1, ROWS):
            move = (piece.x + i, piece.y + i)
            POSSIBLE_MOVES.append(move)
            if piece.x + i > 7 or piece.y + i > 7:
                break
            LR.append(move)

        # Upper right diagonal
        for i in range(1, ROWS):
            move = (piece.x + i, piece.y - i)
            POSSIBLE_MOVES.append(move)
            if piece.x + i > 7 or piece.y - i < 0:
                break
            UR.append(move)

        # Lower left diagonal
        for i in range(1, ROWS):
            move = (piece.x - i, piece.y + i)
            POSSIBLE_MOVES.append(move)
            if piece.x - i < 0 or piece.y + i > 7:
                break
            LL.append(move)

        # Upper left diagonal
        for i in range(1, ROWS):
            move = (piece.x - i, piece.y - i)
            POSSIBLE_MOVES.append(move)
            if piece.x - i < 0 or piece.y - i < 0:
                break
            UL.append(move)

        # Straights
        north = piece.y + 1
        south = ROWS - piece.y
        west = piece.x + 1
        east = COLUMNS - piece.x
        north_moves = []
        south_moves = []
        west_moves = []
        east_moves = []

        for i in range(1, north):
            move = (piece.x, piece.y-i)
            POSSIBLE_MOVES.append(move)
            north_moves.append(move)

        for i in range(1, south):
            move = (piece.x, piece.y+i)
            POSSIBLE_MOVES.append(move)
            south_moves.append(move)

        for i in range(1, west):
            move = (piece.x-i, piece.y)
            POSSIBLE_MOVES.append(move)
            west_moves.append(move)

        for i in range(1, east):
            move = (piece.x+i, piece.y)
            POSSIBLE_MOVES.append(move)
            east_moves.append(move)

        return north_moves, south_moves, west_moves, east_moves, LR, UR, LL, UL

    if piece.name == 'King':
        castle_moves = []

        for i in range(-1, 2):
            for t in range(-1, 2):
                move = (piece.x+t, piece.y+i)
                if piece.x+t <= 7 and piece.x+t >= 0 and piece.y+i <= 7 and piece.y+i >= 0 and move != (piece.x, piece.y):
                    POSSIBLE_MOVES.append(move)

        castle = can_castle()
        if castle == 'Left':
            left = (piece.x-2, piece.y)
            castle_moves.append(left)

        elif castle == 'Right':
            right = (piece.x+3, piece.y)
            castle_moves.append(right)

        elif castle == 'Both':
            left = (piece.x-2, piece.y)
            castle_moves.append(left)
            right = (piece.x+3, piece.y)
            castle_moves.append(right)
        return POSSIBLE_MOVES, castle_moves

    return False


def valid_move(piece, x, y):
    LIST = list_of_moves(piece)
    if x >= 0 and x <= 7 and y >= 0 and y <= 7:
        if piece.name == 'Pawn':
                if (x, y) in LIST[1]:
                    return 'attack'

                elif (x,y) in LIST[0]:
                    return 'move'

        elif piece.name == 'King':
            if (x, y) in LIST[0]:
                return True

            elif (x, y) in LIST[1]:
                return 'castle'

        elif piece.name == 'Knight':
            if (x, y) in LIST:
                return True

        for i in LIST:
            if (x, y) in i:
                return True

    return False


def king_valid_move(board):
    MOVES = []
    x, y = king_coords(board)

    for i in range(-1, 2):
        for t in range(-1, 2):
            move = (x+t, y+i)
            if x+t <= 7 and x+t >= 0 and y+i <= 7 and y+i >= 0:
                MOVES.append(move)

    return MOVES


def pawn_promotion(board):
    for i in range(ROWS):
        for j in range(COLUMNS):
            if i == 0:
                if board[i][j] == 7:
                    board[i][j] = 11

            if i == 7:
                if board[i][j] == 1:
                    board[i][j] = 5
    return board
########################################### CAN_MOVE

def pawn_can_move(piece, x, y):
    loop = 0
    move_y = y - piece.y
    if piece.team == 0:

        # Loop through each spot in front of the pawn consecutively based on the input (1 or 2 spaces)
        for i in range(move_y+1):
            # If the space is free
            if (piece.x, piece.y+i) in FREE:
                loop += 1
            
            if loop == move_y:
                return True
        
    if piece.team == 1:
        pos_movement = move_y * -1

        for i in range(pos_movement+1):
            if (piece.x, piece.y-i) in FREE:
                loop += 1

            if loop == pos_movement:
                return True
            
    return False


def rook_can_move(rook, x, y):
    x_movement = x - rook.x
    y_movement = y - rook.y
    loop = 0
    input = (x, y)

    # Move right
    if x_movement > 0:
        for i in range(x_movement+1):
            if (rook.x+i, rook.y) in FREE:
                loop += 1
                
        if loop == x_movement:
            return True

        if loop+1 == x_movement:
            if rook.team == 0 and input in CURRENT_BLACK:
                return True
            if rook.team == 1 and input in CURRENT_WHITE:
                return True
            #return False

    # Move left
    if x_movement < 0:
        pos_move = (x_movement* -1)
        for i in range(pos_move+1):
            if (rook.x-i, rook.y) in FREE:
                loop += 1

        if loop == pos_move:
            return True

        if loop+1 == pos_move:
            if rook.team == 0 and input in CURRENT_BLACK:
                return True
            if rook.team == 1 and input in CURRENT_WHITE:
                return True
            #return False

    # Move down
    if y_movement > 0:
        for i in range(y_movement+1):
            if (rook.x, rook.y+i) in FREE:
                loop += 1
                
        if loop == y_movement:
            return True

        if loop+1 == y_movement:
            if rook.team == 0 and input in CURRENT_BLACK:
                return True
            if rook.team == 1 and input in CURRENT_WHITE:
                return True
            #return False

    # Move up
    if y_movement < 0:
        pos_move = (y_movement * -1)
        for i in range(pos_move+1):
            if (rook.x, rook.y-i) in FREE:
                loop += 1
                
        if loop == pos_move:
            return True

        if loop+1 == pos_move:
            if rook.team == 0 and input in CURRENT_BLACK:
                return True
            if rook.team == 1 and input in CURRENT_WHITE:
                return True
            #return False
    
    return False



def knight_can_move(knight, x, y):
    if (x, y) in FREE:
        return True

    if knight.team == 0 and (x, y) in CURRENT_BLACK:
        return True

    if knight.team == 1 and (x, y) in CURRENT_WHITE:
        return True
    
    return False


def bishop_can_move(bishop, x, y):
    bx = x - bishop.x
    by = y - bishop.y
    move = abs(bx)
    loop = 0

    if bx > 0 and by > 0:
        for i in range(move + 1):
            if (bishop.x + i, bishop.y + i) in FREE:
                loop += 1

    if bx > 0 and by < 0:
        for i in range(move + 1):
            if (bishop.x + i, bishop.y - i) in FREE:
                loop += 1

    if bx < 0 and by > 0:
        for i in range(move + 1):
            if (bishop.x - i, bishop.y + i) in FREE:
                loop += 1

    if bx < 0 and by < 0:
        for i in range(move + 1):
            if (bishop.x - i, bishop.y - i) in FREE:
                loop += 1

    if loop == move:
        return True

    if loop+1 == move:
        if bishop.team == 0 and (x, y) in CURRENT_BLACK:
            return True
        if bishop.team == 1 and (x, y) in CURRENT_WHITE:
            return True

    else:
        return False

    
def king_can_move(board, x, y):
    enemy_king_defense = king_vs_king(board)
    input = (x, y)

    if input in FREE and input not in enemy_king_defense and not in_check(board, x, y):
        return True

    if turn == 0:
        if input in CURRENT_BLACK:
            return True
        
    if turn == 1:
        if input in CURRENT_WHITE:
            return True
    
    return False


def piece_can_move(piece, x, y):

    if piece.name == 'Rook':
        if rook_can_move(piece, x, y):
            return True

    if piece.name == 'Bishop':
        if bishop_can_move(piece, x, y):
            return True

    if piece.name == 'Queen':
        x = abs(x - piece.x)
        y = abs(y - piece.y)
        if x == y:
            if bishop_can_move(piece, x, y):
                return True
        else:
            if rook_can_move(piece, x, y):
                return True

    if piece.name == 'Knight':
        if knight_can_move(piece, x, y):
            return True

    return False


def cannot_move_check(piece, board, mx, my):
    if turn == 0:
        CURRENT_WHITE.remove((piece.x, piece.y))
        CURRENT_WHITE.append((mx, my))

        if king_in_check(board):
            CURRENT_WHITE.remove((mx, my))
            CURRENT_WHITE.append((piece.x, piece.y))
            return True

        CURRENT_WHITE.remove((mx, my))
        CURRENT_WHITE.append((piece.x, piece.y))

    else:
        CURRENT_BLACK.remove((piece.x, piece.y))
        CURRENT_BLACK.append((mx, my))

        if king_in_check(board):
            CURRENT_BLACK.remove((mx, my))
            CURRENT_BLACK.append((piece.x, piece.y))
            return True

        CURRENT_BLACK.remove((mx, my))
        CURRENT_BLACK.append((piece.x, piece.y))

    return False


################################ PIECE_LISTS



def pawn_list(piece):
    move_list = []
    MOVES, ATTACKS = list_of_moves(piece)

    for i in MOVES:
        if i in FREE:
            move_list.append(i)
        else:
            break

    for i in ATTACKS:
        if turn == 0:
            if i in CURRENT_BLACK:
                move_list.append(i)

        else:
            if i in CURRENT_WHITE:
                move_list.append(i)
        
    return move_list
    

def rook_list(piece):
    move_list = []
    please_work = list_of_moves(piece)

    for i in please_work:
        for sub in i:
            if sub in FREE:
                move_list.append(sub)
                continue

            if turn == 0:
                if sub in CURRENT_BLACK:
                    move_list.append(sub)
                    break

                if sub in CURRENT_WHITE:
                    break

            if turn == 1:
                if sub in CURRENT_WHITE:
                    move_list.append(sub)
                    break

                if sub in CURRENT_BLACK:
                    break
    
    return move_list


def knight_list(piece):
    move_list = []
    MOVES = list_of_moves(piece)

    for i in MOVES:
        if turn == 0:
            if i not in CURRENT_WHITE:
                move_list.append(i)

        else:
            if i not in CURRENT_BLACK:
                move_list.append(i)

    return move_list


def bishop_list(piece):
    move_list = []
    list = list_of_moves(piece)

    for i in list:
        for sub in i:
            if sub in FREE:
                move_list.append(sub)
                continue

            if turn == 0:
                if sub in CURRENT_BLACK:
                    move_list.append(sub)
                    break

                if sub in CURRENT_WHITE:
                    break

            if turn == 1:
                if sub in CURRENT_WHITE:
                    move_list.append(sub)
                    break

                if sub in CURRENT_BLACK:
                    break
    
    return move_list


def queen_list(piece):
    move_list = []
    north_moves, south_moves, west_moves, east_moves, LR, UR, LL, UL = list_of_moves(piece)
    rook = [north_moves, south_moves, west_moves, east_moves]
    bishop = [LR, UR, LL, UL]

    for i in bishop:
        for sub in i:
            if sub in FREE:
                move_list.append(sub)
                continue

            if turn == 0:
                if sub in CURRENT_BLACK:
                    move_list.append(sub)
                    break

                if sub in CURRENT_WHITE:
                    break

            if turn == 1:
                if sub in CURRENT_WHITE:
                    move_list.append(sub)
                    break

                if sub in CURRENT_BLACK:
                    break
    
    for i in rook:
        for sub in i:

            if sub in FREE:
                move_list.append(sub)
                continue

            if turn == 0:
                if sub in CURRENT_BLACK:
                    move_list.append(sub)
                    break

                if sub in CURRENT_WHITE:
                    break

            if turn == 1:
                if sub in CURRENT_WHITE:
                    move_list.append(sub)
                    break

                if sub in CURRENT_BLACK:
                    break
    
    return move_list


def king_list(board):
    move_list = []
    POSSIBLE_MOVES = king_valid_move(board)

    for i in POSSIBLE_MOVES:
        kx = i[0]
        ky = i[1]
        if turn == 0:

            if i not in CURRENT_WHITE:
                if not in_check(board, kx, ky):
                    move_list.append(i)

        else:
            if i not in CURRENT_BLACK:
                if not in_check(board, kx, ky):
                    move_list.append(i)

    return move_list



############################################ MOVE PIECES



def pawn_movement(pawn, board):
    board[pawn.y][pawn.x] = 0

    # If the pawn moves straight
    if movement_x_input == pawn.x:
        if pawn.team == 0:
            white_move = movement_y_input - pawn.y
            board[pawn.y+white_move][pawn.x] = pawn.piece_id
            pawn.y += white_move


        if pawn.team == 1:
            black_move = movement_y_input - pawn.y
            board[pawn.y+black_move][pawn.x] = pawn.piece_id
            pawn.y += black_move


    return board

def pawn_attack(pawn, board, x, y):

    board[pawn.y][pawn.x] = 0

    # If the pawn moves right
    if x - pawn.x == 1:
        # If the pawn belongs to WHITE and also moves 1 down(diagonally)
        if pawn.team == 0 and y - pawn.y == 1:
            board[pawn.y+1][pawn.x+1] = pawn.piece_id
            pawn.x += 1
            pawn.y += 1


        # If the pawn belongs to BLACK and also moves 1 up(diagonally)
        if pawn.team == 1 and y - pawn.y == -1:
            board[pawn.y-1][pawn.x+1] = pawn.piece_id
            pawn.x += 1
            pawn.y -= 1


    # If the pawn moves left
    if x - pawn.x == -1:
        # If the pawn belongs to WHITE and also moves 1 down(diagonally)
        if pawn.team == 0 and y - pawn.y == 1:
            board[pawn.y+1][pawn.x-1] = pawn.piece_id
            pawn.x -= 1
            pawn.y += 1


        # If the pawn belongs to BLACK and also moves 1 up(diagonally)
        if pawn.team == 1 and y - pawn.y == -1:
            board[pawn.y-1][pawn.x-1] = pawn.piece_id
            pawn.x -= 1
            pawn.y -= 1

    return board


def piece_movement(piece, board):
    board[piece.y][piece.x] = 0
    board[movement_y_input][movement_x_input] = piece.piece_id
    piece.x = movement_x_input
    piece.y = movement_y_input
    
    return board


##################################### EDGE RESTRICTIONS

def at_top_edge(piece):
    if piece.y == 0:
        return True

    return False

def at_right_edge(piece):
    if piece.x == 7:
        return True
    
    return False

def at_bottom_edge(piece):
    if piece.y == 7:
        return True

    return False

def at_left_edge(piece):
    if piece.x == 0:
        return True
    
    return False

####################################### KING FUNCTIONS


def king_vs_king(board):
    enemy_king_defense = []

    if turn == 0:
        for i in range(ROWS):
            for j in range(COLUMNS):
                if board[i][j] == 12:
                    x = j
                    y = i

    else:
        for i in range(ROWS):
            for j in range(COLUMNS):
                if board[i][j] == 6:
                    x = j
                    y = i


    for i in range(-1, 2):
        for t in range(-1, 2):
            move = (x+t, y+i)
            enemy_king_defense.append(move)

    return enemy_king_defense



# Get the coords of your own king
def king_coords(board):
    if turn == 0:
        for i in range(ROWS):
            for j in range(COLUMNS):
                if board[i][j] == 6:
                    x = j
                    y = i

    else:
        for i in range(ROWS):
            for j in range(COLUMNS):
                if board[i][j] == 12:
                    x = j
                    y = i

    return x, y


# Combine king_coords and in_check to check if the king is in check
def king_in_check(board):
    x, y = king_coords(board)
    value = in_check(board, x, y)
    if value:
        return value

    return False


def castle_counter():
    if turn == 0:
        if (0, 0) in FREE:
            castlew[0] += 1
        if (7, 0) in FREE:
            castlew[1] += 1
        if (3,0) in FREE:
            castlew[2] += 1
        return castlew

    else:
        if (0, 7) in FREE:
            castleb[0] += 1
        if (7, 7) in FREE:
            castleb[1] += 1
        if (3, 7) in FREE:
            castleb[2] += 1
        return castleb

def can_castle():
    castle = castle_counter()
    if castle[2] != 0:
        return False
    if castle[0] == 0 and castle[1] == 0:
        return 'Both'
    elif castle[0] == 0:
        return 'Left'
    elif castle[1] == 0:
        return 'Right'

def castle_can_move(piece, x, y):
    moves_list = list_of_moves(piece)
    result = can_castle()
    input = (x, y)

    WL = (1, 0)
    WR = (6, 0)
    BL = (1, 7)
    BR = (6, 7)

    if input == WL or input == BL:# and (result == 'Left' or result == 'Both'):
        for i in range(1, 3):
            if (piece.x-i, piece.y) not in FREE:
                return False


    elif input == WR or input == BR:# and (result == 'Right' or result == 'Both'):
        for i in range(1, 4):
            if (piece.x+i, piece.y) not in FREE:
                return False

    return True

def castle(piece, x, y, board):

    board[piece.y][piece.x] = 0
    board[y][x] = piece.piece_id
    piece.x = movement_x_input
    piece.y = movement_y_input
    
    
    if y == 0:
        if x == 1:
            board[0][0] = 0
            board[0][2] = 2

        if x == 6:
            board[0][7] = 0
            board[0][5] = 2

    else:
        if x == 1:
            board[7][0] = 0
            board[7][2] = 8

        if x == 6:
            board[7][7] = 0
            board[7][5] = 8

    return board


################################## USED BY OTHER FUNCTIONS FUNCTIONS

# Get a list of enemy attackers' coordinates
def enemy_coords(board):
    enemy_diagonal = []
    enemy_straight = []
    enemy_knight = []

    if turn == 0:
        for i in range(ROWS):
            for j in range(COLUMNS):
                if board[i][j] == 10 or board[i][j] == 11:
                    enemy_diagonal.append((j,i))
                if board[i][j] == 8 or board[i][j] == 11:
                    enemy_straight.append((j,i))
                if board[i][j] == 9:
                    enemy_knight.append((j,i))

    else:
        for i in range(ROWS):
            for j in range(COLUMNS):
                if board[i][j] == 4 or board[i][j] == 5:
                    enemy_diagonal.append((j,i))
                if board[i][j] == 2 or board[i][j] == 5:
                    enemy_straight.append((j,i))
                if board[i][j] == 3:
                    enemy_knight.append((j,i))

    return enemy_diagonal, enemy_straight, enemy_knight



# On a player's turn, take the board, x, y, and enemy coords to determine if the (x, y) has any threats by looping through diagonals/straights
def in_check(board, x, y):
    enemy_diagonal, enemy_straight, enemy_knight = enemy_coords(board)
    list = []
    if turn == 0:
    # Lower right diagonal
        for i in range(1, ROWS):
            move = (x + i, y + i)  
            list.append(move)

            if move in CURRENT_WHITE and board[y+i][x+i] != 6:
                list.clear()
                break

            if move in CURRENT_BLACK:
                if i == 1 and board[y + i][x + i] == 7:
                    return 'Down_right_diagonal', (x+i, y+i), list
                if move in enemy_diagonal:
                    return 'Down_right_diagonal', (x+i, y+i), list
                else:
                    break

            if x + i == 7 or y + i == 7:
                list.clear()
                break

        # Upper right diagonal
        for i in range(1, ROWS):
            move = (x + i, y - i)
            list.append(move)
            if move in CURRENT_WHITE and board[y-i][x+i] != 6:
                list.clear()
                break

            if move in CURRENT_BLACK:
                if move in enemy_diagonal:
                    return 'Up_right_diagonal', (x+i, y-i), list
                else:
                    break

            if x + i == 7 or y - i == 0:
                list.clear()
                break

        # Lower left diagonal
        for i in range(1, ROWS):
            move = (x - i, y + i)
            list.append(move)
            if move in CURRENT_WHITE and board[y+i][x-i] != 6:
                list.clear()
                break

            if move in CURRENT_BLACK:
                if i == 1 and board[y + i][x - i] == 7:
                    return 'Down_left diagonal', (x-i, y+i), list
                if move in enemy_diagonal:
                    return 'Down_left_diagonal', (x-i, y+i), list
                else:
                    break
                
            if x - i == 0 or y + i == 7:
                list.clear()
                break

        # Upper left diagonal
        for i in range(1, ROWS):
            move = (x-i, y-i)
            list.append(move)
            if move in CURRENT_WHITE and board[y-i][x-i] != 6:
                list.clear()
                break

            if move in CURRENT_BLACK:
                if move in enemy_diagonal:
                    return 'Up_left_diagonal', (x-i, y-i), list
                else:
                    break
                
            if x - i == 0 or y - i == 0:
                list.clear()
                break

        # Straights
        north = y + 1
        south = ROWS - y
        west = x + 1
        east = COLUMNS - x

        for i in range(north):
            move = (x, y-i)
            list.append(move)
            if move in CURRENT_WHITE and board[y-i][x] != 6:
                list.clear()
                break

            if move in CURRENT_BLACK:
                if move in enemy_straight:
                    return 'Up_straight', (x, y-i), list

                else:
                    break

            if y-i == 0:
                list.clear()
                break

        for i in range(south):
            move = (x, y+i)
            list.append(move)
            if move in CURRENT_WHITE and board[y+i][x] != 6:
                list.clear()
                break

            if move in CURRENT_BLACK:
                if move in enemy_straight:
                    return 'Down_straight', (x, y+i), list

                else:
                    break

            if y+i == 7:
                list.clear()
                break

        for i in range(west):
            move = (x-i, y)
            list.append(move)
            if move in CURRENT_WHITE and board[y][x-i] != 6:
                break

            if move in CURRENT_BLACK:
                if move in enemy_straight:
                    return 'Left_straight', (x-i, y), list

                else:
                    break
            
            if x-i == 0:
                list.clear()
                break

        for i in range(east):
            move = (x+i, y)
            list.append(move)
            if move in CURRENT_WHITE and board[y][x+i] != 6:
                break

            if move in CURRENT_BLACK:
                if move in enemy_straight:
                    return 'Right_straight', (x+i, y), list

                else:
                    break
            
            if x+i == 7:
                list.clear()
                break


    else:
        for i in range(1, ROWS):
            move = (x + i, y + i)  
            list.append(move)

            if move in CURRENT_WHITE and board[y+i][x+i] != 12:
                list.clear()
                break

            if move in CURRENT_BLACK:
                if i == 1 and board[y + i][x + i] == 7:
                    return 'Down_right_diagonal', (x+i, y+i), list
                if move in enemy_diagonal:
                    return 'Down_right_diagonal', (x+i, y+i), list
                else:
                    break

            if x + i == 7 or y + i == 7:
                list.clear()
                break
                
        # Upper right diagonal
        for i in range(1, ROWS):
            move = (x + i, y - i)
            list.append(move)
            if move in CURRENT_WHITE and board[y-i][x+i] != 12:
                list.clear()
                break

            if move in CURRENT_BLACK:
                if move in enemy_diagonal:
                    return 'Up_right_diagonal', (x+i, y-i), list
                else:
                    break

            if x + i == 7 or y - i == 0:
                list.clear()
                break

        # Lower left diagonal
        for i in range(1, ROWS):
            move = (x - i, y + i)
            list.append(move)
            if move in CURRENT_WHITE and board[y+i][x-i] != 12:
                list.clear()
                break

            if move in CURRENT_BLACK:
                if i == 1 and board[y + i][x - i] == 7:
                    return 'Down_left diagonal', (x-i, y+i), list
                if move in enemy_diagonal:
                    return 'Down_left_diagonal', (x-i, y+i), list
                else:
                    break
                
            if x - i == 0 or y + i == 7:
                list.clear()
                break

        # Upper left diagonal
        for i in range(1, ROWS):
            move = (x-i, y-i)
            list.append(move)
            if move in CURRENT_WHITE and board[y-i][x-i] != 12:
                list.clear()
                break

            if move in CURRENT_BLACK:
                if move in enemy_diagonal:
                    return 'Up_left_diagonal', (x-i, y-i), list
                else:
                    break
                
            if x - i == 0 or y - i == 0:
                list.clear()
                break

        # Straights
        north = y + 1
        south = ROWS - y
        west = x + 1
        east = COLUMNS - x

        for i in range(north):
            move = (x, y-i)
            list.append(move)
            if move in CURRENT_WHITE and board[y-i][x] != 12:
                list.clear()
                break

            if move in CURRENT_BLACK:
                if move in enemy_straight:
                    return 'Up_straight', (x, y-i), list

                else:
                    break

            if y-i == 0:
                list.clear()
                break

        for i in range(south):
            move = (x, y+i)
            list.append(move)
            if move in CURRENT_WHITE and board[y+i][x] != 12:
                list.clear()
                break

            if move in CURRENT_BLACK:
                if move in enemy_straight:
                    return 'Down_straight', (x, y+i), list

                else:
                    break

            if y+i == 7:
                list.clear()
                break

        for i in range(west):
            move = (x-i, y)
            list.append(move)
            if move in CURRENT_WHITE and board[y][x-i] != 12:
                break

            if move in CURRENT_BLACK:
                if move in enemy_straight:
                    return 'Left_straight', (x-i, y), list

                else:
                    break
            
            if x-i == 0:
                list.clear()
                break

        for i in range(east):
            move = (x+i, y)
            list.append(move)
            if move in CURRENT_WHITE and board[y][x+i] != 12:
                break

            if move in CURRENT_BLACK:
                if move in enemy_straight:
                    return 'Right_straight', (x+i, y), list

                else:
                    break
            
            if x+i == 7:
                list.clear()
                break

    list = [[1, 2], [-1, 2], [-1, -2], [1, -2], [2, 1], [-2, 1], [-2, -1], [2, -1]]
    for i in list:
        x_movement = x + int(i[0])
        y_movement = y + int(i[1])
        move = (x_movement, y_movement)
        
        if move in enemy_knight:
            return 'Knight', (move), list
    
    return False


def protect(board):
    x, y = king_coords(board)
    check, enemy, list = in_check(board, x, y)
    ex = enemy[0]
    ey = enemy[1]
    saviors = []
    # Knight, Right_straight, Left_straight Down_straight Up_straight Up_left_diagonal Down_left_diagonal Up_right_diagonal Down_right_diagonal
    if check:
        if turn == 0:
            for i in CURRENT_WHITE:
                px = i[0]
                py = i[1]

                piece = Piece(px, py, int(board[py][px]), 0)

                if list:
                    for t in list:
                        dx = t[0]
                        dy = t[1]
                        dmove = valid_move(piece, dx, dy)

                        if not dmove:
                            continue

                        if piece.name == 'Pawn':
                            if pawn_can_move(piece, dx, dy):
                                saviors.append((i))

                        if piece_can_move(piece, dx, dy):
                            saviors.append((i))

                moves = valid_move(piece, ex, ey)
                if not moves:
                    continue
                
                if piece.name == 'Pawn':
                    if moves[0] == 'attack':
                        saviors.append((i))

                if piece_can_move(piece, ex, ey):
                    saviors.append((i))


                
        else:
            for i in CURRENT_BLACK:
                px = i[0]
                py = i[1]

                piece = Piece(px, py, int(board[py][px]), 1)

                if list:
                    for t in list:
                        dx = t[0]
                        dy = t[1]
                        dmove = valid_move(piece, dx, dy)

                        if not dmove:
                            continue

                        if piece.name == 'Pawn':
                            if pawn_can_move(piece, dx, dy):
                                saviors.append((i))
                                
                        if piece_can_move(piece, dx, dy):
                            saviors.append((i))


                moves = valid_move(piece, ex, ey)
                if not moves:
                    continue
                
                if piece.name == 'Pawn':
                    if moves[0] == 'attack':
                        saviors.append((i))

                if piece_can_move(piece, ex, ey):
                    saviors.append((i))


    return saviors


def checkmate(board):
    list = protect(board)
    king_moves = king_list(board)
    valid = []

    for i in king_moves:
        if king_can_move(board, i[0], i[1]):
            valid.append((i))

    if not list and not valid:
        return True

    return False
    

def checked_loop(BOARD, piece_x_input, piece_y_input):
    list = protect(BOARD)
    king_moves = king_list(BOARD)
    x, y = king_coords(BOARD)
    valid = []
    input = (piece_x_input, piece_y_input)

    for i in king_moves:
        if king_can_move(BOARD, i[0], i[1]):
            valid.append((i))

    if list and king_moves:
        if input not in list and input != (x, y):
            return True

    elif list and not king_moves:
        if input not in list:
            return True
    
    elif king_moves and not list:
        if input != (x, y):
            return True

    return False



################################################

def input_loop():
    if turn == 0:
        while True:
            piece_x_input = int(input("Player 1 enter the x coordinate of the piece you move: 0-7 : "))
            piece_y_input = int(input("Player 1 enter the y coordinate of the piece you move: 0-7 : "))
            type = determine_piece_id(piece_x_input, piece_y_input, BOARD)

            if (piece_x_input, piece_y_input) not in CURRENT_WHITE:
                print("Input one of your pieces' coordinates")
                continue
            else:
                selected_piece = Piece(piece_x_input, piece_y_input, type, 0)
                break
        

    else:
        while True:
            piece_x_input = int(input("Player 2 enter the x coordinate of the piece you move: 0-7 : "))
            piece_y_input = int(input("Player 2 enter the y coordinate of the piece you move: 0-7 : "))
            type = determine_piece_id(piece_x_input, piece_y_input, BOARD)

            if (piece_x_input, piece_y_input) not in CURRENT_BLACK:
                print("Input one of your pieces' coordinates")
                continue
            
            else:
                selected_piece = Piece(piece_x_input, piece_y_input, type, 1)
                break

    return type, piece_x_input, piece_y_input, selected_piece

#########

# If the movement inputs aren't can't be taken by the piece, return false and restart loop
def piece_check(selected_piece):

    movement_x_input = int(input("Enter the x coordinate in which you want to move the piece to: 0-7 : "))
    movement_y_input = int(input("Enter the y coordinate in which you want to move the piece to: 0-7 : "))

    bruh = valid_move(selected_piece, movement_x_input, movement_y_input)

    # If the move is not in the list of valid moves for the selected piece
    if not bruh:
        print("That is not a valid move for this piece.")
        return 0, 0, 'No'

    if selected_piece.name != 'King' and cannot_move_check(selected_piece, BOARD, movement_x_input, movement_y_input):
        print("You must defend your king from check.")
        return 0, 0, 'No'

    # If the piece is a pawn and can not move forward while attempting to
    if selected_piece.name == 'Pawn' and bruh[0] != 'attack':
        if not pawn_can_move(selected_piece, movement_x_input, movement_y_input):
            print("This pawn can not move here.")
            return 0, 0, 'No'
        

    if selected_piece.name == 'Rook':
        if not rook_can_move(selected_piece, movement_x_input, movement_y_input):
            print("This rook can not move here.")
            return 0, 0, 'No'

    if selected_piece.name == 'Knight':
        if not knight_can_move(selected_piece, movement_x_input, movement_y_input):
            print("This knight can not move here.")
            return 0, 0, 'No'

    if selected_piece.name == 'Bishop':
        if not bishop_can_move(selected_piece, movement_x_input, movement_y_input):
            print("This bishop can not move here.")
            return 0, 0, 'No'


    if selected_piece.name == 'Queen':
        x = abs(movement_x_input - selected_piece.x)
        y = abs(movement_y_input - selected_piece.y)
        if x == y:
            if not bishop_can_move(selected_piece, movement_x_input, movement_y_input):
                print("This queen can not move here")
                return 0, 0, 'No'
            
        else:
            if not rook_can_move(selected_piece, movement_x_input, movement_y_input):
                print("This queen can not move here.")
                return 0, 0, 'No'

    if selected_piece.name == 'King':
        if bruh == 'castle':
            if not can_castle():
                print("This king cannot castle")
                return 0, 0, 'No'
            if not castle_can_move(selected_piece, movement_x_input, movement_y_input):
                print("Something is blocking the castle.")
                return 0, 0, 'No'
        if not king_can_move(BOARD, movement_x_input, movement_y_input):
            print("This king can not move here.")
            return 0, 0, 'No'

    return movement_x_input, movement_y_input, bruh



######################################################


BOARD = create_board()
game_over = False
empty = free_space(BOARD)
white_occupied(BOARD, WHITE)
black_occupied(BOARD, BLACK)
turn_total = 0

while not game_over:
    if turn_total == 0:
        print(BOARD)

    if turn == 0:
        if king_in_check(BOARD):
            if checkmate(BOARD):
                print('Game over, Player 2 wins')
                game_over = True
                break

            else:
                print('You are in check')
                print(protect(BOARD))
                print(king_list(BOARD))
                type, piece_x_input, piece_y_input, selected_piece = input_loop()
                while True:
                    if (checked_loop(BOARD, piece_x_input, piece_y_input)):
                        print('You must deal with check')
                        type, piece_x_input, piece_y_input, selected_piece = input_loop()
                        continue
                
                    else:
                        break
            
        else:
            type, piece_x_input, piece_y_input, selected_piece = input_loop()

        movement_x_input, movement_y_input, bruh = piece_check(selected_piece)

        while True:
            if (bruh == 'No'):
                type, piece_x_input, piece_y_input, selected_piece = input_loop()
                print(list_of_moves(selected_piece))
                movement_x_input, movement_y_input, bruh = piece_check(selected_piece)
                continue

            else:
                break

        if selected_piece.name == 'Pawn':
            if bruh == 'attack':
                nboard = pawn_attack(selected_piece, BOARD, movement_x_input, movement_y_input)

            else:
                nboard = pawn_movement(selected_piece, BOARD)

        elif selected_piece.name == 'King':
            if bruh == 'castle':
                nboard = castle(selected_piece, movement_x_input, movement_y_input, BOARD)
            else:
                nboard = piece_movement(selected_piece, BOARD)
        else:
            nboard = piece_movement(selected_piece, BOARD)


    else:
        if king_in_check(BOARD):
            if checkmate(BOARD):
                print('Game over, Player 1 wins')
                game_over = True
                break

            else:
                print('You are in check')
                print(protect(BOARD))
                print(king_list(BOARD))
                type, piece_x_input, piece_y_input, selected_piece = input_loop()
                while True:
                    if (checked_loop(BOARD, piece_x_input, piece_y_input)):
                        print('You must deal with check')
                        type, piece_x_input, piece_y_input, selected_piece = input_loop()
                        continue
                
                    else:
                        break
            
        else:
            type, piece_x_input, piece_y_input, selected_piece = input_loop()

        movement_x_input, movement_y_input, bruh = piece_check(selected_piece)

        while True:
            if (bruh == 'No'):
                type, piece_x_input, piece_y_input, selected_piece = input_loop()
                print(list_of_moves(selected_piece))
                movement_x_input, movement_y_input, bruh = piece_check(selected_piece)
                continue

            else:
                break

        if selected_piece.name == 'Pawn':
            if bruh == 'attack':
                nboard = pawn_attack(selected_piece, BOARD, movement_x_input, movement_y_input)

            else:
                nboard = pawn_movement(selected_piece, BOARD)

        elif selected_piece.name == 'King':
            if bruh == 'castle':
                nboard = castle(selected_piece, movement_x_input, movement_y_input, BOARD)
            else:
                nboard = piece_movement(selected_piece, BOARD)
        else:
            nboard = piece_movement(selected_piece, BOARD)


    pawn_promotion(nboard)
    CURRENT_BLACK.clear()
    black_occupied(nboard, BLACK)
    CURRENT_WHITE.clear()
    white_occupied(nboard, WHITE)
    
    FREE.clear()
    free_space(nboard)
    castle_counter()
    print(nboard)

    turn += 1
    turn = turn % 2
    turn_total += 1
