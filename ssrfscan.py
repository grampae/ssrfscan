#!/usr/bin/python3
#modular ssrf portscan

import sys
import re
import argparse
import requests
import signal
import urllib3
import os
import base64
import Burpee.burpee
import json

parser = argparse.ArgumentParser(description="ssrf portscan", formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-sss", dest="sssrfurl", required=False, help="Standalone GET: Provide full ssrf url with schema, target and path, must define port with *", default="")
parser.add_argument("-ss", dest="ssrfurl", required=False, help="SSRF GET url, will need to define schema and target at minimum", default="")
parser.add_argument("-s", dest="scheme", required=False, help="Define schema, ex: http://, netdoc:///, gopher://", default="")
parser.add_argument("-t", dest="target", required=False, help="Target to scan, ex: 127.0.0.1", default="")
parser.add_argument("-p", dest="ports", required=False, help="Comma seperated ports to scan", default="21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080")
parser.add_argument("-u", dest="path", required=False, help="Path to request from target", default="")
parser.add_argument("-e", dest="enc", required=False, help="Encode payload (choose b64 or url)")
parser.add_argument("-ssl", dest="https", required=False, help="Use https instead of http with burp file", action="store_true")
parser.add_argument("-f", dest="filename", required=False, type=argparse.FileType("r", encoding="UTF-8"), help="Burp request file")
parser.add_argument("-b", dest="prox", required=False, help="Proxy through burp", action="store_true")

args = parser.parse_args()
if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)

sssrfurl = args.sssrfurl
burpfile = args.filename
path = args.path
ssrfurl = args.ssrfurl
ports = args.ports.split(",")
target = args.target
enc = args.enc
https = args.https
scheme = args.scheme
prox = args.prox
col = ":"
urlscan = ""
headers = ""
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
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
    try:
        target2 = scheme+target+col+port+path
        def getreq():
            r = requests.get(urlscan, headers=headers, verify=False, timeout=12, allow_redirects=False, proxies=proxies)
            restime = str(r.elapsed.total_seconds())
            print("[-] Response from ("+target+":"+port+")  "+str(r.status_code)+" / "+restime+" ")
        def response():    
            if r.text and r.status_code == 200:
                print("[#] "+urlscan)
        if sssrfurl:
            urlscan = re.sub("[*]", port, sssrfurl)
            target = 'target'
            getreq()
            response()
        elif ssrfurl:
            if enc == 'b64':
                b = base64.b64encode(bytes(target2, 'utf-8'))
                urlscan = ssrfurl + b.decode('utf-8')
            elif enc == 'url':
                urlscan = ssrfurl + requests.utils.quote(target2)
            else:
                urlscan = ssrfurl+target2
            getreq()
            response()
        elif burpfile:
            if enc == 'b64':
                b = base64.b64encode(bytes(target2, 'utf-8'))
                target2 = b.decode('utf-8')
            elif enc == 'url':
                target2 = requests.utils.quote(target2)
            headers, post_data = Burpee.burpee.parse_request(burpfile.name)
            method_name, resource = Burpee.burpee.get_method_and_resource(burpfile.name)
            path2 = json.loads(re.sub('ssrf', target2, json.dumps(resource)))
            headers = json.loads(re.sub('ssrf', target2, json.dumps(headers)))
            post_data = json.loads(re.sub('ssrf', target2, json.dumps(post_data)))
            target3 = headers["Host"]
            protocol = "https" if (https is True) else "http"
            urlscan = protocol + "://" + headers["Host"] + path2
            if method_name.lower() == "get":
                r = requests.get(urlscan, headers=headers, verify=False, timeout=12, allow_redirects=False, proxies=proxies)
                restime = str(r.elapsed.total_seconds())
                print("[-] Response from ("+target3+":"+port+")  "+str(r.status_code)+" / "+restime+" ")
                response()
            elif method_name.lower() == "post":
                r = requests.post(urlscan , headers = headers , data = post_data , proxies = proxies , verify = False, timeout=12, allow_redirects=False)
                restime = str(r.elapsed.total_seconds())
                print("[-] Response from ("+target3+":"+port+")  "+str(r.status_code)+" / "+restime+" ")
                response()
    except requests.exceptions.ProxyError:
       print("[!] Cannot connect to proxy")        
    except requests.exceptions.Timeout:
       print("[!] Response from ("+target+":"+port+") Response Timeout")
       continue