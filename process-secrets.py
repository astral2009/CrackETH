import sys, getopt
from os import path
from secrets import randbits
from sha3 import keccak_256
from coincurve import PublicKey
from multiprocessing import Process

wallets = open('eth_wallets.txt').read().split('\n')
for i in range(len(wallets)):
	wallets[i] = int(wallets[i],16)

procs = 4
counter = 0

def main():
	global counter
	while True:
		bits = randbits(256)
		key = hex(bits)[2:]
		if len(key) != 64:
	  		key = '0' * (64 - len(key)) + key
		private_key = bytes.fromhex(key)
		public_key = PublicKey.from_secret(private_key).format(compressed=False)[1:]
		addr = keccak_256(public_key).digest()[-20:]
		addr = '0x' + addr.hex()
		counter += 1
		if int(addr,16) in wallets:
			print(addr, key)
			file = open('FOUND.txt', 'a')
			file.write('{}\t{}\n'.format(addr,key))
			file.close()
		print(counter , end = '\r')

if __name__ == '__main__':
	for i in range(procs):
		exec(f'p' + str(i) + '= Process(target=main)')
		exec(f'p' + str(i) + '.start()')
	for i in range(procs):
		exec(f'p' + str(i) + '.join()')