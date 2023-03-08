class Board:
     def __init__(self, number_of_rows, number_of_cols):
        self.number_of_rows = number_of_rows
        self.number_of_cols = number_of_cols
        self.grid = []
        # Populate the board with empty spaces
        for i in range(number_of_rows):
            line = []
            for j in range(number_of_cols):
                line.append(None)
            self.grid.append(line)

     def move_piece(self, initial_pos: tuple, final_pos: tuple):
        """
        Moves a piece from initial position to final position
        
        :param initial_pos: initial position of the piece
        
        :param final_pos: final position of the piece
        
        :return: None

        :raises: Exception if the piece cannot be moved
        """

        if self.grid[initial_pos[0]][initial_pos[1]] is None:
            raise Exception("There is no piece at the initial position")
        
        if self.grid[final_pos[0]][final_pos[1]] is not None:
            raise Exception("There is piece at the final position")
        
        self.grid[final_pos[0]][final_pos[1]] = self.grid[initial_pos[0]][initial_pos[1]]
        self.grid[initial_pos[0]][initial_pos[1]] = None
        if abs(initial_pos[0] - final_pos[0]) == 2:
            row_to_remove = (initial_pos[0] + final_pos[0]) // 2
            column_to_remove = (initial_pos[1] + final_pos[1]) // 2
            self.remove_piece(self.grid[row_to_remove][column_to_remove])

     def place_piece(self, piece):
        """
        Places a piece on the board
        
        :param piece: the piece to be placed on the board
        
        :return: None

        :raises: Exception if the piece cannot be placed
        """

        if self.grid[piece.position[0]][piece.position[1]] is not None:
            raise Exception("There is already a piece at that position")
        
        self.grid[piece.position[0]][piece.position[1]] = piece

     def remove_piece(self, piece):
        """
        Removes a piece from the board
        
        :param piece: the piece to be removed from the board
        
        :return: None

        :raises: Exception if the piece cannot be removed
        """

        if self.grid[piece.position[0]][piece.position[1]] is None:
            raise Exception("There is no piece at that position")
        
        self.grid[piece.position[0]][piece.position[1]] = None