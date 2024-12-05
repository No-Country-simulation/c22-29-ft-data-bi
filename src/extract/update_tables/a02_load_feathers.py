from config_logs import logger
from constants import INTERMEDIATE_PATH
import pandas as pd
import sys


if not INTERMEDIATE_PATH.exists():
    logger.error('La carpeta no existe, ejecute primero el a01_transform.py')
    sys.exit()

logger.info('Leyendo archivos feathers')

beg_inv = pd.read_feather(
    INTERMEDIATE_PATH.joinpath('a01_beginvfinal12312016.feather'))
end_inv = pd.read_feather(
    INTERMEDIATE_PATH.joinpath('a01_endinvfinal12312016.feather'))
sales = pd.read_feather(
    INTERMEDIATE_PATH.joinpath('a01_salesfinal12312016.feather'))
purchases = pd.read_feather(
    INTERMEDIATE_PATH.joinpath('a01_purchasesfinal12312016.feather'))
invoice_purchases = pd.read_feather(
    INTERMEDIATE_PATH.joinpath('a01_invoicepurchases12312016.feather'))


table_feathers = {
    "beginvfinal12312016": beg_inv,
    "endinvfinal12312016": end_inv,
    "purchasesfinal12312016": purchases,
    "invoicepurchases12312016": invoice_purchases,
    "salesfinal12312016": sales
}

logger.info('Archivos feathers leídos')
