# Description: Character class (PNJ)

from room import Room
import random

class Character:
    """
    Représente un personnage non joueur (PNJ).

    Attributs :
        name : str
            Nom du personnage.
        description : str
            Description du personnage.
        current_room : Room
            Salle où se trouve actuellement le PNJ.
        msgs : list[str]
            Liste de messages affichés quand on lui parle.
    """

    def __init__(self, name, description, current_room, msgs):
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = list(msgs) if msgs is not None else []

    def __str__(self):
        """
        Représentation textuelle du PNJ.

        Exemple :
        Gandalf : un magicien blanc
        """
        return f"{self.name} : {self.description}"

    def move(self):
        """
        Déplace éventuellement le PNJ.

        - Une chance sur deux de se déplacer.
        - S'il se déplace, il va dans une pièce adjacente au hasard.
        - Retourne True s'il a bougé, False sinon.
        """
        # 1 chance sur 2 de bouger
        if not random.choice([True, False]):
            return False

        # Liste des pièces accessibles (exits non None)
        possible_rooms = [room for room in self.current_room.exits.values()
                          if room is not None]
        if not possible_rooms:
            return False

        new_room = random.choice(possible_rooms)

        # Retirer le PNJ de l'ancienne salle
        old_room = self.current_room
        key = self.name.lower()
        if key in old_room.characters:
            del old_room.characters[key]

        # Mettre à jour la salle actuelle
        self.current_room = new_room

        # Ajouter le PNJ dans la nouvelle salle
        new_room.characters[key] = self

        return True

    def get_msg(self):
        """
        Retourne un message du PNJ, en les faisant tourner cycliquement.

        Si msgs = ["Je suis Gandalf", "Abracadabra !"], alors les appels
        successifs renverront :
        - "Je suis Gandalf"
        - "Abracadabra !"
        - "Je suis Gandalf"
        - ...
        """
        if not self.msgs:
            return f"{self.name} n'a rien à dire."

        msg = self.msgs.pop(0)
        self.msgs.append(msg)
        return msg
