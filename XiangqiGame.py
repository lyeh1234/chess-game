# Author: Lawrence Yeh
# Date: 3/12/20
# Description: This program retrieves parameters from make_move fed by user and plays Xiangqi
#              according to all the board/piece rules of the game. It will also output the
#              game status ('UNFINISHED', 'RED_WON', 'BLACK_WON').


# only used for deepcopy for the print_pretty_board function,
# using module for testing/visual purposes
import copy   # commented out for final submission


# class generates game board, determines of moves made are legal, determines check and checkmate,
# outputs game state, returns T/F for player in check, returns T/F for moves made
class XiangqiGame:

    # initializes checks, turn counter, game state, empty board, every individual unique piece
    def __init__(self):
        self._turn_counter = 0  # will need a turn counter for 'red' vs 'black' turns
        self._game_state = 'UNFINISHED'  # initiate state at beginning of game
        self._red_in_check = False
        self._black_in_check = False
        self._board = [[0, 0, 0, 0, 0, 0, 0, 0, 0] for i in range(10)]
        self._pieces = []   # set empty list to place all board pieces in list for iterations later

        # set all unique pieces as objects
        self._rook_r1 = Rook("rook", "a1", "red", "rook r1")
        self._rook_r2 = Rook("rook", "i1", "red", "rook r2")
        self._rook_b1 = Rook("rook", "a10", "black", "rook b1")
        self._rook_b2 = Rook("rook", "i10", "black", "rook b2")
        self._knight_r1 = Knight("knight", "b1", "red", "knight r1")
        self._knight_r2 = Knight("knight", "h1", "red", "knight r2")
        self._knight_b1 = Knight("knight", "b10", "black", "knight b1")
        self._knight_b2 = Knight("knight", "h10", "black", "knight b2")
        self._elephant_r1 = Elephant("elephant", "c1", "red", "elephant r1")
        self._elephant_r2 = Elephant("elephant", "g1", "red", "elephant r2")
        self._elephant_b1 = Elephant("elephant", "c10", "black", "elephant b1")
        self._elephant_b2 = Elephant("elephant", "g10", "black", "elephant b2")
        self._cannon_r1 = Cannon("cannon", "b3", "red", "cannon r1")
        self._cannon_r2 = Cannon("cannon", "h3", "red", "cannon r2")
        self._cannon_b1 = Cannon("cannon", "b8", "black", "cannon b1")
        self._cannon_b2 = Cannon("cannon", "h8", "black", "cannon b2")
        self._guard_r1 = Guard("guard", "d1", "red", "guard r1")
        self._guard_r2 = Guard("guard", "f1", "red", "guard r2")
        self._guard_b1 = Guard("guard", "d10", "black", "guard b1")
        self._guard_b2 = Guard("guard", "f10", "black", "guard b2")
        self._general_r = General("general", "e1", "red", "general r")
        self._general_b = General("general", "e10", "black", "general b")
        self._pawn_r1 = Pawn_Red("pawn", "a4", "red", "pawn r1")
        self._pawn_r2 = Pawn_Red("pawn", "c4", "red", "pawn r2")
        self._pawn_r3 = Pawn_Red("pawn", "e4", "red", "pawn r3")
        self._pawn_r4 = Pawn_Red("pawn", "g4", "red", "pawn r4")
        self._pawn_r5 = Pawn_Red("pawn", "i4", "red", "pawn r5")
        self._pawn_b1 = Pawn_Black("pawn", "a7", "black", "pawn b1")
        self._pawn_b2 = Pawn_Black("pawn", "c7", "black", "pawn b2")
        self._pawn_b3 = Pawn_Black("pawn", "e7", "black", "pawn b3")
        self._pawn_b4 = Pawn_Black("pawn", "g7", "black", "pawn b4")
        self._pawn_b5 = Pawn_Black("pawn", "i7", "black", "pawn b5")

    # print board
    def print_board(self):
        for row in self._board:
            print(row)

    # print a board with the piece names instead of their object address locations
    # imported the copy module to prevent changing actual board
    def print_pretty_board(self):
        pretty_board = copy.deepcopy(self._board)   # deepcopy() to avoid changing actual board
        for i in range(10):
            for k in range(9):
                if pretty_board[i][k] != 0:
                    piece = pretty_board[i][k]
                    pretty_board[i][k] = piece.get_name()

        for row in pretty_board:
            print(row)

    # return either 'UNFINISHED' , 'RED_WON' , 'BLACK_WON'
    def get_game_state(self):

        return self._game_state

    # set game state to new game state
    def set_game_state(self, new_game_state):
        
        self._game_state = new_game_state

    # get coordinates from user and convert to row and column by parsing string
    def get_coordinates(self, location):
        letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
        col = letters.index(location[0])
        row = int(location[1:])-1

        return ([row, col])   # returns list of board coordinates

    # create an list of the objects/unique pieces
    def start_game(self):
        self._pieces = [self._rook_r1, self._rook_r2, self._rook_b1, self._rook_b2,
                       self._knight_r1, self._knight_r2, self._knight_b1, self._knight_b2,
                       self._elephant_r1, self._elephant_r2, self._elephant_b1, self._elephant_b2,
                       self._cannon_r1, self._cannon_r2, self._cannon_b1, self._cannon_b2,
                       self._guard_r1, self._guard_r2, self._guard_b1, self._guard_b2,
                       self._general_r, self._general_b,
                       self._pawn_r1, self._pawn_r2, self._pawn_r3, self._pawn_r4, self._pawn_r5,
                       self._pawn_b1, self._pawn_b2, self._pawn_b3, self._pawn_b4, self._pawn_b5]

        for p in self._pieces:
            coordinates = self.get_coordinates(p.get_location())   # i.e. coordinates = the [a][1] conversion of 'a1'
            self._board[coordinates[0]][coordinates[1]] = p   # i.e. board[a][1] set to current iterated piece object

    # returns 'red' or 'black' for which player
    def get_current_player(self):

        if self._turn_counter % 2 == 0:

            return "red"

        else:

            return "black"

    # returns T if general is in check, F otherwise - all cases of pieces that can check general included
    def general_check(self, enemy_player):

        # get the coordinates of the enemy general
        for row in range(0,10):

            for col in range(0,9):

                # check if the piece is in that space
                if self._board[row][col] != 0:

                    # check if the piece is the enemy general
                    if self._board[row][col].get_piece_type() == "general" and \
                            self._board[row][col].get_player_color() == enemy_player:

                        g_row = row   # general row
                        g_col = col   # general col

                        # check if an attacker is adjacent to the general
                        if enemy_player == "red":   # general/enemy is red, check for black piece attackers

                            # if the general is not on the north edge, check for an attacker above
                            if g_row - 1 != -1:

                                if self._board[g_row-1][g_col] == self._rook_b1 or \
                                        self._board[g_row-1][g_col] == self._rook_b2:

                                    return True
                            
                            # down
                            if self._board[g_row+1][g_col] == self._pawn_b1 or \
                                    self._board[g_row+1][g_col] == self._pawn_b2 or \
                                    self._board[g_row+1][g_col] == self._pawn_b3 or \
                                    self._board[g_row+1][g_col] == self._pawn_b4 or \
                                    self._board[g_row+1][g_col] == self._pawn_b5 or \
                                    self._board[g_row+1][g_col] == self._rook_b1 or \
                                    self._board[g_row+1][g_col] == self._rook_b2:
                        
                                return True

                            # left
                            if self._board[g_row][g_col-1] == self._pawn_b1 or \
                                    self._board[g_row][g_col-1] == self._pawn_b2 or \
                                    self._board[g_row][g_col-1] == self._pawn_b3 or \
                                    self._board[g_row][g_col-1] == self._pawn_b4 or \
                                    self._board[g_row][g_col-1] == self._pawn_b5 or \
                                    self._board[g_row][g_col-1] == self._rook_b1 or \
                                    self._board[g_row][g_col-1] == self._rook_b2:
                        
                                return True
                            
                            # right
                            if self._board[g_row][g_col+1] == self._pawn_b1 or \
                                    self._board[g_row][g_col+1] == self._pawn_b2 or \
                                    self._board[g_row][g_col+1] == self._pawn_b3 or \
                                    self._board[g_row][g_col+1] == self._pawn_b4 or \
                                    self._board[g_row][g_col+1] == self._pawn_b5 or \
                                    self._board[g_row][g_col+1] == self._rook_b1 or \
                                    self._board[g_row][g_col+1] == self._rook_b2:

                                return True
                        
                        # enemy player/general is black, check for red attackers
                        else:

                            # if the general is not on the south edge, check for an attacker below
                            if g_row + 1 != 10:

                                if self._board[g_row+1][g_col] == self._rook_r1 or \
                                        self._board[g_row+1][g_col] == self._rook_r2:

                                    return True
                            
                            # up
                            if self._board[g_row-1][g_col] == self._pawn_r1 or \
                                    self._board[g_row-1][g_col] == self._pawn_r2 or \
                                    self._board[g_row-1][g_col] == self._pawn_r3 or \
                                    self._board[g_row-1][g_col] == self._pawn_r4 or \
                                    self._board[g_row-1][g_col] == self._pawn_r5 or \
                                    self._board[g_row-1][g_col] == self._rook_r1 or \
                                    self._board[g_row-1][g_col] == self._rook_r2:
                        
                                return True

                            # left
                            if self._board[g_row][g_col-1] == self._pawn_r1 or \
                                    self._board[g_row][g_col-1] == self._pawn_r2 or \
                                    self._board[g_row][g_col-1] == self._pawn_r3 or \
                                    self._board[g_row][g_col-1] == self._pawn_r4 or \
                                    self._board[g_row][g_col-1] == self._pawn_r5 or \
                                    self._board[g_row][g_col-1] == self._rook_r1 or \
                                    self._board[g_row][g_col-1] == self._rook_r2:
                        
                                return True
                            
                            # right
                            if self._board[g_row][g_col+1] == self._pawn_r1 or \
                                    self._board[g_row][g_col+1] == self._pawn_r2 or \
                                    self._board[g_row][g_col+1] == self._pawn_r3 or \
                                    self._board[g_row][g_col+1] == self._pawn_r4 or \
                                    self._board[g_row][g_col+1] == self._pawn_r5 or \
                                    self._board[g_row][g_col+1] == self._rook_r1 or \
                                    self._board[g_row][g_col+1] == self._rook_r2:
                        
                                return True

                        # check left of general - rook and canon check
                        g_col_left = g_col - 1
                        left_piece_counter = 0

                        while g_col_left > -1:   # if space left of general is empty

                            if self._board[g_row][g_col_left] != 0:
                                left_piece_counter += 1

                                if enemy_player == "red":   # checking red general, so look for black pieces

                                    # if this is the first piece found, check for the rook
                                    if left_piece_counter == 1:

                                        if self._board[g_row][g_col_left] == self._rook_b1 or \
                                                self._board[g_row][g_col_left] == self._rook_b2:

                                            return True   # red is in check
                                    
                                    # if this is the second piece found, check for the cannon
                                    if left_piece_counter == 2:

                                        if self._board[g_row][g_col_left] == self._cannon_b1 or \
                                                self._board[g_row][g_col_left] == self._cannon_b2:

                                            return True   # red is in check

                                else:   # enemy player is black, check for red attacker

                                    if left_piece_counter == 1:

                                        if self._board[g_row][g_col_left] == self._rook_r1 or \
                                                self._board[g_row][g_col_left] == self._rook_r2:

                                            return True   # black is in check
                                    
                                    # if this is the second piece found, check for the cannon
                                    if left_piece_counter == 2:

                                        if self._board[g_row][g_col_left] == self._cannon_r1 or \
                                                self._board[g_row][g_col_left] == self._cannon_r2:

                                            return True   # red is in check
                                
                                if left_piece_counter > 2:

                                    break   # if 3 pieces, break out of the loop
                                                            
                            g_col_left -= 1   # check next space left
                        
                        # check right of general - rook and canon check
                        g_col_right = g_col + 1
                        right_piece_counter = 0

                        while g_col_right < 9:   # if space left of general is empty

                            if self._board[g_row][g_col_right] != 0:

                                right_piece_counter += 1

                                if enemy_player == "red":   # checking red general, so look for black pieces

                                    # if this is the first piece found, check for the rook
                                    if right_piece_counter == 1:

                                        if self._board[g_row][g_col_right] == self._rook_b1 or \
                                                self._board[g_row][g_col_right] == self._rook_b2:

                                            return True   # red is in check
                                    
                                    # if this is the second piece found, check for the cannon
                                    if right_piece_counter == 2:

                                        if self._board[g_row][g_col_right] == self._cannon_b1 or \
                                                self._board[g_row][g_col_right] == self._cannon_b2:

                                            return True   # red is in check

                                else:   # enemy player is black, so check for red attacker

                                    if right_piece_counter == 1:

                                        if self._board[g_row][g_col_right] == self._rook_r1 or \
                                                self._board[g_row][g_col_right] == self._rook_r2:

                                            return True   # black is in check
                                    
                                    # if this is the second piece found, check for the cannon
                                    if right_piece_counter == 2:

                                        if self._board[g_row][g_col_right] == self._cannon_r1 or \
                                                self._board[g_row][g_col_right] == self._cannon_r2:

                                            return True   # red is in check
                                
                                if right_piece_counter > 2:

                                    break   # found 3 pieces, break out of the loop

                            g_col_right += 1   # check next space right

                        # check above general - rook check
                        if g_row > 1:   # no need to check first two rows, adjacent check covered it
                            g_row_above = g_row - 1
                            above_piece_counter = 0

                            while g_row_above > -1:   # if space left of general is empty

                                if self._board[g_row_above][g_col] != 0:

                                    above_piece_counter += 1

                                    if enemy_player == "red":   # checking red general, look for black pieces

                                        # if this is the first piece found, check for the rook
                                        if above_piece_counter == 1:

                                            if self._board[g_row_above][g_col] == self._rook_b1 or \
                                                    self._board[g_row_above][g_col] == self._rook_b2:

                                                return True   # red is in check
                                        
                                        # if this is the second piece found, check for the cannon
                                        if above_piece_counter == 2:

                                            if self._board[g_row_above][g_col] == self._cannon_b1 or \
                                                    self._board[g_row_above][g_col] == self._cannon_b2:

                                                return True   # red is in check

                                    else:   # enemy player is black, so check for red attacker

                                        if above_piece_counter == 1:

                                            if self._board[g_row_above][g_col] == self._rook_r1 or \
                                                    self._board[g_row_above][g_col] == self._rook_r2:

                                                return True   # black is in check
                                        
                                        # if this is the second piece found, check for the cannon
                                        if above_piece_counter == 2:

                                            if self._board[g_row_above][g_col] == self._cannon_r1 or \
                                                    self._board[g_row_above][g_col] == self._cannon_r2:

                                                return True   # red is in check
                                    
                                    if above_piece_counter > 2:

                                        break   # found 3 pieces, break out of the loop
                                
                                g_row_above -= 1   # check next space above
                        
                        # check below general - rook check
                        if g_row < 8:   # no need to check bottom two rows, adjacent check covered it
                            g_row_below = g_row + 1
                            below_piece_counter = 0

                            while g_row_below < 10:   # if space left of general is empty

                                if self._board[g_row_below][g_col] != 0:

                                    below_piece_counter += 1

                                    if enemy_player == "red":   # checking red general, so look for black pieces

                                        # if this is the first piece found, check for the rook
                                        if below_piece_counter == 1:

                                            if self._board[g_row_below][g_col] == self._rook_b1 or \
                                                    self._board[g_row_below][g_col] == self._rook_b2:

                                                return True   # red is in check
                                        
                                        # if this is the second piece found, check for the cannon
                                        if below_piece_counter == 2:

                                            if self._board[g_row_below][g_col] == self._cannon_b1 or \
                                                    self._board[g_row_below][g_col] == self._cannon_b2:

                                                return True   # red is in check

                                    else:   # enemy player is black, check for red attacker

                                        if below_piece_counter == 1:

                                            if self._board[g_row_below][g_col] == self._rook_r1 or \
                                                    self._board[g_row_below][g_col] == self._rook_r2:

                                                return True   # black is in check
                                        
                                        # if this is the second piece found, check for the cannon
                                        if below_piece_counter == 2:

                                            if self._board[g_row_below][g_col] == self._cannon_r1 or \
                                                    self._board[g_row_below][g_col] == self._cannon_r2:

                                                return True   # red is in check
                                    
                                    if below_piece_counter > 2:

                                        break   # found 3 pieces, break out of the loop

                                g_row_below += 1   # check next space below

                        # knight check - generate all possible knight coordinates
                        knight_coordinates = [
                            [g_row-2, g_col+1],
                            [g_row-2, g_col-1],
                            [g_row-1, g_col+2],
                            [g_row-1, g_col-2],
                            [g_row+2, g_col+1],
                            [g_row+2, g_col-1],
                            [g_row+1, g_col+2],
                            [g_row+1, g_col-2]
                        ]

                        # iterate through potential coordinates to see if there are any enemy knights
                        for k_potentials in knight_coordinates:

                            # check if the coordinate would be on the board
                            if k_potentials[0] > -1 and k_potentials[0] < 10 and \
                                    k_potentials[1] > -1 and k_potentials[1] < 9:

                                if self._board[k_potentials[0]][k_potentials[1]] != 0:

                                    if enemy_player == "red":   # check for black attackers

                                        if self._board[k_potentials[0]][k_potentials[1]] == self._knight_b1 or \
                                                self._board[k_potentials[0]][k_potentials[1]] == self._knight_b2:

                                            return True
                                    
                                    else:   # check for red attackers

                                        if self._board[k_potentials[0]][k_potentials[1]] == self._knight_r1 or \
                                                self._board[k_potentials[0]][k_potentials[1]] == self._knight_r2:

                                            return True
        
        return False   # enemy_player general is not in check - no valid attackers found

    def flying_general(self):

        # get the coordinates of the red general
        for row in range(0,10):

            for col in range(0,9):

                # check if the piece is in that space
                if self._board[row][col] != 0:

                    # check if the piece is the enemy general
                    if self._board[row][col].get_piece_type() == "general" and \
                            self._board[row][col].get_player_color() == "red":

                        g_row = row   # general row
                        g_col = col   # general col
                        
                        # look down the board to see if it can see the black general
                        # with no pieces in between
                        for i in range(g_row+1, 10):

                            # find the first piece in between, if it is not a general
                            # return false, if it is a general, return True
                            if self._board[i][g_col] != 0:

                                if self._board[i][g_col].get_piece_type() != "general":

                                    return False
                                
                                if self._board[i][g_col].get_piece_type() == "general":
                                    # print("There is a flying general! Invalid move. Try again! ")

                                    return True
        
        # return false if no pieces were found below the red general
        return False

    # takes two parameters (position moved from and moved to), also returns T or F based on move conditions
    def make_move(self, start, stop):
        start_coordinates = self.get_coordinates(start)
        stop_coordinates = self.get_coordinates(stop)
        current_player = self.get_current_player()

        # check if the player sent in the same thing for start and stop
        if start == stop:
            # print("That start and stop are the same! Try again! ")

            return False

        # check if there is a piece in that location
        if self._board[start_coordinates[0]][start_coordinates[1]] == 0:
            # print("There is no piece in that starting location! Try again! ")

            return False
        
        # check if the piece in that location is the same as the current player
        if self._board[start_coordinates[0]][start_coordinates[1]].get_player_color() != current_player:
            # print("That is not your piece! Try again! ")

            return False

        # if the space is not empty, check if there is an allied piece already in the stop coordinates
        if self._board[stop_coordinates[0]][stop_coordinates[1]] != 0:

            if self._board[stop_coordinates[0]][stop_coordinates[1]].get_player_color() == current_player:
                # print("You already have an allied piece in that location! Try again! ")

                return False
        
        # if an opponents piece is here, see if can move there and then delete the enemy piece
        # from the pieces list and then move the allied piece to that stop location
        # if it is empty, then just see if can move there and then move the piece if can
        # if the space is empty, check if that piece is able to move to that location under
        # the game rules
        if self._board[start_coordinates[0]][start_coordinates[1]].check_valid_move(start_coordinates,
                                                                                    stop_coordinates,
                                                                                    self._board) is True:

            # if the space has an enemy piece remove it from the pieces list
            if self._board[stop_coordinates[0]][stop_coordinates[1]] != 0:
                piece_to_remove = self._board[stop_coordinates[0]][stop_coordinates[1]]
                self._board[stop_coordinates[0]][stop_coordinates[1]] = \
                    self._board[start_coordinates[0]][start_coordinates[1]]
                self._board[start_coordinates[0]][start_coordinates[1]] = 0

                # check for a flying general, if True, reset the board and return False
                if self.flying_general() is True:
                    self._board[start_coordinates[0]][start_coordinates[1]] = \
                        self._board[stop_coordinates[0]][stop_coordinates[1]]
                    self._board[stop_coordinates[0]][stop_coordinates[1]] = piece_to_remove

                    return False

                self._pieces.remove(piece_to_remove)   # do I need to actually remove it from the list?

            # if the stop space was empty, just move the piece there
            else:
                self._board[stop_coordinates[0]][stop_coordinates[1]] = \
                    self._board[start_coordinates[0]][start_coordinates[1]]
                self._board[start_coordinates[0]][start_coordinates[1]] = 0

                # check for flying general, if True, reset the board and return False
                if self.flying_general() is True:
                    self._board[start_coordinates[0]][start_coordinates[1]] = \
                        self._board[stop_coordinates[0]][stop_coordinates[1]]
                    self._board[stop_coordinates[0]][stop_coordinates[1]] = 0

                    return False

            # check if the red general is in check
            if self.general_check("red") is True:

                # if the red general is already in check and found to still
                # be in check, then black won the game, else just set red to in check True
                if self._red_in_check is True:
                    self.set_game_state("BLACK_WON")

                else:
                    self._red_in_check = True

            # red general was found to not be in check, so set to False
            else:
                self._red_in_check = False
            
            # check if the black general is in check
            if self.general_check("black") is True:

                # if the black general is already in check and found to still
                # be in check, then red won the game, else just set black in check to True
                if self._black_in_check is True:
                    self.set_game_state("RED_WON")

                else:
                    self._black_in_check = True

            # black general was found to not be in check, so set to False
            else:
                self._black_in_check = False
            
            # increment the turn counter since a valid move was made
            self._turn_counter += 1

            return True

        else:
            # print("The piece either cannot move in that direction, or something is in the way! Try again! ")

            return False

    # takes parameter 'red' or 'black' and returns T if player is in check, otherwise F
    def is_in_check(self, player_color):

        if player_color == "red":

            return self._red_in_check   # False by default, can change to True based on make_move conditions

        else:   # if player_color == 'black'

            return self._black_in_check   # False by default, can change to True based on make_move conditions


