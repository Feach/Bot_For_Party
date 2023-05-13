from loguru import logger


def logger_start():
    logger.add("debug.log", format="{time} {level} {message}",
               level="DEBUG", rotation="00:00", compression='zip')
    print("Логирование запушено.")

