hockey_team_table 		= 'CREATE TABLE "hockey_team" ("id" integer NOT NULL PRIMARY KEY, "name" varchar(3) NOT NULL, "long_name" varchar(64) NOT NULL );'

skater_table 			= 'CREATE TABLE "skater" ("id" integer NOT NULL PRIMARY KEY, "nhl_id" integer NOT NULL, "name" varchar(64) NOT NULL, "hockey_team_id" integer NOT NULL REFERENCES "hockey_team" ("id"), "position" varchar(2) NOT NULL );'

miss_type_table 		= 'CREATE TABLE "miss_types" ("id" integer NOT NULL PRIMARY KEY, "name" varchar(16) NOT NULL );'

penalty_type_table 		= 'CREATE TABLE "penalty_types" ("id" integer NOT NULL PRIMARY KEY, "name" varchar(64) NOT NULL );'

play_type_table 		= 'CREATE TABLE "play_types" ("id" integer NOT NULL PRIMARY KEY, "name" varchar(8) NOT NULL );'

shot_type_table 		= 'CREATE TABLE "shot_types" ("id" integer NOT NULL PRIMARY KEY, "name" varchar(16) NOT NULL );'

stop_type_table 		= 'CREATE TABLE "stop_types" ("id" integer NOT NULL PRIMARY KEY, "name" varchar(16) NOT NULL );'

zone_type_table 		= 'CREATE TABLE "zone_types" ("id" integer NOT NULL PRIMARY KEY, "name" varchar(16) NOT NULL );'

strength_type_table 	= 'CREATE TABLE "strength_types" ("id" integer NOT NULL PRIMARY KEY, "name" varchar(16) NOT NULL);'

game_table 				= 'CREATE TABLE "game" ("id" integer NOT NULL PRIMARY KEY, "season_code" varchar(4), "year_code" varchar(16), "game_code" varchar(8), "home_team_id" integer NOT NULL REFERENCES "hockey_team" ("id"), "away_team_id" integer NOT NULL REFERENCES "hockey_team" ("id"), "start_time" varchar(16) NOT NULL, "end_time" varchar(16) NOT NULL, attendance integer NOT NULL);'

star_table 				= 'CREATE TABLE "stars" ("id" integer NOT NULL PRIMARY KEY, "game_id" integer NOT NULL REFERENCES "game" ("id"), "first_id" integer REFERENCES "skater" ("id"), "second_id" integer REFERENCES "skater" ("id"), "third_id" integer REFERENCES "skater" ("id") );'

team_table 				= 'CREATE TABLE "team" ("id" integer NOT NULL PRIMARY KEY, "skater_id" integer NOT NULL REFERENCES "skater" ("id"), "game_id" integer NOT NULL REFERENCES "game" ("id"), "number" integer NOT NULL, "hockey_team_id" NOT NULL REFERENCES "hockey_team" ("id") ); '

play_table				= 'CREATE TABLE "play" ("id" integer NOT NULL PRIMARY KEY, "game_id" integer NOT NULL REFERENCES "game" ("id"), "event_id" integer NOT NULL REFERENCES "play_type" ("id"), "period" integer NOT NULL, "time" varchar(16) NOT NULL, "strength_id" REFERENCES "strength_types" ("id") );'

face_off_table			= 'CREATE TABLE "face_off" ("id" integer NOT NULL PRIMARY KEY, "winner" integer NOT NULL REFERENCES "skater" ("id"), "loser" integer NOT NULL REFERENCES "skater" ("id"), "zone_id" integer NOT NULL REFERENCES "zone_types" ("id") );'

home_face_off_on_ice 	= 'CREATE TABLE "home_face_off_on_ice" ("id" integer NOT NULL PRIMARY KEY, "face_off_id" NOT NULL REFERENCES "face_off" ("id"), "team_id" NOT NULL REFERENCES "team" ("id") );'

away_face_off_on_ice 	= 'CREATE TABLE "away_face_off_on_ice" ("id" integer NOT NULL PRIMARY KEY, "face_off_id" NOT NULL REFERENCES "face_off" ("id"), "team_id" NOT NULL REFERENCES "team" ("id") );'
