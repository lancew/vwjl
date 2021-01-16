CREATE TABLE athletes
  (
     id                           SERIAL PRIMARY KEY,
     username                     VARCHAR(50) UNIQUE NOT NULL,
     biography                    TEXT,
     country                      VARCHAR(100),
     credits                      INTEGER DEFAULT 100,
     dojo                         VARCHAR(100),
     left_arm_fatigue             INTEGER DEFAULT 1,
     left_arm_injury              INTEGER DEFAULT 1,
     left_arm_strength            INTEGER DEFAULT 1,
     left_leg_fatigue             INTEGER DEFAULT 1,
     left_leg_injury              INTEGER DEFAULT 1,
     left_leg_strength            INTEGER DEFAULT 1,
     losses                       INTEGER DEFAULT 0,
     NAME                         VARCHAR(100),
     physical_fatigue             INTEGER DEFAULT 1,
     physical_fitness             INTEGER DEFAULT 1,
     physical_form                INTEGER DEFAULT 1,
     right_arm_fatigue            INTEGER DEFAULT 1,
     right_arm_injury             INTEGER DEFAULT 1,
     right_arm_strength           INTEGER DEFAULT 1,
     right_leg_fatigue            INTEGER DEFAULT 1,
     right_leg_injury             INTEGER DEFAULT 1,
     right_leg_strength           INTEGER DEFAULT 1,
     sensei                       VARCHAR(100),
     waza_ippon_seoi_nage_attack  INTEGER DEFAULT 1,
     waza_ippon_seoi_nage_defense INTEGER DEFAULT 1,
     waza_uchi_mata_attack        INTEGER DEFAULT 1,
     waza_uchi_mata_defense       INTEGER DEFAULT 1,
     weight                       DECIMAL,
     wins                         INTEGER DEFAULT 0
  ) 