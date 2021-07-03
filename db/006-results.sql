CREATE TABLE results
  (
     id            SERIAL PRIMARY KEY,
     competition   INT,
     round         INT,
     winner        varchar(100),
     loser         varchar(100),
     scoreboard_id INT,
     commentary    TEXT
  );