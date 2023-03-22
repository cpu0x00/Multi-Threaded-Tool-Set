# Multi-Threaded-Tool-Set
Multi-Threaded python-based utilities for Blazing Fast cracking and bruteforcing

Tools:

- Multi-Threaded Smb Bruteforcer (mtsb.py):

```
# mtsb.py --help
usage: mtsb.py [-h] --target TARGET [--usersfile USERSFILE] [--user USER] [--passwords PASSWORDS] [--password PASSWORD] [--port PORT] [--threads THREADS] [--verbose]
               [--stop_on_find]

options:
  -h, --help            show this help message and exit
  --target TARGET, -t TARGET
                        target ip address
  --usersfile USERSFILE, -uf USERSFILE
                        users wordlist
  --user USER, -u USER  single username to use
  --passwords PASSWORDS, -pf PASSWORDS
                        passwords wordlist
  --password PASSWORD, -p PASSWORD
                        single password to use
  --port PORT           smb port (default: 445)
  --threads THREADS     threads to use (default: 100)
  --verbose, -v         verbose the bruteforcing attempts
  --stop_on_find        stops once find a single valid user:password

(M)ulti (T)hreaded (S)MB (B)ruteforcer
```
- Multi-Threaded WinRM Bruteforcer (mtwb.py):

```
# mtwb.py --help
usage: mtwb.py [-h] --target TARGET [--port PORT] [--username USERNAME] [--usernames USERNAMES] [--passwords PASSWORDS] [--password PASSWORD] [--threads THREADS]
               [--verbose] [--stop_on_find]

options:
  -h, --help            show this help message and exit
  --target TARGET, -t TARGET
                        the WinRM server IP address
  --port PORT           port to connect to (default=5985)
  --username USERNAME, -u USERNAME
                        username to use
  --usernames USERNAMES, -uf USERNAMES
                        username file to use
  --passwords PASSWORDS, -pf PASSWORDS
                        password file to use
  --password PASSWORD, -p PASSWORD
                        password to use
  --threads THREADS     threads to use (default=20), the more threads the more unreliable results the tool gives.
  --verbose, -v         verbose output
  --stop_on_find        stops once find a single valid user:password

Multi-Threaded WinRM BruteForcer
```

- Multi-Threaded JWT Cracker (mtjc.py):

```
# mtjc.py --help
usage: mtjc.py [-h] --cookie COOKIE --wordlist WORDLIST [--threads THREADS] [--verbose] [--force]

options:
  -h, --help            show this help message and exit
  --cookie COOKIE, -c COOKIE
                        JWT token to crack (HS256)
  --wordlist WORDLIST, -w WORDLIST
                        wordlist to use
  --threads THREADS, -t THREADS
                        threads to work with (default: 100)
  --verbose, -v         verbose the bruteforce attempts (affects the script's performance)
  --force               forces the bruteforcer to continue despite the (invalid base64 error)

(M)ulti (T)hreaded (J)WT (C)racker
```

- Multi-Threaded Zipfile Cracker (mtzc.py):

```
mtzc.py --help
usage: mtzc.py [-h] [--file FILE] [--passwords PASSWORDS] [--threads THREADS] [--verbose]

options:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  zip file to crack
  --passwords PASSWORDS, -p PASSWORDS
                        passwords wordlist to use
  --threads THREADS, -t THREADS
                        threads to work with (default: 2000)
  --verbose, -v         verbosing the bruteforcing attempts (affects the program's performance)

(M)ulti (T)hreaded (Z)ipfile (C)racker
```

- Multi-Threaded FTP Cracker (mtfc.py):

```
# mtfc.py --help
usage: mtfc.py [-h] --target TARGET [--port PORT] [--user USER] [--password PASSWORD] [--usernames USERNAMES] [--passwords PASSWORDS] [--threads THREADS]

options:
  -h, --help            show this help message and exit
  --target TARGET, -t TARGET
                        target ip address
  --port PORT           ftp port
  --user USER, -U USER  username to use
  --password PASSWORD, -P PASSWORD
                        password to use
  --usernames USERNAMES, -u USERNAMES
                        usernames list to use
  --passwords PASSWORDS, -p PASSWORDS
                        passwords list to use
  --threads THREADS     threads to use, default=100

(M)ulti-(T)hreaded (F)TP (C)racker
```
