CREATE TABLE competitions
  (
     id             SERIAL PRIMARY KEY,
     NAME           VARCHAR(100) UNIQUE NOT NULL,
     description    TEXT,
     owner_username VARCHAR(50) NOT NULL,
     entry_fee      INTEGER DEFAULT 1,
     created_on     TIMESTAMP NOT NULL
  ) 
