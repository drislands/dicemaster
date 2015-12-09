## TODO: CHANGE players TO HAVE CurrentDuel point DuelID in duels
## TODO: CHANGE duels SO THAT ALL THE NAMES ARE INSTEAD IDs
##


## STAGES OF COMBAT, SO FAR
# 1:	to hit!
# 2:	to defend!
# 3:	to damage!
# 4:	to riposte!
# 5:	to stun!

from sopel import module
import MySQLdb
import re
import random
import os

# whether or not to show the dexterity and strength rolls
showHiddenRolls = True

# connect to the data base, and create a cursor with which to execute queries
db = MySQLdb.connect(host="localhost",user="dicebot",passwd="megadicebot",db="dicebot")
cur = db.cursor()

#function to make sure that the db is still connected
def testDB(myDB,myCur):
	try:
		myCur.execute('SELECT * FROM players;')
	except (AttributeError, MySQLdb.OperationalError):
		myDB = MySQLdb.connect(host="localhost",user="dicebot",passwd="megadicebot",db="dicebot")

# set the correct profile
cur.execute('SELECT currentP FROM currentprofile WHERE ph=1');
curProfile = cur.fetchone()[0]

# stats are: ATTack, DEFense, HP, STRength, DEXterity,
# minimum values for each stat at char creation
minAtt = 0
minDef = 0
minHP = 0
minStr = 0
minDex = 0
# maximum values for each stat at char creation
maxAtt = 0
maxDef = 0
maxHP = 0
maxStr = 0
maxDex = 0
# number of sides to the dice for each stat
hitDie = 0
defDie = 0
attDie = 0
strDie = 0
dexDie = 0
# threshold for success for each stat die
hitThr = 0
defThr = 0
attThr = 0
strThr = 0
dexThr = 0
# whether or not doubles are counted for a stat
dubHit = 0
dubDef = 0
dubAtt = 0
dubStr = 0
dubDex = 0
# threshold at which a die counts for double
duHiTh = 0
duDfTh = 0
duAtTh = 0
duStTh = 0
duDxTh = 0
# whether or not crit failures are counted
negHit = 0
negDef = 0
negAtt = 0
negStr = 0
negDex = 0
# threshold at whgich a die counts as a crit fail
neHiTh = 0
neDfTh = 0
neAtTh = 0
neStTh = 0
neDxTh = 0
# how many boosts you get for losing/winning
winBoosts = 0
loseBoosts = 0
# how many points a stat is boosted per boost
boostVal = 0
# how many rerolls you get for losing/winning
winRerolls = 0
loseRerolls = 0
# exchange rate between rerolls and stat boosts
rollBoostRate = 0
boostToRoll = 0

def setProfile(profile):
	testDB(db,cur)
	cur.execute('SELECT * FROM variableprofiles WHERE name=\'%s\'' % profile)
	varStats = cur.fetchone()
	# TODO: LOOK INTO HASHES
	# this line is a mess lol. can't think of any other way to do this though
	global minAtt,minDef,minHP,minStr,minDex,maxAtt,maxDef,maxHP,maxStr,maxDex,hitDie,defDie,attDie,strDie,dexDie,hitThr,defThr,attThr,strThr,dexThr,dubHit,dubDef,dubAtt,dubStr,dubDex,duHiTh,duDfTh,duAtTh,duStTh,duDxTh,negHit,negDef,negAtt,negStr,negDex,neHiTh,neDfTh,neAtTh,neStTh,neDxTh,winBoosts,loseBoosts,boostVal,winRerolls,loseRerolls,rollBoostRate,boostToRoll
	## stat variables
	minAtt = varStats[1]
	minDef = varStats[2]
	minHP  = varStats[3]
	minStr = varStats[4]
	minDex = varStats[5]
	maxAtt = varStats[6]
	maxDef = varStats[7]
	maxHP  = varStats[8]
	maxStr = varStats[9]
	maxDex = varStats[10]
	## Dice variables
	# sides on the 3 types of dice
	hitDie = varStats[11]
	defDie = varStats[12]
	attDie = varStats[13]
	strDie = varStats[14]
	dexDie = varStats[15]
	# threshold for success
	hitThr = varStats[16]
	defThr = varStats[17]
	attThr = varStats[18]
	strThr = varStats[19]
	dexThr = varStats[20]
	# whether or not max counts for double
	dubHit = varStats[21]
	dubDef = varStats[22]
	dubAtt = varStats[23]
	dubStr = varStats[24]
	dubDex = varStats[25]
	# threshold for doubles
	duHiTh = varStats[26]
	duDfTh = varStats[27]
	duAtTh = varStats[28]
	duStTh = varStats[29]
	duDxTh = varStats[30]
	# whether or not 1 counts against you
	negHit = varStats[31]
	negDef = varStats[32]
	negAtt = varStats[33]
	negStr = varStats[34]
	negDex = varStats[35]
	# threshold for negatives
	neHiTh = varStats[36]
	neDfTh = varStats[37]
	neAtTh = varStats[38]
	neStTh = varStats[39]
	neDxTh = varStats[40]
	## boost stats
	# boost points gained per win/loss
	winBoosts = varStats[41]
	loseBoosts = varStats[42]
	boostVal = varStats[43]
	# rerolls gained per win/loss
	winRerolls = varStats[44]
	loseRerolls = varStats[45]
	# how many boosts per roll
	rollBoostRate = varStats[46]
	# how many rolls per boost
	boostToRoll = varStats[47]

# set the current profile to the default one specified in the database
setProfile(curProfile)
# defining regularly used queries as functions
def getAtt(name):
	testDB(db,cur)
	cur.execute('SELECT attack FROM players WHERE name=\'%s\'' % name)
	return cur.fetchone()[0]
