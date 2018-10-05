import mysql.connector
import sys,logging


class DBConnect():
    'Common class to get connection object to connect with mysql'

    @staticmethod
    def getConnection():
        """Common method to establish DB connection and reuse it
        """
        try:
            conn = mysql.connector.connect(user='sqluser1', password='Mind@1234$',
                              host='db_url',
                              database='db_password')
            print ("Connection Established\n")
            #logging.info("Connection Established")
            
            return conn
        except Exception as e:
             logging.error("Connection Error ->"+str(e))

#dbconfig = DBConnect()
#conn = DBConnect.getConnection()
#print(conn)
