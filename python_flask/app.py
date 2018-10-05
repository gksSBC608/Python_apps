from flask import Flask, render_template, request, redirect, session, abort
from service import db_access,utils
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
util = utils.Util()

@app.after_request
def apply_caching(response):
    logging.info("Gaurav")
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
        username = form.get('username')
        password=form.get('password')
        print("login credentials: "+username+" "+password)
        logging.info("login credentials: "+username+" "+password)
        password1 = form.get("password1")
        if(password != password1):
               msg = "<h4><font color=red>Two passwords don't match</font></h4>"
               msg += "<div align='left'><a href='register'>Go To Register Page</a></div>"
               return msg
        #print(username+" "+password)
        passwordReset = dbAccess.reset_password(username,password)
        if(passwordReset):
            print("Password reset to: "+password)
            return redirect("login", code=302)
            

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
            acc_no_valid = util.validate_account_number(acc_number)
            if(not acc_no_valid):
                msg = "Account number needs to be of valid format"
                return "{\"message\":"+msg+"}",400
            #username = "ankur"
            payee_acc_number = data["payee_acc_number"]
            payee_acc_name = data["payee_acc_name"]
            payee_acc_bank = data["payee_acc_bank"]
            payee = (payee_acc_number,payee_acc_name,payee_acc_bank)
            payee_data_valid = util.validate_payee_fields(payee)
            if(not payee_data_valid):
                msg = "Payee data invalid"
                return "{\"message\":\""+msg+"\"}",400
            amount_to_transfer = data["amount_to_transfer"]
            amount_valid = util.validate_money_amount(amount_to_transfer)
            if(not amount_valid):
                msg = "Amount not of valid format"
                return "{\"message\":\""+msg+"\"}",400, {'ContentType':'application/json'}
            account_balance = dbAccess.fetch_account_balance(acc_number)
            amount_valid = util.validate_transfer_amount(account_balance,amount_to_transfer)
            if(not amount_valid):
                msg = "Transfer amount exceeds limit, account balance shouldn't be below 1000"
                return "{\"message\":\""+msg+"\"}",400, {'ContentType':'application/json'}
            logging.info("Money transfer initiated between "+username+" and "+payee_acc_name)
            money_transfer_parties =(acc_number,username,payee_acc_number,payee_acc_name,payee_acc_bank,amount_to_transfer)
            is_money_tranfered = dbAccess.transfer_money(money_transfer_parties)
            if(is_money_tranfered):
                message = "<font color=green>Money transfered</font>"
                return json.dumps({'message':message}), 200, {'ContentType':'application/json'}
            else:
                message = "<font color=red>Transaction failed</font>"
                return json.dumps({'message':message}), 400, {'ContentType':'application/json'}            
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
            sec_key = form['sec_key']
            acc_no_valid = util.validate_account_number(acc_number)
            if(not acc_no_valid):
                msg = "Account number needs to be of valid format"
                return "{\"message\":\""+msg+"\"}",400
            amount_valid = util.validate_money_amount(amount)
            if(not amount_valid):
                msg = "Amount not valid"
                return "{\"message\":\""+msg+"\"}",400
            sec_key_to_match = dbAccess.get_sec_key("deposit_money",username)
            if(sec_key==sec_key_to_match):
                money_deposited = dbAccess.deposit_money(username,acc_number,amount)
                if(money_deposited):
                    logging.info("Money deposited, amount is "+str(amount))
                    return "<font color='green'>Money deposited</font>",202;
                else:
                    return "<font color='red'>Money couldn't be deposited</font>",501;
            else:
                logging.info("security keys don't match")
                # implement kill session
                session.clear()
                return "Access forbidden",403
        
    else:
        session['message']="Session invalid"
        return redirect("error", code=400)
            
    
