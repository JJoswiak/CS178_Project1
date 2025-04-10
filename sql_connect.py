import sql_connect
import creds

def get_conn():
    conn = sql_connect.get_conn(
        host= creds.host,
        user= creds.user,
        password = creds.password,
        db=creds.db,
    )
    return conn