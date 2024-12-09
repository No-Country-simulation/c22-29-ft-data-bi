from config_logs import logger
from constants import INTERMEDIATE_PATH
from constants import ENGINE
import pandas as pd
import pyarrow.feather as feather
import pyarrow as pa


def notification_to_update_fact_table(df: pa.Table, table: str):
    query = f"SELECT COUNT(*) AS total FROM {table}"
    total_in_db = pd.read_sql(query, con=ENGINE)['total'].iloc[0]

    total_in_df = len(df)

    if total_in_df > total_in_db:
        logger.info(
            f"Se detectaron {total_in_df - total_in_db} "
            "registros nuevos para insertar.")
    else:
        logger.info(f"No hay registros nuevos para insertar en {table}.")


if __name__ == '__main__':
    
    if not INTERMEDIATE_PATH.exists():
        logger.error('La carpeta no existe, ejecute primero el a01_transform.py')
        sys.exit()
    
    logger.info('Leyendo archivos feathers')
    
    beg_inv = feather.read_table(INTERMEDIATE_PATH.joinpath('a01_beginvfinal12312016.feather'))
    logger.info('Leyendo beg_inv')
    
    end_inv = feather.read_table(INTERMEDIATE_PATH.joinpath('a01_endinvfinal12312016.feather'))
    logger.info('Leyendo end_inv')
    
    sales = feather.read_table(INTERMEDIATE_PATH.joinpath('a01_salesfinal12312016.feather'))
    logger.info('Leyendo sales')
    
    purchases = feather.read_table(INTERMEDIATE_PATH.joinpath('a01_purchasesfinal12312016.feather'))
    logger.info('Leyendo purchases')
    
    invoice_purchases = feather.read_table(INTERMEDIATE_PATH.joinpath('a01_invoicepurchases12312016.feather'))
    logger.info('Leyendo invoice_purchases')

    table_feathers = {
        "beginvfinal12312016": beg_inv,
        "endinvfinal12312016": end_inv,
        "purchasesfinal12312016": purchases,
        "invoicepurchases12312016": invoice_purchases,
        "salesfinal12312016": sales
    }

    logger.info('Archivos feathers leídos')

    for table, df in table_feathers.items():
        notification_to_update_fact_table(df=df, table=table)