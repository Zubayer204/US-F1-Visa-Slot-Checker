import sqlite3
from datetime import date, datetime
import pytz
from flask import Flask, render_template, request, jsonify
app = Flask(__name__, static_folder='static')

@app.route('/')
def home():

    conn = sqlite3.connect("database.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM data")
    result = cursor.fetchone()
    slot_date = result[1].strftime("%d %B")
    updated_at = result[2]
    conn.close()

    return render_template('index.html', slot_date=slot_date, updated_at=updated_at)

@app.route('/update')
def get_data():
    conn = sqlite3.connect("database.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM data")
    result = cursor.fetchone()
    slot_date = result[1].strftime("%d %B")
    updated_at = result[2]
    conn.close()

    return jsonify({"slot_date": slot_date, "updated_at": updated_at})


@app.route("/set_alert", methods=['GET', 'POST'])
def set_alert():
    if request.method == "POST":
        email = request.form.get('email')
        notif_date = request.form.get('notif_date')
        notif_date_obj = datetime.strptime(notif_date, "%Y-%m-%d").date()
        
        conn = sqlite3.connect("database.db", detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = conn.cursor()
        cursor.execute('''INSERT OR REPLACE INTO alarms (email, notif_date) VALUES (?, ?)''', (email, notif_date_obj))
        conn.commit()
        conn.close()

        return render_template("alert.html", data={
            'success': True, 'msg': f"Alert created for {notif_date} or earlier!"}
        )
    else:
        return render_template("alert.html")
    

@app.route("/delete_alert", methods=['GET', 'POST'])
def delete_alert():
    if request.method == 'POST':
        email = request.form.get("email")
        conn = sqlite3.connect("database.db", detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM alarms WHERE email = ?''', (email,))
        result = cursor.fetchone()
        if result:
            cursor.execute("DELETE FROM alarms WHERE id = ?", (result[0],))
            conn.commit()
            conn.close()
            return render_template("delete.html", data={
                "success": True,
                "msg": "Successfully deleted your alert!"
            })
        
        conn.close()
        return render_template("delete.html", data={
            "success": False,
            "msg": "No alerts found for your email"
        })
    
    return render_template("delete.html")


if __name__ == '__main__':
    app.run(debug=True)