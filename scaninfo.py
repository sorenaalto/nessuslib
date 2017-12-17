#!/usr/bin/env python
import sys
import nessuslib

scan_id = sys.argv[1]
sid = int(scan_id)

nessus = nessuslib.nessusAPI(debug=True)
x = nessus.scanInfo(sid)

