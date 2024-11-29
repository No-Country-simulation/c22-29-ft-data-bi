import logging
import pyprojroot
import pandas as pd
from sqlalchemy import create_engine as ce
# pip install python-decouple mysql-connector-python 
# o PyMySQL
from decouple import config
import time
import sys


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
log_file_path = ROOT_PATH / 'logging.log'

logging.basicConfig(
    format='%(asctime)-5s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler(log_file_path, mode='a', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ],
    datefmt='%A %d-%m-%Y %H:%M:%S'
)


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
        logging.info(f"Cargando datos de {archivo} a la tabla {tabla}...")
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
        
        logging.info(f"Datos de {archivo} cargados correctamente a la tabla {tabla}.")
        logging.info(f"Se procesaron {contador} chunks.")
    except Exception as e:
        logging.error(f"Error al cargar {archivo}: {e}")

end_time = time.perf_counter()
execution_time = end_time - start_time
minutes, seconds = divmod(execution_time, 60)

logging.debug(f"Tardó {int(minutes)} minutos {int(seconds)} segundos en ejecutarse.")
logging.info("Proceso de carga completado.")