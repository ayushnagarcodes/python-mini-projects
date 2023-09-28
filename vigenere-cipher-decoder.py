# In this stage, your program should:
# Take an input: An integer representing the length of the keyword
# Take an input: A string of characters separated by spaces ' '
# Take an input: That exact string of characters separated by spaces ' ', but encoded
# Take an input: Your target message is encoded. A string of characters separated by spaces ' '
# Use the keyword to decode your target message
# Replace any x letters in the deciphered message with " " space
# Print the deciphered message.

# Example 1
# > 2
# > a b c d
# > a c c e
# > t i i t x t h p u m d y l p o l x g a n i m i b r
# Output: this should look familiar

# Example 2
# > 3
# > t e s t
# > d i q d
# > c i a b i r h x c c x
# Output: secret test

import string

shift = []
result = ''
len_keyword = int(input())
str_decoded = input().lower().split()
str_encoded = input().split()
final_encoded = input().split()

# Determining the keyword used to decipher Vigenere Cipher
for i in range(len_keyword):
    shift.append(ord(str_encoded[i]) - ord(str_decoded[i]))

# Decoding the given encoded sentence
for k in range(len(final_encoded)):
    index = string.ascii_lowercase.index(final_encoded[k]) - shift[k % len(shift)]
    result += string.ascii_lowercase[index % 26]

print(result.replace('x', ' '))
