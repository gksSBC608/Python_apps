import sqlite3

class SqliteUtil:

    conn = None
    def initiate_db(self):
        self.conn = sqlite3.connect('test.db')
        print("Opened database successfully")

    def create_table(self):
        self.conn.execute('''CREATE TABLE COMPANY
         (ID INT PRIMARY KEY     NOT NULL,
         NAME           TEXT    NOT NULL,
         KEY            TEXT     NOT NULL
         );''')
        print("Table created successfully")

    def insert_data(self,id_v,username,key):
        sql = '''INSERT INTO COMPANY (ID,NAME,KEY) \
        VALUES ('''+str(id_v)+''', "'''+username+'''", "'''+key+'''" )'''
        print(sql)
        self.conn.execute(sql)
        self.conn.commit()
        print("Data inserted successfully")
        #self.conn.close()

    def retrieve_data(self):
        cursor = self.conn.execute("SELECT id, name, key from COMPANY")
        for row in cursor:
            print("ID:"+str(row[0]))
            print(" Name:"+row[1])
            print(" Key:"+row[2]+"\n")

    def count_records(self):
        cursor = self.conn.execute("SELECT count(*) key from COMPANY")
        for row in cursor:
            print("No of records : "+str(row[0]))

    def update_data(self,name,key):
         sql = "UPDATE COMPANY set key = "+key+" where name ="+name
         self.conn.execute(sql)
         self.conn.commit();
         print("Updated data for name "+name)

    def delete_data(self,name):
        sql = "DELETE from COMPANY where name = '"+name+"''"
        self.conn.execute(sql)
        self.conn.commit();
        print("Deleted data for name "+name)

    def delete_data(self,id):
         sql = "DELETE from COMPANY where id = "+str(id)
         self.conn.execute(sql)
         self.conn.commit();
         print("Deleted data for id "+str(id))

    def close_connection(self):
        self.conn.close()


s = SqliteUtil()
s.initiate_db()
#s.create_table()
#s.insert_data(12,'ankur1','123qsdf456')
#s.insert_data(13,'gaurav1','1234sdf456')
s.initiate_db()
s.retrieve_data()
#s.close_connection()
s.count_records()
s.delete_data(10)
s.count_records()
s.delete_data('ankur')
s.count_records()

    
        
