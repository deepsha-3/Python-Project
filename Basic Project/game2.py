
# Number guessing game using python

import random

number = random.randint(1, 100)

a = -1
while (a != number):
    a = int(input("Guess the correct number between 1 to 100: "))