import os


def get_github_host():
  github_host = os.environ['GITHUB_HOST']

  return github_host


def get_proxy_path():
  proxy_path = '/<path:path>' ###

  return proxy_path


def get_healthcheck_path():
  healthcheck_path = os.environ['HEALTHCHECK'] ###

  return healthcheck_path


def get_log_level():
  log_level = os.environ['LOG_LEVEL']

  return log_level


def get_log_ini_file_path():
  log_ini_file_path = './logging.ini'

  return log_ini_file_path


def get_github_username():
  github_username = os.environ['GITHUB_USERNAME']

  return github_username


def get_github_authorisation_token():
  github_authorisation_token = os.environ['GITHUB_AUTHORISATION_TOKEN']

  return github_authorisation_token


def get_table_name():
  table_name = os.environ['TABLE_NAME']

  return table_name


def get_region_name():
  region_name = os.environ['REGION_NAME']

  return region_name


def get_endpoint_url():
  endpoint_url = os.environ['ENDPOINT_URL']

  return endpoint_url


def get_aws_access_key_id():
  aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']

  return aws_access_key_id


def get_aws_secret_access_key():
  aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']

  return aws_secret_access_key
