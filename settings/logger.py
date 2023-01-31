import logging


def set_logger(name: str) -> logging.Logger:
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s %(module)s %(levelname)s] %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S'
    )
    return logging.getLogger(name)


logger = set_logger(__name__)
