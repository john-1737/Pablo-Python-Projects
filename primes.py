import math
from tkinter import messagebox, simpledialog

num = simpledialog.askinteger('Prime numbers', 'Enter a number to check if it is prime.')

primes = [2]
for j in range(2, math.ceil(math.sqrt(num)) + 1):
        isprime = True
        for i in primes[:]:
            if j%i == 0:
                isprime = False
            if isprime:
                primes.append(j)

    primes = list(set(primes))

prime = True
for i in primes:
    if num%i == 0:
        prime = False

if prime:
    messagebox.showinfo(message=f'{num} is prime')
else:
    messagebox.showinfo(message=f'{num} is not prime')        
