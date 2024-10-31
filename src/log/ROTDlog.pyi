import logging


class ROTDLogging:
    def __init__(self, log_location: str) -> None:
        """
        Initialise ROTDLogging

        :param log_location: The location of the log file to be created
        """
        self.logger = None
        ...

    def get_logger(self) -> logging.Logger:
        """
        Get the logger object

        :return: Return the logger object

        """
        ...