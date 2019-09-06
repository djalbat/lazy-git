import dateutil.parser


from datetime import datetime


def to_timestamp(string):
  return int(dateutil.parser.parse(string).timestamp()) ###


def from_timestamp(timestamp):
  return datetime.fromtimestamp(timestamp).strftime('%a, %d %b %Y %H:%M:%S GMT') ###
