# ssrfscan
Modular ssrf port scanner with response codes and timing.

![Screenshot from 2022-03-30 10-03-54](https://user-images.githubusercontent.com/36344197/160858502-a61b39b5-5ede-43b7-b59d-b749a9119e0b.png)

Usage: python3 ssrfscan.py -s https://ssrf.vulnerable.site/?url= -m \\ -t 127.0.0.1 -f /favicon.ico -p 80,443,31337,8080

- -s site that is vulnerable to ssrf up to the point where the payload is introduced.
- -m method of payload request such as http://, gopher://, netdoc:///, \\ etc
- -t the target that is being port scanned
- -f the file at target that is being grabbed, for image based ssrf think files that are common like favicon.ico etc
- -p ports to scan, currently defaults to 21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080
- -b base64 encode the payload, this is everything after the -s flag

Reponses should look similar to the following depending on the ssrf and environments
![Screenshot from 2022-03-30 10-39-55](https://user-images.githubusercontent.com/36344197/160861995-7d84fb3b-4ef3-416f-bfa4-fe90d8ae01dd.png)

If you see a feature that you would like added or suggestion for improvement please let me know.

