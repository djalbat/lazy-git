def _headers_from_response(response):
  headers = {}

  for name, value in response.headers.items():
    headers[name] = value

  return headers


def status_code_from_response(response):
  status_code = response.status_code

  return status_code


def content_from_response(response):
  content = response.content

  return content


def headers_and_status_code_from_response(response):
  headers = _headers_from_response(response)

  status_code = status_code_from_response(response)

  return headers, status_code
