import logging
import os

if not os.path.exists("logs"):
     os.makedirs("logs")

logging.basicConfig(
    filename="logs/srapper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)



def log_info(message):
     logging.info(message)

def log_error(message):
     logging.error(message)

def log_debug(message):
     logging.debug(message)

def log_warning(message):
     logging.warning(message)

def log_exception(message):
     logging.exception(message)

def start_process(process_name):
     logging.info(f"Starting process: {process_name}")

def end_process(process_name):
     logging.info(f"Ending process: {process_name}")