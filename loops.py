while True:
    number = float(input('Pick a number\n'))
    squareroot = number ** 0.5
    if number < 1:
        print('An error ocurred. The inputted number must be positive.')
    else:
        print(f'The square root of {number} is {squareroot}')
    