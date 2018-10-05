import _mysql
import sys,logging


class DBConnect():
    'Common class to get connection object to connect with mysql'

    @staticmethod
    def getConnection():
        """Common method to establish DB connection and reuse it
        """
        try:
            conn = _mysql.connect("localhost", "root", "Welcome123", "banking_tej")
            logging.info(conn)
            logging.info("Connection Established")
            
            return conn
        except Exception as e:
             logging.error("Connection Error ->"+str(e))

#dbconfig = DBConnect()
#conn = DBConnect.getConnection()
#print(conn)
