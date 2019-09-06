from flask import Flask, request, render_template
from requests import get


from utilities.cache import *
from utilities.headers import *
from utilities.request import *
from utilities.logging import *
from utilities.response import *
from utilities.authorisation import *
from utilities.configuration import *


app = Flask(__name__)


logger = get_logger()

proxy_path = get_proxy_path()

healthcheck_path = get_healthcheck_path()


@app.route(healthcheck_path)
def healthcheck():
  return 'OK'


@app.route(proxy_path)
def proxy(path): ###
  url = url_from_request(request)

  headers = headers_from_request(request)

  authorisation_string = authorisation_string_from_headers(headers)

  content, content_type, last_modified = retrieve(authorisation_string, url)

  stored = not (content == None)

  if stored:
    set_if_modified_since_in_headers(headers, last_modified)

  set_host_to_github_host_in_headers(headers)

  delete_content_length_from_headers(headers)

  response = get(url, headers=headers)

  headers, status_code = headers_and_status_code_from_response(response)

  delete_content_encoding_and_transfer_encoding_from_headers(headers)

  if status_code == 304:
    add_content_type_to_headers(content_type, headers)

    status_code = 200  ###

  else:
    content = content_from_response(response)

    if status_code == 200:
      last_modified, content_type = last_modified_and_content_type_from_headers(headers)

      if last_modified:
        store(authorisation_string, url, content, content_type, last_modified)

        content, content_type, last_modified = retrieve(authorisation_string, url)

  return content, status_code, headers


@app.errorhandler(Exception)
def error_handler(exception):
  message = str(exception) ###

  content = render_template('exception.txt', message=message)

  error = message ###

  logger.error(error)

  status_code = 500

  headers = {
    'Content-Type': 'text/plain'
  }

  return content, status_code, headers
