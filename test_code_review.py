import unittest
from code_review import review_code

class TestCodeReview(unittest.TestCase):
    def test_review_code(self):
        """ Test that the review function returns a non-empty response. """
        test_file = "test_sample.py"  # Create a small Python file for testing
        with open(test_file, "w") as f:
            f.write("print('Hello, World!')")

        result = review_code(test_file)
        self.assertTrue(len(result) > 0, "Review should not be empty.")

if __name__ == "__main__":
    unittest.main()
