# In this stage, your program should:
# 1. Take an input: A string of characters separated by spaces ' '
# 2. Take the first input: Identify the shift number by finding the secret word butterscotch in the encoded string
# 3. Take the second input: an encoded string of characters separated by spaces ' '
# 4. Use the shift number to decipher the second message
# 5. Replace any x letters in the deciphered message with " " space
# 6. Print the second deciphered message.

# Example
# > r d c r t r c r f i j c x t r j c g z y y j w x h t y h m c u n j
# > u q j f x j c h t r j c y w d c f c x q n h j
# Output: please come try a slice

import string

user_input_1 = input()
user_input_2 = input()
shift = None


def decipher(string_val, shift_val):
    input_list = string_val.split()
    temp = ''
    for item in input_list:
        index = string.ascii_lowercase.index(item)
        temp += string.ascii_lowercase[(index + shift_val) % 26]
    return temp


# Determining the shift
i = -26
while i <= 26:
    if 'butterscotch' in decipher(user_input_1, i):
        shift = i
        break
    i += 1

result = decipher(user_input_2, shift).replace('x', ' ')
print(result)
