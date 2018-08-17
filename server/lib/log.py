import logging
import sys

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
ch.setFormatter(logging.Formatter('[%(levelname)s]|[%(name)s - %(asctime)s]: %(message)s'))

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

log.addHandler(ch)
