import sqlite3
import cryptocode
def get_info():
    username=input('Please enter your username: ')
    username=username.lower()
    password=input('Please enter your password: ')
    print('original password is: ',password)
    tfa_key=input('Please enter your 2fa key: ')
    global crypt
    crypt=input('Please Set a decription phrase\nThis will be used to unlock the databse and will be needed to be entered in the GetVideoData Script\n')
    global data
    data=[cryptocode.encrypt(username,crypt),cryptocode.encrypt(password,crypt),cryptocode.encrypt(tfa_key,crypt)]
    for d in data:
        print(d)
def create_user_db():
    conn = None
    try:
        conn =sqlite3.connect('users.db')
        print(sqlite3.version)
        c = conn.cursor()
    except Error as e:
        print(e)
    try:
        c.execute("CREATE TABLE IF NOT EXISTS User([id] INTEGER PRIMARY KEY,[username] BLOB UNIQUE NOT NULL,[password] BLOB UNIQUE NOT NULL,[tfa_key] BLOB UNIQUE)")
        print('User database created successfully')
    except conn.Error as e:
        print(e)
        print("errored here")
    try:
        sql = ''' INSERT INTO User(username,password,tfa_key)
        VALUES(?,?,?) '''
        c.execute(sql, data)
        conn.commit()
        print('User Created')
    except conn.Error as e:
        print(e)
            
if __name__=="__main__":
    get_info()
    create_user_db()
