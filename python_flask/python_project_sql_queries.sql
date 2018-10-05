create database banking_tej;

use banking_tej;

create table users(
user_id int primary key auto_increment,
username varchar(20) unique,
password varchar(10),
firstname varchar(15),
lastname varchar(15)
);

create table accounts(
account_number bigint(10) primary key,
account_balance double,
bank_name varchar(30),
user_id int,
unique(account_number,bank_name),
foreign key(user_id) references users(user_id)
);

create table beneficiaries(
beneficiary_id int primary key auto_increment,
beneficiary_name  varchar(40),
beneficiary_ac_no bigint unique,
beneficiary_user_id int,
user_id int,
foreign key(beneficiary_user_id) references users(user_id),
foreign key(user_id) references users(user_id),
foreign key(beneficiary_ac_no) references accounts(account_number)
);

create table security_keys(
key_id varchar(20) primary key,
key_value varchar(50),
user_id int,
foreign key(user_id) references users(user_id)
);

select key_value from security_keys INNER JOIN users where security_keys.key_id='add_payee' and users.username='teji';

insert into users values(null,'gaurav','password','Gaurav','Sharan');
insert into accounts values(9800150001,30000.0,'State Bank Of India',1 );

INSERT INTO security_keys VALUES('add_payee', '?t~cb;tqcS92U]D?iFvQZaK$mN', 1) ON DUPLICATE KEY UPDATE key_value="A";
INSERT INTO security_keys VALUES('add_payee', '?t~cb;tqcS92U]D?iFvQZaK$mN', (select user_id from users where username = 'teji')) ON DUPLICATE KEY UPDATE key_value="A";  
#name="A", age=19