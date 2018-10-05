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
        
