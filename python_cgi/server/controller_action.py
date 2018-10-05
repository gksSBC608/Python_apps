#!"C:\Users\Gaurav\AppData\Local\Programs\Python\Python36-32\\python.exe"

import cgi, cgitb, os, logging, re
from service import DBAccess,utils
from random import randint

print ("Content-Type: text/html\n\n")

def init_config():
    """
    This method is called in beginning, it configures error handling to show CGI errors on UI and
    enables logging in proper format
    """
    cgitb.enable()
    log_fname = "logs/my_account_app.log"
    logging.basicConfig(filename=log_fname,
                    filemode='a',
                    level=logging.DEBUG,
                    format='%(asctime)s : %(levelname)s %(filename)s => %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                   )




class Account():
    """ This is controler class, it receives request from client
    and processes by contacting Service class to access database
    """
    dbAccess = None
    uri_base= ""
    #util = util.Util()
    
    def __init__(self):
         self.dbAccess = DBAccess.DBAccess()
         self.util = utils.Util()
         #print("From inside constructor")

    def get_uri_base(self,url):
        tokens = url.split("/")
        self.uri_base = tokens[1]        

    def generate_account_number(self):
        """ This method generates dynamic account number
        """
        acc_first_five_char = "98001"
        last_five_digit = randint(10000, 99999)
        str_d = acc_first_five_char+str(last_five_digit)
        acc_number = int(str_d)
        logging.info("Account number generated")
        return acc_number

    def render_dashboard(self,username):
        """ This method is meant to render content on dashboard when login
            is successful
        """
        header = "<div align='right'><a href='/"+self.uri_base+"'>Logout</a></div>"
        logging.debug("header in home page has content =>"+header)
    
        user_profile = self.dbAccess.fetch_account_detail(username);
        acc_number = user_profile[2]
        acc_holder_name = user_profile[0]+" "+user_profile[1]
        acc_balance = user_profile[3]
    
    
        content = "<div align = center><table>"
        content += "<tr><td>Account Name</td><td>"+acc_holder_name+"</td></tr>"
        content += "<tr><td>Account Number</td><td>"+str(acc_number)+"</td></tr>"
        content += "<tr><td>Account Balance</td><td>"+str(acc_balance)+"</td></tr>"
        content += "</table></div>"

        query_string = "?username="+username+"&acc_number="+acc_number
        footer = "<div>";

        add_payee_btn = "<button type='button' onclick=\"window.location.href='/"+self.uri_base+"/addpayee.html"+query_string+"'\">Add Payee</button>"
        remove_payee_btn = "<button type='button' onclick=\"window.location.href='/"+self.uri_base+"/removepayee.html"+query_string+"'\">Remove Payee</button>"
        money_transfer_btn = "<button type='button' onclick=\"window.location.href='/"+self.uri_base+"/transfermoney.html"+query_string+"'\">Transfer Money</button>"
        money_deposit_btn = "<button type='button' onclick=\"window.location.href='/"+self.uri_base+"/depositmoney.html"+query_string+"'\">Deposit Money</button>"

        footer += add_payee_btn+"<br>"
        footer += remove_payee_btn+"<br>"
        footer += money_transfer_btn+"<br>"
        footer += money_deposit_btn+"<br>"
        print(header)
        print("<h2 align='center'>User Dashboard</h2>")
        print(content)
        print(footer)


    def process_login(self):
        """ This method has the logic to accept credentials to login, validate it
            and render dashboard, error page if wrong credentials is passed
        """
        # Create the form object
        frmLogin = cgi.FieldStorage()
        # Get the values
        username = frmLogin.getvalue("username")
        password = frmLogin.getvalue("password")

        
        #field_vaidated = self.validate_login_fields(username)
        field_vaidated = self.util.validate_login_fields(username)
        if(field_vaidated):
            isValidUser = self.dbAccess.validate_login(username,password)

        if(isValidUser==True):
            #print("User "+username+" validated to login")
            logging.info("User "+username+" validated to login")
            self.render_dashboard(username)
            #self.render_data()
        else:
            logging.warning("User "+username+" is invalid")
            print("<h1><font color= red>Trespasser</font><h1>")
            print("<h3>You seem to have entered wrong username or password</h3>")
            print("<br><a href='/"+self.uri_base+"'>Go back to login page</a>")

    def process_reset_password(self):
        """ This method has the logic to rest password
        """
        #print("Inside reset password method")
        form = cgi.FieldStorage()
        username = form.getvalue("username")
        password = form.getvalue("password")
        password1 = form.getvalue("password1")
        if(password != password1):
               print("<h4><font color=red>Two passwords don't match</font></h4>")
               print("<div align='left'><a href='/"+self.uri_base+"/register.html'>Go To Register Page</a></div>")
               exit()
        #print(username+" "+password)
        passwordReset = self.dbAccess.reset_password(username,password)
        header = "<div align='left'><a href='/"+self.uri_base+"'>Go To Login Page</a></div>"
        if(passwordReset):
            logging.info("Password reset for user "+username)
            message = "<h3>Password Reset Successful</h3>"
        else:
            logging.warning("Password reset unsuccessful for user "+username)
            message = "<h3><font color=red>Some unknown error</font></h3>" 
        print(header)
        print(message)


    def process_register(self):
        """ This method has the logic to accept data to register a new user and redirects
            to login page on a successful registration.
        """
        form = cgi.FieldStorage()
        firstname = form.getvalue("firstname")
        lastname = form.getvalue("lastname")
        bankname = form.getvalue("bankname")
        username = form.getvalue("username")
        password = form.getvalue("password")
        password1 = form.getvalue("password1")

        registration_data=(firstname,lastname,bankname,username)
        registration_data_valid = self.util.validate_registration_fields(registration_data)
        #print("Registration data valid :"+registration_data_valid)
        if(registration_data_valid):
            if(password != password1):
               print("<h4><font color=red>Two passwords don't match</font></h4>")
               print("<div align='left'><a href='/"+self.uri_base+"/register.html'>Go To Register Page</a></div>")
            else:
                account_number = self.util.generate_account_number()
                logging.info("New account number "+str(account_number)+" created for "+firstname+" "+lastname)
                user_profile = (firstname,lastname,bankname,username,password,account_number)
                #print(firstname,lastname,bankname,username,password,password1,account_number,sep="; ")
                is_registered = self.dbAccess.register_user(user_profile)
                if(is_registered):
                    logging.info("Account number "+str(account_number)+" registered for user "+firstname+" "+lastname)
                    print("<h4><font color=green>Registered <b>"+firstname+" "+lastname+"</b> for account <b>"+str(account_number)+", </b> with username <b>"+username+"</b></font></h4>")
                    print("<div align='left'><a href='/"+self.uri_base+"'>Go To Login Page</a></div>")
                else:
                    print("<div align='left'><a href='/"+self.uri_base+"'>Go To Login Page</a></div>")
                    print("<div align='right'><a href='/"+self.uri_base+"/register.html'>Go To Register Page</a></div>")
                    print("<h4>Could not register "+firstname+" "+lastname+"</h4>")
        else:
            print("<div align='left'><a href='/"+self.uri_base+"'>Go To Login Page</a></div>")
            print("<div align='right'><a href='/"+self.uri_base+"/register.html'>Go To Register Page</a></div>")
            print("<font color=red><h4 align = center>Registration data invalid</h4></font>")
         
               
    def process_addpayee(self):
        """ This method receives data to add a new payee
        """
        form = cgi.FieldStorage()
        payee_added = False
        payee_acc_no = form.getvalue("payee_acc_no")
        payee_acc_name = form.getvalue("payee_acc_name")
        payee_acc_bank = form.getvalue("payee_acc_bank")
        username= form.getvalue("username")
        user_id = self.dbAccess.get_userid_by_username(username)
        acc_no = form.getvalue("acc_no")
        payee = (payee_acc_no,payee_acc_name,payee_acc_bank,user_id)
        payee_data_valid = self.util.validate_add_payee_fields(payee)
        if(payee_data_valid):
            payee_added = self.dbAccess.add_payee(payee)
        
        if(payee_added):
            logging.info("Payee "+payee_acc_name+" added by "+username)
            print("<div align='right'><a href='/"+self.uri_base+"'>Logout</a></div>")
            print("<div align='left'><a href='/"+self.uri_base+"/server/controller_action.py/render_dashboard?username="+username+"'>Go To Home</a></div>")
            print("<h3><font color=green>Payee "+payee_acc_name+" added</font></h3>")
        else:
            logging.error("Payee "+payee_acc_name+" couldn't be added")
            print("payee could not be added")
            
    def process_fetch_account_balance(self):
        """ This method has ha logic to fetch account balnce for the
            account number asked.
        """
        form = cgi.FieldStorage()
        acc_number = form.getvalue("acc_number")
        acc_balance = self.dbAccess.fetch_account_balance(acc_number)
        print("{\"balance\":"+str(acc_balance)+"}")

    def process_transfer_money(self):
        """This method is meant to transfer money from between two parties.
        First party is the logged in user and second one is any payee added
        earlier
        """
        form = cgi.FieldStorage()
        acc_number = form.getvalue("acc_number")
        username = form.getvalue("user_id")
        payee_acc_number = form.getvalue("payee_acc_number")
        payee_acc_name = form.getvalue("payee_acc_name")
        payee_acc_bank = form.getvalue("payee_acc_bank")
        amount_to_transfer = form.getvalue("amount_to_transfer")
        is_amount_valid = self.util.validate_money_amount(amount_to_transfer)
        logging.info("Money transfer initiated between "+username+" and "+payee_acc_name)
        is_money_tranfered = False
        if(is_amount_valid):
            money_transfer_parties =(acc_number,username,payee_acc_number,payee_acc_name,payee_acc_bank,amount_to_transfer)
            is_money_tranfered = self.dbAccess.transfer_money(money_transfer_parties)
        
        if(is_money_tranfered):
            redirect_url = "/"+self.uri_base+"/server/controller_action.py/render_dashboard?username="+username
            print("<h2><font color=green>Money transfered</font></h2>")
            print("<a href ="+redirect_url+">Go to home page</a>")
        
        else:
            print("<font color=red><h4>Transaction failed</h4></font>")

    def process_get_payee_accounts(self):
        """This method is meant to fetch all payee account numbers and populate
        those in UI to enable the user to transfer money
        """
        form = cgi.FieldStorage()
        username = form.getvalue("username")
        payee_accounts = self.dbAccess.get_payee_accounts(username)
        return payee_accounts;

    def process_get_payee_data(self):
        """This method is meant to fetch all payee account numbers and populate
        those in UI to enable the user to transfer money
        """
        form = cgi.FieldStorage()
        payee_acc_number = form.getvalue("payee_acc_number")
        payee_data = self.dbAccess.get_payee_data(payee_acc_number)
        #print(str(payee_data))
        #result = "{\"ben_name\":"+payee_data[0]+","\"bank_name\":"+payee_data[1]+"}"
        result = "{\"ben_name\":\""+payee_data[0]+"\","
        result += "\"bank_name\":\""+payee_data[1]+"\"}"
        print(result)

    def process_remove_payee(self):
        """This method is meant to remove a payee added earlier
        """
        form = cgi.FieldStorage()
        payee_acc_number = form.getvalue("payee_acc_number")
        payee_acc_name = form.getvalue("payee_acc_name")
        payee_acc_bank = form.getvalue("payee_acc_bank")
        username = form.getvalue("username")
        acc_number = form.getvalue("acc_number")
        #printnt("In controller : "+str(payee_acc_number))
        payee=(payee_acc_number,payee_acc_name,payee_acc_bank)
        payee_removed = self.dbAccess.remove_payee(payee)
        if(payee_removed):
            print("<h3><font color=green>Payee removed</font></h3>")
            redirect_url = "/"+self.uri_base+"/server/controller_action.py/render_dashboard?username="+username
            print("<a href ="+redirect_url+">Go to home page</a>")
        else:
            print("<h3><font color=red>Payee remove unsuccessful</font></h3>")
            redirect_url = "/"+self.uri_base+"/server/controller_action.py/render_dashboard?username="+username
            print("<a href ="+redirect_url+">Go to home page</a>")
    
    def process_deposit_money(self):
        """This method is meant to deposit the money to own account
        """
        form = cgi.FieldStorage()
        username = form.getvalue("username")
        acc_number = form.getvalue("acc_number")
        amount = form.getvalue("amount")
        #print(username,acc_number,amount,sep="->")
        #print("<br>")
        is_amount_valid = self.util.validate_money_amount(amount)
        if(is_amount_valid):
            money_deposited = self.dbAccess.deposit_money(username,acc_number,amount)
            if(money_deposited):
                logging.info("Money deposited, amount is "+str(amount))
                print("<font color='green'>Money deposited</font>");
            else:
                print("<font color='red'>Money couldn't be deposited</font>");
        else:
            print("<font color=red><h4>Invalid amount</h4></font>");

    def check_if_user_registered(self):
        form = cgi.FieldStorage()
        username = form.getvalue("username")
        is_registered = self.dbAccess.check_if_user_registered(username)
        print('{"user":"'+str(is_registered)+'"}')
        

"""These code fragments are decision making block to send control to any of
the controller methods based on URL pattern
""" 
    
account = Account()
init_config()
current_url = os.environ["REQUEST_URI"]
account.get_uri_base(current_url)

logging.info("Access URL is, "+current_url)

if(current_url.endswith("login")):
    account.process_login()
elif(current_url.endswith("/reset_password")):
    account.process_reset_password()
elif(current_url.endswith("/register")):
    account.process_register()
elif(current_url.endswith("/addpayee")):
    account.process_addpayee()
elif(re.search(".+render_dashboard.+",current_url)):
     form = cgi.FieldStorage()
     username = form.getvalue("username")
     account.render_dashboard(username)
elif(re.search(".+/accountbalance.+",current_url)):
    account.process_fetch_account_balance()    
elif(current_url.endswith("/transfer_money")):
    account.process_transfer_money()
elif(re.search(".+/getpayee_accounts.+",current_url)):
    account.process_get_payee_accounts()
elif(re.search(".+/is_user_registered.+",current_url)):
    account.check_if_user_registered()
elif(re.search(".+/getpayee_data.+",current_url)):
    account.process_get_payee_data()
elif(current_url.endswith("/remove_payee")):
    account.process_remove_payee()
elif(current_url.endswith("/deposit_money")):
    account.process_deposit_money()
