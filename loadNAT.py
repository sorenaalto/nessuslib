#!/usr/bin/env python

import csv

with open('natlist.csv') as f:
	csvin = csv.reader(f)
	for r in csvin:
		ip1 = r[0].rstrip()
		ip2 = r[1].rstrip()

		if ip1.startswith('196'):
			ipout = ip1
			ipin = ip2
		else:
			ipout = ip2
			ipin = ip1

		print "insert into nat (ipout,ipin) values ('%s','%s')" % (ipout,ipin)



