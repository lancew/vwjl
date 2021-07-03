CREATE TABLE competitions_athletes
  (
     id             SERIAL PRIMARY KEY,
     competition_id INTEGER NOT NULL,
     athlete_id     INTEGER NOT NULL,
     added_on       TIMESTAMP NOT NULL,
     unique(athlete_id, competition_id)
  )