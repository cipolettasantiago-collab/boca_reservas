import unittest
from booking_state import ReservationEvidence, reservation_confirmed

class BookingStateTests(unittest.TestCase):
    def test_green_sector_is_not_booking(self):
        self.assertFalse(reservation_confirmed(ReservationEvidence(match_id="878",sector="PRN3")))
    def test_cart_without_provider_proof_is_not_booking(self):
        self.assertFalse(reservation_confirmed(ReservationEvidence(match_id="878",reservation_id="temporary",sector="PRN3",seat="72")))
    def test_complete_provider_proof(self):
        self.assertTrue(reservation_confirmed(ReservationEvidence(match_id="878",reservation_id="confirmed-123",confirmed_by_provider=True,sector="PRN3",seat="72")))

if __name__ == "__main__": unittest.main()