# class defines pieces on the board - piece type, location, color, which piece specifically
class Piece:

    def __init__(self, piece_type, location, color, name):
        self._piece_type = piece_type   # piece type (i.e. rook_r1 versus pawn_b4)
        self._location = location   # current location (start) of piece on board stored in piece objects
        self._player_color = color   # attribute color for pieces, 'red' or 'black'
        self._name = name

    def get_name(self):

        return self._name

    def get_piece_type(self):

        return self._piece_type
    
    def get_location(self):

        return self._location
    
    def get_player_color(self):

        return self._player_color


# class sets rules for rook piece movement through check_valid_move
class Rook(Piece):

    # returns T/F for valid moves on board, takes start and stop positions as parameters
    def check_valid_move(self, start, stop, board):
        
        col1 = start[1]   # set 'rook r1' start column to second number in [0,0]
        row1 = start[0]
        col2 = stop[1]   # for 'a3', [2,0] = [row, col] so col2 = 0
        row2 = stop[0]   # row1 = 2

        # move rook downward
        if col1 == col2 and row1 < row2:

            while row1 != row2:

                if row1 < row2:

                    # check if the piece is blocked by a piece in the next space (assuming
                    # that next space is not the stop location
                    if board[row1+1][col1] != 0 and (row1+1) != row2:
                        # print("Piece is blocked! Try again!")

                        return False

                    else:
                        row1 += 1

            return True   # row1 == row2, move valid

        # move rook upward
        if col1 == col2 and row1 > row2:

            while row1 != row2:

                if row1 > row2:

                    # check if piece is blocked by piece in next space (assuming next space is not the stop location
                    if board[row1-1][col1] != 0 and (row1-1) != row2:
                        # print("Piece is blocked! Try again!")

                        return False

                    else:
                        row1 -= 1

            return True

        # move rook to the right
        if row1 == row2 and col1 < col2:

            while col1 != col2:

                if col1 < col2:

                    # check if piece is blocked by piece in next space (assuming next space is not the stop location)
                    if board[row1][col1+1] != 0 and (col1+1) != col2:
                        # print("Piece is blocked! Try again!")

                        return False

                    else:
                        col1 += 1

            return True   # col1 == col2, move valid

        # move rook to the left
        if row1 == row2 and col1 > col2:

            while col1 != col2:

                if col1 > col2:

                    # check if piece is blocked by piece in next space (assuming next space is not the stop location)
                    if board[row1][col1-1] != 0 and (col1-1) != col2:
                        # print("Piece is blocked! Try again!")

                        return False

                    else:
                        col1 -= 1

            return True

        return False   # move invalid


