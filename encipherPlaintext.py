# Enciphers User Input
# Dan Egner 28/08/2020

# To-do:
# - sanitise user inputs for capitals and non-alphabetic characters other than spaces
# - sanitise ceasar shift user choice
# - sanitise vigenere keyword choice
# - handle vigenere keywords longer than plaintext
# - sanitise enigma plugboard inputs and reject fewer than 6 pairs/duplicate pairs
# - make rotor and ring offsets only accept single alphabetic character
# - !!! implement two turnover points for rotors 6, 7, and 8
# - make user choose type of enigma mahcine, and supply multiple choice for the approriate rotors and reflectors
# - implement 4 rotors for the appropriate enigma model(s)
# - use 10 plugboard pairs with empty input = aa bb cc etc.



def getUserInput():

	# Get plaintext from user input
	plaintext = input("\nPlease enter plaintext:\n")
	plaintext = plaintext.lower()

	# Encode plaintext string to bytes, in a byte array to allow editing
	plaintextbytes = bytearray(plaintext, "utf-8")
	
	# Remove spaces from plaintextbytes
	removedspaces = 0
	for i in range(0, len(plaintextbytes)):
		if plaintextbytes[i - removedspaces] == 32:
			del(plaintextbytes[i - removedspaces])
			removedspaces += 1

	return(plaintextbytes)



def encipherCeasarShift(plain):

	# User chooses which ceasar shift
	shift = int(input("\nPlease choose a Ceasar Shift (1 to 25):\n"))

	# Encipher the plaintext character by character
	cipher = plain
	for i in range(0, len(cipher)):
		cipher[i] += shift

		# If character was shifted beyond Z, loop it back round to start of alphabet
		if cipher[i] >= 123:
			cipher[i] -= 26

	cipherstring = cipher.decode()

	# Capitalise ciphertext
	cipherstring = cipherstring.upper()

	return(cipherstring)



def encipherVigenere(plain):

	# User chooses keyword
	keyword = bytearray(input("\nPlease choose a keyword:\n"), "utf-8")

	# Repeat keyword to cover length of plaintext
	remainder = len(plain) % len(keyword)
	remainderkeyword = bytearray()
	for i in range(0, remainder):
		remainderkeyword.append(keyword[i])

	nonremainder = len(plain) // len(keyword)
	fullkeyword = keyword * nonremainder
	fullkeyword += remainderkeyword

	# Encipher the plaintext character by character
	cipher = plain
	for i in range(0, len(cipher)):
		cipher[i] += (fullkeyword[i] - 97)

		# If character was shifted beyond Z, loop it back round to start of alphabet
		if cipher[i] >= 123:
			cipher[i] -= 26

	cipherstring = cipher.decode()

	# Capitalise ciphertext
	cipherstring = cipherstring.upper()

	return(cipherstring)



def boundValue(value, low, high):
	# Loops integers between a lower and upper bound
	diff = high - low
	return (((value - low) % diff) + low)



def rotateEnigmaRotor(rotor, rotation):

	# Shift the input bytearray by the rotation value
	for i in range(0, len(rotor[0])):
		rotor[0][i] += rotation

		# If character was shifted beyond Z, loop it back round to start of alphabet
		if rotor[0][i] >= 123:
			rotor[0][i] -= 26

	# Shift the output bytearray by the rotation value
	# A different method (vs above) is required because output bytearray is not in alphabetic order
	outputcopy = rotor[1][:]   # Creates new object rather than copying the reference
	for i in range(0, len(rotor[1])):
		if (i + rotation) <= (len(rotor[1]) - 1):
			rotor[1][i] = outputcopy[i + rotation]
		elif (i + rotation) > (len(rotor[1]) - 1):
			rotor[1][i] = outputcopy[(i + rotation) % len(rotor[1])]

	return(rotor)



