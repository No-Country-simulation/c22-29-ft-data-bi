from config_logs import logger
from constants import DATA_PATH, INTERMEDIATE_PATH, chunk_size
import pyarrow.feather as feather
import pyarrow as pa
import pandas as pd
import sys


RAW_PATH = DATA_PATH / 'raw'

def process_and_save_to_feather(file_path, output_name, chunksize=chunk_size):
    """
    Lee un archivo CSV grande por chunks y lo guarda directamente en formato Feather.

    Args:
        file_path (str): Nombre del archivo CSV a procesar.
        output_name (str): Nombre base del archivo Feather de salida.
        chunksize (int): Número de filas por chunk (porción).
    """
    logger.info(f'Procesando archivo: {file_path}')
    try:
        feather_dir = INTERMEDIATE_PATH / output_name
        feather_dir.mkdir(parents=True, exist_ok=True)

        chunk_counter = 0
        for chunk in pd.read_csv(
            RAW_PATH.joinpath(file_path), chunksize=chunksize):
            
            chunk.drop(
                columns=['Store', 'Brand', 'Description', 'Size', 'VendorName'],
                inplace=True,
                errors='ignore'
            )
            
            if file_path == 'InvoicePurchases12312016.csv' and 'Approval' in chunk.columns:
                del chunk['Approval']

            if file_path == "SalesFINAL12312016.csv":
                chunk['SalesDate'] = pd.to_datetime(
                    chunk['SalesDate'], errors='coerce', format='%m/%d/%Y'
                )
                chunk['SalesDate'] = chunk['SalesDate'].dt.strftime('%Y-%m-%d')

            feather_file = feather_dir / f"{output_name}_chunk_{chunk_counter}.feather"
            chunk.reset_index(drop=True).to_feather(feather_file)

            logger.info(f'Guardado chunk {chunk_counter} en {feather_file}')
            chunk_counter += 1

        logger.info(f'Archivo procesado y guardado en {feather_dir}')
    except Exception as e:
        logger.error(f"Error procesando {file_path}: {e}")
        sys.exit(1)


def concatenate_feather_with_pyarrow(output_name):
    feather_dir = INTERMEDIATE_PATH / output_name
    feather_files = sorted(feather_dir.glob("*.feather"))

    if not feather_files:
        logger.warning(f"No se encontraron archivos Feather en {feather_dir}.")
        return

    logger.info(f"Concatenando {len(feather_files)} archivos Feather para {output_name}...")

    concatenated_table = None

    for i, feather_file in enumerate(feather_files):
        table = feather.read_table(feather_file)
        concatenated_table = table if concatenated_table is None else pa.concat_tables([concatenated_table, table])
        logger.info(f"Archivo {i + 1}/{len(feather_files)} procesado: {feather_file}")

    output_file = INTERMEDIATE_PATH / f"a01_{output_name}.feather"
    feather.write_feather(concatenated_table, output_file)
    logger.info(f"Archivo Feather concatenado guardado en: {output_file}")


if __name__ == "__main__":
    if not RAW_PATH.exists():
        logger.error('La carpeta RAW_PATH no existe. Ejecute primero download_from_gdrive.py')
        sys.exit()

    if INTERMEDIATE_PATH.exists():
        logger.info(f'Limpiando carpeta: {INTERMEDIATE_PATH}')
        for file in INTERMEDIATE_PATH.rglob("*"):
            if file.is_file():
                file.unlink()

    INTERMEDIATE_PATH.mkdir(parents=True, exist_ok=True)

    process_and_save_to_feather(
        'BegInvFINAL12312016.csv', 'beginvfinal12312016')
    process_and_save_to_feather(
        'EndInvFINAL12312016.csv', 'endinvfinal12312016')
    process_and_save_to_feather(
        'PurchasesFINAL12312016.csv', 'purchasesfinal12312016')
    process_and_save_to_feather(
        'InvoicePurchases12312016.csv', 'invoicepurchases12312016')
    process_and_save_to_feather(
        'SalesFINAL12312016.csv', 'salesfinal12312016')


    concatenate_feather_with_pyarrow('beginvfinal12312016')
    concatenate_feather_with_pyarrow('endinvfinal12312016')
    concatenate_feather_with_pyarrow('purchasesfinal12312016')
    concatenate_feather_with_pyarrow('invoicepurchases12312016')
    concatenate_feather_with_pyarrow('salesfinal12312016')

    logger.info('Procesamiento completo y archivos finales guardados.')
