import eel
import sqlite3

eel.init("web")

db = sqlite3.connect("database.db")
sql = db.cursor()

user_id = 0

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
    spec_code TEXT,
    course INT,
    password TEXT,
    f_status TEXT,
    avatar_path TEXT,
    vd_path TEXT
)""")

db.commit()

# sql.execute(f"INSERT INTO users VALUES (1, 'test_badge', 'second_test', 'first_test', 'thrid_test', 1, 'test_rang', 'test_position', 'test_sex', 'test_birth_date', 'test_faculty', 'test_department', 'test_spec_code', 'test_course', 'test_password', 'test_f_status', 'test_avatar_path', 'test_vd_path')")
# db.commit()

@eel.expose

def check_user(user_login, user_password):
    print(f"def check_user ({user_login},{user_password})")
    sql.execute(f"SELECT badge FROM users WHERE badge = '{user_login}'")

    if sql.fetchone() is None:
        print("err: account not exists")
        eel.py_send_msg("Аккаунт не найден.")
    else:
        print("redirect to main.html")
        sql.execute(f"SELECT * FROM users WHERE badge = '{user_login}'")
        db.commit()
        user_info = sql.fetchone()
        print(user_info['second_name'])
        eel.py_redirect("main.html")

def recv_data_reg_account(user_login="None", user_password="None"):
    sql.execute(f"SELECT badge FROM users WHERE badge = '{user_login}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO users VALUES ('1','second_test', 'first_test', 'thrid_test', 1, 'test_rang', 'test_position', 'test_sex', 'test_birth_date', 'test_faculty', 'test_department', 'test_spec_code', 'test_course', 'test_password', 'test_f_status', 'test_avatar_path', 'test_')")
        db.commit()
        
        print("Аккаунт зарегистрирован!")
    else:
        print("Такая запись уже имеется!")

eel.start("index.html", size=(1017,639))