def getDef(name):
	testDB(db,cur)
	cur.execute('SELECT defense FROM players WHERE name=\'%s\'' % name)
	return cur.fetchone()[0]
def getStr(name):
	testDB(db,cur)
	cur.execute('SELECT strength FROM players WHERE name=\'%s\'' % name)
	return cur.fetchone()[0]
def getDex(name):
	testDB(db,cur)
	cur.execute('SELECT dexterity FROM players WHERE name=\'%s\'' % name)
	return cur.fetchone()[0]
def getID(name):
	testDB(db,cur)
	cur.execute('SELECT ID FROM players WHERE name=\'%s\'' % name)
	return cur.fetchone()[0]
def getName(ID):
	testDB(db,cur)
	cur.execute('SELECT name FROM players WHERE id=%s' % ID)
	return cur.fetchone()[0]
def getMaxHP(name):
	testDB(db,cur)
	cur.execute('SELECT maxhp FROM players WHERE name=\'%s\'' % name)
	return cur.fetchone()[0]
def getCurHP(name):
	testDB(db,cur)
	cur.execute('SELECT curhp FROM players WHERE name=\'%s\'' % name)
	return cur.fetchone()[0]
def getActive(name):
	testDB(db,cur)
	cur.execute('SELECT active FROM players WHERE name=\'%s\'' % name)
	return cur.fetchone()[0]
def doesExist(name):
	testDB(db,cur)
	cur.execute('SELECT * FROM players WHERE name=\'%s\'' % name)
	return cur.fetchone()
def getBoosts(name):
	testDB(db,cur)
	cur.execute('SELECT Boosts FROM players WHERE name=\'%s\'' % name)
	return cur.fetchone()[0]
def getUsedBoosts(name):
	testDB(db,cur)
	cur.execute('SELECT Used_Boosts FROM players WHERE name=\'%s\'' % name)
	return cur.fetchone()[0]
def getRerolls(name):
	testDB(db,cur)
	cur.execute('SELECT Rerolls FROM players WHERE name=\'%s\'' % name)
	return cur.fetchone()[0]
def getUsedRerolls(name):
	testDB(db,cur)
	cur.execute('SELECT Used_Rerolls FROM players WHERE name=\'%s\'' % name)
	return cur.fetchone()[0]
def getCurrentDuel(name):
	testDB(db,cur)
	cur.execute('SELECT CurrentDuel FROM players WHERE name=\'%s\'' % name)
	return cur.fetchone()[0]
def getStatus(name):
	testDB(db,cur)
	cur.execute('SELECT Status FROM players WHERE name=\'%s\'' % name)
	return cur.fetchone()[0]

#### defining more complicated functions that involve queries
# Creates a player with the name of the user who called it, and random stats
@module.commands('createplayer')
def createPlayer(bot, trigger):
	testDB(db,cur)
	if doesExist(trigger.nick):
		bot.reply('Your player already exists!')
	else:
		# generate stats based on variables set above
		att = random.randint(minAtt,maxAtt)
		defense = random.randint(minDef,maxDef)
		hp = random.randint(minHP,maxHP)
		strength = random.randint(minStr,maxStr)
		dex = random.randint(minDex,maxDex)
		# ID (auto generated), Active, Name, Attack, Defense, MaxHP, Current HP, boosts, used boosts, rerolls, used rerolls
		cur.execute('INSERT INTO players VALUES(NULL,0,\'%s\',%s,%s,%s,%s,%s,%s,0,0,0,0,NULL,\'healthy\')' % (trigger.nick,att,defense,strength,dex,hp,hp))
		bot.reply('Your character is created! Your max hp is %s, you have %s attack dice and %s defense dice, you have %s strength dice and %s dexterity dice, and you are listed as player %s. Game on!' % (hp,att,defense,strength,dex,getID(trigger.nick)))
		db.commit()

# Check Stats
@module.commands('stats')
def getStats(bot, trigger):
	testDB(db,cur)
	if not trigger.group(2):
		if not doesExist(trigger.nick):
			bot.reply('Your player needs to exist first! Say \'.createplayer\' to get started.')
		else:
			cur.execute('SELECT * FROM players WHERE name=\'%s\'' % trigger.nick)
			results = cur.fetchone()
			bot.reply('Your Attack is %s, Defense is %s, Strength is %s, Dexterity is %s, and you have %s/%sHP.' % (results[3],results[4],results[5],results[6],results[8],results[7]))
			bot.reply('You have used %s Boost points and have %s remaining Boost points to spend.' % (results[10],results[9]))
			bot.reply('You have used %s stat Rerolls and have %s remaining stat Rerolls.' % (results[12],results[11]))
			cur.execute('SELECT * FROM duels WHERE duelid=%s', (getCurrentDuel(trigger.nick),))
			results = cur.fetchone()
			if results:
				if results[0]==getID(trigger.nick):
					opponent = results[1]
					if results[2]:
						bot.reply('You are currently in a duel with %s.' % opponent)
					else:
						bot.reply('You currently are awaiting %s for a response to your challenge.' % opponent)
				else:
					opponent = results[0]
					if results[2]:
						bot.reply('You are currently in a duel with %s.' % opponent)
					else:
						bot.reply('%s is currently awaiting your acceptance of their challenge.' % opponent)
			else:
				bot.reply('You are not currently in, or waiting on, a duel.')
	else:
		if not doesExist(trigger.group(2)):
			bot.reply('Sorry, %s isn\'t an existing player.' % trigger.group(2))
		else:
			cur.execute('SELECT * FROM players WHERE name=\'%s\'' % trigger.group(2))
			results = cur.fetchone()
			bot.reply('The stats for the player %s are as follows:' % trigger.group(2))
			bot.reply('Attack is %s, Defense is %s, Strength is %s, Dexterity is %s, and %s/%sHP.' % (results[3],results[4],results[5],results[6],results[8],results[7]))
			bot.reply('They have used %s Boost points and have %s remaining Boost points to spend.' % (results[10],results[9]))
			bot.reply('They have used %s stat Rerolls and have %s remaining stat Rerolls.' % (results[12],results[11]))
			cur.execute('SELECT * FROM duels WHERE duelid=%s', (getCurrentDuel(trigger.group(2)),))
			results = cur.fetchone()
			if results:
				if results[0]==getID(trigger.group(2)):
					opponent = results[1]
					if opponent==getID(trigger.nick):
						opponent = 'you'
					if results[2]:
						bot.reply('They are currently in a duel with %s.' % opponent)
					else:
						bot.reply('They currently are awaiting %s for a response to their challenge.' % opponent)
				else:
					opponent = results[0]
					if opponent==getID(trigger.nick):
						opponent = 'you'
					if results[2]:
						bot.reply('They are currently in a duel with %s.' % opponent)
					else:
						if opponent=='you':
							bot.reply('You are currently awaiting their acceptance of your challenge.')
						else:
							bot.reply('%s is currently awaiting their acceptance of their challenge.' % opponent)
			else:
				bot.reply('They are not currently in, or waiting on, a duel.')


