class Item:
    """
    Représente un objet manipulable par le joueur.

    Attributs :
        name : str
            Nom de l'objet.
        description : str
            Description de l'objet.
        weight : float
            Poids de l'objet en kg.
        item_type : str
            Type : "arme", "équipement", "potion", "munition", "artefact", etc.
        quantity : int
            Quantité (pour potions et munitions).
        damage : int
            Pour les armes.
        durability : int
            Pour les armes.
        armor_phys : int
            Pour les équipements.
        armor_mag : int
            Pour les équipements.
        bonus : dict
            Pour les artefacts (ex: {"crit_chance": 0.1})
    """

    # Catégories globales à définir ailleurs dans le code
    ARMES = {}
    UTILISABLES = {}
    EQUIPEMENT = {}
    ARTEFACTS = {}
    MONSTER_ITEMS = {}

    def __init__(self, name, description="", weight=0, item_type=None, quantity=1, **kwargs):
        self.name = name
        self.stats = {}

        # Chercher l'objet dans toutes les catégories
        for cat in [Item.ARMES, Item.UTILISABLES, Item.EQUIPEMENT, Item.ARTEFACTS, Item.MONSTER_ITEMS]:
            if name in cat:
                self.stats.update(cat[name])

        # Mettre à jour avec kwargs (pour permettre override ou ajout direct)
        self.stats.update(kwargs)

        # Définir les attributs principaux
        self.description = self.stats.get("description", description)
        self.weight = self.stats.get("weight", weight)
        self.item_type = self.stats.get("type", item_type)
        self.quantity = self.stats.get("quantity", quantity)

        # Armes
        self.damage = self.stats.get("damage", 0)
        self.durability = self.stats.get("durability", 0)

        # Équipement
        self.armor_phys = self.stats.get("armor_phys", 0)
        self.armor_mag = self.stats.get("armor_mag", 0)

        # Artefacts
        self.bonus = self.stats.get("bonus", {})

    def __str__(self):
        qte_str = f" x{self.quantity}" if self.item_type in ["potion", "munition"] and self.quantity > 1 else ""
        return f"{self.name}{qte_str} : {self.description} ({self.weight} kg)"


