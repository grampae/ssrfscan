# ssrfscan
Modular ssrf port scanner that takes input from cli or burp request file.  
Output is shown as status code and time to complete request.  
If response returns content and has a status code of 200, it will show that url for further investigation.  

![Screenshot from 2022-04-03 18-04-26](https://user-images.githubusercontent.com/36344197/161451602-0c5c4240-3482-4fb5-8f49-38db746e0ec5.png)


- Example: `ssrfscan.py -ss https://ssrf.vulnerable.site/?url= -c http:// -t 127.0.0.1 -p 80,443,31337,8080 -u /favicon.ico -e b64 -b`  
*Set site vulnerable to ssrf with -ss , http://127.0.0.1/favicon.ico will be requested on ports 80,443,31337,8080, base64 encoded, and proxied through burp*  
- Example: `ssrfscan.py -f getreq2.txt -t 127.0.0.1 -u /someplace/special.svg -s http:// -e url`  
*Request burp saved request file (must define insertion point as 'ssrf'), port scan http://127.0.0.1/someplace/special.svg, url encoded*  
- Example: `ssrfscan.py -sss 'https://somevulnerable.site/afile.aspx?url=http://127.0.0.1:*/index.html' -p 22,21`  
*Simple method, provide whole ssrf url including target, define port location with '*'




Reponses should look similar to the following depending on the ssrf and responses.
![Screenshot from 2022-03-30 10-39-55](https://user-images.githubusercontent.com/36344197/160861995-7d84fb3b-4ef3-416f-bfa4-fe90d8ae01dd.png)

If you see a feature that you would like added or suggestion for improvement please let me know.

