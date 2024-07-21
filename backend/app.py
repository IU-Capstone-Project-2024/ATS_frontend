from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
import sqlite3

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")


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
            'timestamp': trade[4]
        } for trade in trades
    ]
    return jsonify(trades_list)


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
    _decisions = query_db("SELECT model, action, timestamp FROM decisions")
    action_mapping = {"sell": 0, "hold": -1, "buy": 0}
    result = [{"model": row[0], "action": action_mapping[row[1].lower()], "timestamp": row[2]} for row in _decisions]
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
                latest_decisions["result"] = latest_decisions["ml1"]
    else:
        latest_decisions = {"last_vote_time": "", "ml1": "", "ml2": "", "algo": "", "result": ""}
    return jsonify(latest_decisions)


@socketio.on('connect')
def handle_connect():
    print('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


def notify_frontend():
    socketio.emit('update_decision', {'data': 'update'})


if __name__ == '__main__':
    socketio.run(app, debug=True)
