import random

# PasswordGenerator
# The PasswordGenerator class provides for the algorithm to generate the password.
# Class to generate password using algorithm defined in "Password Algorithm Steps" file

class PasswordGenerator(object):
  # Constants
  _LOWERCASE_LETTERS = "abcdefghijklmnopqrstuvwxyz"
  _UPPERCASE_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  _NUMBERS = "0123456789"
  _SYMBOLS = "!\\" + '"' + "#$%&'()*+,-./:;<>=?@[\]^_`{|}~"
  _PHRASE_CHARS = _LOWERCASE_LETTERS + _UPPERCASE_LETTERS + _NUMBERS + _SYMBOLS
  _CHAR_TYPE_DEFICIT_NUMBER = 2
  
  # Returns a random character from a string (char_str)
  def _get_random_character(self, char_str):
    if not char_str == None:
      return char_str[random.randint(0, len(char_str) - 1)]
    else:
      return None
  
  # Checks and returns whether a given string (phrase) contains only the characters allowed to be used in this algorithm
  def is_valid_string(self, phrase):
    for i in range(len(phrase)):
      if self._PHRASE_CHARS.find(phrase[i]) == -1:
        return False
    return True
  
  # Creates an initial seed for the password
  # Adds the character codes of corresponding characters of site and phrase (cycling over if needed) and mods the result with the length of the complete character list
  # Returns a seed string with the characters represented by these calculated codes
  def get_combined_site_and_phrase_string(self, site, phrase):
    if len(site) < 1 or len(phrase) < 1:
      raise ValueError("Parameters site and phrase cannot be empty.")
    new_phrase = ""
    phrase1 = ""
    phrase2 = ""
    if len(phrase) > len(site):
      phrase1 = phrase
      phrase2 = site
    else:
      phrase1 = site
      phrase2 = phrase
    j = 0
    for i in range(len(phrase1)):
      j = i % len(phrase2)
      char_index = (self._PHRASE_CHARS.find(phrase1[i]) + self._PHRASE_CHARS.find(phrase2[j])) % len(self._PHRASE_CHARS)
      new_phrase += self._PHRASE_CHARS[char_index]
    return new_phrase
  
  # Scrambles string phrase by iterating over it like a binary search and appending the midpoints of sections from left to right on each pass
  def scramble_phrase(self, phrase):
    if len(phrase) == 0:
      return ""
    str = ""
    ranges = [[0, len(phrase) - 1]]
    while len(ranges) > 0:
      new_ranges = []
      for i in range(len(ranges)):
        low = ranges[i][0]
        high = ranges[i][1]
        mid = (low + high) // 2
        str += phrase[mid]
        new_low1 = low
        new_high1 = mid - 1
        new_low2 = mid + 1
        new_high2 = high
        if new_high1 >= new_low1:
          new_ranges.append([new_low1, new_high1])
        if new_high2 >= new_low2:
          new_ranges.append([new_low2, new_high2])
      ranges = new_ranges
    return str
  
  # Determines which type of character is deficient in the string makeup
  # Picks character with minimum instances in makeup if difference of maximum and minimum instances is at least _CHAR_TYPE_DEFICIT_NUMBER in order of lowercase letters, uppercase letters, numbers, and special characters
  def get_char_type_deficit(self, makeup):
    keys = list(makeup.keys())
    vals = list(makeup.values())
    min_number = vals[0]
    min_index = 0
    max_number = vals[0]
    max_index = 0
    for i in range(len(makeup)):
      if vals[i] < min_number:
        min_number = vals[i]
        min_index = i
      if vals[i] > max_number:
        max_number = vals[i]
        max_index = i
    if max_number - min_number >= self._CHAR_TYPE_DEFICIT_NUMBER:
      return keys[min_index]
    else:
      return ""
  
  # Sums the character codes of phrase as folllows:
  # Sums character codes of odd indices if len(phrase) is odd
  # Sums character codes of even indices if len(phrase) is even
  def sum_phrase_indices_odd_or_even(self, phrase):
    if not self.is_valid_string(phrase):
      raise ValueError("String must consist solely of lowercase letters, uppercase letters, numbers, and symbols.")
    sum = 0
    i = len(phrase) % 2
    while i <= len(phrase) - 1:
      sum += self._PHRASE_CHARS.find(phrase[i])
      i += 2
    return sum
  
  # Returns the type of character char_arg (lowercase/uppercase letter, number, special character) as a string
  def get_char_type(self, char_arg):
    if not len(char_arg) == 1:
      raise ValueError("Not a character.")
    if self._LOWERCASE_LETTERS.find(char_arg) > -1:
      return "lowercase"
    elif self._UPPERCASE_LETTERS.find(char_arg) > -1:
      return "uppercase"
    elif self._NUMBERS.find(char_arg) > -1:
      return "numbers"
    elif self._SYMBOLS.find(char_arg) > -1:
      return "symbols"
  
  # Generates and returns the password as a string.
  # Parameters:
  # length (must be at least 1)
  # site - a string of at least length 1 denoting the name of the site for this password
  # phrase - an arbitrary phrase that the user will remember to associate with this site; used to generate password seed
  def make_password(self, length, site, phrase):
    if length < 1 or not self.is_valid_string(site) or len(site) < 1 or not self.is_valid_string(phrase) or len(phrase) < 1:
      raise ValueError("Length must be at least 1, and site and phrase must consist only of lowercase letters, uppercase letters, numbers, and special keyboard characters.")
    material = self.scramble_phrase(self.get_combined_site_and_phrase_string(site, phrase))
    password = ""
    phrase_index = 0
    symbol_types = {"lowercase": 0, "uppercase": 0, "numbers": 0, "symbols": 0}
    for i in range(length):
      deficit = self.get_char_type_deficit(symbol_types)
      char_to_insert = ""
      password_sum = self.sum_phrase_indices_odd_or_even(password)
      if deficit == "lowercase":
        char_to_insert = self._get_random_character(self._LOWERCASE_LETTERS)
      elif deficit == "uppercase":
        char_to_insert = self._get_random_character(self._UPPERCASE_LETTERS)
      elif deficit == "numbers":
        char_to_insert = self._get_random_character(self._NUMBERS)
      elif deficit == "symbols":
        char_to_insert = self._get_random_character(self._SYMBOLS)
      else:
        char_to_insert = material[phrase_index]
        phrase_index += 1
      password += char_to_insert
      symbol_types[self.get_char_type(char_to_insert)] += 1
      if phrase_index == len(material):
        phrase_index = 0
        phrase_offset = max(1, abs((self._PHRASE_CHARS.find(material[0]) - self._PHRASE_CHARS.find(material[len(material) - 1]))) // 2)
        new_material = ""
        for k in range(len(material)):
          new_material += self._PHRASE_CHARS[(self._PHRASE_CHARS.find(material[k]) + phrase_offset) % len(self._PHRASE_CHARS)]
        material = new_material
    return password
