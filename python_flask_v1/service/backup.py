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
