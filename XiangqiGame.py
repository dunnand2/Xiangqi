
import copy

class XiangqiGame:
    """class for xiangqi game. holds pieces and controls game."""
    def __init__(self):
        self.__player_turn = "red"
        self.__red_pieces = []
        self.__black_pieces = []
        self.__board = []
        self.__column_letters = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8}
        self.__game_state = "UNFINISHED"

        # Create 2D array to be used as board
        self._create_board()

        # Add pieces to board
        self._setup_board()

        # Add all pieces to separate lists to signify each pieces team. This will hopefully make it easier to search if
        # general is in check
        self._add_pieces_to_team_lists()

    def get_board(self):
        """returns current board"""
        return self.__board

    def get_game_state(self):
        return self.__game_state

    def get_piece(self, row, column):
        return self.__board[row][column]

    def is_in_check(self, team, board=None):
        """takes red or black as parameter, and returns whether that team's general is in check"""

        # if no board is given use current board
        if board is None:
            board = self.__board

        # initialize general row and column to zero as placeholder
        general_row = 0
        general_column = 0

        if team == "red":
            for row in range(10):
                for column in range(9):
                    piece = board[row][column]
                    if piece is None:
                        pass
                    else:
                        if type(piece) == General and piece.get_player() == "red":
                            general_row = piece.get_row()
                            general_column = piece.get_column()

            for piece in self.__black_pieces:
                if piece.is_legal_move(general_row, general_column, board):
                    return True
            return False

        if team == "black":
            for row in range(10):
                for column in range(9):
                    piece = board[row][column]
                    if piece is None:
                        pass
                    else:
                        if type(piece) == General and piece.get_player() == "black":
                            general_row = piece.get_row()
                            general_column = piece.get_column()

            for piece in self.__red_pieces:
                if piece.is_legal_move(general_row, general_column, board):
                    return True
            return False

    def is_checkmate(self, team):
        """method that searches all possible moves to see if there is a checkmate"""
        if team == "black":
            for piece in self.__black_pieces:
                for next_row in range(10):
                    for next_column in range(9):
                        if self._test_move(piece.get_row(), piece.get_column(), next_row, next_column):
                            return False
            self.__game_state = 'RED_WON'
            return True

        if team == "red":
            for piece in self.__red_pieces:
                for next_row in range(10):
                    for next_column in range(9):
                        if self._test_move(piece.get_row(), piece.get_column(), next_row, next_column):
                            return False
            self.__game_state = 'BLACK_WON'
            return True

    def make_move(self, current_square, next_square, board=None):

        # Use current game board if no other board is passed to the function
        if board is None:
            board = self.get_board()

        if self.__game_state != "UNFINISHED":
            return False

        # get row and column index from square notation
        current_row, current_column = self._get_column_and_row(current_square)

        # assign the current piece from the board to "piece" (None if there is no piece on the given square)
        piece = board[current_row][current_column]

        # get row and column index of the square the piece is to be moved to
        next_row, next_column = self._get_column_and_row(next_square)

        # if no piece in space, return False, not a valid move
        if piece is None:
            return False

        # if the piece belongs to the player when it is not their turn, return false
        if self.__player_turn != piece.get_player():
            return False

        # if the move passes the test move function and is valid, move the piece
        if self._test_move(current_row, current_column, next_row, next_column):

            # assign next piece to a variable to remove it from the piece list
            next_piece = board[next_row][next_column]
            if next_piece is not None:
                if next_piece.get_player() == "black":
                    self.__black_pieces.remove(next_piece)
                else:
                    self.__red_pieces.remove(next_piece)

            # Change the piece object's attributes storing its location
            piece.move_piece(next_row, next_column, board)

            # Update the board to the new board locations
            board[next_row][next_column] = piece
            board[current_row][current_column] = None

            # Update the players turn
            if self.__player_turn == "red":
                self.__player_turn = "black"
                if self.is_checkmate("black"):
                    print("Checkmate!")

            else:
                self.__player_turn = "red"
                if self.is_checkmate("red"):
                    print("Checkmate!")

            return True

    def print_board(self):
        """function that prints out board for user. If space is empty prints 'x', else prints piece abbreviation"""

        # for loop that prints iterates through the board and prints each space
        for i in range(len(self.__board)):

            # print the river
            if i == 5:
                print()
            for j in range(len(self.__board[i])):

                # if space is empty print an x
                if self.__board[i][j] is None:
                    print("x  ", end="")

                # else print the abbreviation of the piece
                else:
                    piece = self.__board[i][j]
                    piece.print_piece_on_board()
            print("")
        print("\n")

    def _add_pieces_to_team_lists(self):
        """function that adds all pieces to one of two lists, separating them by team"""
        for i in range(10):
            for j in range(9):
                if self.__board[i][j] is not None:
                    piece = self.__board[i][j]
                    if piece.get_player() == "red":
                        self.__red_pieces.append(piece)
                    else:
                        self.__black_pieces.append(piece)

    def _check_for_own_piece(self, piece, next_piece):
        """returns false if next square has a piece on the same team"""
        if next_piece is not None:
            if next_piece.get_player() == piece.get_player():
                return False
            else:
                return True
        else:
            return True

    def _create_board(self):
        """functions that creates the 2D array that will be used as the board"""
        for i in range(10):
            column = []
            for j in range(9):
                column.append(None)
            self.__board.append(column)

    def _get_column_and_row(self, board_square):
        """function to take a board square (ie c4) and return the row and column index of that square"""
        # get letter of the column from the board square parameter
        col = board_square[0]

        column_index = self.__column_letters[col]
        row_index = int(board_square[1:]) - 1
        return row_index, column_index

    def _setup_board(self):
        """function that sets all initial pieces to their correct locations on the board"""
        self.__board[0][0] = Chariot(0, 0, player="red")
        self.__board[0][1] = Horse(0, 1, player="red")
        self.__board[0][2] = Elephant(0, 2, player="red")
        self.__board[0][3] = Advisor(0, 3, player="red")
        self.__board[0][4] = General(0, 4, player="red")
        self.__board[0][5] = Advisor(0, 5, player="red")
        self.__board[0][6] = Elephant(0, 6, player="red")
        self.__board[0][7] = Horse(0, 7, player="red")
        self.__board[0][8] = Chariot(0, 8, player="red")
        self.__board[2][1] = Cannon(2, 1, player="red")
        self.__board[2][7] = Cannon(2, 7, player="red")
        self.__board[3][0] = Soldier(3, 0, player="red")
        self.__board[3][2] = Soldier(3, 2, player="red")
        self.__board[3][4] = Soldier(3, 4, player="red")
        self.__board[3][6] = Soldier(3, 6, player="red")
        self.__board[3][8] = Soldier(3, 8, player="red")

        self.__board[9][0] = Chariot(9, 0, player="black")
        self.__board[9][1] = Horse(9, 1, player="black")
        self.__board[9][2] = Elephant(9, 2, player="black")
        self.__board[9][3] = Advisor(9, 3, player="black")
        self.__board[9][4] = General(9, 4, player="black")
        self.__board[9][5] = Advisor(9, 5, player="black")
        self.__board[9][6] = Elephant(9, 6, player="black")
        self.__board[9][7] = Horse(9, 7, player="black")
        self.__board[9][8] = Chariot(9, 8, player="black")
        self.__board[7][1] = Cannon(7, 1, player="black")
        self.__board[7][7] = Cannon(7, 7, player="black")
        self.__board[6][0] = Soldier(6, 0, player="black")
        self.__board[6][2] = Soldier(6, 2, player="black")
        self.__board[6][4] = Soldier(6, 4, player="black")
        self.__board[6][6] = Soldier(6, 6, player="black")
        self.__board[6][8] = Soldier(6, 8, player="black")

    def _test_move(self, current_row, current_column, next_row, next_column):
        """Tests move and sees"""

        # create a copy of the board to test new moves
        test_board = copy.deepcopy(self.__board)

        # assign the current piece from the board to "piece"
        piece = test_board[current_row][current_column]

        next_piece = test_board[next_row][next_column]

        # return False if space has no piece. It cannot be a valid move
        if piece is None:
            return False

        if not piece.move_piece(next_row, next_column, test_board) or \
                not self._check_for_own_piece(piece, next_piece):
            return False

        else:
            test_board[next_row][next_column] = piece
            test_board[current_row][current_column] = None

            temp_removal_piece = self.get_board()[next_row][next_column]

            if next_piece is None:
                check = self.is_in_check(piece.get_player(), test_board)

            elif next_piece.get_player() == "red":
                self.__red_pieces.remove(temp_removal_piece)
                check = self.is_in_check(piece.get_player(), test_board)
                self.__red_pieces.append(temp_removal_piece)

            else:
                self.__black_pieces.remove(temp_removal_piece)
                check = self.is_in_check(piece.get_player(), test_board)
                self.__black_pieces.append(temp_removal_piece)

            return not check


