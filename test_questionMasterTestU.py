import unittest
from QuestionMaster import QuestionMaster
import os

class QuestionMasterTestU(unittest.TestCase):

    def test_load_quesion_match_answers(self):
        qMaster = QuestionMaster(False)

        qMaster.load(["question1", "question2"], ["answer1", "answer2"])

        self.assertEqual(qMaster.getQuestionsCount(), 2)

    def test_load_quesion_mismatch_answers(self):
        qMaster = QuestionMaster(False)

        qMaster.load(["question1", "questions2"], ["answer1"])

        self.assertEqual(qMaster.getQuestionsCount(), 0)

    def test_load_answers_mismatch_quesion(self):
        qMaster = QuestionMaster(False)

        qMaster.load(["question1"], ["answer1", "answer2"])

        self.assertEqual(qMaster.getQuestionsCount(), 0)


    def test_readFile_valid_path(self):
        qMaster = QuestionMaster(False)
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        
        lines = qMaster.readFile(os.path.join(fileDir, "gameData/questionsample.txt"))

        self.assertTrue(lines != "")


    def test_readFile_invalid_path(self):
        qMaster = QuestionMaster(False)
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        
        lines = qMaster.readFile(os.path.join(fileDir, "somebadfilepath"))

        self.assertTrue(lines == "")
    
    def test_generateQwithA_valid_result(self):
        qMaster = QuestionMaster()

        q,a = qMaster.generateQwithA()

        self.assertTrue(q != "")
        self.assertTrue(a.lower() in ["a","b","c",'d'])

if __name__ == '__main__':
    unittest.main()