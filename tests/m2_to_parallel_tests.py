import unittest
from utils.m2_to_parallel import *


class M2ToParallelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        test_path = '/home/yli/gec-docs/conll14st-test-data/noalt/official-2014.combined.m2'
        test_file = open(test_path)
        cls.m2_file = test_file.read().strip().split("\n\n")
        test_file.close()

    def test_process_chunks(self):
        orig, corr = process_chunks(self.m2_file)
        self.assertEqual(len(orig), len(corr))
        self.assertEqual(len(orig), len(self.m2_file))


if __name__ == '__main__':
    unittest.main()
