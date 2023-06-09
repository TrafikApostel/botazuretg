from time import sleep
from tcp_latency import *
import datetime
import sqlite3
conn = sqlite3.connect('servers.db',check_same_thread=False)
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS servers(
   userid INT,
   email TEXT,
   password TEXT,
   ip TEXT,
   log TEXT,
   pas Text,
   time_add Text,
   status Text,
   status_use Text,
   time_die Text,
   money Text
   );
""")
conn.commit()
def cheack(ip):
    try:
        r = measure_latency(host=ip, port=3389, runs=2, timeout=2.5)
    except:
        return False
    if len(r)!=0:
        return True
    else:
        return False
while True:
    records = cur.execute("SELECT * FROM servers")
    all_orders = cur.fetchall()
    for order in all_orders:
        r = cheack(order[3])
        if r == False:
            sqlite_update_query = """Update servers set status = ?, time_die = ? where email = ?"""
            cur.executemany(sqlite_update_query, [('hz',f'{datetime.date.today()} {datetime.datetime.now().hour}:{datetime.datetime.now().minute}' ,order[1])])
            conn.commit()
        else:
            str_d1 = order[6].split(' ')[0]
            str_d2 = str(datetime.datetime.now()).split(' ')[0]
            d1 = datetime.datetime.strptime(str_d1, "%Y-%m-%d")
            d2 = datetime.datetime.strptime(str_d2, "%Y-%m-%d")
            delta = d2 - d1
            if delta.days >= 4:
                sqlite_update_query = """Update servers set money = ? where email = ?"""
                cur.executemany(sqlite_update_query, [('pay',order[1])])
                conn.commit()
    sleep(10000)
    sleep(10000)
    sleep(10000)
    sleep(10000)
    sleep(10000)
    sleep(10000)
    sleep(10000)
    sleep(10000)
    sleep(6400)
