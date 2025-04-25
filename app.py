from flask import Flask, render_template, request, url_for, g, redirect
from sqlite_demo import *

app = Flask(__name__)

def get_db():
    """Get a thread-local database connection"""
    if 'db' not in g:
        g.db = ScheduleDB()
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    """Close the database at the end of each request"""
    db = g.pop('db', None)
    if db is not None:
        db.conn.close()

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/add', methods=['POST', 'GET'])
def add_schedule_item():
    db = get_db()
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        priority_level = request.form.get('priority_level')
        repetition = request.form.get('repetition')
        repetition_days = []
        days_mapping = {
            'Monday': 0,
            'Tuesday': 1,
            'Wednesday': 2,
            'Thursday': 3,
            'Friday': 4,
            'Saturday': 5,
            'Sunday': 6
        }
        for day in days_mapping:
            if request.form.get(day):
                repetition_days.append(days_mapping[day])
    else:
        return render_template('add.html')

    item = ScheduleItem(
        title,
        description,
        datetime.datetime(2025, 4, 16, 13, 30, 45),
        datetime.datetime(2025, 4, 16, 13, 45, 45),
        priority_level,
        repetition,
        repetition_days
    )
    try:
        db.insert_item(item)
        db.c.execute("SELECT * FROM schedule_item")
        print(db.c.fetchall())
        close_db()
        return redirect('/add')
    except:
        return "There was an issue adding your event"

if __name__ == "__main__":
    app.run(debug=True)


    