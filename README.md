# wordpressbruteforcer

Multithreaded python wordpress bruteforcer

```
[+] Wordpress bruteforcer
[+] getyourbots.com
--------------------------------------------------------------------------------
usage: main.py [-h] [--target TARGET_URL] [--username USERNAME]
               [--passwordsfile PASSWORDSFILE] [--threads THREADS]
               [--proxy PROXY] [--timeout TIMEOUT] [--verbose]

Wordpress bruteforcer

optional arguments:
  -h, --help            show this help message and exit
  --target TARGET_URL   Wordpress URL (eg. http://mywp.com or
                        http://mywp.com:80)
  --username USERNAME   Wordpress username
  --passwordsfile PASSWORDSFILE
                        File containing passwords
  --threads THREADS     Number of threads to run (default 1)
  --proxy PROXY         A proxy chain in this format
                        type[socks5/socks4/http]:host:port (eg.
                        socks5:127.0.0.1:8080)
  --timeout TIMEOUT     Requests timeout (in seconds)
  --verbose             Prints details about the scanning
```

### Install
    git clone https://github.com/getyourbots/wordpressbruteforcer
    
### Prerequisites
    - Python 2.7 - https://www.python.org/downloads/release/python-2710/