# Quick stats
@module.commands('qstats')
def getQuickStats(bot, trigger):
	testDB(db,cur)
	if not doesExist(trigger.nick):
		bot.reply('Your player needs to exist first! Say \'.createplayer\' to get started.')
	else:
		cur.execute('SELECT * FROM players WHERE name=\'%s\'' % trigger.nick)
		results = cur.fetchone()
		bot.reply('Att: %s' % results[3])
		bot.reply('Def: %s' % results[4])
		bot.reply('Str: %s' % results[5])
		bot.reply('Dex: %s' % results[6])
		bot.reply('HP: %s/%s' % (results[8],results[7]))

# Reroll your stats
@module.commands('reroll')
def rerollStats(bot, trigger):
	testDB(db,cur)
	if not doesExist(trigger.nick):
		bot.reply('Your player needs to exist first! Say \'.createplayer\' to get started.')
	elif getRerolls(trigger.nick) < 1:
		bot.reply('You don\'t have any stat rerolls remaining!')
	else:
		# generate new stats based on variables set above
		att = random.randint(minAtt,maxAtt)
		defense = random.randint(minDef,maxDef)
		hp = random.randint(minHP,maxHP)
		strength = random.randint(minStr,maxStr)
		dex = random.randint(minDex,maxDex)
		# remove one reroll and increment the UsedRerolls stat
		cur.execute('UPDATE players SET attack=%s,defense=%s,strength=%s,dexterity=%s,maxhp=%s,curhp=%s,rerolls=rerolls-1,used_rerolls=used_rerolls+1 WHERE name=\'%s\'' % (att,defense,strength,dex,hp,hp,trigger.nick))
		bot.reply('You have used one reroll and have %s remaining. You have used %s reroll(s) total.' % (getRerolls(trigger.nick),getUsedRerolls(trigger.nick)))
		bot.reply('Your new stats are: Attack - %s, Defense - %s, Strength - %s, Dexterity - %s, Max HP - %s. Game on!' % (att,defense,strength,dex,hp))
		db.commit()

# Boost a stat
@module.commands('boost')
def boostStat(bot, trigger):
	testDB(db,cur)
	stat = trigger.group(2)
	if not doesExist(trigger.nick):
		bot.reply('Your player needs to exist first! Say \'.createplayer\' to get started.')
	elif getBoosts(trigger.nick) < 1:
		bot.reply('You don\'t have any stat boosts remaining!')
	elif (stat=='attack' or stat=='defense' or stat=='hp' or stat=='strength' or stat=='dexterity'):
		if stat=='attack':
			cur.execute('UPDATE players SET attack=attack+%s WHERE name=\'%s\'' % (boostVal,trigger.nick))
			bot.reply('Your Attack stat has been increased by %s, for a total of %s.' % (boostVal,getAtt(trigger.nick)))
		elif stat=='defense':
			cur.execute('UPDATE players SET defense=defense+%s WHERE name=\'%s\'' % (boostVal,trigger.nick))
			bot.reply('Your Defense stat has been increased by %s, for a total of %s.' % (boostVal,getDef(trigger.nick)))
		elif stat=='strength':
			cur.execute('UPDATE players SET strength=strength+%s WHERE name=\'%s\'' % (boostVal,trigger.nick))
			bot.reply('Your Strength stat has been increased by %s, for a total of %s.' % (boostVal,getStr(trigger.nick)))
		elif stat=='dexterity':
			cur.execute('UPDATE players SET dexterity=dexterity+%s WHERE name=\'%s\'' % (boostVal,trigger.nick))
			bot.reply('Your Dexterity stat has been increased by %s, for a total of %s.' % (boostVal,getDex(trigger.nick)))
		else:
			cur.execute('UPDATE players SET maxhp=maxhp+%s,curhp=curhp+%s WHERE name=\'%s\'' % trigger.nick)
			bot.reply('Your Max HP has been increased by %s, for a total of %s.' % (boostVal,getMaxHP(trigger.nick)))
		cur.execute('UPDATE players SET boosts=boosts-1,used_boosts=used_boosts+1 WHERE name=\'%s\'' % trigger.nick)
		bot.reply('You have used one stat boost and have %s remaining. You have used %s stat boost(s) total.' % (getBoosts(trigger.nick),getUsedBoosts(trigger.nick)))
		db.commit()
	else:
		bot.reply('Sorry, \'%s\' isn\'t a stat I know of. Try again?' % stat)

