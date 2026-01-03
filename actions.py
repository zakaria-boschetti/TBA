 # Description: The actions module.

from room import Room
from item import Item
from player import Player
from character import *

# The actions module contains the functions that are called when a command is executed.
# Each function takes 3 parameters:
# - game: the game object
# - list_of_words: the list of words in the command
# - number_of_parameters: the number of parameters expected by the command
# The functions return True if the command was executed successfully, False otherwise.
# The functions print an error message if the number of parameters is incorrect.
# The error message is different depending on the number of parameters expected by the command.


# The error message is stored in the MSG0 and MSG1 variables and formatted with the command_word variable, the first word in the command.
# The MSG0 variable is used when the command does not take any parameter.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
# The MSG1 variable is used when the command takes 1 parameter.
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

class Actions:

    @staticmethod
    def go(game, list_of_words, number_of_parameters):
        """
        Move the player in the direction specified by the parameter.

        The parameter must correspond à une direction valide du jeu :
        - directions cardinales : N, S, E, O (ou nord, sud, est, ouest)
        - directions verticales : haut / bas (U, D, monter, descendre)

        La vérification et la normalisation de la direction sont faites
        dans Player.move / Room.normalize_direction.

        Returns:
            bool: True si le déplacement a réussi, False sinon.
        """
        
        player = game.player
        l = len(list_of_words)

        # Vérifier le nombre de paramètres
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Direction demandée
        direction = list_of_words[1]

        # On tente de déplacer le joueur
        success = player.move(direction)

        # Si le déplacement a réussi, on fait bouger les PNJ
        if success:
            game.update_characters()
            
        # Après que le joueur ait changé de pièce
        if player.current_room.name == "maison-ancien":
            game.player.quest_manager.check_action_objectives("aller", "chez l'ancien")

        game.check_end_game()

        return success

    @staticmethod
    def back(game, list_of_words, number_of_parameters):
        """
        Revient en arrière en utilisant l'historique du joueur.

        Commande : back
        Ne prend aucun paramètre.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        player = game.player
        return player.back()

    def history(game, list_of_words, number_of_parameters):
        """
        Affiche l'historique des pièces déjà visitées.

        Commande : history
        Ne prend aucun paramètre.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        player = game.player
        print(player.get_history())
        return True
    
    @staticmethod
    def look(game, list_of_words, number_of_parameters):
        """
        Affiche la description de la pièce, les items et les PNJ présents.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        room = game.player.current_room

        # Description de la pièce + sorties
        print(room.get_long_description())

        # Items dans la pièce
        print(room.get_inventory())

        # PNJ dans la pièce
        if room.characters:
            print("\nPersonnages présents :")
            for char in room.characters.values():
                print(f"    - {char}")
            print()

        return True

    @staticmethod
    def take(game, list_of_words, number_of_parameters):
        """
        Prendre un item dans la pièce et le mettre dans l'inventaire du joueur.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        item_name = list_of_words[1]
        player = game.player
        room = player.current_room

        # L'objet est-il dans la pièce ?
        if item_name not in room.inventory:
            print(f"\nL'objet '{item_name}' n'est pas dans la pièce.\n")
            return False

        item = room.inventory[item_name]

        # Vérifier la limite de poids
        if player.get_current_weight() + item.weight > player.max_weight:
            print(f"\nVous ne pouvez pas prendre l'objet '{item_name}' : poids maximal atteint.\n")
            return False

        # Déplacer l'objet de la pièce vers l'inventaire du joueur
        player.inventory[item_name] = item
        del room.inventory[item_name]

        print(f"\nVous avez pris l'objet '{item_name}'.\n")
        
        if hasattr(player, "quest_manager") and player.quest_manager is not None:
            player.quest_manager.check_action_objectives("obtenir", item.name)
          
        game.check_end_game()
          
        return True

    def drop(game, list_of_words, number_of_parameters):
        """
        Déposer un item de l'inventaire dans la pièce actuelle.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        item_name = list_of_words[1]
        player = game.player
        room = player.current_room

        # L'objet est-il dans l'inventaire ?
        if item_name not in player.inventory:
            print(f"\nL'objet '{item_name}' n'est pas dans l'inventaire.\n")
            return False

        item = player.inventory[item_name]

        # Déplacer l'objet de l'inventaire vers la pièce
        room.inventory[item_name] = item
        del player.inventory[item_name]

        print(f"\nVous avez déposé l'objet '{item_name}'.\n")
        return True

    def check(game, list_of_words, number_of_parameters):
        """
        Affiche l'inventaire du joueur.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        player = game.player
        print(player.get_inventory())
        return True
    
    def talk(game, list_of_words, number_of_parameters):
        """
        Parler à un PNJ dans la pièce actuelle.

        Usage : talk <nom>
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        name = list_of_words[1].lower()
        room = game.player.current_room

        if name not in room.characters:
            print(f"\nIl n'y a pas de personnage nommé '{name}' ici.\n")
            return False

        char = room.characters[name]
        msg = char.get_msg()
        if msg:
            print(f"\n{msg}\n")
            
        if hasattr(game.player, "quest_manager") and game.player.quest_manager is not None:
            game.player.quest_manager.check_action_objectives("parler", name)
        game.check_end_game()

    
    @staticmethod
    def quests(game, list_of_words, number_of_parameters):
        """
        Show all quests and their status.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quests(game, ["quests"], 0)
        <BLANKLINE>
        📋 Liste des quêtes:
          ❓ Grand Explorateur (Non activée)
          ❓ Grand Voyageur (Non activée)
          ❓ Découvreur de Secrets (Non activée)
        <BLANKLINE>
        True
        >>> Actions.quests(game, ["quests", "param"], 0)
        <BLANKLINE>
        La commande 'quests' ne prend pas de paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Show all quests
        game.player.quest_manager.show_quests()
        return True


    @staticmethod
    def quest(game, list_of_words, number_of_parameters):
        """
        Show details about a specific quest.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quest(game, ["quest", "Grand", "Voyageur"], 1)
        <BLANKLINE>
        📋 Quête: Grand Voyageur
        📖 Déplacez-vous 10 fois entre les lieux.
        <BLANKLINE>
        Objectifs:
          ⬜ Se déplacer 10 fois (Progression: 0/10)
        <BLANKLINE>
        🎁 Récompense: Bottes de voyageur
        <BLANKLINE>
        True
        >>> Actions.quest(game, ["quest"], 1)
        <BLANKLINE>
        La commande 'quest' prend 1 seul paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])

        # Prepare current counter values to show progress
        current_counts = {
            "Se déplacer": game.player.move_count
        }

        # Show quest details
        game.player.quest_manager.show_quest_details(quest_title, current_counts)
        return True


    @staticmethod
    def activate(game, list_of_words, number_of_parameters):
        """
        Activate a specific quest.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.activate(game, ["activate", "Grand", "Voyageur"], 1) # doctest: +ELLIPSIS
        <BLANKLINE>
        🗡️  Nouvelle quête activée: Grand Voyageur
        📝 Déplacez-vous 10 fois entre les lieux.
        <BLANKLINE>
        True
        >>> Actions.activate(game, ["activate"], 1)
        <BLANKLINE>
        La commande 'activate' prend 1 seul paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])

        # Try to activate the quest
        if game.player.quest_manager.activate_quest(quest_title):
            return True

        msg1 = f"\nImpossible d'activer la quête '{quest_title}'. "
        msg2 = "Vérifiez le nom ou si elle n'est pas déjà active.\n"
        print(msg1 + msg2)
        # print(f"\nImpossible d'activer la quête '{quest_title}'. \
        #             Vérifiez le nom ou si elle n'est pas déjà active.\n")
        return False


    @staticmethod
    def rewards(game, list_of_words, number_of_parameters):
        """
        Display all rewards earned by the player.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.rewards(game, ["rewards"], 0)
        <BLANKLINE>
        🎁 Aucune récompense obtenue pour le moment.
        <BLANKLINE>
        True
        >>> Actions.rewards(game, ["rewards", "param"], 0)
        <BLANKLINE>
        La commande 'rewards' ne prend pas de paramètre.
        <BLANKLINE>
        False
        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Show all rewards
        game.player.show_rewards()
        return True



    def quit(game, list_of_words, number_of_parameters):
        """
        Quit the game.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> quit(game, ["quit"], 0)
        True
        >>> quit(game, ["quit", "N"], 0)
        False
        >>> quit(game, ["quit", "N", "E"], 0)
        False

        """
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Set the finished attribute of the game object to True.
        player = game.player
        msg = f"\nMerci {player.name} d'avoir joué. Au revoir.\n"
        print(msg)
        game.finished = True
        return True

    def help(game, list_of_words, number_of_parameters):
        """
        Print the list of available commands.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Print the list of available commands.
        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            print("\t- " + str(command))
        print()
        return True

    @staticmethod
    def fight(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG1.format(command_word=list_of_words[0]))
            return False

        player = game.player
        room = player.current_room
        monster_name = list_of_words[1].lower()

        if monster_name not in room.characters:
            print(f"\nIl n'y a pas de monstre nommé '{monster_name}' ici.\n")
            return False

        monster = room.characters[monster_name]
        if not isinstance(monster, MonsterCharacter):
            print(f"\n{monster_name} n'est pas un monstre.\n")
            return False
        print(f"\n⚔️  Vous engagez le combat contre {monster.name} !\n")

        # Combat simple : player attaque puis le monstre réplique si vivant
        dmg = monster.take_damage(player.get_attack())
        print(f"\nVous attaquez {monster.name} et infligez {dmg} dégâts.")
        print(f"{monster.name} : {monster.display_health_bar()}")

        if monster.is_alive():
            dmg = monster.attack_player(player)
            
            
        else:
            print(f"\n{monster.name} est vaincu !")
            monster.drop_loot()   # Le loot tombe dans la salle
            del room.characters[monster_name]
                

        return True
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    @staticmethod
    def teleport(self, words, number_of_parameters):
        if len(words) < 2:
            print("Usage : teleport <salle> ou teleport <entité> <salle>")
            return

        # Joueur par défaut
        if len(words) == 2:
            entity = self.player
            target_room_name = words[1]

        else:
            entity_name = words[1].lower()
            target_room_name = words[2]

            entity = self.player.current_room.characters.get(entity_name)
            if not entity:
                print(f"Il n'y a pas de monstre ou PNJ nommé '{entity_name}' ici.")
                return

        # 🔍 Recherche de la salle
        target_room = self.get_room_by_name(target_room_name)
        if not target_room:
            print(f"La salle '{target_room_name}' n'existe pas.")
            return

        # Déplacement
        old_room = entity.current_room
        key = entity.name.lower()

        if key in old_room.characters:
            del old_room.characters[key]

        entity.current_room = target_room
        target_room.characters[key] = entity

        print(f"{entity.name} a été téléporté de {old_room.name} à {target_room.name} !")
