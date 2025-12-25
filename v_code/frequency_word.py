# Write a Python program to input a sentence and display the frequency of each word. 

sentence = input("Enter a sentence:")

word = sentence.split()
frequency = {}
for w in word:
    if w in frequency:
        frequency[w] += 1
    else:
        frequency[w] = 1

print("Word Frequency:")
for w, freq in frequency.items():
    print(f"{w}: {freq}")