@app.route('/accountbalance')
def accountbalance():
    if 'user' in session:
        username = session.get('user')
        acc_number = request.args.get("acc_number")
        acc_no_valid = util.validate_account_number(acc_number)
        if(not acc_no_valid):
            msg = "Account number needs to be of valid format"
            return "{\"message\":"+msg+"}",400
        acc_balance = dbAccess.fetch_account_balance(acc_number)
        return "{\"balance\":"+str(acc_balance)+"}",200
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
            sec_key = form.get("sec_key")
            #username = "ankur"
            acc_number = form.get("acc_number")
            #print("In controller : "+str(payee_acc_number))
            sec_key_to_match = '1256asdf65'
            sec_key_to_match = dbAccess.get_sec_key("remove_payee",username)
            logging.info("sec key in header is:->"+sec_key)
            logging.info("sec key to be matched with is:->"+sec_key_to_match)
            if(sec_key==sec_key_to_match):
                payee=(payee_acc_number,payee_acc_name,payee_acc_bank)
                payee_data_valid = util.validate_payee_fields(payee)
                if(not payee_data_valid):
                    msg = "Payee data not valid"
                    return msg,400
                payee_removed = dbAccess.remove_payee(payee)
                if(payee_removed):
                    res ="<h3><font color=green>Payee removed</font></h3>"
                    redirect_url = "/home"
                    res += "<a href ="+redirect_url+">Go to home page</a>"
                    return res,202
                else:
                    res ="<h3><font color=red>Payee remove unsuccessful</font></h3>"
                    redirect_url = "/home"
                    res += "<a href ="+redirect_url+">Go to home page</a>"
                    return res,500
            else:
                logging.info("security keys don't match")
                # implement kill session
                session.clear()
                return "Access forbidden",403
            
        
    else:
        session['message']="Session invalid"
        return redirect("error", code=400)
    

@app.route('/check_benficiary',methods=['POST'])
def check_benficiary():
    if 'user' in session:
        logging.info("request.data is:"+str(request.data))
        logging.info("request.json is:"+str(request.json))
        data = request.json
        payee_acc_no = data['payee_acc_no']
        username = session.get('user')
        payee_acc_valid = util.validate_account_number(payee_acc_no)
        if(not payee_acc_valid):
            msg = "Payee account number not of valid format"
            return msg,400
        payee_added = dbAccess.check_benficiary(username,payee_acc_no)
        logging.info("response from dao layer:->"+str(payee_added))
        if(payee_added):
            #return "payee account number exists"
            return json.dumps({'acc_exists':True}), 200, {'ContentType':'application/json'}
        else:
            #return "payee account number doesn't exist"
            sec_key = util.generate_sec_key()
            print("sec key is "+sec_key)
            result = dbAccess.update_sec_key("add_payee",sec_key,username)
            if(result):
                return json.dumps({'acc_exists':False}), 200, {'ContentType':'application/json','security-key':sec_key}
            else:
                return json.dumps({'acc_exists':True}), 200, {'ContentType':'application/json','security-key':''}
    else:
        session['message']="Session invalid"
        return redirect("error", code=400)
    

@app.route('/payee.add',methods=['GET', 'POST'])
def add_payee():
    if 'user' in session:
        username = session.get('user')
        if request.method == 'GET':
            return render_template("addpayee.html")
        elif request.method == 'POST':
            sec_key = request.headers.get('security-key')
            sec_key_to_match = '1234asdf56'
            sec_key_to_match = dbAccess.get_sec_key("add_payee",username)
            print("sec key in header is:->"+sec_key)
            print("sec key to be matched with is:->"+sec_key_to_match)
            logging.info("sec key in header is:->"+sec_key)
            logging.info("sec key to be matched with is:->"+sec_key_to_match)
            print("Going to compare")
            if(sec_key==sec_key_to_match):
                logging.info("matched the security keys successfully")
                form = request.form
                payee_acc_no=form['payee_acc_no']
                payee_acc_name=form.get('payee_acc_name')
                payee_acc_bank=form.get('payee_acc_bank')
                #username ='ankur'
                username = session.get('user')
                payee_added = dbAccess.check_benficiary(username,payee_acc_no)
                if(payee_added):
                    return json.dumps({'message':'Account already exists'}), 400, {'ContentType':'application/json'}
                user_id = dbAccess.get_userid_by_username(username)
                logging.info("user id obtained from the DB for user "+username+" is:= "+str(user_id))
                payee = (payee_acc_no,payee_acc_name,payee_acc_bank,user_id)
                logging.info("payee data to be added:-> "+payee_acc_no+" "+payee_acc_name+" "+payee_acc_bank)
                payee_data_valid = util.validate_payee_fields(payee)
                if(not payee_data_valid):
                    msg = "Payee data invalid"
                    return msg,400
                payee_added = dbAccess.add_payee(payee)
                if(payee_added):
                    #return "payee added", 202
                    return json.dumps({'message':"payee added"}), 202, {'ContentType':'application/json'}
                else:
                    #return "payee could not be added",400
                    return json.dumps({'message':"payee could not be added"}), 400, {'ContentType':'application/json'}
            else:
                logging.info("security keys don't match")
                # implement kill session
                session.clear()
                return "Forbidden",403
    else:
        session['message']="Session invalid"
        return redirect("error", code=403)

