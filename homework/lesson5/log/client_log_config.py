import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(name)-10s %(message)s',
    level=logging.INFO
)

logger = logging.getLogger('client')

formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(name)-10s %(message)s')
file_handler = logging.FileHandler('client.log', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def log_info(msg: str) -> None:
    """
    Логгинг инфо

    :param msg: сообщение для логгирования
    """
    logger.info(msg)


def log_debug(msg: str) -> None:
    """
    Логгинг дебага

    :param msg: сообщение для логгирования
    """
    logger.debug(msg)


def log_warning(msg: str) -> None:
    """
    Логгинг предупреждения

    :param msg: сообщение для логгирования
    """
    logger.warning(msg)


def log_error(msg: str) -> None:
    """
    Логгинг ошибки

    :param msg: сообщение для логгирования
    """
    logger.error(msg)


def log_critical(msg: str) -> None:
    """
    Логгинг критической ошибки

    :param msg: сообщение для логгирования
    """
    logger.critical(msg)


if __name__ == '__main__':
    log_info('Sample info message')
    log_debug('Sample debug message')
    log_warning('Sample warning message')
    log_error('Sample error message')
    log_critical('Sample critical message')
