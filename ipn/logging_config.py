import logging
import os

def setup_logging():
    log_dir = os.path.join(os.path.expanduser("~"), ".ipn")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logging.basicConfig(
        filename=os.path.join(log_dir, 'ipn.log'),
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
    )
    # Adding console handler for logging
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
