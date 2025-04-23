import sqlite3
import json

conn = sqlite3.connect("schedule_item.db")

c = conn.cursor()

c.execute("""CREATE TABLE schedule_item (
            title text,
            description text,
            start_date text,
            end_date text,
            priority level text,
            repetition text,
            repetition_days text
        )""")

repetition_days = [1]
c.execute("INSERT INTO schedule_item VALUES ('Projekt do skoly', 'Projekt do nejakeho predmetu', '2025-04-16 13:30', '2025-04-16 13:45', 'High', True, '[1]')")

conn.commit()

conn.close()