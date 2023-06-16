import traceback
import telebot
from tcp_latency import measure_latency
from telebot import types
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
bot = telebot.TeleBot('6167631724:AAHsvrI5EDAjwYqCfasc8bjVNv-sqwQrVV8')
accaunts = {}
def cheack(ip):
    try:
        r = measure_latency(host=ip, port=3389, runs=2, timeout=2.5)
    except:
        return False
    if len(r)!=0:
        return True
    else:
        return False
@bot.message_handler(content_types=['text', 'document', 'audio','photo','video','voice','video_note'])
def get_text_messages(message):
    try:
        exit = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("Основное меню", callback_data='exit')
        exit.add(btn1)
        if message.text == '/start':
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton("Добавить аккаунт", callback_data='add_ac')
            btn2 = types.InlineKeyboardButton("Сколько машин я сделал", callback_data='statistic')
            btn3 = types.InlineKeyboardButton("Удалить аккант", callback_data='del')
            btn4 = types.InlineKeyboardButton("Починить аккаунт", callback_data='error')
            markup.add(btn1,btn3)
            markup.add(btn4,btn2)
            bot.send_message(message.from_user.id,'Ебать функциОнал',reply_markup=markup)
        elif message.text.split(' ')[0] == '/give' and message.from_user.username == 'HelloUserName0':
            records = cur.execute("SELECT * FROM servers")
            all_orders = cur.fetchall()
            i = 1
            acs=[]
            for order in all_orders:
                if order[-4] == 'good' and order[-3] == 'new':
                    i += 1
                    sqlite_update_query = """Update servers set status_use = ? where ip = ?"""
                    cur.executemany(sqlite_update_query, [('old', order[3])])
                    conn.commit()
                    acs.append(f'{order[3]};{order[4]};{order[5]}')
            write_form = ''
            for ac in acs:
                write_form = write_form + ac + '\n'
            f = open('1.txt', 'w+')  # открытие в режиме записи
            f.write(write_form)
            f.close()
            bot.send_document(message.from_user.id,open('1.txt'),reply_markup=exit)
        elif message.text.split(' ')[0] == '/stat' and message.from_user.username == 'HelloUserName0':
            records = cur.execute("SELECT * FROM servers")
            all_orders = cur.fetchall()
            x = 0
            y = 0
            z = 0
            w = 0
            for order in all_orders:
                print(order)
                if order[-4] == 'good':
                    x+=1
                if order[-3] == 'new':
                    y += 1
                if order[-4] == 'hz':
                    z += 1
                    bot.send_message(message.from_user.id,f'Проверьте аккаунт {order[1]}|{order[2]} сервер {order[3]} не даёт ответ')
                if order[-4] == 'die':
                    w+=1
            bot.send_message(message.from_user.id,f'Живых {x} Новых {y} Ошибок {z} Мёртвых {w}')
        elif message.text == '/all' and message.from_user.username == 'HelloUserName0':
            records = cur.execute("SELECT * FROM servers")
            all_orders = cur.fetchall()
            for order in all_orders:
                bot.send_message(message.from_user.id, f'{order}')
        elif message.text == '/pay':#and message.from_user.username == 'HelloUserName0'
            acs_pay = {}
            records = cur.execute("SELECT * FROM servers")
            all_orders = cur.fetchall()
            for order in all_orders:
                if order[-1] == 'pay':
                    try:
                        acs_pay[order[0]] =acs_pay[order[0]]+1
                    except:
                        acs_pay[order[0]]=1
            for ac_pay in acs_pay:
                bot.send_message(message.from_user.id,f'Пользователь {str(ac_pay)} колличестов машин {acs_pay[ac_pay]}')
                sqlite_update_query = """Update servers set money = ? where userid = ?"""
                cur.executemany(sqlite_update_query, [('good', ac_pay)])
        else:
            bot.send_message(message.from_user.id, f'Я не понимаю о чём вы')
    except Exception as e:
        print(e)
        bot.send_message(message.from_user.id, f'❌ Ошибка, проверьте правильность написанния')
def step_del(message):
    records = cur.execute("SELECT * FROM servers")
    all_orders = cur.fetchall()
    test = False
    for order in all_orders:
        if order[1] == message.text:
            test = True
    sqlite_update_query = """Update servers set status = ?, time_die = ? where email = ?"""
    cur.executemany(sqlite_update_query, [('die',f'{datetime.date.today()} {datetime.datetime.now().hour}:{datetime.datetime.now().minute}' ,message.text)])
    conn.commit()
    exit = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Основное меню", callback_data='exit')
    exit.add(btn1)
    if test == True:
        bot.send_message(message.from_user.id, f'{message.text} успешно удалён',reply_markup=exit)
    else:
        bot.send_message(message.from_user.id, f'{message.text} не найден', reply_markup=exit)
