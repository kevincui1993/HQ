import unittest
from QuestionMaster import QuestionMaster
import os

class QuestionMasterTestU(unittest.TestCase):

    def atest_readFile_valid_path(self):
        qMaster = QuestionMaster(False)
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        
        lines = qMaster.readFile(os.path.join(fileDir, "gameData/questions.json"))

        self.assertTrue(lines != "")


    def atest_readFile_invalid_path(self):
        qMaster = QuestionMaster(False)
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        
        lines = qMaster.readFile(os.path.join(fileDir, "somebadfilepath"))

        self.assertTrue(lines == "")
    
    def atest_generateQwithA_valid_result(self):
        qMaster = QuestionMaster()

        q,a = qMaster.generateQwithA()

        self.assertTrue(q != "")
        self.assertTrue(a.lower() in ["a","b","c",'d','e'])

    def test_load_quesion_valid_data(self):
        qMaster = QuestionMaster(False)

        qMaster.load("{\"questions\":[{\"question\":\"Krusty is the guild master of which guild in Log Horizon?\",\"correct_answer\":\"D. D. D\",\"incorrect_answers\":[\"Silver Sword\",\"West Wind Brigade\",\"Oceanic Systems (Marine Agency)\"]}]}")

        self.assertEqual(qMaster.getQuestionsCount(), 1)

    def test_load_quesion_missing_questions_tag(self):
        qMaster = QuestionMaster(False)

        qMaster.load("{\"a\":[{\"question\":\"Krusty is the guild master of which guild in Log Horizon?\",\"correct_answer\":\"D. D. D\",\"incorrect_answers\":[\"Silver Sword\",\"West Wind Brigade\",\"Oceanic Systems (Marine Agency)\"]}]}")

        self.assertEqual(qMaster.getQuestionsCount(), 0)


    def test_load_quesion_missing_question_tag(self):
        qMaster = QuestionMaster(False)

        qMaster.load("{\"questions\":[{\"correct_answer\":\"D. D. D\",\"incorrect_answers\":[\"Silver Sword\",\"West Wind Brigade\",\"Oceanic Systems (Marine Agency)\"]}]}")

        self.assertEqual(qMaster.getQuestionsCount(), 0)

    def test_load_quesion_missing_incorrect_answers_tag(self):
        qMaster = QuestionMaster(False)

        qMaster.load("{\"questions\":[{\"question\":\"Krusty is the guild master of which guild in Log Horizon?\",\"correct_answer\":\"D. D. D\"}]}")

        self.assertEqual(qMaster.getQuestionsCount(), 0)

    def test_load_quesion_missing_correct_answers_tag(self):
        qMaster = QuestionMaster(False)

        qMaster.load("{\"questions\":[{\"question\":\"Krusty is the guild master of which guild in Log Horizon?\",\"incorrect_answers\":[\"Silver Sword\",\"West Wind Brigade\",\"Oceanic Systems (Marine Agency)\"]}]}")

        self.assertEqual(qMaster.getQuestionsCount(), 0)

    def test_load_quesion_malform_json(self):
        qMaster = QuestionMaster(False)

        qMaster.load("{\"questions\":[{\"question\":\"Krusty is the guild master of which guild in Log Horizon?\",\"correct_answer\":\"D. D. D\",\"incorrect_answers\":[\"Silver Sword\",\"West Wind Brigade\",\"Oceanic Systems (Marine Agency)\"]")

        self.assertEqual(qMaster.getQuestionsCount(), 0)

    def test_formatQuestionText_multiple_choices(self):
        qMaster = QuestionMaster(False)
        questionStr, choices, ans = "question?", ["ans1", "ans2", "ans3", "ans4"], "ans4"

        formattedQText, ansText, numChoices = qMaster.formatQuestionText(questionStr, choices, ans)

        self.assertTrue("question?" in formattedQText)
        self.assertTrue("A. " in formattedQText)
        self.assertTrue("\tB. " in formattedQText)
        self.assertTrue("\tC. " in formattedQText)
        self.assertTrue("\tD. " in formattedQText)
        self.assertTrue("\tE. " not in formattedQText)
        self.assertEquals(formattedQText[formattedQText.find(ans)-3], ansText)
        self.assertEquals(numChoices, len(choices))

    def test_formatQuestionText_true_false(self):
        qMaster = QuestionMaster(False)
        questionStr, choices, ans = "question?", ["true","false"], "true"

        formattedQText, ansText, numChoices = qMaster.formatQuestionText(questionStr, choices, ans)

        self.assertTrue("question?" in formattedQText)
        self.assertTrue("A. " in formattedQText)
        self.assertTrue("\tB. " in formattedQText)
        self.assertTrue("\tC. " not in formattedQText)
        self.assertTrue("\tD. " not in formattedQText)
        self.assertTrue("\tE. " not in formattedQText)
        self.assertEquals(formattedQText[formattedQText.find(ans)-3], ansText)
        self.assertEquals(numChoices, len(choices))

        
if __name__ == '__main__':
    unittest.main()