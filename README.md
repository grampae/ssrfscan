# ssrfscan
Modular ssrf port scanner that takes input from cli.  
Output is shown as status code and time to complete request.  
If response returns content and has a status code of 200, it will show that url for further investigation.  

![Screenshot from 2022-04-03 18-04-26](https://user-images.githubusercontent.com/36344197/161451602-0c5c4240-3482-4fb5-8f49-38db746e0ec5.png)


Example usage: python3 ssrfscan.py -s https://ssrf.vulnerable.site/?url= -c http:// -t 127.0.0.1 -p 80,443,31337,8080 -u /favicon.ico -e b64 -b

- -s site that is vulnerable to ssrf up to the point where the payload is introduced
- -c scheme of payload request such as http://, gopher://, netdoc:///, \\\ etc
- -t the target that is being port scanned
- -u target path to request, for image based ssrf think files that are common like favicon.ico etc
- -p comma seperated ports to scan, currently defaults to 21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080
- -e (url,b64) base64 or url encode the payload, this is everything after the -s flag
- -b Proxy requests through Burp

Reponses should look similar to the following depending on the ssrf and responses.
![Screenshot from 2022-03-30 10-39-55](https://user-images.githubusercontent.com/36344197/160861995-7d84fb3b-4ef3-416f-bfa4-fe90d8ae01dd.png)

If you see a feature that you would like added or suggestion for improvement please let me know.

