from base64 import b64encode, b64decode


alternative_characters = b'+-'


def encode(string):
  encoded_string = b64encode(string.encode(), alternative_characters).decode() ###

  return encoded_string


def decode(encoded_string):
  string = b64decode(encoded_string, alternative_characters).decode() ###

  return string
