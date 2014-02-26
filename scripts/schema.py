hockey_team_tbl = 'CREATE TABLE "hockey_team" ("id" integer NOT NULL PRIMARY KEY, "name" varchar(3) NOT NULL, "long_name" varchar(64) NOT NULL );'

skat_tbl = 'CREATE TABLE "skater" ("id" integer NOT NULL PRIMARY KEY, "nhl_id" integer NOT NULL, "name" varchar(64) NOT NULL, "hockey_team_id" integer NOT NULL REFERENCES "hockey_team" ("id"), "position" varchar(2) NOT NULL );'

miss_tbl = 'CREATE TABLE "miss_types" ("id" integer NOT NULL PRIMARY KEY, "name" varchar(16) NOT NULL );'

penl_tbl = 'CREATE TABLE "penalty_types" ("id" integer NOT NULL PRIMARY KEY, "name" varchar(64) NOT NULL );'

play_tbl = 'CREATE TABLE "play_types" ("id" integer NOT NULL PRIMARY KEY, "name" varchar(8) NOT NULL );'

shot_tbl = 'CREATE TABLE "shot_types" ("id" integer NOT NULL PRIMARY KEY, "name" varchar(16) NOT NULL );'

stop_tbl = 'CREATE TABLE "stop_types" ("id" integer NOT NULL PRIMARY KEY, "name" varchar(16) NOT NULL );'

zone_tbl = 'CREATE TABLE "zone_types" ("id" integer NOT NULL PRIMARY KEY, "name" varchar(16) NOT NULL );'

game_tbl = 'CREATE TABLE "game" ("id" integer NOT NULL PRIMARY KEY, "season_code" varchar(4), "year_code" varchar(16), "game_code" varchar(8), "home_team_id" integer NOT NULL REFERENCES "hockey_team" ("id"), "away_team_id" integer NOT NULL REFERENCES "hockey_team" ("id"), "start_time" varchar(16) NOT NULL, "end_time" varchar(16) NOT NULL, attendance integer NOT NULL);'

star_tbl = 'CREATE TABLE "stars" ("id" integer NOT NULL PRIMARY KEY, "game_id" integer NOT NULL REFERENCES "game" ("id"), "first_id" integer NOT NULL REFERENCES "skater" ("id"), "second_id" integer NOT NULL REFERENCES "skater" ("id"), "third_id" integer NOT NULL REFERENCES "skater" ("id") );'

team_tbl = 'CREATE TABLE "team" ("id" integer NOT NULL PRIMARY KEY, "skater_id" integer NOT NULL REFERENCES "skater" ("id"), "game_id" integer NOT NULL REFERENCES "game" ("id"), "number" integer NOT NULL, "hockey_team_id" NOT NULL REFERENCES "hockey_team" ("id") ); '