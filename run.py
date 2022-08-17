""" Script for constant update of results from OEVENT database """
import logging
from time import sleep

import oevent2xml
import requests

# connection to FireBird
CONNECTION_STRING = "localhost:3050/C:\\Users\\Klemen\\AppData\\Roaming\\OEvent\\Data\\Competition11.gdb"
STAGE = 4
WAIT_TIME = 15
RESULTS_FILE = "results.xml"

# connection to OZS
# set UPLOAD to False in case you do not want the data to be uploaded to OZS
UPLOAD = True
COMPETITION_ID = 1858
COMPETITION_SECRET = "0ae283bb8749abc3b3cc3e6bd3049d04"
# ozs1855 ee6d842a2ef75491c9098fb802e9125b
# ozs1856 a82434b606afdc06df532ca16cf9f65c
# ozs1857 82d1b54016b992c984eebd820a14c0ad
# ozs1858 0ae283bb8749abc3b3cc3e6bd3049d04
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
            x = requests.post(UPLOAD_URL, data={
                "id": COMPETITION_ID,
                "secret": COMPETITION_SECRET,
                "live": oevent2xml.to_xml(CONNECTION_STRING, STAGE)
            })
            # print(x.text)
            if x.status_code == 200 and x.text == "OK":
                LOGGER.info("Successfully uploaded to OZS, event %d, stage %d", COMPETITION_ID, STAGE)
            else:
                LOGGER.error("Error: %s", x.text)

    except (SystemExit, KeyboardInterrupt):
        raise
    except Exception as exception:
        LOGGER.exception("Failed during update")
    finally:
        sleep(WAIT_TIME)
