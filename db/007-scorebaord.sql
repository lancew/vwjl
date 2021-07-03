CREATE TABLE scoreboard
  (
     id            SERIAL PRIMARY KEY,
     result_id     INT,
     clock_minutes INT,
     clock_seconds INT,
     white_athlete varchar(100),
     white_ippon   INT,
     white_wazari  INT,
     white_shido   INT,
     blue_athlete  varchar(100),
     blue_ippon    INT,
     blue_wazari   INT,
     blue_shido    INT
  );