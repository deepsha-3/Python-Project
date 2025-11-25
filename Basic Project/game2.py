
# Number guessing game using python

import random

number = random.randint(1, 100)

a = -1
guess_value = 0

while (a != number):
    print ("You can guess the number between 1 to 100.")
    a = int(input("Guess the correct number between 1 to 100: "))
    guess_value += 1

    if (a> number):
        print("Please, give a smaller number.")

    else:
        print("Please, give a larger number.")

print(f"Congratulations! You guessed the correct number {number} in {guess_value} attempts.")    