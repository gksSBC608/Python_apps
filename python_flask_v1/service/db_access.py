from .db_util import DBConnect
import logging

class DBAccess():
    def validate_login(self, username, password):
        """
        Method to validate if user is valid; if his credentials exist in DB-
        True is returnrd, else False
        """
        result = False
        try:
            conn = DBConnect.getConnection()
        except Exception as e:
            logging.error("Connection Error in validating login ->" + str(e))
            print("Connection Error in validating login ->", e)
            return False
        try:
            #print(conn)
            cursor = conn.cursor()
            sql = "select username,password from users where username='"+username+"' and password ='"+password+"'";
            cursor.execute(sql)
            rows = cursor.fetchall()
            print(str(rows))
            recs_num = cursor.rowcount
            print('Total Row(s):', recs_num)
            logging.info("login SQL query fetched "+str(recs_num)+" records")
            if(1 <= recs_num):
                logging.info("login successful")
                result=True
            else:
                result= False
        except Exception as e:
            logging.error("Database error in validating login, " + str(e))
            print("Database error in validating login, " + str(e))
            result = False
        finally:
            conn.close()
            # print("Result is :",result)
        return result

    def fetch_account_detail(self,username):
        sql = "select firstname,lastname,account_number,account_balance,bank_name from users,accounts where users.user_id = accounts.user_id and users.username='"+username+"'"
        logging.debug("SQL query to fetch account detail is ->"+sql)
        try:
          conn = DBConnect.getConnection()      
        except Exception as e:
          print ("Connection Error ->", e)
          logging.error("Connection Error in fetching acc dtail, ->"+str(e))
          return False
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            #print(str(rows))
            for record in rows:
                print(record)
            for firstname, lastname,account_no, account_balance,bankname in rows:
                print(firstname+" "+lastname+" "+str(account_no)+" "+str(account_balance)+" "+bankname)
        except Exception as e:
          print ("Database Error ->", e)
          logging.error("Database error in fetching acc detail, "+str(e))
        finally:
          conn.close()
        return record

    def get_userid_by_username(self,username):
        try:
          conn = DBConnect.getConnection()
        except Exception as e:
          logging.error("Database error while getting userid by username, "+str(e))
          print ("Connection Error ->", e)
	
        sql = "select user_id from users where username='"+username+"'"  
        #print(sql)	
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            #print(str(rows))
            for (user_i) in rows:
                #print(user_i)
                user_id = user_i[0];
            print("user_id for username, "+username+" is "+user_id)
            logging.debug("user_id for username, "+username+" is "+user_id)
        except Exception as e:
          logging.error("Database error while getting user id by username, "+str(e))
          print("Database Error ->",e)
        return user_id

    def add_payee(self,payee):
        """
        This method adds a new payee as per account number, name and bank provided in UI
        """
        result = False
        payee_acc_no = payee[0]
        payee_acc_name = payee[1]
        payee_acc_bank = payee[2]
        user_id = payee[3]
        payee_name_arr = payee_acc_name.split(' ')
        firstname = payee_name_arr[0]
        lastname = payee_name_arr[1]
        try:
            conn = DBConnect.getConnection()
        except Exception as e:
          print ("Connection Error ->", e)
          logging.error("Error in db connection while adding payee ->"+str(e))
          return False

        username = firstname.lower()
        password = "password"
        print(username+" "+password)
        print(firstname+" "+lastname)
        print("payee data to be added:-> "+str(payee_acc_no)+" "+str(payee_acc_name)+" "+str(payee_acc_bank))
        sql_add_user = "insert into users values(null,'"+username+"','"+password+"','"+firstname+"','"+lastname+"')"
        print(sql_add_user)
        beneficiary_user_id =0
        try:
             cursor = conn.cursor()
             cursor.execute(sql_add_user)
             print(str(cursor))
             conn.commit()
             if(cursor.lastrowid):
                 print('last insert id', cursor.lastrowid)
                 beneficiary_user_id =cursor.lastrowid
             else:
                 print('last insert id not found')
             #return True
        except Exception as e:
             print("Database Error while adding user ->",e)
             logging.error("Database Error while adding user to add new payee->",+str(e))
             return False
        try:
            sql_add_account = "insert into accounts values("+str(payee_acc_no)+",1000.0,'"+payee_acc_bank+"',"+str(beneficiary_user_id)+")"
            print(sql_add_account)
            cursor.execute(sql_add_account)
            conn.commit()
        except Exception as e1:
            print("Database Error while adding account ->",e1)
            logging.error("Database Error while adding accout for adding a new payee ->",+str(e1))
            return False
        try:
            sql_add_payee = "insert into beneficiaries values(null,'"+payee_acc_name+"',"+str(payee_acc_no)+","+str(beneficiary_user_id)+","+str(user_id)+")"
            logging.debug("Query to add payee "+sql_add_payee)
            print("Query to add payee "+sql_add_payee)
            cursor.execute(sql_add_payee)
            conn.commit()
            payee_id = cursor.lastrowid
            logging.info("Payee added with ID "+str(payee_id))
            print("Payee added with ID "+str(payee_id))
            result = True
        except Exception as e1:
            print("Database Error while adding beneficiary ->",e1)
            logging.error("Database Error while adding payee to beneficiaries table ->",+str(e))
            return False
        return result

    def register_user(self,user_profile):
        """
        This method registers a new user based on data supplied in the UI
        """
        #user_profile = (firstname,lastname,bankname,username,password,account_number)
        result = False
        firstname = user_profile[0]
        lastname = user_profile[1]
        bankname = user_profile[2]
        username = user_profile[3]
        password = user_profile[4]
        account_number = user_profile[5]
        #print(firstname,lastname,bankname,username,password,account_number,sep=',')
        #sql = "insert into users values(null,'gaurav','gaurav','Gaurav','Sharan')"
        sql_add_user = "insert into users values(null,'"+username+"','"+password+"','"+firstname+"','"+lastname+"')"
        logging.info("Query to insert into users ->"+sql_add_user)
        print("Query to insert into users ->"+sql_add_user)
        try:
          conn = DBConnect.getConnection()
      
        except Exception as e:
          print ("Connection Error ->", e)
          logging.error("Connection Error while register user ->"+str(e))
          return False
        try:
            cursor = conn.cursor()
            cursor.execute(sql_add_user)
            print(str(cursor))
            conn.commit()
            new_id = cursor.lastrowid
            print("id generated is =>",new_id)
            sql_acc = "insert into accounts values("+str(account_number)+",1000.0,'"+bankname+"',"+str(new_id)+")"
            logging.debug("Query to insert into accounts ->"+sql_acc)
            print("Query to insert into accounts ->"+sql_acc)
            cursor.execute(sql_acc)
            conn.commit()
            result = True
        except Exception as e:
          print("Database error =>",e)
          logging.error("Database error while registering a new user, "+str(e))
          result = False
        finally:
          conn.close()      
        return result

    def account_detail(self,username):
        try:
          conn = DBConnect.getConnection()
      
        except Exception as e:
          print ("Connection Error ->", e)
          logging.error("Error while getting account detail ->"+str(e))
          return False
        sql_get_acc_detail = "select a.account_number,a.account_balance from accounts a, users u where a.user_id=u.user_id and u.username='"+username+"'"
        try:
            cursor = conn.cursor()
            cursor.execute(sql_get_acc_detail)
            rows = cursor.fetchall()
            for record in rows:
                print(record)
        except Exception as e:
            print("Database error =>",e)
            logging.error("Database error in getting account detail, "+str(e))
            return False
        return record

    def check_benficiary(self,username,payee_acc_no):
        try:
          conn = DBConnect.getConnection()
        except Exception as e:
          print ("Connection Error ->", e)
          logging.error("Error while db connection while checking a beneficiary ->"+str(e))
        #sql = "SELECT count(*) as rec_count FROM beneficiaries b where user_id="+user_id+" and beneficiary_ac_no ="+payee_acc_no
        sql = "select count(*) as rec_count from beneficiaries b, users u where b.beneficiary_ac_no="+str(payee_acc_no)+" and  b.user_id=u.user_id and u.username='"+username+"'"
        print(sql)
        result = False
        count = 0
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            for record in rows:
                print(record)
                count = int(record[0])
        except Exception as e:
            print("Database error =>",e)
            logging.error("Database error in checking beneficiary, "+str(e))
            return False
        if(count>0):
            print("Payee account number exists")
            return True
        else:
            print("Payee account number doesn't exist")
            return False

    def get_payee_accounts(self,username):
        """
        This method fetches the account number of all payees to poplulate in payee list in order to enable money transfer
        """
        try:
          conn = DBConnect.getConnection()
      
        except Exception as e:
          print ("Connection Error ->", e)
          logging.error("Error in db connection while getting payee accounts ->"+str(e))
        sql = "select beneficiary_ac_no from users u,beneficiaries b where u.user_id=b.user_id and u.username='"+username+"'"
        logging.info("SQL query to get beneficiary account number from username, "+sql)
        #print("Query to fetch all beneficiary accounts of user: "+username+" ",sql)
        try:
          accounts = ()
          index = 0
          accounts = list(accounts)
          cursor = conn.cursor()
          cursor.execute(sql)
          rows = cursor.fetchall()
          for record in rows:
              #print(record[0])
              accounts.insert(index,int(record[0]))
              index += 1
        except Exception as e:
            print("Database error =>",e)
            logging.error("Database error in getting payee accounts, "+str(e))
        return accounts

    def get_payee_data(self,payee_acc_number):
        """
        This method fetches detail of a payee in order to populate in remove payee page
        """
        try:
          conn = DBConnect.getConnection()
      
        except Exception as e:
          print ("Connection Error ->", e)
          logging.error("Error in db connection while getting payee data ->"+str(e))
          

        sql = "select b.beneficiary_name ,a.bank_name from beneficiaries b,accounts a where b.beneficiary_ac_no = a.account_number and b.beneficiary_ac_no="+str(payee_acc_number)
        print(sql)
        try:
          cursor = conn.cursor()
          cursor.execute(sql)
          rows = cursor.fetchall()
          #rec = ()
          result = ()
          index = 0
          result = list(result)
          for record in rows:
              #print(record)
              result.insert(index,record[index])
              index += 1
              result.insert(index,record[index])
          print(result)            
        except Exception as e:
          print("Database Error ->",e)
          logging.error("Database error in getting payee data, "+str(e))
          return False
        return result

    def remove_payee(self,payee):
        """
        This method receives payee information and remobes it from database
        """
        payee_acc_no = payee[0]
        payee_acc_name = payee[1]
        payee_acc_bank = payee[2]
        result = False
        try:
          conn = DBConnect.getConnection()
      
        except Exception as e:
          print ("Connection Error ->", str(e))
          logging.error("Error while db connection while removing payee "+payee_acc_name+" ->"+str(e))

        sql = "delete from beneficiaries where beneficiary_ac_no="+str(payee_acc_no)+" and beneficiary_ac_no in (select account_number from accounts where bank_name='"+payee_acc_bank+"')"
        #print(sql)
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            #print(str(cursor))
            conn.commit()
            result=True
        except Exception as e:
            print("Database Error ->",e)
            logging.error("Database error in removing a payee, "+str(e))
            result = False
        finally:
            conn.close()
        return result

    def check_if_user_registered(self,username):
        result=False
        try:
          conn = DBConnect.getConnection()
      
        except Exception as e:
          print ("Connection Error ->", e)
          logging.error("Error while db connection while checking if user is registered ->"+str(e))

        sql = "select * from users where username='"+username+"'"
        logging.debug("Query to check if user exists:->"+sql)
        print("Query to check if user exists:->"+sql)
        try:
          cursor = conn.cursor()
          cursor.execute(sql)
          rows = cursor.fetchall()
          recs_num = cursor.rowcount
          print("No of rows fetched: "+str(recs_num))
          if(1 <= recs_num):
            result=True
          else:
            result= False
        except Exception as e:
          print("Database Error ->",e)
          logging.error("Error while checking if user is registered->"+str(e))
          result = False
        finally:
          conn.close()
        return result

    def reset_password(self,username,password):
        """
        Method to reset password, database is updated with the new data supplied to this method
        """
        result = False
        try:
          conn = DBConnect.getConnection()
      
        except Exception as e:
          print ("Connection Error ->", e)
          logging.error("Connection Error ->"+str(e))

        try:
          sql = "update users set password='"+password+"' where username='"+username+"'"
          logging.debug("SQL query to reset password -> "+sql)
          cursor = conn.cursor()
          cursor.execute(sql)
          #print(str(cursor))
          conn.commit()
          result=True
        except Exception as e:
          print ("Database Error ->", e)
          logging.error("Database error while reset password, "+str(e))
          result = False
        finally:
          conn.close()
        return result
    
    def deposit_money(self,username,acc_number,amount):
        result=False
        try:
          conn = DBConnect.getConnection()
          logging.info("Connection established")
        except Exception as e:
          print ("Connection Error ->", e)
          logging.error("Database conn error while fdepositing money->",str(e))

        sql = "update accounts set account_balance=account_balance+"+str(amount)+" where account_number="+str(acc_number)+ " and user_id in (select user_id from users where username='"+username+"')"
        logging.debug("SQL query to update user account while depositing money :="+sql)
        try:
          cursor = conn.cursor()
          cursor.execute(sql)
          #print(str(cursor))
          conn.commit()
          result=True
        except Exception as e:
          print("Database Error ->",e)
          logging.error("Error while depositing money -> "+str(e))
        finally:
          conn.close()
        return result

    def fetch_account_balance(self,acc_number):
        """
        Method to fetch account balance for given account number
        """
        sql = "select account_balance from accounts where account_number="+str(acc_number)
        #print(sql)
        try:
          conn = DBConnect.getConnection()
      
        except Exception as e:
          print ("Connection Error ->", e)
          logging.error("Connection Error ->"+str(e))

        try:
          cursor = conn.cursor()
          cursor.execute(sql)
          rows = cursor.fetchall()
          recs_num = cursor.rowcount
          logging.debug("Number of elements in the record is:"+str(recs_num))
          balance = 0.0
          for record in rows:
            balance = float(record[0])
            print(type(balance))
            print(balance) 
                 
        except Exception as e:
          print ("Database Error ->", e)
          logging.error("Error while fetching account balance->"+str(e))
        return balance

    def deduct_balance(self,acc_number,username,amount):
        """
        This method deducts balance from the account of one who is sending money
        """
        result =False
        try:
          conn = DBConnect.getConnection()
      
        except Exception as e:
          print ("Connection Error ->", e)
          logging.error("Connection Error ->"+str(e))
        sql = "update accounts set account_balance = account_balance-"+str(amount)+" where account_number="+str(acc_number)+" and user_id in (select user_id from users where username='"+username+"')"
        logging.debug("SQL query to deduct balance -> "+sql)
        try:
          cursor = conn.cursor()
          cursor.execute(sql)
          #print(str(cursor))
          conn.commit()
          result=True
        except Exception as e:
          print("Error while deducting balance ->"+str(e))
          logging.error("Error while deducting balance->"+str(e))
          result = False
        finally:
          conn.close()
        return result
    
    def add_balance(self,payee_acc_number,payee_acc_bank,amount):
        """
        This method adds balance to the account of payee in course of money transfer. 
        """
        result = False
        sql = "update accounts set account_balance = account_balance+"+str(amount)+" where account_number="+str(payee_acc_number)+" and bank_name='"+payee_acc_bank+"'"
        logging.debug("SQL query to add balance -> "+sql)
        try:
          conn = DBConnect.getConnection()
      
        except Exception as e:
          print ("Connection Error ->", e)
        try:
          cursor = conn.cursor()
          cursor.execute(sql)
          #print(str(cursor))
          conn.commit()
          result=True
        except Exception as e:
          print("Database Error ->",e)
          logging.error("Database Error ->",str(e))
        finally:
          conn.close()
        return result

    def transfer_money(self,money_transfer_data):
        """
        This method fetches two account detail and transfers money between the two
        """
        result =False
        #print("required detail to transfer money is,",str(money_transfer_data))
        acc_number= money_transfer_data[0]
        username= money_transfer_data[1]
        payee_acc_number = money_transfer_data[2]
        payee_acc_name=money_transfer_data[3]
        payee_acc_bank = money_transfer_data[4]
        amount_to_transfer = money_transfer_data[5]
        balance_deducted = self.deduct_balance(acc_number,username,amount_to_transfer)
        logging.debug("Balance transfer initiated at dao level")
        if(balance_deducted):
          logging.debug("Blance deducted from debit account")
          result = self.add_balance(payee_acc_number,payee_acc_bank,amount_to_transfer)
          logging.debug("Blance credited to credit account")
        return result

#dba = DbAccess()
#isvalid = dba.validateLogin("admin","admin")
#print(isvalid)
