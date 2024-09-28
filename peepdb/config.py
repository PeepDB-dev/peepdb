import base64
import json
import os
from dataclasses import dataclass
import logging

import click
import keyring
from cachetools import TTLCache, cached
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from .exceptions import InvalidPassword

@dataclass
class KeySecurity():
    KEYRING = "os-keyring"
    PASSWORD = "password"


CONFIG_DIR = os.path.expanduser("~/.peepdb")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
SECURITY_CONFIG_FILE = os.path.join(CONFIG_DIR, "security_config.json")
KEYRING_USERNAME = "PEEP_DB_KEY"
KEYRING_SERVICE_NAME = "PEEP_DB"

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
@cached(cache=TTLCache(maxsize=1024, ttl=600))
def generate_key_from_password(salt):
    password = click.prompt("Please entry the password to encrpyt/decrpty DB passwords",
                            type=str).encode('utf-8')
    salt = base64.b64decode(salt)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password)).decode("utf-8")


@cached(cache=TTLCache(maxsize=1024, ttl=600))
def fetch_key_from_keyring():
    key = keyring.get_password(KEYRING_SERVICE_NAME, KEYRING_USERNAME)
    if not key:
        key = Fernet.generate_key().decode("utf-8")
        keyring.set_password(KEYRING_SERVICE_NAME, KEYRING_USERNAME, key)
    return key


def get_key_security_config():
    security_config = {}
    if os.path.exists(SECURITY_CONFIG_FILE):
        with open(SECURITY_CONFIG_FILE, "r") as f:
            security_config = json.load(f)

    if "PEEP_DB_KEY_SECURITY" not in security_config:
        security_config = add_key_security()

    return security_config['PEEP_DB_KEY_SECURITY']


def get_key():
    key_security_config = get_key_security_config()
    if key_security_config['type'] == KeySecurity.KEYRING:
        # Fetching encryption key from keyring
        key = fetch_key_from_keyring()
    else:
        # Dynamically generating encryption key from users input
        key = generate_key_from_password(key_security_config['salt'])
    return key


def encrypt(message: str) -> str:
    return Fernet(get_key()).encrypt(message.encode()).decode()


def decrypt(token: str) -> str:
    return Fernet(get_key()).decrypt(token.encode()).decode()


def save_connection(name, db_type, host, user, password, database):
    logger.debug(f"Saving connection: {name}, {db_type}, {host}, {user}, {'*' * len(password) if password else 'None'}, {database}")
    
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    config = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)

    if db_type == 'sqlite':
        config[name] = {
            "db_type": db_type,
            "host": host,  # Store the file path directly for SQLite
            "database": database
        }
    else:
        config[name] = {
            "db_type": db_type,
            "host": encrypt(host),
            "user": encrypt(user),
            "password": encrypt(password),
            "database": encrypt(database)
        }

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)
    
    logger.debug("Connection saved successfully")


def get_connection(name):
    if not os.path.exists(CONFIG_FILE):
        return None

    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)

    if name not in config:
        return None

    conn = config[name]
    try:
        if conn["db_type"] == 'sqlite':
            return (
                conn["db_type"],
                conn["host"],  # No need to decrypt for SQLite
                "",  # Empty string for user
                "",  # Empty string for password
                conn["database"]
            )
        else:
            return (
                conn["db_type"],
                decrypt(conn["host"]),
                decrypt(conn["user"]),
                decrypt(conn["password"]),
                decrypt(conn["database"])
            )
    except InvalidToken:
        raise InvalidPassword("Password is invalid !!!")


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


def add_key_security():
    security_config = {}
    key_security = click.prompt('Specify the way you want to store your encryption key',
                                type=click.Choice([KeySecurity.KEYRING, KeySecurity.PASSWORD]))
    security_config['PEEP_DB_KEY_SECURITY'] = {"type": key_security}
    if key_security == KeySecurity.PASSWORD:
        security_config["PEEP_DB_KEY_SECURITY"]['salt'] = base64.b64encode(
            os.urandom(16)).decode('utf-8')
    with open(SECURITY_CONFIG_FILE, "w") as f:
        json.dump(security_config, f)
    return security_config
