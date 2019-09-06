from re import compile
from base64 import b64decode, b64encode


from utilities.array import *


authorisation_header_regular_expression = compile('^Basic (.+)$')


def _authorisation_header_from_headers(headers):
  if not 'Authorization' in headers:
    raise Exception('The authorisation header is missing.')

  authorisation_header = headers['Authorization']  ###

  return authorisation_header


def _authorisation_string_from_authorisation_header(authorisation_header):
  matches = authorisation_header_regular_expression.match(authorisation_header)

  groups = matches.groups()

  first_group = first(groups)

  b64encoded_authorisation_string = first_group ###

  authorisation_string = b64decode(b64encoded_authorisation_string).decode()  ###

  return authorisation_string


def authorisation_string_from_headers(headers):
  authorisation_header = _authorisation_header_from_headers(headers)

  authorisation_string = _authorisation_string_from_authorisation_header(authorisation_header)

  return authorisation_string


def headers_from_authorisation_string(authorisation_string):
  encoded_authorisation_string = b64encode(authorisation_string.encode('utf-8')).decode('utf-8') ###

  authorisation_header = 'Basic {encoded_authorisation_string}'.format(encoded_authorisation_string=encoded_authorisation_string) ###

  headers = {
    'Authorization': authorisation_header
  }

  return headers
