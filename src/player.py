class Player:
    
    def __init__(self, name: str, color: str):
        """
        Creates a Player insrtance with a given name
        :param name:
            (str) - name of the player
        :param color:
            (str) - color of the player
        """
        self.name = name
        self.color = color

    def __repr__(self):
        return f"{self.name}"