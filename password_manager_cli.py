import os

from password_manager import PasswordManager

# PasswordManagerCLI
# Command-line interface for the user to interact with the password manager

# by Jalen Ballard
# 01/31/2020

# Class that uses PasswordManager to create an interactive CLI for the password manager
class PasswordManagerCLI(object):
  # Constants
  _DEFAULT_PATH = "vault.json"
  _MIN_RECOMMENDED_LENGTH = 14
  _MIN_REQUIRED_LENGTH = 6
  
  # Instance variables
  _password_manager = None
  
  # Constructor that initializes PasswordManager instance
  # vault_path is the path of the password vault file (created if nonexistant)
  # password is the master password
  # Prompts user for vault path and master password if not specified in parameters
  def __init__(self, vault_path=None, password=None):
    self.print_welcome()
    if vault_path == None or len(vault_path) == 0 or password == None or len(password) == 0:
      self.prompt_for_vault()
    else:
      self._password_manager = PasswordManager(vault_path, password)
  
  # Print welcome message
  def print_welcome(self):
    print("Welcome to the password manager.")
    print("This interface will guide you through creating and retrieving passwords.")
    print("You must enter a site name and arbitrary phrase you associate with that site to serve as the seed for generating the password.")
    print("Passwords will be saved in a single vault file encrypted using a master password that you provide.")
    print("Inputs other than menu entries are case-sensitive.")
    print("Site names and phrases must consist only of lowercase letters, uppercase letters, numbers, and special keyboard characters (no spaces).")
    print()
  
  # Takes input: integer in interval [a, infinity)
  def _take_numerical_input_at_least(self, message, a):
    entered_number = ""
    while not str.isdigit(entered_number) or (str.isdigit(entered_number) and (int(entered_number) < a)):
      entered_number = input(message + " ")
      if not str.isdigit(entered_number) or (str.isdigit(entered_number) and (int(entered_number) < a)):
        print("You need to enter an integer of at least " + str(a) + ". Please try again.")
    return int(entered_number)
  
  # Takes input: nonempty string equal to parameter check_str
  def _take_nonempty_equal_input(self, message, check_str):
    entered_string = ""
    while len(entered_string) == 0 or not entered_string == check_str:
      entered_string = input(message + " ")
      if len(entered_string) == 0 or not entered_string == check_str:
        print("You need to enter a nonempty string equal to what you previously entered to verify your input. Please try again.")
    return entered_string
  
  # Takes input: nonempty string
  def _take_nonempty_input(self, message):
    entered_string = ""
    while len(entered_string) == 0:
      entered_string = input(message + " ")
      if len(entered_string) == 0:
        print("You need to enter a nonempty string. Please try again.")
    return entered_string
  
  # Takes input: nonempty string of valid characters
  def _take_nonempty_input_of_valid_characters(self, message):
    entered_string = ""
    while len(entered_string) == 0 or not self._password_manager.is_valid_string(entered_string):
      entered_string = input(message + " ")
      if len(entered_string) == 0 or not self._password_manager.is_valid_string(entered_string):
        print("You need to enter a nonempty string consisting only of lowercase letters, uppercase letters, numbers, and standard special keyboard characters. Please try again.")
    return entered_string
  
  # Takes input: y for yes and n for no (case-insensitive)
  def _take_yes_or_no_input(self, message):
    entered_choice = ""
    while not entered_choice == "y" and not entered_choice == "n":
      entered_choice = str.lower(input(message + " (y/n) "))
      if not entered_choice == "y" and not entered_choice == "n":
        print("Enter y for yes and n for no.")
    return entered_choice == "y"
  
  # Takes input: meant for different choices in a text menu (case-insensitive)
  def _take_case_insensitive_menu_input(self, message, options):
    entered_choice = ""
    while not entered_choice in options:
      entered_choice = str.lower(input(message + " "))
      if not entered_choice in options:
        print("Please enter a valid option.")
    return entered_choice
  
  # Prompt user for vault path and master password
  def prompt_for_vault(self):
    print("Now you must choose which vault you want to use for this instance.")
    print("If you do not enter a path, the default value of " + self._DEFAULT_PATH + " will be used.")
    print()
    print("Please enter the path of the vault to create or open:")
    path = input()
    if path == "":
      path = self._DEFAULT_PATH
    if os.path.isfile(path):
      print("Now you must enter the master password used to unlock this vault.")
      master_password = ""
      locked = True
      while locked:
        master_password = self._take_nonempty_input("Enter master password:")
        try:
          self._password_manager = PasswordManager(path, master_password)
        except ValueError:
          print("The password is incorrect. Please try again.")
          continue
        locked = False
    else:
      print("This vault does not exist. You must create a new vault with a master password you will use to unlock the vault when opening this application.")
      print()
      master_password = self._take_nonempty_input("Enter master password:")
      self._take_nonempty_equal_input("Reenter master password:", master_password)
      self._password_manager = PasswordManager(path, master_password)
    print()
  
  # Prints out the stored sites and appropriate passwords in alphabetical order of site
  def view_passwords(self):
    passwords = sorted(self._password_manager.get_passwords(), key = lambda i: i["site"])
    if len(passwords) == 0:
      print("No passwords to report.")
    for i in range(len(passwords)):
      print("Site: " + passwords[i]["site"] + ", Password: " + passwords[i]["password"])
    print()
  
  # Prompt the user for appropriate information and create a new password
  def new_password(self):
    length = self._take_numerical_input_at_least("Enter the password length (at least " + str(self._MIN_RECOMMENDED_LENGTH) + " recommended, " + str(self._MIN_REQUIRED_LENGTH) + " minimum):", self._MIN_REQUIRED_LENGTH)
    site = self._take_nonempty_input_of_valid_characters("Enter the site name:")
    if self._password_manager.password_exists(site):
      confirm_replace = self._take_yes_or_no_input("A password for this site already exists. Do you want to generate a new password and replace the old entry?")
      if not confirm_replace:
        print("Cancelled.")
        print()
        return
    phrase = self._take_nonempty_input_of_valid_characters("Enter an arbitrary phrase you associate with this site:")
    password = self._password_manager.generate_password(length, site, phrase)
    print()
    print("Your generated password is: " + password)
    print()
  
  # Deletes a password by site specified by user
  def delete_password(self):
    site = self._take_nonempty_input_of_valid_characters("Please enter the site name associated with the password to delete:")
    if self._password_manager.password_exists(site):
      confirmation = self._take_yes_or_no_input("Are you sure you want to delete this password?")
      if confirmation:
        self._password_manager.delete_password(site)
        print("Password deleted.")
      else:
        print("Cancelled.")
    else:
      print("There is no password associated with that site. Operation cancelled.")
    print()
  
  # Displays menu for user to choose options
  # Gives menu to view passwords, generate passwords, delete passwords, and quit
  def enter_menu(self):
    menu_options = {"v": "View saved passwords", "n": "Generate new password", "d": "Delete password", "q": "Quit"}
    choice = ""
    while not choice == "q":
      print()
      print("Menu:")
      for letter in menu_options:
        print(letter + " - " + menu_options[letter])
      print()
      choice = self._take_case_insensitive_menu_input("Enter your choice:", menu_options)
      if choice == "v":
        self.view_passwords()
      elif choice == "n":
        self.new_password()
      elif choice == "d":
        self.delete_password()
      elif choice == "q":
        print("Quitting...")
  