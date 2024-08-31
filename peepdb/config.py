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

def save_connection(name, db_type, host, user, password, database):
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    config = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)

    config[name] = {
        "db_type": db_type,
        "host": encrypt(host),
        "user": encrypt(user),
        "password": encrypt(password),
        "database": encrypt(database)
    }

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

def get_connection(name):
    if not os.path.exists(CONFIG_FILE):
        return None

    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)

    if name not in config:
        return None

    conn = config[name]
    return (
        conn["db_type"],
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

    if not config:
        print("No saved connections.")
        return

    print("Saved connections:")
    for name, details in config.items():
        db_type = details.get('db_type', 'Unknown')
        print(f"- {name} ({db_type})")
    
def remove_connection(name):
    if not os.path.exists(CONFIG_FILE):
        return False

    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)

    if name not in config:
        return False

    del config[name]

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

    return True

def remove_all_connections():
    if not os.path.exists(CONFIG_FILE):
        return 0

    count = 0
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            count = len(config)

        os.remove(CONFIG_FILE)
    except FileNotFoundError:
        # File was deleted between check and remove
        pass
    except json.JSONDecodeError:
        # File exists but is not valid JSON
        os.remove(CONFIG_FILE)
    
    return count