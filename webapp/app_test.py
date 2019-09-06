import pytest


from app import app


from utilities.cache import *
from utilities.request import *
from utilities.response import *
from utilities.authorisation import *
from utilities.configuration import *


github_username = get_github_username()

github_authorisation_token = get_github_authorisation_token()


empty_query = ''

default_path = '/'
spurious_path = '/123'
rate_limit_path = '/rate_limit'
healthcheck_path = get_healthcheck_path()

spurious_content = b'zxcvzxcv'

spurious_username = 'ASDFASDFASDF'

spurious_authorisation_token = '1234123412341234'

spurious_authorisation_string = '{spurious_username}:{spurious_authorisation_token}'.format(spurious_username=spurious_username, spurious_authorisation_token=spurious_authorisation_token)

genuine_username = github_username ###

genuine_authorisation_token = github_authorisation_token ###

genuine_authorisation_string = '{genuine_username}:{genuine_authorisation_token}'.format(genuine_username=genuine_username, genuine_authorisation_token=genuine_authorisation_token)

genuine_resource_path = '/repos/glg/lazy-git/contents/README.md'


initialise_table()


flush_all()


@pytest.fixture
def client():
  client = app.test_client()

  yield client


def test_if_healthcheck_path_then_status_code_200_is_returned(client):
  path = healthcheck_path

  query = empty_query

  url = url_from_path_and_query(path, query)

  response = client.get(url)

  status_code = status_code_from_response(response)

  assert status_code == 200


def test_if_spurious_path_without_authorisation_then_status_code_500_is_returned(client):
  path = spurious_path

  query = empty_query

  url = url_from_path_and_query(path, query)

  response = client.get(url)

  status_code = status_code_from_response(response)

  flush_all()

  assert status_code == 500


def test_if_spurious_path_with_spurious_authorisation_then_status_code_401_is_returned(client):
  path = spurious_path

  query = empty_query

  url = url_from_path_and_query(path, query)

  authorisation_string = spurious_authorisation_string

  headers = headers_from_authorisation_string(authorisation_string)

  response = client.get(url, headers=headers)

  status_code = status_code_from_response(response)

  flush_all()

  assert status_code == 401


def test_if_spurious_path_with_genuine_authorisation_then_status_code_404_is_returned(client):
  path = spurious_path

  query = empty_query

  url = url_from_path_and_query(path, query)

  authorisation_string = genuine_authorisation_string

  headers = headers_from_authorisation_string(authorisation_string)

  response = client.get(url, headers=headers)

  status_code = status_code_from_response(response)

  flush_all()

  assert status_code == 404


def test_if_rate_limit_path_with_spurious_authorisation_then_status_code_401_is_returned(client):
  path = rate_limit_path

  query = empty_query

  url = url_from_path_and_query(path, query)

  authorisation_string = spurious_authorisation_string

  headers = headers_from_authorisation_string(authorisation_string)

  response = client.get(url, headers=headers)

  status_code = status_code_from_response(response)

  flush_all()

  assert status_code == 401


def test_if_rate_limit_path_with_genuine_authorisation_then_status_code_200_is_returned(client):
  path = rate_limit_path

  query = empty_query

  url = url_from_path_and_query(path, query)

  authorisation_string = genuine_authorisation_string

  headers = headers_from_authorisation_string(authorisation_string)

  response = client.get(url, headers=headers)

  status_code = status_code_from_response(response)

  flush_all()

  assert status_code == 200


def test_if_genuine_resource_path_with_genuine_authorisation_then_status_code_200_is_returned(client):
  path = genuine_resource_path

  query = empty_query

  url = url_from_path_and_query(path, query)

  authorisation_string = genuine_authorisation_string

  headers = headers_from_authorisation_string(authorisation_string)

  response = client.get(url, headers=headers)

  status_code = status_code_from_response(response)

  flush_all()

  assert status_code == 200


def test_if_resource_is_not_stored_then_it_is_stored(client):
  path = genuine_resource_path

  query = empty_query

  url = url_from_path_and_query(path, query)

  authorisation_string = genuine_authorisation_string

  flush(authorisation_string, url)

  headers = headers_from_authorisation_string(authorisation_string)

  client.get(url, headers=headers)

  content, content_type, last_modified = retrieve(authorisation_string, url)

  stored = not (content == None)

  flush_all()

  assert stored


def test_if_resource_is_stored_then_stored_content_is_returned(client):
  path = genuine_resource_path

  query = empty_query

  url = url_from_path_and_query(path, query)

  authorisation_string = genuine_authorisation_string

  headers = headers_from_authorisation_string(authorisation_string)

  client.get(url, headers=headers)

  content, content_type, last_modified = retrieve(authorisation_string, url)

  content = spurious_content ###

  flush(authorisation_string, url)

  store(authorisation_string, url, content, content_type, last_modified)

  response = client.get(url, headers=headers)

  flush(authorisation_string, url)

  data = response.data

  content = data ###

  flush_all()

  assert content == spurious_content
