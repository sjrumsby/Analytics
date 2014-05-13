import sys
from django.db import models

try:
    from django.db import models
except Exception:
    print "There was an error loading django modules. Do you have django installed?"
    sys.exit()

class Hockey_Team(models.Model):
	name            = models.CharField(max_length=3)
	full_name       = models.CharField(max_length=24)

	def __unicode__(self):
		return self.name

class Game(models.Model):
	date            = models.DateField()
	home_team       = models.ForeignKey(Hockey_Team, related_name="home_team")
	away_team       = models.ForeignKey(Hockey_Team, related_name="away_team")
	start_time      = models.TimeField()
	end_time		= models.TimeField()
	season_id		= models.IntegerField(max_length=10)
	year_id			= models.IntegerField(max_length=10)
	game_id			= models.IntegerField(max_length=10)
	home_score		= models.IntegerField(max_length=2)
	away_score		= models.IntegerField(max_length=2)
	attendance		= models.IntegerField(max_length=6)
	
class Skater(models.Model):
	nhl_id          = models.IntegerField(max_length=8)
	name            = models.CharField(max_length=64, default="")
	hockey_team     = models.ForeignKey(Hockey_Team, default=0)
	position        = models.CharField(max_length=2, default="")
	games           = models.IntegerField(max_length=8, default=0)
	goals           = models.IntegerField(max_length=8, default=0)
	assists         = models.IntegerField(max_length=8, default=0)
	points          = models.IntegerField(max_length=8, default=0)
	plus_minus      = models.IntegerField(max_length=4, default=0)
	shg             = models.IntegerField(max_length=8, default=0)
	sha             = models.IntegerField(max_length=8, default=0)
	ppg             = models.IntegerField(max_length=8, default=0)
	ppa             = models.IntegerField(max_length=8, default=0)
	gwg             = models.IntegerField(max_length=8, default=0)
	psg             = models.IntegerField(max_length=8, default=0)
	pims            = models.IntegerField(max_length=8, default=0)
	hits            = models.IntegerField(max_length=8, default=0)
	shots           = models.IntegerField(max_length=8, default=0)
	blocks          = models.IntegerField(max_length=8, default=0)
	fights          = models.IntegerField(max_length=8, default=0)
	giveaways       = models.IntegerField(max_length=8, default=0)
	takeaways       = models.IntegerField(max_length=8, default=0)
	faceoff_win     = models.IntegerField(max_length=8, default=0)
	faceoff_loss    = models.IntegerField(max_length=8, default=0)
	shootout_made   = models.IntegerField(max_length=8, default=0)
	shootout_fail   = models.IntegerField(max_length=8, default=0)
	wins            = models.IntegerField(max_length=8, default=0)
	otloss          = models.IntegerField(max_length=8, default=0)
	shutouts        = models.IntegerField(max_length=8, default=0)
	penshot_save    = models.IntegerField(max_length=8, default=0)
	penshot_ga      = models.IntegerField(max_length=8, default=0)
	shootout_save   = models.IntegerField(max_length=8, default=0)
	shootout_ga     = models.IntegerField(max_length=8, default=0)
	saves           = models.IntegerField(max_length=8, default=0)
	goals_against   = models.IntegerField(max_length=8, default=0)

	def __unicode__(self):
		return self.name

class Miss_Type(models.Model):
	name 			= models.CharField(max_length=32, default='')

class Penalty_Type(models.Model):
	name 			= models.CharField(max_length=32, default='')

class Play_Type(models.Model):
	name 			= models.CharField(max_length=32, default='')

class Shot_Type(models.Model):
	name 			= models.CharField(max_length=32, default='')

class Stop_Type(models.Model):
	name 			= models.CharField(max_length=32, default='')

class Strength_Type(models.Model):
	name 			= models.CharField(max_length=32, default='')

class Zone_Type(models.Model):
	name 			= models.CharField(max_length=32, default='')

class Stars(models.Model):
	game 			= models.ForeignKey(Game)
	first_star		= models.ForeignKey(Skater, related_name="first_star",null=True)
	second_star 	= models.ForeignKey(Skater, related_name="second_star",null=True)
	third_star		= models.ForeignKey(Skater, related_name="third_star",null=True)

class Team(models.Model):
	skater			= models.ForeignKey(Skater)
	game 			= models.ForeignKey(Game)
	hockey_team 	= models.ForeignKey(Hockey_Team)
	number			= models.IntegerField(max_length=3)
	
class Play(models.Model):
	game			= models.ForeignKey(Game)
	time			= models.TimeField()
	event			= models.ForeignKey(Play_Type)
	strength		= models.ForeignKey(Strength_Type,null=True)
	period			= models.IntegerField(max_length=3)
	zone			= models.ForeignKey(Zone_Type,null=True)
	
class Face_Off(models.Model):
	play 			= models.ForeignKey(Play)
	winner			= models.ForeignKey(Skater, related_name="winner")
	loser			= models.ForeignKey(Skater, related_name="loser")
	
class Home_Face_Off_On_Ice(models.Model):
	Face_Off		= models.ForeignKey(Face_Off)
	skater			= models.ForeignKey(Skater)

