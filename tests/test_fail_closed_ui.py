import unittest
from monitor.state import classify, State, Observation

class FailClosedTests(unittest.TestCase):
    def test_decorative_green_is_not_availability(self):
        self.assertEqual(classify(Observation(True,False,0,("turf",))),State.MAP_ERROR)
    def test_no_claim_from_unverified_map(self):
        self.assertEqual(classify(Observation(True,True,1)),State.NO_AVAILABILITY)

if __name__=="__main__":unittest.main()
