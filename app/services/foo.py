import logging

from app.models.config import Config


logger = logging.getLogger(__name__)


def foo(config: Config):
    logger.info(config)