@app.route('/getpayee_accounts')
def getpayee_accounts():
    if 'user' in session:
        username = session.get('user')
        sec_key = util.generate_sec_key()
        print("sec key is "+sec_key)
        sec_key_generated = dbAccess.update_sec_key("transfer_money_payee_data",sec_key,username)
        if(sec_key_generated):
            payee_accounts = dbAccess.get_payee_accounts(username)
            return str(payee_accounts),200,{'security-key':sec_key}
        else:
            payee_accounts =[]
            return str(payee_accounts),500,{'security-key':'1234asdf56'}
    else:
        session['message']="Session invalid"
        return redirect("error", code=400)
    
@app.route('/getpayee_accounts_0')
def getpayee_accounts_for_remove_payee():
    if 'user' in session:
        username = session.get('user')
        sec_key = util.generate_sec_key()
        print("sec key is "+sec_key)
        sec_key_generated = dbAccess.update_sec_key("remove_payee_0",sec_key,username)
        if(sec_key_generated):
            payee_accounts = dbAccess.get_payee_accounts(username)
            return str(payee_accounts),200,{'security-key':sec_key}
        else:
            payee_accounts =[]
            return str(payee_accounts),500,{'security-key':'1234asdf56'}
    else:
        session['message']="Session invalid"
        return redirect("error", code=400)


@app.route('/getpayee_data_0')
def getpayee_data_for_remove_payee_request():
    if 'user' in session:
        sec_key = request.headers.get('security-key')
        sec_key_to_match = '1234asdf56'
        username = session.get('user')
        sec_key_to_match = dbAccess.get_sec_key("remove_payee_0",username)
        logging.info("sec key in header is:->"+sec_key)
        logging.info("sec key to be matched with is:->"+sec_key_to_match)
        if(sec_key==sec_key_to_match):
            payee_acc_number = request.args.get("payee_acc_number")
            payee_data = dbAccess.get_payee_data(payee_acc_number)
            #print(str(payee_data))
            #result = "{\"ben_name\":"+payee_data[0]+","\"bank_name\":"+payee_data[1]+"}"
            result = "{\"ben_name\":\""+payee_data[0]+"\","
            result += "\"bank_name\":\""+payee_data[1]+"\"}"
            #return result,{'security-key':'1256asdf65'}
            sec_key = util.generate_sec_key()
            print("sec key is "+sec_key)
            logging.info("Going to insert the sec key to remove payee")
            sec_key_updated = dbAccess.update_sec_key("remove_payee",sec_key,username)
            #logging.info("Inserted the sec key to remove payee")
            #logging.info("After inserting the sec key to remove payee, result got from db layer is "+str(sec_key_updated))
            #print("Inserted the sec key to remove payee")
            #print("After inserting the sec key to remove payee, result got from db layer is "+str(sec_key_updated))
            if(sec_key_updated):
                return result,{'security-key':sec_key}
            else:
                return result,500,{'security-key':''}
        else:
            logging.info("security keys don't match")
            # implement kill session
            session.clear()
            return "Forbidden",403
    else:
        return "Invalid session",401

