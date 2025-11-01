#The concept is simple. I want to add junk characters to already encrypted text to make it harder to analyze.
#How I will go about this is simple. I will use a formula based on the plaintext length to determine where to add junk. 
#It cannot be random as it needs to be reproducible for decryption.
#Junk Letter = J
#J_value = (second_letter_of_word_value + (character_count/word_count))%26
#Where to add J = int((last_letter_of_word_value/character_count) + 5) % word_length

import string, math, re

cipherText = ("czilmyppyhnyyhsyuvlmfcbupeyvyyyhufcxpynblqcpyxxuhxmyyphqnbyqiltfxczilqbutncfncfm")  # original input string to be processed

def insertJunk(cipherText):
    
    alphabet = list("abcdefghijklmnopqrstuvwxyz")  # list of lowercase letters used for mapping letters -> index and back
    charCount = len(cipherText)                    # total number of characters in the ciphertext string (includes spaces/punctuation)
    wordCount = len(cipherText.split())            # number of words (split by whitespace)
    modifier = list(cipherText.lower().split())    # list of lowercase words (split on whitespace) that we'll mutate
    for string in modifier:
        number = modifier.index(string)            # index of the current word inside modifier (position in word list)
        lstring = list(string)                     # list of characters for the current word (so we can insert a char)
        toCalc = (string[0])                       # the first character of the current word (used to compute J_value)
        # j_value: numeric index (0-25) for the junk letter J. 
        # It uses the index of the 2nd letter of the word, subtracts 1, adds the integer division charCount/wordCount,
        # then reduces modulo 26 to stay in a-z range.
        j_value = int (alphabet.index(toCalc)-1 + (charCount/wordCount)) % 26
        j = alphabet[j_value]                      # the actual junk letter (character) to insert, derived from j_value
        # l_value: auxiliary numeric value used to compute insertion index.
        # It uses the second-to-last character of the word (string[len(string)-2]),
        # takes its alphabet index minus 1, adds charCount/wordCount, then reduces mod 26.
        l_value = int (alphabet.index(string[len(string)-2])-1 + (charCount/wordCount)) % 26
        # Compute insertion index with the formula: int(l_value/charCount + 3) % len(string)
        # - l_value/charCount produces a small fraction (since l_value < 26 and charCount typically larger)
        # - adding 3 biases the insertion toward later positions
        # - modulo word length ensures index is within the word bounds
        # Then insert the junk letter `j` at that computed position in lstring.
        lstring.insert(int(l_value/charCount+3)%len(string), j)
        string =''.join(lstring)                   # reassemble the mutated word from its character list
        modifier[number] = string                  # replace the original word in modifier with the mutated one
    print (modifier)                               # debug: print list of mutated words
    lmodifier = ''.join(modifier)                  # concatenate all mutated words into one long string (no spaces)
    # finalText: strip out anything that isn't lowercase letter or digit (removes punctuation and non-alphanumerics)
    finalText = re.sub('[^a-z0-9]+', '', lmodifier)
    print (finalText)                              # debug: print the final compacted string
    
    

insertJunk(cipherText)


#fixes I want to make: Prevent periods and capitalization from being an issue by removing all of that at the start
#Stuff to add: Decryption. Use this same formula to decrypt messages that have been struck by this encryption method. 
#I could also make this thing pre and post cipher after running it through the insert junk.
#Add more junk letters, add more functionality by allowing the user to input their string. Make sure it works with punctuation in the text too. 
# Decrypting it seems pretty easy. Just use the insertion formula to remove whatever letters would be there. The only problem is it also uses word count, which is obscured by removing spaces. 
#Decrypting this from scratch with other ciphers at play is pretty impossible for me. 
