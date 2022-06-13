""" Script for constant update of results from OEVENT database """
import logging
from time import sleep

import oevent2xml
import requests

# connection to FireBird
CONNECTION_STRING = "localhost:3050/C:\\Users\\Klemen\\AppData\\Roaming\\OEvent\\Data\\Competition9.gdb"
WAIT_TIME = 10
RESULTS_FILE = "results.xml"

# connection to OZS
# set UPLOAD to False in case you do not want the data to be uploaded to OZS
UPLOAD = True
COMPETITION_ID = 1904
COMPETITION_SECRET = "69edbd48b11d6dc71b19e8baf380edd1"
UPLOAD_URL = "http://orientacijska-zveza.si/sl/api/live/upload.html"

LOGGER = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s", level=logging.INFO)

while True:
    try:
        # write to file
        with open(RESULTS_FILE, "wb") as f:
            f.write(oevent2xml.to_xml(CONNECTION_STRING))
        LOGGER.info("Successfully updated %s", RESULTS_FILE)

        # post to OZS website
        if (UPLOAD):
            requests.post(UPLOAD_URL, data={
                "id": COMPETITION_ID,
                "secret": COMPETITION_SECRET,
                "live": oevent2xml.to_xml(CONNECTION_STRING)
            })
            LOGGER.info("Successfully uploaded to OZS, event %d", COMPETITION_ID)

    except (SystemExit, KeyboardInterrupt):
        raise
    except Exception as exception:
        LOGGER.exception("Failed during update")
    finally:
        sleep(WAIT_TIME)
