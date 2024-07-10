from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)


def query_db(query, args=(), one=False):
    conn = sqlite3.connect("backend/db.sqlite")
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/api/trades', methods=['GET'])
def get_trades():
    trades = query_db("SELECT * FROM trades")
    trades_list = [
        {
            'id': trade[0],
            'trade_type': trade[1],
            'symbol': trade[2],
            'quantity': trade[3],
            'price': trade[4],
            'timestamp': trade[5]
        } for trade in trades
    ]
    return jsonify(trades_list)


@app.route('/api/stats', methods=['GET'])
def get_stats():
    trades = query_db("SELECT * FROM trades")

    # Filter trades into buys and sells
    buys = [trade for trade in trades if trade[1].lower() == 'buy']
    sells = [trade for trade in trades if trade[1].lower() == 'sell']

    total_buys = sum(trade[3] for trade in buys)
    total_sells = sum(trade[3] for trade in sells)

    avg_buy_price = sum(trade[4] * trade[3] for trade in buys) / total_buys if total_buys else 0
    avg_sell_price = sum(trade[4] * trade[3] for trade in sells) / total_sells if total_sells else 0

    # Calculate total profit as (sell price - average buy price) * quantity sold
    total_profit = total_sells * (avg_sell_price - avg_buy_price)

    stats = {
        'total_buys': total_buys,
        'total_sells': total_sells,
        'avg_buy_price': avg_buy_price,
        'avg_sell_price': avg_sell_price,
        'total_profit': total_profit
    }

    return jsonify(stats)


if __name__ == '__main__':
    app.run(debug=True)
