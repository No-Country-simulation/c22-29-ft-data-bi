from config_logs import logger
from constants import ROOT_PATH
import subprocess


update_path = ROOT_PATH / 'src' / 'extract' / 'update_tables'


def execute_script(script_name):
    """Ejecuta un script Python en la misma carpeta."""
    try:
        script_path = update_path.joinpath(script_name)
        logger.info(f"Ejecutando: {script_path}")
        
        subprocess.run(['python', script_path], check=True)
        
        logger.info(f"Finalizado: {script_path}\n")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error al ejecutar {script_name}: {e}")
    except Exception as e:
        logger.error(f"Error inesperado: {e}")

if __name__ == "__main__":
    scripts = [
        "a01_transform.py",
        "a02_load_feathers.py",
        "a03_load_dimensions.py",
        "a04_load_facts.py"
    ]
    
    for script in scripts:
        execute_script(script)
