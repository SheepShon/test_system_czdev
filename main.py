import eel
import sqlite3
import time

eel.init("web")

db = sqlite3.connect("database.db")
sql = db.cursor()

app_version = "czt_v0.2.3_alpha"

user_id = 0
user_info = {}
test_id = 0
questions = []

sql.execute("""CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    badge TEXT,
    second_name TEXT,
    first_name TEXT,
    thrid_name TEXT,
    permissions INT,
    rang TEXT,
    position TEXT,
    sex TEXT,
    birth_date TEXT,
    faculty TEXT,
    department TEXT,
    password TEXT,
    f_status TEXT,
    avatar_path TEXT,
    vd_path TEXT
)""")
db.commit()

sql.execute("""CREATE TABLE IF NOT EXISTS themes (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT,
    author_id INT
)""")
db.commit()

sql.execute("""CREATE TABLE IF NOT EXISTS tests (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT,
    time INT,
    theme_id INT,
    author_id INT,
    img TEXT
)""")
db.commit()

sql.execute("""CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    test_id INT,
    name TEXT,
    answer INT,
    theme_id INT,
    author_id INT
)""")
db.commit()

sql.execute("""CREATE TABLE IF NOT EXISTS variants (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT,
    test_id INT,
    question_id INT,
    author_id INT
)""")
db.commit()

# sql.execute(f"INSERT INTO users VALUES (1, 'test_badge', 'second_test', 'first_test', 'thrid_test', 1, 'test_rang', 'test_position', 'test_sex', 'test_birth_date', 'test_faculty', 'test_department', 'test_spec_code', 'test_course', 'test_password', 'test_f_status', 'test_avatar_path', 'test_vd_path')")
# db.commit()

@eel.expose
def get_app_version():
    eel.upd_app_version(app_version)

@eel.expose
def check_user(user_login, user_password):
    global user_id, user_info
    print(f"def check_user ({user_login},{user_password})")
    sql.execute(f"SELECT badge FROM users WHERE badge = '{user_login}'")

    if sql.fetchone() is None:
        print("err: account not exists")
        eel.change_mes_color(0)
        eel.py_send_msg("Аккаунт не найден")
    else:
        sql.execute(f"SELECT * FROM users WHERE badge = '{user_login}'")
        db.commit()
        user_info = sql.fetchone()
        if user_password == user_info[12]:
            user_id = user_info[0]
            eel.py_redirect("main.html")
            eel.change_mes_color(1)
            eel.py_send_msg("Успешная авторизация")
            print(f"redirect to main.html, load user_id = {user_id}")
        else:
            eel.change_mes_color(0)
            eel.py_send_msg("Жетон или пароль указаны не верно")

@eel.expose
def upd_data_main():
    eel.py_send_data("user_info_second_name", user_info[2])
    eel.py_send_data("user_info_first_name", user_info[3])
    eel.py_send_data("user_info_third_name", user_info[4])
    eel.py_send_data("user_info_badge", user_info[1])
    eel.py_send_data("user_info_position", user_info[7])
    eel.py_send_data("user_info_rang", user_info[6])
    eel.py_send_data("user_info_faculty", user_info[10])
    eel.py_send_data("user_info_department", user_info[11])
    eel.send_permission(user_info[5])

@eel.expose
def upd_data_test():
    eel.py_send_data("user_info_second_name", user_info[2])
    eel.py_send_data("user_info_first_name", user_info[3])
    eel.py_send_data("user_info_third_name", user_info[4])
    eel.py_send_data("user_info_position", user_info[7])
    eel.py_send_data("user_info_rang", user_info[6]) 

    sql.execute(f"SELECT COUNT(*) FROM questions WHERE test_id={test_id}")
    res = sql.fetchone()
    eel.py_send_data("questions_progress_vsego", res[0])

@eel.expose
def upd_end_data_test():
    sql.execute(f"SELECT * FROM tests WHERE id={test_id}")
    res = sql.fetchone()
    print(res)
    eel.py_send_data("end_test_name", res[1])

@eel.expose
def get_test_id():
    eel.set_test_id(test_id)


@eel.expose
def py_get_right_answer(question_id):
    sql.execute(f"SELECT answer FROM questions WHERE id={question_id}")
    res = sql.fetchone()
    eel.get_right_answer(res[0])


@eel.expose
def upd_test_question(test_id, question_id):
    print(f"upd test id: {test_id}, question_id: {question_id}")
    sql.execute(f"SELECT * FROM questions WHERE test_id={test_id}")
    res = sql.fetchall()

    eel.upd_question_text(res[question_id-1][2]) # Обновить текст вопроса

    db_question_id = res[question_id-1][0]
    eel.set_db_question_id(db_question_id)

     
    sql.execute(f"SELECT DISTINCT question_id FROM variants WHERE test_id = {test_id}") # Получить уникальные ID вопросов
    res = sql.fetchall()

    for i in range(0, len(res)):
        questions.insert(i, res[i][0])

    qid = questions[question_id-1]
    sql.execute(f"SELECT COUNT(*) FROM variants WHERE test_id = {test_id} AND question_id = {qid}")
    cnt = sql.fetchone()

    for i in range(0, cnt[0]):
        qid = questions[question_id-1]
        sql.execute(f"SELECT * FROM variants WHERE test_id = {test_id} AND question_id = {qid}")
        qve = sql.fetchall()
        eel.add_answer_test(qve[i][0], qve[i][1])
    
@eel.expose
def crt_themes():
    sql.execute(f"SELECT COUNT(*) FROM themes")
    req = sql.fetchone()
    count = int(req[0])
    print(f"loaded themes: {count}")

    for i in range(1,count+1):
        sql.execute(f"SELECT name FROM themes WHERE id={i}")
        eel.create_theme(i, sql.fetchone())
    
@eel.expose
def crt_tests():
    sql.execute(f"SELECT COUNT(*) FROM tests")
    req = sql.fetchone()
    count = int(req[0])
    print(f"loaded tests: {count}")

    for i in range(1,count+1):
        sql.execute(f"SELECT * FROM tests WHERE id={i}")
        res = sql.fetchone()
        sql.execute(f"SELECT COUNT(*) FROM questions WHERE test_id={i}")
        res_2 = sql.fetchone()
        eel.create_test(res[3], res[1], res[2], res_2[0], i)

@eel.expose
def load_test(id):
    global test_id
    test_id = id
    print(f"redirect to test.html, load test_id = {test_id}")
    eel.py_redirect("test.html")

@eel.expose
def register_user(second_name, first_name, thrid_name, sex, birth_date, f_status, badge, position, rang, faculty, department, password, avatar_path, vd_path):
    sql.execute(f"SELECT badge FROM users WHERE badge = '{badge}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO users (badge, second_name, first_name, thrid_name, permissions, rang, position, sex, birth_date, faculty, department, password, f_status, avatar_path, vd_path) VALUES ('{badge}', '{second_name}', '{first_name}', '{thrid_name}', 1, '{rang}', '{position}', '{sex}', '{birth_date}', '{faculty}', '{department}', '{password}', '{f_status}', '{avatar_path}', '{vd_path}')")
        db.commit()
        eel.load_auth_layout()
        eel.change_mes_color(1)
        eel.py_send_msg("Аккаунт успешно зарегистрирован")
    else:
        eel.change_mes_color(0)
        eel.py_send_msg("Аккаунт с таким жетоном уже зарегистрирован")

eel.start("index.html", size=(1017,639))