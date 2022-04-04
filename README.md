# ssrfscan
Modular ssrf port scanner that takes input from cli or burp request file  
GET/POST supported and you can proxy your request through burp  

The idea is that you can change http:// to gopher:// or /favicon.ico to /robots.txt etc without having to modify the rest of the request  

There are three ways to run ssrfscan  
1. -sss Provide full url including vulnerable ssrf site plus target you intend on scanning, define port location with *  
2. -ss Provide parts individually, ssrf url, schema, target, ports, path (only ssrf url, schema and target are required)  
3. -f Provide burp request file (define insertion point with the string 'ssrf', must define schema and target also -c http:// -t 127.0.0.1 etc)  

Optional:
1. -e b64 or -e url (encode payload with base64 or url encoding)
2. -ssl (used with -f, tell ssrfscan to use https:// instead of http://)
3. -b (proxy requests through burp)


![Screenshot from 2022-04-03 18-04-26](https://user-images.githubusercontent.com/36344197/161451602-0c5c4240-3482-4fb5-8f49-38db746e0ec5.png)

Output is shown as status code and time to complete request.  
If response returns content and has a status code of 200, it will show that url for further investigation.  

- Example: `ssrfscan.py -ss https://ssrf.vulnerable.site/?url= -s http:// -t 127.0.0.1 -p 80,443,31337,8080 -u /favicon.ico -e b64 -b`  
*Set site vulnerable to ssrf with -ss , http://127.0.0.1/favicon.ico will be requested on ports 80,443,31337,8080, base64 encoded, and proxied through burp*  
- Example: `ssrfscan.py -f getreq2.txt -t 127.0.0.1 -u /someplace/special.svg -s http:// -e url`  
*Request burp saved request file (must define insertion point as 'ssrf'), port scan http://127.0.0.1/someplace/special.svg, url encoded*  
- Example: `ssrfscan.py -sss 'https://somevulnerable.site/afile.aspx?url=http://127.0.0.1:*/index.html' -p 80,8080`  
*Simple method, provide whole ssrf url including target, define port location with '*'




Reponses should look similar to the following depending on the ssrf and responses.
![Screenshot from 2022-03-30 10-39-55](https://user-images.githubusercontent.com/36344197/160861995-7d84fb3b-4ef3-416f-bfa4-fe90d8ae01dd.png)

If you see a feature that you would like added or suggestion for improvement please let me know.

