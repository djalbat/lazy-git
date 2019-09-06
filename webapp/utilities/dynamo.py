import boto3


from utilities.configuration import *


table_name = get_table_name()
region_name = get_region_name()
endpoint_url = get_endpoint_url()
aws_access_key_id = get_aws_access_key_id()
aws_secret_access_key = get_aws_secret_access_key()


dynamo_db_client = boto3.client('dynamodb', region_name=region_name, endpoint_url=endpoint_url, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key) ###

dynamo_db_resource = boto3.resource('dynamodb', region_name=region_name, endpoint_url=endpoint_url, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key) ###


def _check_table_exists():
  tables = dynamo_db_client.list_tables()

  table_names = tables['TableNames'] ###

  table_exists = table_name in table_names

  return table_exists


def _create_table():
  table = dynamo_db_client.create_table(
    TableName=table_name,
    KeySchema=[
      {
        'AttributeName': 'authorisation_string',
        'KeyType': 'HASH'
      },
      {
        'AttributeName': 'url',
        'KeyType': 'RANGE'
      }
    ],
    AttributeDefinitions=[
      {
        'AttributeName': 'authorisation_string',
        'AttributeType': 'S'
      },
      {
        'AttributeName': 'url',
        'AttributeType': 'S'
      }
    ],
    ProvisionedThroughput={
      'ReadCapacityUnits': 1024,
      'WriteCapacityUnits': 8
    }
  )

  return table


def _delete_table():
  table = _get_table()

  table.delete()

  return


def _get_table():
  table = dynamo_db_resource.Table(table_name)

  return table


def initialise_table():
  table_exists = _check_table_exists()

  if not table_exists:
    _create_table()

  return


def get_all_items():
  table = _get_table()

  result = table.scan()

  items = result['Items']

  return items


def scan_items(filter_expression):
  table = _get_table()

  FilterExpression = filter_expression ###

  try:
    result = table.scan(FilterExpression=FilterExpression)

    items = result['Items']  ###

  except:
    raise

  return items


def query_items(key_condition_expression, expression_attribute_names, expression_attribute_values):
  table = _get_table()

  FilterExpression = key_condition_expression ###

  ExpressionAttributeNames = expression_attribute_names ###

  ExpressionAttributeValues = expression_attribute_values  ###

  try:
    result = table.scan(FilterExpression=FilterExpression , ExpressionAttributeNames=ExpressionAttributeNames, ExpressionAttributeValues=ExpressionAttributeValues)

    items = result['Items']  ###

  except:
    raise

  return items


def get_item(key):
  table = _get_table()

  Key = key ###

  try:
    result = table.get_item(Key=Key)

    item = result['Item'] if 'Item' in result else None  ###

  except:
    raise

  return item


def put_item(key):
  table = _get_table()

  item = key ###

  Item = item ###

  try:
    table.put_item(Item=Item)

  except:
    raise


def delete_item(key):
  table = _get_table()

  Key = key ###

  table.delete_item(Key=Key)

  return


def update_item(key, update_expression, expression_attribute_values):
  table = _get_table()

  Key = key  ###

  UpdateExpression = update_expression  ###

  ExpressionAttributeValues = expression_attribute_values  ###

  try:
    table.update_item(Key=Key, UpdateExpression=UpdateExpression, ExpressionAttributeValues=ExpressionAttributeValues)

  except:
    raise

  return


def update_item_on_condition(key, update_expression, condition_expression, expression_attribute_values):
  table = _get_table()

  Key = key  ###

  UpdateExpression = update_expression  ###

  ConditionExpression = condition_expression ###

  ExpressionAttributeValues = expression_attribute_values  ###

  try:
    table.update_item(Key=Key, UpdateExpression=UpdateExpression, ConditionExpression=ConditionExpression, ExpressionAttributeValues=ExpressionAttributeValues)

  except Exception as exception:
    message = str(exception) ###

    if 'ConditionalCheckFailedException' in message:
      pass

    else:
      raise

  return
