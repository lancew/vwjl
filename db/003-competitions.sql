CREATE TABLE competitions
  (
     id             SERIAL PRIMARY KEY,
     name           varchar(100) UNIQUE NOT NULL,
     description    TEXT,
     owner_username varchar(50) NOT NULL,
     entry_fee      INTEGER DEFAULT 1,
     created_on     TIMESTAMP NOT NULL
  )
