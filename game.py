# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
from character import Character
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
        self.commands["go"] = Command(
            "go",
            " <direction> : se déplacer (N, S, E, O, haut, bas)",
            Actions.go,
            1
        )
        self.commands["back"] = Command("back", " : revenir au lieu précédent", Actions.back, 0)
        self.commands["history"] = Command("history", " : afficher l'historique des lieux visités", Actions.history, 0)
        self.commands["look"] = Command("look", " : observer la pièce", Actions.look, 0)
        self.commands["take"] = Command("take", " <objet> : prendre un objet", Actions.take, 1)
        self.commands["drop"] = Command("drop", " <objet> : déposer un objet", Actions.drop, 1)
        self.commands["check"] = Command("check", " : afficher l'inventaire", Actions.check, 0)
        self.commands["talk"] = Command("talk", " <personnage> : parler à un personnage", Actions.talk, 1)
        self.commands["quests"] = Command("quests"
                                          , " : afficher la liste des quêtes"
                                          , Actions.quests
                                          , 0)
        self.commands["quest"] = Command("quest"
                                         , " <titre> : afficher les détails d'une quête"
                                         , Actions.quest
                                         , 1)
        self.commands["activate"] = Command("activate"
                                            , " <titre> : activer une quête"
                                            , Actions.activate
                                            , 1)
        self.commands["rewards"] = Command("rewards"
                                           , " : afficher vos récompenses"
                                           , Actions.rewards
                                           , 0)

    def _setup_rooms(self):
        self.maison_haut = Room("maison-haut", "à l'étage de ta maison.")
        self.maison_bas = Room("maison-bas", "au rez-de-chaussée de ta maison.")
        self.village = Room("village", "sur la place du village.")
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
        self.daungon = Room("daungon", "dans les sous-sols sombres.")

        self.rooms = [
            self.maison_haut, self.maison_bas, self.village, self.magasin,
            self.magasin_echange, self.maison_ancien, self.foret, self.foret_sombre,
            self.route_capital, self.avant_post_capital, self.rue_capitale,
            self.guild, self.auberge, self.magasin_capital, self.foret_capital,
            self.daungon
        ]
   

    def _setup_items(self):
        pomme = Item("pomme", "une pomme bien juteuse", 1)
        self.maison_bas.inventory["pomme"] = pomme


    def _setup_characters(self):
        mere = Character(
            "mere",
            "ta mère, elle a l'air inquiète",
            self.maison_bas,
            ["Range ta chambre !", "Fais attention sur la route."]
        )

        marchand = Character(
            "marchand",
            "un marchand ambulant",
            self.magasin,
            ["Bonjour, tu veux acheter ?", "Je voyage beaucoup."]
        )

        self.maison_bas.characters["mere"] = mere
        self.magasin.characters["marchand"] = marchand
        self.characters = [marchand]


    def _setup_exits(self):   
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
            "haut": None, "bas": None
        }

        # Magasin du village
        self.magasin.exits = {
            "N": None, "E": self.village, "S": None, "O": None,
            "haut": self.magasin_echange, "bas": None
        }

        # Salle d'échange au-dessus du magasin
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
        self.daungon.exits = {
            "N": None, "E": None, "S": None, "O": None,
            "haut": self.rue_capitale,
            "bas": None
        }

    def _register_directions(self):
        for room in self.rooms:
            for direction in room.exits.keys():
                Room.register_direction(direction)

    def _setup_player(self):
        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = self.maison_haut
        
    def _setup_quests(self):
        # --- Quêtes ---

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
        return None


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