# Trade a reroll for a number of stat points
@module.commands('trade')
def tradeReroll(bot, trigger): 
	testDB(db,cur)
	if not doesExist(trigger.nick):
		bot.reply('Your player needs to exist first! Say \'.createplayer\' to get started.')
	elif getRerolls(trigger.nick) < 1:
		bot.reply('You don\'t have any rerolls to trade!')
	else:
		cur.execute('UPDATE players SET rerolls=rerolls-1,boosts=boosts+%s WHERE name=\'%s\'' % (rollBoostRate,trigger.nick))
		bot.reply('You now have one fewer reroll, a total of %s remaining.' % getRerolls(trigger.nick))
		bot.reply('You now have %s additional stat boost(s), for a total of %s.' % (rollBoostRate,getBoosts(trigger.nick)))
		db.commit()

# Challenges another player to a duel
@module.commands('challenge')
def challengePlayer(bot, trigger):
	testDB(db,cur)
	if not doesExist(trigger.nick):
		bot.reply('Your player needs to exist first! Say \'.createplayer\' to get started.')
	elif not doesExist(trigger.group(2)):
		bot.reply('There is no player called %s, I\'m afraid. Tell them to \'.createplayer\'!' % trigger.group(2))
	else:
		# check to see if there are any active duels with the player
		cur.execute('SELECT * FROM players WHERE name=\'%s\' AND currentduel IS NOT NULL' % trigger.nick)
		activeDuel = cur.fetchone()
		# check to see if the player is already waiting for a response
		cur.execute('SELECT * FROM duels WHERE Challenger=%s AND accepted=false;' % getID(trigger.nick))
		youChallenging = cur.fetchone()
		# check to see if the player is being waited on for a response
		cur.execute('SELECT * FROM duels WHERE Defender=%s AND accepted=false;' % getID(trigger.nick))
		youWaiting = cur.fetchone()
		# check to see if the challenged has any active duels
		cur.execute('SELECT * FROM players WHERE name=\'%s\' AND currentduel IS NOT NULL' % trigger.group(2))
		themActive = cur.fetchone()
		# check to see if the challenged is waiting on a response
		cur.execute('SELECT * FROM duels WHERE Challenger=%s AND accepted=false;' % getID(trigger.group(2)))
		themChallenging = cur.fetchone()
		# check to see if the challenged is being waited on for a response
		cur.execute('SELECT * FROM duels WHERE Defender=%s AND accepted=false;' % getID(trigger.nick))
		themWaiting = cur.fetchone()
		##
		if activeDuel:
			bot.reply('You already have an open duel! Finish that first before stating another!')
		elif youChallenging:
			bot.reply('You already have an open challenge waiting on %s\'s response!' % youChallenging[1])
		elif youWaiting:
			bot.reply('There is already a challenge from %s waiting on your response!' % youWaiting[0])
		elif themActive:
			bot.reply('%s is already in a duel. Wait for them to finish!' % trigger.group(2))
		elif themChallenging:
			bot.reply('%s has challenged %s for a duel and cannot accept duels at this time.' % (trigger.group(2),themChallenging[1]))
		elif themWaiting:
			bot.reply('%s has been challenged by %s for a duel and cannot accept duels at this time.' % (trigger.group(2),themWaiting[0]))
		else:
			# creates the duel data 
			chaTot = getMaxHP(trigger.nick) + getAtt(trigger.nick) + getDef(trigger.nick) + getStr(trigger.nick) + getDex(trigger.nick)
			defTot = getMaxHP(trigger.group(2)) + getAtt(trigger.group(2)) + getDef(trigger.group(2)) + getStr(trigger.group(2)) + getDex(trigger.group(2))
			if chaTot > defTot:
				favour = trigger.nick
			else:
				favour = trigger.group(2)
			duelID = os.urandom(16)
			cur.execute('INSERT INTO duels VALUES(%s,%s,false,%s,NULL,false,%s,%s,1,0,0);', (getID(trigger.nick), getID(trigger.group(2)),getID(favour),getID(trigger.group(2)),duelID))
			cur.execute('UPDATE players SET currentduel=%s WHERE id=%s OR id=%s', (duelID,getID(trigger.nick),getID(trigger.group(2))))
			bot.say('%s: You are officially challenged to a duel by %s! Say \'.accept\' to begin the battle!' % (trigger.group(2),trigger.nick))
			db.commit()

# Accepts a duel from another player
@module.commands('accept')
def acceptChallenge(bot, trigger):
	testDB(db,cur)
	if not doesExist(trigger.nick):
		bot.reply('Your player needs to exist first! Say \'.createplayer\' to get started.')
	else:
		cur.execute('SELECT * FROM duels WHERE duelid=%s', (getCurrentDuel(trigger.nick),))
		waiting = cur.fetchone()
		if not waiting:
			bot.reply('You don\'t have any waiting challenges, I\'m afraid. Issue one with \'.challenge <name>\'!')
		else:
			# Updates the duel once it's confirmed to be valid to be active
			cur.execute('UPDATE duels SET accepted=true, active=true WHERE duelid=%s', (getCurrentDuel(trigger.nick),))
			bot.say('%s: %s has accepted your challenge!' % (getName(waiting[0]),trigger.nick))
			bot.say('The duel between %s and %s is now beginning, with the defender, %s, having the first move!' % (trigger.nick,getName(waiting[0]),trigger.nick))
			db.commit()

