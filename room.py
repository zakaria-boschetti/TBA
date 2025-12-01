# Define the Room class.

class Room:

    """
    Classe Room :
    Représente un lieu du jeu d'aventure. Un lieu possède un nom, une
    description et un ensemble de sorties permettant de rejoindre
    d'autres lieux.

    Attributs :
    name : str
        Le nom du lieu.
    description : str
        La description textuelle du lieu, affichée au joueur.
    exits : dict[str, Room]
        Un dictionnaire associant une direction (str) à un objet Room
        correspondant à la sortie dans cette direction.

    Méthodes :
    init(name, description)
        Constructeur, initialise le nom, la description et les sorties.
    get_exit(direction) -> Room | None
        Retourne le lieu dans la direction donnée, ou None si invalide.
    get_exit_string() -> str
        Retourne une chaîne décrivant toutes les sorties disponibles.
    get_long_description() -> str
        Retourne une description longue du lieu incluant ses sorties.

    Exceptions :
    Aucune.
    """







    # Define the constructor. 
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
    
    # Define the get_exit method.
    def get_exit(self, direction):

        # Return the room in the given direction if it exists.
        if direction in self.exits.keys():
            return self.exits[direction]
        else:
            return None
    
    # Return a string describing the room's exits.
    def get_exit_string(self):
        exit_string = "Sorties: " 
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    # Return a long description of this room including exits.
    def get_long_description(self):
        return f"\nVous êtes {self.description}\n\n{self.get_exit_string()}\n"