# class sets rules for knight piece movement through check_valid_move
class Knight(Piece):

    # returns T/F for valid moves on board, takes start and stop positions as parameters
    def check_valid_move(self, start, stop, board):

        # RULES: knight cannot jump over other pieces immediately in front of the direction they are moving
        # good test case since elephant r1 blocks knight r1 initially
        col1 = start[1]   # 'knight r1' is 'b1' aka [0,1] so col1 = 1
        row1 = start[0]   # row1 = 0
        col2 = stop[1]   # for 'd2' aka [1,3] = [row, col], col2 = 3
        row2 = stop[0]   # row2 = 1

        # one absolute value difference must be 1 and the other must be 2, otherwise it is not a valid knight move
        if abs(row1-row2) != 1 or abs(col1-col2) != 2:

            if abs(row1-row2) != 2 or abs(col1-col2) != 1:
                # print("Not a valid knight move! Try again!")

                return False

        # check for collision on the way (no need to check the end location since
        # that is checked in make_move()). The only potential squares that could
        # collide are on the row/col that has an absolute value of 2
        
        # moving up and down, check along the column
        if abs(row1-row2) == 2:

            # moving down
            if row1 < row2:

                if board[row1+1][col1] != 0:
                    # print("Piece is blocked! Try again!")

                    return False
                
            # moving up
            else:

                if board[row1-1][col1] != 0:
                    # print("Piece is blocked! Try again!")

                    return False

        # moving left and right, check along the row
        else:

            # moving to the right
            if col1 < col2:

                if board[row1][col1+1] != 0:
                    # print("Piece is blocked! Try again!")

                    return False

            # moving to the left
            else:

                if board[row1][col1-1] != 0:
                    # print("Piece is blocked! Try again!")

                    return False

        return True


