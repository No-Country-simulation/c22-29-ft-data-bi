import pyprojroot
from sqlalchemy import create_engine as ce
from decouple import config


ENGINE = ce(config('engine_mysql'))

chunk_size = 3000

ROOT_PATH = pyprojroot.here()

DATA_PATH = ROOT_PATH / 'data'

INTERMEDIATE_PATH = DATA_PATH / 'intermediate'

log_file_path = ROOT_PATH / 'logger.log'

columns_to_dimension = ['InventoryId', 'Store', 'Brand', 'Description', 'Size']
