import logging

def setup_logger(name):
    """
    Function to set up a logger.
    """
    # Configure the logger
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("telegram_bot.log"),  # Log to a file
            logging.StreamHandler()  # Also log to console
        ]
    )
    # Create and return a logger
    logger = logging.getLogger(name)
    return logger
