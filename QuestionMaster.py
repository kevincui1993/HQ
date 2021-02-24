from logger import log
from random import randrange
from random import shuffle
import os
import json
import sys

class QuestionMaster:
    '''
    This class is responsible for storing and generating quetions and answers

    Attributes
    ----------
    questions : list(tuple)
        stores questions 
    '''

    def __init__(self, load=True):
        self.questions = []
        if load:
            fileDir = os.path.dirname(os.path.realpath('__file__'))
            self.load(self.readFile(os.path.join(fileDir, "gameData/questions.json")))

    def readFile(self, path):
        ''' 
        Opens up a file and read all lines from it. 

        Parameters:
            path (str): file path

        Returns:
            lines[0] (str) : the first line of the file
        '''

        lines = ""
        try:
            with open(path) as f:
                lines = f.readlines()
        except:
            log(self.__class__.__name__).warning("Failed to open file {}".format(path))

        return lines[0]

    def load(self, jsonStr):
        ''' 
        Read and parse jsonStr to store questions and answers internally 

        Parameters:
            jsonStr (str): a json string that holds questions and answers

        Returns:
            Nothing
        '''

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
                    log(self.__class__.__name__).warning("Rejected question {}".format(item))
                    continue

                self.questions.append((item["question"],  item["incorrect_answers"], item["correct_answer"]))
        else:
            log(self.__class__.__name__).warning("Failed to find quetions tag when loading the questions")

    def formatQuestionText(self, questionStr, choices, ans):
        ''' 
        Formats the question so it can be nicely displayed to players 

        Parameters:
            questionStr (str): a string containing the question
            choices (list(str)): a list containing multiple choices 
            ans (str): the answer 

        Returns:
            (formattedQText, ansText) (str, str) : a tuple with formatted text and the answer's tag
        '''

        text = ['A', 'B', 'C', 'D', 'E']

        formattedQText = "{}\n".format(questionStr)
        ansText = "A"
        for i in range(len(choices)):
            if choices[i] == ans:
                ansText = text[i]
            formattedQText += "{}. {}\t".format(text[i], choices[i])

        return (formattedQText, ansText)

    def generateQwithA(self):
        ''' 
        Generate a random question with choices randomized 

        Parameters:
            Nothing

        Returns:
            (qText, ansText) (str, str) : a tuple with formatted text and the answer's tag
        '''

        index = randrange(len(self.questions))

        question, incorrect, correct = self.questions[index]
        choices = incorrect + [correct]
        shuffle(choices)

        return self.formatQuestionText(question, choices, correct)

    def clear(self):
        ''' 
        clears all questions 

        Parameters:
            Nothing

        Returns:
            Nothing
        '''

        self.questions.clear()

    def getQuestionsCount(self):
        ''' 
        Gets the number of questions 

        Parameters:
            Nothing

        Returns:
            len(self.questions) (int) : number of questions
        '''

        return len(self.questions)



