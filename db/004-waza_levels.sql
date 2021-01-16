CREATE TABLE waza_level
  (
     id         SERIAL PRIMARY KEY,
     athlete_id INT NOT NULL,
     waza       VARCHAR(100) NOT NULL,
     attack     INT DEFAULT 0,
     defence    INT DEFAULT 0,
     UNIQUE( athlete_id, waza )
  ) 
