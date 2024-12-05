from config_logs import logger
from constants import DATA_PATH, INTERMEDIATE_PATH, chunk_size
import pandas as pd
import os
import sys
import shutil


RAW_PATH = DATA_PATH / 'raw'


def read_large_csv(file_path, chunksize=chunk_size):
    """
    Lee un archivo CSV grande por chunks
    y concatena las partes en un solo DataFrame.

    Args:
        file_path (str): Ruta al archivo CSV.
        chunksize (int): Número de filas por chunk (porción).
    
    Returns:
        pd.DataFrame: DataFrame con todos los datos concatenados.
    """
    logger.info(f'Leyendo {file_path}')
    chunks = []
    for chunk in pd.read_csv(RAW_PATH.joinpath(file_path), chunksize=chunksize):
        if file_path == 'InvoicePurchases12312016.csv':
                del chunk['Approval']

        if file_path == "SalesFINAL12312016.csv":
            chunk['SalesDate'] = pd.to_datetime(
                chunk['SalesDate'], errors='coerce', format='%m/%d/%Y')
            chunk['SalesDate'] = chunk['SalesDate'].dt.strftime('%Y-%m-%d')
        chunks.append(chunk)
    logger.info(f'Leído {file_path}')
    return pd.concat(chunks, ignore_index=True)


def save_to_feather(df, feather: str):
    """
    Guardando en archivo feather en la carpeta `intermediate`
    """
    file_path = INTERMEDIATE_PATH.joinpath(f'a01_{feather}.feather')
    df.to_feather(file_path)
    logger.info(f'Guardado en {file_path}')



if __name__ == "__main__" :
    
    if not RAW_PATH.exists():
        logger.error('La carpeta no existe, ejecute primero download_from_gdrive.py')
        sys.exit()

    if INTERMEDIATE_PATH.exists():
        shutil.rmtree(INTERMEDIATE_PATH)

    os.makedirs(INTERMEDIATE_PATH)
    
    beg_inv_final_12312016 = read_large_csv('BegInvFINAL12312016.csv')
    end_inv_final_12312016 = read_large_csv('EndInvFINAL12312016.csv')
    purchases_final_12312016 = read_large_csv('PurchasesFINAL12312016.csv')
    invoice_purchases_12312016 = read_large_csv('InvoicePurchases12312016.csv')
    sales_final_12312016 = read_large_csv('SalesFINAL12312016.csv')


    save_to_feather(beg_inv_final_12312016, 'beginvfinal12312016')
    save_to_feather(end_inv_final_12312016, 'endinvfinal12312016')
    save_to_feather(purchases_final_12312016, 'purchasesfinal12312016')
    save_to_feather(invoice_purchases_12312016, 'invoicepurchases12312016')
    save_to_feather(sales_final_12312016, 'salesfinal12312016')