# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions

class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
    
    # Setup the game
    def setup(self):

        # Setup commands

        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        # On met à jour juste le texte d'aide pour inclure haut/bas
        go = Command(
            "go",
            " <direction> : se déplacer (N, S, E, O, haut, bas)",
            Actions.go,
            1
        )
        self.commands["go"] = go
        
        # =======================
        #   Setup rooms
        # =======================

        maison_haut = Room("maison-haut", "à l'étage de ta maison.")
        maison_bas = Room("maison-bas", "au rez-de-chaussée de ta maison.")
        village = Room("village", "sur la place du village.")
        magasin = Room("magasin", "dans le petit magasin du village.")
        magasin_echange = Room("magasin-echange", "à l'étage du magasin, dans la salle d'échange.")
        maison_ancien = Room("maison-ancien", "devant l’ancienne maison en bas du village.")
        foret = Room("foret", "à l'entrée de la forêt.")
        foret_sombre = Room("foret-sombre", "dans une partie sombre de la forêt.")
        route_capital = Room("route-capital", "sur la route menant à la capitale.")
        avant_post_capital = Room(
            "avant-post-capital",
            "à l'avant-poste qui garde l'entrée de la capitale."
        )
        rue_capitale = Room(
            "rue-capitale",
            "dans la grande rue principale de la capitale."
        )
        guild = Room("guild", "dans la guilde des aventuriers.")
        auberge = Room("auberge", "dans les étages de l'auberge de la capitale.")
        magasin_capital = Room("magasin-capital", "dans le grand magasin de la capitale.")
        foret_capital = Room("foret-capital", "dans la grande forêt au sud de la capitale.")
        daungon = Room("daungon", "dans les sous-sols sombres de la capitale.")

        # On les ajoute dans self.rooms
        self.rooms = [
            maison_haut,
            maison_bas,
            village,
            magasin,
            magasin_echange,
            maison_ancien,
            foret,
            foret_sombre,
            route_capital,
            avant_post_capital,
            rue_capitale,
            guild,
            auberge,
            magasin_capital,
            foret_capital,
            daungon,
        ]

        # =========================
        #   Create exits for rooms
        # =========================

        # Maison haut / bas
        maison_haut.exits = {
            "N": None, "E": None, "S": None, "O": None,
            "haut": None, "bas": maison_bas
        }

        maison_bas.exits = {
            "N": None, "E": None, "S": village, "O": None,
            "haut": maison_haut, "bas": None
        }

        # Village central
        village.exits = {
            "N": maison_bas, "E": foret, "S": maison_ancien, "O": magasin,
            "haut": None, "bas": None
        }

        # Magasin du village
        magasin.exits = {
            "N": None, "E": village, "S": None, "O": None,
            "haut": magasin_echange, "bas": None
        }

        # Salle d'échange au-dessus du magasin
        magasin_echange.exits = {
            "N": None, "E": None, "S": None, "O": None,
            "haut": None, "bas": magasin
        }

        # Ancienne maison (au sud du village)
        maison_ancien.exits = {
            "N": village, "E": None, "S": None, "O": None,
            "haut": None, "bas": None
        }

        # Forêt
        foret.exits = {
            "N": None, "E": foret_sombre, "S": None, "O": village,
            "haut": None, "bas": None
        }

        # Forêt sombre
        foret_sombre.exits = {
            "N": None, "E": route_capital, "S": None, "O": foret,
            "haut": None, "bas": None
        }

        # Route vers la capitale
        route_capital.exits = {
            "N": None, "E": avant_post_capital, "S": None, "O": foret_sombre,
            "haut": None, "bas": None
        }

        # Avant-poste
        avant_post_capital.exits = {
            "N": None, "E": None, "S": rue_capitale, "O": route_capital,
            "haut": None, "bas": None
        }

        # Rue principale de la capitale
        rue_capitale.exits = {
            "N": avant_post_capital, "E": magasin_capital,
            "S": foret_capital, "O": guild,
            "haut": None, "bas": None
        }

        # Guild
        guild.exits = {
            "N": None, "E": rue_capitale, "S": None, "O": None,
            "haut": auberge, "bas": None
        }

        # Auberge (étage)
        auberge.exits = {
            "N": None, "E": None, "S": None, "O": None,
            "haut": None, "bas": guild
        }

        # Magasin de la capitale
        magasin_capital.exits = {
            "N": None, "E": None, "S": None, "O": rue_capitale,
            "haut": None, "bas": None
        }

        # Forêt capitale
        foret_capital.exits = {
            "N": None,
            "E": None, "S": None, "O": None,
            "haut": None, "bas": None
        }

        # Daungon (sous-sol)
        daungon.exits = {
            "N": None, "E": None, "S": None, "O": None,
            "haut": rue_capitale,
            "bas": None
        }

        # =========================
        #  Enregistrer les directions valides (TP)
        # =========================

        for room in self.rooms:
            for direction in room.exits.keys():
                Room.register_direction(direction)

        # =========================
        # Setup player and starting room
        # =========================

        self.player = Player(input("\nEntrez votre nom: "))
        # On commence : à l'étage de la maison
        self.player.current_room = maison_haut

    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
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
    

def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()
