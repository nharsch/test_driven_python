from django.test import TestCase # TestCase is augmented form Unittest.TestCase

# Create your tests here.
class SmokeTest(TestCase):

	def test_bad_maths(self):
		self.assertEqual(1, 2)
		