class Piece:
    """generic piece class that will be parent for all other pieces"""
    def __init__(self, row=0, column=0, abbreviation="", player=None):
        self._row = row
        self._column = column
        self._player = player
        self._abbreviation = abbreviation

    def move_piece(self, next_row, next_column, current_board):
        """function to move piece is move is legal"""
        if self.is_legal_move(next_row, next_column, current_board):
            self._row = next_row
            self._column = next_column
            return True
        else:
            return False

    def get_abbreviation(self):
        """return piece abbreviation"""
        return self._abbreviation

    def get_row(self):
        """returns row of piece"""
        return self._row

    def get_column(self):
        """returns column of piece"""
        return self._column

    def get_player(self):
        """returns whether piece belongs to red or black"""
        return self._player

    def print_piece_on_board(self):
        """helper function that prints type of piece to board"""
        print(self._abbreviation + " ", end="")

    def set_row(self, row):
        self._row = row

    def set_column(self, column):
        self._column = column

    def _check_for_own_piece(self, next_piece):
        """returns false if next square has a piece on the same team"""
        if next_piece is not None:
            if next_piece.get_player() == self.get_player():
                return False
            else:
                return True
        else:
            return True

class General(Piece):
    """class for the general piece. Inherits from the piece class"""
    def __init__(self, row, column, abbreviation='Gn', player=0):
        super().__init__(row, column, abbreviation, player)

    def is_legal_move(self, row, column, current_board):
        """checks if the proposed move is legal"""

        # check if general is moving more than one row or column at a time
        if (abs(self._row - row) > 1) or (abs(self._column - column) > 1):
            return False

        # check if general is not moving orthogonally
        if (abs(self._column - column) > 0) and (abs(self._row - row) > 0):
            return False

        # check if general is within palace columns
        if column < 3 or column > 5:
            return False

        # check if general within palace rows if on red side
        if (self.get_player() == 'Black') and (row < 7 or row > 9):
            return False

        # check if general is within palace rows if on black side
        if (self.get_player() == 'Red') and (row < 0 or row > 2):
            return False

        # return True if passes all conditions
        else:
            return True


