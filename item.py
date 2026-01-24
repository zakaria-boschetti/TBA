# item.py

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
            Type : "weapon", "armor", "helmet", "shield", "other", "magic",
                   "potion", "munition", "artefact", "quest", etc.
        quantity : int
            Quantité (pour potions et munitions).

        damage : int
            Dégâts (pour les armes).
        durability : int
            Durabilité (pour les armes).

        armor_phys : int
            Armure physique (équipements).
        armor_mag : int
            Armure magique (équipements).

        bonus : dict
            Bonus divers (artefacts / effets spéciaux).
        heal : int
            Soin (consommables).
        mana : int
            Mana (consommables).

    Notes de compatibilité :
        - Le code accepte les clés FR/EN dans kwargs : dégâts/damage, durabilité/durability,
          armure_phys/armor_phys, armure_mag/armor_mag, quantité/quantity, type/item_type, etc.
        - Des propriétés attack/armor/magic/hp sont exposées pour compatibilité future
          avec l'interface graphique, sans casser ton modèle actuel.
    """

    ARMES = {}
    UTILISABLES = {}
    EQUIPEMENT = {}
    ARTEFACTS = {}
    MONSTER_ITEMS = {}

    _KEY_MAP = {
        "type": "type",
        "item_type": "type",

        "description": "description",
        "desc": "description",

        "weight": "weight",
        "poids": "weight",

        "quantity": "quantity",
        "quantite": "quantity",
        "quantité": "quantity",

        "damage": "damage",
        "degats": "damage",
        "dégâts": "damage",

        "durability": "durability",
        "durabilite": "durability",
        "durabilité": "durability",

        "crit_chance": "crit_chance",
        "chance_crit": "crit_chance",

        "armor_phys": "armor_phys",
        "armure_phys": "armor_phys",

        "armor_mag": "armor_mag",
        "armure_mag": "armor_mag",

        "bonus": "bonus",
        "heal": "heal",
        "soin": "heal",
        "mana": "mana",
        "magie": "mana",

        "attack": "attack",
        "attaque": "attack",
        "armor": "armor",
        "armure": "armor",
        "magic": "magic",
        "hp": "hp",
        "pv": "hp",
    }

    _EQUIPMENT_TYPES = {
        "weapon", "armor", "helmet", "shield", "other", "magic", "equipment",
        "arme", "équipement", "equipement",
    }

    def __init__(self, name, description, weight=0.0, display_name=None, item_type=None, quantity=1, **kwargs):
        self.name = name 
        self.stats = {}   
                      
        self.display_name = display_name or name  # nom affiché
        self.description = description
        self.weight = weight
    

        for cat in [Item.ARMES, Item.UTILISABLES, Item.EQUIPEMENT, Item.ARTEFACTS, Item.MONSTER_ITEMS]:
            if name in cat:
                self.stats.update(cat[name])

        normalized_kwargs = {}
        for k, v in kwargs.items():
            key = Item._KEY_MAP.get(k, k)
            normalized_kwargs[key] = v

        self.stats.update(normalized_kwargs)

        self.description = self.stats.get("description", description)
        self.item_type = self.stats.get("type", item_type)
        self.quantity = self.stats.get("quantity", quantity)

        # Règle demandée : tous les équipements = 1 kg
        if self.item_type in Item._EQUIPMENT_TYPES:
            self.weight = 1
        else:
            if "weight" in self.stats:
                self.weight = self.stats["weight"]
            else:
                self.weight = weight

        self.damage = int(self.stats.get("damage", 0) or 0)
        self.durability = int(self.stats.get("durability", 0) or 0)
        self.crit_chance = float(self.stats.get("crit_chance", 0) or 0)

        self.armor_phys = int(self.stats.get("armor_phys", 0) or 0)
        self.armor_mag = int(self.stats.get("armor_mag", 0) or 0)

        self.bonus = self.stats.get("bonus", {})
        if self.bonus is None:
            self.bonus = {}

        self.heal = int(self.stats.get("heal", 0) or 0)
        self.mana = int(self.stats.get("mana", 0) or 0)

        self._attack = int(self.stats.get("attack", 0) or 0)
        self._armor = int(self.stats.get("armor", 0) or 0)
        self._magic = int(self.stats.get("magic", 0) or 0)
        self._hp = int(self.stats.get("hp", 0) or 0)

    @property
    def attack(self):
        if self._attack:
            return self._attack
        return self.damage

    @property
    def armor(self):
        if self._armor:
            return self._armor
        return self.armor_phys

    @property
    def magic(self):
        return self._magic

    @property
    def hp(self):
        return self._hp

    def __str__(self):
        qte_str = f" x{self.quantity}" if self.item_type in ["potion", "munition"] and self.quantity > 1 else ""
        return f"{self.display_name}{qte_str} : {self.description} ({self.weight} kg)"