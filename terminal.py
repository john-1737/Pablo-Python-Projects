savefiles = {}
helplist = {'open Python' : 'Opens a Python editor workspace.',
            'close Python' : 'Closes a Python editor workspace.',
            'save' : 'Saves a Python file to your files.',
            'run' : 'Runs a Python file in a file menu or Python workspace, and opens a text file in a file menu.',
            'open Python shell' : 'Opens a Python shell. You cannot save in the Python shell.',
            'close shell' : 'Closes a Python shell.',
            'exit terminal' : 'Closes the terminal. Your saved projects are deleted when you close the terminal.',
            'open text creator' : 'Opens a text creator workspace.',
            '$close$' : 'Closes a text creator workspace.',
            '$save$' : 'Saves a text file to your files.',
            'help' : 'Opens the help menu.',
            'open file' : 'Opens a file in a file menu.',
            'close file' : 'Closes a file menu.',
            'view' : 'Views the contents of a file in a file menu.',
            'delete all files' : 'Deletes all of your files.',
            'delete file' : 'Deletes a specified file.'}
def loadtext(text):
    return savefiles[text][1]
while True:
    command = input()
    if command == 'open Python':
        x = ''
        print('\tEnter "save" to save to your library.\n\tEnter "run" to run your program.\n\tSet a variable to "loadtext" (no quotes) followed by a text or Python file name in paren-\n\ttheses to load the text or Python file data onto that variable.\n\tEnter "close Python" to exit.')
        while command != 'close Python':
            command = input('\t')
            if command == 'close Python':
                pass
            elif command == 'save':
                savename = input('\tPlease enter a name to save your file.\n\t')
                savefiles[savename] = ['python', x]
            elif command == 'run':
                exec(x)
            else:
                x = (f'{x}\n{command}')
    elif command == 'open Python shell':
        x = ''
        print('\tUse the Python Shell to test projects only.\n\tCode in the Python shell cannot be saved.\n\tSet a variable to "loadtext" (no quotes) followed by a text or Python file name in parentheses to load the text or Python file data onto that variable.\n\tEnter "exit shell" to exit.')
        while command != 'close shell':
            command = input('\t>')
            if not command == 'close shell':
                x = (f'{x}\n{command}')
                exec(x)
    elif command == 'exit terminal':
        if input('\tAre you sure? All of your projects will be deleted when you exit the terminal.\n\tEnter "exit" to exit the terminal. Enter anything else to cancel.\n\t') == 'exit':
            break
    elif command == 'open text creaator':
        print('Type "$save$" to save.\nType "$close$" to exit.')
        while command != '$close$':
            command = input('\t')
            if command == '$save$':
                savename = input('\tPlease enter a name to save your file.\n')
                savefiles[savename] = ['text', x]
            elif command == '$close$':
                pass
            else:
                x = (f'{x}\n{command}')
    elif command == 'open file':
        filename = input('\tEnter the name of the file you would like to open:\n\t')
        if savefiles[filename][0] == 'python':
            print('\tEnter "run" to run the program.\n\tEnter "view" to view the code.\n\tEnter "close file" to exit.')
        else:
            print('\tEnter "run" or "view" to view the text.\n\tEnter "close file" to exit.')
        while command != 'close file':
            command = input('\t')
            if command == 'run':
                if savefiles[filename][0] == 'python':
                    exec(savefiles[filename][1])
                else:
                    print(savefiles[filename][1])
            elif command == 'view':
                print(savefiles[filename][1])
            elif command == 'close file':
                pass
            else:
                print('\tCommand not recognized. Please check spelling and punctuation.')
    elif command == 'delete all files':
        if input('\tType "delete" to delete all files. Type anything else to cancel.\n\t') == 'delete':
            for filename in savefiles:
                del savefiles[filename]
    elif command == 'delete file':
        filename = input('\tPlease enter the file that you would like to delete.\n\t')
        if input('\tType "delete" to delete file. Type anything else to cancel.\n\t') == 'delete':
            del savefiles[filename]
    elif command == 'help':
        function_help = input('\tEnter the function that you need help with or enter "all" to view everything.\n\tDo not type Python functions/keywords.\n\t')
        if function_help == 'all':
            print(f'\t{helplist}')
        else:
            print(f'\t{helplist[function_help]}')
    else:
        print('Command not recognized. Please check spelling and punctuation.')
    