questions = {'What is Taylor Swift\'s favorite number?' : '13',
             "Which jewelry is commonly worn by Swifties?\nA = rings B = necklaces C = bracelets" : "C",
             "True or false : Taylor Swift's first album was Red." : 'F',
             "What is Taylor Swift's favorite color?\nA = red B = purple C = blue" : 'B',
             "When did Taylor Swift receive her first award?\nA = 2006 B = 2007 C = 2008" : 'B',
             'How old was Taylor Swift when she released her first album?' : '16',
             'How many cats does Taylor Swift have as of 2023?' : '3'}
def gamestart():
    print("It's time for a Taylor Swift quiz!\nHere are some instructions for the quiz:")
    print("On open-ended questions, type your answer.\nOn multiple-choice questions, type the letter of your choice.\nOn true or false questions, enter T for true and F for false.\nYou get one point per question. There are 7 questions.")
def quiz():
    global score
    score = 0
    for x in questions:
        answerinput = input(f'{x}\n')
        if answerinput == questions[x]:
            print('Correct!')
            score = score + 1
        else:
            print('Incorrect!')
        print(f'Current score : {score}')
gamestart()
if input('Type "go" to begin!\n') == 'go':
    quiz()
    print('You completed the quiz!')  
    print(f'Your score is {score}!')