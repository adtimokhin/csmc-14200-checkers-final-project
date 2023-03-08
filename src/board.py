class Board:
     def __init__(self, number_of_rows, number_of_cols):
        self.number_of_rows = number_of_rows
        self.number_of_cols = number_of_cols
        self.board = []
        # Populate the board with empty spaces
        for i in range(number_of_rows):
            line = []
            for j in range(number_of_cols):
                line.append(None)
            self.board.append(line)
