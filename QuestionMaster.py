from logger import *
from random import randrange
import os

class QuestionMaster:

    def __init__(self, load=True):
        self.questions = []
        if load:
            fileDir = os.path.dirname(os.path.realpath('__file__'))
            qpath = os.path.join(fileDir, "gameData/questionsample.txt")
            apath = os.path.join(fileDir, "gameData/answersample.txt")
            qlines = self.readFile(qpath)
            alines = self.readFile(apath)
            self.load(qlines, alines)

    def readFile(self, path):
        lines = ""
        try:
            with open(path) as f:
                lines = f.read().splitlines()
        except:
            log(self.__class__.__name__).warning("Failed to open file {}".format(path))

        return lines

    def load(self, qlines, alines):
        if len(alines) != len(qlines):
            log(self.__class__.__name__).warning("Failed to load question & answer mismatch")
            return

        for i in range(len(qlines)):
            formatted_qline = qlines[i].replace('\\n', '\n').replace('\\t', '\t')
            self.questions.append((formatted_qline, alines[i]))

    def generateQwithA(self):
        index = randrange(len(self.questions))
        return self.questions[index]

    def clear(self):
        self.questions.clear()

    def getQuestionsCount(self):
        return len(self.questions)