# Rejects a duel from another player
@module.commands('reject')
def rejectChallenge(bot, trigger):
	testDB(db,cur)
	if not doesExist(trigger.nick):
		bot.reply('Your player needs to exist first! Say \'.createplayer\' to get started.')
	else:
		cur.execute('SELECT * FROM duels WHERE duelid=%s', (getCurrentDuel(trigger.nick),))
		waiting = cur.fetchone()
		if not waiting:
			bot.reply('You don\'t have any waiting challenges to reject. Issue one with \'.challenge <name>\'!')
		else:
			# Updates the duel once it's confirmed to be valid to be active
			cur.execute('DELETE FROM duels WHERE duelid=%s', (getCurrentDuel(trigger.nick),))
			cur.execute('UPDATE players SET currentduel=NULL WHERE id=%s OR id=%s', (getID(trigger.nick),waiting[0]))
			bot.say('%s: %s has rejected your duel! "%s", they said!' % (getName(waiting[0]),trigger.nick,trigger.group(2)))
			db.commit()

# Attacks a player
@module.commands('attack')
def attackDuel(bot, trigger):
	testDB(db,cur)
	if not doesExist(trigger.nick):
		bot.reply('Your player needs to exist first! Say \'.createplayer\' to get started.')
	else:
		# determine if the player is actually in a duel or not
		cur.execute('SELECT * FROM duels WHERE (defender=%s OR challenger=%s) AND active=true' % (getID(trigger.nick),getID(trigger.nick)))
		duelResults = cur.fetchone()
		if not duelResults:
			cur.execute('SELECT challenger FROM duels WHERE defender=%s AND active=false AND accepted=false' % getID(trigger.nick))
			cha = cur.fetchone()
			if(cha):
				bot.reply('You have a waiting request from %s! You have to .accept their challenge first!' % cha[0])
			else:
				bot.reply('You are not currently in a duel! Go .challenge someone!')
		# test to see if it's the player's turn
		elif not (duelResults[6]==getID(trigger.nick)):
			bot.reply('Wait your turn, it\'s %s\'s turn!' % duelResults[6])
		elif duelResults[8]==2:
			bot.reply('It\'s your turn to .defend, not attack!')
		else:
			# set the opponent
			if duelResults[0]==getID(trigger.nick):
				opponent = duelResults[1]
			else:
				opponent = duelResults[0]
			# if it's time to determine your hits
			if duelResults[8]==1:
				rolls = "To hit: "
				hits = 0
				# this loop rolls a number of dice equal to the attacker's Att stat
				for x in range (0,getAtt(trigger.nick)):
					# rolls a hitDie-sided die, specified above
					tRoll = random.randint(1,hitDie)
					rolls = rolls + str(tRoll) + ', '
					# determines if the roll is high enough to count
					if tRoll > (hitThr - 1):
						# if double hits are counted, and if it's worthy of being one
						if dubHit and tRoll > (duHiTh - 1):
							hits = hits + 2
						# otherwise, just add 1 hit
						else:
							hits = hits + 1
					# determine if critical fails count and modify accordingly
					elif negHit and tRoll < (neHiTh + 1):
						hits = hits - 1
				rolls = rolls + '!'              # these two lines are to 
				rolls = re.sub(', !', '', rolls) #  remove the last comma
				bot.reply('%s -- a grand total of %s hit(s)!' % (rolls,hits))
				# determine Strength hits
				spRolls = "Strength roll: "
				spHits = 0
				for x in range (0,getStr(trigger.nick)):
					# rolls a strDie-sided die, specified above
					tRoll = random.randint(1,strDie)
					spRolls = spRolls + str(tRoll) + ', '
					# you know the drill, you goof
					if tRoll > (strThr - 1):
						# dubs bro
						if dubStr and tRoll > (duStTh - 1):
							spHits = spHits + 2
						# regs bro
						else:
							spHits = spHits + 1
					# wat about negs brah
					elif negStr and tRoll < (neStTh + 1):
						spHits = spHits - 1
				spRolls = spRolls + '!'
				spRolls = re.sub(', !', '', spRolls) # this stuff again
				# aw, zero hits!
				if hits < 1:
					cur.execute('UPDATE duels SET turn=%s WHERE duelid=%s', (opponent,getCurrentDuel(trigger.nick)))
					bot.reply('Too bad! The turn passes to %s for the next round!' % opponent)
				# sets the dice column to the number of hits, to be used with the next .defend command, and changes the turn and the stage
				else:
					cur.execute('UPDATE duels SET turn=%s,dice=%s,specialdice=%s,stage=2 WHERE duelid=%s', (opponent,hits,spHits,getCurrentDuel(trigger.nick)))
					bot.say('%s: it is your turn to .defend!' % opponent) # the hits for Attack and for Strength are stored in the duel data
				if showHiddenRolls:
					bot.reply(spRolls)
					bot.reply('Grand total of %s for your strength roll. Shh.....', spHits)
			# if it's time to determine your ultimate damage, following a .defend command
			elif duelResults[8]==3:
				rolls = "Damage roll: "
				hits = 0
				# this loop rolls dice equal to the difference between the attack roll and the defense roll
				for x in range (0,duelResults[9]):
					# rolls a attDie-sided die, specified above
					tRoll = random.randint(1,attDie)
					rolls = rolls + str(tRoll) + ', '
					# determines if the roll is high enough to count
					if tRoll > (attThr - 1):
						# if double hits are counted, and if it's worthy of being one
						if dubAtt and tRoll > (duAtTh - 1):
							hits = hits + 2
						# otherwise, just one hit
						else:
							hits = hits + 1
					# determine if crit failures count and subtract accordingly
					elif negAtt and tRoll < (neAtTh + 1):
						hits = hits - 1
				rolls = rolls + '!'
				rolls = re.sub(', !', '', rolls)
				bot.reply('%s -- a grand total of *%s damage*!' % (rolls,hits))
				# aw, zero damage!
				if hits < 1:
					if getStatus(opponent)=='stunned':
						cur.execute('UPDATE duels SET stage=1,dice=0,specialdice=0 WHERE duelid=%s', (getCurrentDuel(trigger.nick),))
						cur.execute('UPDATE players SET status=\'healthy\' WHERE name=\'%s\'' % opponent)
						bot.reply('Shame! As %s\'s stun wears off, you have another chance to .attack!' % opponent)
					elif getStatus(opponent)=='healthy':
						cur.execute('UPDATE duels SET turn=%s,stage=1,dice=0 WHERE duelid=%s', (opponent,getCurrentDuel(trigger.nick)))
						bot.reply('Too bad! The turn passes to *%s* for the next round!' % opponent)
					else:
						bot.reply('Something is wrong with the Status column! :o')
				# if the opponent has less current HP than the damage done (or the same amount), they lose! process the final results
				elif getCurHP(opponent) < (hits + 1):
					# set winner to the player, set active duel to false
					cur.execute('UPDATE duels SET winner=%s,active=false WHERE duelid=%s' % (trigger.nick,getCurrentDuel(trigger.nick))) 
					# grant the winner their boost(s) and set HP to max
					cur.execute('UPDATE players SET boosts=boosts+%s,curhp=maxhp,currentduel=NULL,status=\'healthy\' WHERE name=\'%s\'' % (winBoosts,trigger.nick))
					bot.reply('You are the winner of the duel against *%s*! You have gained *%s* stat point(s) for your victory!' % (opponent,winBoosts))
					# grant the loser a reroll and set his HP to max
					cur.execute('UPDATE players SET rerolls=rerolls+%s,curhp=maxhp,currentduel=NULL,status=\'healthy\' WHERE name=\'%s\'' % (loseRerolls,opponent))
					bot.say('%s: Better luck next time. You get %s stat reroll(s), tradable for %s stat point(s) each.' % (opponent,loseRerolls,rollBoostRate))
					bot.say('The duel between *%s* and *%s* has officially ended. The winner was *%s*! Both of them have been healed back to max. See you next time!' % (duelResults[0],duelResults[1],trigger.nick))
				# otherwise, just deal the damage
				else:
					if getStatus(opponent)=='stunned':
						cur.execute('UPDATE duels SET stage=1,dice=0,specialdice=0 WHERE duelid=%s', (getCurrentDuel(trigger.nick),))
						cur.execute('UPDATE players SET status=\'healthy\',curhp=curhp-%s WHERE name=\'%s\'' % (hits,opponent))
						bot.say('%s: You have %s/%s HP remaining! Your stun wears off!' % (opponent,getCurHP(opponent),getMaxHP(opponent)))
						bot.reply('It is your chance to .attack again while %s is recovering!' % opponent)
					elif getStatus(opponent)=='healthy':
						cur.execute('UPDATE duels SET turn=%s,dice=0,stage=1 WHERE duelid=%s' % (opponent,getCurrentDuel(trigger.nick)))
						cur.execute('UPDATE players SET curhp=curhp-%s WHERE name=\'%s\'' % (hits,opponent))
						bot.say('%s: You have %s/%s HP remaining! It is your turn to .attack!' % (opponent,getCurHP(opponent),getMaxHP(opponent)))
					else:
						bot.reply('Something is wrong with the Status column! :o')
			elif duelResults[8]==4:
				rolls = "Riposte roll: "
				hits = 0
				setProfile('riposte damage')
				# this loop rolls dice equal to the difference bewteen the last Attack roll and the last Dex roll
				for x in range (0,duelResults[9]):
					# rolls an dexDie-sided die
					tRoll = random.randint(1,dexDie)
					rolls = rolls + str(tRoll) + ', '
					# roll high enough to count?
					if tRoll > (dexThr - 1):
						# check double
						if dubDex and tRoll > (duDxTh - 1):
							hits = hits + 2
						#otherwise, just one
						else:
							hits = hits + 1
					# determine if crit fails count
					elif negDex and tRoll < (neDxTh + 1):
						hits = hits - 1
				rolls = rolls + '!'
				rolls = re.sub(', !', '', rolls)
				bot.reply('%s -- a grand total of *%s riposte damage*!' % (rolls,hits))
				# aw, zero damage!
				if hits < 1:
					cur.execute('UPDATE duels SET stage=1,dice=0 WHERE duelid=%s', (getCurrentDuel(trigger.nick),))
					bot.reply('Unsuccessful riposte, but it\'s now your turn to .attack!')
				# if the opponent has less current HP than the damage done (or the same amount), they lose! process the final results
				elif getCurHP(opponent) < (hits + 1):
					# set winner to the player, set active duel to false
					cur.execute('UPDATE duels SET winner=%s,active=false WHERE duelid=%s' % (trigger.nick,getCurrentDuel(trigger.nick))) 
					# grant the winner their boost(s) and set HP to max
					cur.execute('UPDATE players SET boosts=boosts+%s,curhp=maxhp,currentduel=NULL,status=\'healthy\' WHERE name=\'%s\'' % (winBoosts,trigger.nick))
					bot.reply('You are the winner of the duel against *%s*! You have gained *%s* stat point(s) for your victory!' % (opponent,winBoosts))
					# grant the loser a reroll and set his HP to max
					cur.execute('UPDATE players SET rerolls=rerolls+%s,curhp=maxhp,currentduel=NULL,status=\'healthy\' WHERE name=\'%s\'' % (loseRerolls,opponent))
					bot.say('%s: Better luck next time. You get %s stat reroll(s), tradable for %s stat point(s) each.' % (opponent,loseRerolls,rollBoostRate))
					bot.say('The duel between *%s* and *%s* has officially ended. The winner was *%s*! Both of them have been healed back to max. See you next time!' % (duelResults[0],duelResults[1],trigger.nick))
				# otherwise, just deal the damage
				else:
					cur.execute('UPDATE duels SET stage=1,dice=0 WHERE duelid=%s', (getCurrentDuel(trigger.nick),))
					cur.execute('UPDATE players SET curhp=curhp-%s WHERE name=\'%s\'' % (hits,opponent))
					bot.say('%s: You have %s/%s HP remaining!' % (opponent,getCurHP(opponent),getMaxHP(opponent)))
					bot.reply('Successful riposte! It is your turn to .attack!')

			else:
				bot.reply('Not really sure how you got here....the Stage column must be messed up. Check it out!')
			db.commit()

