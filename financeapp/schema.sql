
DROP TABLE IF EXISTS 'categories';
DROP TABLE IF EXISTS 'payment_methods';
DROP TABLE IF EXISTS 'transaction_types';
DROP TABLE IF EXISTS 'transactions';
DROP TABLE IF EXISTS 'users';

--
-- Table structure for table 'categories'
--
CREATE TABLE 'categories' (
  'id_categories' INTEGER  PRIMARY  KEY  AUTOINCREMENT,
  'category' TEXT DEFAULT NULL
)



-- Table structure for table 'payment_methods'
--
CREATE TABLE 'payment_methods' (
  'id' INTEGER  PRIMARY  KEY AUTOINCREMENT,
  'payment_method' TEXT NOT NULL,
  'user_id' INTEGER  NOT NULL,  
  FOREIGN KEY (user_id)
  REFERENCES users (id)  
  ON UPDATE CASCADE
) 

-- Table structure for table 'transaction_types'
--
CREATE TABLE 'transaction_types' (
  'idtransaction_types' INTEGER  PRIMARY  KEY AUTOINCREMENT,
  'type' TEXT DEFAULT NULL  
) 

--
-- Table structure for table 'transactions'
--
CREATE TABLE 'transactions' (
  'id' INTEGER  PRIMARY  KEY AUTOINCREMENT,
  'registered_time' datetime NOT NULL,
  'date' date NOT NULL,
  'description' TEXT NOT NULL,
  'is_paid' BOOLEAN  NOT NULL DEFAULT 'False',
  'user_id' INTEGER  NOT NULL,
  'category_id' INTEGER  NOT NULL,
  'payment_method_id' INTEGER  NOT NULL,
  'type_id' INTEGER  NOT NULL, 
  KEY 'transactions_user_idx' ('user_id'),
  KEY 'transactions_category_idx' ('category_id'),
  KEY 'transactions_payment_method_idx' ('payment_method_id'),
  KEY 'transactions_type_idx' ('type_id'),
  FOREIGN KEY ('category_id') REFERENCES 'categories' ('id_categories') ON UPDATE CASCADE,
  FOREIGN KEY ('payment_method_id') REFERENCES 'payment_methods' ('id') ON UPDATE CASCADE,
  FOREIGN KEY ('type_id') REFERENCES 'transaction_types' ('idtransaction_types') ON UPDATE CASCADE,
  FOREIGN KEY ('user_id') REFERENCES 'users' ('id') ON UPDATE CASCADE
) 


-- Table structure for table 'users'
--
CREATE TABLE 'users' (
  'id' INTEGER  PRIMARY  KEY AUTOINCREMENT,
  'login' TEXT NOT NULL,
  'password' TEXT NOT NULL,
  'name' TEXT NOT NULL,
  'last_name' TEXT NOT NULL,
  'email' TEXT NOT NULL,  
  UNIQUE KEY 'email_UNIQUE' ('email')
) 