class Advisor(Piece):
    """class for the general piece. Inherits from the piece class"""
    def __init__(self, row, column, abbreviation='Ad', player=0):
        super().__init__(row, column, abbreviation, player)

    def is_legal_move(self, row, column, current_board):
        """check if the proposed move is legal"""

        # check if advisor is not moving diagonally and that it is only moving one space
        if (abs(self._column - column) != 1) or (abs(self._row - row) != 1):
            return False

        # check if advisor is within palace columns
        if column < 3 or column > 5:
            return False

        # check if advisor within palace rows if on red side
        if (self.get_player() == 'Black') and (row < 7 or row > 9):
            return False

        # check if advisor is within palace rows if on black side
        if (self.get_player() == 'Red') and (row < 0 or row > 2):
            return False

        # return True if passes all conditions
        else:
            return True


class Elephant(Piece):
    """class for the general piece. Inherits from the piece class"""
    def __init__(self, row, column, abbreviation='El', player=0):
        super().__init__(row, column, abbreviation, player)

    def is_legal_move(self, row, column, current_board):
        """check if the proposed move is legal"""

        # check if elephant is moving diagonally and that it is moving exactly two spaces
        if (abs(self._column - column) != 2) or (abs(self._row - row) != 2):
            return False

        # check that elephants path is clear
        if not self._check_if_clear_path(row, column, current_board):
            return False

        # check if elephant within does not cross river if on red side
        if (self.get_player() == 'Red') and (row > 4):
            return False

        # check if elephant within does not cross river if on black side
        if (self.get_player() == 'Black') and (row < 5):
            return False

        else:
            return True

    def _check_if_clear_path(self, row, column, current_board):
        """helper function to see if another piece is blocking the elephants move"""

        # assign intermediate row and column to the space in between the current and proposed square
        intermediate_row = int(self._row + ((row - self._row)/2))
        intermediate_column = int(self._column + ((column - self._column)/2))

        # if the intermediate space is empty return True if there is a piece Flase
        intermediate_space = current_board[intermediate_row][intermediate_column]
        if intermediate_space is not None:
            return False
        else:
            return True


