#  Rock, Scissors, Paper game in  python.


# This game is between computer and user
"""
Rock(r)= 1
Scissors(s)= -1
paper(s)= 0
""" 
import random


computer = random.choice([-1,0,1])
you= input("Enter your choice:")
you_lower = you.lower()  
youDict={"r": 1, "s":-1, "p":0}

reverseDict={1:"Rock", -1:"Scissors",0:"Paper"}
  
yournum= youDict.get(you_lower)

if yournum is None:
    print("Invalid Value.\nPlease enter 'r' for Rock, 's' for Scissors, or 'p' for Paper.")
else:
    print(f"Computer chose: {reverseDict[computer]}\nYou chose: {reverseDict[yournum]}  ")

    if(computer== yournum):
        print("Both choices are same.It's a tie!")

    else: 
        if(computer==-1 and yournum==1):
            print("You Win!")
            
        elif(computer==-1 and yournum==0):
            print("You Lose!")
        
        elif(computer==1 and yournum==-1):
           print("You Lose!")

        elif(computer==1 and yournum==0):
          print("You Win!")

        elif(computer==0 and yournum==-1): 
           print("You Lose!")

        elif(computer==0 and yournum==1):
           print("You Win")
    
        else:
           print("I think you can't understand game logic.")
