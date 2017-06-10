""" Script for constant update of results from OEVENT database """
import logging
from time import sleep

import oevent2xml

CONNECTION_STRING = "192.168.1.5:C:\\Users\\smocnik\\AppData\\Roaming\\OEvent\\Data\\Competition10.gdb"
WAIT_TIME = 30
RESULTS_FILE = "results.xml"

LOGGER = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s", level=logging.INFO)

while True:
    try:
        with open(RESULTS_FILE, "wb") as f:
            f.write(oevent2xml.to_xml(CONNECTION_STRING))
        LOGGER.info("Successfully updated %s", RESULTS_FILE)
    except (SystemExit, KeyboardInterrupt):
        raise
    except Exception as exception:
        LOGGER.exception("Failed during update")
    finally:
        sleep(WAIT_TIME)
