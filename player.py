# Define the Player class.
from room import Room
from item import Item
from quest import QuestManager

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
        self.history = []
        # Inventaire du joueur
        self.inventory = {}
        # Poids maximal transportable
        self.max_weight = 5
        
        self.move_count = 0
        self.quest_manager = QuestManager(self)
        self.rewards = []
    
    # Define the move method.
    def move(self, direction):
        """
        Tente de déplacer le joueur dans la direction donnée.

        - Si la direction n'est pas reconnue (ex: 'H') :
              → "Direction 'H' non reconnue."
        - Si la direction est valide mais qu'il n'y a pas de sortie dans cette direction :
              → "Aucune porte dans cette direction !"
        - Sinon :
              → on ajoute la salle actuelle à l'historique,
                 on change de salle, on affiche la nouvelle description
                 et l'historique.
        """

        # Normaliser la direction
        normalized = Room.normalize_direction(direction)

        # Si la direction n'est pas reconnue par notre table
        if normalized is None or normalized not in Room.VALID_DIRECTIONS:
            print(f"\nDirection '{direction}' non reconnue.\n")
            return False

        # On utilise get_exit de Room qui travaille avec la direction normalisée
        next_room = self.current_room.get_exit(normalized)

        # If the next room is None, print an error message and return False.
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        
        self.history.append(self.current_room)
        
        # Set the current room to the next room.
        self.current_room = next_room
        print(self.current_room.get_long_description())
        
        # Check room visit objectives
        self.quest_manager.check_room_objectives(self.current_room.name)

        # Increment move counter and check movement objectives
        self.move_count += 1
        self.quest_manager.check_counter_objectives("Se déplacer", self.move_count)

        return True
    
    def back(self):
        """
        Revient en arrière si possible, en utilisant l'historique.

        - Si l'historique est vide : impossible de revenir en arrière.
        - Sinon : dépile la dernière pièce visitée, s'y déplace,
                  affiche la description et l'historique.
        """
        if not self.history:
            print("\nImpossible de revenir en arrière : aucun déplacement précédent.\n")
            return False

        previous_room = self.history.pop()
        self.current_room = previous_room
        print(self.current_room.get_long_description())
        return True

    def get_history(self):
        """
        Construit une chaîne de caractères représentant l'historique des pièces
        visitées (sans la pièce actuelle).
        """
        if not self.history:
            return "\nVous n'avez encore visité aucune autre pièce.\n"

        s = "\nVous avez déja visité les pièces suivantes:\n"
        for room in self.history:
            s += f"    - {room.description}\n"
        return s

    def get_current_weight(self):
        """
        Calcule le poids total des objets dans l'inventaire.
        """
        return sum(item.weight for item in self.inventory.values())
    
    def get_inventory(self):
        """
        Retourne une chaîne représentant l'inventaire du joueur.

        - Si l'inventaire est vide :
              "Votre inventaire est vide."
        - Sinon :
              "Vous disposez des items suivants :"
                 - nom : description (x kg)
        """
        if not self.inventory:
            return "\nVotre inventaire est vide.\n"

        s = "\nVous disposez des items suivants:\n"
        for item in self.inventory.values():
            s += f"    - {item}\n"
        return s
    
    def add_reward(self, reward):
        """
        Add a reward to the player's rewards list.
        
        Args:
            reward (str): The reward to add.
            
        Examples:
        
        >>> player = Player("Bob")
        >>> player.add_reward("Épée magique") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vous avez obtenu: Épée magique
        <BLANKLINE>
        >>> "Épée magique" in player.rewards
        True
        >>> player.add_reward("Épée magique") # Adding same reward again
        >>> len(player.rewards)
        1
        """
        if reward and reward not in self.rewards:
            self.rewards.append(reward)
            print(f"\n🎁 Vous avez obtenu: {reward}\n")


    def show_rewards(self):
        """
        Display all rewards earned by the player.
        
        Examples:
        
        >>> player = Player("Charlie")
        >>> player.show_rewards() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Aucune récompense obtenue pour le moment.
        <BLANKLINE>
        >>> player.add_reward("Bouclier d'or") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vous avez obtenu: Bouclier d'or
        <BLANKLINE>
        >>> player.show_rewards() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vos récompenses:
        • Bouclier d'or
        <BLANKLINE>
        """
        if not self.rewards:
            print("\n🎁 Aucune récompense obtenue pour le moment.\n")
        else:
            print("\n🎁 Vos récompenses:")
            for reward in self.rewards:
                print(f"  • {reward}")
            print()
    