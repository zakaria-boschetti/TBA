# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
from character import Character , MonsterCharacter
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
    
    # Setup the game
    def setup(self):
        self._setup_commands()
        self._setup_rooms()
        self._setup_items()
        self._setup_characters()
        self._setup_exits()
        self._register_directions()
        self._setup_player()
        self._setup_quests()

    
    def _setup_commands(self):
        self.commands["help"] = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["quit"] = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["go"] = Command("go"," <direction> : se déplacer (N, S, E, O, haut, bas)",Actions.go,1)
        self.commands["back"] = Command("back", " : revenir au lieu précédent", Actions.back, 0)
        self.commands["history"] = Command("history", " : afficher l'historique des lieux visités", Actions.history, 0)
        self.commands["look"] = Command("look", " : observer la pièce", Actions.look, 0)
        self.commands["take"] = Command("take", " <objet> : prendre un objet", Actions.take, 1)
        self.commands["drop"] = Command("drop", " <objet> : déposer un objet", Actions.drop, 1)
        self.commands["check"] = Command("check", " : afficher l'inventaire", Actions.check, 0)
        self.commands["talk"] = Command("talk", " <personnage> : parler à un personnage", Actions.talk, 1)
        self.commands["quests"] = Command("quests"
                                          , " : afficher la liste des quêtes", Actions.quests , 0)
        self.commands["quest"] = Command("quest" , " <titre> : afficher les détails d'une quête", Actions.quest, 1)
        self.commands["activate"] = Command("activate", " <titre> : activer une quête", Actions.activate, 1)
        self.commands["rewards"] = Command("rewards", " : afficher vos récompenses", Actions.rewards, 0)
        self.commands["fight"] =Command("fight", " <monstre> : combattre un monstre dans la salle actuelle", Actions.fight, 1)
        self.commands["teleport"] =Command("teleport"," <nom_salle> : téléporte le joueur vers une salle spécifiée", Actions.teleport,1)

    def _setup_rooms(self):
        self.maison_haut = Room("maison-haut", "à l'étage de ta maison.")
        self.maison_bas = Room("maison-bas", "au rez-de-chaussée de ta maison.")
        self.village = Room("village", "sur la place du village.")
        self.forge = Room("forge", "le forgeron travaille .")
        self.magasin = Room("magasin", "dans le petit magasin du village.")
        self.magasin_echange = Room("magasin-echange", "à l'étage du magasin.")
        self.maison_ancien = Room("maison-ancien", "devant l’ancienne maison.")
        self.foret = Room("foret", "à l'entrée de la forêt.")
        self.foret_sombre = Room("foret-sombre", "dans une partie sombre de la forêt.")
        self.route_capital = Room("route-capital", "sur la route menant à la capitale.")
        self.avant_post_capital = Room("avant-post-capital", "à l'avant-poste de la capitale.")
        self.rue_capitale = Room("rue-capitale", "dans la rue principale de la capitale.")
        self.guild = Room("guild", "dans la guilde des aventuriers.")
        self.auberge = Room("auberge", "dans l'auberge.")
        self.magasin_capital = Room("magasin-capital", "dans le magasin de la capitale.")
        self.foret_capital = Room("foret-capital", "dans la forêt de la capitale.")
        self.donjon = Room("donjon", "dans les sous-sols sombres.")



        #----------------------------------------- Donjon -----------------------------------------------------#
        # Niveau 1
        self.donjon_1 = Room("salle-donjon-1", "salle principale du niveau 1, l'entrée du donjon.")
        self.donjon_1_chambre = Room("salle-chambre-abandonnee", "Une petite chambre poussiéreuse.")
        self.donjon_1_tunnel = Room("salle-tunnel-etroit", "Un tunnel sombre menant à des coins inconnus.")
        self.donjon_1_exploration = Room("salle-exploration", "Une salle avec quelques coffres vides.")

        # Niveau 2
        self.donjon_2 = Room("salle-donjon-2", "salle principale du niveau 2, escalier descendant.")
        self.donjon_2_salle_1 = Room("salle-caverne-humide", "Une caverne avec de l'eau stagnante.")
        self.donjon_2_salle_2 = Room("salle-galerie-sombre", "Galerie obscure, difficile à traverser.")
        self.donjon_2_salle_3 = Room("salle-aux-cristaux", "Des cristaux brillants illuminent la pièce.")

        # Niveau 3
        self.donjon_3 = Room("salle-donjon-3", "salle principale du niveau 3, l'air est plus froid.")
        self.donjon_3_salle_1 = Room("salle-pieges", "Attention aux pièges au sol.")
        self.donjon_3_salle_2 = Room("salle-statues", "Des statues effrayantes ornent les murs.")
        self.donjon_3_salle_3 = Room("salle-tresor", "Une salle avec un coffre verrouillé.")

        # Niveau 4
        self.donjon_4 = Room("salle-donjon-4", "salle principale du niveau 4, de la brume flotte dans l'air.")
        self.donjon_4_salle_1 = Room("salle-araignee", "Des toiles d'araignée partout.")
        self.donjon_4_salle_2 = Room("salle-puits", "Un puits profond rempli d'eau noire.")
        self.donjon_4_salle_3 = Room("salle-lanternes", "Quelques lanternes éclairent la pièce.")

        # Niveau 5
        self.donjon_5 = Room("salle-donjon-5", "salle principale du niveau 5, le sol est glissant.")
        self.donjon_5_salle_1 = Room("salle-feu", "Des torches illuminent cette salle.")
        self.donjon_5_salle_2 = Room("salle-chaines", "Des chaînes pendent du plafond.")
        self.donjon_5_salle_3 = Room("salle-pierres", "Des pierres anciennes jonchent le sol.")

        # Boss
        self.donjon_boss = Room("salle-boss", "Une immense salle où le boss ultime vous attend !")

        #-----------------------------------------FIN Donjon -----------------------------------------------------#


        

        self.rooms = [
            # Village / maison / capital
            self.maison_haut, self.maison_bas, self.village, self.forge,
            self.magasin, self.magasin_echange, self.maison_ancien, self.foret,
            self.foret_sombre, self.route_capital, self.avant_post_capital,
            self.rue_capitale, self.guild, self.auberge, self.magasin_capital,
            self.foret_capital, self.donjon,

            # Donjon niveau 1
            self.donjon_1, self.donjon_1_chambre, self.donjon_1_tunnel, self.donjon_1_exploration,

            # Donjon niveau 2
            self.donjon_2, self.donjon_2_salle_1, self.donjon_2_salle_2, self.donjon_2_salle_3,

            # Donjon niveau 3
            self.donjon_3, self.donjon_3_salle_1, self.donjon_3_salle_2, self.donjon_3_salle_3,

            # Donjon niveau 4
            self.donjon_4, self.donjon_4_salle_1, self.donjon_4_salle_2, self.donjon_4_salle_3,

            # Donjon niveau 5
            self.donjon_5, self.donjon_5_salle_1, self.donjon_5_salle_2, self.donjon_5_salle_3,

            # Boss
            self.donjon_boss
        ]




    def _setup_items(self):
       
        # --- Armes ---
        self.épée = Item("épée", "Une épée solide, tranchante et fiable.", 2, dégâts=60, durabilité=40, type="melee", niveau_requis=1, vendable=15)
        self.arc = Item("arc", "Un arc léger pour attaquer à distance.", 2, dégâts=25, durabilité=20, type="distance", niveau_requis=1)
        self.hache = Item("hache", "Une hache lourde, inflige de gros dégâts.", 5, dégâts=75, durabilité=25, type="melee", niveau_requis=2, vendable=15)
        self.dague = Item("dague", "Petite mais rapide, avec chance de critique élevée.", 1, dégâts=45, durabilité=20, type="melee", niveau_requis=1, crit_chance=0.2)
        self.bâton = Item("bâton", "Un bâton ancien augmentant les pouvoirs magiques.", 3, dégâts=35, durabilité=50, type="melee", niveau_requis=1, magie_bonus=5)

        # --- Objets utilisables ---
        self.pomme = Item("pomme", "Une petite pomme rouge.", 0.2, heal=5, type="potion", vendable=1)
        self.orange = Item("orange", "Une orange juteuse.", 0.2, heal=5, type="potion", vendable=15)
        self.poulet = Item("poulet", "Un petit morceau de poulet rôti.", 0.5, heal=5, type="potion", vendable=15)
        self.potion_soin = Item("potion-soin", "Restaure une partie de la vie.", 0.5, heal=20, type="potion")
        self.potion_mana = Item("potion-mana", "Restaure un peu de mana.", 0.5, mana=15, type="potion")
        self.flèches = Item("flèches", "Flèches pour votre arc.", 0.1, quantité=1, type="munition")

        # --- Équipement ---
        self.armure = Item("armure", "Armure de base offrant une bonne protection.", 10, armure_phys=3, armure_mag=1)
        self.bottes = Item("bottes", "Bottes légères augmentant l'agilité.", 1.5, armure_phys=1, armure_mag=0, agilite=2, vendable=15)
        self.gants = Item("gants", "Gants renforçant vos attaques.", 0.5, armure_phys=1, armure_mag=0, attaque=2)
        self.casque = Item("casque", "Casque de protection pour la tête.", 2, armure_phys=2, armure_mag=1)

        # --- Artefacts ---
        self.anneau = Item("anneau", "Anneau donnant plus de chance de critique.", 0.1, bonus={"crit_chance": 0.1})
        self.amulette = Item("amulette", "Amulette augmentant votre agilité.", 0.2, bonus={"agilite": 2})
        self.talisman = Item("talisman", "Talisman offrant une protection équilibrée.", 0.3, bonus={"armure_phys": 2, "armure_mag": 2})

        # --- Matériaux de monstres ---
        self.oreille = Item("oreille", "Oreille récupérée sur un gobelin.", 0.1)
        self.gelée = Item("gelée", "Gelée visqueuse d'un slime.", 0.2)
        self.noyau = Item("noyau", "Noyau solide d'un golem de pierre.", 5.0)

        
        #lieu se situe l item
        self.maison_bas.inventory["pomme"] = self.pomme
        


    def _setup_characters(self):
        mere = Character(
            "mere",
            "ta mère, elle a l'air inquiète",
            self.maison_bas,
            ["Range ta chambre !", "Fais attention sur la route."],
            movable=True
        )

        ancien = Character(
        "Ancien",
        "Le sage qui vit dans l'ancienne maison",
        self.maison_ancien,
        ["La patience est une vertu.", "Les forêts cachent des secrets."],
        movable=False
    )

        # --- Commerçants ---
        marchand = Character(
            "Marchand",
            "Un marchand ambulant proposant divers objets",
            self.magasin,
            ["Bonjour ! Tu veux acheter ?", "J'ai des objets rares en stock !"],
            movable=False
        )

        forgeron = Character(
            "Forgeron",
            "Un maître forgeron qui vend et répare des armes",
            self.forge,
            ["Mes armes sont solides.", "Tu veux une arme améliorée ?"],
            movable=False
        )

        aubergiste = Character(
            "Aubergiste",
            "Tient l'auberge et propose nourriture et boissons",
            self.auberge,
            ["Bienvenue ! Un petit repas ?", "Repose-toi bie n, voyageur."],
            movable=False
        )

        # --- PNJ spéciaux / échanges ---
        mage = Character(
            "Mage",
            "Un mage qui échange des artefacts magiques",
            self.guild,
            ["Je peux t'enseigner des sorts.", "J'ai des artefacts puissants."],
            movable=False
        )
        herboriste = Character(
            "Herboriste",
            "Vendeur d'herbes et potions rares",
            self.foret,
            ["Mes potions guérissent tout.", "Je peux t'échanger des ingrédients."],
            movable=False
        )
        villageois = Character(
            "Villageois",
            "Un habitant du village qui se promène ici et là",
            self.village,
            ["Bonjour !", "Il fait beau aujourd'hui, non ?"],
            movable=False
        )



        # --- Ajouter les PNJ aux salles correspondantes ---
        self.maison_bas.characters["mere"] = mere
        self.village.characters["villageois"] = villageois
        self.maison_ancien.characters["ancien"] = ancien
        self.magasin.characters["marchand"] = marchand
        self.forge.characters["forgeron"] = forgeron
        self.auberge.characters["aubergiste"] = aubergiste
        self.guild.characters["mage"] = mage
        self.foret.characters["herboriste"] = herboriste

        # --- Liste globale pour le jeu ---
        self.characters = [mere, villageois, ancien, marchand, forgeron, aubergiste, mage, herboriste]

        # -------------------------
        # MONSTRES CLASSIQUES
        # -------------------------
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
                Item("oreille", "Une oreille de gobelin.", 0.1),
                Item("potion-soin", "Potion pour récupérer des PV.", 0.5)
            ],
            movable=False
        )

        hobelin = MonsterCharacter(
            name="hobelin",
            description="l'évolution du gobelin agressif.",
            current_room=self.foret,
            msgs=[],         
            hp=50,
            attack=8,
            attack_max=12,
            defense=4,
            loot=[
                Item("oreille", "Une oreille de gobelin.", 0.1),
                Item("potion-soin", "Potion pour récupérer des PV.", 0.5),
                Item("potion-mana", "Potion pour récupérer du mana.", 0.5)
            ],
            movable=False
        )

        slime = MonsterCharacter(
            name="slime",
            description="Une masse visqueuse gélatineuse.",
            current_room=self.donjon_1,
            msgs=[],
            hp=20,
            attack=2,
            attack_max=4,
            defense=1,
            loot=[
                Item("gelée", "Une gelée visqueuse.", 0.2),
                Item("potion-soin", "Potion pour récupérer des PV.", 0.5)
            ],
            movable=False
        )

        bandit = MonsterCharacter(
            name="bandit",
            description="Un bandit à l'air menaçant, armé d'une dague.",
            current_room=self.village,
            msgs=[],
            hp=40,
            attack=6,
            attack_max=10,
            defense=3,
            loot=[
                Item("herbe", "Une plante médicinale.", 0.3),
                Item("potion-soin", "Potion de soin basique.", 0.5)
            ],
            movable=False
        )

        # -------------------------
        # BOSS
        # -------------------------
        golem = MonsterCharacter(
            name="Golem-de-Pierre",
            description="Un golem massif de pierre, difficile à vaincre.",
            current_room=self.donjon_3_salle_2,
            msgs=[],
            hp=300,
            attack=18,
            attack_max=20,
            defense=10,
            loot=[
                Item("noyau de golem", "Noyau solide d'un golem de pierre.", 15.0),
                Item("pierre magique", "Pierre avec pouvoirs mystiques.", 8.0)
            ],
            movable=False
        )


        furie_nocturne = MonsterCharacter(
                name="furie-nocturne",
                description="Une créature mystérieuse et puissante, ses statistiques sont inconnues avant le combat.",
                current_room=self.donjon_boss,
                msgs=[],
                hp=500,
                attack=75,
                attack_max=90,
                defense=150,
                monster_type="Dragon",
                weak_to=["ice", "light"],
                resist_to=["physical", "fire"],
                crit_chance=10.0,
                speed=15,
                is_boss=True,
                loot=[
                    Item("écaille de fureur nocturne", "Écaille mystique de la Furie Nocturne.", 10.0),
                    Item("dent noire", "Dent acérée du dragon.", 5.0),
                    Item("cage de plasma", "Une cage d'énergie rare.", 2.0),
                    Item("griffe sombre", "Griffe noire et tranchante.", 1.0)
                ],
                patterns=[
                    {"name": "Souffle électrique", "type": "aoe", "dmg_mult": 1.5, "cooldown": 3},
                    {"name": "Griffes rapides", "type": "attack", "dmg_mult": 1.2, "cooldown": 1},
                    {"name": "Frappe tonitruante", "type": "attack", "dmg_mult": 2.0, "cooldown": 4,
                    "condition": lambda boss, ctx: boss.hp <= boss.hp_max * 0.5},
                    {"name": "Invisibilité", "type": "buff", "dmg_mult": 0, "cooldown": 5,
                    "condition": lambda boss, ctx: not boss.buff_active}
                ],
            movable=False
         )

        # Marque spéciale : stats inconnues pour le joueur
        furie_nocturne.hidden_lore = [
            "L'enfant illégitime entre les ombres et le tonnerre",
            "Si vous tombez dessus, priez..."
        ]

        # --- Ajouter à la liste globale des personnages/monstres ---
        self.characters.append(furie_nocturne)


        # --- Ajouter les monstres aux salles ---
        self.foret.characters["gobelin"] = gobelin
        
        
        self.donjon_1.characters["slime"] = slime
        self.donjon_3_salle_2.characters["golem"] = golem
        
        
        self.donjon_boss.characters["furie-nocturne"] = furie_nocturne

        # --- Ajouter les monstres à la liste globale du jeu ---
        self.characters += [gobelin, slime, golem,bandit,hobelin,furie_nocturne,golem]




 



    def _setup_exits(self):    #ajouter le boss 
        # Maison haut / bas
        self.maison_haut.exits = {
            "N": None, "E": None, "S": None, "O": None,
            "haut": None, "bas": self.maison_bas
        }

        self.maison_bas.exits = {
            "N": None, "E": None, "S": self.village, "O": None,
            "haut": self.maison_haut, "bas": None
        }

        # Village central
        self.village.exits = {
            "N": self.maison_bas, "E": self.foret, "S": self.maison_ancien, "O": self.magasin,
            "haut": self.forge , "bas": None
        }

                # Magasin du village
        self.forge.exits = {
            "N": None, "E": None, "S": None, "O": None,
            "haut": None, "bas": self.village
        }
        
        
        # Magasin du village
        self.magasin.exits = {
            "N": None, "E": self.village, "S": None, "O": None,
            "haut": self.magasin_echange, "bas": None
        }

        # salle d'échange au-dessus du magasin
        self.magasin_echange.exits = {
            "N": None, "E": None, "S": None, "O": None,
            "haut": None, "bas": self.magasin
        }

        # Ancienne maison (au sud du village)
        self.maison_ancien.exits = {
            "N": self.village, "E": None, "S": None, "O": None,
            "haut": None, "bas": None
        }

        # Forêt
        self.foret.exits = {
            "N": None, "E": self.foret_sombre, "S": None, "O": self.village,
            "haut": None, "bas": None
        }

        # Forêt sombre
        self.foret_sombre.exits = {
            "N": None, "E": self.route_capital, "S": None, "O": self.foret,
            "haut": None, "bas": None
        }

        # Route vers la capitale
        self.route_capital.exits = {
            "N": None, "E": self.avant_post_capital, "S": None, "O": self.foret_sombre,
            "haut": None, "bas": None
        }

        # Avant-poste
        self.avant_post_capital.exits = {
            "N": None, "E": None, "S": self.rue_capitale, "O": self.route_capital,
            "haut": None, "bas": None
        }

        # Rue principale de la capitale
        self.rue_capitale.exits = {
            "N": self.avant_post_capital, "E": self.magasin_capital,
            "S": self.foret_capital, "O": self.guild,
            "haut": None, "bas": None
        }

        # Guild
        self.guild.exits = {
            "N": None, "E": self.rue_capitale, "S": None, "O": None,
            "haut": self.auberge, "bas": None
        }

        # Auberge (étage)
        self.auberge.exits = {
            "N": None, "E": None, "S": None, "O": None,
            "haut": None, "bas": self.guild
        }

        # Magasin de la capitale
        self.magasin_capital.exits = {
            "N": None, "E": None, "S": None, "O": self.rue_capitale,
            "haut": None, "bas": None
        }

        # Forêt capitale
        self.foret_capital.exits = {
            "N": None,
            "E": None, "S": None, "O": None,
            "haut": None, "bas": None
        }

        # Daungon (sous-sol)
        self.donjon.exits = {
            "N": None, "E": None, "S": None, "O": None,
            "haut": self.rue_capitale,
            "bas": self.donjon_1
        }
        
        
        
       

        # Donjon 1
        self.donjon_1.exits = {
            "N": None, "E": self.donjon_1_chambre, "S": self.donjon_1_tunnel, "O": None,
            "haut": self.rue_capitale, "bas": self.donjon_2
        }
        self.donjon_1_chambre.exits = {"O": self.donjon_1, "E": self.donjon_1_exploration,
                                    "N": None, "S": None, "haut": None, "bas": None}
        self.donjon_1_exploration.exits = {"O": self.donjon_1_chambre,
                                        "N": None, "S": None, "E": None, "O": self.donjon_1_chambre,
                                        "haut": None, "bas": None}
        self.donjon_1_tunnel.exits = {"O": self.donjon_1, "N": None, "S": None, "E": None, "haut": None, "bas": None}

        # Donjon 2
        self.donjon_2.exits = {"N": None, "E": self.donjon_2_salle_1, "S": self.donjon_2_salle_2, "O": None,
                            "haut": self.donjon_1, "bas": self.donjon_3}
        self.donjon_2_salle_1.exits = {"O": self.donjon_2, "E": self.donjon_2_salle_3,
                                    "N": None, "S": None, "haut": None, "bas": None}
        self.donjon_2_salle_2.exits = {"O": self.donjon_2, "N": None, "S": None, "E": None, "haut": None, "bas": None}
        self.donjon_2_salle_3.exits = {"O": self.donjon_2_salle_1, "N": None, "S": None, "E": None, "haut": None, "bas": None}

        # Donjon 3
        self.donjon_3.exits = {"N": None, "E": self.donjon_3_salle_1, "S": self.donjon_3_salle_2, "O": None,
                            "haut": self.donjon_2, "bas": self.donjon_4}
        self.donjon_3_salle_1.exits = {"O": self.donjon_3, "E": self.donjon_3_salle_3,
                                    "N": None, "S": None, "haut": None, "bas": None}
        self.donjon_3_salle_2.exits = {"O": self.donjon_3, "N": None, "S": None, "E": None, "haut": None, "bas": None}
        self.donjon_3_salle_3.exits = {"O": self.donjon_3_salle_1, "N": None, "S": None, "E": None, "haut": None, "bas": None}

        # Donjon 4
        self.donjon_4.exits = {"N": None, "E": self.donjon_4_salle_1, "S": self.donjon_4_salle_2, "O": None,
                            "haut": self.donjon_3, "bas": self.donjon_5}
        self.donjon_4_salle_1.exits = {"O": self.donjon_4, "E": self.donjon_4_salle_3,
                                    "N": None, "S": None, "haut": None, "bas": None}
        self.donjon_4_salle_2.exits = {"O": self.donjon_4, "N": None, "S": None, "E": None, "haut": None, "bas": None}
        self.donjon_4_salle_3.exits = {"O": self.donjon_4_salle_1, "N": None, "S": None, "E": None, "haut": None, "bas": None}

        # Donjon 5
        self.donjon_5.exits = {"N": None, "E": self.donjon_5_salle_1, "S": self.donjon_5_salle_2, "O": None,
                            "haut": self.donjon_4, "bas": self.donjon_boss}
        self.donjon_5_salle_1.exits = {"O": self.donjon_5, "E": self.donjon_5_salle_3,
                                    "N": None, "S": None, "haut": None, "bas": None}
        self.donjon_5_salle_2.exits = {"O": self.donjon_5, "N": None, "S": None, "E": None, "haut": None, "bas": None}
        self.donjon_5_salle_3.exits = {"O": self.donjon_5_salle_1, "bas": self.donjon_boss,
                                    "N": None, "S": None, "E": None, "haut": None}

        
        self.donjon_boss.exits = {
            "O": None ,  
            "N": None,
            "S": None,
            "E": None,
            "haut": None,
            "bas": None
        }

                
        
   # if  boss.hp == 0 :  
    #    self.donjon_boss.exits["O"] = self.donjon_10  # Active la sortie si boss battue
     #   print(f"La sortie O de {donjon_boss.exits} est maintenant accessible !")

      
        
        
        
        

    def _register_directions(self):
        for room in self.rooms:
            for direction in room.exits.keys():
                Room.register_direction(direction)

    def _setup_player(self):
        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = self.maison_haut
       
    def get_room_by_name(self, room_name):
        room_name = room_name.lower().replace("-", "_")

        for room in self.rooms:
            if room.name.lower().replace("-", "_") == room_name:
                return room

        return None

       
        
    def _setup_quests(self):
        
        
        
         #####################################                   ###############################################

        #####################################            QUETES ###############################################
        
         #####################################                   ###############################################

        quete_mere = Quest(
            title="Parler à maman",
            description="Va parler à ta mère au rez-de-chaussée.",
            objectives=["parler avec mere"],
            reward="cookie",
        )
        self.player.quest_manager.add_quest(quete_mere)

        quete_lieu = Quest(
            title="Chez l'ancien",
            description="un crane tout lisse plein de savoir  ", 
            objectives=["aller chez l'ancien"],
            reward="lait",
        )
        self.player.quest_manager.add_quest(quete_lieu)


        quete_objet = Quest(
            title="obtenir la pomme",
            description="Va chercher la pomme de la mère",
            objectives=["obtenir la pomme"],
            reward="cookie",
        )
        self.player.quest_manager.add_quest(quete_objet)        
        
        
        
        quete_gobelin = Quest(
            title="Nettoyage de la forêt",
            description="Des gobelins attaquent les voyageurs près de la forêt. Élimine-en un.",
            objectives=["tuer gobelin"],
            reward="potion-soin"
        )
        self.player.quest_manager.add_quest(quete_gobelin)

        quete_slime = Quest(
            title="Menace visqueuse",
            description="Une créature étrange bloque l'accès du donjon. Débarrasse-toi du slime.",
            objectives=["tuer slime"],
            reward="épée"
        )
        self.player.quest_manager.add_quest(quete_slime)

        quete_bandit = Quest(
            title="Le bandit du village",
            description="Un bandit terrorise les habitants du village. Il faut l'arrêter.",
            objectives=["tuer bandit"],
            reward="armure"
        )
        self.player.quest_manager.add_quest(quete_bandit)

        quete_golem = Quest(
            title="Le cœur de pierre",
            description="Un golem ancien garde une salle du donjon. Détruis-le et récupère son noyau.",
            objectives=["tuer Golem-de-Pierre"],
            reward="noyau"
        )
        self.player.quest_manager.add_quest(quete_golem)

                
        quete_furie = Quest(
            title="La Furie Nocturne",
            description="Une créature légendaire hante les profondeurs du donjon. Mets fin à son règne.",
            objectives=["tuer furie-nocturne"],
            reward="écaille de fureur nocturne"
        )
        self.player.quest_manager.add_quest(quete_furie)

        quete_donjon = Quest(
            title="Dans les profondeurs",
            description="Entre dans le donjon et explore sa première salle.",
            objectives=["aller salle-donjon-1"],
            reward="potion-mana"
        )
        self.player.quest_manager.add_quest(quete_donjon)

        
        
        
        
        
        #####################################                   ###############################################

        #####################################            QUETES ###############################################
        
         #####################################                   ###############################################
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

    def update_characters(self):
        """
        Met à jour la position des PNJ mobiles à chaque tour de jeu.
        """
        for c in self.characters:
            moved = c.move()
            if DEBUG and moved:
                print(f"DEBUG: {c.name} s'est déplacé dans {c.current_room.name}")


    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # On lit la commande du joueur
            self.process_command(input("> "))
            self.check_game_over()
        return None


    def check_game_over(self):
        if self.player.hp <= 0 and not self.finished:
            self.game_over()
            
    def game_over(self):
        print("\n💀 GAME OVER 💀")
        print("Votre aventure s'arrête ici.\n")
        self.finished = True







    # Process the command entered by the player
    def process_command(self, command_string) -> None:
        
        if not command_string:
            print()
            return

        # Split the command string into a list of words
        list_of_words = command_string.split(" ")

        command_word = list_of_words[0]

        # If the command is not recognized, print an error message
        if command_word not in self.commands.keys():
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")
        # If the command is recognized, execute it
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)

    # Print the welcome message
    def print_welcome(self):
        print(f"\nBienvenue {self.player.name} dans ce jeu d'aventure !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        print(self.player.current_room.get_long_description())
    
    
    def check_end_game(self):
        """
        Vérifie si toutes les quêtes sont terminées.
        Si oui, termine le jeu avec un message.
        """
        if self.player.quest_manager.all_quests_completed():
            print("\n Félicitations ! Tu as terminé toutes les quêtes !")
            print(" Tu as gagné le jeu !\n")
            self.finished = True

def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()