# class sets rules for elephant piece movement through check_valid_move
class Elephant(Piece):

    # returns T/F for valid moves on board, takes start and stop positions as parameters
    def check_valid_move(self, start, stop, board):

        # RULES: elephant cannot cross river (river is row1 = 4 or 5), cannot jump over others in diagonal path,
        # moves in diagonal motion of 2 spaces only (cannot move diagonal 1 space)
        col1 = start[1]   # 'elephant r1' is 'c1' aka [0,2] so col1 = 2
        row1 = start[0]   # row1 = 0
        col2 = stop[1]   # for 'a3' aka [2,0] = [row, col], col2 = 0
        row2 = stop[0]   # row2 = 2

        # move elephant diagonal down-left
        if row1 < row2 and col1 > col2:

            while row1 != row2:

                if row1 < 5:

                    # check for collision
                    if board[row1+1][col1-1] != 0:

                        return False

                    row1 += 2
                    col1 -= 2

                    if row1 > 4:

                        return False   # elephant red cannot cross river/touch row [5]
                
                if row1 > 4:

                    # check for collision
                    if board[row1+1][col1-1] != 0:

                        return False

                    row1 += 2
                    col1 -= 2

                    if row1 < 5:

                        return False   # elephant black cannot cross river/touch row [4]

            return True   # move valid

        # move elephant diagonal down-right
        if row1 < row2 and col1 < col2:

            while row1 != row2:

                if row1 < 5:

                    # check for collision
                    if board[row1+1][col1+1] != 0:

                        return False

                    row1 += 2
                    col1 += 2

                    if row1 > 4:

                        return False   # elephant red cannot cross river/touch row [5]
                
                if row1 > 4:

                    # check for collision
                    if board[row1+1][col1+1] != 0:

                        return False

                    row1 += 2
                    col1 += 2

                    if row1 < 5:

                        return False   # elephant black cannot cross river/touch row [4]

            return True  # move valid

        # move elephant diagonal up-left
        if row1 > row2 and col1 > col2:

            while row1 != row2:

                if row1 < 5:

                    # check for collision
                    if board[row1-1][col1-1] != 0:

                        return False

                    row1 -= 2
                    col1 -= 2

                    if row1 > 4:

                        return False   # elephant red cannot cross river/touch row [5]
                
                if row1 > 4:

                    # check for collision
                    if board[row1-1][col1-1] != 0:

                        return False

                    row1 -= 2
                    col1 -= 2

                    if row1 < 5:

                        return False   # elephant black cannot cross river/touch row [4]

            return True  # move valid

        # move elephant diagonal up-right
        if row1 > row2 and col1 < col2:

            while row1 != row2:

                if row1 < 5:

                    # check for collision
                    if board[row1-1][col1+1] != 0:

                        return False

                    row1 -= 2
                    col1 += 2

                    if row1 > 4:

                        return False   # elephant red cannot cross river/touch row [5]
                
                if row1 > 4:

                    # check for collision
                    if board[row1-1][col1+1] != 0:

                        return False

                    row1 -= 2
                    col1 += 2

                    if row1 < 5:

                        return False   # elephant black cannot cross river/touch row [4]

            return True  # move valid
        
        return False


