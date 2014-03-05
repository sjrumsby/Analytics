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

home_face_off_on_ice 	= 'CREATE TABLE "home_face_off_on_ice" ("id" integer NOT NULL PRIMARY KEY, "face_off_id" integer NOT NULL REFERENCES "face_off" ("id"), "skater_id" integer NOT NULL REFERENCES "skater" ("id") );'

away_face_off_on_ice 	= 'CREATE TABLE "away_face_off_on_ice" ("id" integer NOT NULL PRIMARY KEY, "face_off_id" integer NOT NULL REFERENCES "face_off" ("id"), "skater_id" integer NOT NULL REFERENCES "skater" ("id") );'

block_table				= 'CREATE TABLE "block" ("id" integer NOT NULL PRIMARY KEY, "shooter" integer NOT NULL REFERENCES skater ("id"), "blocker" integer NOT NULL REFERENCES skater ("id"), "shot_type_id" integer NOT NULL REFERENCES shot_type ("id"), "zone_type_id" integer NOT NULL REFERENCES zone_type ("id") );'

home_block_on_ice 		= 'CREATE TABLE "home_block_on_ice" ("id" integer NOT NULL PRIMARY KEY, "block_id" integer NOT NULL REFERENCES "block" ("id"), "skater_id" integer NOT NULL REFERENCES "skater" ("id") );'

away_block_on_ice 		= 'CREATE TABLE "away_block_on_ice" ("id" integer NOT NULL PRIMARY KEY, "block_id" integer NOT NULL REFERENCES "block" ("id"), "skater_id" integer NOT NULL REFERENCES "skater" ("id") );'

shot_table				= 'CREATE TABLE "shot" ("id" integer NOT NULL PRIMARY KEY, "shooter" integer NOT NULL REFERENCES skater ("id"), "shot_type_id" integer NOT NULL REFERENCES shot_type ("id"), "zone_type_id" integer NOT NULL REFERENCES zone_type ("id"), "distance" integer NOT NULL );'

home_shot_on_ice 		= 'CREATE TABLE "home_shot_on_ice" ("id" integer NOT NULL PRIMARY KEY, "shot_id" integer NOT NULL REFERENCES "shot" ("id"), "skater_id" integer NOT NULL REFERENCES "skater" ("id") );'

away_shot_on_ice 		= 'CREATE TABLE "away_shot_on_ice" ("id" integer NOT NULL PRIMARY KEY, "shot_id" integer NOT NULL REFERENCES "shot" ("id"), "skater_id" integer NOT NULL REFERENCES "skater" ("id") );'

hit_table				= 'CREATE TABLE "hit" ("id" integer NOT NULL PRIMARY KEY, "hitter" integer NOT NULL REFERENCES skater ("id"), "hittee" integer NOT NULL REFERENCES skater ("id"), "zone_type_id" integer NOT NULL REFERENCES "zone_type" ("id") );'

home_hit_on_ice 		= 'CREATE TABLE "home_hit_on_ice" ("id" integer NOT NULL PRIMARY KEY, "hit_id" integer NOT NULL REFERENCES "hit" ("id"), "skater_id" integer NOT NULL REFERENCES "skater" ("id") );'

away_hit_on_ice 		= 'CREATE TABLE "away_hit_on_ice" ("id" integer NOT NULL PRIMARY KEY, "hit_id" integer NOT NULL REFERENCES "hit" ("id"), "skater_id" integer NOT NULL REFERENCES "skater" ("id") );'

stop_table				= 'CREATE TABLE "stop" ("id" integer NOT NULL PRIMARY KEY, "stop_type_id" integer NOT NULL REFERENCES stop_type ("id") );'

home_stop_on_ice 		= 'CREATE TABLE "home_stop_on_ice" ("id" integer NOT NULL PRIMARY KEY, "stop_id" integer NOT NULL REFERENCES "stop" ("id"), "skater_id" integer NOT NULL REFERENCES "skater" ("id") );'

away_stop_on_ice 		= 'CREATE TABLE "away_stop_on_ice" ("id" integer NOT NULL PRIMARY KEY, "stop_id" integer NOT NULL REFERENCES "stop" ("id"), "skater_id" integer NOT NULL REFERENCES "skater" ("id") );'

miss_table				= 'CREATE TABLE "miss" ("id" integer NOT NULL PRIMARY KEY, "shooter" integer NOT NULL REFERENCES skater ("id"), "miss_type_id" integer NOT NULL REFERENCES miss_type ("id"), "shot_type_id" integer NOT NULL REFERENCES shot_type ("id"), "zone_type_id" integer NOT NULL REFERENCES zone_type ("id"), "distance" integer NOT NULL );'

home_miss_on_ice 		= 'CREATE TABLE "home_miss_on_ice" ("id" integer NOT NULL PRIMARY KEY, "miss_id" integer NOT NULL REFERENCES "miss" ("id"), "skater_id" integer NOT NULL REFERENCES "skater" ("id") );'

away_miss_on_ice 		= 'CREATE TABLE "away_miss_on_ice" ("id" integer NOT NULL PRIMARY KEY, "miss_id" integer NOT NULL REFERENCES "miss" ("id"), "skater_id" integer NOT NULL REFERENCES "skater" ("id") );'
