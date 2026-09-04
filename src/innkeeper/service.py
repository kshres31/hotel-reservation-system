import sqlite3
from contextlib import closing
from datetime import date
from pathlib import Path

class Hotel:
    def __init__(self,database: Path): self.database=database
    def initialize(self):
        self.database.parent.mkdir(parents=True,exist_ok=True)
        with closing(sqlite3.connect(self.database)) as connection:
            connection.executescript("""CREATE TABLE IF NOT EXISTS rooms(number INTEGER PRIMARY KEY, kind TEXT NOT NULL, nightly_cents INTEGER NOT NULL CHECK(nightly_cents>0)); CREATE TABLE IF NOT EXISTS bookings(id INTEGER PRIMARY KEY, room_number INTEGER NOT NULL REFERENCES rooms(number), guest TEXT NOT NULL, check_in TEXT NOT NULL, check_out TEXT NOT NULL, cancelled INTEGER NOT NULL DEFAULT 0);"""); connection.commit()
    def add_room(self,number:int,kind:str,nightly_cents:int):
        if nightly_cents<1: raise ValueError("price must be positive")
        self._execute("INSERT INTO rooms VALUES (?,?,?)",(number,kind.strip(),nightly_cents))
    def available(self,check_in:date,check_out:date):
        self._dates(check_in,check_out)
        query="""SELECT number,kind,nightly_cents FROM rooms WHERE number NOT IN (SELECT room_number FROM bookings WHERE cancelled=0 AND check_in < ? AND check_out > ?) ORDER BY number"""
        with closing(sqlite3.connect(self.database)) as connection: return connection.execute(query,(check_out.isoformat(),check_in.isoformat())).fetchall()
    def book(self,room:int,guest:str,check_in:date,check_out:date)->int:
        if not guest.strip(): raise ValueError("guest name is required")
        if room not in {row[0] for row in self.available(check_in,check_out)}: raise ValueError("room is not available")
        with closing(sqlite3.connect(self.database)) as connection:
            cursor=connection.execute("INSERT INTO bookings(room_number,guest,check_in,check_out) VALUES (?,?,?,?)",(room,guest.strip(),check_in.isoformat(),check_out.isoformat())); connection.commit(); return int(cursor.lastrowid)
    def cancel(self,booking_id:int): self._execute("UPDATE bookings SET cancelled=1 WHERE id=?",(booking_id,))
    def bookings(self):
        with closing(sqlite3.connect(self.database)) as connection: return connection.execute("SELECT id,room_number,guest,check_in,check_out,cancelled FROM bookings ORDER BY id DESC").fetchall()
    def _execute(self,query,params):
        with closing(sqlite3.connect(self.database)) as connection: connection.execute(query,params); connection.commit()
    @staticmethod
    def _dates(check_in,check_out):
        if check_out<=check_in: raise ValueError("check-out must be after check-in")