# The defend command!
@module.commands('defend')
def defendDuel(bot, trigger):
	testDB(db,cur)
	if not doesExist(trigger.nick):
		bot.reply('Your player needs to exist first! Say \'.createplayer\' to get started.')
	else:
		# determine if the player is actually in a duel or not
		cur.execute('SELECT * FROM duels WHERE (defender=%s OR challenger=%s) AND active=true' % (getID(trigger.nick),getID(trigger.nick)))
		duelResults = cur.fetchone()
		if not duelResults:
			cur.execute('SELECT challenger FROM duels WHERE defender=%s AND active=false AND accepted=false' % getID(trigger.nick))
			cha = cur.fetchone()
			if(cha):
				bot.reply('You have a waiting request from %s! You have to .accept their challenge first!' % cha[0])
			else:
				bot.reply('You are not currently in a duel! Go .challenge someone!')
		# test to see if it's the player's turn
		elif not (duelResults[6]==getID(trigger.nick)):
			bot.reply('Wait your turn, it\'s %s\'s turn!' % duelResults[6])
		elif duelResults[8]==1 or duelResults[8]==3 or duelResults[8]==4:
			bot.reply('It\'s your turn to .attack, not defend!')
		elif duelResults[8]==2:
			rolls = "Defense roll: "
			hits = 0
			if duelResults[0]==getID(trigger.nick):
				opponent = duelResults[1]
			else:
				opponent = duelResults[0]
			# this loop rolls dice equal to the player's defense stat
			for x in range (0,getDef(trigger.nick)):
				# rolls a defDie-sided die, specified above
				tRoll = random.randint(1,defDie)
				rolls = rolls + str(tRoll) + ', '
				# determine if the roll is high enough to count
				if tRoll > (defThr - 1):
					# if double hits are counted, and if it's worthy of being one...
					if dubDef and tRoll > (duDfTh - 1):
						hits = hits + 2
					# otherwise, just one hit
					else:
						hits = hits + 1
				# determine if failures count and subtract accordingly
				elif negAtt and tRoll < (neDfTh + 1):
					hits = hits - 1
			rolls = rolls + '!'
			rolls = re.sub(', !', '', rolls)
			# time for some dex rolls!
			spRolls = "Dexterity roll: "
			spHits = 0
			for x in range (0,getDex(trigger.nick)):
				tRoll = random.randint(1,dexDie)
				spRolls = spRolls + str(tRoll) + ', '
				# do i really need to say it?
				if tRoll > (dexThr - 1):
					if dubDex and tRoll > (duDxTh - 1):
						spHits = spHits + 2
					else:
						spHits = spHits = 1
				elif negDex and tRoll < (neDxTh + 1):
					spHits = spHits - 1
			spRolls = spRolls + '!'
			spRolls = re.sub(', !', '', spRolls)
			bot.reply('%s -- a grand total of _%s hit(s)_!' % (rolls,hits))
			if showHiddenRolls:
				bot.reply(spRolls)
				bot.reply('You got a Dex roll of %s. Shhh....' % spHits)
			## duelResults[9] is the Hit roll from last time, and [10] is the Str roll
			isStun = False
			isRiposte = False
			if duelResults[10] > ((2 * hits) - 1) and spHits > ((2 * duelResults[9]) - 1):
				if (duelResults[10] + duelResults[9]) > (hits + spRolls):
					isStun = True
				elif (duelResults[10] + duelResults[9]) < (hits + spRolls):
					isRiposte = True
			elif duelResults[10] > ((2 * hits) - 1):
				isStun = True
			elif spHits > ((2 * duelResults[9]) - 1):
				isRiposte = True
			# react according to the situation, ie stun, riposte, neither
			newDice = duelResults[9] - hits
			if isStun:
				if hits < 1:
					cur.execute('UPDATE duels SET turn=%s,stage=3,dice=%s,specialdice=0 WHERE duelid=%s', (opponent,newDice,getCurrentDuel(trigger.nick)))
					cur.execute('UPDATE players SET status=\'stunned\' WHERE name=\'%s\'' % opponent)
					bot.reply('Too bad! Unfortunately, %s\'s blow manages to stun you! The turn passes to them for damage!' % opponent)
				elif newDice < 1:
					cur.execute('UPDATE duels SET turn=%s,stage=1,dice=0,specialdice=0 WHERE duelid=%s', (opponent,getCurrentDuel(trigger.nick)))
					bot.reply('Your armour holds, no damage for %s! Their strike winds you though, leaving you stunned! The turn passes back to them for a new .attack with %s damage dice!' % (opponent,newDice))
				else:
					cur.execute('UPDATE duels SET turn=%s,stage=3,dice=%s,specialdice=0 WHERE duelid=%s', (opponent,newDice,getCurrentDuel(trigger.nick)))
					cur.execute('UPDATE players SET status=\'stunned\' WHERE name=\'%s\'' % trigger.nick)
					bot.reply('Your armour blocks some of the attack, but %s\'s blow winds you!' % opponent)
					bot.say('%s: You have _%s_ remaining dice for damage, and you will have the opportunity to .attack again after due to your stun!' % (opponent,newDice))
			elif isRiposte:
				if hits < 1: # currently we're determining riposte dice by whatever your dex roll was
					cur.execute('UPDATE duels SET stage=4,dice=%s,specialdice=0 WHERE duelid=%s', (spHits-duelResults[9],getCurrentDuel(trigger.nick)))
					bot.reply('Your....uh...armour sucks but...your weapon is fast! ...I guess.... Either way, you successfully riposte.')
				elif newDice < 1:
					cur.execute('UPDATE duels SET stage=4,dice=%s,specialdice=0 WHERE duelid=%s', (spHits-duelResults[9],getCurrentDuel(trigger.nick)))
					bot.reply('You are able to swiftly and deftly parry %s\'s attack away! You can now .attack with a riposte!' % opponent)
				else:
					cur.execute('UPDATE duels SET stage=4,dice=%s,specialdice=0 WHERE duelid=%s', (spHits-duelResults[9],getCurrentDuel(trigger.nick)))
					bot.reply('%s\'s attack nearly strikes you, but you parry them away at the last second, catching them off guard! You can now .attack with a riposte!' % opponent)
			else:
				if hits < 1:
					cur.execute('UPDATE duels SET turn=%s,stage=3 WHERE duelid=%s', (opponent,getCurrentDuel(trigger.nick)))
					bot.reply('Too bad! The turn passes to *%s* for damage, with %s dice at their disposal!' % (opponent,duelResults[9]))
				elif newDice < 1:
					cur.execute('UPDATE duels SET stage=1,dice=0,specialdice=0 WHERE duelid=%s', (getCurrentDuel(trigger.nick),))
					bot.reply('Your armour holds, no damage for %s! It is your turn to .attack!' % opponent)
				else:
					cur.execute('UPDATE duels SET turn=%s,stage=3,dice=%s WHERE %s', (opponent,newDice,getCurrentDuel(trigger.nick)))
					bot.say('%s: You have _%s_ dice remaining for damage. It is your turn to .attack!' % (opponent,newDice))
			db.commit()

	#		newDice = duelResults[9] - hits
	#		# aw, zero defense!
	#		if hits < 1:
	#			cur.execute('UPDATE duels SET turn=\'%s\',stage=3 WHERE (challenger=\'%s\' OR defender=\'%s\') AND active=true' % (opponent,trigger.nick,trigger.nick))
	#			bot.reply('Too bad! The turn passes to *%s* for damage!' % opponent)
	#		elif newDice < 0:
	#			newDice = 0 - newDice
	#			cur.execute('UPDATE duels SET stage=4,dice=%s WHERE (challenger=\'%s\' OR defender=\'%s\') AND active=true' % (newDice,trigger.nick,trigger.nick))
	#			bot.reply('A chance for a riposte! You have _%s_ dice to use for your counter-.attack!!' % newDice)
	#		elif newDice < 1:
	#			cur.execute('UPDATE duels SET stage=1,dice=0 WHERE (challenger=\'%s\' OR defender=\'%s\') AND active=true' % (trigger.nick,trigger.nick))
	#			bot.reply('A perfect parry! It is your turn to .attack!')
	#		else:
	#			cur.execute('UPDATE duels SET turn=\'%s\',stage=3,dice=%s WHERE (challenger=\'%s\' OR defender=\'%s\') AND active=true' % (opponent,newDice,trigger.nick,trigger.nick))
	#			bot.say('%s: You have _%s_ dice remaining for damage. It is your turn to .attack!' % (opponent,newDice))
	#		db.commit()

