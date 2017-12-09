import logging
import sys

from .constants import PROJECT_NAME, LOG_LEVEL

logger = logging.getLogger(PROJECT_NAME)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(LOG_LEVEL)
stdout_handler.setFormatter(formatter)
logger.addHandler(stdout_handler)
logger.setLevel(LOG_LEVEL)

logger.debug("Logger initialised")