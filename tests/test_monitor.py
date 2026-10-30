import unittest
from monitor.state import Observation, State, classify
from monitor.runner import monitor_once

class FakeAdapter:
    def __init__(self, observation): self.observation=observation
    def read_observation(self): return self.observation

class MonitorTests(unittest.TestCase):
    def test_session_expired(self):
        self.assertEqual(classify(Observation(False,False,0)),State.AUTH_REQUIRED)
    def test_empty_map_not_sold_out(self):
        self.assertEqual(classify(Observation(True,False,0)),State.MAP_ERROR)
    def test_grey_sectors(self):
        self.assertEqual(classify(Observation(True,True,24)),State.NO_AVAILABILITY)
    def test_green_sector_unverified(self):
        self.assertEqual(classify(Observation(True,True,24,("PRN3",))),State.POSSIBLE_AVAILABILITY)
    def test_verified_seat(self):
        self.assertEqual(classify(Observation(True,True,24,("PRN3",),True)),State.CONFIRMED_AVAILABILITY)
    def test_stop_on_auth_failure(self):
        self.assertFalse(monitor_once(FakeAdapter(Observation(False,False,0)))["retry"])

if __name__=="__main__": unittest.main()
