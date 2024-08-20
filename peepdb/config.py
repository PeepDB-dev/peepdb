import os
import json
from cryptography.fernet import Fernet

CONFIG_DIR = os.path.expanduser("~/.peepdb")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
KEY_FILE = os.path.join(CONFIG_DIR, "key.key")

def get_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
    else:
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
    return key

def encrypt(message: str) -> str:
    return Fernet(get_key()).encrypt(message.encode()).decode()

def decrypt(token: str) -> str:
    return Fernet(get_key()).decrypt(token.encode()).decode()

def save_connection(db_type, host, user, password, database):
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    config = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)

    config[db_type] = {
        "host": encrypt(host),
        "user": encrypt(user),
        "password": encrypt(password),
        "database": encrypt(database)
    }

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

def get_connection(db_type):
    if not os.path.exists(CONFIG_FILE):
        return None

    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)

    if db_type not in config:
        return None

    conn = config[db_type]
    return (
        decrypt(conn["host"]),
        decrypt(conn["user"]),
        decrypt(conn["password"]),
        decrypt(conn["database"])
    )

def list_connections():
    if not os.path.exists(CONFIG_FILE):
        print("No saved connections.")
        return

    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)

    print("Saved connections:")
    for db_type in config.keys():
        print(f"- {db_type}")