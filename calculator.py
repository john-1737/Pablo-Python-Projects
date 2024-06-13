while True:
    calc = input("Enter a calculation or type 'exit' to close the calculator.\nUse * to multiply and / to divide.\n")
    if calc == 'exit':
        break
    else:
        print(eval(calc))