class Horse(Piece):
    """class for the general piece. Inherits from the piece class"""
    def __init__(self, row, column, abbreviation='Hr', player=0):
        super().__init__(row, column, abbreviation, player)

    def is_legal_move(self, row, column, current_board):
        """check if the proposed move is legal"""

        # check if horse is always moving 1 point orthogonally and 1 point diagonally
        if not ((abs(self._column - column) == 1) and (abs(self._row - row) == 2)) or \
                ((abs(self._column - column) == 2) and (abs(self._row - row) == 1)):
            return False

        # check that horses path is clear
        if not self._check_if_clear_path(row, column, current_board):
            return False

        else:
            return True

    def _check_if_clear_path(self, row, column, current_board):
        """helper function to see if another piece is blocking the elephants move"""

        # assign intermediate row and column to the space in between the current and proposed square
        if abs(self._column - column) == 2:
            intermediate_row = self._row
            intermediate_column = int(self._column + ((column - self._column) / 2))
            intermediate_space = current_board[intermediate_row][intermediate_column]
            if intermediate_space is not None:
                return False
            else:
                return True
        elif abs(self._row - row) == 2:
            intermediate_row = int(self._row + ((row - self._row)/2))
            intermediate_column = self._column

            # if the intermediate space is empty return True if there is a piece False
            intermediate_space = current_board[intermediate_row][intermediate_column]
            if intermediate_space is not None:
                return False
            else:
                return True
        else:
            return False

class Chariot(Piece):
    """class for the general piece. Inherits from the piece class"""
    def __init__(self, row, column, abbreviation='Ch', player=0):
        super().__init__(row, column, abbreviation, player)

    def is_legal_move(self, row, column, current_board):
        """check if the proposed move is legal"""

        # check if chariot moves orthogonally only
        if (abs(self._column - column) != 0) and (abs(self._row - row) != 0):
            return False

        # check that chariot path is clear
        if not self._check_if_clear_path(row, column, current_board):
            return False

        else:
            return True

    def _check_if_clear_path(self, row, column, current_board):
        """helper function to see if another piece is blocking the elephants move"""

        # assign intermediate row and column to the space in between the current and proposed square
        if abs(self._column - column) != 0:

            # step is the variable to increment through the range of points that the chariot will pass through
            step = int((column - self._column)/abs(column - self._column))
            start = self._column + step
            stop = column
            for next_column in range(start, stop, step):
                intermediate_row = self._row
                intermediate_column = next_column
                intermediate_space = current_board[intermediate_row][intermediate_column]
                if intermediate_space is not None:
                    return False
            return True

        elif abs(self._row - row) != 0:

            # step is the variable to increment through the range of points that the chariot will pass through
            step = int((row - self._row)/abs(row - self._row))
            start = self._row + step
            stop = row
            for next_row in range(start, stop, step):
                intermediate_row = next_row
                intermediate_column = self._column
                intermediate_space = current_board[intermediate_row][intermediate_column]
                if intermediate_space is not None:
                    return False
            return True

        else:
            return False


