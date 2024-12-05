from config_logs import logger
from constants import (
    ENGINE, columns_to_dimension
)
from a02_load_feathers import (
    beg_inv, end_inv, sales, purchases, invoice_purchases
)
import pandas as pd


def inventory() -> pd.DataFrame:
    sub_df1 = beg_inv[columns_to_dimension]
    sub_df2 = end_inv[columns_to_dimension]
    sub_df3 = sales[columns_to_dimension]
    sub_df4 = purchases[columns_to_dimension]

    inventario_df = pd.concat(
        [sub_df1, sub_df2, sub_df3, sub_df4], ignore_index=True
    )

    inventario_df = inventario_df.drop_duplicates(
        subset=['InventoryId'], keep='first'
    )

    logger.info('Crear inventario_df desde los feathers')
    return inventario_df


def vendors() -> pd.DataFrame:
    
    vendor_sales_unicos = sales[['VendorNo', 'VendorName']] \
        .drop_duplicates() \
        .sort_values('VendorNo') \
        .reset_index(drop=True)

    vendor_sales_unicos['VendorName'] = (
        vendor_sales_unicos['VendorName'].str.strip()
    )
    
    valores_unicos = invoice_purchases[['VendorNumber', 'VendorName']] \
        .drop_duplicates() \
        .sort_values('VendorNumber') \
        .reset_index(drop=True)

    valores_unicos['VendorName'] = valores_unicos['VendorName'].str.strip()
    
    vendor_purchases_unicos = purchases[['VendorNumber', 'VendorName']] \
        .drop_duplicates() \
        .sort_values('VendorNumber') \
        .reset_index(drop=True)

    vendor_purchases_unicos['VendorName'] = (
        vendor_purchases_unicos['VendorName'].str.strip()
    )
    
    vendor_purchases_unicos = (
        vendor_purchases_unicos
        .drop(
            vendor_purchases_unicos[
                vendor_purchases_unicos['VendorName'] == 'VINEYARD BRANDS INC'
            ].index
        )
    )
    
    vendor_purchases_unicos = (
        vendor_purchases_unicos
        .drop(
            vendor_purchases_unicos[
                vendor_purchases_unicos['VendorName'] == 'SOUTHERN WINE & SPIRITS NE'
            ].index
        )
    )

    valores_unicos = (
        valores_unicos
        .drop(
            valores_unicos[
                valores_unicos['VendorName'] == 'VINEYARD BRANDS INC'
            ].index
        )
    )
    
    valores_unicos = (
        valores_unicos
        .drop(
            valores_unicos[
                valores_unicos['VendorName'] == 'SOUTHERN WINE & SPIRITS NE'
            ].index
        )
    )
    
    vendor_sales_unicos.rename(
        columns={'VendorNo': 'VendorNumber'}, inplace=True
    )

    vendors_df = pd.concat(
        [valores_unicos, vendor_purchases_unicos, vendor_sales_unicos],
        ignore_index=True
    )
    
    vendors_df = vendors_df.drop_duplicates(
        subset=['VendorNumber'], keep='first'
    )
    logger.info('Crear vendors_df desde los feathers')
    return vendors_df


def check_new_records(df: pd.DataFrame, id: str, table: str):
    logger.debug(f"Consultando {table}")
    query = f"SELECT {id} FROM {table}"
    existing_ids = pd.read_sql(query, con=ENGINE)[id].tolist()
    
    new_data = df[~df[id].isin(existing_ids)]
    if not new_data.empty:
        new_data.to_sql(table, con=ENGINE, if_exists='append', index=False)
        logger.info(f"{len(new_data)} registros nuevos insertados en {table}.")
    else:
        logger.info(f"En {table} no hay datos nuevos para insertar.")


if __name__ == "__main__" :
    inventario_df = inventory()
    vendors_df = vendors()

    check_new_records(
        df=inventario_df, id='InventoryId', table='inventory')

    check_new_records(
        df=vendors_df, id='VendorNumber', table='vendors')