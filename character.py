# Description: Character class (PNJ)

from room import Room
import random
from typing import List, Optional, Dict

def clamp(value, min_value, max_value):
    """Clamp la valeur entre min_value et max_value."""
    return max(min_value, min(value, max_value))

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

    def __init__(self, name, description, current_room, msgs,movable=True):
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = list(msgs) if msgs is not None else []
        self.movable = movable  # True si le PNJ peut se déplacer

    def __str__(self):
        """Représentation textuelle du PNJ."""
        return f"{self.name} : {self.description}"

    def move(self):
        """Déplace éventuellement le PNJ dans une salle adjacente."""
        if not self.movable:
            return False  # PNJ immobile

        # 50% de chance de bouger
        if not random.choice([True, False]):
            return False

        possible_rooms = [room for room in self.current_room.exits.values() if room is not None]
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
        new_room.characters[key] = self

        return True

    def get_msg(self):
        """Retourne un message du PNJ de manière cyclique."""
        if not self.msgs:
            return f"{self.name} n'a rien à dire."

        msg = self.msgs.pop(0)
        self.msgs.append(msg)
        return msg


# -------------------------
# Classe Monster (PNJ combat)
# -------------------------
class MonsterCharacter(Character):
    """Monstre avec stats, loot et IA."""

    def __init__(self, name, description, current_room, msgs,
                 hp, attack, attack_max, xp_reward=10,
                 defense=0, armor_mag=0, monster_type="Unknown",
                 weak_to=None, resist_to=None, speed=10, crit_chance=5.0,
                 loot=None, is_boss=False, patterns=None,movable=True):
        
        super().__init__(name, description, current_room, msgs)
        self.hp_max = hp
        self.hp = hp
        self.dmg_min = attack
        self.dmg_max = attack_max
        self.xp_reward = xp_reward
        self.armor_phys = defense
        self.armor_mag = armor_mag
        self.monster_type = monster_type
        self.weak_to = weak_to or []
        self.resist_to = resist_to or []
        self.speed = speed
        self.crit_chance = crit_chance
        self.loot = loot if loot else {}  # dictionnaire vide par défaut
        self.enraged = False
        self.buff_active = False
        self.is_monster = True
        self.is_boss = is_boss
        self.movable = movable  # True si le PNJ peut se déplacer
        # Boss / patterns
        self.patterns = []
        self.turn_counter = 0
        if patterns:
            for p in patterns:
                p_copy = p.copy()
                p_copy.setdefault("cooldown", 0)
                p_copy.setdefault("_cd_remaining", 0)
                self.patterns.append(p_copy)

    # -------------------------
    # Méthodes de combat
    # -------------------------
    def is_alive(self):
        return self.hp > 0

    def roll_damage(self):
        return random.randint(self.dmg_min, self.dmg_max)

    def attack_player(self, player):
        """
        Fait attaquer le monstre sur le joueur.

        Paramètres :
            player : objet joueur avec méthode take_damage(amount)
        
        Retour :
            dict contenant :
                - 'dmg': dégâts appliqués au joueur
                - 'is_crit': bool, indique si c'était un coup critique
        """
        # Calcul des dégâts de base
        dmg = self.roll_damage()

        # Vérification coup critique
        is_crit = random.random() * 100 <= self.crit_chance
        if is_crit:
            dmg = int(dmg * 1.7)

        # Application des bonus de rage ou buff
        if self.enraged:
            dmg = int(dmg * 1.3)
        if self.buff_active:
            dmg = int(dmg * 1.25)

        # Appliquer les dégâts au joueur si possible
        applied = player.take_damage(dmg) if hasattr(player, "take_damage") else dmg

        return {"dmg": applied, "is_crit": is_crit}

    def display_health_bar(self, length=20):
        """Retourne une barre de vie sous forme de chaîne."""
        ratio = self.hp / self.hp_max
        filled = int(ratio * length)
        empty = length - filled
        bar = "█" * filled + "░" * empty
        return f"{self.name} : [{bar}] {self.hp}/{self.hp_max} PV"
        

    
    
    def drop_loot(self):
        """
        Dépose les objets du monstre dans la salle actuelle.
        Appelée lorsque le monstre est vaincu.
        """
        if not self.loot:
            return

        room = self.current_room
        for item in self.loot:
            # Si l'objet existe déjà dans la salle, on pourrait cumuler ou ignorer
            # Ici on ajoute simplement
            room.inventory[item.name] = item

        # On vide le loot pour éviter les doublons
        self.loot = []

        print(f"\n{self.name} laisse tomber :")
        for item in room.inventory.values():
            print(f"  - {item.name} : {item.description}")





    def take_damage(self, amount: int, dmg_type="physical"):
        dmg = amount
        if dmg_type in self.weak_to:
            dmg = int(amount * 1.4)
        if dmg_type in self.resist_to:
            dmg = int(amount * 0.8)
        if dmg_type == "physical":
            dmg -= self.armor_phys
        elif dmg_type == "magic":
            dmg -= self.armor_mag
        dmg = clamp(int(dmg), 0, 999999)
        self.hp = clamp(self.hp - dmg, 0, self.hp_max)
        return dmg

    def decide_ai(self, player, context=None):
        context = context or {}
        # tentative de fuite si HP faible
        if self.hp <= int(self.hp_max * 0.2):
            flee_chance = 20 + max(0, 10 - self.speed)
            if random.randint(1, 100) <= flee_chance:
                return {"action": "flee"}
        if not self.enraged and self.hp <= int(self.hp_max * 0.35):
            if random.randint(1, 100) <= 40:
                self.enraged = True
                return {"action": "enrage"}
        if not self.buff_active and random.randint(1, 100) <= 10:
            self.buff_active = True
            return {"action": "buff"}
        return {"action": "attack"}

    def perform_action(self, player, context=None):
        dec = self.decide_ai(player, context)
        action = dec["action"]
        if action == "flee":
            return {"result": "fled", "message": f"{self.name} tente de fuir !"}
        if action == "enrage":
            return {"result": "enraged", "message": f"{self.name} entre en rage !"}
        if action == "buff":
            return {"result": "buffed", "message": f"{self.name} se renforce temporairement !"}
        # attaque
        atk = self.attack()
        dmg = atk["dmg"]
        crit = atk["is_crit"]
        applied = player.take_damage(dmg) if hasattr(player, "take_damage") else dmg
        return {
            "result": "attack",
            "dmg": applied,
            "is_crit": crit,
            "message": f"{self.name} attaque et inflige {applied} dégâts{' (crit)' if crit else ''}."
        }

    # -------------------------
    # Boss : choisir et exécuter un pattern
    # -------------------------
    def choose_pattern(self, context=None):
        if not self.patterns:
            return None
        context = context or {}
        candidates = [p for p in self.patterns
                      if p["_cd_remaining"] <= 0 and p.get("condition", lambda b,c: True)(self, context)]
        if not candidates:
            return self.patterns[0]
        return random.choice(candidates)

    def perform_pattern(self, player, context=None):
        context = context or {}
        self.turn_counter += 1
        for p in self.patterns:
            if p["_cd_remaining"] > 0:
                p["_cd_remaining"] -= 1
        pattern = self.choose_pattern(context)
        if not pattern:
            return {"result": "none", "message": f"{self.name} hésite..."}

        pattern["_cd_remaining"] = pattern.get("cooldown", 0)
        typ = pattern.get("type", "attack")
        dmg_mult = pattern.get("dmg_mult", 1.0)
        name = pattern.get("name", "Pattern")

        dmg_base = int(random.randint(self.dmg_min, self.dmg_max) * dmg_mult)
        is_crit = random.random() * 100 <= self.crit_chance
        if is_crit:
            dmg_base = int(dmg_base * 1.7)
        applied = player.take_damage(dmg_base) if hasattr(player, "take_damage") else dmg_base

        if typ in ("attack", "charge"):
            return {"result": "pattern_attack", "pattern": name, "dmg": applied, "is_crit": is_crit,
                    "message": f"{self.name} utilise {name} et inflige {applied} dégâts{' (crit)' if is_crit else ''}."}
        if typ == "aoe":
            return {"result": "pattern_aoe", "pattern": name, "dmg": applied, "is_crit": is_crit,
                    "message": f"{self.name} utilise {name} (AOE) et inflige {applied} dégâts{' (crit)' if is_crit else ''}."}
        if typ == "buff":
            self.buff_active = True
            return {"result": "pattern_buff", "pattern": name,
                    "message": f"{self.name} utilise {name} et se renforce."}
        return {"result": "none", "message": f"{self.name} hésite..."}
