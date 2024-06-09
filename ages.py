for x in range(0,3):
    age = int(input("What\'s your age?\n"))
    if age >= 18:
        print('Hi grown-up')
    elif age <= 2:
        print('Hi baby')
    else:
        print("Hi kid")