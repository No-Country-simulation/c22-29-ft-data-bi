from constants import log_file_path
import logging
import sys


logging.basicConfig(
    format='%(asctime)-5s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler(log_file_path, mode='a', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ],
    datefmt='%A %d-%m-%Y %H:%M:%S'
)


logger = logging.getLogger(__name__)
