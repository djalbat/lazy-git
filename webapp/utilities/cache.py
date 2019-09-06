from utilities.key import *
from utilities.dynamo import *
from utilities.timestamp import *


def flush_all():
  items = get_all_items()

  for item in items:
    authorisation_string = item['authorisation_string']

    url = item['url']

    key = key_from_authorisation_string_and_url(authorisation_string, url)

    delete_item(key)

  return


def flush(authorisation_string, url):
  key = key_from_authorisation_string_and_url(authorisation_string, url)

  delete_item(key)

  return


def store(authorisation_string, url, content, content_type, last_modified):
  decoded_content = content.decode()

  last_modified_timestamp = to_timestamp(last_modified)

  key = key_from_authorisation_string_and_url(authorisation_string, url)

  update_expression = 'SET content_type = :content_type, decoded_content = :decoded_content, last_modified_timestamp = :last_modified_timestamp'

  condition_expression = 'attribute_not_exists(last_modified_timestamp) OR last_modified_timestamp < :last_modified_timestamp'

  expression_attribute_values = {
    ':content_type': content_type,
    ':decoded_content': decoded_content,
    ':last_modified_timestamp': last_modified_timestamp
  }

  update_item_on_condition(key, update_expression, condition_expression, expression_attribute_values)

  return


def retrieve(authorisation_string, url):
  content = None

  content_type = None

  last_modified = None

  key = key_from_authorisation_string_and_url(authorisation_string, url)

  item = get_item(key)

  if item:
    content_type = item['content_type']

    decoded_content = item['decoded_content']

    last_modified_timestamp = item['last_modified_timestamp']

    content = decoded_content.encode()

    last_modified = from_timestamp(last_modified_timestamp)

  return content, content_type, last_modified
