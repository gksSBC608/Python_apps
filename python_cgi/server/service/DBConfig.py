import _mysql
import sys

class DBConnect():
    'Common class to get connection object to connect with mysql'
    
    @staticmethod
    def getConnection():
        """Common method to establish DB connection and reuse it            
        """
        try:
            conn = _mysql.connect("localhost", "root", "Welcome123", "banking_mindtree")
            #print ("Connection Established\n")
            return conn
        except Exception as e:
            print ("Connection Error ->", e)


#dbconfig = DBConnect()
#DBConnect.getConnection()
         
            
        
