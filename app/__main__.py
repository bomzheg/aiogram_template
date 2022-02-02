import logging
from pathlib import Path

from app.config import load_config
from app.services.foo import foo


logger = logging.getLogger(__name__)


def main():
    app_dir = Path(__file__).parent.parent
    config = load_config(app_dir)

    logger.info("started")

    foo(config)


if __name__ == '__main__':
    main()
