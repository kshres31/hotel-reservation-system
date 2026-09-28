import contextlib
import io
import sqlite3
import tempfile
import unittest
from pathlib import Path

from innkeeper.cli import main


class RoomPriceTests(unittest.TestCase):
    def test_nonfinite_prices_are_rejected_before_creating_database(self):
        with tempfile.TemporaryDirectory() as folder:
            database = Path(folder) / "hotel.db"
            for price in ("nan", "inf", "-inf"):
                with self.subTest(price=price):
                    errors = io.StringIO()
                    with contextlib.redirect_stderr(errors), self.assertRaises(SystemExit) as error:
                        main(["--database", str(database), "add-room", "101", "queen", "--", price])
                    self.assertEqual(error.exception.code, 2)
                    self.assertIn("price must be finite", errors.getvalue())
                    self.assertFalse(database.exists())

    def test_finite_price_still_creates_room(self):
        with tempfile.TemporaryDirectory() as folder:
            database = Path(folder) / "hotel.db"
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main(["--database", str(database), "add-room", "101", "queen", "129.50"]), 0)
            with contextlib.closing(sqlite3.connect(database)) as connection:
                self.assertEqual(connection.execute("SELECT nightly_cents FROM rooms WHERE number=101").fetchone(), (12950,))
