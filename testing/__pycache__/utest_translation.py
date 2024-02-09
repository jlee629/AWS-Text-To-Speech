import os, sys
import unittest

import translation_service

class TranslationServiceTest(unittest.TestCase):
    def setUp(self):
        self.service = translation_service.TranslationService()

    def test_translate_text(self):
        translation = self.service.translate_text('웃다')
        self.assertTrue(translation)
        self.assertEqual('ko', translation['sourceLanguage'])
        self.assertEqual('laugh', translation['translatedText'])
        print('OK test for translation')
        

if __name__ == "__main__":
    unittest.main()