import logging
from util.settings import DEBUG

def get_logger(name:str):
    #default = "__app__"
    logger = logging.getLogger(name)
    formatter = logging.Formatter('%(levelname)-8s: %(asctime)s | %(filename)-12s - %(funcName)-12s : %(lineno)-4s -- %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
    
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    log_map = {"__app__": "app.log"}
    if name == "__app__":
        fh = logging.FileHandler(log_map[name])
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
    if DEBUG:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    return logger