from flask import Flask, render_template, request, url_for, g, redirect, jsonify
from sqlite_demo import *
from datetime import datetime

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

def get_db():
    """Get a thread-local database connection"""
    if 'db' not in g:
        g.db = ScheduleDB()
    return g.db

def day_of_the_week(results):
    days = {
        0: [],  # Monday
        1: [],  # Tuesday
        2: [],  # Wednesday
        3: [],  # Thursday
        4: [],  # Friday
        5: [],  # Saturday
        6: []   # Sunday
    }

    for row in results:
        dt = datetime.fromisoformat(row[2])
        day_of_week = dt.weekday()
        days[day_of_week].append(row)

    ordered_results = []
    for day in range(7):  # 0-6 for Monday-Sunday
        ordered_results.extend(days[day])
    
    print(days)
    return ordered_results

@app.teardown_appcontext
def close_db(e=None):
    """Close the database at the end of each request"""
    db = g.pop('db', None)
    if db is not None:
        db.conn.close()

@app.route('/')
def main():
    db = get_db()
    db.c.execute("SELECT * FROM schedule_item ORDER BY start_time")
    results = db.c.fetchall()
    return render_template('index.html', results = results, datetime=datetime)

@app.route('/add', methods=['POST', 'GET'])
def add_schedule_item():
    db = get_db()
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        priority_level = request.form.get('priority_level')
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
    start_time = datetime.strptime(start_time, '%H:%M').time()
    end_time = datetime.strptime(end_time, '%H:%M').time()

    item = ScheduleItem(
        title,
        description,
        start_time,
        end_time,
        priority_level,
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

    