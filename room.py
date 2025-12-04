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

    # Ensemble des directions valides (rempli automatiquement depuis la map)
    VALID_DIRECTIONS = set()

    # Dictionnaire pour normaliser les directions saisies par le joueur
    # vers une forme canonique (N, S, E, O, "haut", "bas", etc.)
    DIRECTION_MAP = {
        "n": "N",
        "nord": "N",

        "s": "S",
        "sud": "S",

        "e": "E",
        "est": "E",

        "o": "O",
        "ouest": "O",

        "u": "haut",
        "up": "haut",
        "haut": "haut",
        "monter": "haut",

        "d": "bas",
        "down": "bas",
        "bas": "bas",
        "descendre": "bas",
    }

    # Define the constructor. 
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.inventory = {}
        self.characters = {}

    @staticmethod
    def normalize_direction(direction):
        """
        Prend une direction entrée par le joueur (ex: 'n', 'Nord', 'ouest', 'U')
        et la renvoie sous forme normalisée (ex: 'N', 'O', 'haut', 'bas').
        Retourne None si la direction n'est pas reconnue.
        """
        if not isinstance(direction, str):
            return None
        d = direction.strip().lower()
        return Room.DIRECTION_MAP.get(d, None)

    @classmethod
    def register_direction(cls, direction):
        """
        Enregistre une direction comme valide dans l'ensemble global
        des directions possibles.
        Appelée depuis la construction de la map (game.setup).
        """
        cls.VALID_DIRECTIONS.add(direction)

    # Define the get_exit method.
    def get_exit(self, direction):

        # Normaliser la direction avant de chercher dans le dictionnaire
        normalized = Room.normalize_direction(direction)
        if normalized is None:
            return None

        # Return the room in the given direction if it exists.
        if normalized in self.exits.keys():
            return self.exits[normalized]
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
    
    def get_inventory(self):
        """
        Retourne une chaîne décrivant ce que contient la pièce.

        - Si la pièce est vide :
              "Il n'y a rien ici."
        - Sinon :
              "La pièce contient :"
                 - nom : description (x kg)
        """
        if not self.inventory:
            return "\nIl n'y a rien ici.\n"

        s = "\nLa pièce contient :\n"
        for item in self.inventory.values():
            s += f"    - {item}\n"
        return s