# class sets rules for cannon piece movement through check_valid_move
class Cannon(Piece):

    # returns T/F for valid moves on board, takes start and stop positions as parameters
    def check_valid_move(self, start, stop, board):

        # RULES: cannon moves like rook but when capturing, it needs to jump over one and only one
        # piece to capture the enemy piece, can jump over ally/enemy

        col1 = start[1]  # set 'cannon r1' start at 'b3' aka [2,1]
        row1 = start[0]
        col2 = stop[1]  # for 'b7', [6,1] = [row, col] so col2 = 1
        row2 = stop[0]  # row2 = 6

        # check if the cannon is capturing a piece or moving to an empty piece
        capturing = False

        if board[row2][col2] != 0:
            capturing = True

        # move cannon downward
        if col1 == col2 and row1 < row2:

            if capturing is False:

                while row1 != row2:

                    # check if the piece is blocked by a piece in the next space (assuming
                    # that next space is not the stop location
                    if board[row1+1][col1] != 0 and (row1+1) != row2:
                        # print("Piece is blocked! Try again!")

                        return False

                    else:
                        row1 += 1

                return True   # row1 == row2, move valid
            
            if capturing is True:
                number_of_pieces_between = 0

                for check_coordinate in range(row1+1, row2):

                    if board[check_coordinate][col1] != 0:
                        number_of_pieces_between += 1
                
                if number_of_pieces_between != 1:

                    return False

                else:

                    return True

        # move cannon upward
        if col1 == col2 and row1 > row2:

            if capturing is False:

                while row1 != row2:

                    # check if the piece is blocked by a piece in the next space (assuming
                    # that next space is not the stop location
                    if board[row1-1][col1] != 0 and (row1-1) != row2:
                        # print("Piece is blocked! Try again!")

                        return False

                    else:
                        row1 -= 1

                return True   # row1 == row2, move valid
            
            if capturing is True:
                number_of_pieces_between = 0

                for check_coordinate in range(row2+1, row1):

                    if board[check_coordinate][col1] != 0:
                        number_of_pieces_between += 1
                
                if number_of_pieces_between != 1:

                    return False

                else:

                    return True

        # move cannon to the right
        if row1 == row2 and col1 < col2:

            if capturing is False:

                while col1 != col2:
                    # check if the piece is blocked by a piece in the next space (assuming
                    # that next space is not the stop location

                    if board[row1][col1+1] != 0 and (col1+1) != col2:
                        # print("Piece is blocked! Try again!")

                        return False

                    else:
                        col1 += 1

                return True   # col1 == col2, move valid
            
            if capturing is True:
                number_of_pieces_between = 0

                for check_coordinate in range(col1+1, col2):

                    if board[row1][check_coordinate] != 0:
                        number_of_pieces_between += 1
                
                if number_of_pieces_between != 1:

                    return False

                else:

                    return True

        # move cannon to the left
        if row1 == row2 and col1 > col2:

            if capturing is False:

                while col1 != col2:

                    # check if the piece is blocked by a piece in the next space (assuming
                    # that next space is not the stop location
                    if board[row1][col1-1] != 0 and (col1-1) != col2:
                        # print("Piece is blocked! Try again!")

                        return False

                    else:
                        col1 -= 1

                return True   # col1 == col2, move valid
            
            if capturing is True:
                number_of_pieces_between = 0

                for check_coordinate in range(col2+1, col1):

                    if board[row1][check_coordinate] != 0:
                        number_of_pieces_between += 1
                
                if number_of_pieces_between != 1:

                    return False

                else:

                    return True

        return False   # move invalid


