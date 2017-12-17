#!/usr/bin/python

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import json
import time

class nessusAPI:
	def __init__(self,debug=False):
		self.debug = debug
		# disable the annoying warning for self-signed SSL
		requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
		with open(".authtoken","r") as authf:
			self.authtoken = authf.read().replace("\n","")
		with open(".nessuscfg.json") as cfgf:
			self.cfg = json.load(cfgf)
			print "Loaded config:",self.cfg
		self.token_checked = False

	def getAuthToken(self):
		if self.token_checked:
			return self.authtoken

		session_url = self.cfg['base_url'] + "session/"
		self.authcookie = "token=%s" % (self.authtoken)
		self.authheaders = {"X-Cookie":self.authcookie}
		r = requests.get(session_url,headers=self.authheaders,verify=False)
		rsp = r.json()
		if rsp.has_key("error"):
			# login and generate new token
			creds = json.dumps({'username':self.cfg['username'],'password':self.cfg['password']})
			print creds
			headers = {'Content-type':'application/json'}
			r = requests.post(session_url,verify=False,data=creds,headers=headers)
			rsp = r.json()
			if self.debug:
				print "login, rsp=",rsp
			# extract token
			self.authtoken = rsp['token']
			self.authcookie = "token=%s" % (self.authtoken)
			self.authheaders = {"X-Cookie":self.authcookie}
			with open(".authtoken","w") as authf:
				authf.write(self.authtoken)
				print "new token saved"
		else:
			print "token is ok",rsp

		self.token_checked = True
		return self.authtoken

	def listScans(self):
		self.getAuthToken()
		scans_url = self.cfg['base_url'] + "scans/"
		r = requests.get(scans_url,headers=self.authheaders,verify=False)
		rsp = r.json()
		if self.debug:
			print json.dumps(rsp,indent=4)
		return rsp

	def scanInfo(self,scan_id):
		self.getAuthToken()
		scans_url = self.cfg['base_url'] + "scans/%d" % (scan_id)
		r = requests.get(scans_url,headers=self.authheaders,verify=False)
		rsp = r.json()
		if self.debug:
			print json.dumps(rsp,indent=4)
		return rsp

	def launchScan(self,scan_id):
		self.getAuthToken()
		launch_url = self.cfg['base_url'] + "scans/%d/launch" % (scan_id)
		r = requests.post(launch_url,headers=self.authheaders,verify=False)
		rsp = r.json()
		if self.debug:
			print json.dumps(rsp,indent=4)
		return rsp

	def requestReport(self,scan_id,history_id,format):
		self.getAuthToken()
		req_url = self.cfg['base_url'] +  "scans/%d/export?history_id=%d" % (scan_id,history_id)
		fdata = {"format":format}
		fdata_s = json.dumps(fdata)
		print "requestReport, data=",fdata,fdata_s
		r = requests.post(req_url,headers=self.authheaders,data=fdata,verify=False)
		rsp = r.json()
		if self.debug:
			print json.dumps(rsp,indent=4)
		return rsp	

	def exportStatus(self,scan_id,file_id):
		self.getAuthToken()
		req_url = self.cfg['base_url'] +  "scans/%d/export/%d/status" % (scan_id,file_id)
		r = requests.get(req_url,headers=self.authheaders,verify=False)
		rsp = r.json()
		if self.debug:
			print json.dumps(rsp,indent=4)
		return rsp	

	def downloadReport(self,scan_id,file_id,filename=None):
		self.getAuthToken()
		req_url = self.cfg['base_url'] +  "scans/%d/export/%d/download" % (scan_id,file_id)
		r = requests.get(req_url,headers=self.authheaders,verify=False)
		if filename == None:
			filename = "%d-%d" % (scan_id,file_id)
		with open(filename,'wb') as f:
			for block in r.iter_content(4096):
				f.write(block)

	
	def requestReportAndDownload(self,scan_id,history_id,format,filename=None):
		r = self.requestReport(scan_id,history_id,format)
		file_id = r['file']
		busy = True
		while busy:
			time.sleep(5)
			r = self.exportStatus(scan_id,file_id)
			status = r['status']
			if status == 'ready':
				busy = False
		self.downloadReport(scan_id,file_id,filename)

def main():
	api = nessusAPI()
	rsp = api.listScans()
	for scan in rsp["scans"]:
		print "Scan",scan["id"],scan["name"]
		api.scanInfo(scan["id"])

if __name__ == '__main__':
	main()
