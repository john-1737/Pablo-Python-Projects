casetypes = {'C': 'camelCase',
             'P': 'PascalCase',
             'U': 'UPPER_SNAKE_CASE',
             'S': 'snake_case'}

def snake_case(text):
    text = text.lower()
    returntext = text.replace(' ', '_')
    return returntext
    
def UPPER_SNAKE_CASE(text):
    text = text.upper()
    returntext = text.replace(' ', '_')
    return returntext

def camelCase(text):
    text = text.title()
    text = list(text)
    text[0] = text[0].lower()
    text = ''.join(text)
    returntext = text.replace(' ', '')
    return returntext
def PascalCase(text):
    text = text.title()
    returntext = text.replace(' ', '')
    return returntext

while True:
    text = input('Enter some text:\n')
    case = input('''Select a case:
    S = snake_case
    U = UPPER_SNAKE_CASE
    C = camelCase
    P = PascalCase\n''')
    casetype = casetypes[case.upper()]
    print(f'{text} in {casetype} is:')
    if casetype == 'camelCase':
        print(camelCase(text))
    elif casetype == 'PascalCase':
        print(PascalCase(text))
    elif casetype == 'snake_case':
        print(snake_case(text))
    elif casetype == 'UPPER_SNAKE_CASE':
        print(UPPER_SNAKE_CASE(text))
    if input('Click ENTER/RETURN to keep going, any other key to exit.') != '':
        break