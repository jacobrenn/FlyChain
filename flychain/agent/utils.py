from config import APP_FOLDER, OPENAI_KEY_FILE
from getpass import getpass
import os

def _write_openai_api_key():
    
    # If the folder is not created, create it
    if not os.path.exists(APP_FOLDER):
        os.makedirs(APP_FOLDER)

    # Get the key and write it to the file
    api_key = getpass('OpenAI API Key: ')
    with open(OPENAI_KEY_FILE, 'w') as f:
        f.write(api_key)

def get_openai_api_key():

    # If the key file exists, return it
    if os.path.exists(OPENAI_KEY_FILE):
        with open(OPENAI_KEY_FILE, 'r') as f:
            key = f.read().strip()
        return key
    
    # Else, write the folder and get the key
    else:
        _write_openai_api_key()
        return get_openai_api_key()
