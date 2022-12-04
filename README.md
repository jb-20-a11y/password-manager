# Python-Based CLI Password Manager
This package consists of Python classes to manage a master password vault as well as generate passwords for the end-user. A front-end CLI is also included to interact with these classes and provide complete password manager functionality.

## Features
* Built-in pseudorandom password generator that works on the specified key length
* Create and retrieve passwords by site name (or any other arbitrary descriptor)
* Passwords are stored in a vault encrypted by a master password

## Prerequisites
Python 3 and the pycryptodomex package are required in order to run this program.

## Run
Run `password_manager_runner.py` to run the front-end command-line interface.