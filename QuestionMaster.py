from logger import log
from random import randrange
from random import shuffle
import os
import json
import sys

class QuestionMaster:

    def __init__(self, load=True):
        self.questions = []
        if load:
            fileDir = os.path.dirname(os.path.realpath('__file__'))
            self.load(self.readFile(os.path.join(fileDir, "gameData/questions.json")))

    def readFile(self, path):
        lines = ""
        try:
            with open(path) as f:
                lines = f.readlines()
        except:
            log(self.__class__.__name__).warning("Failed to open file {}".format(path))

        return lines[0]

    def load(self, jsonStr):
        try:
            data = json.loads(jsonStr)
        except:
            log(self.__class__.__name__).warning("Unexpected error: {}".format(sys.exc_info()[0]))
            return 

        if "questions" in data:
            for item in data["questions"]:
                if "incorrect_answers" not in item or \
                    "correct_answer" not in item or \
                    "question" not in item or len(item["incorrect_answers"]) + 1 > 5:
                    log(self.__class__.__name__).warning("Reject question {}".format(item))
                    continue

                self.questions.append((item["question"],  item["incorrect_answers"], item["correct_answer"]))
        else:
            log(self.__class__.__name__).warning("Failed to find quetions tag when loading the questions")

    def formatQuestionText(self, questionStr, choices, ans):
        text = ['A', 'B', 'C', 'D', 'E']

        formattedQText = "{}\n".format(questionStr)
        ansText = "A"
        for i in range(len(choices)):
            if choices[i] == ans:
                ansText = text[i]
            formattedQText += "{}. {}\t".format(text[i], choices[i])

        return (formattedQText, ansText)

    def generateQwithA(self):
        index = randrange(len(self.questions))

        question, incorrect, correct = self.questions[index]
        choices = incorrect + [correct]
        shuffle(choices)

        qText, ansText = self.formatQuestionText(question, choices, correct)

        return (qText, ansText)

    def clear(self):
        self.questions.clear()

    def getQuestionsCount(self):
        return len(self.questions)



