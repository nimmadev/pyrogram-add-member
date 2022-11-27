import logging
import sys
def pamlog(name):
    # create logger Name PAM
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(logging.INFO)
    if not logger.hasHandlers():
    # create console handler and set level to INFO
        pam = logging.StreamHandler()
        pam.setLevel(logging.INFO)
        
        # create formatter For PAM
        formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        
        # add formatter to pam
        pam.setFormatter(formatter)
        
        # add ch to logger
        logger.addHandler(pam)
    else:
        pass
    return logger
