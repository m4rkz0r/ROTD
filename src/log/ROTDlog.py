import logging


class ROTDLogging:
    def __init__(self, log_location):
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(log_location),
                logging.StreamHandler()
            ])

        self.logger = logging.getLogger(__name__)

    def get_logger(self):
        # Return logger
        return self.logger
