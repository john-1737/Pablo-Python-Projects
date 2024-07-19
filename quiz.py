class quizlist:
    def __init__(self, quiz):
        self.questionlist = quiz
    def quizquestion(self,question):
        text = input(f'{question}\n')
        if text == self.questionlist[question]:
            return True
        else:
            return False
    def quizlist(self, correcttext, incorrecttext):
        score = 0
        for question in self.questionlist:
            text = input(f'{question}\n')
            if text == self.questionlist[question]:
                print(correcttext)
                score = score + 1
            else:
                print(incorrecttext)
        return score

         
def askquestion(question, answer):
    text = input(f'{question}\n')
    if text == answer:
        return True
    else:
        return False
    