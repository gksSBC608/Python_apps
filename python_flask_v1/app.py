from flask import Flask, render_template, request, redirect, session
from service import db_access
from random import randint
import logging,re,os,json


def init_config():
    """
    This method is called in beginning, it configures error handling to show CGI errors on UI and
    enables logging in proper format
    """
    log_fname = "logs/my_account_app.log"
    logging.basicConfig(filename=log_fname,
                    filemode='a',
                    level=logging.DEBUG,
                    format='%(asctime)s : %(levelname)s %(filename)s => %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                   )
init_config()
app = Flask(__name__)

dbAccess = db_access.DBAccess()

@app.after_request
def apply_caching(response):
    #logging.info("Gaurav")
    logging.debug(str(response))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0"
    #response.headers["Pragma"] = "no-cache"
    return response

@app.before_request
def session_management():
    # make the session last indefinitely until it is cleared
    session.permanent = True

@app.route('/')
def login_page():
    # reset the session data
    session.clear()
    return render_template("index.html")

@app.route('/password.reset',methods=['GET', 'POST'])
def reset_password():
    if request.method == 'GET':
        return render_template("resetpassword.html")
    elif request.method == 'POST':
        form = request.form
        username="ankur"
        password=form.get('password')
        logging.info("login credentials: "+username+" "+password)
        password1 = form.get("password1")
        if(password != password1):
               msg = "<h4><font color=red>Two passwords don't match</font></h4>"
               msg += "<div align='left'><a href='register'>Go To Register Page</a></div>"
               return msg
        #print(username+" "+password)
        passwordReset = dbAccess.reset_password(username,password)
        if(passwordReset):
            return redirect("login", code=200)
            

@app.route('/is_user_registered',methods=['GET'])
def is_user_registered():
    username = request.args.get("username")
    is_registered = dbAccess.check_if_user_registered(username)
    return json.dumps({'user':is_registered}), 200, {'ContentType':'application/json'}
    

@app.route('/money.transfer',methods=['GET', 'POST'])
def transfer_money():
    if 'user' in session:
        username = session.get('user')
        if request.method == 'GET':
            return render_template("transfermoney.html")
        elif request.method == 'POST':
            data = request.json
            acc_number = data["account_number"]
            #username = "ankur"
            payee_acc_number = data["payee_acc_number"]
            payee_acc_name = data["payee_acc_name"]
            payee_acc_bank = data["payee_acc_bank"]
            amount_to_transfer = data["amount_to_transfer"]
            logging.info("Money transfer initiated between "+username+" and "+payee_acc_name)
            money_transfer_parties =(acc_number,username,payee_acc_number,payee_acc_name,payee_acc_bank,amount_to_transfer)
            is_money_tranfered = dbAccess.transfer_money(money_transfer_parties)
            if(is_money_tranfered):
                message = "<font color=green>Money transfered</font>"
                return json.dumps({'message':message}), 200, {'ContentType':'application/json'}
            else:
                message = "<font color=red>Transaction failed</font>"
                return json.dumps({'message':message}), 200, {'ContentType':'application/json'}            
    else:
        session['message']="Session invalid"
        return redirect("error", code=400)
    

@app.route('/money.deposit',methods=['GET', 'POST'])
def deposit_money():
    if 'user' in session:
        username = session.get('user')
        if request.method == 'GET':
            return render_template("depositmoney.html")
        elif request.method == 'POST':
            form = request.form
            #username='ankur'
            acc_number = form['acc_number']
            amount = form['amount']
            money_deposited = dbAccess.deposit_money(username,acc_number,amount)
            if(money_deposited):
                logging.info("Money deposited, amount is "+str(amount))
                return "<font color='green'>Money deposited</font>";
            else:
                return "<font color='red'>Money couldn't be deposited</font>";
        
    else:
        session['message']="Session invalid"
        return redirect("error", code=400)
            
    
@app.route('/accountbalance')
def accountbalance():
    if 'user' in session:
        username = session.get('user')
        acc_number = request.args.get("acc_number")
        acc_balance = dbAccess.fetch_account_balance(acc_number)
        return "{\"balance\":"+str(acc_balance)+"}"
    else:
        session['message']="Session invalid"
        return redirect("error", code=400)
    

@app.route('/payee.remove',methods=['GET', 'POST'])
def remove_payee():
    if 'user' in session:
        username = session.get('user')
        if request.method == 'GET':
            return render_template("removepayee.html")
        elif request.method == 'POST':
            form = request.form
            payee_acc_number = form.get("payee_acc_number")
            payee_acc_name = form.get("payee_acc_name")
            payee_acc_bank = form.get("payee_acc_bank")
            #username = "ankur"
            acc_number = form.get("acc_number")
            #print("In controller : "+str(payee_acc_number))
            payee=(payee_acc_number,payee_acc_name,payee_acc_bank)
            payee_removed = dbAccess.remove_payee(payee)
            if(payee_removed):
                res ="<h3><font color=green>Payee removed</font></h3>"
                redirect_url = "/home"
                res += "<a href ="+redirect_url+">Go to home page</a>"
            else:
                res ="<h3><font color=red>Payee remove unsuccessful</font></h3>"
                redirect_url = "/home"
                res += "<a href ="+redirect_url+">Go to home page</a>"
            return res
        
    else:
        session['message']="Session invalid"
        return redirect("error", code=400)
    

@app.route('/check_benficiary',methods=['POST'])
def check_benficiary():
        logging.info("request.data is:"+str(request.data))
        logging.info("request.json is:"+str(request.json))
        data = request.json
        payee_acc_no = data['payee_acc_no']
        username ='ankur'
        #logging.info("before getting user_id, username is:="+username)
        #user_id = dbAccess.get_userid_by_username(username)
        #logging.info("username "+username+" && user_id"+user_id)
        payee_added = dbAccess.check_benficiary(username,payee_acc_no)
        logging.info("response from dao layer:->"+str(payee_added))
        if(payee_added):
            #return "payee account number exists"
            return json.dumps({'acc_exists':True}), 200, {'ContentType':'application/json'}
        else:
            #return "payee account number doesn't exist"
            return json.dumps({'acc_exists':False}), 200, {'ContentType':'application/json','security-key':'1234asdf56'}
        
    

@app.route('/payee.add',methods=['GET', 'POST'])
def add_payee():
    if 'user' in session:
        username = session.get('user')
        if request.method == 'GET':
            return render_template("addpayee.html")
        elif request.method == 'POST':
            sec_key = request.headers.get('security-key')
            sec_key_to_match = '1234asdf56'
            logging.info("sec key in header is:->"+sec_key)
            logging.info("sec key to be matched with is:->"+sec_key_to_match)
            if(sec_key==sec_key_to_match):
                logging.info("matched the keys")
                form = request.form
                payee_acc_no=form['payee_acc_no']
                payee_acc_name=form.get('payee_acc_name')
                payee_acc_bank=form.get('payee_acc_bank')
                username ='ankur'
                user_id = dbAccess.get_userid_by_username(username)
                logging.info("user id obtained from the DB is:= "+str(user_id))
                payee = (payee_acc_no,payee_acc_name,payee_acc_bank,user_id)
                logging.info("payee data to be added:-> "+payee_acc_no+" "+payee_acc_name+" "+payee_acc_bank)
                payee_added = dbAccess.add_payee(payee)
                if(payee_added):
                    return "payee added", 200
                else:
                    return "payee could not be added",202
            else:
                logging.info("security keys don't match")
                # implement kill session
                session.clear()
                return "this is response"
    else:
        session['message']="Session invalid"
        return redirect("error", code=400)

@app.route('/getpayee_accounts')
def getpayee_accounts():
    if 'user' in session:
        username = session.get('user')
        #username = "ankur"
        payee_accounts = dbAccess.get_payee_accounts(username)
        return str(payee_accounts)
    else:
        session['message']="Session invalid"
        return redirect("error", code=400)

@app.route('/getpayee_data')
def getpayee_data():
    payee_acc_number = request.args.get("payee_acc_number")
    payee_data = dbAccess.get_payee_data(payee_acc_number)
    #print(str(payee_data))
    #result = "{\"ben_name\":"+payee_data[0]+","\"bank_name\":"+payee_data[1]+"}"
    result = "{\"ben_name\":\""+payee_data[0]+"\","
    result += "\"bank_name\":\""+payee_data[1]+"\"}"
    return result

@app.route('/remove_payee',methods=['POST'])
def remove_payee_from_record():
    form = request.form
    payee_acc_number = form.get("payee_acc_number")
    payee_acc_name = form.get("payee_acc_name")
    payee_acc_bank = form.get("payee_acc_bank")
    username = "ankur"
    acc_number = form.get("acc_number")
    #print("In controller : "+str(payee_acc_number))
    payee=(payee_acc_number,payee_acc_name,payee_acc_bank)
    payee_removed = dbAccess.remove_payee(payee)
    if(payee_removed):
        res ="<h3><font color=green>Payee removed</font></h3>"
        redirect_url = "/home"
        res += "<a href ="+redirect_url+">Go to home page</a>"
    else:
        res ="<h3><font color=red>Payee remove unsuccessful</font></h3>"
        redirect_url = "/home"
        res += "<a href ="+redirect_url+">Go to home page</a>"
    return res

@app.route('/accountdetail')
def accountdetail():
    if 'user' in session:
        username = session.get('user')
        #username = "ankur"
        acc_detail = dbAccess.account_detail(username)
        account = {}
        account['acc_number']=acc_detail[0]
        account['acc_balance']=acc_detail[1]
        return json.dumps(account), 200, {'ContentType':'application/json'}   
    else:
        session['message']="Session invalid"
        return redirect("error", code=400)
    
def generate_account_number():
        """ This method generates dynamic account number
        """
        acc_first_five_char = "98001"
        last_five_digit = randint(10000, 99999)
        str_d = acc_first_five_char+str(last_five_digit)
        acc_number = int(str_d)
        logging.info("Account number generated")
        return acc_number 

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    elif request.method == 'POST':
        form = request.form
        firstname=form['firstname']
        lastname=form.get('lastname')
        bankname=form['bankname']
        username=form['username']
        password=form.get('password')
        password1 = form["password1"]
        if(password != password1):
               msg = "<h4><font color=red>Two passwords don't match</font></h4>"
               msg += "<div align='left'><a href='register'>Go To Register Page</a></div>"
               return msg
        registration_data=(firstname,lastname,bankname,username)
        account_number = generate_account_number()
        logging.info("New account number "+str(account_number)+" created for "+firstname+" "+lastname)
        user_profile = (firstname,lastname,bankname,username,password,account_number)
        #print(firstname,lastname,bankname,username,password,password1,account_number,sep="; ")
        is_registered = dbAccess.register_user(user_profile)
        if(is_registered):
            logging.info("Account number "+str(account_number)+" registered for user "+firstname+" "+lastname)
            msg = "<h4><font color=green>Registered <b>"+firstname+" "+lastname+"</b> for account <b>"+str(account_number)+", </b> with username <b>"+username+"</b></font></h4>"
            msg += "<div align='left'><a href='/login'>Go To Login Page</a></div>"
            return msg
        else:
            msg = "<div align='left'><a href='/python_project'>Go To Login Page</a></div>"
            msg += "<div align='right'><a href='/register'>Go To Register Page</a></div>"
            msg += "<h4>Could not register "+firstname+" "+lastname+"</h4>"
            return msg
        

@app.route('/home')
def homepage():
    if 'user' in session:
        username = session.get('user')
        user_profile=dbAccess.fetch_account_detail(username)
        profile = {}
        profile['Account Name']=user_profile[0]+" "+user_profile[1]
        session['user'] = username
        profile['Bank Name']=user_profile[4]
        profile['Account Number']=user_profile[2]
        profile['Account Balance']=user_profile[3]
        profile['username']=username
        return render_template("home.html",profile=profile)
    else:
        session['message']="Session invalid"
        return redirect("error", code=400)

@app.route('/error')
def error_page():
    if 'user' in session:
        message=session.get('message')
        session.clear()
        if(message==None):
            message = "Invalid session"
        return render_template("error.html",message=message)
    else:
        session.clear()
        return render_template("login.html")
    

@app.route('/logout')
def logout():
    session.clear()
    return render_template("login.html")

@app.route('/header')
def serve_header():
    return render_template("header_homepage.html")

@app.route('/header.login')
def serve_login_header():
    return render_template("header_login.html")
   


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = request.form
        username=form['username']
        password=form.get('password')
        logging.info("login credentials: "+username+" "+password)
        creds = (username,password)
        is_user_valid = dbAccess.validate_login(username,password)
        if(is_user_valid):
            user_profile=dbAccess.fetch_account_detail(username)
            profile = {}
            profile['Account Name']=user_profile[0]+" "+user_profile[1]
            session['user'] = username
            profile['Bank Name']=user_profile[4]
            profile['Account Number']=user_profile[2]
            profile['Account Balance']=user_profile[3]            
	    #return str(user_profile)
            return render_template("home.html",profile=profile)
        else:
            if 'user' in session:
                return session.get('user')
            else:
                return "Invalid credentials"
    else:
        # reset the session data
        if(session):
            session.clear()        
        return render_template("login.html")

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(host='0.0.0.0',port=8082,debug=True)