# The forfeit command!
@module.commands('forfeit')
def forfeitDuel(bot, trigger):
	testDB(db,cur)
	if not doesExist(trigger.nick):
		bot.reply('Your player needs to exist first! Say \'.createplayer\' to get started.')
	else:
		cur.execute('SELECT * FROM duels WHERE duelid=%s AND active=true', (getCurrentDuel(trigger.nick),))
		duelResults = cur.fetchone()
		if not duelResults:
			bot.reply('You are not currently in a duel! Go .challenge someone before giving up!')
		else:
			if duelResults[0]==getID(trigger.nick):
				opponent = duelResults[1]
			else:
				opponent = duelResults[0]
			cur.execute('UPDATE duels SET winner=%s,active=false WHERE duelid=%s', (opponent,getCurrentDuel(trigger.nick)))
			# grant the winner their boost(s) and set HP to max
			cur.execute('UPDATE players SET boosts=boosts+%s,curhp=maxhp WHERE id=%s' % (winBoosts,opponent))
			bot.say('%s: You are the winner of the duel against %s! You have gained %s stat point(s) for your victory!' % (getName(opponent),trigger.nick,winBoosts))
			# grant the loser a reroll and set his HP to max
			cur.execute('UPDATE players SET rerolls=rerolls+%s,curhp=maxhp WHERE name=\'%s\'' % (loseRerolls,trigger.nick))
			bot.reply('Better luck next time. You get %s stat reroll(s), tradable for %s stat point(s) each.' % (loseRerolls,rollBoostRate))
			bot.say('The duel between %s and %s has officially ended. The winner was %s! Both of them have been healed back to max. See you next time!' % (getName(duelResults[0]),getName(duelResults[1]),getName(opponent)))
			db.commit()

# override the help command
@module.commands('help')
def help(bot, trigger):
	bot.reply('No help for you!')
