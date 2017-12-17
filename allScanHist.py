#!/usr/bin/env python

import time
import nessuslib

nessus = nessuslib.nessusAPI()
x = nessus.listScans()

slist = x['scans']
print "iterate over list of scans"
for scan in slist:
	print scan
	sid = scan['id']
	sname = scan['name']
	sinfo = nessus.scanInfo(sid)
	scanhist = sinfo['history']
	print "iterate of history list"
	for hist in scanhist:
		hid = hist['history_id']
		ts = hist['creation_date']
		stype = "nessus"
		fname = "dump/%s-%d.%s" % (sname,ts,stype)
		d1 = time.ctime(int(hist['creation_date']))
		d2 = time.ctime(int(hist['last_modification_date']))
		
		print sname,sid,hid,hist['uuid'],d1,d2
		#nessus.requestReportAndDownload(sid,hid,stype,fname)

