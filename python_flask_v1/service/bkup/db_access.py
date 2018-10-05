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
            logging.error("Connection Error ->" + str(e))
            print("Connection Error ->", e)

        try:
            # print("In db class "+username+" "+password)
            sql = "select username,password from users where username='" + username + "' and password ='" + password + "'";
            logging.debug("SQL query to login ->" + sql)
            conn.query(sql)
            all_recs = conn.store_result()
            logging.info("No of records fetched: "+str(all_recs.num_rows()))
            # print ("Number of Records Retrieved ->", all_recs.num_rows())
            if (1 == all_recs.num_rows()):        
                result = True
            else:
                result = False


        except Exception as e:
            logging.error("Database error, " + str(e))
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
          logging.error("Connection Error ->"+str(e))
      
        try:
          conn.query(sql)
          #print("Query to fetch user profile ->"+sql)
          all_recs = conn.store_result()
          rec = all_recs.fetch_row()
          #print("Number of elements in the record is:",len(rec))
          for firstname, lastname,account_no, account_balance,bank_name in rec:
            fname= str(firstname,'utf-8')
            lname = str(lastname,'utf-8')
            #print(fname,lname,account_no,account_balance,sep='->')
            logging.info("Account detail fetched is:"+str((fname,lname,account_no,account_balance,bank_name)))
          #return (fname,lname,account_no,account_balance,bank_name)
      
        except Exception as e:
          logging.error("Database error, "+str(e))
        finally:
          conn.close()
        return (fname,lname,account_no,account_balance,bank_name)

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
          return False

        username = firstname.lower()
        password = "password"
        sql_add_user = "insert into users values(null,'"+username+"','"+password+"','"+firstname+"','"+lastname+"')"
        logging.debug("Query to add payee user ->"+sql_add_user)
        try:
          conn.query(sql_add_user)
          beneficiary_user_id = conn.insert_id()
          logging.info("User added with ID "+str(beneficiary_user_id))
        except Exception as e:
          print("Database Error while adding user ->",e)
          logging.error("Database Error while adding user ->"+str(e))
          return False
        try:
          sql_add_account = "insert into accounts values("+str(payee_acc_no)+",1000.0,'"+payee_acc_bank+"',"+str(beneficiary_user_id)+")"
          logging.debug("Query to add account is ->"+sql_add_account)
          conn.query(sql_add_account)
          #acc_id = conn.insert_id()
          logging.info("Account added with ID "+str(payee_acc_no))
        except Exception as e:
          print("Database error while adding account =>",e)
          logging.error("Database error while adding account, "+str(e))
          return False
        try:
          sql_add_payee = "insert into beneficiaries values(null,'"+payee_acc_name+"',"+str(payee_acc_no)+","+str(beneficiary_user_id)+","+str(user_id)+")"
          logging.debug("Query to add payee "+sql_add_payee)
          conn.query(sql_add_payee)
          payee_id = conn.insert_id()
          logging.info("Payee added with ID "+str(payee_id))
          result = True
        except Exception as e:
          print("Database error while adding payee =>",e)
          logging.error("Database error while adding payee, "+str(e))
          result = False
        finally:
          conn.close()     
        return result

    def get_userid_by_username(self,username):
        try:
          conn = DBConnect.getConnection()
        except Exception as e:
          logging.error("Database error while adding payee, "+str(e))
          print ("Connection Error ->", e)
	
        sql = "select user_id from users where username='"+username+"'"  
        #print(sql)	
        try:
          conn.query(sql)
          all_recs = conn.store_result()
          rec = all_recs.fetch_row()
          #print("Number of elements in the record is:",len(rec))
          user_id =0
          for user_i in rec:
            #print(str(user_i))
            user_id = int(user_i[0])
        except Exception as e:
          logging.error("Database error while adding payee, "+str(e))
          print("Database Error ->",e)
        return user_id

    def check_benficiary(self,username,payee_acc_no):
        try:
          conn = DBConnect.getConnection()
        except Exception as e:
          print ("Connection Error ->", e)
        #sql = "SELECT count(*) as rec_count FROM beneficiaries b where user_id="+user_id+" and beneficiary_ac_no ="+payee_acc_no
        sql = "select count(*) as rec_count from beneficiaries b, users u where b.beneficiary_ac_no="+payee_acc_no+" and  b.user_id=u.user_id and u.username='"+username+"'"
        #print(sql)
        result = False
        count = 0
        try:
          conn.query(sql)
          all_recs = conn.store_result()
          records = all_recs.fetch_row()
          logging.info("records : "+str(records))
          print("Number of elements in the record is:",len(records))
          for rec in records:
              logging.info("rec as string : "+str(rec)+" "+rec[0])
              print("rec as string : "+str(rec)+" "+rec[0] )
              count = int(rec[0])
          
        except Exception as e:
            logging.error("Database error while checking if beneficiary already exists, "+str(e))
        if(count>0):
            print("Account number exists")
            return True
        else:
            print("Account number doesn't exist")
            return False

    def get_payee_accounts(self,username):
        """
        This method fetches the account number of all payees to poplulate in payee list in order to enable money transfer
        """
        try:
          conn = DBConnect.getConnection()
      
        except Exception as e:
          print ("Connection Error ->", e)
        sql = "select beneficiary_ac_no from users u,beneficiaries b where u.user_id=b.user_id and u.username='"+username+"'"
        logging.info("SQL query to get beneficiary account number from username, "+sql)
        #print("Query to fetch all beneficiary accounts of user: "+username+" ",sql)
        try:
          conn.query(sql)
          all_recs = conn.store_result()
          rec = all_recs.fetch_row()
          #print(type(rec))
          #print(len(rec))
          accounts = ()
          index = 0
          accounts = list(accounts)
          while(rec):
            for id in rec:
              acc_no = id[0]
              #print(acc_no)
              accounts.insert(index,int(acc_no))
              index += 1

            rec = all_recs.fetch_row()
          #accounts = tuple(accounts)
          print(str(accounts))
          return accounts   
    
        except Exception as e:
          print("Database Error->",e)

    def get_payee_data(self,payee_acc_number):
        """
        This method fetches detail of a payee in order to populate in remove payee page
        """
        try:
          conn = DBConnect.getConnection()
      
        except Exception as e:
          print ("Connection Error ->", e)

        sql = "select b.beneficiary_name ,a.bank_name from beneficiaries b,accounts a where b.beneficiary_ac_no = a.account_number and b.beneficiary_ac_no="+payee_acc_number
        #print(sql)
        try:
          conn.query(sql)
          all_recs = conn.store_result()
          rec = all_recs.fetch_row()
          #print(str(rec))
          result = ()
          index = 0
          result = list(result)
          while(rec):
            for ben,bank in rec:
              ben_name = str(ben, 'utf-8')
              bank_name = str(bank, 'utf-8')
              #print(ben_name,bank_name)
              result.insert(index,ben_name)
              index += 1
              result.insert(index,bank_name)
          
            rec = all_recs.fetch_row()
          return result
        except Exception as e:
          print("Database Error ->",e)
        

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
          print ("Connection Error ->", e)

        sql = "delete from beneficiaries where beneficiary_ac_no="+str(payee_acc_no)+" and beneficiary_ac_no in (select account_number from accounts where bank_name='"+payee_acc_bank+"')"
        #print(sql)
        #select beneficiary_name from beneficiaries where beneficiary_ac_no= 9800150005 and beneficiary_ac_no in (select account_number from accounts where bank_name ='HDFC Bank')
        try:
          conn.query(sql)
          result =True
        except Exception as e:
          print("Database Error ->",e)
        finally:
          conn.close()

        return result

    def account_detail(self,username):
        try:
          conn = DBConnect.getConnection()
      
        except Exception as e:
          print ("Connection Error ->", e)

        sql = "select a.account_number,a.account_balance from accounts a, users u where a.user_id=u.user_id and u.username='"+username+"'"
        try:
          conn.query(sql)
          #print("Query to fetch user profile ->"+sql)
          all_recs = conn.store_result()
          rec = all_recs.fetch_row()
          print("Number of elements in the record is:",len(rec))
          logging.info("Number of elements in the record is:",len(rec))
          for account_no, account_balance in rec:
            #print(fname,lname,account_no,account_balance,sep='->')
            logging.info("Account detail fetched is:"+str((account_no,account_balance)))
          #return (fname,lname,account_no,account_balance,bank_name)
      
        except Exception as e:
          logging.error("Database error, "+str(e))
        finally:
          conn.close()
        return (account_no,account_balance)

    def deposit_money(self,username,acc_number,amount):
        result=False
        try:
          conn = DBConnect.getConnection()
          logging.info("Connection established")
        except Exception as e:
          print ("Connection Error ->", e)

        sql = "update accounts set account_balance=account_balance+"+str(amount)+" where account_number="+str(acc_number)+ " and user_id in (select user_id from users where username='"+username+"')"
        logging.info("SQL query to update user account while depositing money :="+sql)
        try:
          conn.query(sql)
          result = True

        except Exception as e:
          print("Database Error ->",e)
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
          conn.query(sql)
          all_recs = conn.store_result()
          rec = all_recs.fetch_row()
          #print("Number of elements in the record is:",len(rec))
          balance = 0.0
          for acc_balance in rec:
            balance = float(acc_balance[0])
            #print(type(balance))
      
          return balance       
        except Exception as e:
          print ("Database Error ->", e)

    def deduct_balance(self,acc_number,username,amount):
        """
        This method deducts balance from the account of one who is sending money
        """
        result =False
        try:
          conn = DBConnect.getConnection()
      
        except Exception as e:
          print ("Connection Error ->", e)
        sql = "update accounts set account_balance = account_balance-"+str(amount)+" where account_number="+str(acc_number)+" and user_id in (select user_id from users where username='"+username+"')"
        logging.debug("SQL query to deduct balance -> "+sql)
        try:
          conn.query(sql)
          result = True
        except Exception as e:
          print("Database Error ->",e)
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
          conn.query(sql)
          result = True
        except Exception as e:
          print("Database Error ->",e)
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
        if(balance_deducted):
          result = self.add_balance(payee_acc_number,payee_acc_bank,amount_to_transfer)
      
        return result

    def check_if_user_registered(self,username):
        result=False
        try:
          conn = DBConnect.getConnection()
      
        except Exception as e:
          print ("Connection Error ->", e)

        sql = "select * from users where username='"+username+"'"
        logging.debug("Query to check if user exists:->"+sql)
        try:
          conn.query(sql)
          all_recs = conn.store_result()
          #print ("Number of Records Retrieved ->", all_recs.num_rows())
          if(1 <= all_recs.num_rows()):
            result=True
          else:
            result= False

        except Exception as e:
          print("Database Error ->",e)
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
          conn.query(sql)
          result = True
        except Exception as e:
          print ("Database Error ->", e)
          logging.error("Database error, "+(e))
          result = False
        finally:
          conn.close()
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
        sql = "insert into users values(null,'"+username+"','"+password+"','"+firstname+"','"+lastname+"')"
        logging.info("Query to insert into users ->"+sql)
        try:
          conn = DBConnect.getConnection()
      
        except Exception as e:
          print ("Connection Error ->", e)
          logging.error("Connection Error ->"+str(e))

        try:
          conn.query(sql)
          new_id = conn.insert_id()
          #print("id generated is =>",new_id)
          #sql_acc = "insert into accounts values("+account_number+",1000,'"+bankname+"',"+new_id+")"
          sql_acc = "insert into accounts values("+str(account_number)+",1000.0,'"+bankname+"',"+str(new_id)+")"
          logging.debug("Query to insert into accounts ->"+sql_acc)
          conn.query(sql_acc)
          result = True
        except Exception as e:
          print("Database error =>",e)
          logging.error("Database error, "+(e))
          result = False
        finally:
          conn.close()
      
        return result


  