def step_pas(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Добавить аккаунт", callback_data='add_ac')
    btn2 = types.InlineKeyboardButton("Сколько машин я сделал", callback_data='statistic')
    btn3 = types.InlineKeyboardButton("Удалить аккант", callback_data='del')
    btn4 = types.InlineKeyboardButton("Починить аккаунт", callback_data='error')
    markup.add(btn1, btn3)
    markup.add(btn4, btn2)
    exit = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Основное меню", callback_data='exit')
    exit.add(btn1)
    pas = message.text
    try:
        test = accaunts[message.from_user.id]['ip2']
        accaunts[message.from_user.id] = {'email': accaunts[message.from_user.id]['email'],
                                          'password': accaunts[message.from_user.id]['password'],
                                          'ip1': accaunts[message.from_user.id]['ip1'],
                                          'login1': accaunts[message.from_user.id]['login1'],
                                          'pas1': accaunts[message.from_user.id]['pas1'],'ip2': accaunts[message.from_user.id]['ip2'],
                                          'login2': accaunts[message.from_user.id]['login2'],
                                          'pas2': pas}
        data = (message.from_user.id, accaunts[message.from_user.id]['email'], accaunts[message.from_user.id]['password'], accaunts[message.from_user.id]['ip1'], accaunts[message.from_user.id]['login1'],
                accaunts[message.from_user.id]['pas1'],f'{datetime.date.today()} {datetime.datetime.now().hour}:{datetime.datetime.now().minute}','good','new','','wait')
        cur.execute("INSERT INTO servers VALUES(?, ?, ?, ?, ?, ?, ?,?,?,?,?);", data)
        conn.commit()
        data = (
        message.from_user.id, accaunts[message.from_user.id]['email'], accaunts[message.from_user.id]['password'],
        accaunts[message.from_user.id]['ip2'],
        accaunts[message.from_user.id]['login2'],
        accaunts[message.from_user.id]['pas2'],
        f'{datetime.date.today()} {datetime.datetime.now().hour}:{datetime.datetime.now().minute}', 'good','new','','wait')
        cur.execute("INSERT INTO servers VALUES(?, ?, ?, ?, ?, ?, ?,?,?,?,?);", data)
        conn.commit()
        bot.send_message(message.from_user.id, f'Вы успешно добавили аккаунт {accaunts[message.from_user.id]}', reply_markup=markup)
    except Exception:
        traceback.print_exc()
        accaunts[message.from_user.id] = {'email': accaunts[message.from_user.id]['email'],
                                          'password': accaunts[message.from_user.id]['password'],
                                          'ip1': accaunts[message.from_user.id]['ip1'],
                                          'login1': accaunts[message.from_user.id]['login1'], 'pas1': pas}
        msg = bot.send_message(message.from_user.id, f'Введите ip', reply_markup=exit)
        bot.register_next_step_handler(msg, step_ip)
def step_login(message):
    exit = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Основное меню", callback_data='exit')
    exit.add(btn1)
    login = message.text
    try:
        test = accaunts[message.from_user.id]['ip2']
        accaunts[message.from_user.id] = {'email': accaunts[message.from_user.id]['email'],
                                          'password': accaunts[message.from_user.id]['password'],
                                          'ip1': accaunts[message.from_user.id]['ip1'],
                                          'login1': accaunts[message.from_user.id]['login1'],
                                          'pas1': accaunts[message.from_user.id]['pas1'],
                                          'ip2': accaunts[message.from_user.id]['ip2'], 'login2': login}
    except KeyError:
        accaunts[message.from_user.id] = {'email': accaunts[message.from_user.id]['email'],
                                          'password': accaunts[message.from_user.id]['password'],
                                          'ip1': accaunts[message.from_user.id]['ip1'], 'login1': login}
    msg = bot.send_message(message.from_user.id, f'Введите пароль', reply_markup=exit)
    bot.register_next_step_handler(msg, step_pas)
def step_ip(message):
    exit = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Основное меню", callback_data='exit')
    exit.add(btn1)
    ip = message.text
    bot.send_message(message.from_user.id, f'{ip} проверяется, ожидайте 7 секунд', reply_markup=exit)
    r = cheack(ip)
    if r == False:
        msg = bot.send_message(message.from_user.id, f'{ip} не работает, попробуйте снова', reply_markup=exit)
        return bot.register_next_step_handler(msg, step_ip)
    records = cur.execute("SELECT * FROM servers")
    all_orders = cur.fetchall()
    for order in all_orders:
        if order[3] == ip and order[-4] == 'good':
            msg = bot.send_message(message.from_user.id, f'Такой ip уже записан. Введите новый', reply_markup=exit)
            return bot.register_next_step_handler(msg, step_ip)
    try:
        test =accaunts[message.from_user.id]['ip1']
        if ip == test:
            msg = bot.send_message(message.from_user.id, f'Такой ip уже записан. Введите новый', reply_markup=exit)
            return bot.register_next_step_handler(msg, step_ip)
        accaunts[message.from_user.id] = {'email': accaunts[message.from_user.id]['email'],
                                          'password': accaunts[message.from_user.id]['password'],
                                          'ip1': accaunts[message.from_user.id]['ip1'],
                                          'login1': accaunts[message.from_user.id]['login1'],
                                          'pas1': accaunts[message.from_user.id]['pas1'], 'ip2': ip}
    except KeyError:
        accaunts[message.from_user.id] = {'email': accaunts[message.from_user.id]['email'],
                                          'password': accaunts[message.from_user.id]['password'], 'ip1': ip}
    msg = bot.send_message(message.from_user.id, f'Введите логин', reply_markup=exit)
    bot.register_next_step_handler(msg, step_login)
def step_password(message):
    exit = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Основное меню", callback_data='exit')
    exit.add(btn1)
    password = message.text
    accaunts[message.from_user.id] = {'email': accaunts[message.from_user.id]['email'],'password': password}
    msg = bot.send_message(message.from_user.id, f'Введите ip', reply_markup=exit)
    bot.register_next_step_handler(msg, step_ip)
def step_email(message):
    exit = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Основное меню", callback_data='exit')
    exit.add(btn1)
    email = message.text
    records = cur.execute("SELECT * FROM servers")
    all_orders = cur.fetchall()
    for order in all_orders:
        if order[1] == email:
            msg = bot.send_message(message.from_user.id, 'Почта уже использована.Введите другую почту')
            return bot.register_next_step_handler(msg, step_email)
    accaunts[message.from_user.id] = {'email':email}
    msg = bot.send_message(message.from_user.id,f'Введите пароль',reply_markup=exit)
    bot.register_next_step_handler(msg, step_password)
def step_error(message):
    exit = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Основное меню", callback_data='exit')
    exit.add(btn1)
    all_orders = cur.fetchall()
    for order in all_orders:
        if order[1] == message.text:
            sqlite_update_query = """Update servers set status = ? where email = ?"""
            cur.executemany(sqlite_update_query, [('good', message.text)])
            conn.commit()
            bot.send_message(message.from_user.id, f'{message.text} успешно восстановлен', reply_markup=exit)
            break
    bot.send_message(message.from_user.id, f'{message.text} почта не найдена', reply_markup=exit)
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    exit = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Основное меню", callback_data='exit')
    exit.add(btn1)
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Добавить аккаунт", callback_data='add_ac')
    btn2 = types.InlineKeyboardButton("Сколько машин я сделал", callback_data='statistic')
    btn3 = types.InlineKeyboardButton("Удалить аккант", callback_data='del')
    btn4 = types.InlineKeyboardButton("Починить аккаунт", callback_data='error')
    markup.add(btn1, btn3)
    markup.add(btn4, btn2)
    try:
        if call.data == 'add_ac':
            msg = bot.send_message(call.from_user.id,'введите почту')
            bot.register_next_step_handler(msg, step_email)
        elif call.data == 'exit':
            bot.send_message(call.from_user.id, 'Ебать функциОнал',reply_markup=markup)
        elif call.data == 'statistic':
            records = cur.execute("SELECT * FROM servers")
            all_orders = cur.fetchall()
            x = 0
            y = 0
            z = 0
            w = 0
            for order in all_orders:
                if order[0] != call.from_user.id:
                    continue
                if order[-4] == 'good':
                    x += 1
                if order[-3] == 'new':
                    y += 1
                if order[-4] == 'hz':
                    z += 1
                    bot.send_message(call.from_user.id,
                                     f'Проверьте аккаунт {order[1]}|{order[2]} сервер {order[3]} не даёт ответ')
                if order[-4] == 'die':
                    w += 1
            bot.send_message(call.from_user.id, f'Живых {x} Новых {y} Ошибок {z} Мёртвых {w}',reply_markup=exit)
        elif call.data == 'del':
            msg = bot.send_message(call.from_user.id, f'Введите почту аккаунта')
            bot.register_next_step_handler(msg, step_del)
        elif call.data == 'error':
            msg = bot.send_message(call.from_user.id, f'Введите почту аккаунта')
            bot.register_next_step_handler(msg, step_error)
    except Exception as e:
        print(e)
        bot.send_message(call.from_user.id, f'❌ Ошибка, проверьте правильность написанния')
while True:
    try:
        bot.polling(none_stop=True, interval=0,timeout=25)
    except Exception as e:
        bot.send_message(1845957426,str(e))
