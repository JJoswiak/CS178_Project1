import pymysql
import creds

def get_db_connection():
   conn = pymysql.connect(
       host= creds.host,
       user= creds.user,
       password = creds.password,
       db=creds.db,
   )
   return conn