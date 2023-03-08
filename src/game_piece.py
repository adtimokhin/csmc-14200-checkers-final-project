class GamePiece: 
    def __init__(self, position, player):
        """
        Constructor
        :param position:
            the position of the game piece on the board 
        :param player: 
            the player who owns the piece
        :param is_king: 
            the type of the game piece (whether the checker is a king or not)
        :returns
            None
        """
        self.position = position
        self.player = player
        self.is_king = False

    def __repr__(self):
        return f"GP-{self.player}"

    def tranform(self):
        """
        Transforms a game piece into a king 
        :param None
            only self
        :returns
            None
        """
        self.is_king = not self.is_king