CREATE TABLE results
  (
     id            SERIAL PRIMARY KEY,
     competition   INT,
     round         INT,
     winner        VARCHAR(100),
     loser         VARCHAR(100),
     scoreboard_id INT,
     commentary    TEXT
  ); 