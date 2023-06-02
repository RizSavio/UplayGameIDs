import logging
import os
import platform
import sys

if platform.system() == 'Windows':
    import winreg
else:
    logging.error("This code is intended for Windows operating systems only.")
    sys.exit(1)


def get_uplay_game_ids():
    try:
        with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as base_reg:
            sub_key_path = r"SOFTWARE\WOW6432Node\Ubisoft\Launcher\Installs"

            with winreg.OpenKey(base_reg, sub_key_path, 0, winreg.KEY_READ) as sub_key:
                num_sub_keys, num_values, _ = winreg.QueryInfoKey(sub_key)
                game_names = []  # List to store game names

                for i in range(num_sub_keys):
                    try:
                        game_id = winreg.EnumKey(sub_key, i)
                        game_name_key_path = os.path.join(sub_key_path, game_id)

                        with winreg.OpenKey(base_reg, game_name_key_path, 0, winreg.KEY_READ) as game_name_key:
                            _, name, _ = winreg.EnumValue(game_name_key, 1)

                        game_path = os.path.dirname(name)
                        game_name = os.path.basename(game_path)

                        # Add combined game name and ID to the list
                        combined_name_id = f"Game: {game_name} - ID: {game_id}\n\tURL Scheme Handler (Shortcut): " \
                                           f"\t\tuplay://launch/{game_id}/0\n"

                        print(combined_name_id)
                        logging.info(combined_name_id)
                        game_names.append(combined_name_id)

                    except OSError as e:
                        logging.error("Error while processing game ID:", e)

        game_names.sort()  # Sort the game_names list alphabetically

        # Export the list of game names and IDs to a text file in the current working directory
        export_game_names(game_names)

    except Exception as e:
        logging.error("Error accessing the Windows Registry:", e)


def export_game_names(game_names, file_path="UplayGameIDs.txt"):
    try:
        with open(file_path, "w") as file:
            for game_name_id in game_names:
                file.write(game_name_id + "\n")

        logging.info(f"UplayGameIDs exported to {file_path}")

    except Exception as e:
        logging.error("Error exporting game names:", e)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w',
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # Call the function to execute the code
    get_uplay_game_ids()
    os.system("pause")
