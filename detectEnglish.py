# Detects English Words
# Dan Egner 19/07/2020



# Load list of english words from dictionary text file
def loadDictionary():
    dictionary_file = open("dictionary.txt")
    english_words = []
    english_words = list(dictionary_file.read().split("\n"))

    i = 0
    for word in english_words:
        english_words[i] = word.lower()
        i += 1

    dictionary_file.close()
    return english_words


# Make uppercase characters lowercase and remove any non-alphabetic characters
def sanitiseInput(inputtext):
    uppercase_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowercase_alphabet = uppercase_alphabet + uppercase_alphabet.lower()

    inputtext = inputtext.lower()
    sanitised_text = []
    for character in inputtext:
        if character in lowercase_alphabet:
            sanitised_text.append(character)
    return "".join(sanitised_text)


# Identify English words present in the sanitised input text
def identifyEnglishWords(sanitisedtext, wordlist):
    count = 0
    identified_words = []

    for word in wordlist:
        if word in sanitisedtext:
            count += 1
            identified_words.append(word)

    if len(identified_words) < len(sanitisedtext) / 5:   # Only return if enough words are found to suggest the input text is in English
        identified_words = []
    
    return identified_words




from __main__ import potential_solution

def detectEnglish_main():
    word_list = loadDictionary()
    clean_input = sanitiseInput(str(potential_solution))
    words_found = identifyEnglishWords(clean_input, word_list)
    return words_found



if __name__ == "__main__":
    print("Running detectEnglish.py as standalone")
    detectEnglish_main()
else:
    print("Running detectEnglish.py from another module")
    detectEnglish_main()
