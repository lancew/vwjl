CREATE TABLE accounts
  (
     user_id    SERIAL PRIMARY KEY,
     username   VARCHAR (50) UNIQUE NOT NULL,
     passphrase VARCHAR (150) NOT NULL,
     created_on TIMESTAMP NOT NULL,
     last_login TIMESTAMP
  ); 