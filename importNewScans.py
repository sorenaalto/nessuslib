#!/usr/bin/env python

from datetime import datetime
import os
import nessuslib

import MySQLdb

user = "www"
passwd = "geek"
dbname = "nessus"

db = MySQLdb.connect("localhost",user,passwd,dbname)
c = db.cursor()
qs = "select * from scans where loadstat is NULL"
c.execute(qs)
rows = c.fetchall()
#arow = c.fetchone()
for row in rows:
		print row
		scan_id = row[0]
		filename = row[7]
		print scan_id,filename
		loadmsg = "START %s loading scan_id=%d from %s" % (datetime.now(),scan_id,filename)
		qs = "update scans set loadstat='%s' where id=%d" % (loadmsg,scan_id)
		print qs
		c.execute(qs)
		cmd = "./scanDataLoader.py %d \"%s\"" % (scan_id,filename)
		print cmd
		os.system(cmd)
		loadmsg = "END %s loading scan_id=%d from %s" % (datetime.now(),scan_id,filename)
		qs = "update scans set loadstat='%s' where id=%d" % (loadmsg,scan_id)
		print qs
		c.execute(qs)
		c.execute("commit")
