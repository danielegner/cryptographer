# Decrypts Ceasar Shift Ciphertext
# Dan Egner 19/07/2020




potential_solution = "shipwreckofthewhaleshipessex"
import detectEnglish

import numpy as np


def main():
	ciphertext = "VKLSZUHFNRIWKHZKDOHVKLSHVVHA"

	uppercase_alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
	#uppercase_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	uppercase_alphabet = np.array(uppercase_alphabet)
	

	for i in range(25):

		cipher_alphabet = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
		cipher_alphabet = [x + i for x in cipher_alphabet]
		cipher_alphabet = np.array(cipher_alphabet)

		for j in range(len(cipher_alphabet)):
			if cipher_alphabet[j] >= 26:
				cipher_alphabet[j] = cipher_alphabet[j] - 26

		attempt_plaintext = []
		for j in range(len(ciphertext)):
			attempt_plaintext.append(uppercase_alphabet[cipher_alphabet[np.where(uppercase_alphabet == ciphertext[j])]])

		print(str(attempt_plaintext))


if __name__ == "__main__":
	print("Running decryptCeasar.py as standalone")
	main()
else:
	print("Running decryptCeasar.py from another module")
	main()