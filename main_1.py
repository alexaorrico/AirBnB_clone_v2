#!/usr/bin/python3
"""Testing file
"""
import hashlib
import MySQLdb
import sys
from models.user import User


if __name__ == "__main__":
    """ Access to database and get password TODO
    """
    user_email = "b@b.com"
    clear_pwd = "pwdB"
    hidden_pwd = hashlib.md5(clear_pwd.encode()).hexdigest()
    '''
    user = User({"email": user_email, "password": clear_pwd, "first_name": "fart", "last_name": "Knocker", "created_at": "2017-03-25 02:17:06", "updated_at": "2017-03-25 02:17:06"})
    user.save()
    '''

    conn = MySQLdb.connect(host="localhost", port=3306, user=sys.argv[1], passwd=sys.argv[2], db=sys.argv[3], charset="utf8")
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE email = '{}' LIMIT 1".format(user_email))
    query_rows = cur.fetchall()
    for row in query_rows:
        if hidden_pwd.lower() == row[0].lower():
            print("OK")
    cur.close()
    conn.close()
