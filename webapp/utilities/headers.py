from utilities.configuration import *


def add_content_type_to_headers(content_type, headers):
  headers['Content-Type'] = content_type

  return


def set_if_modified_since_in_headers(headers, last_modified):
  if_modified_since = last_modified ###

  headers['If-Modified-Since'] = if_modified_since

  return


def set_host_to_github_host_in_headers(headers):
  github_host = get_github_host()

  host = github_host ###

  headers['Host'] = host ###

  return


def last_modified_and_content_type_from_headers(headers):
  last_modified = None

  if 'Last-Modified' in headers:
    last_modified_header = headers['Last-Modified']
    last_modified = last_modified_header  ###

  content_type = headers['Content-Type']

  return last_modified, content_type


def delete_content_length_from_headers(headers):
  if 'Content-Length' in headers:
    del headers['Content-Length']

    return


def delete_content_encoding_and_transfer_encoding_from_headers(headers):
  if 'Content-Encoding' in headers:
    del headers['Content-Encoding']

  if 'Transfer-Encoding' in headers:
    del headers['Transfer-Encoding']

  return
