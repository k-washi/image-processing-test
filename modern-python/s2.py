import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from util.log_conf import get_logger
logger = get_logger(__file__)

logger.debug("テストメッセージ")

logger2 = get_logger("__app__")
logger2.info("info メッセージ")