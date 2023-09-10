import logging
import datetime
# Configure the logger
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Create a logger instance
logger = logging.getLogger(__name__)

# Create a FileHandler that outputs logs to a file with a date-based filename
log_filename = datetime.datetime.now().strftime("%Y-%m-%d.log")
file_handler = logging.FileHandler(log_filename)

# Optionally, configure the log level for the file handler
file_handler.setLevel(logging.DEBUG)

# Create a formatter for the file handler
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)