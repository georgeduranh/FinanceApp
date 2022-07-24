DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS payment_methods;
DROP TABLE IF EXISTS transaction_types;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS users;

--
-- Table structure for table categories
--
CREATE TABLE categories (
  id_categories INTEGER  PRIMARY  KEY  AUTOINCREMENT,
  category TEXT DEFAULT NULL,
  user_id INTEGER  NOT NULL,
  FOREIGN KEY (user_id)
  REFERENCES users (id)  
  ON UPDATE CASCADE
);


-- Table structure for table payment_methods
--
CREATE TABLE payment_methods (
  id INTEGER  PRIMARY  KEY AUTOINCREMENT,
  payment_method TEXT NOT NULL,
  user_id INTEGER  NOT NULL,  
  FOREIGN KEY (user_id)
  REFERENCES users (id)  
  ON UPDATE CASCADE
) ;

-- Table structure for table transaction_types
--
CREATE TABLE transaction_types (
  id INTEGER  PRIMARY  KEY AUTOINCREMENT,
  transaction_type TEXT DEFAULT NULL,
  user_id INTEGER  NOT NULL,
  FOREIGN KEY (user_id)
  REFERENCES users (id)  
  ON UPDATE CASCADE 
) ;

--
-- Table structure for table transactions
--
CREATE TABLE transactions (
  id INTEGER  PRIMARY  KEY AUTOINCREMENT,
  registered_time TIMESTAMP  NOT NULL DEFAULT CURRENT_TIMESTAMP,
  date_tx datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  description TEXT NOT NULL,
  is_paid BOOLEAN  NOT NULL DEFAULT 'False',
  user_id INTEGER  NOT NULL,
  amount float  NOT NULL,
  category_id INTEGER  NOT NULL,
  payment_method_id INTEGER  NOT NULL,
  type_id INTEGER  NOT NULL,
  FOREIGN KEY (user_id)  REFERENCES users (id)  ON UPDATE CASCADE,  
  FOREIGN KEY (category_id) REFERENCES categories (id_categories) ON UPDATE CASCADE,
  FOREIGN KEY (payment_method_id) REFERENCES payment_methods (id) ON UPDATE CASCADE,
  FOREIGN KEY (type_id) REFERENCES transaction_types (idtransaction_types) ON UPDATE CASCADE
  
) ;

CREATE TABLE users (
  id INTEGER  PRIMARY  KEY AUTOINCREMENT,
  login TEXT NOT NULL,
  password TEXT NOT NULL,
  name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE
) 


CREATE TABLE buget (
  id INTEGER  PRIMARY  KEY AUTOINCREMENT,  
  amount_budget float  NOT NULL,
  type_budget_id INT  NOT NULL,
  user_id INTEGER  NOT NULL,
  category_id INTEGER  NOT NULL,    
  FOREIGN KEY (user_id)  REFERENCES users (id)  ON UPDATE CASCADE,  
  FOREIGN KEY (type_budget_id) REFERENCES type_budget (id) ON UPDATE CASCADE  
) ;

CREATE TABLE type_budget (
  id INTEGER  PRIMARY  KEY AUTOINCREMENT,  
  type_expense TEXT  NOT NULL,
  user_id INTEGER  NOT NULL,
  FOREIGN KEY (buget_id)  REFERENCES buget (id)  ON UPDATE CASCADE, 
  FOREIGN KEY (user_id)  REFERENCES users (id)  ON UPDATE CASCADE,    
) ;