#!/usr/bin/env python

import nessuslib

nessus = nessuslib.nessusAPI(debug=True)
x = nessus.listScans()

