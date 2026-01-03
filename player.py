# player.py
from room import Room
from item import Item
from quest import QuestManager


class Player:
    """
    Classe représentant le joueur :
    - déplacements
    - inventaire
    - quêtes
    - combat / stats
    - équipement
    - XP / niveaux
    """

    def __init__(self, name: str):
        self.name = name
        self.current_room = None
        self.history = []

        # ===== INVENTAIRE =====
        self.inventory = {}          # {nom_item: Item}
        self.max_weight = 5

        # ===== QUÊTES =====
        self.move_count = 0
        self.quest_manager = QuestManager(self)
        self.rewards = []

        # ===== ÉCONOMIE =====
        self.gold = 5

        # ===== STATS DE BASE =====
        self.level = 1
        self.base_attack = 10
        self.base_magic = 0
        self.base_armor = 0
        self.base_hp = 10000

        # ===== XP =====
        self.xp = 0
        self.xp_to_next = 50

        # ===== STATS ACTUELLES =====
        self.attack = self.base_attack
        self.magic = self.base_magic
        self.armor = self.base_armor
        self.max_hp = self.base_hp
        self.hp = self.max_hp

        # ===== ÉQUIPEMENT =====
        self.equipped_helmet = None
        self.equipped_armor = None
        self.equipped_other = None
        self.equipped_shield = None
        self.equipped_weapon = None
        self.equipped_magic = None

    # =========================================================
    # DÉPLACEMENTS
    # =========================================================

    def move(self, direction):
        normalized = Room.normalize_direction(direction)

        if normalized is None or normalized not in Room.VALID_DIRECTIONS:
            print(f"\nDirection '{direction}' non reconnue.\n")
            return False

        next_room = self.current_room.get_exit(normalized)
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False

        self.history.append(self.current_room)
        self.current_room = next_room
        print(self.current_room.get_long_description())

        # Quêtes
        self.quest_manager.check_room_objectives(self.current_room.name)
        self.move_count += 1
        self.quest_manager.check_counter_objectives("Se déplacer", self.move_count)

        return True

    def back(self):
        if not self.history:
            print("\nImpossible de revenir en arrière.\n")
            return False

        self.current_room = self.history.pop()
        print(self.current_room.get_long_description())
        return True

    def get_history(self):
        if not self.history:
            return "\nVous n'avez encore visité aucune autre pièce.\n"

        s = "\nVous avez déjà visité :\n"
        for room in self.history:
            s += f"  - {room.description}\n"
        return s

    # =========================================================
    # INVENTAIRE
    # =========================================================

    def get_current_weight(self):
        return sum(item.weight for item in self.inventory.values())

    def get_inventory(self):
        if not self.inventory:
            return "\nVotre inventaire est vide.\n"

        s = "\nInventaire:\n"
        for item in self.inventory.values():
            s += f"  - {item}\n"
        return s

    def add_item(self, item: Item):
        if self.get_current_weight() + item.weight > self.max_weight:
            print("\nVous portez trop de choses.\n")
            return False

        self.inventory[item.name] = item
        print(f"\nVous obtenez {item.name}.\n")
        return True

    def remove_item(self, item_name: str):
        return self.inventory.pop(item_name, None)

    def has_item(self, item_name: str) -> bool:
        return item_name in self.inventory

    # =========================================================
    # ÉQUIPEMENT & STATS
    # =========================================================

    def recalc_stats(self):
        atk = self.base_attack
        mag = self.base_magic
        arm = self.base_armor
        hp_bonus = 0

        for it in [
            self.equipped_helmet,
            self.equipped_armor,
            self.equipped_other,
            self.equipped_shield,
            self.equipped_weapon,
            self.equipped_magic,
        ]:
            if it:
                atk += it.attack
                mag += it.magic
                arm += it.armor
                hp_bonus += it.hp

        self.attack = atk
        self.magic = mag
        self.armor = arm
        self.max_hp = self.base_hp + hp_bonus
        self.hp = min(self.hp, self.max_hp)

    def equip_item(self, item: Item):
        if item.name not in self.inventory:
            print("\nObjet absent de l'inventaire.\n")
            return False

        slot_map = {
            "helmet": "equipped_helmet",
            "armor": "equipped_armor",
            "other": "equipped_other",
            "shield": "equipped_shield",
            "weapon": "equipped_weapon",
            "magic": "equipped_magic",
        }

        slot = slot_map.get(item.item_type)
        if slot is None:
            print("\nObjet non équipable.\n")
            return False

        current = getattr(self, slot)
        setattr(self, slot, None if current is item else item)
        self.recalc_stats()
        return True

    # =========================================================
    # COMBAT / XP
    # =========================================================

    def get_attack(self):
        """Compatibilité avec actions.py"""
        return self.attack

    def display_health_bar(self, length=20):
        """Retourne une barre de vie sous forme de chaîne."""
        ratio = self.hp / self.max_hp
        filled = int(ratio * length)
        empty = length - filled
        bar = "█" * filled + "░" * empty
        return f"{self.name} : [{bar}] {self.hp}/{self.max_hp} PV"
        


    
    
    def take_damage(self, dmg: int, dmg_type: str = "physical") -> int:
        """
        Applique des dégâts au personnage en tenant compte :
        - du type de dégâts
        - des faiblesses / résistances
        - de l'armure
        -  se stop a 0 PV
        """

        # --- Modificateurs élémentaires ---
        real_dmg = dmg

        if hasattr(self, "weak_to") and dmg_type in self.weak_to:
            real_dmg = int(real_dmg * 1.4)

        if hasattr(self, "resist_to") and dmg_type in self.resist_to:
            real_dmg = int(real_dmg * 0.8)

        # --- Armure ---
        if dmg_type == "physical":
            armor = getattr(self, "armor_phys", 0)
        elif dmg_type == "magic":
            armor = getattr(self, "armor_mag", 0)
        else:
            armor = 0

        real_dmg = max(0, real_dmg - armor)

        # --- Application des dégâts ---
        self.hp -= real_dmg
        self.hp = max(0, self.hp)  # 🔒 Verrou absolu

        # --- Affichage ---
        print(f"\n💥 {self.name} subit {real_dmg} dégâts !")
        print(self.display_health_bar())

        if self.hp == 0:
            print("\n💀 Vous êtes mort.\n")

        return real_dmg

    def xp_required_for_level(self, level: int) -> int:
        return 50 * level

    def gain_xp(self, amount: int):
        self.xp += amount
        print(f"\n+{amount} XP\n")

        while self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            self.level_up()

    def level_up(self):
        self.level += 1
        self.base_hp += 20 
        self.base_attack += 5
        self.base_magic += 2
        self.base_armor += 1

        self.xp_to_next = self.xp_required_for_level(self.level)
        self.recalc_stats()
        self.hp = self.max_hp

        print(
            f"\n=== LEVEL UP ===\n"
            f"Niveau {self.level}\n"
            f"ATK +5 | MAG +2 | ARM +1 | PV +20\n"
        )

    # =========================================================
    # OR & RÉCOMPENSES
    # =========================================================

    def add_gold(self, amount: int):
        self.gold += amount

    def can_afford(self, price: int) -> bool:
        return self.gold >= price

    def spend_gold(self, price: int) -> bool:
        if self.gold >= price:
            self.gold -= price
            return True
        return False

    def add_reward(self, reward):
        if reward and reward not in self.rewards:
            self.rewards.append(reward)
            print(f"\n🎁 Vous avez obtenu : {reward}\n")

    def show_rewards(self):
        if not self.rewards:
            print("\n🎁 Aucune récompense.\n")
        else:
            print("\n🎁 Récompenses :")
            for r in self.rewards:
                print(f"  • {r}")
            print()
