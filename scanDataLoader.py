#!/usr/bin/env python

import MySQLdb

import sys
from xml.dom.minidom import parse
from xml.dom import Node
from pprint import pprint

scan_id = int(sys.argv[1])
scan_file = sys.argv[2]

dom = parse(scan_file)

db = MySQLdb.connect("localhost","www","geek","nessus")
cursor = db.cursor()

# clean any old elements for scan id
tsid = (scan_id,)
cursor.execute("delete from scan_hosts where scan_id=%s",tsid)
cursor.execute("delete from scan_host_items where scan_id=%s",tsid)
cursor.execute("delete from scan_host_info where scan_id=%s",tsid)
cursor.execute("delete from scan_item_info where scan_id=%s",tsid)

def quotify(x):
	return ("'%s'" % x)

def dquotify(x):
	return ("\"%s\"" % x)

ricount = 0

for host in dom.getElementsByTagName("ReportHost"):
	ip = host.getAttribute("name")
	print "ip=",ip
	qs = """insert into scan_hosts (scan_id,ip,ip_addr,ip_subnet) 
		values (%s,%s,inet_aton(%s),inet_aton(%s)&0xffffff00)"""
	vals = (scan_id,ip,ip,ip)
	print qs, vals
	cursor.execute(qs,vals)
	# get new id
	qs = "select last_insert_id() as host_id from scan_hosts limit 1"
	print qs
	cursor.execute(qs)
	data = cursor.fetchone()
	host_id = int(data[0])
#	host_id = 9998
	for item in host.childNodes:
		print "...",item.nodeName,ip
		if item.nodeName == "HostProperties":
			for child in item.childNodes:
				if child.nodeName == "tag" and child.attributes.has_key("name"):
					tag = child.attributes["name"].value
					value = child.childNodes[0].nodeValue
					qs = """insert into scan_host_info (scan_id,host_id,tag,value) 
							values (%s,%s,%s,%s)""" 
					vals = (scan_id,host_id,tag,value)
					print qs % vals
					cursor.execute(qs,vals)
		if item.nodeName == "ReportItem":
			attrnames = ['ip','scan_id','host_id']
			values = [ip,str(scan_id),str(host_id)]
			pholders = ['%s','%s','%s']
			for akey in item.attributes.keys():
				aval = item.attributes[akey]
				attrnames.append(akey)
				values.append(aval.value)
				pholders.append("%s")
			xfields = ",".join(attrnames)
			xvalues = ",".join(values)
			xholders = ",".join(pholders)

			print "fields=",xfields
			print "values=",xvalues
			print "phold=",xholders

			sqltmp1 = "insert into scan_host_items ("+xfields+") values ("+xholders+")" 
			print sqltmp1
			print values
			print sqltmp1 % tuple(values)
			cursor.execute(sqltmp1,tuple(values))

			# get last_insert_id()...
			ricount = ricount+1

			qs = "select last_insert_id() as N from scan_host_items limit 1"
			cursor.execute(qs)
			data = cursor.fetchone()
			last_id = int(data[0])
#			last_id = 9999
			print "last_id=",last_id,"type=",type(last_id)

			for child in item.childNodes:
				if child.nodeName != "#text":
					#print "   child:",child.nodeName,child.childNodes[0].nodeValue
					tmp = """insert into scan_item_info (scan_id,ritem_id,tag,value) 
							values (%s,%s,%s,%s)"""
					tag = child.nodeName
					text = child.childNodes[0].nodeValue
					vals = (scan_id,last_id,tag,text)
					sql2 = tmp % (scan_id,last_id,tag,text)
					print sql2
					cursor.execute(tmp,vals)

			# commit after each host record
			db.commit()
