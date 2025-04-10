from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
import sqlite3
import threading
import time
import requests
from datetime import datetime, timedelta


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

current_session_price = 0


def query_db(query, args=(), one=False):
    conn = sqlite3.connect("backend/db.sqlite")
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/api/trades', methods=['GET'])
def get_trades():
    trades = query_db("SELECT * FROM logs")
    trades_list = [
        {
            'id': trade[0],
            'trade_type': trade[1],
            'symbol': "BTCUSDT",
            'quantity': trade[2],
            'price': trade[3],
            'timestamp': (datetime.strptime(trade[4], '%Y-%m-%d %H:%M:%S') + timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')
        } for trade in trades
    ]
    return jsonify(trades_list)


@app.route('/api/btc_price', methods=['GET'])
def get_btc_price():
    global current_session_price
    if current_session_price == 0:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
        data = response.json()
        current_session_price = float(data['bitcoin']['usd'])
    return jsonify({'price': current_session_price})


@app.route('/api/stats', methods=['GET'])
def get_stats():
    trades = query_db("SELECT * FROM logs")
    buys = [trade for trade in trades if trade[1].lower() == 'buy']
    sells = [trade for trade in trades if trade[1].lower() == 'sell']

    total_buys = sum(float(trade[2]) for trade in buys)
    total_sells = sum(float(trade[2]) for trade in sells)

    avg_buy_price = sum(float(trade[3]) * float(trade[2]) for trade in buys) / total_buys if total_buys else 0
    avg_sell_price = sum(float(trade[3]) * float(trade[2]) for trade in sells) / total_sells if total_sells else 0

    total_profit = total_sells * (avg_sell_price - avg_buy_price)

    stats = {
        'total_buys': total_buys,
        'total_sells': total_sells,
        'avg_buy_price': avg_buy_price,
        'avg_sell_price': avg_sell_price,
        'total_profit': total_profit
    }

    return jsonify(stats)


@app.route('/api/decisions', methods=['GET'])
def get_decisions():
    _decisions = query_db("SELECT model, action, timestamp FROM decisions WHERE model='Result'")
    action_mapping = {"sell": -1, "hold": 0, "buy": 1}
    result = [{"model": row[0], "action": action_mapping[row[1].lower()], "timestamp": (datetime.strptime(
        row[2], '%Y-%m-%d %H:%M:%S') + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S')} for row in _decisions]
    return jsonify(result)


@app.route('/api/get_latest_decision', methods=['GET'])
def get_latest_decision():
    decisions = query_db("SELECT model, action, timestamp FROM decisions ORDER BY timestamp DESC")
    action_mapping = {"sell": "sell", "hold": "hold", "buy": "buy"}
    if decisions:
        latest_timestamp = decisions[0][2]
        latest_decisions = {"last_vote_time": latest_timestamp, "ml1": "", "ml2": "", "algo": "", "result": ""}
        for row in decisions:
            if row[2] == latest_timestamp:
                if row[0] == "Knife":
                    latest_decisions["ml1"] = action_mapping[row[1].lower()]
                elif row[0] == "Sparse":
                    latest_decisions["ml2"] = action_mapping[row[1].lower()]
                elif row[0] == "Algorithms":
                    latest_decisions["algo"] = action_mapping[row[1].lower()]
                elif row[0] == "Result":
                    latest_decisions["result"] = action_mapping[row[1].lower()]
    else:
        latest_decisions = {"last_vote_time": "", "ml1": "", "ml2": "", "algo": "", "result": ""}
    latest_decisions["last_vote_time"] = (datetime.strptime(latest_timestamp, '%Y-%m-%d %H:%M:%S') +
                                          timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')
    print(latest_decisions)
    return jsonify(latest_decisions)


@ socketio.on('connect')
def handle_connect():
    print('Client connected')


@ socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


def notify_frontend():
    while True:
        socketio.emit('update_decision', {'data': 'update'})
        time.sleep(3)  # Wait for 3 seconds before sending the next update


def start_notification_thread():
    notification_thread = threading.Thread(target=notify_frontend)
    notification_thread.daemon = True  # Daemonize the thread so it automatically dies when the main thread exits
    notification_thread.start()


if __name__ == '__main__':
    start_notification_thread()
    socketio.run(app, debug=True)
