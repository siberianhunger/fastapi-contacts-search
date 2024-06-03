import logging


def setup_logger(name=None):
    """
    Set up and return a logger with the specified name.
    If no name is provided, a root logger will be returned.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    ch.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(ch)

    return logger


if __name__ == "__main__":
    logger = setup_logger('example')
    logger.info('This is an info message')
