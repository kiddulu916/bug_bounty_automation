import logging
import os

def setup_logger(name="bughunt"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # Stream handler
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
        logger.addHandler(stream_handler)

    return logger

def setup_error_logger(target):
    os.makedirs(f"outputs/{target}", exist_ok=True)
    error_log_path = f"outputs/{target}/recon_errors.log"
    error_logger = logging.getLogger(f"error_{target}")
    error_logger.setLevel(logging.ERROR)

    if not error_logger.handlers:
        fh = logging.FileHandler(error_log_path)
        fh.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s"))
        error_logger.addHandler(fh)

    return error_logger
