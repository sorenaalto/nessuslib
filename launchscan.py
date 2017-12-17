#!/usr/bin/env python
import sys
import nessuslib

scan_id = sys.argv[1]
sid = int(scan_id)

nessus = nessuslib.nessusAPI()
x = nessus.launchScan(sid)