class Away_Face_Off_On_Ice(models.Model):
	Face_Off		= models.ForeignKey(Face_Off)
	skater			= models.ForeignKey(Skater)

class Block(models.Model):
	play 			= models.ForeignKey(Play)
	shooter			= models.ForeignKey(Skater, related_name="shooter")
	blocker			= models.ForeignKey(Skater, related_name="blocker")
	shot_type		= models.ForeignKey(Shot_Type)

class Home_Block_On_Ice(models.Model):
	Face_Off		= models.ForeignKey(Block)
	skater			= models.ForeignKey(Skater)

class Away_Block_On_Ice(models.Model):
	Face_Off		= models.ForeignKey(Block)
	skater			= models.ForeignKey(Skater)

class Shot(models.Model):
	play 			= models.ForeignKey(Play)
	shooter			= models.ForeignKey(Skater)
	shot_type		= models.ForeignKey(Shot_Type)
	distance		= models.IntegerField(max_length=3)

class Home_Shot_On_Ice(models.Model):
	Face_Off		= models.ForeignKey(Shot)
	skater			= models.ForeignKey(Skater)

class Away_Shot_On_Ice(models.Model):
	Face_Off		= models.ForeignKey(Shot)
	skater			= models.ForeignKey(Skater)

class Hit(models.Model):
	play 			= models.ForeignKey(Play)
	hitter			= models.ForeignKey(Skater, related_name="hitter")
	hittee			= models.ForeignKey(Skater, related_name="hittee")

class Home_Hit_On_Ice(models.Model):
	Face_Off		= models.ForeignKey(Hit)
	skater			= models.ForeignKey(Skater)

class Away_Hit_On_Ice(models.Model):
	Face_Off		= models.ForeignKey(Hit)
	skater			= models.ForeignKey(Skater)

class Stop(models.Model):
	play 			= models.ForeignKey(Play)
	stop_type		= models.ForeignKey(Stop_Type)

class Home_Stop_On_Ice(models.Model):
	Face_Off		= models.ForeignKey(Stop)
	skater			= models.ForeignKey(Skater)

class Away_Stop_On_Ice(models.Model):
	Face_Off		= models.ForeignKey(Stop)
	skater			= models.ForeignKey(Skater)

class Miss(models.Model):
	play 			= models.ForeignKey(Play)
	shooter			= models.ForeignKey(Skater)
	miss_type		= models.ForeignKey(Miss_Type)
	shot_type		= models.ForeignKey(Shot_Type)

class Home_Miss_On_Ice(models.Model):
	Face_Off		= models.ForeignKey(Miss)
	skater			= models.ForeignKey(Skater)

class Away_Miss_On_Ice(models.Model):
	Face_Off		= models.ForeignKey(Miss)
	skater			= models.ForeignKey(Skater)

class Goal(models.Model):
	play 			= models.ForeignKey(Play)
	scorer			= models.ForeignKey(Skater, related_name="scorer")
	first_assist	= models.ForeignKey(Skater, related_name="first_assist")
	second_assist	= models.ForeignKey(Skater, related_name="second_assist")

class Home_Goal_On_Ice(models.Model):
	Face_Off		= models.ForeignKey(Goal)
	skater			= models.ForeignKey(Skater)

class Away_Goal_On_Ice(models.Model):
	Face_Off		= models.ForeignKey(Goal)
	skater			= models.ForeignKey(Skater)

class Giveaway(models.Model):
	play 			= models.ForeignKey(Play)
	giver			= models.ForeignKey(Skater)

class Home_Giveaway_On_Ice(models.Model):
	Face_Off		= models.ForeignKey(Giveaway)
	skater			= models.ForeignKey(Skater)

class Away_Giveaway_On_Ice(models.Model):
	Face_Off		= models.ForeignKey(Giveaway)
	skater			= models.ForeignKey(Skater)

class Takeaway(models.Model):
	play 			= models.ForeignKey(Play)
	taker			= models.ForeignKey(Skater)

class Home_Takeaway_On_Ice(models.Model):
	Face_Off		= models.ForeignKey(Takeaway)
	skater			= models.ForeignKey(Skater)

class Away_Takeaway_On_Ice(models.Model):
	Face_Off		= models.ForeignKey(Takeaway)
	skater			= models.ForeignKey(Skater)
	
class Period_Start(models.Model):
	time = models.TimeField()
	
class Home_Period_Start_On_Ice(models.Model):
	Face_Off		= models.ForeignKey(Period_Start)
	skater			= models.ForeignKey(Skater)

class Away_Period_Start_On_Ice(models.Model):
	Face_Off		= models.ForeignKey(Period_Start)
	skater			= models.ForeignKey(Skater)

class Period_End(models.Model):
	time = models.TimeField()

class Home_Period_End_On_Ice(models.Model):
	Face_Off		= models.ForeignKey(Period_End)
	skater			= models.ForeignKey(Skater)

class Away_Period_End_On_Ice(models.Model):
	Face_Off		= models.ForeignKey(Period_End)
	skater			= models.ForeignKey(Skater)