import logging
import pyprojroot
import pandas as pd
from sqlalchemy import create_engine as ce
# pip install python-decouple mysql-connector-python 
# o PyMySQL
from decouple import config
import time


chunk_size = 3000

ROOT_PATH = pyprojroot.here()

DATA_PATH = ROOT_PATH / 'data'

engine = ce(config('engine_mysql'))
"""
Para el .env
engine_mysql = mysql+mysqlconnector://usuario:contrasena@localhost:3306/database
engine_mysql = mysql+pymysql://usuario:contrasena@localhost:3306/database
"""

# Para hacer logging
log_file_path = ROOT_PATH / 'logger.log'

logger = logging.getLogger('c22-29-ft-data-bi')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(log_file_path, mode='a')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Lista de archivos CSV y sus tablas correspondientes
archivos_tablas = {
    'BegInvFINAL12312016.csv': "beginvfinal12312016",
    'EndInvFINAL12312016.csv': "endinvfinal12312016",
    'PurchasesFINAL12312016.csv': "purchasesfinal12312016",
    'InvoicePurchases12312016.csv': "invoicepurchases12312016",
    'SalesFINAL12312016.csv': "salesfinal12312016",
}

# Cargar cada archivo CSV a su respectiva tabla
start_time = time.perf_counter()

for archivo, tabla in archivos_tablas.items():
    try:
        logger.info(f"Cargando datos de {archivo} a la tabla {tabla}...")
        contador = 0
        for chunk in pd.read_csv(
            DATA_PATH.joinpath(archivo), chunksize=chunk_size
        ):
            chunk.drop(
                columns=['Store', 'Brand', 'Description', 'Size', 'VendorName'],
                inplace=True,
                errors='ignore'
            )
            
            if archivo == 'InvoicePurchases12312016.csv':
                del chunk['Approval']

            if archivo == "SalesFINAL12312016.csv":
                chunk['SalesDate'] = pd.to_datetime(
                    chunk['SalesDate'], errors='coerce', format='%m/%d/%Y')
                chunk['SalesDate'] = chunk['SalesDate'].dt.strftime('%Y-%m-%d')
            
            print(f"Procesa chunk {contador + 1} para el {archivo}...")
            chunk.to_sql(tabla, con=engine, if_exists="append", index=False)
            contador += 1
        
        logger.info(f"Datos de {archivo} cargados correctamente a la tabla {tabla}.")
        logger.info(f"Se procesaron {contador} chunks.")
    except Exception as e:
        logger.error(f"Error al cargar {archivo}: {e}")

end_time = time.perf_counter()
execution_time = end_time - start_time
minutes, seconds = divmod(execution_time, 60)

logger.debug(f"Tardó {int(minutes)} minutos {int(seconds)} segundos en ejecutarse.")
logger.info("Proceso de carga completado.")