def rotateEnigmaRing(rotor, rotation):

	# Add the rotation value to the output bytearray
	for i in range(0, len(rotor[1])):
		rotor[1][i] += rotation

		# If character was shifted beyond Z, loop it back round to start of alphabet
		if rotor[1][i] >= 123:
			rotor[1][i] -= 26

	# Then shift the output bytearray to the right (i.e. opposite to the rotor offset shift) by the rotation value
	outputcopy = rotor[1][:]   # Creates new object rather than copying the reference
	for i in range(0, len(rotor[1])):
		if (i + rotation) <= (len(rotor[1]) - 1):
			rotor[1][i + rotation] = outputcopy[i]
		elif (i + rotation) > (len(rotor[1]) - 1):
			rotor[1][(i + rotation) % len(rotor[1])] = outputcopy[i]

	return(rotor)



def encipherEnigma(plain):

	# User chooses enigma model
	# Enigma I: 3 rotors from choice of 3
	# Enigma M3: 3 rotors from choice of 8
	# Enigma M4: 3 rotors from choice of 8, plus 1 static fourth rotor from choice of 2
	enigmamodel = input("\nPlease choose enigma model:\n1. Enigma I (Army)\n2. Enigma M3 (Navy)\n3. Enigma M4 (U-boat)\n")

	if enigmamodel == "1":

		eightchoices = False
		fourrotors = False

		rotor1 = [bytearray("abcdefghijklmnopqrstuvwxyz", "utf-8"), bytearray("ekmflgdqvzntowyhxuspaibrcj", "utf-8")]
		rotor2 = [bytearray("abcdefghijklmnopqrstuvwxyz", "utf-8"), bytearray("ajdksiruxblhwtmcqgznpyfvoe", "utf-8")]
		rotor3 = [bytearray("abcdefghijklmnopqrstuvwxyz", "utf-8"), bytearray("bdfhjlcprtxvznyeiwgakmusqo", "utf-8")]

		rotor1turnover = [b"q"[0], b"q"[0]]   # Bodge by duplicating the turnover point of all rotors with only one
		rotor2turnover = [b"e"[0], b"e"[0]]
		rotor3turnover = [b"v"[0], b"v"[0]]

		reflectorA = [bytearray("abcdefghijklmnopqrstuvwxyz", "utf-8"), bytearray("ejmzalyxvbwfcrquontspikhgd", "utf-8")]
		reflectorB = [bytearray("abcdefghijklmnopqrstuvwxyz", "utf-8"), bytearray("yruhqsldpxngokmiebfzcwvjat", "utf-8")]
		reflectorC = [bytearray("abcdefghijklmnopqrstuvwxyz", "utf-8"), bytearray("fvpjiaoyedrzxwgctkuqsbnmhl", "utf-8")]


	elif enigmamodel == "2":

		eightchoices = True
		fourrotors = False

		rotor1 = [bytearray("abcdefghijklmnopqrstuvwxyz", "utf-8"), bytearray("ekmflgdqvzntowyhxuspaibrcj", "utf-8")]
		rotor2 = [bytearray("abcdefghijklmnopqrstuvwxyz", "utf-8"), bytearray("ajdksiruxblhwtmcqgznpyfvoe", "utf-8")]
		rotor3 = [bytearray("abcdefghijklmnopqrstuvwxyz", "utf-8"), bytearray("bdfhjlcprtxvznyeiwgakmusqo", "utf-8")]
		rotor4 = [bytearray("abcdefghijklmnopqrstuvwxyz", "utf-8"), bytearray("esovpzjayquirhxlnftgkdcmwb", "utf-8")]
		rotor5 = [bytearray("abcdefghijklmnopqrstuvwxyz", "utf-8"), bytearray("vzbrgityupsdnhlxawmjqofeck", "utf-8")]
		rotor6 = [bytearray("abcdefghijklmnopqrstuvwxyz", "utf-8"), bytearray("jpgvoumfyqbenhzrdkasxlictw", "utf-8")]
		rotor7 = [bytearray("abcdefghijklmnopqrstuvwxyz", "utf-8"), bytearray("nzjhgrcxmyswboufaivlpekqdt", "utf-8")]
		rotor8 = [bytearray("abcdefghijklmnopqrstuvwxyz", "utf-8"), bytearray("fkqhtlxocbjspdzramewniuygv", "utf-8")]

		rotor1turnover = [b"q"[0], b"q"[0]]   # Bodge by duplicating the turnover point of all rotors with only one
		rotor2turnover = [b"e"[0], b"e"[0]]
		rotor3turnover = [b"v"[0], b"v"[0]]
		rotor4turnover = [b"j"[0], b"j"[0]]
		rotor5turnover = [b"z"[0], b"z"[0]]
		rotor6turnover = [b"z"[0], b"m"[0]]
		rotor7turnover = [b"z"[0], b"m"[0]]
		rotor8turnover = [b"z"[0], b"m"[0]]

		reflectorA = [bytearray("abcdefghijklmnopqrstuvwxyz", "utf-8"), bytearray("ejmzalyxvbwfcrquontspikhgd", "utf-8")]
		reflectorB = [bytearray("abcdefghijklmnopqrstuvwxyz", "utf-8"), bytearray("yruhqsldpxngokmiebfzcwvjat", "utf-8")]
		reflectorC = [bytearray("abcdefghijklmnopqrstuvwxyz", "utf-8"), bytearray("fvpjiaoyedrzxwgctkuqsbnmhl", "utf-8")]


	elif enigmamodel == "3":

		eightchoices = True
		fourrotors = True

		rotor1 = [bytearray("abcdefghijklmnopqrstuvwxyz", "utf-8"), bytearray("ekmflgdqvzntowyhxuspaibrcj", "utf-8")]
		rotor2 = [bytearray("abcdefghijklmnopqrstuvwxyz", "utf-8"), bytearray("ajdksiruxblhwtmcqgznpyfvoe", "utf-8")]
		rotor3 = [bytearray("abcdefghijklmnopqrstuvwxyz", "utf-8"), bytearray("bdfhjlcprtxvznyeiwgakmusqo", "utf-8")]
		rotor4 = [bytearray("abcdefghijklmnopqrstuvwxyz", "utf-8"), bytearray("esovpzjayquirhxlnftgkdcmwb", "utf-8")]
		rotor5 = [bytearray("abcdefghijklmnopqrstuvwxyz", "utf-8"), bytearray("vzbrgityupsdnhlxawmjqofeck", "utf-8")]
		rotor6 = [bytearray("abcdefghijklmnopqrstuvwxyz", "utf-8"), bytearray("jpgvoumfyqbenhzrdkasxlictw", "utf-8")]
		rotor7 = [bytearray("abcdefghijklmnopqrstuvwxyz", "utf-8"), bytearray("nzjhgrcxmyswboufaivlpekqdt", "utf-8")]
		rotor8 = [bytearray("abcdefghijklmnopqrstuvwxyz", "utf-8"), bytearray("fkqhtlxocbjspdzramewniuygv", "utf-8")]

		rotor1turnover = [b"q"[0], b"q"[0]]   # Bodge by duplicating the turnover point of all rotors with only one
		rotor2turnover = [b"e"[0], b"e"[0]]
		rotor3turnover = [b"v"[0], b"v"[0]]
		rotor4turnover = [b"j"[0], b"j"[0]]
		rotor5turnover = [b"z"[0], b"z"[0]]
		rotor6turnover = [b"z"[0], b"m"[0]]
		rotor7turnover = [b"z"[0], b"m"[0]]
		rotor8turnover = [b"z"[0], b"m"[0]]

		staticrotorbeta = [bytearray("abcdefghijklmnopqrstuvwxyz", "utf-8"), bytearray("leyjvcnixwpbqmdrtakzgfuhos", "utf-8")]
		staticrotorgamma = [bytearray("abcdefghijklmnopqrstuvwxyz", "utf-8"), bytearray("fsokanuerhmbtiycwlqpzxvgjd", "utf-8")]

		reflectorBthin = [bytearray("abcdefghijklmnopqrstuvwxyz", "utf-8"), bytearray("enkqauywjicopblmdxzvfthrgs", "utf-8")]
		reflectorCthin = [bytearray("abcdefghijklmnopqrstuvwxyz", "utf-8"), bytearray("rdobjntkvehmlfcwzaxgyipsuq", "utf-8")]


	# User chooses rotor order
	if fourrotors == True:
		rotorlist = [rotor1, rotor2, rotor3, rotor4, rotor5, rotor6, rotor7, rotor8]
		staticrotorlist = [staticrotorbeta, staticrotorgamma]

		fourthrotor = input("\nPlease choose leftmost rotor (beta or gamma):\n")
		rotororder = bytearray(input("\nPlease choose remaining rotor order, left to right (e.g. 123):\n"), "utf-8")

	elif fourrotors == False:
		if eightchoices == True:
			rotorlist = [rotor1, rotor2, rotor3, rotor4, rotor5, rotor6, rotor7, rotor8]
		elif eightchoices == False:
			rotorlist = [rotor1, rotor2, rotor3]

		rotororder = bytearray(input("\nPlease choose rotor order, left to right (e.g. 123):\n"), "utf-8")

	# Sets the normal three rotors to the user-assigned choices
	rightrotor = rotorlist[rotororder[2] - 49]
	rightmidrotor = rotorlist[rotororder[1] - 49]
	leftmidrotor = rotorlist[rotororder[0] - 49]

	# Sets the static fourth rotor to the user choice, if required
	if fourrotors == True:
		if fourthrotor == "beta":
			leftrotor = staticrotorlist[0]
		elif fourthrotor == "gamma":
			leftrotor = staticrotorlist[1]

	# Sets the right and rightmid turnover points to their appropriate historical values (leftmid rotor never turns any further rotor so is omitted)
	if eightchoices == True:
		turnoverlist = [rotor1turnover, rotor2turnover, rotor3turnover, rotor4turnover, rotor5turnover, rotor6turnover, rotor7turnover, rotor8turnover]
	elif eightchoices == False:
		turnoverlist = [rotor1turnover, rotor2turnover, rotor3turnover]
	rightturnover = turnoverlist[rotororder[2] - 49]
	rightmidturnover = turnoverlist[rotororder[1] - 49]


	# User chooses rotor offsets
	if fourrotors == True:
		fourthrotoroffset = bytes(input("\nPlease choose leftmost rotor offset (e.g. a):\n"), "utf-8")
		rotoroffsets = bytearray(input("\nPlease choose remaining rotor offets, left to right (e.g. abc):\n"), "utf-8")

	elif fourrotors == False:
		rotoroffsets = bytearray(input("\nPlease choose rotor offets, left to right (e.g. abc):\n"), "utf-8")
	
	rightoffset = rotoroffsets[2]
	rightrotor = rotateEnigmaRotor(rotor = rightrotor, rotation = (rightoffset - 97))

	rightmidoffset = rotoroffsets[1]
	rightmidrotor = rotateEnigmaRotor(rotor = rightmidrotor, rotation = (rightmidoffset - 97))

	leftmidoffset = rotoroffsets[0]
	leftmidrotor = rotateEnigmaRotor(rotor = leftmidrotor, rotation = (leftmidoffset - 97))

	if fourrotors == True:
		leftrotor = rotateEnigmaRotor(rotor = leftrotor, rotation = (fourthrotoroffset[0] - 97))


	# User chooses ring settings
	if fourrotors == True:
		fourthrotorringsetting = bytes(input("\nPlease choose leftmost rotor ring setting (e.g. a):\n"), "utf-8")
		ringsettings = bytearray(input("\nPlease choose remaining ring settings, left to right (e.g. abc):\n"), "utf-8")

	elif fourrotors == False:
		ringsettings = bytearray(input("\nPlease choose ring settings, left to right (e.g. abc):\n"), "utf-8")

	rightringsetting = ringsettings[2]
	rightrotor = rotateEnigmaRing(rotor = rightrotor, rotation = (rightringsetting - 97))

	middleringsetting = ringsettings[1]
	rightmidrotor = rotateEnigmaRing(rotor = rightmidrotor, rotation = (middleringsetting - 97))

	leftringsetting = ringsettings[0]
	leftmidrotor = rotateEnigmaRing(rotor = leftmidrotor, rotation = (leftringsetting - 97))

	if fourrotors == True:
		leftrotor = rotateEnigmaRing(rotor = leftrotor, rotation = (fourthrotorringsetting[0] - 97))


	# User chooses reflector
	if fourrotors == True:
		reflectorchoice = input("\nPlease choose reflector:\n1. UKW-b (thin)\n2. UKW-c (thin)\n")
		if reflectorchoice == "1":
			reflector = reflectorBthin
		elif reflectorchoice == "2":
			reflector = reflectorCthin

	elif fourrotors == False:

		if eightchoices == True:
			reflectorchoice = input("\nPlease choose reflector:\n1. UKW-B\n2. UKW-C\n")
			if reflectorchoice == "1":
				reflector = reflectorB
			elif reflectorchoice == "2":
				reflector = reflectorC

		elif eightchoices == False:
			reflectorchoice = input("\nPlease choose reflector:\n1. UKW-A\n2. UKW-B\n3. UKW-C\n")
			if reflectorchoice == "1":
				reflector = reflectorA
			elif reflectorchoice == "2":
				reflector = reflectorB
			elif reflectorchoice == "3":
				reflector = reflectorC


	# User chooses plugboard connections, with default as no connection pairs
	plugboardswaps = bytearray(input("\nPlease choose 10 plugboard letter pairs (e.g. aj eb ...):\n"), "utf-8")
	if plugboardswaps == bytearray("", "utf-8"):
		plugboardswaps = "aa bb cc dd ee ff gg hh ii jj"
	plugboard = [bytearray("abcdefghijklmnopqrstuvwxyz", "utf-8"), bytearray("abcdefghijklmnopqrstuvwxyz", "utf-8")]

	for i in range(0, 28, 3):
		for j in range(0, len(plugboard[1])):
			if plugboard[1][j] == plugboardswaps[i]:
				plugboard[1][j] = plugboardswaps[i + 1]

			elif plugboard[1][j] == plugboardswaps[i + 1]:
				plugboard[1][j] = plugboardswaps[i]


	# Encipher the plaintext character by character
	cipher = plain
	for i in range(0, len(cipher)):

		# Rotate leftmost and middle rotors if middle rotor was sitting on its turnover point before this keypress (double step!)
		if rightmidrotor[0][0] == rightmidturnover[0] or rightmidrotor[0][0] == rightmidturnover[1]:
			leftmidrotor = rotateEnigmaRotor(rotor = leftmidrotor, rotation = 1)
			rightmidrotor = rotateEnigmaRotor(rotor = rightmidrotor, rotation = 1)

		# Rotate middle rotor if the rightmost rotor was sitting on its turnover point before this keypress
		elif rightrotor[0][0] == rightturnover[0] or rightrotor[0][0] == rightturnover[1]:
			rightmidrotor = rotateEnigmaRotor(rotor = rightmidrotor, rotation = 1)

		# Rotate rightmost rotor once (occurs every keypress)
		rightrotor = rotateEnigmaRotor(rotor = rightrotor, rotation = 1)


		# Calculate the relative offsets between each pair of adjacent components
		currentoffset_plugboard = b"a"[0] - 97   # Never changes
		currentoffset_rightrotor = rightrotor[0][0] - 97
		currentoffset_rightmidrotor = rightmidrotor[0][0] - 97
		currentoffset_leftmidrotor = leftmidrotor[0][0] - 97
		if fourrotors == True:
			currentoffset_leftrotor = leftrotor[0][0] - 97
		currentoffset_reflector = b"a"[0] - 97   # Never changes

		# Direction is important, use negative sign for opposite signal directions (e.g. right to plug = -plug_to_right)
		plug_to_right = currentoffset_rightrotor - currentoffset_plugboard
		right_to_rightmid = currentoffset_rightmidrotor - currentoffset_rightrotor
		rightmid_to_leftmid = currentoffset_leftmidrotor - currentoffset_rightmidrotor
		if fourrotors == True:
			leftmid_to_left = currentoffset_leftrotor - currentoffset_leftmidrotor
			left_to_reflect = currentoffset_reflector - currentoffset_leftrotor
		elif fourrotors == False:
			leftmid_to_reflect = currentoffset_reflector - currentoffset_leftmidrotor


		# Perform forward plugboard swap
		for j in range(0, len(plugboard[0])):
			if plugboard[0][j] == cipher[i]:
				cipher[i] = plugboard[1][j]
				break

		# Perform forward rightrotor swap
		for j in range(0, len(rightrotor[0])):
			if rightrotor[0][j] == boundValue(value = (cipher[i] + plug_to_right), low = 97, high = 123):
				cipher[i] = rightrotor[1][j]
				break

		# Perform forward rightmidrotor swap
		for j in range(0, len(rightmidrotor[0])):
			if rightmidrotor[0][j] == boundValue(value = (cipher[i] + right_to_rightmid), low = 97, high = 123):
				cipher[i] = rightmidrotor[1][j]
				break

		# Perform forward leftmidrotor swap
		for j in range(0, len(leftmidrotor[0])):
			if leftmidrotor[0][j] == boundValue(value = (cipher[i] + rightmid_to_leftmid), low = 97, high = 123):
				cipher[i] = leftmidrotor[1][j]
				break

		# If fourth rotor in use, perform forward leftrotor swap, reflection, reverse leftrotor swap, and reverse leftmidrotor swap
		if fourrotors == True:
			# Perform forward leftrotor swap
			for j in range(0, len(leftrotor[0])):
				if leftrotor[0][j] == boundValue(value = (cipher[i] + leftmid_to_left), low = 97, high = 123):
					cipher[i] = leftrotor[1][j]
					break

			# Perform reflection
			for j in range(0, len(reflector[0])):
				if reflector[0][j] == boundValue(value = (cipher[i] + left_to_reflect), low = 97, high = 123):
					cipher[i] = reflector[1][j]
					break

			# Peform reverse leftrotor swap
			for j in range(0, len(leftrotor[1])):
				if leftrotor[1][j] == boundValue(value = (cipher[i] - left_to_reflect), low = 97, high = 123):
					cipher[i] = leftrotor[0][j]
					break

			# Peform reverse leftmidrotor swap
			for j in range(0, len(leftmidrotor[1])):
				if leftmidrotor[1][j] == boundValue(value = (cipher[i] - leftmid_to_left), low = 97, high = 123):
					cipher[i] = leftmidrotor[0][j]
					break

		# Else perform reflection and reverse leftmidrotor swap only
		elif fourrotors == False:
			# Perfrom reflection
			for j in range(0, len(reflector[0])):
				if reflector[0][j] == boundValue(value = (cipher[i] + leftmid_to_reflect), low = 97, high = 123):
					cipher[i] = reflector[1][j]
					break

			# Peform reverse leftmidrotor swap
			for j in range(0, len(leftmidrotor[1])):
				if leftmidrotor[1][j] == boundValue(value = (cipher[i] - leftmid_to_reflect), low = 97, high = 123):
					cipher[i] = leftmidrotor[0][j]
					break

		# Peform reverse rightmidrotor swap
		for j in range(0, len(rightmidrotor[1])):
			if rightmidrotor[1][j] == boundValue(value = (cipher[i] - rightmid_to_leftmid), low = 97, high = 123):
				cipher[i] = rightmidrotor[0][j]
				break

		# Peform reverse rightrotor swap
		for j in range(0, len(rightrotor[1])):
			if rightrotor[1][j] == boundValue(value = (cipher[i] - right_to_rightmid), low = 97, high = 123):
				cipher[i] = rightrotor[0][j]
				break

		# Perform reverse plugboard swap
		for j in range(0, len(plugboard[1])):
			if plugboard[1][j] == boundValue(value = (cipher[i] - plug_to_right), low = 97, high = 123):
				cipher[i] = plugboard[0][j]
				break


	cipherstring = cipher.decode()

	# Capitalise ciphertext
	cipherstring = cipherstring.upper()

	return(cipherstring)




def main():

	sanitisedbytes = getUserInput()

	# Use chooses which cipher
	cipherchoice = input("\nPlease choose a cipher:\n1. Ceasar shift\n2. Vigenere\n3. Enigma\n")

	if cipherchoice == "1":
		ceasarciphertext = encipherCeasarShift(plain = sanitisedbytes)
		print(ceasarciphertext)
	
	elif cipherchoice == "2":
		vigenereciphertext = encipherVigenere(plain = sanitisedbytes)
		print(vigenereciphertext)

	elif cipherchoice == "3":
		enigmaciphertext = encipherEnigma(plain = sanitisedbytes)
		print(enigmaciphertext)

	# Wait for user to close program
	input("\nPRESS ENTER TO EXIT")
	for i in range(0, 3):
		print(">>>")



if __name__ == "__main__":
	print("[Running encipherPlaintext.py as standalone]")
	main()

else:
	print("[Running encipherPlaintext.py from another module]")
	main()