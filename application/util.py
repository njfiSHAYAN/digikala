import logging

def get_logger(severity="INFO"):
    logging.basicConfig(
        format="%(asctime)s  %(levelname)-6s %(filename)s:%(lineno)s - %(name)s.%(funcName)s()   %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger(__name__)
    logger.setLevel(getattr(logging, severity))
    return logger