# class sets rules for red pawn piece movement through check_valid_move
class Pawn_Red(Piece):

    # returns T/F for valid moves on board, takes start and stop positions as parameters
    def check_valid_move(self, start, stop, board):

        # RULES: pawn moves one space forward only until it crosses the river,
        # row [4], then it can begin to move left/right one space as well

        col1 = start[1]  # 'c4' = [3,2]
        row1 = start[0]   # row1 = 3
        col2 = stop[1]  # 'c5' = [4,2]
        row2 = stop[0]  # row2 = 4


        if row1 < 5:   # so if pawn is at row [3] or [4], move down only

            while row1 == (row2-1):

                if row1 < row2:
                    row1 += 1   # moves 1 space down

                    return True   # move valid

                else:

                    return False  # cannot move backward

            return False   # all other not pawn-like movements invalid


        if row1 > 4 and col1 > col2:   # enemy side of river, move left

            while col1 > col2:

                if col1 != col2:
                    col1 -= 1   # moves 1 space left

                    return True  # move valid

                else:

                    return False  # cannot move backward

            return False  # all other not pawn-like movements invalid

        if row1 > 4 and col1 < col2:   # enemy side of river, move right

            while col1 < col2:

                if col1 != col2:
                    col1 += 1   # moves 1 space right

                    return True  # move valid

                else:

                    return False  # cannot move backward

            return False  # all other not pawn-like movements invalid

        if row1 > 4 and col1 == col2:

            while row1 != row2:

                if row1 < row2:  # moves 1 space forward
                    row1 +=1   # pawn moves down 1

                    return True  # move valid

                else:

                    return False  # cannot move backward

            return False  # all other not pawn-like movements invalid


