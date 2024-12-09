from config_logs import logger
from constants import (
    SERVICE_ACCOUNT_FILE, DATA_PATH, RAW_PATH, INTERMEDIATE_PATH, FOLDER_ID
)
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.service_account import Credentials
import time
import io
import os
import sys
import shutil


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
            logger.info(
                f"Downloading {file_name}: {int(status.progress() * 100)}%")
    logger.info(f"{file_name} descargado en {file_path}")


if os.path.exists(DATA_PATH):
    shutil.rmtree(DATA_PATH)

os.makedirs(DATA_PATH)
os.makedirs(RAW_PATH)
gitkeep_path = DATA_PATH.joinpath('.gitkeep')
with open(gitkeep_path, "w") as archivo:
    pass
logger.info("Crear directorio data")

files = list_files_in_folder(FOLDER_ID)
if not files:
    logger.warning("No se encontraron archivos en la carpeta.")
else:
    for file in files:
        logger.info(f"Descargando {file['name']}...")
        download_file(file['id'], file['name'], RAW_PATH)

end_time = time.perf_counter()
execution_time = end_time - start_time
minutes, seconds = divmod(execution_time, 60)

logger.debug(f"Tardó {int(minutes)} minutos {int(seconds)} segundos en ejecutarse.")
