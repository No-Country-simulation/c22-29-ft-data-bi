import logging
import pyprojroot
from decouple import config
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.service_account import Credentials
import time
import io
import os
import sys
import shutil


ROOT_PATH = pyprojroot.here()

SERVICE_ACCOUNT_PATH = ROOT_PATH / 'src' / 'extract'

SERVICE_ACCOUNT_FILE = SERVICE_ACCOUNT_PATH.joinpath(
    config('SERVICE_ACCOUNT_FILE')
)

DATA_PATH = ROOT_PATH / 'data'

FOLDER_ID = config('id_carpeta')

# Para hacer logging
log_file_path = ROOT_PATH / 'logger.log'

logging.basicConfig(
    format='%(asctime)-5s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler(log_file_path, mode='a', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ],
    datefmt='%A %d-%m-%Y %H:%M:%S'
)


start_time = time.perf_counter()

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
drive_service = build('drive', 'v3', credentials=credentials)


def list_files_in_folder(folder_id):
    query = f"'{folder_id}' in parents and trashed=false"
    results = drive_service.files().list(
        q=query, fields="files(id, name)"
    ).execute()
    return results.get('files', [])


def download_file(file_id, file_name, save_path):
    request = drive_service.files().get_media(fileId=file_id)
    file_path = os.path.join(save_path, file_name)
    with io.FileIO(file_path, 'wb') as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            logging.info(
                f"Downloading {file_name}: {int(status.progress() * 100)}%")
    logging.info(f"{file_name} descargado en {file_path}")


if os.path.exists(DATA_PATH):
    shutil.rmtree(DATA_PATH)

os.makedirs(DATA_PATH)
gitkeep_path = DATA_PATH.joinpath('.gitkeep')
with open(gitkeep_path, "w") as archivo:
    pass
logging.info("Crear directorio data")

files = list_files_in_folder(FOLDER_ID)
if not files:
    logging.warning("No se encontraron archivos en la carpeta.")
else:
    for file in files:
        logging.info(f"Descargando {file['name']}...")
        download_file(file['id'], file['name'], DATA_PATH)

end_time = time.perf_counter()
execution_time = end_time - start_time
minutes, seconds = divmod(execution_time, 60)

logging.debug(f"Tardó {int(minutes)} minutos {int(seconds)} segundos en ejecutarse.")
