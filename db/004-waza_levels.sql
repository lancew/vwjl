CREATE TABLE waza_level
  (
     id         SERIAL PRIMARY KEY,
     athlete_id INT NOT NULL,
     waza       varchar(100) NOT NULL,
     attack     INT DEFAULT 0,
     defence    INT DEFAULT 0,
     unique( athlete_id, waza )
  )
