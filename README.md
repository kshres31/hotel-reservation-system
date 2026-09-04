# Innkeeper

A small SQLite-backed hotel reservation system that tracks rooms, guests, stays, availability, and cancellations.

```powershell
$env:PYTHONPATH = "src"
python -m innkeeper.cli add-room 101 queen 129
python -m innkeeper.cli available 2026-09-10 2026-09-12
python -m innkeeper.cli book 101 "Alex Smith" 2026-09-10 2026-09-12
python -m innkeeper.cli list
```

Bookings use half-open date ranges, so a new guest may check in on the previous guest's check-out date. Run tests with `python -m unittest discover -s tests -v`.

