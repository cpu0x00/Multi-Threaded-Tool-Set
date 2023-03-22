# Multi Threaded Zipfile Cracker

import time
import pyzipper
import argparse
from concurrent.futures import ThreadPoolExecutor 
from os import _exit
from pwn import log
from os import system

parser = argparse.ArgumentParser(epilog="(M)ulti (T)hreaded (Z)ipfile (C)racker")

parser.add_argument('--file', '-f', help='zip file to crack')
parser.add_argument('--passwords', '-p', help='passwords wordlist to use')
parser.add_argument('--threads', '-t', type=int, default=2000, help='threads to work with (default: 2000)')
parser.add_argument('--verbose', '-v', action="store_true", help="verbosing the bruteforcing attempts (affects the program's performance)")

args = parser.parse_args()

zipfile = args.file

write_name = f'{zipfile}_EXTRACTED'.replace('.zip', '')

print(f"[*] cracking: {zipfile}")
print(f"[*] using wordlist: {args.passwords}")
passwords = open(args.passwords, 'r', encoding='latin1').readlines()
passwords_list = [p.strip() for p in passwords] 
print(f'[*] using {len(passwords_list)} passwords\n')
if not args.verbose:

	progress = log.progress('')
	progress.status('Bruteforcing...')

start = time.perf_counter()
def zipcrack(file,password):


		zip_file = pyzipper.AESZipFile(file, 'r')

		try:
			
			pwd = password.encode()
			if zip_file.extractall(write_name, pwd=pwd) == None:
				print('\n')
				log.info(f"cracked: {password} ")
				finish = time.perf_counter()
				log.info(f'finished in {round(finish-start)} second(s)')
				system('tset') # using tset utility for reseting the standard output for the terminal
				_exit(1)

		except RuntimeError:
			if args.verbose:
				print(f'tried: {password}')				

	
			
try:

	with ThreadPoolExecutor(args.threads) as ex:
		result = [ex.submit(zipcrack, zipfile, password) for password in passwords_list]
except KeyboardInterrupt:
	progress.status('termenating...')
	log.info('reseting the terminal...')
	system('tset') # using tset utility for reseting the standard output for the terminal
	_exit(0)