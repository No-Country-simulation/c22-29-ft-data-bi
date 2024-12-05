from config_logs import logger
from constants import ENGINE
from a02_load_feathers import table_feathers
import pandas as pd


def notification_to_update_fact_table(df: pd.DataFrame, table: str):
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
    for table, df in table_feathers.items():
        notification_to_update_fact_table(df=df, table=table)