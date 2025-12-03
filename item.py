# Description: Item class

class Item:
    """
    Représente un objet manipulable par le joueur.

    Attributs :
    name : str
        Nom de l'objet (clé utilisée pour le désigner).
    description : str
        Description textuelle de l'objet.
    weight : int | float
        Poids de l'objet (en kg).
    """

    def __init__(self, name, description, weight):
        self.name = name
        self.description = description
        self.weight = weight

    def __str__(self):
        """
        Retourne une représentation textuelle de l'objet.

        Exemple :
        sword : une épée au fil tranchant comme un rasoir (2 kg)
        """
        return f"{self.name} : {self.description} ({self.weight} kg)"
