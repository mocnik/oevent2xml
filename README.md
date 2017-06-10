# OEVENT2XML

OEVENT2XML exports results from OEVENT to [IOF Data Standsard 3.0](http://orienteering.org/resources/it/data-standard-3-0/) XML format. OEVENT needs to run in network mode using FirebirdSQL database server.

## Example

```python
import xml

conn = "192.168.1.5:C:\\Users\\smocnik\\AppData\\Roaming\\OEvent\\Data\\Competition10.gdb"

with open("r.xml", "wb") as f:
    f.write(oevent2xml.to_xml(conn))
```

## Dependencies:
* firebirdsql
* PyXB

## Usage with liveresultat:
* http://liveresultat.orientering.se/?lang=en
* http://liveresultat.orientering.se/adm/admincompetitions.php
* https://github.com/petlof/liveresults 