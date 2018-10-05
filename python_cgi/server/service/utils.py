import logging,re
from random import randint

class Util():
    """ This class has the utility methods needed in controller

    """


    def validate_login_fields(self,username):
        # username shouldn't have special characters
        r1 = re.search("^\w+$",username)
        return r1;

    def validate_registration_fields(self,registration_data):
        name_pattern = "^[A-Z][a-z]+$"
        name_pattern1 = ""
        bankname_pattern = "^[A-Z][A-Za-z]+(\s[A-Za-z]+)+$"
        username_pattern = "^\w+$"
        firstname = registration_data[0]
        lastname = registration_data[1]
        bankname = registration_data[2]
        username = registration_data[3]
        r1 = bool(re.search(name_pattern,firstname))
        r2 = bool(re.search(name_pattern,lastname))
        r3 = bool(re.search(bankname_pattern,bankname))
        r4 = bool(re.search(username_pattern,username))
        return r1 and r2 and r3 and r4
        
        

    def validate_add_payee_fields(self,payee):
        name_pattern = "^[A-Z][a-z]+(\s{0,1}[A-Z][a-z]*)*$"
        bankname_pattern = "^[A-Z][A-Za-z]+(\s[A-Za-z]+)+$"
        acc_no_pattern = "^[1-9][0-9]{9}$"

        #print(str(payee))
        payee_acc_no = payee[0]
        payee_name = payee[1]
        payee_bankname = payee[2]

        r1 = bool(re.search(acc_no_pattern,payee_acc_no))
        r2 = bool(re.search(name_pattern,payee_name))
        r3 = bool(re.search(bankname_pattern,payee_bankname))
        
        return r1 and r2 and r3      
        
    
    def validate_money_amount(self,amount_to_transfer):
        amount_pattern = "^[\d]{2,5}$"
        return bool(re.search(amount_pattern,str(amount_to_transfer)))

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
        print(username)

     
