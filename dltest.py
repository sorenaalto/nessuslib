#!/usr/bin/env python
import sys
import nessuslib

scan_id = sys.argv[1]
sid = int(scan_id)

nessus = nessuslib.nessusAPI()
x = nessus.scanInfo(sid)
sname = x['info']['name']
history = x['history'][0]
hid = history['history_id']
ts = history['creation_date']
stype = "nessus"
fname = "%s-%s.%s" % (sname,ts,stype)

nessus.requestReportAndDownload(sid,hid,stype,fname)