class Cannon(Piece):
    """class for the general piece. Inherits from the piece class"""
    def __init__(self, row, column, abbreviation='Ca', player=0):
        super().__init__(row, column, abbreviation, player)

    def is_legal_move(self, row, column, current_board):
        """check if the proposed move is legal"""

        # check if cannon moves diagonally only
        if abs(self._column - column) > 0 and abs(self._row - row) > 0:
            return False

        # check that cannon path is clear
        if not self._check_if_clear_path(row, column, current_board):
            return False

        else:
            return True

    def _check_if_clear_path(self, row, column, current_board):
        """helper function to see if another piece is blocking the elephants move"""

        # get number of pieces blocking cannon's path
        number_of_pieces_in_path = self._check_number_pieces_blocking(row, column, current_board)

        # if zero or only 1 piece in path, move is valid
        if number_of_pieces_in_path == 0:
            if current_board[row][column] is not None:
                return False
            return True
        if number_of_pieces_in_path == 1:
            piece = current_board[row][column]
            if piece is None:
                return False
            elif piece.get_player() == self.get_player():
                return False
            else:
                return True
        else:
            return False

    def _check_number_pieces_blocking(self, row, column, current_board):
        """helper function to count number of pieces blocking cannon"""

        # initialize a variable to count pieces in cannons path
        number_of_pieces_in_path = 0
        row_increment = 0
        column_increment = 0

        # set the row and column to increment either 1 or -1 one depending on the proposed move
        try:
            row_increment = int((row - self.get_row())/abs(row - self.get_row()))
        except ZeroDivisionError:
            row_increment = 0
        try:
            column_increment = int((column - self._column)/abs(column - self._column))
        except ZeroDivisionError:
            column_increment = 0

        # set the loop counter to be one less than the difference between the proposed space and new space
        if column_increment != 0:
            i = abs(self.get_column() - column) - 1
        else:
            i = abs(self.get_row() - row) - 1

        intermediate_row = self.get_row()
        intermediate_column = self.get_column()

        while i > 0:
            intermediate_row += row_increment
            intermediate_column += column_increment
            intermediate_space = current_board[intermediate_row][intermediate_column]
            if intermediate_space is not None:
                number_of_pieces_in_path += 1
            i -= 1
        return number_of_pieces_in_path

class Soldier(Piece):
    """class for the general piece. Inherits from the piece class"""
    def __init__(self, row, column, abbreviation='So', player=0):
        super().__init__(row, column, abbreviation, player)

    def is_legal_move(self, row, column, current_board):
        """check if the proposed move is legal"""

        # Return false if solider moves backwards
        if self._is_moving_backward(row):
            return False

        # If solider moves more than one space return False
        if abs(self._row - row) > 1:
            return False

        # If soldier has not crossed river, return false if it moves horizontally
        if not self._has_crossed_river():
            if abs(self._column - column) != 0:
                return False

        # If soldier has crossed river, return false if it does not move orthogonally
        if self._has_crossed_river():
            if abs(self._column - column) != 0 and abs(self._row - row != 0):
                return False

            # If solider has crossed river, return false if it moves more than one space horizontally
            if abs(self._column - column) > 1:
                return False

        return True

    def _has_crossed_river(self):
        """helper function that checks if soldier has crossed river"""

        # if piece is red, check if return True if soldier has crossed river
        if self.get_player() == "red":
            if self._row > 4:
                return True
            else:
                return False
        elif self.get_player() == "black":
            if self._row < 5:
                return True
            else:
                return False

    def _is_moving_backward(self, row):
        """helper function that checks to make sure solider does not move backwards"""
        if self.get_player() == "red":
            if (self._row - row) > 0:
                return True
            else:
                return False
        elif self.get_player() == "black":
            if (self._row - row) < 0:
                return True
            else:
                return False


if __name__ == "__main__":
    game = XiangqiGame()
    move_result = game.make_move('c1', 'e3')
    black_in_check = game.is_in_check('black')
    game.make_move('e7', 'e6')
    state = game.get_game_state()
    print(state)

    """game = XiangqiGame()
    game.print_board()
    game.make_move('d1', 'e2')
    game.make_move('e1', 'd1')
    game.make_move('b8', 'c8')
    game.make_move('b3', 'b9')
    game.make_move('c8', 'c4')
    game.make_move('e2', 'd1')
    game.make_move('a10', 'a9')
    game.make_move('a4', 'a5')
    game.make_move('a9', 'b9')
    game.make_move('a5', 'a6')
    game.make_move('b9', 'b1')
    game.make_move('a6', 'a7')
    game.make_move('b1', 'a1')
    game.make_move('a7', 'b7')
    game.make_move('a1', 'c1')
    game.make_move('b7', 'c7')
    game.make_move('i10', 'i9')
    game.make_move('c7', 'd7')
    game.make_move('i9', 'e9')
    game.make_move('d7', 'e7')
    game.make_move('h8', 'f8')
    game.make_move('e7', 'f7')
    game.make_move('f8', 'f1')
    game.make_move('e1', 'f1')
    game.make_move('e9', 'e4')
    game.make_move('f7', 'g7')
    game.make_move('c1', 'c3')
    game.make_move('g7', 'h7')
    game.make_move('c3', 'f3')

    game.print_board()
    print(game.get_game_state())"""