# class sets rules for black pawn piece movement through check_valid_move
class Pawn_Black(Piece):

    # returns T/F for valid moves on board, takes start and stop positions as parameters
    def check_valid_move(self, start, stop, board):

        # RULES: pawn moves one space forward only until it crosses the river,
        # row [4], then it can begin to move left/right one space as well

        col1 = start[1]  # 'c7' = [6,2]
        row1 = start[0]   # row1 = 6
        col2 = stop[1]  # 'c6' = [5,2]
        row2 = stop[0]  # row2 = 5

        if row1 > 4:   # so if pawn is at row 3 or 4, move up only

            while row1 == (row2+1):

                if row1 > row2:
                    row1 -= 1   # moves 1 space up

                    return True   # move valid

                else:

                    return False  # cannot move backward

            return False   # all other not pawn-like movements invalid


        if row1 < 5 and col1 > col2:   # enemy side of river, move left

            while col1 > col2:

                if col1 != col2:
                    col1 -= 1   # moves 1 space left

                    return True  # move valid

                else:

                    return False  # cannot move backward

            return False  # all other not pawn-like movements invalid

        if row1 < 5 and col1 < col2:   # enemy side of river, move right

            while col1 < col2:

                if col1 != col2:
                    col1 += 1   # moves 1 space right

                    return True  # move valid

                else:

                    return False  # cannot move backward

            return False  # all other not pawn-like movements invalid

        if row1 < 5 and col1 == col2:

            while row1 != row2:

                if row1 > row2:  # moves 1 space forward
                    row1 -=1   # pawn moves up 1

                    return True  # move valid

                else:

                    return False  # cannot move backward

            return False  # all other not pawn-like movements invalid
    

# class sets rules for guard piece movement through check_valid_move
class Guard(Piece):

    # returns T/F for valid moves on board, takes start and stop positions as parameters
    def check_valid_move(self, start, stop, board):
        col1 = start[1]  # 'c7' = [6,2]
        row1 = start[0]   # row1 = 6
        col2 = stop[1]  # 'c6' = [5,2]
        row2 = stop[0]  # row2 = 5

        # start and stop are inside the palace
        if col1 < 3 or col1 > 5 or col2 < 3 or col2 > 5:

            return False
        
        # pieces are only moving 1 diagonal space
        if abs(row1-row2) != 1 or abs(col1-col2) != 1:

            return False

        # if the guard is red
        if self.get_player_color() == "red":

            if row1 < 0 or row1 > 2 or row2 < 0 or row2 > 2:

                return False

        # if the guard is black
        else:

            if row1 < 7 or row1 > 9 or row2 < 7 or row2 > 9:

                return False

        # no need to check collisions since can only move one space and check for an allied piece done in make_move()
        return True


