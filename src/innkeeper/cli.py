import argparse
import math
import sqlite3
from datetime import date
from pathlib import Path
from .service import Hotel

def main(argv=None):
    parser=argparse.ArgumentParser(description="Manage hotel rooms and bookings"); parser.add_argument("--database",type=Path,default=Path("hotel.db")); subs=parser.add_subparsers(dest="command",required=True)
    room=subs.add_parser("add-room"); room.add_argument("number",type=int); room.add_argument("kind"); room.add_argument("price",type=float)
    available=subs.add_parser("available"); available.add_argument("check_in",type=date.fromisoformat); available.add_argument("check_out",type=date.fromisoformat)
    book=subs.add_parser("book"); book.add_argument("room",type=int); book.add_argument("guest"); book.add_argument("check_in",type=date.fromisoformat); book.add_argument("check_out",type=date.fromisoformat)
    cancel=subs.add_parser("cancel"); cancel.add_argument("booking_id",type=int); subs.add_parser("list")
    args=parser.parse_args(argv)
    if args.command=="add-room" and not math.isfinite(args.price):
        parser.error("price must be finite")
    hotel=Hotel(args.database); hotel.initialize()
    try:
        if args.command=="add-room": hotel.add_room(args.number,args.kind,round(args.price*100)); print("Room added.")
        elif args.command=="available":
            for row in hotel.available(args.check_in,args.check_out): print(f"Room {row[0]} | {row[1]} | ${row[2]/100:.2f}")
        elif args.command=="book": print(f"Booking #{hotel.book(args.room,args.guest,args.check_in,args.check_out)} created.")
        elif args.command=="cancel": hotel.cancel(args.booking_id); print("Booking cancelled.")
        else:
            for row in hotel.bookings(): print(row)
    except (ValueError,sqlite3.IntegrityError) as exc: parser.error(str(exc))
    return 0

if __name__=="__main__": raise SystemExit(main())
