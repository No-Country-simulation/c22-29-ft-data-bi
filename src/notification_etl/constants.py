import pyprojroot
from sqlalchemy import create_engine as ce
from decouple import config


ENGINE = ce(config('engine_mysql'))

ROOT_PATH = pyprojroot.here()

SERVICE_ACCOUNT_PATH = ROOT_PATH / 'src' / 'extract'

SERVICE_ACCOUNT_FILE = SERVICE_ACCOUNT_PATH.joinpath(
    config('SERVICE_ACCOUNT_FILE')
)

chunk_size = 3000

ROOT_PATH = pyprojroot.here()

DATA_PATH = ROOT_PATH / 'data'

RAW_PATH = DATA_PATH / 'raw'

INTERMEDIATE_PATH = DATA_PATH / 'intermediate'

FOLDER_ID = config('id_carpeta')

log_file_path = ROOT_PATH / 'logger.log'

columns_to_dimension = ['InventoryId', 'Store', 'Brand', 'Description', 'Size']
