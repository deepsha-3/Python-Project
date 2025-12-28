# Write a python program using a function to check whether a given number is prime or not.

def prime(num):
    if num <1 or num == 1: 
        return False
    else:
        for i in range(2,int(num**0.5)+1):
            if num % i == 0:
                return False
    return True
 
num = int(input("Enter a number:"))

if prime(num):
    print("The given number is prime number.")

else: 
    print("The given number is not a prime number.")