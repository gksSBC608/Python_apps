from service import db_access

dbAccess = db_access.DBAccess()
username= "admin"
password = "admin"
#isValidUser = dbAccess.validate_login(username,password)
#print(isValidUser)

#acc_detail = dbAccess.fetch_account_detail('admin')
#print(str(acc_detail))

#user_id = dbAccess.get_userid_by_username('admin')
#print(user_id)
#(1,)

payee_acc_no=1234567891
payee_acc_name="George K"
payee_acc_bank="State Bank of India"
username ='admin'
#user_id = dbAccess.get_userid_by_username(username)
#print("user id obtained from the DB is:= "+str(user_id))
#payee = (payee_acc_no,payee_acc_name,payee_acc_bank,user_id)
#print("payee data to be added:-> "+str(payee_acc_no)+" "+str(payee_acc_name)+" "+str(payee_acc_bank))
#payee_added = dbAccess.add_payee(payee)
#print("payee_added is :"+str(payee_added))

#form = request.form
firstname="Arijit"
lastname="Basu"
bankname="Dena Bank"
username="arijit"
password="password"
password1 = "password"
account_number = 1234567678
user_profile = (firstname,lastname,bankname,username,password,account_number)
#is_registered = dbAccess.register_user(user_profile)
#print(is_registered)

#dbAccess.account_detail(username)
#rec = dbAccess.check_benficiary(username,payee_acc_no)
#print(rec)
#accounts = dbAccess.get_payee_accounts('admin')
#print(accounts)

#payee_data=dbAccess.get_payee_data(1234567891)
#print(payee_data)

payee_acc_number = 1234567891
payee_acc_name = "George K"
payee_acc_bank = "State Bank of India"
username = "admin"
acc_number = 9800150001
#print("In controller : "+str(payee_acc_number))
payee=(payee_acc_number,payee_acc_name,payee_acc_bank)
#payee_removed = dbAccess.remove_payee(payee)
#print(payee_removed)

#is_reg=dbAccess.check_if_user_registered('admin')
#print(is_reg)
#is_reg=dbAccess.check_if_user_registered('admin1')
#print(is_reg)

username = "arijit"
password_new = "password1"
#passwordReset = dbAccess.reset_password(username,password_new)
#if(passwordReset):
#    print("password reset to "+password_new+" for user "+username)

#username='ankur'
acc_number = 1234567678
amount = 500
username="arijit"
#acc_balance = dbAccess.fetch_account_balance(acc_number)
#print("balance before deposit:- "+str(acc_balance))
#money_deposited = dbAccess.deposit_money(username,acc_number,amount)
#if(money_deposited):
#    print("Money deposited, amount is "+str(amount))
#acc_balance = dbAccess.fetch_account_balance(acc_number)
#print("balance after deposit:- "+str(acc_balance))

acc_number = 9800150001
username = "admin"
payee_acc_number = 1234567678
payee_acc_name = "Arijit Basu"
payee_acc_bank = "Dena Bank"
amount_to_transfer = 1000
print("Money transfer initiated between "+username+" and "+payee_acc_name)
money_transfer_parties =(acc_number,username,payee_acc_number,payee_acc_name,payee_acc_bank,amount_to_transfer)
is_money_tranfered = dbAccess.transfer_money(money_transfer_parties)
if(is_money_tranfered):
    message = "<font color=green>Money transfered</font>"
    print(message)


