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

    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.history = []

        # Référence vers Game (injectée dans Game.setup)
        self.game = None

        # ===== INVENTAIRE =====
        self.inventory = {}          # {nom_item: Item}
        self.max_weight = 16

        # ===== QUÊTES =====
        self.move_count = 0
        self.quest_manager = QuestManager(self)
        self.rewards = []

        # ===== ÉCONOMIE =====
        self.gold = 1000

        # ===== STATS DE BASE =====
        self.level = 1
        self.base_attack = 10
        self.base_magic = 0
        self.base_armor = 0
        self.base_hp = 1000

        # ===== XP =====
        self.xp = 0
        self.xp_to_next = self.xp_required_for_level(self.level)

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

        # ===== RESSOURCES (mana) =====
        # rétro-compatible : si tu n'utilises pas le mana ailleurs, ça n'empêche rien
        self.base_mana = 30
        self.max_mana = self.base_mana
        self.mana = self.max_mana

        # ===== BUFFS TEMPORAIRES (consommables) =====
        # ex: potion_force => +atk pendant X tours
        # structure : {"attack": {"amount": 5, "turns": 3}, ...}
        self._temp_buffs = {}


    # =========================================================
    # DÉPLACEMENTS
    # =========================================================

    def move(self, direction):
        normalized = Room.normalize_direction(direction)
        if normalized is None:
            print("\nDirection non reconnue.\n")
            return False

        next_room = self.current_room.get_exit(normalized)
        if next_room is None:
            print("\nAucune sortie dans cette direction.\n")
            return False

        self.history.append(self.current_room)
        self.current_room = next_room
        self.move_count += 1

        print(self.current_room.get_long_description())

        if self.quest_manager is not None:
            self.quest_manager.check_action_objectives("aller", self.current_room.name)

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
            s += f"  - {room.name}\n"
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
            q = int(getattr(item, "quantity", 1) or 1)
            s += f"  - {item.name} x{q}\n"
        s += f"\nPoids: {self.get_current_weight()} / {self.max_weight} kg\n"
        return s


        s = "\nInventaire:\n"
        for item in self.inventory.values():
            q = int(getattr(item, "quantity", 1) or 1)
            s += f"  - {item.name} x{q}\n"
        s += f"\nPoids: {self.get_current_weight()} / {self.max_weight} kg\n"
        return s

    def add_item(self, item):
        if self.get_current_weight() + item.weight > self.max_weight:
            print("\nVous portez trop de choses.\n")
            return False

        # quantité par défaut
        q_add = int(getattr(item, "quantity", 1) or 1)

        # ✅ STACK
        if item.name in self.inventory:
            existing = self.inventory[item.name]
            existing.quantity = int(getattr(existing, "quantity", 1) or 1) + q_add
            print(f"\nVous obtenez {item.name} x{q_add} (total: x{existing.quantity}).\n")
        else:
            item.quantity = q_add
            self.inventory[item.name] = item
            print(f"\nVous obtenez {item.name} x{item.quantity}.\n")

        if hasattr(self, "quest_manager") and self.quest_manager is not None:
            self.quest_manager.check_action_objectives("obtenir", item.name)

        return True



    def remove_item(self, item_name, qty=1):
        item = self.inventory.get(item_name)
        if item is None:
            return None

        qty = int(qty or 1)
        current_q = int(getattr(item, "quantity", 1) or 1)

        if current_q > qty:
            item.quantity = current_q - qty
            return item
        else:
            return self.inventory.pop(item_name, None)



    def has_item(self, item_name):
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
                # Buffs temporaires (consommables)
                atk += int(self._temp_buffs.get("attack", {}).get("amount", 0) or 0)
                arm += int(self._temp_buffs.get("armor", {}).get("amount", 0) or 0)
                mag += int(self._temp_buffs.get("magic", {}).get("amount", 0) or 0)


        self.attack = atk
        self.magic = mag
        self.armor = arm
        self.max_hp = self.base_hp + hp_bonus
        self.hp = min(self.hp, self.max_hp)
        # Mana : même logique que HP
        self.max_mana = max(0, int(getattr(self, "base_mana", 0) or 0))
        self.mana = min(int(getattr(self, "mana", self.max_mana) or 0), self.max_mana)


    def equip_item(self, item):
        if item is None or not isinstance(item, Item):
            return False

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
        if current is item:
            setattr(self, slot, None)
        else:
            setattr(self, slot, item)

        self.recalc_stats()
        return True
    
    def unequip_slot(self, slot_name: str):
        slot_map = {
            "helmet": "equipped_helmet",
            "armor": "equipped_armor",
            "other": "equipped_other",
            "shield": "equipped_shield",
            "weapon": "equipped_weapon",
            "magic": "equipped_magic",
        }

        attr = slot_map.get(slot_name)
        if not attr:
            return False

        setattr(self, attr, None)
        self.recalc_stats()
        return True


    # =========================================================
    # COMBAT / XP
    # =========================================================

    def get_attack(self):
        return self.attack
    
    def get_attack_value(self):
        """Retourne l'attaque effective (attaque + buffs temporaires)."""
        bonus = 0
        b = self._temp_buffs.get("attack")
        if b and b.get("turns", 0) > 0:
            bonus += int(b.get("amount", 0) or 0)
        return int(self.attack) + bonus

    def get_armor_value(self):
        """Retourne l'armure effective (armure + buffs temporaires)."""
        bonus = 0
        b = self._temp_buffs.get("armor")
        if b and b.get("turns", 0) > 0:
            bonus += int(b.get("amount", 0) or 0)
        return int(getattr(self, "armor", 0) or 0) + bonus

    def apply_temp_buff(self, stat: str, amount: int, turns: int = 3):
        """Applique (ou prolonge) un buff temporaire."""
        stat = str(stat).lower().strip()
        if turns <= 0 or amount == 0:
            return

        cur = self._temp_buffs.get(stat)
        if cur and cur.get("turns", 0) > 0:
            cur["amount"] = max(int(cur.get("amount", 0) or 0), int(amount))
            cur["turns"] = max(int(cur.get("turns", 0) or 0), int(turns))
        else:
            self._temp_buffs[stat] = {"amount": int(amount), "turns": int(turns)}

    def tick_buffs(self, n: int = 1):
        """Décrémente la durée des buffs (à appeler à la fin d'un tour)."""
        n = max(0, int(n))
        if n == 0:
            return
        to_del = []
        for k, v in self._temp_buffs.items():
            v["turns"] = int(v.get("turns", 0) or 0) - n
            if v["turns"] <= 0:
                to_del.append(k)
        for k in to_del:
            self._temp_buffs.pop(k, None)

    def is_consumable(self, item) -> bool:
        if item is None:
            return False
        t = getattr(item, "item_type", getattr(item, "type", ""))
        if str(t).lower() == "potion":
            return True
        for key in ("heal", "mana", "boost_attack", "boost_defense", "boost_agility"):
            if getattr(item, key, 0):
                return True
        st = getattr(item, "stats", {}) or {}
        for key in ("boost_attack", "boost_defense", "boost_agility"):
            if st.get(key):
                return True
        return False

    def consume_item(self, item_name: str, turns_for_buffs: int = 3):
        """Consomme un objet de l'inventaire.
        Retour: dict (changed, message, removed)
        """
        if not item_name:
            return {"changed": False, "message": "Aucun objet."}

        item = self.inventory.get(item_name)
        if item is None:
            return {"changed": False, "message": f"Objet '{item_name}' absent de l'inventaire."}

        if not self.is_consumable(item):
            return {"changed": False, "message": f"{item_name} n'est pas consommable."}

        stats = getattr(item, "stats", {}) or {}
        healed = int(stats.get("heal", getattr(item, "heal", 0)) or 0)
        mana_gain = int(stats.get("mana", 0) or 0)

        stats = getattr(item, "stats", {}) or {}
        boost_atk = int(stats.get("boost_attack", getattr(item, "boost_attack", 0)) or 0)
        boost_def = int(stats.get("boost_defense", getattr(item, "boost_defense", 0)) or 0)
        boost_agi = int(stats.get("boost_agility", getattr(item, "boost_agility", 0)) or 0)

        parts = []

        if healed > 0:
            before = int(self.hp)
            self.hp = min(int(self.max_hp), int(self.hp) + healed)
            parts.append(f"+{self.hp - before} PV")

        if mana_gain > 0:
            before = int(getattr(self, "mana", 0) or 0)
            self.mana = min(int(getattr(self, "max_mana", 0) or 0), before + mana_gain)
            parts.append(f"+{self.mana - before} Mana")

        if boost_atk:
            self.apply_temp_buff("attack", boost_atk, turns=turns_for_buffs)
            parts.append(f"ATK +{boost_atk} ({turns_for_buffs} tours)")

        if boost_def:
            self.apply_temp_buff("armor", boost_def, turns=turns_for_buffs)
            parts.append(f"ARM +{boost_def} ({turns_for_buffs} tours)")

        if boost_agi:
            self.apply_temp_buff("agility", boost_agi, turns=turns_for_buffs)
            parts.append(f"AGI +{boost_agi} ({turns_for_buffs} tours)")

        # retire l'objet (consommé)
        self.inventory.pop(item_name, None)

        msg = f"✅ Tu consommes {getattr(item, 'display_name', item_name)}"
        msg += (" : " + ", ".join(parts)) if parts else "."
        return {"changed": True, "message": msg, "removed": item_name, "item": item}
    


    def display_health_bar(self, length=20):
        if self.max_hp <= 0:
            return f"{self.name} : [....................] 0/0 PV"
        ratio = self.hp / self.max_hp
        filled = int(ratio * length)
        empty = length - filled
        bar = "█" * filled + "░" * empty
        return f"{self.name} : [{bar}] {self.hp}/{self.max_hp} PV"

    def take_damage(self, dmg, dmg_type="physical"):
            """
            Réduction d'armure "diminishing returns":
            - armor = 0  => 100% des dégâts
            - armor = 50 => ~66% des dégâts
            - armor = 100 => 50% des dégâts
            """
            dmg = int(dmg)
            if callable(getattr(self, "get_armor_value", None)):
                arm = max(0, int(self.get_armor_value() or 0))
            else:
                arm = max(0, int(getattr(self, "armor", 0) or 0))

            if dmg <= 0:
                return 0

            # réduction progressive
            real = int(round(dmg * (100 / (100 + arm))))

            # minimum 1 dégât si une attaque touche
            real = max(1, real)

            self.hp -= real
            if self.hp < 0:
                self.hp = 0
            return real


    def xp_required_for_level(self, level):
        base = 50
        growth = 1.4
        return int(round(base * (growth ** (level - 1))))

    def gain_xp(self, amount):
        self.xp += amount
        print(f"\n Vous gagnez {amount} XP.")

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
            "\n=== LEVEL UP ===\n"
            f"Niveau {self.level}\n"
            "ATK +5 | MAG +2 | ARM +1 | PV +20\n"
        )

    # =========================================================
    # OR & RÉCOMPENSES
    # =========================================================

    def add_gold(self, amount):
        self.gold += amount

    def can_afford(self, price):
        return self.gold >= price

    def spend_gold(self, price):
        if self.gold >= price:
            self.gold -= price
            return True
        return False

    def add_reward(self, reward):
        """
        Reward de quête => devient un ITEM dans l'inventaire.
        - reward peut être une string ("potion_soin") ou un Item.
        """
        # 1) Si c'est déjà un Item
        if hasattr(reward, "name"):
            try:
                return self.add_item(reward)
            except Exception:
                # fallback : garde trace si inventaire plein
                self.rewards.append(getattr(reward, "name", str(reward)))
                return False

        # 2) Si c'est une string : on essaie de récupérer l'Item depuis game (self.game.potion_soin, etc.)
        item_obj = None
        g = getattr(self, "game", None)
        if g is not None:
            item_obj = getattr(g, str(reward), None)

        # 3) Si on a un Item connu du jeu, on en fabrique un exemplaire “neuf”
        if item_obj is not None and hasattr(item_obj, "name"):
            try:
                from item import Item
                cloned = Item(
                    item_obj.name,
                    getattr(item_obj, "description", ""),
                    getattr(item_obj, "weight", 0.0),
                    item_type=getattr(item_obj, "item_type", None),
                    quantity=getattr(item_obj, "quantity", 1),
                    **getattr(item_obj, "stats", {}),
                )
                return self.add_item(cloned)
            except Exception:
                # si clone échoue, on tente d'ajouter l'objet tel quel
                try:
                    return self.add_item(item_obj)
                except Exception:
                    self.rewards.append(str(reward))
                    return False

        # 4) Sinon : on crée un item “quest” générique
        try:
            from item import Item
            created = Item(str(reward), "Récompense de quête.", 0.1, item_type="quest")
            return self.add_item(created)
        except Exception:
            self.rewards.append(str(reward))
            return False


    def show_rewards(self):
        if not self.rewards:
            print("\nAucune récompense.\n")
        else:
            print("\nRécompenses :")
            for r in self.rewards:
                print(f"  - {r}")
            print()

