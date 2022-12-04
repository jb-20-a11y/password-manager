import sys

# PasswordManagerRunner
# Starts an instance of PasswordManagerCLI

# Check Python version (must be using 3)
if (sys.version_info) < (3, 0):
  print("ERROR: Python 3 is required. This program is currently running in Python 2.")
  exit()

# Check for crypto modules (install pycryptodomex module for this program to function)
try:
  from password_manager_cli import PasswordManagerCLI
except:
  print("The pycryptodomex module is not installed. Please install this module for the program to function.")
  exit()

cli = None
cli_error = False

try:
  cli = PasswordManagerCLI()
except:
  cli_error = True
  print("The initialization of the password vault file failed. Perhaps the path provided is an invalid OS path, or the file is corrupted.")
  
if not cli == None and not cli_error:
  cli.enter_menu()
