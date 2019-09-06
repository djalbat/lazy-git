import sys
import logging


class Error_Filter(logging.Filter):
  def __init__(self, param=None):
    self.param = param

  def filter(self, record):
    allow = False if record.levelname == 'ERROR' else True

    return allow

error_filter = Error_Filter()


null_handler = logging.NullHandler()

stdout_handler = logging.StreamHandler(sys.stdout)

stdout_handler.setLevel(logging.NOTSET)

stderr_handler = logging.StreamHandler(sys.stderr)


logging.basicConfig(level=logging.DEBUG, handlers=[null_handler])


logger = logging.getLogger()

stderr_handler.setLevel(logging.ERROR)

stdout_handler.addFilter(error_filter)

logger.addHandler(stdout_handler)

logger.addHandler(stderr_handler)


def get_logger():
  return logger
