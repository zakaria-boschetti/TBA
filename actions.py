 # Description: The actions module.

from room import Room
from item import Item
from player import Player
from character import *
from character import MonsterCharacter

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
        player = game.player
        l = len(list_of_words)

        if l != number_of_parameters + 1:
            print(MSG1.format(command_word=list_of_words[0]))
            return False

        direction = list_of_words[1]

        # --- BLOQUER L'ACCÈS À LA FORÊT TANT QUE LA QUÊTE "parler au chef" N'EST PAS FINIE ---
        current_room = player.current_room

        # Récupère la salle cible via les sorties
        target_room = None
        if hasattr(current_room, "exits") and direction in current_room.exits:
            target_room = current_room.exits[direction]

        if target_room and getattr(target_room, "name", "").lower() == "foret":
            qm = getattr(player, "quest_manager", None)

            def quest_done(title_like: str) -> bool:
                """Retourne True si une quête dont le titre contient title_like est terminée."""
                if not qm:
                    return False
                for q in getattr(qm, "quests", []):
                    title = str(getattr(q, "title", getattr(q, "name", ""))).lower()
                    if title_like in title:
                        # plusieurs compatibilités possibles
                        if getattr(q, "completed", False) is True:
                            return True
                        if getattr(q, "is_completed", False) is True:
                            return True
                        status = str(getattr(q, "status", "")).lower()
                        if status in ("done", "completed", "terminée", "terminee", "validée", "validee"):
                            return True
                return False

            # Ici on cherche une quête dont le titre contient "chef" ou "parler au chef"
            if not quest_done("Rencontrer l'ancien") and not quest_done("ancien"):
                print("\n🚫 Accès à la forêt verrouillé : tu dois d'abord valider la quête 'Parler au chef'.\n")
                return False

        # Marchand refuse le retour en arrière
        if getattr(game, "following_npc", None) is not None:
            # si tu utilises l'historique du player :
            if hasattr(player, "history") and player.history:
                previous_room = player.history[-1]
                current_room = player.current_room
                target_room = getattr(current_room, "exits", {}).get(direction)
                if target_room is previous_room:
                    print("\n Le marchand refuse de faire demi-tour. Continue vers la capitale.\n")
                    return False
        

        success = player.move(direction) 
        
        
        # ---------------------------
        # ESCORTE : déplacer le PNJ APRÈS le déplacement du joueur
        # ---------------------------
        if success and getattr(game, "following_npc", None) is not None and not getattr(game, "marchand_removed", False):
            npc = game.following_npc
            npc_key = getattr(npc, "name", "npc").lower()

            old_room = getattr(npc, "current_room", None)
            new_room = game.player.current_room

            # retirer de l'ancienne salle
            if old_room is not None and hasattr(old_room, "characters"):
                old_room.characters.pop(npc_key, None)

            # placer dans la nouvelle salle
            npc.current_room = new_room
            if hasattr(new_room, "characters"):
                new_room.characters[npc_key] = npc

        # --- STOP escorte quand on atteint l'avant-poste ---
        if success and getattr(game, "following_npc", None) is not None:
            if game.player.current_room and game.player.current_room.name == "avant_post_capitale":
                npc = game.following_npc
                npc_key = getattr(npc, "name", "npc").lower()

                # il reste à l'avant-poste, mais ne suit plus
                game.following_npc = None

                print("\n Le marchand ambulant : 'Merci ! À partir d'ici je suis en sécurité. Au revoir !'\n")

                # flag pour dire qu'il est "posé" à l'avant-poste
                game.marchand_waiting_at_avantpost = True


        # --- Disparition du marchand quand tu quittes l'avant-poste vers la capitale ---
        if success and getattr(game, "marchand_waiting_at_avantpost", False):
            if game.player.current_room and game.player.current_room.name == "rue_capitale":
                # on le retire de l'avant-poste (il ne doit plus apparaître ensuite)
                try:
                    game.avant_post_capitale.characters.pop("marchand_ambulant", None)
                except Exception:
                    pass

                game.marchand_waiting_at_avantpost = False
                game.marchand_removed = True


        if success:
            game.update_characters()

            if hasattr(player, "quest_manager") and player.quest_manager is not None:
                try:
                    player.quest_manager.check_action_objectives("aller", player.current_room.name)
                except Exception as e:
                    print(f"\n[ERREUR Quêtes] check_action_objectives(aller, {player.current_room.name}) -> {e}\n")


            game.check_end_game()

        return success

    @staticmethod
    def back(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False
        return game.player.back()

    @staticmethod
    def history(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False

        player = game.player
        if hasattr(player, "get_history"):
            print(player.get_history())
        else:
            if not getattr(player, "history", []):
                print("\nAucun historique.\n")
            else:
                print("\nHistorique :")
                for r in player.history:
                    print(f"  - {r.name}")
                print()
        return True

    @staticmethod
    def look(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False

        room = game.player.current_room

        # Description + sorties
        print(room.get_long_description())

        # Objets
        if hasattr(room, "get_inventory"):
            print(room.get_inventory())
        else:
            inv = getattr(room, "inventory", {})
            if not inv:
                print("\nIl n'y a rien ici.\n")
            else:
                print("\nLa pièce contient :")
                for it in inv.values():
                    print(f"    - {it}")
                print()

        # Personnages / monstres
        chars = getattr(room, "characters", {})
        if chars:
            pnjs = []
            monstres = []
            for c in chars.values():
                if isinstance(c, MonsterCharacter):
                    monstres.append(c)
                else:
                    pnjs.append(c)

            if pnjs:
                print("\nPersonnages présents :")
                for c in pnjs:
                    print(f"    - {c}")
                print()

            if monstres:
                print("\nMonstres présents :")
                for m in monstres:
                    print(f"    - {m.name} : {m.description}")
                print()

        return True


    @staticmethod
    def take(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG1.format(command_word=list_of_words[0]))
            return False

        item_name = list_of_words[1]
        player = game.player
        room = player.current_room

        if item_name not in room.inventory:
            print(f"\nL'objet '{item_name}' n'est pas dans la pièce.\n")
            return False

        item = room.inventory[item_name]

        if player.get_current_weight() + item.weight > player.max_weight:
            print(f"\nVous ne pouvez pas prendre l'objet '{item_name}' : poids maximal atteint.\n")
            return False

        ok = player.add_item(item)
        if not ok:
            return False

        del room.inventory[item_name]
        print(f"\nVous avez pris l'objet '{item_name}'.\n")

        print(f"\nVous avez pris l'objet '{item_name}'.\n")

        if hasattr(player, "quest_manager") and player.quest_manager is not None:
            player.quest_manager.check_action_objectives("obtenir", item.name)

        game.check_end_game()
        return True

    @staticmethod
    def drop(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG1.format(command_word=list_of_words[0]))
            return False

        item_name = list_of_words[1]
        player = game.player
        room = player.current_room

        if item_name not in player.inventory:
            print(f"\nL'objet '{item_name}' n'est pas dans l'inventaire.\n")
            return False

        item = player.inventory[item_name]
        room.inventory[item_name] = item
        del player.inventory[item_name]

        print(f"\nVous avez déposé l'objet '{item_name}'.\n")
        return True

    @staticmethod
    def check(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False

        player = game.player
        if hasattr(player, "get_inventory"):
            print(player.get_inventory())
        else:
            print("\n" + player.list_inventory() + "\n")
        return True

    @staticmethod
    def talk(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG1.format(command_word=list_of_words[0]))
            return False

        npc_key = list_of_words[1].lower()
        room = game.player.current_room

        char = room.characters.get(npc_key)

        # Alias : si le joueur tape "marchand" dans la forêt, on vise le marchand escorté
        if not char and npc_key == "marchand":
            char = room.characters.get("marchand_ambulant")
            if char:
                npc_key = "marchand_ambulant"


        if not char:
            print(f"\nIl n'y a pas de personnage nommé '{npc_key}' ici.\n")
            return False


        # 100% GUI
        if not getattr(game, "gui", None):
            print("\nLe dialogue est disponible uniquement en interface graphique.\n")
            return True

        dlg = getattr(game, "dialogues", {}).get(npc_key)

        # ---------------------------
        # CAS : LE MARCHAND AMBULANT ======
        # ---------------------------

        if npc_key == "marchand_ambulant":
            room = game.player.current_room

            # Valider l'objectif "parler marchand_ambulant" dès qu'on lui parle
            if getattr(game.player, "quest_manager", None):
                try:
                    game.player.quest_manager.check_action_objectives("parler", npc_key)
                except Exception as e:
                    print(f"\n[ERREUR Quêtes] check_action_objectives(parler, {npc_key}) -> {e}\n")


            # 1) Tant que les squelettes sont vivants
            squelettes_obj = room.characters.get("squelettes")
            squelettes_en_vie = (
                isinstance(squelettes_obj, MonsterCharacter)
                and getattr(squelettes_obj, "is_alive", lambda: True)()
            )
            if squelettes_en_vie:
                # GUI dialogue simple
                game.gui.open_npc_dialogue(
                    portrait_key="marchand_ambulant" if "marchand_ambulant" in game.gui.npc_images else "villageois",
                    title_line="MARCHAND :",
                    first_message=(
                        "Ces squelettes vont me tuer !\n"
                        "S'il te plaît, débarrasse-t'en d'abord !"
                    ),
                    choices=["(Je vais les combattre)", "(D'accord)", "(Fermer)"],
                    replies=["Vite !", "Merci !", ""],
                )
                return True

            # 2) Les squelettes sont morts => on active l'escorte si pas déjà
            if getattr(char, "talked", False) and game.following_npc is not None:
                game.gui.open_npc_dialogue(
                    portrait_key="marchand_ambulant" if "marchand_ambulant" in game.gui.npc_images else "villageois",
                    title_line="MARCHAND :",
                    first_message=(
                        "Tant que tu marches vers la capitale, je reste derrière toi.\n"
                        "Je ne fais pas demi-tour, d'accord ?"
                    ),
                    choices=["(OK)", "(Fermer)", "(Fermer)"],
                    replies=["Parfait.", "", ""],
                )
                return True

            # Premier vrai dialogue après l'avoir sauvé
            game.gui.open_npc_dialogue(
                portrait_key="marchand_ambulant" if "marchand_ambulant" in game.gui.npc_images else "villageois",
                title_line="MARCHAND :",
                first_message=(
                    "Tu m'as sauvé la vie.\n"
                    "Je vais à la capitale.\n"
                    "Je peux t'y suivre, mais je ne reviendrai pas en arrière pour toi."
                ),
                choices=["(Allons-y)", "(Je réfléchis)", "(Fermer)"],
                replies=["Je te suis !", "Ne tarde pas.", ""],
            )

            if game.following_npc is None:
                game.following_npc = char
                game.saved_merchant = True

            char.talked = True
            return True

        # ---------------------------
        # CAS : marchand boutique
        # ---------------------------
        if dlg and dlg.get("open_shop"):
            game.gui.open_shop_window(char)
            return True
        
        if npc_key == "marchand":
            game.gui.open_shop_window(char)
            return True
        # ---------------------------
        # CAS : échange
        # ---------------------------
        if dlg and dlg.get("open_exchange"):
            game.gui.open_exchange_window(char)
            return True

        # ---------------------------
        # CAS : GARDE DU VILLAGE
        # ---------------------------
        if npc_key == "guard_village":
            if not dlg:
                print("\nDialogue du garde manquant dans game.dialogues.\n")
                return True

            # L'Ancien est dans maison_ancien (pas dans la salle du garde)
            ancien_obj = None
            try:
                ancien_obj = game.maison_ancien.characters.get("ancien")
            except Exception:
                ancien_obj = None

            has_spoken_to_ancien = bool(ancien_obj and getattr(ancien_obj, "talked", False))

            if not has_spoken_to_ancien:
                # répétition
                if getattr(char, "pre_ancien_done", False):
                    game.gui.open_npc_dialogue(
                        portrait_key=dlg.get("portrait_key", "villageois"),
                        title_line=dlg["title"],
                        first_message=dlg["pre_repeat_text"],
                        choices=["(Fermer)", "(Fermer)", "(Fermer)"],
                        replies=["", "", ""],
                    )
                    return True

                # première cinématique pré-ancien
                char.pre_ancien_done = True
                game.gui.open_npc_dialogue(
                    portrait_key=dlg.get("portrait_key", "villageois"),
                    title_line=dlg["title"],
                    first_message=dlg["pre_first"],
                    choices=dlg["pre_choices"],
                    replies=dlg["pre_replies"],
                )
                return True

            else:
                # répétition post-ancien
                if getattr(char, "post_ancien_done", False):
                    game.gui.open_npc_dialogue(
                        portrait_key=dlg.get("portrait_key", "villageois"),
                        title_line=dlg["title"],
                        first_message=dlg["post_repeat_text"],
                        choices=["(Fermer)", "(Fermer)", "(Fermer)"],
                        replies=["", "", ""],
                    )
                    return True

                # première cinématique post-ancien
                char.post_ancien_done = True
                game.gui.open_npc_dialogue(
                    portrait_key=dlg.get("portrait_key", "villageois"),
                    title_line=dlg["title"],
                    first_message=dlg["post_first"],
                    choices=dlg["post_choices"],
                    replies=dlg["post_replies"],
                )
                return True

        # ---------------------------
        # CAS : dialogues scénarisés (mère, ancien, etc.)
        # ---------------------------
        if dlg:
            # repeat si déjà parlé
            if getattr(char, "talked", False):
                game.gui.open_npc_dialogue(
                    portrait_key=dlg.get("portrait_key", npc_key),
                    title_line=dlg.get("title", f"{char.name.upper()} :"),
                    first_message=dlg.get("repeat_text", "..."),
                    choices=["(Fermer)", "(Fermer)", "(Fermer)"],
                    replies=["", "", ""],
                )
                return True

            # premier dialogue
            game.gui.open_npc_dialogue(
                portrait_key=dlg.get("portrait_key", npc_key),
                title_line=dlg["title"],
                first_message=dlg["first"],
                choices=dlg["choices"],
                replies=dlg["replies"],
            )
            char.talked = True

            if getattr(game.player, "quest_manager", None):
                try:
                    game.player.quest_manager.check_action_objectives("parler", npc_key)
                except Exception as e:
                    print(f"\n[ERREUR Quêtes] check_action_objectives(parler, {npc_key}) -> {e}\n")


            game.check_end_game()
            return True

        # ---------------------------
        # FALLBACK : PNJ sans dialogue scénarisé
        # ---------------------------
        if callable(getattr(char, "get_msg", None)):
            simple_text = char.get_msg()
        else:
            simple_text = char.description

        game.gui.open_npc_dialogue(
            portrait_key=npc_key if npc_key in game.gui.npc_images else "villageois",
            title_line=f"{char.name.upper()} :",
            first_message=simple_text,
            choices=["(Fermer)", "(Fermer)", "(Fermer)"],
            replies=["", "", ""],
        )

        if getattr(game.player, "quest_manager", None):
            game.player.quest_manager.check_action_objectives("parler", npc_key)

        game.check_end_game()
        return True



    @staticmethod
    def quests(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False

        qm = getattr(game.player, "quest_manager", None)
        if qm is None:
            print("\nAucune quête.\n")
            return True

        if hasattr(qm, "show_quests"):
            qm.show_quests()
        else:
            qm.list_quests()
        return True

    @staticmethod
    def quest(game, list_of_words, number_of_parameters):
        if len(list_of_words) < number_of_parameters + 1:
            print(MSG1.format(command_word=list_of_words[0]))
            return False

        quest_title = " ".join(list_of_words[1:])
        qm = getattr(game.player, "quest_manager", None)
        if qm is None:
            print("\nAucune quête.\n")
            return True

        if hasattr(qm, "show_quest_details"):
            current_counts = {"Se déplacer": getattr(game.player, "move_count", 0)}
            qm.show_quest_details(quest_title, current_counts)
        else:
            qm.show_details(quest_title)
        return True

    @staticmethod
    def activate(game, list_of_words, number_of_parameters):
        if len(list_of_words) < number_of_parameters + 1:
            print(MSG1.format(command_word=list_of_words[0]))
            return False

        quest_title = " ".join(list_of_words[1:])
        qm = getattr(game.player, "quest_manager", None)
        if qm is None:
            print("\nAucune quête.\n")
            return False

        if hasattr(qm, "activate_quest"):
            ok = qm.activate_quest(quest_title)
        else:
            ok = qm.activate(quest_title)
        return bool(ok)

    @staticmethod
    def rewards(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False
        game.player.show_rewards()
        return True

    @staticmethod
    def quit(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False
        player = game.player
        print(f"\nMerci {player.name} d'avoir joué. Au revoir.\n")
        game.finished = True
        return True

    @staticmethod
    def help(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False

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

        print(f"\nVous engagez le combat contre {monster.name}.\n")

        if getattr(game, "gui", None):
            game.gui.open_combat_window(monster)
            return True


            game.check_end_game()

        return True

    @staticmethod
    def activateall(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False

        qm = getattr(game.player, "quest_manager", None)
        if qm is None:
            print("\nAucune quête.\n")
            return True

        quests = getattr(qm, "quests", [])
        if not quests:
            print("\nAucune quête.\n")
            return True

        activated = 0
        for q in quests:
            title = getattr(q, "title", getattr(q, "name", None))
            if not title:
                continue
            # essaie d'activer avec la méthode qui existe
            if hasattr(qm, "activate_quest"):
                ok = qm.activate_quest(str(title))
            elif hasattr(qm, "activate"):
                ok = qm.activate(str(title))
            else:
                # fallback : si tu stockes un flag
                if hasattr(q, "active"):
                    q.active = True
                    ok = True
                elif hasattr(q, "is_active"):
                    q.is_active = True
                    ok = True
                else:
                    ok = False

            if ok:
                activated += 1

        print(f"\n✅ Quêtes activées : {activated}/{len(quests)}\n")
        return True

    @staticmethod
    def teleport(game, list_of_words, number_of_parameters):
        if len(list_of_words) < 2:
            print("Usage : teleport <salle> ou teleport <entité> <salle>")
            return False

        # Déterminer l'entité et la salle cible
        if len(list_of_words) == 2:
            entity = game.player
            target_room_name = list_of_words[1]
        else:
            entity_key = list_of_words[1].lower()
            target_room_name = list_of_words[2]

            room = game.player.current_room
            entity = room.characters.get(entity_key)

            # Si pas trouvé par clé, chercher par nom (au cas où la clé diffère)
            if entity is None:
                for c in room.characters.values():
                    if getattr(c, "name", "").lower() == entity_key:
                        entity = c
                        break

            if entity is None:
                print(f"Il n'y a pas de monstre ou PNJ nommé '{entity_key}' ici.")
                return False

        target_room = game.get_room_by_name(target_room_name)
        if not target_room:
            print(f"La salle '{target_room_name}' n'existe pas.")
            return False

        # Retirer de l'ancienne salle si l'entité y est enregistrée
        old_room = getattr(entity, "current_room", None)
        if old_room is not None and hasattr(old_room, "characters"):
            key = getattr(entity, "name", "").lower()
            if key in old_room.characters and old_room.characters[key] is entity:
                del old_room.characters[key]
            else:
                # sécurité : si la clé est différente, supprimer la bonne entrée
                for k, v in list(old_room.characters.items()):
                    if v is entity:
                        del old_room.characters[k]
                        break

        # Cas spécial joueur : mettre à jour l'historique
        if entity is game.player:
            if game.player.current_room is not None:
                game.player.history.append(game.player.current_room)

        # Déplacement
        entity.current_room = target_room
        if hasattr(target_room, "characters"):
            target_room.characters[getattr(entity, "name", "").lower()] = entity

        # Message
        if old_room is not None:
            print(f"{getattr(entity, 'name', 'Entité')} a été téléporté de {old_room.name} à {target_room.name} !")
        else:
            print(f"{getattr(entity, 'name', 'Entité')} a été téléporté vers {target_room.name} !")

        return True
