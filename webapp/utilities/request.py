from utilities.configuration import *


def url_from_path_and_query(path, query):
  github_host = get_github_host()

  url = '{github_host}{path}{query}'.format(github_host=github_host, path=path, query=query)

  return url


def url_from_request(request):
  path = request.path

  query = '?' + request.query_string.decode() if request.query_string else ''

  url = url_from_path_and_query(path, query)

  return url


def headers_from_request(request):
  headers = {}

  for name, value in request.headers.items(): ###
    headers[name] = value

  return headers
