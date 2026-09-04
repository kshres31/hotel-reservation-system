import tempfile, unittest
from datetime import date
from pathlib import Path
from innkeeper.service import Hotel

class HotelTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.hotel=Hotel(Path(self.temp.name)/"hotel.db"); self.hotel.initialize(); self.hotel.add_room(101,"queen",12900)
    def tearDown(self): self.temp.cleanup()
    def test_booking_blocks_overlapping_stay(self):
        self.hotel.book(101,"Alex",date(2026,9,10),date(2026,9,12))
        self.assertEqual(self.hotel.available(date(2026,9,11),date(2026,9,13)),[])
        self.assertEqual(len(self.hotel.available(date(2026,9,12),date(2026,9,13))),1)
    def test_cancel_releases_room(self):
        booking=self.hotel.book(101,"Sam",date(2026,10,1),date(2026,10,3)); self.hotel.cancel(booking)
        self.assertEqual(len(self.hotel.available(date(2026,10,1),date(2026,10,3))),1)
    def test_rejects_bad_dates(self):
        with self.assertRaisesRegex(ValueError,"check-out"): self.hotel.available(date(2026,9,3),date(2026,9,3))

if __name__=="__main__": unittest.main()

