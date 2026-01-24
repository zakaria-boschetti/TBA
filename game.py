# game.py
# Description: Game class

from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
from character import Character, MonsterCharacter
from quest import Quest

DEBUG = True


class Game:
    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.characters = []
        self.gui = None
        self.dialogues = {}
        

        # PNJ qui suit le joueur (ex: le marchand)
        self.following_npc = None

        # flag pour dire que le marchand a quitté le jeu DÉFINITIVEMENT
        self.marchand_removed = False

        # ✅ a-t-on sauvé le marchand des squelettes ?
        self.saved_merchant = False

        # la scène "bandits sur la route de la capitale" a-t-elle déjà été jouée ?
        self.route_bandits_done = False

        # le mage a-t-il déjà intervenu dans ce combat spécial ?
        self.mage_already_intervened = False


    # Setup the game
    def setup(self, player_name=None):
        self._setup_commands()
        self._setup_rooms()
        self._setup_items()
        self._setup_characters()
        self._setup_exits()
        self._register_directions()
        self._setup_player(player_name)
        self._setup_dialogues()
        self._setup_quests()


    def _setup_commands(self):
        self.commands["help"] = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["quit"] = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["go"] = Command(
            "go",
            " <direction> : se déplacer (N, S, E, O, haut, bas)",
            Actions.go,
            1,
        )
        self.commands["back"] = Command("back", " : revenir au lieu précédent", Actions.back, 0)
        self.commands["history"] = Command("history", " : afficher l'historique des lieux visités", Actions.history, 0)
        self.commands["look"] = Command("look", " : observer la pièce", Actions.look, 0)
        self.commands["take"] = Command("take", " <objet> : prendre un objet", Actions.take, 1)
        self.commands["drop"] = Command("drop", " <objet> : déposer un objet", Actions.drop, 1)
        self.commands["check"] = Command("check", " : afficher l'inventaire", Actions.check, 0)
        self.commands["talk"] = Command("talk", " <personnage> : parler à un personnage", Actions.talk, 1)
        self.commands["quests"] = Command("quests", " : afficher la liste des quêtes", Actions.quests, 0)
        self.commands["quest"] = Command("quest", " <titre> : afficher les détails d'une quête", Actions.quest, 1)
        self.commands["activate"] = Command("activate", " <titre> : activer une quête", Actions.activate, 1)
        self.commands["rewards"] = Command("rewards", " : afficher vos récompenses", Actions.rewards, 0)
        self.commands["fight"] = Command(
            "fight",
            " <monstre> : combattre un monstre dans la salle actuelle",
            Actions.fight,
            1,
        )
        self.commands["teleport"] = Command(
            "teleport",
            " <nom_salle> : téléporte le joueur vers une salle spécifiée",
            Actions.teleport,
            1,
        )
        self.commands["activateall"] = Command("activateall", " : activer toutes les quêtes", Actions.activateall, 0)


    def _setup_rooms(self):
        self.maison_haut = Room("maison_haut", "à l'étage de ta maison.")
        self.maison_bas = Room("maison_bas", "au rez-de-chaussée de ta maison.")
        self.village = Room("village", "sur la place du village.")
        self.magasin_village = Room("magasin_village", "dans le petit magasin du village.")
        self.magasin_echange_village = Room("magasin_echange_village", "la où tu peut échanger tes objets contre de l'argent")
        self.auberge = Room("auberge", "dans la salle commune de l'auberge.")
        self.maison_ancien = Room("maison_ancien", "dans la maison de l'ancien.")
        self.foret = Room("foret", "dans une forêt sombre et dense.")
        self.foret_sombre = Room("foret_sombre", "Une forêt sombre et inquiétante...")
        self.route_capitale = Room("route_capitale", "La route vers la capitale... dangereuse.")
        self.avant_post_capitale = Room("avant_post_capitale", "au poste avancé près de la capitale.")
        self.rue_capitale = Room("rue_capitale", "dans une rue animée de la capitale.")
        self.chateau = Room("chateau", "dans le grand château de la capitale.")
        self.foret_capitale = Room("foret_capitale", "dans une grande forêt sombre et dense.")
        self.guild = Room("guild", "dans la guilde des mages.")
        
        self.donjon = Room("donjon", "dans les sous-sols sombres.")
        


        #----------------------------------------- Donjon -----------------------------------------------------#
        # Niveau 1
        self.donjon_1 = Room("salle_donjon_1", "salle principale du niveau 1, l'entrée du donjon.")
        self.donjon_1_chambre = Room("salle_chambre_abandonnee", "Une petite chambre poussiéreuse.")
        self.donjon_1_tunnel = Room("salle_tunnel_etroit", "Un tunnel sombre menant à des coins inconnus.")
        self.salle_exploration = Room("salle_exploration", "Une salle avec quelques coffres vides.")

        # Niveau 2
        self.donjon_2 = Room("salle_donjon_2", "salle principale du niveau 2, escalier descendant.")
        self.donjon_2_salle_1 = Room("salle_caverne_humide", "Une caverne avec de l'eau stagnante.")
        self.donjon_2_salle_2 = Room("salle_galerie_sombre", "Galerie obscure, difficile à traverser.")
        self.donjon_2_salle_3 = Room("salle_aux_cristaux", "Des cristaux brillants illuminent la pièce.")

        
        # =========================
        # Donjon 3 – Salles
        # =========================
        self.d3_depart = Room("donjon3_depart", " Tu entres dans le labyrinthe.")
        self.d3_arrivee = Room("donjon3_arrivee", "Tu as trouvé la sortie du labyrinthe !")

        self.d3_s1  = Room("donjon3_s1",  "S1 — Un couloir principal.")
        self.d3_s2  = Room("donjon3_s2",  "S2 — Une salle froide.")
        self.d3_s3  = Room("donjon3_s3",  "S3 — Des marques au mur.")
        self.d3_s4  = Room("donjon3_s4",  "S4 — Une impasse sombre.")
        self.d3_s5  = Room("donjon3_s5",  "S5 — Un carrefour étroit.")
        self.d3_s6  = Room("donjon3_s6",  "S6 — L'air est humide.")
        self.d3_s7  = Room("donjon3_s7",  "S7 — Un passage sinueux.")
        self.d3_s8  = Room("donjon3_s8",  "S8 — Une salle silencieuse.")
        self.d3_s9  = Room("donjon3_s9",  "S9 — Une grande pièce vide.")
        self.d3_s10 = Room("donjon3_s10", "S10 — Un couloir vers l'est.")
        self.d3_s11 = Room("donjon3_s11", "S11 — Un tunnel bas.")
        self.d3_s12 = Room("donjon3_s12", "S12 — Des pierres effondrées.")
        self.d3_s13 = Room("donjon3_s13", "S13 — Un passage dangereux.")
        self.d3_s14 = Room("donjon3_s14", "S14 — Un recoin près de la sortie.")
        self.d3_s15 = Room("donjon3_s15", "S15 — Une salle isolée.")



        # Niveau 4
        self.donjon_4 = Room("salle_donjon_4", "salle principale du niveau 4, de la brume flotte dans l'air.")
        self.donjon_4_salle_1 = Room("salle_araignee", "Des toiles d'araignée partout.")
        self.donjon_4_salle_2 = Room("salle_puits", "Un puits profond rempli d'eau noire.")
        self.donjon_4_salle_3 = Room("salle_lanternes", "Quelques lanternes éclairent la pièce.")

        # Niveau 5
        self.donjon_5 = Room("salle_donjon_5", "salle principale du niveau 5, le sol est glissant.")
        self.donjon_5_salle_1 = Room("salle_feu", "Des torches illuminent cette salle.")
        self.donjon_5_salle_2 = Room("salle_chaines", "Des chaînes pendent du plafond.")
        self.donjon_5_salle_3 = Room("salle_pierres", "Des pierres anciennes jonchent le sol.")

        # Boss
        self.donjon_boss = Room("salle_boss", "Une immense salle où le boss ultime vous attend !")

        #-----------------------------------------FIN Donjon ------------------


        self.rooms = [
            self.maison_haut,
            self.maison_bas,
            self.village,
            self.magasin_village,
            self.magasin_echange_village,
            self.auberge,
            self.maison_ancien,
            self.foret,
            self.foret_sombre,
            self.route_capitale,
            self.avant_post_capitale,
            self.rue_capitale,
            self.foret_capitale,
            self.chateau,
            self.guild,
            self.donjon,
            # Donjon niveau 1
            self.donjon_1, self.donjon_1_chambre, self.donjon_1_tunnel, self.salle_exploration,

            # Donjon niveau 2
            self.donjon_2, self.donjon_2_salle_1, self.donjon_2_salle_2, self.donjon_2_salle_3,

            # Donjon niveau 3
            self.d3_depart, self.d3_arrivee, self.d3_s1, self.d3_s2, self.d3_s3, self.d3_s4,
            self.d3_s5, self.d3_s6, self.d3_s7, self.d3_s8, self.d3_s9, self.d3_s10, self.d3_s11,
            self.d3_s12, self.d3_s13, self.d3_s14, self.d3_s15,
            # Donjon niveau 4
            self.donjon_4, self.donjon_4_salle_1, self.donjon_4_salle_2, self.donjon_4_salle_3,

            # Donjon niveau 5
            self.donjon_5, self.donjon_5_salle_1, self.donjon_5_salle_2, self.donjon_5_salle_3,

            # Boss
            self.donjon_boss
        ]

    def _setup_items(self):


        # Weapons
        self.b_f_sword = Item(
            "b_f_sword",
            "Une énorme épée qui augmente fortement ta force.",
            3.0,
            display_name="B.F. Sword",
            type="weapon",
            damage=18, durability=35, niveau_requis=2, vendable=65
        )

        self.long_sword = Item(
            "long_sword",
            "Une épée longue bien équilibrée.",
            2.5,
            display_name="Long Sword",
            type="weapon",
            damage=12, durability=45, niveau_requis=1, vendable=35
        )

        self.caulfields_warhammer = Item(
            "caulfields_warhammer",
            "Un marteau lourd et brutal.",
            4.5,
            display_name="Caulfield's Warhammer",
            type="weapon",
            damage=16, durability=30, niveau_requis=2, vendable=55
        )

        self.serrated_dirk = Item(
            "serrated_dirk",
            "Une dague dentelée : rapide, bon critique.",
            1.2,
            display_name="Serrated Dirk",
            type="weapon",
            damage=10, durability=25, niveau_requis=1, crit_chance=0.15, vendable=45
        )

        self.hearthbound_axe = Item(
            "hearthbound_axe",
            "Une hache fiable, bons dégâts.",
            4.0,
            display_name="Hearthbound Axe",
            type="weapon",
            damage=15, durability=35, niveau_requis=2, vendable=50
        )

        # Shield
        self.glacial_buckler = Item(
            "glacial_buckler",
            "Bouclier glacé : défense + un peu de PV.",
            3.0,
            display_name="Glacial Buckler",
            type="shield",
            armure_phys=3, hp=10, vendable=45
        )

        # Armors
        self.bramble_vest = Item(
            "bramble_vest",
            "Armure épineuse : bonne défense.",
            6.0,
            display_name="Bramble Vest",
            type="armor",
            armure_phys=4, hp=15, vendable=40
        )

        self.winged_moonplate = Item(
            "winged_moonplate",
            "Armure légère : défense + agilité.",
            4.0,
            display_name="Winged Moonplate",
            type="armor",
            armure_phys=3, agilite=2, vendable=50
        )

        # Magic/Other
        self.sheen = Item(
            "sheen",
            "Cristal magique : augmente un peu la magie.",
            0.8,
            display_name="Sheen",
            type="magic",
            magie_bonus=3, vendable=35
        )

        self.zeal = Item(
            "zeal",
            "Équipement léger : vitesse/crit (soft).",
            0.7,
            display_name="Zeal",
            type="other",
            bonus={"crit_chance": 0.05, "agilite": 1},
            vendable=45
        )

        self.rod_of_ages = Item(
            "rod_of_ages",
            "Artefact ancien : bonus magie + PV (modéré).",
            2.5,
            display_name="Rod of Ages",
            type="magic",
            magie_bonus=5, hp=20, vendable=700, niveau_requis=3
        )

        
       
        

        self.pomme = Item("pomme", "Une petite pomme rouge.", 0.2, heal=30, type="potion", vendable=1)
        self.depart = Item("depart", "une carte du Labyrinthe.", 0.2, vendable=1)
        self.potion_soin = Item(
            "potion_soin", 
            "Restaure une partie de la vie.", 
            0.5, heal=50, type="potion", vendable=15)

        self.maison_bas.inventory["pomme"] = self.pomme
        self.d3_depart.inventory["depart"] = self.depart

    def _setup_characters(self):
        mere = Character(
            "mere",
            "ta mère, elle a l'air inquiète",
            self.maison_bas,
            ["Range ta chambre !", "Fais attention sur la route."],
            movable=False,
        )

        ancien = Character(
            "ancien",
            "Le sage qui vit dans l'ancienne maison",
            self.maison_ancien,
            ["La patience est une vertu.", "Les forêts cachent des secrets."],
            movable=False,
        )

        marchand = Character(
            "marchand",
            "Un marchand proposant divers objets",
            self.magasin_village,
            ["Bonjour ! Tu veux acheter ?", "J'ai des objets rares en stock !"],
            movable=False,
        )

        vendeur = Character(
            "vendeur",
            "Un vendeur  proposant divers objets",
            self.magasin_village,
            ["Bonjour ! Tu veux acheter ?", "J'ai des objets rares en stock !"],
            movable=False,
        )


        

        marchand_ambulant = Character(
            "marchand_ambulant",
            "Un marchand ambulant terrorisé, coincé avec sa caravane.",
            self.foret_sombre,
            ["Merci... tu peux m'aider ?"],
            movable=False,
        )
        self.foret_sombre.characters["marchand_ambulant"] = marchand_ambulant

        self.marchand_ambulant = marchand_ambulant


        aubergiste = Character(
            "aubergiste",
            "Tient l'auberge et propose nourriture et boissons",
            self.auberge,
            ["Bienvenue ! Un petit repas ?", "Repose-toi bien, voyageur."],
            movable=False,
        )

        mage = Character(
            "mage",
            "Un mage qui échange des artefacts magiques",
            self.guild,
            ["Je peux t'enseigner des sorts.", "J'ai des artefacts puissants."],
            movable=False,
        )

        herboriste = Character(
            "herboriste",
            "Une herboriste connaissant les plantes médicinales",
            self.village,
            ["Je peux te vendre des potions.", "Les plantes sont ma spécialité."],
            movable=False,
        )

        villageois = Character(
            "villageois",
            "Un villageois parlant de la vie du village",
            self.village,
            ["Bonjour !", "Il fait beau aujourd'hui, non ?"],
            movable=False,
        )
        
        guard_village = Character(
            "guard_village",
            "guard_village parlant de la vie du village",
            self.village,
            ["Bonjour !"],
            movable=False,
        )


        marchand_guilde = Character(
            "marchand_guilde",
            "Un marchand affilié à la guilde : il vend de l'équipement rare.",
            self.guild,
            ["Bienvenue à la guilde. Besoin d'équipement ?", "J'ai du stock réservé aux membres."],
            movable=False,
        )

        echangeur_auberge = Character(
            "echangeur_auberge",
            "Un courtier discret : il rachète tes objets contre de l'or.",
            self.auberge,
            ["Je peux te racheter ce que tu trouves.", "Montre-moi ton sac…"],
            movable=False,
        )


        self.maison_bas.characters["mere"] = mere
        self.village.characters["villageois"] = villageois
        self.maison_ancien.characters["ancien"] = ancien
        self.village.characters["guard_village"] = guard_village
        self.magasin_village.characters["marchand"] = marchand
        self.magasin_echange_village.characters["vendeur"] = vendeur
        self.auberge.characters["aubergiste"] = aubergiste
        self.guild.characters["mage"] = mage
        self.village.characters["herboriste"] = herboriste
        self.guild.characters["marchand_guilde"] = marchand_guilde
        self.auberge.characters["echangeur_auberge"] = echangeur_auberge  

        self.characters = [mere, villageois, ancien,guard_village, marchand, vendeur, aubergiste, mage, herboriste, marchand_guilde, echangeur_auberge]

        
        gobelin = MonsterCharacter(
            name="gobelin",
            description="Un petit gobelin malicieux et agressif.",
            current_room=self.foret,
            msgs=[],
            hp=35,
            attack=5,
            attack_max=8,
            defense=2,
            loot=[
                Item("noyau", "Noyau solide (golem).", 0.2, vendable=8),
                Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15)

            ],
            movable=False,
            xp_reward=10
        )

        gobelin = MonsterCharacter(
            name="gobelin",
            description="Un petit gobelin malicieux et agressif.",
            current_room=self.foret,
            msgs=[],
            hp=35,
            attack=5,
            attack_max=8,
            defense=2,
            loot=[
                Item("noyau", "Noyau solide (golem).", 0.2, vendable=8),
                Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15)
            ],
            movable=False,
            xp_reward=10
        )

        hobelin = MonsterCharacter(
            name="hobelin",
            description="Un hobelin plus costaud qu'un gobelin.",
            current_room=self.foret,
            msgs=[],
            hp=60,
            attack=8,
            attack_max=12,
            defense=4,
            loot=[Item("noyau", "Noyau solide (golem).", 0.2, vendable=8),],
            movable=False,
            xp_reward=15
        )



        bandit = MonsterCharacter(
            name="bandit",
            description="Un bandit qui détrousse les voyageurs.",
            current_room=self.foret,
            msgs=[],
            hp=70,
            attack=12,
            attack_max=16,
            defense=5,
            loot=[Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
                  Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15)
        ],
            movable=False,
            xp_reward=18
        )

        slime = MonsterCharacter(
            name="slime",
            description="Un slime gélatineux.",
            current_room=self.donjon_1,
            msgs=[],
            hp=25,
            attack=4,
            attack_max=6,
            defense=1,
            loot=[Item("noyau", "Noyau solide (golem).", 0.2, vendable=8),],
            movable=False,
            xp_reward=8
        )

        golem = MonsterCharacter(
            name="golem",
            description="Un golem de pierre massif.",
            current_room=self.donjon_2,
            msgs=[],
            hp=120,
            attack=18,
            attack_max=25,
            defense=10,
            loot=[Item("noyau", "Noyau solide (golem).", 0.2, vendable=8),],
            movable=False,
            xp_reward=40
        )

        furie_nocturne = MonsterCharacter(
            name="furie_nocturne",
            description="Le boss final, une créature de l'ombre.",
            current_room=self.donjon_boss,
            msgs=[],
            hp=250,
            attack=25,
            attack_max=35,
            defense=15,
            loot=[Item("écaille de fureur nocturne", "Trophée du boss.", 2.0)],
            movable=False,
            xp_reward=120
        )

        squelettes = MonsterCharacter(
            name="squelettes",
            description="Un groupe de sept squelettes encerclant la caravane du marchand.",
            current_room=self.foret_sombre,
            msgs=[],
            hp=70,
            attack=35,        # 7*5
            attack_max=35,
            defense=2,
            loot=[Item("noyau", "Un noyau vendable.", 0.1, vendable=8),],     
            movable=False,
            xp_reward=20
        )

        # --- BANDITS (groupe) ---
        bandits = MonsterCharacter(
            name="bandits",
            description="Un groupe de sept bandits lourdement armés bloque la route de la capitale.",
            current_room=self.route_capitale,
            msgs=[],
            hp=120,
            attack=35,
            attack_max=50,
            defense=5,
            loot=[Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
                  Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15)
            ],
            movable=False,
            xp_reward=30
        )
        

        chevre_humaine = MonsterCharacter(
            name="chevre_humaine",
            description="Une créature démoniaque mi-humaine mi-chèvre à la force brutale.",
            current_room=self.d3_s11,
            msgs=[],
            hp=120,
            attack=18,
            attack_max=26,
            defense=12,
            loot=[Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
                  Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15)
            ],
            movable=False,
            xp_reward=45
        )
        

        demone = MonsterCharacter(
            name="demone",
            description="Une démone agile et vicieuse frappant avec rapidité.",
            current_room=self.d3_s10,
            msgs=[],
            hp=65,
            attack=14,
            attack_max=20,
            defense=6,
            loot=[Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
                  Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15)
            ],
            movable=False,
            xp_reward=28
        )

        demon = MonsterCharacter(
            name="demon",
            description="Un démon robuste issu des profondeurs du donjon.",
            current_room=self.d3_s14,
            msgs=[],
            hp=150,
            attack=36,
            attack_max=50,
            defense=10,
            loot=[Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
                  Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15)
            ],
            movable=False,
            xp_reward=35
        )

        fantome_boss = MonsterCharacter(
            name="fantome_boss",
            description="L’esprit tourmenté d’un ancien seigneur du donjon.",
            current_room=self.donjon_2_salle_3,
            msgs=[],
            hp=140,
            attack=20,
            attack_max=28,
            defense=14,
            loot=[Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
                  Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15)
            ],
            movable=False,
            xp_reward=70
        )

        goblin_combat = MonsterCharacter(
            name="goblin_combat",
            description="Un gobelin entraîné pour le combat rapproché.",
            current_room=self.donjon_2_salle_2,
            msgs=[],
            hp=70,
            attack=15,
            attack_max=21,
            defense=7,
            loot=[Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
                  Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15)
            ],
            movable=False,
            xp_reward=25
        )

        goblin_ingi = MonsterCharacter(
            name="goblin_ingi",
            description="Un gobelin ingénieur utilisant des mécanismes dangereux.",
            current_room=self.donjon_2_salle_2,
            msgs=[],
            hp=60,
            attack=13,
            attack_max=22,
            defense=6,
            loot=[Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
                  Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15)
            ],
            movable=False,
            xp_reward=27
        )

        gargouille_giante = MonsterCharacter(
            name="gargouille_giante",
            description="Une gargouille géante animée par une magie ancienne.",
            current_room=self.donjon_2_salle_1,
            msgs=[],
            hp=160,
            attack=22,
            attack_max=30,
            defense=18,
            loot=[Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
                  Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15)
            ],
            movable=False,
            xp_reward=80
        )

        goblin_mage_foret = MonsterCharacter(
            name="goblin_mage",
            description="Un gobelin lançant des sorts instables.",
            current_room=self.donjon_2_salle_3,
            msgs=[],
            hp=55,
            attack=17,
            attack_max=26,
            defense=5,
            loot=[Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
                  Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15)],
            movable=False,
            xp_reward=30
        )

        golem_bois = MonsterCharacter(
            name="golem_bois",
            description="Un golem massif composé de bois ancien et de racines.",
            current_room=self.donjon_2_salle_1,
            msgs=[],
            hp=130,
            attack=18,
            attack_max=25,
            defense=15,
            loot=[Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
                  Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15) ],
            movable=False,
            xp_reward=50
        )

        golem_meca = MonsterCharacter(
            name="golem_meca",
            description="Un golem mécanique lourdement blindé.",
            current_room=self.donjon_4_salle_3,
            msgs=[],
            hp=170,
            attack=20,
            attack_max=28,
            defense=20,
            loot=[Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
                  Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15)  ],
            movable=False,
            xp_reward=85
        )

        homme_feu = MonsterCharacter(
            name="homme_feu",
            description="Une entité humanoïde composée de flammes vivantes.",
            current_room=self.donjon_4_salle_2,
            msgs=[],
            hp=100,
            attack=19,
            attack_max=27,
            defense=9,
            loot=[Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
                  Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15)  ],
            movable=False,
            xp_reward=40
        )

        horde_zombie = MonsterCharacter(
            name="horde_zombie",
            description="Un groupe de zombies avançant de manière implacable.",
            current_room=self.donjon_4_salle_1,
            msgs=[],
            hp=150,
            attack=37,
            attack_max=60,
            defense=10,
            loot=[Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
                  Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15)  ],
            movable=False,
            xp_reward=55
        )

        kraken = MonsterCharacter(
            name="kraken",
            description="Une créature tentaculaire surgie des profondeurs.",
            current_room=self.donjon_4_salle_2,
            msgs=[],
            hp=180,
            attack=22,
            attack_max=32,
            defense=16,
            loot=[Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
                  Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15)   ],
            movable=False,
            xp_reward=90
        )

        kraken_glace = MonsterCharacter(
            name="kraken_glace",
            description="Un kraken recouvert de glace éternelle.",
            current_room=self.donjon_4_salle_1,
            msgs=[],
            hp=190,
            attack=21,
            attack_max=31,
            defense=18,
            loot=[Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
                  Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15)  ],
            movable=False,
            xp_reward=95
        )

        oeil_enfer = MonsterCharacter(
            name="oeil_enfer",
            description="Un œil démoniaque flottant qui observe et attaque.",
            current_room=self.d3_s12,
            msgs=[],
            hp=80,
            attack=18,
            attack_max=25,
            defense=8,
            loot=[Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
                  Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15)  ],
            movable=False,
            xp_reward=35
        )

        orc = MonsterCharacter(
            name="orc",
            description="Un guerrier orc brutal et endurant.",
            current_room=self.d3_s6,
            msgs=[],
            hp=95,
            attack=17,
            attack_max=24,
            defense=11,
            loot=[Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
                  Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15)  ],
            movable=False,
            xp_reward=38
        )

        orc_glace = MonsterCharacter(
            name="orc_glace",
            description="Un orc imprégné d’énergie glaciale.",
            current_room=self.d3_s9,
            msgs=[],
            hp=100,
            attack=16,
            attack_max=23,
            defense=13,
            loot=[Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
                  Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15)   ],
            movable=False,
            xp_reward=40
        )

        orc_shaman = MonsterCharacter(
            name="orc_shaman",
            description="Un chaman orc maîtrisant des rituels obscurs.",
            current_room=self.d3_s7,
            msgs=[],
            hp=85,
            attack=18,
            attack_max=27,
            defense=9,
            loot=[Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
                  Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15)  ],
            movable=False,
            xp_reward=42
        )

        pet_enfer = MonsterCharacter(
            name="pet_enfer",
            description="Une petite créature infernale imprévisible.",
            current_room=self.d3_s8,
            msgs=[],
            hp=50,
            attack=15,
            attack_max=22,
            defense=5,
            loot=[Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
                  Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15)  ],
            movable=False,
            xp_reward=22
        )

        phoenix = MonsterCharacter(
            name="phoenix",
            description="Un oiseau de feu renaissant de ses cendres.",
            current_room=self.d3_s12,
            msgs=[],
            hp=150,
            attack=21,
            attack_max=30,
            defense=12,
            loot=[Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
                  Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15)  ],
            movable=False,
            xp_reward=75
        )

        serpent = MonsterCharacter(
            name="serpent",
            description="Un serpent géant rapide et venimeux.",
            current_room=self.d3_s2,
            msgs=[],
            hp=70,
            attack=16,
            attack_max=23,
            defense=6,
            loot=[Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
                  Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15)  ],
            movable=False,
            xp_reward=26
        )

        serpent_feu = MonsterCharacter(
            name="serpent_feu",
            description="Un serpent entouré de flammes brûlantes.",
            current_room=self.d3_s5,
            msgs=[],
            hp=85,
            attack=18,
            attack_max=26,
            defense=7,
            loot=[Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
                  Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15) ],
            movable=False,
            xp_reward=32
        )

        slime_eau = MonsterCharacter(
            name="slime_eau",
            description="Un slime composé d’eau stagnante.",
            current_room=self.donjon_1,
            msgs=[],
            hp=60,
            attack=12,
            attack_max=18,
            defense=8,
            loot=[Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
                  Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15) ],
            movable=False,
            xp_reward=20
        )

        slime_feu = MonsterCharacter(
            name="slime_feu",
            description="Un slime brûlant au contact.",
            current_room=self.d3_s13,
            msgs=[],
            hp=65,
            attack=14,
            attack_max=21,
            defense=7,
            loot=[Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
                  Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15) ],
            movable=False,
            xp_reward=22
        )

        slime_nature = MonsterCharacter(
            name="slime_nature",
            description="Un slime verdoyant régénérant lentement.",
            current_room=self.d3_depart,
            msgs=[],
            hp=75,
            attack=13,
            attack_max=19,
            defense=9,
            loot=[Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
                  Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15)],
            movable=False,
            xp_reward=24
        )

        squelette_feu = MonsterCharacter(
            name="squelette_feu",
            description="Un squelette animé par des flammes infernales.",
            current_room=self.d3_s3,
            msgs=[],
            hp=70,
            attack=16,
            attack_max=24,
            defense=8,
            loot=[Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
                  Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15)  ],
            movable=False,
            xp_reward=30
        )

        squelette_mage = MonsterCharacter(
            name="squelette_mage",
            description="Un mage squelette maîtrisant la magie noire.",
            current_room=self.d3_s12,
            msgs=[],
            hp=65,
            attack=18,
            attack_max=26,
            defense=6,
            loot=[Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
                  Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15)  ],
            movable=False,
            xp_reward=32
        )

        squelette_shaman = MonsterCharacter(
            name="squelette_shaman",
            description="Un chaman squelette invoquant des esprits.",
            current_room=self.d3_s15,
            msgs=[],
            hp=80,
            attack=19,
            attack_max=28,
            defense=9,
            loot=[Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
                  Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15) ],
            movable=False,
            xp_reward=38
        )

        trolle = MonsterCharacter(
            name="trolle",
            description="Un troll massif à la force écrasante.",
            current_room=self.d3_s10,
            msgs=[],
            hp=200,
            attack=24,
            attack_max=35,
            defense=22,
            loot=[Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
                  Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15) ],
            movable=False,
            xp_reward=100
        )

        zombie_evoluer = MonsterCharacter(
            name="zombie_evoluer",
            description="Un zombie muté devenu extrêmement dangereux.",
            current_room=self.d3_s11,
            msgs=[],
            hp=110,
            attack=22,
            attack_max=30,
            defense=14,
            loot=[Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
                  Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15)  ],
            movable=False,
            xp_reward=55
        )

        
        
        
        crane_feu = MonsterCharacter(
            name="crane_feu",
            description="Un démon mi humain mi chèvre",
            current_room=self.donjon_2_salle_3,
            msgs=[],
            hp=35,
            attack=5,
            attack_max=8,
            defense=2,
            loot=[
                Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
                Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15)  ],
            movable=False,
            xp_reward=10
        )



        coffre_piege = MonsterCharacter(
            name="coffre_piege",
            description="Un démon mi humain mi chèvre",
            current_room=self.donjon_1_tunnel,
            msgs=[],
            hp=35,
            attack=5,
            attack_max=8,
            defense=2,
            loot=[
                Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
                Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15) ],
            movable=False,
            xp_reward=10
        ) 

        corbeau = MonsterCharacter(
            name="corbeau",
            description=" KOA KOA",
            current_room=self.foret_capitale,
            msgs=[],
            hp=23,
            attack=7,
            attack_max=12,
            defense=0,
            loot=[
                Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15)   ],
            movable=False,
            xp_reward=10
        ) 
       
       
        fantome = MonsterCharacter(
            name="fantome",
            description="Un esprit errant lié à ce lieu.",
            current_room=self.donjon_2,
            msgs=[],
            hp=65,
            attack=7,
            attack_max=10,
            defense=2,
            loot=[
                Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15)  ],
            movable=False,
            xp_reward=15
)


        goblin_mage = MonsterCharacter(
            name="goblin_mage",
            description="Un gobelin maniant une magie instable.",
            current_room=self.donjon_1_chambre,
            msgs=[],
            hp=50,
            attack=8,
            attack_max=11,
            defense=3,
            loot=[
                Item("potion_soin", "Restaure une partie de la vie.", 0.5, heal=50, type="potion", vendable=15)  ],
            movable=False,
            xp_reward=18
        )

        golem_feu = MonsterCharacter(
            name="golem_feu",
            description="Un golem massif constitué de roche en fusion.",
            current_room=self.donjon_5_salle_2,
            msgs=[],
            hp=200,
            attack=25,
            attack_max=28,
            defense=2,
            loot=[Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
            ],
            movable=False,
            xp_reward=10
        )


        zombie = MonsterCharacter(
            name="zombie",
            description="Un cadavre réanimé animé par une magie noire.",
            current_room=self.donjon_1_tunnel,
            msgs=[],
            hp=35,
            attack=5,
            attack_max=8,
            defense=2,
            loot=[
                Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
            ],
            movable=False,
            xp_reward=10
        )

        goblin_mage = MonsterCharacter(
            name="goblin_mage",
            description="Un gobelin chétif maniant une magie instable.",
            current_room=self.foret_capitale,
            msgs=[],
            hp=35,
            attack=9,
            attack_max=15,
            defense=2,
            loot=[
                Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
            ],
            movable=False,
            xp_reward=10
        )


        serpent_glace = MonsterCharacter(
            name="serpent_glace",
            description="Un serpent couvert d'écailles gelées.",
            current_room=self.donjon_5_salle_1,
            msgs=[],
            hp=80,
            attack=55,
            attack_max=80,
            defense=23,
            loot=[
                Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
            ],
            movable=False,
            xp_reward=10
        )

        phoenix = MonsterCharacter(
            name="phoenix",
            description="Un oiseau de feu renaissant éternellement de ses cendres.",
            current_room=self.donjon_5_salle_3,
            msgs=[],
            hp=1500,
            attack=25,
            attack_max=28,
            defense=2,
            loot=[
                Item("noyau", "Un noyau vendable.", 0.1, vendable=8),
            ],
            movable=False,
            xp_reward=10
        )

        


        # =========================================================
        # ✅ PLACEMENT COHÉRENT DES MONSTRES PAR ÉTAGES (THEME)
        # =========================================================

        # -------------------------
        # NIVEAU 1 — Entrée (gobelins / slimes / pièges)
        # -------------------------
        self.donjon_1.characters["slime"] = slime
        self.donjon_1.characters["slime_nature"] = slime_nature
        self.donjon_1_chambre.characters["goblin_mage"] = goblin_mage      
        self.donjon_1_tunnel.characters["goblin_combat"] = goblin_combat
        self.donjon_1_tunnel.characters["goblin_ingi"] = goblin_ingi
        self.donjon_1_tunnel.characters["coffre_piege"] = coffre_piege     

        # -------------------------
        # NIVEAU 2 — Humidité / corruption (morts-vivants / eau)
        # -------------------------
        self.donjon_2_salle_1.characters["zombie"] = zombie
        self.donjon_2_salle_2.characters["slime_eau"] = slime_eau
        self.donjon_2_salle_2.characters["serpent"] = serpent
        self.donjon_2_salle_3.characters["zombie_evoluer"] = zombie_evoluer
        self.donjon_2_salle_3.characters["horde_zombie"] = horde_zombie
        self.donjon_2_salle_1.characters["golem_bois"] = golem_bois      

        # -------------------------
        # NIVEAU 3 — Labyrinthe (esprits / illusions)
        # -------------------------
        self.donjon_2.characters["fantome"] = fantome
        self.donjon_2_salle_3.characters["fantome_boss"] = fantome_boss
        # le corbeau peut être un “éclaireur” du labyrinthe (sinon tu le laisses en forêt)
        self.d3_s8.characters["corbeau"] = corbeau
        # squelette mage + shaman = magie noire = bon pour labyrinthe
        self.d3_s12.characters["squelette_mage"] = squelette_mage
        self.d3_s15.characters["squelette_shaman"] = squelette_shaman

        # -------------------------
        # NIVEAU 4 — Brume / glace / abyssal (glace + monstres lourds)
        # -------------------------
        self.donjon_4_salle_3.characters["golem_meca"] = golem_meca
        self.donjon_4_salle_1.characters["kraken_glace"] = kraken_glace
        self.donjon_4_salle_2.characters["kraken"] = kraken
        self.donjon_4_salle_3.characters["orc_glace"] = orc_glace
        self.donjon_4_salle_2.characters["serpent_glace"] = serpent_glace
        self.donjon_4_salle_1.characters["gargouille_giante"] = gargouille_giante

        # -------------------------
        # NIVEAU 5 — 🔥 FEU / ENFER 🔥 (TOUT ce qui brûle / démoniaque)
        # -------------------------
        self.donjon_5_salle_1.characters["homme_feu"] = homme_feu
        self.donjon_5_salle_1.characters["crane_feu"] = crane_feu
        self.donjon_5_salle_2.characters["golem_feu"] = golem_feu
        self.donjon_5_salle_2.characters["serpent_feu"] = serpent_feu
        self.donjon_5_salle_2.characters["slime_feu"] = slime_feu
        self.donjon_5_salle_3.characters["demon"] = demon
        self.donjon_5_salle_3.characters["demone"] = demone
        self.donjon_5_salle_3.characters["pet_enfer"] = pet_enfer
        self.donjon_5_salle_3.characters["oeil_enfer"] = oeil_enfer
        # Phoenix = mini-boss feu -> ici seulement (plus dans le niveau 3)
        self.donjon_5.characters["phoenix"] = phoenix

        # -------------------------
        # Boss final (inchangé)
        # -------------------------
        self.donjon_boss.characters["furie_nocturne"] = furie_nocturne

        # -------------------------
        # Hors-donjon (tu gardes tes scénarios)
        # -------------------------
        self.foret.characters["bandit"] = bandit
        self.foret.characters["gobelin"] = gobelin
        self.foret.characters["hobelin"] = hobelin
        self.foret_sombre.characters["squelettes"] = squelettes
        self.route_capitale.characters["bandits"] = bandits

        # goblin mage de forêt (celui renommé) : seulement dans foret_capitale
        self.foret_capitale.characters["goblin_mage"] = goblin_mage_foret

        # chevre_humaine + trolle + orc + orc_shaman : si tu veux les garder,
        # on les met au niveau 4 (bestial / lourd / expérimental)
        self.donjon_4_salle_1.characters["trolle"] = trolle
        self.donjon_4_salle_2.characters["chevre_humaine"] = chevre_humaine
        self.donjon_4_salle_3.characters["orc"] = orc
        self.donjon_4_salle_2.characters["orc_shaman"] = orc_shaman
   
        
        
        self.characters += [
            gobelin,
            hobelin,
            bandit,
            slime,
            golem,
            furie_nocturne,
            squelettes,
            bandits,
            chevre_humaine,
            demone,
            demon,
            fantome_boss,
            goblin_combat,
            goblin_ingi,
            gargouille_giante,
            goblin_mage,     
            golem_bois,
            golem_meca,
            homme_feu,
            horde_zombie,
            kraken,
            kraken_glace,
            oeil_enfer,
            orc,
            orc_glace,
            orc_shaman,
            pet_enfer,
            phoenix,        
            serpent,
            serpent_feu,
            slime_eau,
            slime_feu,
            slime_nature,
            squelette_feu,
            squelette_mage,
            squelette_shaman,
            trolle,
            zombie_evoluer,
            crane_feu,
            coffre_piege,
            corbeau,
            fantome,
            golem_feu,
            zombie,
            serpent_glace
        ]

       

        


    def _setup_dialogues(self):
        """
        Dialogues centralisés (exactement ceux du code pas propre),
        mais stockés dans Game pour que Actions reste clean.
        """
        self.dialogues = {
            # =========================
            # MÈRE (exactement ton texte)
            # =========================
            "mere": {
                "portrait_key": "mere",
                "title": "LA MÈRE :",
                "first": "\"Tu vas vraiment partir, fiston ? Avant que tu t'en ailles... j'aimerais te dire quelque chose.\"",
                "choices": [
                    "\"Ne t'inquiète pas, maman... Je veux juste faire ce qu'il faut.\"",
                    "\"J'ai pas le temps pour ça, maman.\"",
                    "\"Oui... Je dois partir. J'ai besoin de réponses.\"",
                ],
                "replies": [
                    "Je le sais mon coeur...\n"
                    "Avant de partir, monte à l'étage. Ton père avait laissé son épée dans le coffre.\n"
                    "Prends-la, elle te protègera.\n"
                    "Et ensuite... va voir l'ancien. Lui seul connaît la vérité sur ce qui t'attend.",
                    "Alors écoute-moi bien.\n"
                    "Monte à l'étage récupérer l'épée de ton père, tu en auras besoin.\n"
                    "Puis va voir l'ancien : il t'expliquera tout ce que je ne peux pas te dire.",
                    "... Même si tu me parles comme ça, je veux seulement que tu sois en sécurité.\n"
                    "Monte prendre l'épée à l'étage.\n"
                    "Et surtout... va voir l'ancien avant de quitter le village.\n"
                    "Tu comprendras pourquoi plus tard.",
                ],
                "repeat_text": (
                    "\nTa mère te prend les mains :\n"
                    "\"Je t'ai déjà dit tout ce que je pouvais, mon cœur. "
                    "Va, et surtout reste en vie.\"\n"
                ),
            },

            # =========================
            # GARDE DU VILLAGE
            # =========================
            "guard_village": {
                "portrait_key": "guard_village",
                "title": "LE GARDE :",

                # pré-Ancien (la 1ère fois)
                "pre_first": "\"Halte-là ! Ordre de l'Ancien : personne ne sort du village sans avoir reçu ses instructions.\"",
                "pre_choices": [
                    "\"Je veux juste aller voir ce qu'il y a dans la forêt.\"",
                    "\"Je n'ai pas de temps à perdre avec vos règles.\"",
                    "\"Pourquoi je dois voir l'Ancien d'abord ?\"",
                ],
                "pre_replies": [
                    "Pas question. Tu ne sais pas ce qui t'attend là-bas, "
                    "et moi je ne veux pas ramasser ton corps.\n"
                    "Va voir l'Ancien au sud du village, dans sa vieille maison.",
                    "Alors tu as encore plus besoin de lui parler.\n"
                    "Lui seul sait ce qui rôde dans cette forêt.\n"
                    "Reviens me voir une fois que tu l'auras rencontré.",
                    "Parce que lui connaît la vérité sur ce qui se passe au-delà des arbres.\n"
                    "Ses ordres sont clairs : tant qu'il ne t'a pas parlé, tu restes ici.",
                ],
                "pre_repeat_text": (
                    "\nLe garde soupire :\n"
                    "\"Je t'ai déjà dit : va voir l'Ancien au sud du village. "
                    "Tant que ce n'est pas fait, tu restes ici.\"\n"
                ),

                # post-Ancien (après avoir parlé à l’Ancien)
                "post_first": "\"Je vois dans ton regard que l'Ancien t'a tout dit...\"",
                "post_choices": [
                    "\"Il m'a demandé de quitter le village, coûte que coûte.\"",
                    "\"Je ne suis pas sûr d'être prêt, mais je dois y aller.\"",
                    "\"Je veux juste en finir avec tout ça.\"",
                ],
                "post_replies": [
                    "Alors je ne peux plus te retenir.\n"
                    "La route vers la forêt t'est ouverte.\n"
                    "Fais attention, et ne meurs pas trop vite.",
                    "Personne n'est jamais vraiment prêt.\n"
                    "Mais si l'Ancien t'a choisi, c'est qu'il a ses raisons.\n"
                    "Va. La forêt t'attend.",
                    "Tu parles comme quelqu'un qui a déjà trop souffert.\n"
                    "Traverse la forêt, trouve tes réponses.\n"
                    "Je garderai le village en ton absence.",
                ],
                "post_repeat_text": (
                    "\nLe garde hoche la tête :\n"
                    "\"La route est ouverte pour toi. Fais ce que tu as à faire, héros.\"\n"
                ),
            },

            # =========================
            # ANCIEN
            # =========================
            "ancien": {
                "portrait_key": "ancien",
                "title": "L'ANCIEN :",
                "first": "\"Te voilà enfin... Le village murmure ton départ depuis longtemps.\"",
                "choices": [
                    "\"Pourquoi tout le monde me cache la vérité ?\"",
                    "\"Je veux comprendre ces visions que je fais la nuit.\"",
                    "\"Je n'ai pas le temps. Dis-moi juste où aller.\"",
                ],
                "replies": [
                    "Parce que la vérité effraie plus que les mensonges. "
                    "Mais si tu es prêt à écouter, je peux commencer à t'expliquer.",
                    "Ces visions ne sont pas des rêves ordinaires. "
                    "Elles sont liées à un ancien pacte, à ta famille... et à ton destin.",
                    "Toujours aussi pressé... Va vers la capitale. "
                    "Là-bas, quelqu'un t'attend avec les réponses que tu cherches.",
                ],
                "repeat_text": (
                    "\nL'Ancien te regarde longuement :\n"
                    "\"Je t'ai déjà donné plus de réponses que la plupart des gens n'en auront jamais.\n"
                    "Maintenant, va tracer ta route.\"\n"
                )
            },

            # =========================
            # Marchand du village (boutique)
            # =========================
            "marchand_village": {
                "open_shop": True
            },

            "marchand_guilde": {
                "open_shop": True
            },

            # =========================
            # Salle d’échange
            # =========================
            "echange_village": {
                "open_exchange": True
            },
            
            "vendeur": {
            "open_exchange": True
            },

            "echangeur_auberge": {
                "open_exchange": True
            },
        }

    def get_dialogue(self, npc_key: str):
        if not npc_key:
            return None
        return self.dialogues.get(npc_key.lower())


    def _setup_exits(self):
        self.maison_haut.exits = {"bas": self.maison_bas}
        self.maison_bas.exits = {"haut": self.maison_haut, "S": self.village}

        # Village: ajout d'accès vers magasin et auberge
        self.village.exits = {
            "N": self.maison_bas,
            "O": self.magasin_village,
            "E": self.maison_ancien,
            "S": self.foret,
        }

        # Magasin mène à la forge
        self.magasin_village.exits = {"E": self.village, "haut": self.magasin_echange_village}
        self.magasin_echange_village.exits = {"bas": self.magasin_village}

        self.maison_ancien.exits = {"O": self.village}

        self.foret.exits = {"N": self.village, "E": self.foret_sombre}
        self.foret_sombre.exits = {"O": self.foret, "S": self.route_capitale }
        self.route_capitale.exits = {"N": self.foret_sombre, "S": self.avant_post_capitale }
        self.avant_post_capitale.exits = {"N": self.route_capitale, "S": self.rue_capitale}

        self.rue_capitale.exits = {"N": self.avant_post_capitale, "E": self.chateau, "O": self.guild, "S": self.foret_capitale,"bas":self.donjon }
        self.foret_capitale.exits = {"N": self.rue_capitale}
        self.chateau.exits = {"O": self.rue_capitale}
        self.guild.exits = {"E": self.rue_capitale, "haut": self.auberge }
        self.auberge.exits = {"bas": self.guild}
        # Daungon (sous-sol)
        self.donjon.exits = {
            "N": None, "E": None, "S": None, "O": None,
            "haut": self.rue_capitale,
            "bas": self.donjon_1
        }
        

        # Donjon 1
        self.donjon_1.exits = {
            "N": None, "E": self.donjon_1_chambre, "S": self.donjon_1_tunnel, "O": None,
            "haut": self.donjon
        }
        self.donjon_1_chambre.exits = {"O": self.donjon_1}
        self.salle_exploration.exits = {"N": self.donjon_1_tunnel, "bas": self.donjon_2 }

        self.donjon_1_tunnel.exits = {"S": self.salle_exploration,"N": self.donjon_1}

        # Donjon 2
        self.donjon_2.exits = {"E": self.donjon_2_salle_1, "S": self.donjon_2_salle_2,
                            "haut": self.salle_exploration}
        self.donjon_2_salle_1.exits = {"O": self.donjon_2, "E": self.donjon_2_salle_3,
                                    "N": None, "S": None, "haut": None, "bas": None}
        self.donjon_2_salle_2.exits = {"N": self.donjon_2, "S": None, "E": None, "haut": None, "bas": None}
        self.donjon_2_salle_3.exits = {"O": self.donjon_2_salle_1,"bas": self.d3_depart}

       # =========================
        # Donjon 3 – Exits (Labyrinthe)
        # =========================

        # DÉPART -> S9
        self.d3_depart.exits = {
            "S": self.d3_s1,
            "haut": self.donjon_2_salle_3
        }

        self.d3_s1.exits = {
            "N": self.d3_depart,
            "O": self.d3_s2
        }

        self.d3_s2.exits = {
            "E": self.d3_s1,
            "S": self.d3_s3
        }
        
        self.d3_s3.exits = {
            "N": self.d3_s2,
            "S": self.d3_s4,
            "E": self.d3_s5
        }

        self.d3_s4.exits = {
            "N": self.d3_s3
        }

        self.d3_s5.exits = {
            "O": self.d3_s3,
            "S": self.d3_s6
        }

        
        self.d3_s6.exits = {
            "N": self.d3_s5,
            "E": self.d3_s7, 
        }

        self.d3_s7.exits = {
            "O": self.d3_s6,
            "E": self.d3_s11,
            "N": self.d3_s8
        }
        
        self.d3_s8.exits = {
            "N": self.d3_s9,
            "S": self.d3_s7
        }

        self.d3_s9.exits = {
            "E": self.d3_s10,
            "S": self.d3_s8
        }
    
        self.d3_s10.exits = {
            "O": self.d3_s9,
            "N": self.d3_arrivee
        }
        
        self.d3_arrivee.exits = {
            "S": self.d3_s10,
            "bas": self.donjon_4
        }
        
        self.d3_s11.exits = {
            "O": self.d3_s7,
            "N": self.d3_s12
        }

        self.d3_s12.exits = {
            "E": self.d3_s13,
            "S": self.d3_s11
        }

        self.d3_s13.exits = {
            "O": self.d3_s12,
            "N": self.d3_s14,
            "S": self.d3_s15
        }

        self.d3_s14.exits = {
            "S": self.d3_s13
        }

        self.d3_s15.exits = {
            "N": self.d3_s13
}

        # Donjon 4
        self.donjon_4.exits = {"S": self.donjon_4_salle_1, "E": self.donjon_4_salle_2,
                            "haut": self.d3_arrivee}
        self.donjon_4_salle_1.exits = {"N": self.donjon_4, "E": self.donjon_4_salle_3,
                                    "N": None, "S": None, "haut": None, "bas": None}
        self.donjon_4_salle_2.exits = {"O": self.donjon_4, "S": None, "E": None, "haut": None, "bas": None}
        self.donjon_4_salle_3.exits = {"O": self.donjon_4_salle_1,"bas": self.donjon_5}


        # Donjon 5
        self.donjon_5.exits = {"S": self.donjon_5_salle_1, "E": self.donjon_5_salle_2,
                            "haut": self.donjon_4_salle_3}
        self.donjon_5_salle_1.exits = {"N": self.donjon_5, "E": self.donjon_5_salle_3,
                                    "N": None, "S": None, "haut": None, "bas": None}
        self.donjon_5_salle_2.exits = {"O": self.donjon_5, "S": None, "E": None, "haut": None, "bas": None}
        self.donjon_5_salle_3.exits = {"O": self.donjon_5_salle_1,"bas": self.donjon_boss}



        
        self.donjon_boss.exits = {
            "O": None ,  
            "N": None,
            "S": None,
            "E": None,
            "haut": None,
            "bas": None
        }


    def _register_directions(self):
        for room in self.rooms:
            for direction in room.exits.keys():
                Room.register_direction(direction)

    def _setup_player(self, player_name=None):
        if not player_name:
            try:
                player_name = input("\nEntrez votre nom: ")
            except Exception:
                player_name = "Hero"

        self.player = Player(player_name)
        self.player.current_room = self.maison_haut
        self.player.max_weight = 16
        self.player.game = self

    def get_room_by_name(self, room_name):
        room_name = room_name.lower().replace("-", "_")
        for room in self.rooms:
            if room.name.lower().replace("-", "_") == room_name:
                return room
        return None

    def _setup_quests(self):
        quete_ancien = Quest(
            title="Rencontrer l'Ancien",
            description="Parle à l'Ancien au sud du village pour comprendre ce qui se passe.",
            objectives=["parler ancien"],
            reward=self.potion_soin,
            xp_reward=20,
        )
        self.player.quest_manager.add_quest(quete_ancien)

        quete_foret = Quest(
            title="Nettoyer la forêt",
            description="Éliminer les monstres qui infestent la forêt.",
            objectives=[
                "tuer gobelin",
                "tuer hobelin",
            ],
            reward=Item(
                "épée_foret",
                "Une épée forgée pour combattre les créatures sauvages.",
                item_type="weapon",
                damage=14,
            ),
            xp_reward=20,
        )
        self.player.quest_manager.add_quest(quete_foret)


        quete_escorte_marchand = Quest(
            title="Escorter le marchand",
            description="Protéger le marchand jusqu'à l'avant-poste de la capitale.",
            objectives=[
                "parler marchand_ambulant",
                "tuer squelettes",
                "aller avant_post_capitale",
            ],
            reward=Item(
                "bourse_or",
                "Une bourse remplie d'or.",
                item_type="quest",
                bonus={"gold": 300},
            ),
            xp_reward=20,
        )

        self.player.quest_manager.add_quest(quete_escorte_marchand)




        quete_marchand = Quest(
            title="Sauver le marchand",
            description="Un marchand est attaqué par des squelettes dans la forêt sombre.",
            objectives=[
                "tuer squelettes",
            ],
            reward=Item(
                "anneau_protecteur",
                "Un anneau gravé offrant une légère protection.",
                item_type="other",
                armor=2,
            ),
            xp_reward=20,
        )
        self.player.quest_manager.add_quest(quete_marchand)


        quete_capitale = Quest(
            title="Atteindre la capitale",
            description="Traverse la forêt et les avant-postes pour arriver à la capitale.",
            objectives=["aller rue_capitale"],
            reward= self.bramble_vest,
            xp_reward=20,
        )
        self.player.quest_manager.add_quest(quete_capitale)

        quete_donjon = Quest(
            title="Dans les profondeurs",
            description="Entre dans le donjon et explore sa première salle.",
            objectives=["aller salle_exploration"],
            reward = self.potion_soin,
            xp_reward=20,
        )
        self.player.quest_manager.add_quest(quete_donjon)

        quete_boss = Quest(
            title="Vaincre la Furie Nocturne",
            description="Affronte le boss final du donjon et mets fin à son règne.",
            objectives=["tuer furie_nocturne"],
            reward=Item(
                "ecaille_furie_nocturne",
                "Une écaille sombre, preuve de ta victoire.",
                0.2,
                item_type="quest",
            ),
            xp_reward=20,
        )
        self.player.quest_manager.add_quest(quete_boss)

    def update_characters(self):
        for c in self.characters:
            moved = c.move()
            if DEBUG and moved:
                print(f"DEBUG: {c.name} s'est déplacé dans {c.current_room.name}")

    def play(self):
        self.setup()
        self.print_welcome()
        while not self.finished:
            self.process_command(input("> "))
            self.check_game_over()
        return None

    def check_game_over(self):
        if self.player.hp <= 0 and not self.finished:
            self.game_over()

    def game_over(self):
        print("\nGAME OVER")
        print("Votre aventure s'arrête ici.\n")
        self.finished = True

    def process_command(self, command_string):
        if not command_string:
            print()
            return

        list_of_words = command_string.split(" ")
        command_word = list_of_words[0]

        if command_word not in self.commands:
            print(
                f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n"
            )
            return

        command = self.commands[command_word]
        command.action(self, list_of_words, command.number_of_parameters)

    def print_welcome(self):
        print(f"\nBienvenue {self.player.name} dans ce jeu d'aventure !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        print(self.player.current_room.get_long_description())

    def check_end_game(self):
        qm = getattr(self.player, "quest_manager", None)
        if qm is None:
            return
        # gagné seulement si toutes les quêtes de la liste sont terminées
        if all(q.is_completed for q in qm.quests) and qm.quests:
            print("\nFélicitations ! Tu as terminé toutes les quêtes !")
            print("Tu as gagné le jeu !\n")
            self.finished = True