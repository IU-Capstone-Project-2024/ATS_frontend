from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
SQLITE_DB_PATH = "backend/db.sqlite"
CORS(app)


def query_db(query, args=(), one=False):
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/api/trades', methods=['GET'])
def get_trades():
    trades = query_db("SELECT * FROM trades")
    return jsonify(trades)


if __name__ == '__main__':
    app.run(debug=True)
