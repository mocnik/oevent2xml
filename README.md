# OEVENT2XML

OEVENT2XML exports results from OEVENT to [IOF Data Standsard 3.0](http://orienteering.org/resources/it/data-standard-3-0/) XML format. OEVENT needs to run in network mode using FirebirdSQL database server.

Additionally, the module sends the XML to a Slovenian orienteering federation web service.

## Example - generate XML

```python
import xml

conn = "192.168.1.5:C:\\Users\\smocnik\\AppData\\Roaming\\OEvent\\Data\\Competition10.gdb"

with open("r.xml", "wb") as f:
    f.write(oevent2xml.to_xml(conn))
```

## Example - send data to OZS
Run the service with:
```python run.py```

Configuration is in the `run.py` file. The first part takes care about connection to FireBird + generation of the XML file. 5 stages are supported for each event.

```python
# connection to FireBird
CONNECTION_STRING = "localhost:3050/C:\\Users\\Klemen\\AppData\\Roaming\\OEvent\\Data\\Competition11.gdb"
STAGE = 4
WAIT_TIME = 15
RESULTS_FILE = "results.xml"
```

Second part takes care about uploading to OZS pages:
```python
# connection to OZS
# set UPLOAD to False in case you do not want the data to be uploaded to OZS
UPLOAD = True
COMPETITION_ID = 9999
COMPETITION_SECRET = "0ae283bb8749abc3b3cc3e6bd3049d04"
UPLOAD_URL = "http://orientacijska-zveza.si/sl/api/live/upload.html"
```

## Dependencies:
* firebirdsql
* PyXB

## Usage with liveresultat:
* http://liveresultat.orientering.se/?lang=en
* http://liveresultat.orientering.se/adm/admincompetitions.php
* https://github.com/petlof/liveresults