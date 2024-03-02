import logging

class Logger:
    def __init__(self):
        self.logger = logging.getLogger('my_logger')
        self.logger.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler('db_errors.log')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def error(self, message):
        self.logger.error(message)