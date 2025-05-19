import logging
import sys
import os

LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def configurar_logging(nivel=logging.INFO, log_file="logs/app.log"):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logging.basicConfig(
        level=nivel,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),        # Log no terminal
            logging.FileHandler(log_file, encoding="utf-8")  # Log no arquivo
        ]
    )
