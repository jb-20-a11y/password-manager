import os, sys
from Cryptodome import Random
from Cryptodome.Cipher import AES
from Cryptodome.Hash import HMAC, SHA256
from Cryptodome.Protocol.KDF import PBKDF2

# PasswordManagerCrypto
# Allows for AES encryption of the vault via a master password

# Class to provide AES-GCM cryptography
# The password vault is unlocked by a master password that unlocks a 256-bit key used to encrypt the vault using a PBKDF2-derived key generated from the password and with random salt
class PasswordManagerCrypto(object):
  # Constants used for AES-GCM encryption
  _DKLEN = 32 # Derived key length
  _COUNT = 1000 # PBKDF2 iteration count value
  _SALT_LENGTH = 32 # Salt length
  
  # Instance variables
  _key = None
  
  # Constructor: initially starts out with blank key
  def __init__(self):
    self._key = None
  
  # Generates a random 256-bit key, encrypts it with a PBKDF2 key derived from the given password, and returns the encrypted key and salt
  # The random key is stored in the instance to be able to encrypt and decrypt data with it
  def generate_key(self, password):
    random_key = Random.get_random_bytes(self._DKLEN)
    salt = Random.get_random_bytes(self._SALT_LENGTH)
    kdf = PBKDF2(password, salt, self._DKLEN, self._COUNT)
    self._key = kdf
    enc_key = self.encrypt(random_key)
    self._key = random_key
    return {"enc_key": enc_key, "salt": salt}
  
  # Unlocks the real encryption key used for data, encrypted by the PBKDF2-derived key based on the password
  # The real key is stored in this instance to be able to encrypt and decrypt data
  # ValueError thrown if decryption failed; caught by the caller to allow user to reenter password
  def unlock_key(self, password, enc_key, salt):
    self._key = PBKDF2(password, salt, self._DKLEN, self._COUNT)
    self._key = self.decrypt(enc_key)
  
  # Encrypt data using AES-GCM and current key value
  # Returns bytes with tag, nonce, and ciphertext
  def encrypt(self, data):
    cipher = AES.new(self._key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return tag + cipher.nonce + ciphertext
  
  # Decrypt data using the current key - assumed to consist of bytes: authentication tag (16 bytes) + nonce (16 bytes) + ciphertext
  # Returns decrypted data as bytes
  # ValueError thrown if decryption failed; caught by the caller to allow user to reenter password
  def decrypt(self, data):
    tag = data[0:16]
    nonce = data[16:32]
    ciphertext = data[32:]
    cipher = AES.new(self._key, AES.MODE_GCM, nonce=nonce)
    decrypted = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted

