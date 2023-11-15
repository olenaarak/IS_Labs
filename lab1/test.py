import unittest

import reader
from knowledge_base import KnowledgeBase

class KnowledgeBaseTest(unittest.TestCase):

    def setUp(self):
        self.input = reader.parse_input()
        self.knowledge_base = KnowledgeBase()
        for item in self.input:
            self.knowledge_base.add(item)

    def test_child_parent(self):
        question = reader.parse_fact('Child child2 ?X')
        answer = self.knowledge_base.query(question)
        self.assertEqual(str(answer[0]), '?X : father1')
        self.assertEqual(str(answer[1]), '?X : mother1')

    def test_grandchild(self):
        question = reader.parse_fact('GrandChild child2 ?X')
        answer = self.knowledge_base.query(question)
        self.assertEqual(str(answer[0]), '?X : grandmother2')
        self.assertEqual(str(answer[1]), '?X : grandfather1')

    def test_son_in_law(self):
        question = reader.parse_fact("SonInLaw father1 ?X")
        answer = self.knowledge_base.query(question)
        self.assertEqual(str(answer[0]), "?X : grandfather1")

    def test_daughter_in_law(self):
        question = reader.parse_fact("DaughterInLaw mother1 ?X")
        answer = self.knowledge_base.query(question)
        self.assertEqual(str(answer[0]), "?X : grandmother2")

    def test_sibling_in_law(self):
        question = reader.parse_fact("SiblingInLaw mother2 ?X")
        answer = self.knowledge_base.query(question)
        self.assertEqual(str(answer[0]), "?X : father1")


if __name__ == '__main__':
    unittest.main()