# class sets rules for general piece movement through check_valid_move
class General(Piece):

    # returns T/F for valid moves on board, takes start and stop positions as parameters
    def check_valid_move(self, start, stop, board):
        col1 = start[1]  # 'c7' = [6,2]
        row1 = start[0]   # row1 = 6
        col2 = stop[1]  # 'c6' = [5,2]
        row2 = stop[0]  # row2 = 5
    
        # start and stop are inside the palace
        if col1 < 3 or col1 > 5 or col2 < 3 or col2 > 5:

            return False
        
        # if the general is red
        if self.get_player_color() == "red":

            if row1 < 0 or row1 > 2 or row2 < 0 or row2 > 2:

                return False

        # if the general is black
        else:

            if row1 < 7 or row1 > 9 or row2 < 7 or row2 > 9:

                return False

        # piece either moves along row or column - total absolute value between two rows and two columns
        # does not equal 1, then the piece did not move one space up/down or left/right
        if (abs(row1-row2) + abs(col1-col2)) != 1:

            return False
        
        # no need to check collisions since can only move one space and check for an allied piece done in make_move()
        return True
    

# returns T/F to determine if input was valid
def valid_input_check(user_input):
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]

    try:
        int(user_input[1:])
    except ValueError:
        return False

    if len(user_input) < 2 or len(user_input) > 3:
        return False
    elif int(user_input[1:]) < 1 or int(user_input[1:]) > 10:
        return False
    elif user_input[0] not in letters:
        return False
    else:
        return True


# set up the game
game = XiangqiGame()
game.start_game()


# runs interactive game (with print statements to prompt user)
while(game.get_game_state() == "UNFINISHED"):
    print()
    print("Current board: ")
    print()
    game.print_pretty_board()
    print()

    # ask the player what piece they want to move where and make sure the input is valid
    print("What piece do you want to move (enter coordinates like a1):")
    start = input()
    while(valid_input_check(start) is not True):
        print("You entered invalid start coordinates not on the board! Please try again: ")
        start = input()

    print("Where do you want to move it to (enter coordinates like c3)?")
    stop = input()
    while(valid_input_check(stop) is not True):
        print("You entered invalid stop coordinates not on the board! Please try again: ")
        stop = input()

    game.make_move(start, stop)


# game = XiangqiGame()
# move_result = game.make_move('c1', 'e3')
# print("black in check?")
# black_in_check = game.is_in_check('black')
# print(black_in_check)   # returns False, check
# game.make_move('e7', 'e6')
# state = game.get_game_state()
# print(state)   # returns UNFINISHED, check

# print("red in check?")
# print(game.is_in_check("red")) # should be True
# print(game.get_game_state()) # should be UNFINISHED
# game.make_move('a2', 'a1')
# print(game.get_game_state()) # should be BLACK_WON

# # To grader: if you want to do a bunch of make_move() calls and then check the game state
# # here is the following I have done myself to check various cases for my pieces in game
# # example of a red player winning with a cannon:
# game.make_move('b3', 'd3')
# game.make_move('a10', 'a9')
# game.make_move('d3', 'd6')
# game.make_move('a9', 'f9')
# game.make_move('d6', 'e6')
# print("black in check? ")
# print(game.is_in_check("black")) # should be True
# print(game.get_game_state()) # should be UNFINISHED
# game.make_move('f9', 'f3')
# print(game.get_game_state()) # should be RED_WON

# # example of a black player moving out of check:
# game.make_move('b3', 'd3')
# game.make_move('a10', 'a9')
# game.make_move('d3', 'd6')
# game.make_move('a9', 'f9')
# game.make_move('d6', 'e6')
# print("black in check? ")
# print(game.is_in_check("black")) # should be True
# print(game.get_game_state()) # should be UNFINISHED
# game.make_move('f9', 'e9')
# # this move the rook in between the attacking cannon, meaning 2 pieces in between, general no longer in check
# print(game.get_game_state()) # should be UNFINISHED
# game.make_move('e6', 'd6') # move the cannon out of attacking position
# print(game.is_in_check("black")) # should be False
# print(game.get_game_state()) # should be UNFINISHED

# # example of a black player winning with a knight
# game.make_move('i1', 'i2')
# game.make_move('b10', 'c8')
# game.make_move('a1', 'a2')
# game.make_move('c7', 'c6')
# game.make_move('a2', 'a1')
# game.make_move('c8', 'd6')
# game.make_move('a1', 'a2')
# game.make_move('d6', 'f5')
# game.make_move('e1', 'e2')
# game.make_move('f5', 'd4')
# print("red in check?")
# print(game.is_in_check("red")) # should be True
# print(game.get_game_state()) # should be UNFINISHED
# game.make_move('a2', 'a1')
# print(game.get_game_state()) # should be BLACK_WON

# # example of a black player winning with a rook
# game.make_move('i1', 'i2')
# game.make_move('a10', 'a9')
# game.make_move('a1', 'a2')
# game.make_move('a9', 'd9')
# game.make_move('a2', 'a1')
# game.make_move('d9', 'd3')
# game.make_move('a1', 'a2')
# game.make_move('d3', 'e3')
# print("red in check?")
# print(game.is_in_check("red")) # should be True
# print(game.get_game_state()) # should be UNFINISHED
# game.make_move('a2', 'a1')
# print(game.get_game_state()) # should be BLACK_WON

# # Fancy game loop: comment the code all the way below and follow
# # the instructions of the program. (and uncomment import copy)
# # and uncomment the print_board, print_pretty_board, and valid_input_check
# # functions above
# # run the game until the game state changes because either red or black won
# # or there is a stalemate. At that point, change the game state and game ends

#     print("Red in check? ")
#     print(game.is_in_check("red"))
#     print("Black in check? ")
#     print(game.is_in_check("black"))
#     print(game.get_game_state())

# print("Final Result: ")
# print(game.get_game_state())
