import pymysql
import creds

def get_conn():
    conn = pymysql.connect(
        host= creds.host,
        user= creds.user,
        password = creds.password,
        db=creds.db,
    )
    return conn