@app.route('/getpayee_data')
def getpayee_data():
    if 'user' in session:
        sec_key = request.headers.get('security-key')
        sec_key_to_match = '1234asdf56'
        username = session.get('user')
        sec_key_to_match = dbAccess.get_sec_key("transfer_money_payee_data",username)
        logging.info("sec key in header is:->"+sec_key)
        logging.info("sec key to be matched with is:->"+sec_key_to_match)
        if(sec_key==sec_key_to_match):
            payee_acc_number = request.args.get("payee_acc_number")
            payee_data = dbAccess.get_payee_data(payee_acc_number)
            #print(str(payee_data))
            #result = "{\"ben_name\":"+payee_data[0]+","\"bank_name\":"+payee_data[1]+"}"
            result = "{\"ben_name\":\""+payee_data[0]+"\","
            result += "\"bank_name\":\""+payee_data[1]+"\"}"
            return result,{'security-key':'1256asdf65'}
        else:
            logging.info("security keys don't match")
            # implement kill session
            session.clear()
            return "Forbidden",403
    else:
        return "Invalid session",401





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
    payee_data_valid = self.util.validate_payee_fields(payee)
    if(not payee_data_valid):
        msg = "Payee data not valid"
        return msg,400
    payee_removed = dbAccess.remove_payee(payee)
    if(payee_removed):
        res ="<h3><font color=green>Payee removed</font></h3>"
        redirect_url = "/home"
        res += "<a href ="+redirect_url+">Go to home page</a>"
        return res,202
    else:
        res ="<h3><font color=red>Payee remove unsuccessful</font></h3>"
        redirect_url = "/home"
        res += "<a href ="+redirect_url+">Go to home page</a>"
        return res,500

@app.route('/accountdetail')
def accountdetail():
    if 'user' in session:
        username = session.get('user')
        #username = "ankur"
        acc_detail = dbAccess.account_detail(username)
        sec_key = util.generate_sec_key()
        print("sec key for deposit money is "+sec_key)
        logging.info("sec key for deposit money is "+sec_key)
        sec_key_added = dbAccess.update_sec_key("deposit_money",sec_key,username)
        account = {}
        
        if(sec_key_added):
            account['acc_number']=acc_detail[0]
            account['acc_balance']=acc_detail[1]
            account['sec_key']=sec_key
            return json.dumps(account), 200, {'ContentType':'application/json'}
        else:
            return json.dumps(account), 500, {'ContentType':'application/json'}
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
        message = {}
        message['page']="register"
        return render_template("register.html",message='register')
    elif request.method == 'POST':
        form = request.form
        firstname=form['firstname']
        lastname=form.get('lastname')
        bankname=form['bankname']
        username=form['username']
        password=form.get('password')
        password1 = form["password1"]
        registration_data=(firstname,lastname,bankname,username)
        registration_data_valid = util.validate_registration_fields(registration_data)
        if(not registration_data_valid):
            msg = "Registration data invalid"
            return msg,400
        if(password != password1):
               msg = "<h4><font color=red>Two passwords don't match</font></h4>"
               msg += "<div align='left'><a href='register'>Go To Register Page</a></div>"
               return msg,400
               #abort(404)
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
            return msg,200
        else:
            msg = "<div align='left'><a href='/python_project'>Go To Login Page</a></div>"
            msg += "<div align='right'><a href='/register'>Go To Register Page</a></div>"
            msg += "<h4>Could not register "+firstname+" "+lastname+"</h4>"
            return msg,500
        

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
        return render_template("home.html",profile=profile),200
    else:
        session['message']="Session invalid"
        return redirect("error", code=303)

@app.route('/error')
def error_page():
    if 'user' in session:
        message=session.get('message')
        session.clear()
        if(message==None):
            message = "Invalid session"
        return render_template("error.html",message=message),401
    else:
        session.clear()
        return render_template("login.html"),400
    

@app.route('/logout')
def logout():
    if 'user' in session:
        session.clear()
        return render_template("login.html")
    else:
        #return "Invalid session",401
        return render_template("login.html"),400

@app.route('/header')
def serve_header():
    #reset the session data
    session.clear()
    return render_template("header_homepage.html")
    

@app.route('/header.login')
def serve_login_header():
    #reset the session data
    session.clear()
    return render_template("header_login.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = request.form
        username=form['username']
        password=form.get('password')
        logging.info("login credentials: "+username+" "+password)
        field_validated = util.validate_login_fields(username)
        is_user_valid = False
        if(field_validated):
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
                return session.get('user')+" has an active session",400
            else:
                return "Invalid credentials",400
    else:
        # reset the session data
        #session.clear()
        return render_template("login.html")

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(host='0.0.0.0',port=8083,debug=True)
