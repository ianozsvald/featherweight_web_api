import unittest
import numpy as np
import featherweight_api as fthr

# the start of some very trivial tests to enable numpy->JSON encoding

class Test(unittest.TestCase):
    def test_encoding(self):
        d = 'something'
        response = fthr.jsonify_numpy(d)

        d = np.array([0])
        response = fthr.jsonify_numpy(d)

