#!/usr/bin/env python

import time
import nessuslib

import MySQLdb

user = "www"
passwd = "geek"
dbname = "nessus"

db = MySQLdb.connect("localhost",user,passwd,dbname)
c = db.cursor()
qs = "select * from scans"
c.execute(qs)
rows = c.fetchall()
uuids_seen = set()
for row in rows:
	scan_uuid = row[4]
	uuids_seen.add(scan_uuid)


nessus = nessuslib.nessusAPI()
x = nessus.listScans()

slist = x['scans']
print "iterate over list of scans"
for scan in slist:
	#print scan
	sid = scan['id']
	sname = scan['name']
	print "Scan",sid,sname
	sinfo = nessus.scanInfo(sid)
	scanhist = sinfo['history']
	if scanhist == None:
		scanhist = []
	print "iterate of history list"
	for hist in scanhist:
		stat = hist['status']
		hid = hist['history_id']
		ts = hist['creation_date']
		uuid = hist['uuid']
		ctime = int(hist['creation_date'])
		lmtime = int(hist['last_modification_date'])
		d1 = time.ctime(ctime)
		d2 = time.ctime(lmtime)
		print "...scan history",hid,d1
		if uuid in uuids_seen or stat != "completed":
			print "...",uuid,"already seen, skipping"
			pass
		else:
			print "...downloading scan file"
			stype = "nessus"
			fname = "dump/%s-%d.%s" % (sname,ts,stype)
		
			values = (sname,sid,hid,uuid,ctime,lmtime,fname)
			print values

			qs = """insert into scans (scan_name,scan_id,hist_id,scan_uuid,starttime,endtime,xmlfilename)
				values ('%s',%s,%s,'%s', FROM_UNIXTIME(%d), FROM_UNIXTIME(%d),'%s')""" % values
			print qs
			c.execute(qs)
			print "...requesting scan report"
			nessus.requestReportAndDownload(sid,hid,stype,fname)
			print "...report data saved in",fname
			c.execute("commit")
print "done, hey"
