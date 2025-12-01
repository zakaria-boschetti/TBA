# Define the Player class.
class Player():

    """
    Représente le joueur du jeu, incluant son nom et la salle où il se trouve.

    Cette classe gère la position du joueur dans le jeu ainsi que ses déplacements.
    Le joueur possède un nom et est présent dans un lieu dit  (current_room),
    qui peut changer lorsqu'il se déplace via les sorties définies dans chaque salle .

    Attribus:
    ----------
    name : str
        Nom du joueur.
    current_room : Room or None
        Salle dans laquelle se trouve actuellement le joueur.
        None tant que le joueur n'a pas été placé dans une salle.

    Methods
    -------
    move(direction) -> bool
        Déplace le joueur dans la direction spécifiée, si une sortie existe.
        Retourne True si le déplacement a réussi, False sinon.
    """

    # Define the constructor.
    def __init__(self, name):
        self.name = name
        self.current_room = None
    
    # Define the move method.
    def move(self, direction):
        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.exits[direction]

        # If the next room is None, print an error message and return False.
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        
        # Set the current room to the next room.
        self.current_room = next_room
        print(self.current_room.get_long_description())
        return True

    