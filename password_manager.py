import base64
import copy
import json
import os
from password_generator import PasswordGenerator
from password_manager_crypto import PasswordManagerCrypto

# PasswordManager
# The PasswordManager class handles the generation, storage, and retrieval of passwords

# Class to provide main functionality of password manager (creating/removing/storing passwords)
class PasswordManager(object):
  # Constants
  _TEXT_ENCODING = "UTF-8"
  
  # Instance variables
  _passwords = []
  _path = None
  _master_password = None
  _generator = PasswordGenerator()
  _crypto = PasswordManagerCrypto()
  _saving = False
  _enc_key = None
  _salt = None
  
  # Constructor
  # vault_path is the path of the file containing the password vault (created if nonexistant)
  # master_password is the master password associated with the vault (used to generate key if vault is nonexistant)
  def __init__(self, vault_path=None, master_password=None):
    if not vault_path == None and not len(vault_path) == 0 and not master_password == None and not len(master_password) == 0:
      self._path = vault_path
      self._master_password = master_password
      self._load_vault()
  
  # Load the password vault using the master password (create if nonexistant)
  def _load_vault(self):
    if os.path.isfile(self._path):
      enc_vault_file = open(self._path, "r")
      enc_vault_file_contents = enc_vault_file.read()
      enc_vault_file.close()
      enc_vault_dict = json.loads(enc_vault_file_contents)
      enc_key = base64.b64decode(enc_vault_dict["enc_key"].encode(self._TEXT_ENCODING))
      salt = base64.b64decode(enc_vault_dict["salt"].encode(self._TEXT_ENCODING))
      enc_passwords = base64.b64decode(enc_vault_dict["enc_passwords"].encode(self._TEXT_ENCODING))
      self._crypto.unlock_key(self._master_password, enc_key, salt)
      passwords_json = self._crypto.decrypt(enc_passwords).decode(self._TEXT_ENCODING)
      self._passwords = json.loads(passwords_json)
      self._enc_key = enc_key
      self._salt = salt
      self._saving = True
    else:
      key_details = self._crypto.generate_key(self._master_password)
      self._enc_key = key_details["enc_key"]
      self._salt = key_details["salt"]
      self._saving = True
      self._save_vault()
  
  # Save vault to file if this instance of the manager is using a vault for storage
  def _save_vault(self):
    if self._saving:
      enc_passwords = self._crypto.encrypt(json.dumps(self._passwords).encode(self._TEXT_ENCODING))
      enc_passwords_b64 = base64.b64encode(enc_passwords).decode(self._TEXT_ENCODING)
      enc_key_b64 = base64.b64encode(self._enc_key).decode(self._TEXT_ENCODING)
      salt_b64 = base64.b64encode(self._salt).decode(self._TEXT_ENCODING)
      vault_contents = {"enc_key": enc_key_b64, "salt": salt_b64, "enc_passwords": enc_passwords_b64}
      vault_file_contents = json.dumps(vault_contents)
      vault_file_handle = open(self._path, "w")
      vault_file_handle.write(vault_file_contents)
      vault_file_handle.close()
  
  # Return if a password exists in the vault (by site string)
  def password_exists(self, site):
    for password_entry in self._passwords:
      if "site" in password_entry and password_entry["site"] == site:
        return True
    return False
  
  # Generate a password
  # Takes length, site string, and phrase (arbitrary phrase the user associates with the site)
  # Length should be at least 1; site string and phrase should be nonempty and of valid characters
  def generate_password(self, length, site, phrase):
    if length < 1 or site == None or site == "" or phrase == None or phrase == "":
      return None
    password = self._generator.make_password(length, site, phrase)
    entry = {"site": site, "password": password}
    if self.password_exists(site):
      for i in range(len(self._passwords)):
        if self._passwords[i]["site"] == site:
          self._passwords[i] = entry
    else:
      self._passwords.append(entry)
    self._save_vault()
    return password
  
  # Deletes a password by site string (does nothing if nonexistant)
  def delete_password(self, site):
    if self.password_exists(site):
      for i in range(len(self._passwords)):
        if self._passwords[i]["site"] == site:
          del self._passwords[i]
          break
      self._save_vault()
  
  # Returns list of passwords.
  # Each entry is a dictionary with site and password keys.
  def get_passwords(self):
    return copy.deepcopy(self._passwords)
  
  # Checks and returns whether a given string contains only the characters allowed to be used in this algorithm
  def is_valid_string(self, phrase):
    return self._generator.is_valid_string(phrase)
