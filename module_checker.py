try:
    import importlib
    import subprocess
    import sys
    import random
    import json
    import logging
    import shutil

    # Function to check if a given module is installed and import it if it is
    def check_module(module_name):
        print(f'Checking Module: {module_name}')
        logging.info(f'Checking Module: {module_name}')
        try:
            # Try importing the module
            importlib.import_module(module_name)
            print(f'Module {module_name} imported successfully\n')
            logging.info(f"Module {module_name} imported successfully")
            return True
        except ImportError as e:
            # If the module is not installed, attempt to install it
            result = subprocess.run(["python", "-m", "pip", "show", module_name], capture_output=True)
            if result.returncode == 0:
                # If the module is installed but not imported, log a warning
                print(f'Module {module_name} not imported, but is installed\n')
                logging.warning(f"Module {module_name} not imported, but is installed")
                return True
            else:
                # If the module is neither installed nor imported, log a warning and return False
                print(f'Module {module_name} not imported or installed\n')
                logging.warning(f"Module {module_name} not imported or installed")
                return False

    # Function to install a given module using pip
    def install_module(module_name):
        try:
            # Use pip to install the module
            subprocess.check_call(["python", "-m", "pip", "install", module_name])
            print(f'{module_name} was installed successfully\n')
            logging.info(f"{module_name} was installed successfully")
        except subprocess.CalledProcessError as e:
            # If an error occurs during installation, log an error and exit
            print(f'Failed to install {module_name}\n')
            logging.error(f"Failed to install {module_name}")
            logging.error(e)

    # Function to check if pip is installed and install it if it is not
    def check_and_install_pip():
        try:
            # Try importing pip
            import pip
            print(f'pip is already installed.\n')
            logging.info("pip is already installed.")
        except ImportError as e:
            # If pip is not installed, prompt the user to install it
            print(f'pip is already installed.\n')
            logging.info("pip is not installed.")
            user_input = input("pip is not installed. Do you want to install it? (y/n): ")
            logging.debug(f"pip is not installed. Do you want to install it? (y/n): {user_input}")
            if user_input.lower() == 'y':
                try:
                    # Use ensurepip to install pip
                    subprocess.call([sys.executable, "-m", "ensurepip"])
                    print(f'pip is already installed.\n')
                    logging.info("pip has been successfully installed.")
                except subprocess.CalledProcessError as e:
                    # If an error occurs during installation, log an error and exit
                    print(f'pip is already installed.\n')
                    logging.error("An error occurred while installing pip. Aborting.")
                    sys.exit("An error occurred while installing pip. Aborting.")
            else:
                # If the user chooses not to install pip, log an error and exit
                print(f'pip is already installed.\n')
                logging.error("pip is required to run this script. Aborting.")
                sys.exit("pip is required to run this script. Aborting.")

    # Function to load a JSON file, format it if necessary, and return the formatted data
    def format_json_file(file_path):
        retries = 0
        formatted_data = None
    
        # Retry loading the file a maximum of 3 times in case of file not found or permission errors
        while retries < 3:
            try:
                # Try to open the file and load its contents
                with open(file_path, "r") as file:
                    data = file.read()
                    # Try to correct the JSON formatting
                    formatted_data = json.loads(data)
                    logging.info(f"Successfully opened and formatted JSON file {file_path}.")
                break
            
            except (FileNotFoundError, PermissionError) as e:
                # If there is an error opening the file, log a warning and increment the retry counter
                logging.warning(f"Error opening file {file_path}: {e}")
                retries += 1
    
            except json.JSONDecodeError as e:
                # If there is an error decoding the JSON data, log a warning and increment the retry counter
                logging.warning(f"Error decoding JSON data in {file_path}: {e}")
                formatted_data = None
                retries += 1
            if retries == 3:
                # If the maximum number of retries is reached, log an error and return None
                logging.error(f"Failed to open or format JSON file {file_path} after 3 attempts.")
        return formatted_data
             
    # Function to check if a JSON file exists and load its contents
    def check_json_file(retries=0):
        file_path = "data_management\server_info.json"
        logging.info("Checking JSON file")
        # The script will only try to read the file 3 times, in case of file being missing or permission issues.
        while retries < 3:
            try:
                # Try to open the file and load its contents
                with open(file_path, "r") as file:
                    json_check = json.load(file)
                    logging.info(f"File {file_path} loaded successfully!")
                break

            except FileNotFoundError as e:
                # If the file is missing, log a warning and exit the loop
                logging.warning(f"File {file_path} is missing!: {e}")
                break

            except PermissionError as e:
                # If there is an error opening the file, log a warning and increment the retry counter
                logging.warning(f"Error opening file {file_path}: {e}")
                retries += 1

            except json.JSONDecodeError as e:
                # If there is an error decoding the JSON data, try to format the file and write the formatted data back to the file
                logging.warning(f"Error decoding JSON data in {file_path}: {e}")
                formatted_data = format_json_file(file_path)
                if formatted_data is not None:
                    with open(file_path, "w") as file:
                        json.dump(formatted_data, file, indent=4)
                        logging.info(f"Formatted JSON data written to {file_path}")
                    break
                retries += 1
        if retries == 3:
            # If the maximum number of retries is reached, log an error
            logging.error(f"Failed to open or format JSON file {file_path} after 3 attempts.")

    # set up logging to file
    logging.basicConfig(filename='logs\\console.log', level=logging.DEBUG, format='%(asctime)s (%(levelname)s) %(message)s')
    # copy the existing log file to console_prev.log
    shutil.copy2('logs\\console.log', 'logs\\console_prev.log')
    # clear the existing console.log
    open('logs\\console.log', 'w').close()

    required_version = (3, 6)

    logging.info(f'Python version: {sys.version_info}')

    if sys.version_info < required_version:
        # Check if the current Python version is at least 3.6
        logging.critical("This script requires Python version {}.{} or higher".format(*required_version))
        raise Exception("This script requires Python version {}.{} or higher".format(*required_version))

    # Check if pip is installed and install it if it is not
    try:
        import pip
        logging.info("pip is already installed.")
    except ImportError as e:
        logging.info("pip is not installed.")
        user_input = input("pip is not installed. Do you want to install it? (y/n): ")
        logging.debug(f"pip is not installed. Do you want to install it? (y/n): {user_input}")
        if user_input.lower() == 'y':
            try:
                subprocess.call([sys.executable, "-m", "ensurepip"])
                logging.info("pip has been successfully installed.")
            except subprocess.CalledProcessError as e:
                logging.error("An error occurred while installing pip. Aborting.")
                sys.exit("An error occurred while installing pip. Aborting.")
        else:
            logging.error("pip is required to run this script. Aborting.")
            sys.exit("pip is required to run this script. Aborting.")

    # List of required modules
    modules_to_check = ['python-a2s', 'mcstatus', 'requests', 'fivempy', 'samp_client', 'discord', 'fuzzywuzzy', 'matplotlib', 'configparser']

    # Loop through each module and check if it is installed
    while True:
        subprocess.call("cls" if sys.platform == "win32" else "clear", shell=True)
        all_installed = True
        for module_name in modules_to_check:
            logging.info(f'Checking Module: {module_name}')
            try:
                # Try importing the module
                importlib.import_module(module_name)
                logging.info(f"Module {module_name} imported successfully")
            except ImportError as e:
                # If the module is not installed, attempt to install it
                result = subprocess.run(["python", "-m", "pip", "show", module_name], capture_output=True)
                if result.returncode == 0:
                    # If the module is installed but not imported, log a warning
                    logging.warning(f"Module {module_name} not imported, but is installed")
                else:
                    # If the module is neither installed nor imported, log a warning and set all_installed to False
                    logging.warning(f"Module {module_name} not imported or installed")
                    all_installed = False
                    while True:
                        # If the module is not installed, prompt the user to install it
                        user_input = input(f"In order to run this script, '{module_name}' needs to be installed.\nWould you like to install it? (y/n): ")
                        if user_input.lower() == 'y' or user_input.lower() == 'yes':
                            install_module(module_name)
                            break
                        elif user_input.lower() == 'n' or user_input.lower() == 'no':
                            sys.exit()
                        else:
                            print("Please answer 'y' or 'n'")
        if all_installed:
            # If all modules are installed, check the JSON file and run the data management and Discord bot scripts
            check_json_file()
            subprocess.call(["python", "data_management\\data_manager.py"])
            subprocess.call(["python", "discord_bot\\discord_bot.py"])
            break

except KeyboardInterrupt:
    goodbye = ["Whoops, looks like you got a little trigger happy with that keyboard.", "You hit the emergency eject button! Aborting mission!", "You pressed the big red 'STOP' button! All systems shutting down.", "Goodbye cruel world! **keyboard smash**", "Well, I see you're in a hurry to leave. Bye for now!", "Goodbye cruel world!", "Going home already? Don't forget to come back!", "Just when things were getting interesting...", "Aww, come on. Can't we just keep going?", "See you soon! Or not, if you don't come back...", "It's been fun, let's do this again soon.", "Adios amigo! Or should I say, hasta la vista?", "Bye bye birdie!", "Au revoir, my friend.", "Well, this is unexpected. We'll meet again soon, I hope.", "Don't leave so soon, we were just getting started!", "Why so quick to say goodbye?", "You can run, but you can't hide from this script.", "Please come back, I promise to be more fun next time.", "Don't press that key again, I'm sensitive.", "Don't let the door hit you on the way out.", "You're breaking my heart by leaving so soon.", "Why so hasty? The fun was just beginning!"]
    x = random.randint(0, len(goodbye) - 1)

    print(f"\n\n{goodbye[x]}")
    sys.exit()