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
import string
import time

# if true, then whoever is not the favoured player winning gets a bonus stat point
favourPoints = True
fixedRiposte = False
# whether or not to show the dexterity and strength rolls
showHiddenRolls = False
showWinningRolls = True
# whether or not to show debug logs
DEBUG = False
DEBUG_CONTROL = True
ADMIN_CONTROL = True
ADMINS = ('jabird',)
DEBUGGERS = ('jabird','dad')

# connect to the data base, and create a cursor with which to execute queries
db = MySQLdb.connect(host="localhost",user="dicebot",passwd="megadicebot",db="dicebot")
cur = db.cursor()

### commenting out since this hasn't helped yet
#function to make sure that the db is still connected
#def testDB(myDB,myCur):
#	try:
#		myCur.execute('SELECT * FROM players;')
#	except (AttributeError, MySQLdb.OperationalError):
#		myDB = MySQLdb.connect(host="localhost",user="dicebot",passwd="megadicebot",db="dicebot")

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
favourBoosts = 0
# how many points a stat is boosted per boost
boostVal = 0
# how many rerolls you get for losing/winning
winRerolls = 0
loseRerolls = 0
# exchange rate between rerolls and stat boosts
rollBoostRate = 0
boostToRoll = 0
# HP boost modifier, if any
hpBoostMod = 0
# Determines how many dice are used in a Riposte roll
riposteDice = 0

def setProfile(profile):
	#testDB(db,cur)
	cur.execute('SELECT * FROM variableprofiles WHERE name=\'%s\'' % profile)
	varStats = cur.fetchone()
	# this line is a mess lol. can't think of any other way to do this though
	global minAtt,minDef,minHP,minStr,minDex,maxAtt,maxDef,maxHP,maxStr,maxDex,hitDie,defDie,attDie,strDie,dexDie,hitThr,defThr,attThr,strThr,dexThr,dubHit,dubDef,dubAtt,dubStr,dubDex,duHiTh,duDfTh,duAtTh,duStTh,duDxTh,negHit,negDef,negAtt,negStr,negDex,neHiTh,neDfTh,neAtTh,neStTh,neDxTh,winBoosts,loseBoosts,favourBoosts,boostVal,winRerolls,loseRerolls,rollBoostRate,boostToRoll,hpBoostMod,riposteDice
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
	favourBoosts = varStats[43]
	boostVal = varStats[44]
	# rerolls gained per win/loss
	winRerolls = varStats[45]
	loseRerolls = varStats[46]
	# how many boosts per roll
	rollBoostRate = varStats[47]
	# how many rolls per boost
	boostToRoll = varStats[48]
	# multiplier for HP boost
	hpBoostMod = varStats[49]
	# dice for riposte roll
	riposteDice = varStats[50]

# set the current profile to the default one specified in the database
setProfile(curProfile)
# defining regularly used queries as functions
def getAtt(ID):
	#testDB(db,cur)
	cur.execute('SELECT attack FROM players WHERE ID=%s' % ID)
	return cur.fetchone()[0]
def getDef(ID):
	#testDB(db,cur)
	cur.execute('SELECT defense FROM players WHERE ID=%s' % ID)
	return cur.fetchone()[0]
def getStr(ID):
	#testDB(db,cur)
	cur.execute('SELECT strength FROM players WHERE ID=%s' % ID)
	return cur.fetchone()[0]
def getDex(ID):
	#testDB(db,cur)
	cur.execute('SELECT dexterity FROM players WHERE ID=%s' % ID)
	return cur.fetchone()[0]
def getPlayerID(name):
	#testDB(db,cur)
	cur.execute('SELECT ID FROM players WHERE name=%s', (name,))
	return cur.fetchone()[0]
def getName(ID):
	#testDB(db,cur)
	cur.execute('SELECT name FROM players WHERE id=%s' % ID)
	return cur.fetchone()[0]
def getMaxHP(ID):
	#testDB(db,cur)
	cur.execute('SELECT maxhp FROM players WHERE ID=%s' % ID)
	return cur.fetchone()[0]
def getCurHP(ID):
	#testDB(db,cur)
	cur.execute('SELECT curhp FROM players WHERE ID=%s' % ID)
	return cur.fetchone()[0]
def getActive(ID):
	#testDB(db,cur)
	cur.execute('SELECT active FROM players WHERE ID=%s' % ID)
	return cur.fetchone()[0]
def doesExist(name):
	#testDB(db,cur)
	cur.execute('SELECT * FROM players WHERE name=%s', (name,))
	return cur.fetchone()
def getBoosts(ID):
	#testDB(db,cur)
	cur.execute('SELECT Boosts FROM players WHERE ID=%s' % ID)
	return cur.fetchone()[0]
def getUsedBoosts(ID):
	#testDB(db,cur)
	cur.execute('SELECT Used_Boosts FROM players WHERE ID=%s' % ID)
	return cur.fetchone()[0]
def getRerolls(ID):
	#testDB(db,cur)
	cur.execute('SELECT Rerolls FROM players WHERE ID=%s' % ID)
	return cur.fetchone()[0]
def getUsedRerolls(ID):
	#testDB(db,cur)
	cur.execute('SELECT Used_Rerolls FROM players WHERE ID=%s' % ID)
	return cur.fetchone()[0]
def getCurrentDuel(name):
	#testDB(db,cur)
	cur.execute('SELECT CurrentDuel FROM players WHERE name=\'%s\'' % name)
	return cur.fetchone()[0]
def getStatus(ID):
	#testDB(db,cur)
	cur.execute('SELECT Status FROM players WHERE ID=%s' % ID)
	return cur.fetchone()[0]

################
# Getters for equipment-based information
# TODO: make getters that determine stats after modifiers are taken into account
def getInventory(ID):
	cur.execute('SELECT * FROM inventory WHERE ID=%s' % ID)
	return cur.fetchone()

# does item exist?
def doesItemExist(name):
	cur.execute('SELECT * FROM item_definitions WHERE name=%s', (name,))
	return cur.fetchone()

# get the item id from an item name
def getItemID(name):
	cur.execute('SELECT ItemID FROM item_definitions WHERE name=%s', (name,))
	return cur.fetchone()[0]

# get the itemid from existing item
def getExistItemID(ID):
	cur.execute('SELECT ID FROM items WHERE itemid=%s' % ID)
	return cur.fetchone()[0]

# get the existing ID from an itemid
def getExistID(ID):
	cur.execute('SELECT ItemID FROM items WHERE id=%s' % ID)
	return cur.fetchone()[0]

# get the item name from item id
def getItemName(ID):
	cur.execute('SELECT Name FROM item_definitions WHERE itemid=%s' % ID)
	return cur.fetchone()[0]

# a shortcut to getItemName(getExistID())
def getExistName(ID):
	return getItemName(getExistID(ID))

# get the type of the item
def getItemType(ID):
	cur.execute('SELECT Type FROM item_definitions WHERE itemid=%s' % ID)
	return cur.fetchone()[0]

###
# get type of weapon: main hand, off hand, one hand, both hands
def getWeaponHand(ID):
	cur.execute('SELECT Hand FROM weapon_definitions WHERE itemid=%s' % ID)
	return cur.fetchone()[0]

# get slot of weapon: head, shoulders, hands, legs, feet, back
def getArmourSlot(ID):
	cur.execute('SELECT Slot FROM armour_definitions WHERE itemid=%s' % ID)
	return cur.fetchone()[0]

# get the list of parts for a piece of armour
def getArmourParts(ID):
	cur.execute('SELECT Part1,Part2,Part3 FROM armour_definitions WHERE itemid=%s' % ID)
	return cur.fetchone()

# get the list of parts for a weapon
def getWeaponParts(ID):
	cur.execute('SELECT Part1,Part2,Part3 FROM weapon_definitions WHERE itemid=%s' % ID)
	return cur.fetchone()

# get passive effect ID from armour
def getArmourPE(ID):
	cur.execute('SELECT PassiveEffect FROM armour_parts WHERE partid=%s' % ID)
	return cur.fetchone()[0]

# get passive effect ID from weapon
def getWeaponPE(ID):
	cur.execute('SELECT PassiveEffect FROM weapon_parts WHERE partid=%s' % ID)
	return cur.fetchone()[0]

###
# add item to inventory
def addToInventory(PID,IID):
	cur.execute('SELECT Inventory FROM inventory WHERE ID=%s' % PID)
	inventory = cur.fetchone()[0]
	if inventory:
		inventory = inventory + ' ' + str(IID)
	else:
		inventory = str(IID)
	cur.execute('UPDATE inventory SET Inventory=%s', (inventory,))
	db.commit()

# remove an item from inventory
def removeFromInventory(PID,IID):
	cur.execute('SELECT Inventory FROM inventory WHERE ID=%s' % PID)
	inventory = list(cur.fetchone()[0])
	inventory.remove(str(IID))
	if inventory:
		' '.join(inventory)
		cur.execute('UPDATE inventory SET Inventory=%s', (inventory,))
	else:
		cur.execute('UPDATE inventory SET Inventory=null')
	db.commit()

###
# get True HP (based on own items)
def getTrueMaxHP(ID):
	inventory = getInventory(ID)
	inventory.pop(0)
	inventory.pop(8)
	total = getMaxHP(ID)
	for x in inventory:
		if x:
			if getItemType(getExistID(x))=='armour':
				parts = getArmourParts(getExistID(x))
			else:
				parts = getWeaponParts(getExistID(x))
			for y in parts:
				cur.execute('SELECT Scope,Stat,Modifier,IsSpecial FROM passive_effects WHERE effectid=%d' % getArmourPE(y))
				effects = cur.fetchone()
				if effects(1)=='hp' and not effects(3) and (effects(0)=='self' or effects(0)=='team'):
					total = total + int(effects(2))
			
	##if # TODO: ADD HP EFFECTS FROM ANY BUFFS OR DEBUFFS. MAYBE LEAVE FOR NEXT UPDATE?
	## TODO: FINISH THE FUNCTION
				
#
################

########
## Determining logic for stuns and ripostes
def mayStun(strength,defense):
	if strength > ((defense * 2) - 1):
		return True
	else:
		return False

def mayRiposte(dexterity,attack,defense):
	if int((dexterity + defense) / 2) > ((attack * 2) - 1):
		return True
	else:
		return False
##
########

#### defining more complicated functions that involve queries
# Creates a player with the name of the user who called it, and random stats
@module.commands('createplayer')
def createPlayer(bot, trigger):
	#testDB(db,cur)
	if doesExist(trigger.nick):
		bot.reply('\00313Your player already exists!')
	else:
		random.seed(time.time())
		# generate stats based on variables set above
		att = random.randint(minAtt,maxAtt)
		defense = random.randint(minDef,maxDef)
		hp = random.randint(minHP,maxHP)
		strength = random.randint(minStr,maxStr)
		dex = random.randint(minDex,maxDex)
		# ID (auto generated), Active, Name, Attack, Defense, MaxHP, Current HP, boosts, used boosts, rerolls, used rerolls
		cur.execute('INSERT INTO players VALUES(NULL,0,\'%s\',%s,%s,%s,%s,%s,%s,0,0,0,0,NULL,\'healthy\')' % (trigger.nick,att,defense,strength,dex,hp,hp))
		cur.execute('SELECT LAST_INSERT_ID()')
		newID = cur.fetchone()[0]
		cur.execute('INSERT INTO inventory VALUES(%s,null,null,null,null,null,null,null,null,null)' % newID)
		bot.reply('\00313Your character is created! Your max hp is %s, you have %s attack dice and %s defense dice, you have %s strength dice and %s dexterity dice, and you are listed as player %s. Game on!' % (hp,att,defense,strength,dex,getPlayerID(trigger.nick)))
		db.commit()

# Check Stats
@module.commands('stats')
def getStats(bot, trigger):
	#testDB(db,cur)
	if not trigger.group(2):
		if not doesExist(trigger.nick):
			bot.reply('\00313Your player needs to exist first! Say \'.createplayer\' to get started.')
		else:
			cur.execute('SELECT * FROM players WHERE name=\'%s\'' % trigger.nick)
			results = cur.fetchone()
			bot.reply('\00313Your Attack is %s, Defense is %s, Strength is %s, Dexterity is %s, and you have %s/%sHP.' % (results[3],results[4],results[5],results[6],results[8],results[7]))
			bot.reply('\00313You have used %s Boost points and have %s remaining Boost points to spend.' % (results[10],results[9]))
			bot.reply('\00313You have used %s stat Rerolls and have %s remaining stat Rerolls.' % (results[12],results[11]))
			cur.execute('SELECT * FROM duels WHERE duelid=%s', (getCurrentDuel(trigger.nick),))
			results = cur.fetchone()
			if results:
				if results[0]==getPlayerID(trigger.nick):
					opponent = getName(results[1])
					if results[2]:
						bot.reply('\00313You are currently in a duel with %s.' % opponent)
					else:
						bot.reply('\00313You currently are awaiting %s for a response to your challenge.' % opponent)
				else:
					opponent = getName(results[0])
					if results[2]:
						bot.reply('\00313You are currently in a duel with %s.' % opponent)
					else:
						bot.reply('\00313%s is currently awaiting your acceptance of their challenge.' % opponent)
			else:
				bot.reply('\00313You are not currently in, or waiting on, a duel.')
		#	items = list(getInventory(getPlayerID(trigger.nick)))
		#	items.pop(0)
		#	isNaked = True
		#	for x in items:
		#		if x:
		#			isNaked = False
		#	if isNaked:
		#		bot.reply('\00313You are naked!')
		#	else:
		#		wearing = ''
		#		extendedInventory = items.pop(8).split()
		#		for x in items:
		#			if x and wearing:
		#				wearing = wearing + ', ' + getItemName(x)
		#			elif x:
		#				wearing = getItemName(x)
		#		if wearing:
		#			bot.reply('\00313You are currently wearing/wielding the following:')
		#			bot.reply('\00313%s' % wearing)
		#		holding = ''
		#		for x in extendedInventory:
		#			if x and holding:
		#				holding = holding + ', ' + getExistName(x)
		#			elif x:
		#				holding = getExistName(x)
		#		if holding:
		#			bot.reply('\00313You are currently holding the following:')
		#			bot.reply('\00313%s' % holding)
	else:
		if not doesExist(trigger.group(2)):
			bot.reply('\00313Sorry, %s isn\'t an existing player.' % trigger.group(2))
		else:
			cur.execute('SELECT * FROM players WHERE name=\'%s\'' % trigger.group(2))
			results = cur.fetchone()
			bot.reply('\00313The stats for the player %s are as follows:' % trigger.group(2))
			bot.reply('\00313Attack is %s, Defense is %s, Strength is %s, Dexterity is %s, and %s/%sHP.' % (results[3],results[4],results[5],results[6],results[8],results[7]))
			bot.reply('\00313They have used %s Boost points and have %s remaining Boost points to spend.' % (results[10],results[9]))
			bot.reply('\00313They have used %s stat Rerolls and have %s remaining stat Rerolls.' % (results[12],results[11]))
			cur.execute('SELECT * FROM duels WHERE duelid=%s', (getCurrentDuel(trigger.group(2)),))
			results = cur.fetchone()
			if results:
				if results[0]==getPlayerID(trigger.group(2)):
					opponent = getName(results[1])
					if opponent==trigger.nick:
						opponent = 'you'
					else:
						opponent = getName(opponent)
					if results[2]:
						bot.reply('\00313They are currently in a duel with %s.' % opponent)
					else:
						bot.reply('\00313They currently are awaiting %s for a response to their challenge.' % opponent)
				else:
					opponent = getName(results[0])
					if opponent==trigger.nick:
						opponent = 'you'
					if results[2]:
						bot.reply('\00313They are currently in a duel with %s.' % opponent)
					else:
						if opponent=='you':
							bot.reply('\00313You are currently awaiting their acceptance of your challenge.')
						else:
							bot.reply('\00313%s is currently awaiting their acceptance of their challenge.' % opponent)
			else:
				bot.reply('\00313They are not currently in, or waiting on, a duel.')

# Quick stats
@module.commands('qstats')
def getQuickStats(bot, trigger):
	#testDB(db,cur)
	if not doesExist(trigger.nick):
		bot.reply('\00313Your player needs to exist first! Say \'.createplayer\' to get started.')
	else:
		cur.execute('SELECT * FROM players WHERE name=\'%s\'' % trigger.nick)
		results = cur.fetchone()
		bot.reply('\00313Att: %s' % results[3])
		bot.reply('\00313Def: %s' % results[4])
		bot.reply('\00313Str: %s' % results[5])
		bot.reply('\00313Dex: %s' % results[6])
		bot.reply('\00313HP: %s/%s' % (results[8],results[7]))

# Quick HP for you or another player
@module.commands('qhp')
def getQuickHP(bot, trigger):
	#testDB(db,cur)
	if trigger.group(2):
		if not doesExist(trigger.group(2)):
			bot.reply('\00313There is no player called %s.' % trigger.group(2))
		else:
			bot.reply('\00313%s\'s HP: %s/%s' % (trigger.group(2),getCurHP(getPlayerID(trigger.group(2))),getMaxHP(getPlayerID(trigger.group(2)))))
	elif not doesExist(trigger.nick):
		bot.reply('\00313Your player needs to exist first! Say \'.createplayer\' to get started.')
	else:
		bot.reply('\00313Your HP: %s/%s' % (getCurHP(getPlayerID(trigger.nick)),getMaxHP(getPlayerID(trigger.nick))))

# List of Players
@module.commands('players')
def getPlayers(bot, trigger):
	#testDB(db,cur)
	cur.execute('SELECT name FROM players')
	results = cur.fetchall()
	if not results:
		bot.reply('There are no players at this time.')
	else:
		bot.reply('List of players:')
		for x in results:
			bot.reply('%s' % x)

# Reroll your stats
@module.commands('reroll')
def rerollStats(bot, trigger):
	random.seed(time.time())
	#testDB(db,cur)
	if not doesExist(trigger.nick):
		bot.reply('\00313Your player needs to exist first! Say \'.createplayer\' to get started.')
	elif getRerolls(getPlayerID(trigger.nick)) < 1:
		bot.reply('\00313You don\'t have any stat rerolls remaining!')
	else:
		# generate new stats based on variables set above
		att = random.randint(minAtt,maxAtt)
		defense = random.randint(minDef,maxDef)
		hp = random.randint(minHP,maxHP)
		strength = random.randint(minStr,maxStr)
		dex = random.randint(minDex,maxDex)
		# remove one reroll and increment the UsedRerolls stat
		cur.execute('UPDATE players SET attack=%s,defense=%s,strength=%s,dexterity=%s,maxhp=%s,curhp=%s,rerolls=rerolls-1,used_rerolls=used_rerolls+1 WHERE name=\'%s\'' % (att,defense,strength,dex,hp,hp,trigger.nick))
		bot.reply('\00313You have used one reroll and have %s remaining. You have used %s reroll(s) total.' % (getRerolls(getPlayerID(trigger.nick)),getUsedRerolls(getPlayerID(trigger.nick))))
		bot.reply('\00313Your new stats are: Attack - %s, Defense - %s, Strength - %s, Dexterity - %s, Max HP - %s. Game on!' % (att,defense,strength,dex,hp))
		db.commit()

# Boost a stat
@module.commands('boost')
def boostStat(bot, trigger):
	#testDB(db,cur)
	if trigger.group(2):
		stat = trigger.group(2).lower()
	if not doesExist(trigger.nick):
		bot.reply('\00313Your player needs to exist first! Say \'.createplayer\' to get started.')
	elif getBoosts(getPlayerID(trigger.nick)) < 1:
		bot.reply('\00313You don\'t have any stat boosts remaining!')
	elif not trigger.group(2):
		bot.reply('\00313You need to pick a stat to .boost! Att(ack), Def(ense), Dex(terity), Str(ength) and HP (Health) are your options.')
	elif (stat=='attack' or stat=='defense' or stat=='hp' or stat=='strength' or stat=='dexterity' or stat=='dex' or stat=='str' or stat=='att' or stat=='def' or stat=='health'):
		if stat=='attack' or stat=='att':
			cur.execute('UPDATE players SET attack=attack+%s WHERE name=\'%s\'' % (boostVal,trigger.nick))
			bot.reply('\00313Your Attack stat has been increased by %s, for a total of %s.' % (boostVal,getAtt(getPlayerID(trigger.nick))))
		elif stat=='defense' or stat=='def':
			cur.execute('UPDATE players SET defense=defense+%s WHERE name=\'%s\'' % (boostVal,trigger.nick))
			bot.reply('\00313Your Defense stat has been increased by %s, for a total of %s.' % (boostVal,getDef(getPlayerID(trigger.nick))))
		elif stat=='strength' or stat=='str':
			cur.execute('UPDATE players SET strength=strength+%s WHERE name=\'%s\'' % (boostVal,trigger.nick))
			bot.reply('\00313Your Strength stat has been increased by %s, for a total of %s.' % (boostVal,getStr(getPlayerID(trigger.nick))))
		elif stat=='dexterity' or stat=='dex':
			cur.execute('UPDATE players SET dexterity=dexterity+%s WHERE name=\'%s\'' % (boostVal,trigger.nick))
			bot.reply('\00313Your Dexterity stat has been increased by %s, for a total of %s.' % (boostVal,getDex(getPlayerID(trigger.nick))))
		else:
			cur.execute('UPDATE players SET maxhp=maxhp+%s,curhp=curhp+%s WHERE name=\'%s\'' % (boostVal*hpBoostMod,boostVal*hpBoostMod,trigger.nick))
			bot.reply('\00313Your Max HP has been increased by %s, for a total of %s.' % (boostVal*hpBoostMod,getMaxHP(getPlayerID(trigger.nick))))
		cur.execute('UPDATE players SET boosts=boosts-1,used_boosts=used_boosts+1 WHERE name=\'%s\'' % trigger.nick)
		bot.reply('\00313You have used one stat boost and have %s remaining. You have used %s stat boost(s) total.' % (getBoosts(getPlayerID(trigger.nick)),getUsedBoosts(getPlayerID(trigger.nick))))
		db.commit()
	else:
		bot.reply('\00313Sorry, \'%s\' isn\'t a stat I know of. Try again?' % stat)

# Trade a reroll for a number of stat points
@module.commands('trade')
def tradeReroll(bot, trigger): 
	#testDB(db,cur)
	if not doesExist(trigger.nick):
		bot.reply('\00313Your player needs to exist first! Say \'.createplayer\' to get started.')
	elif getRerolls(getPlayerID(trigger.nick)) < 1:
		bot.reply('\00313You don\'t have any rerolls to trade!')
	else:
		cur.execute('UPDATE players SET rerolls=rerolls-1,boosts=boosts+%s WHERE name=\'%s\'' % (rollBoostRate,trigger.nick))
		bot.reply('\00313You now have one fewer reroll, a total of %s remaining.' % getRerolls(getPlayerID(trigger.nick)))
		bot.reply('\00313You now have %s additional stat boost(s), for a total of %s.' % (rollBoostRate,getBoosts(getPlayerID(trigger.nick))))
		db.commit()

# Challenges another player to a duel
@module.commands('challenge')
def challengePlayer(bot, trigger):
	#testDB(db,cur)
	if not doesExist(trigger.nick):
		bot.reply('\00313Your player needs to exist first! Say \'.createplayer\' to get started.')
	elif not doesExist(trigger.group(2)):
		bot.reply('\00313There is no player called %s, I\'m afraid. Tell them to \'.createplayer\'!' % trigger.group(2))
	elif trigger.group(2)==trigger.nick:
		bot.reply('\00313You can\'t challenge yourself!')
	else:
		# check to see if there are any active duels with the player
		cur.execute('SELECT * FROM players WHERE name=%s AND currentduel IS NOT NULL', (trigger.nick,))
		activeDuel = cur.fetchone()
		# check to see if the player is already waiting for a response
		cur.execute('SELECT * FROM duels WHERE Challenger=%s AND accepted=false;' % getPlayerID(trigger.nick))
		youChallenging = cur.fetchone()
		# check to see if the player is being waited on for a response
		cur.execute('SELECT * FROM duels WHERE Defender=%s AND accepted=false;' % getPlayerID(trigger.nick))
		youWaiting = cur.fetchone()
		# check to see if the challenged has any active duels
		cur.execute('SELECT * FROM players WHERE name=%s AND currentduel IS NOT NULL', (trigger.group(2),))
		themActive = cur.fetchone()
		# check to see if the challenged is waiting on a response
		cur.execute('SELECT * FROM duels WHERE Challenger=%s AND accepted=false;' % getPlayerID(trigger.group(2)))
		themChallenging = cur.fetchone()
		# check to see if the challenged is being waited on for a response
		cur.execute('SELECT * FROM duels WHERE Defender=%s AND accepted=false;' % getPlayerID(trigger.nick))
		themWaiting = cur.fetchone()
		##
		if activeDuel:
			bot.reply('\00313You already have an open duel! Finish that first before stating another!')
		elif youChallenging:
			bot.reply('\00313You already have an open challenge waiting on %s\'s response!' % youChallenging[1])
		elif youWaiting:
			bot.reply('\00313There is already a challenge from %s waiting on your response!' % youWaiting[0])
		elif themActive:
			bot.reply('\00313%s is already in a duel. Wait for them to finish!' % trigger.group(2))
		elif themChallenging:
			bot.reply('\00313%s has challenged %s for a duel and cannot accept duels at this time.' % ((trigger.group(2),themChallenging[1])))
		elif themWaiting:
			bot.reply('\00313%s has been challenged by %s for a duel and cannot accept duels at this time.' % ((trigger.group(2),themWaiting[0])))
		else:
			# creates the duel data 
			chaTot = getMaxHP(getPlayerID(trigger.nick)) + getAtt(getPlayerID(trigger.nick)) + getDef(getPlayerID(trigger.nick)) + getStr(getPlayerID(trigger.nick)) + getDex(getPlayerID(trigger.nick))
			defTot = getMaxHP(getPlayerID(trigger.group(2))) + getAtt(getPlayerID(trigger.group(2))) + getDef(getPlayerID(trigger.group(2))) + getStr(getPlayerID(trigger.group(2))) + getDex(getPlayerID(trigger.group(2)))
			if chaTot > defTot:
				favour = trigger.nick
			elif defTot > chaTot:
				favour = trigger.group(2)
			duelID = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(32))
			cur.execute('INSERT INTO duels VALUES(%s,%s,false,%s,NULL,false,%s,%s,1,0,0);', (getPlayerID(trigger.nick), getPlayerID(trigger.group(2)),getPlayerID(favour),getPlayerID(trigger.group(2)),duelID))
			cur.execute('UPDATE players SET currentduel=%s WHERE id=%s OR id=%s', (duelID,getPlayerID(trigger.nick),getPlayerID(trigger.group(2))))
			bot.say('\00313%s: You are officially challenged to a duel by %s! Say \'.accept\' to begin the battle!' % (trigger.group(2),trigger.nick))
			db.commit()

# Accepts a duel from another player
@module.commands('accept')
def acceptChallenge(bot, trigger):
	#testDB(db,cur)
	if not doesExist(trigger.nick):
		bot.reply('\00313Your player needs to exist first! Say \'.createplayer\' to get started.')
	else:
		cur.execute('SELECT * FROM duels WHERE duelid=%s', (getCurrentDuel(trigger.nick),))
		waiting = cur.fetchone()
		if not waiting:
			bot.reply('\00313You don\'t have any waiting challenges, I\'m afraid. Issue one with \'.challenge <name>\'!')
		elif waiting[5]==1:
			bot.reply('\00313Your duel is already underway!')
		elif waiting[0]==getPlayerID(trigger.nick):
			bot.reply('\00313You can\'t accept your own invitation! You fool!')
		else:
			# Updates the duel once it's confirmed to be valid to be active
			cur.execute('UPDATE duels SET accepted=true, active=true WHERE duelid=%s', (getCurrentDuel(trigger.nick),))
			bot.say('\00313%s: %s has accepted your challenge!' % (getName(waiting[0]),trigger.nick))
			if waiting[3]:
				favourString = 'The favoured player is ' + getName(waiting[3]) + '. '
			else:
				favourString = ''
			bot.say('\00313The duel between %s and %s is now beginning. %sThe defender, %s, has the first move!' % (trigger.nick,getName(waiting[0]),favourString,trigger.nick))
			db.commit()

# Rejects a duel from another player
@module.commands('reject','decline','pansyout')
def rejectChallenge(bot, trigger):
	#testDB(db,cur)
	if not doesExist(trigger.nick):
		bot.reply('\00313Your player needs to exist first! Say \'.createplayer\' to get started.')
	else:
		cur.execute('SELECT * FROM duels WHERE duelid=%s', (getCurrentDuel(trigger.nick),))
		waiting = cur.fetchone()
		if not waiting:
			bot.reply('\00313You don\'t have any waiting challenges to reject. Issue one with \'.challenge <name>\'!')
		elif waiting[5]==1 and waiting[1]==getPlayerID(trigger.nick):
			bot.reply('\00313Too late, you already accepted it! .forfeit if you don\'t want to keep fighting!')
		elif waiting[5]==1:
			bot.reply('\00313Too late, it\'s already been accepted! Not that you can reject your own duels anyway!')
		elif waiting[0]==getPlayerID(trigger.nick):
			bot.reply('\00313you can\'t reject your own duel! You goon!')
		else:
			# Updates the duel once it's confirmed to be valid to be active
			cur.execute('DELETE FROM duels WHERE duelid=%s', (getCurrentDuel(trigger.nick),))
			cur.execute('UPDATE players SET currentduel=NULL WHERE id=%s OR id=%s', (getPlayerID(trigger.nick),waiting[0]))
			bot.say('\00313%s: %s has rejected your duel! "%s", they said!' % (getName(waiting[0]),trigger.nick,trigger.group(2)))
			db.commit()

# Retracts a waiting challenge
@module.commands('retract','maybenot')
def retractChallenge(bot, trigger):
	#testDB(db,cur)
	if not  doesExist(trigger.nick):
		bot.reply('\00313Your player needs to exist first! Say \'.createplayer\' to get started.')
	else:
		cur.execute('SELECT * FROM duels WHERE duelid=%s', (getCurrentDuel(trigger.nick),))
		waiting = cur.fetchone()
		if not waiting:
			bot.reply('\00313You don\'t have any waiting challenges to retract. Issue one with \'.challenge <name>\'!')
		elif waiting[5]==1 and waiting[0]==getPlayerID(trigger.nick):
			bot.reply('\00313Too late, it\'s already been accepted! .forfeit if you don\'t feel like fighting anymore!')
		elif waiting[5]==1:
			bot.reply('\00313Too late, you alread accepted this duel! You can\'t retract someone else\'s duel anyway!')
		elif waiting[1]==getPlayerID(trigger.nick):
			bot.reply('\00313You can\'t retract someone else\'s duel!')
		else:
			# Updates the duel once it's confirmed to be a valid request
			cur.execute('DELETE FROM duels WHERE duelid=%s', (getCurrentDuel(trigger.nick),))
			cur.execute('UPDATE players SET currentduel=NULL WHERE currentduel=%s', (getCurrentDuel(trigger.nick),))
			bot.reply('\00313Your challenge has been retracted!')
			db.commit()

# Attacks a player
@module.commands('attack','attack!')
def attackDuel(bot, trigger):
	random.seed(time.time())
	#testDB(db,cur)
	if not doesExist(trigger.nick):
		bot.reply('\00313Your player needs to exist first! Say \'.createplayer\' to get started.')
	else:
		# determine if the player is actually in a duel or not
		cur.execute('SELECT * FROM duels WHERE (defender=%s OR challenger=%s) AND active=true' % (getPlayerID(trigger.nick),getPlayerID(trigger.nick)))
		duelResults = cur.fetchone()
		if not duelResults:
			cur.execute('SELECT challenger FROM duels WHERE defender=%s AND active=false AND accepted=false' % getPlayerID(trigger.nick))
			cha = cur.fetchone()
			if(cha):
				bot.reply('\00313You have a waiting request from %s! You have to .accept their challenge first!' % getName(cha[0]))
			else:
				bot.reply('\00313You are not currently in a duel! Go .challenge someone!')
		# test to see if it's the player's turn
		elif not (duelResults[6]==getPlayerID(trigger.nick)):
			bot.reply('\00313Wait your turn, it\'s %s\'s turn!' % getName(duelResults[6]))
		elif duelResults[8]==2:
			bot.reply('\00313It\'s your turn to .defend, not attack!')
		else:
			# set the opponent
			if duelResults[0]==getPlayerID(trigger.nick):
				opponent = duelResults[1]
			else:
				opponent = duelResults[0]
			# if it's time to determine your hits
			if duelResults[8]==1:
				rolls = "To hit: "
				hits = 0
				# this loop rolls a number of dice equal to the attacker's Att stat
				for x in range (0,getAtt(getPlayerID(trigger.nick))):
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
				bot.reply('\00313%s -- a grand total of %s hit(s)!' % (rolls,hits))
				# determine Strength hits
				spRolls = "Strength roll: "
				spHits = 0
				for x in range (0,getStr(getPlayerID(trigger.nick))):
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
					bot.reply('\00313Too bad! The turn passes to %s for the next round!' % getName(opponent))
				# sets the dice column to the number of hits, to be used with the next .defend command, and changes the turn and the stage
				else:
					cur.execute('UPDATE duels SET turn=%s,dice=%s,specialdice=%s,stage=2 WHERE duelid=%s', (opponent,hits,spHits,getCurrentDuel(trigger.nick)))
					bot.say('\00313%s: it is your turn to .defend!' % getName(opponent)) # the hits for Attack and for Strength are stored in the duel data
				if showHiddenRolls:
					bot.reply(spRolls)
					bot.reply('\00313Grand total of %s for your strength roll. Shh.....' % str(spHits))
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
				bot.reply('\00313%s -- a grand total of *%s damage*!' % (rolls,hits))
				# aw, zero damage!
				if hits < 1:
					if getStatus(opponent)=='stunned':
						cur.execute('UPDATE duels SET stage=1,dice=0,specialdice=0 WHERE duelid=%s', (getCurrentDuel(trigger.nick),))
						cur.execute('UPDATE players SET status=\'healthy\' WHERE id=%s' % opponent)
						bot.reply('\00313Shame! As %s\'s stun wears off, you have another chance to .attack!' % getName(opponent))
					elif getStatus(opponent)=='healthy':
						cur.execute('UPDATE duels SET turn=%s,stage=1,dice=0 WHERE duelid=%s', (opponent,getCurrentDuel(trigger.nick)))
						bot.reply('\00313Too bad! The turn passes to *%s* for the next round!' % getName(opponent))
					else:
						bot.reply('\00313Something is wrong with the Status column! :o')
				# if the opponent has less current HP than the damage done (or the same amount), they lose! process the final results
				elif getCurHP(opponent) < (hits + 1):
					# set winner to the player, set active duel to false
					cur.execute('UPDATE duels SET winner=%s,active=false WHERE duelid=%s', (getPlayerID(trigger.nick),getCurrentDuel(trigger.nick))) 
					# grant the winner their boost(s) and set HP to max
					cur.execute('UPDATE players SET boosts=boosts+%s,curhp=maxhp,currentduel=NULL,status=\'healthy\' WHERE name=\'%s\'' % (winBoosts,trigger.nick))
					bot.reply('\00313You are the winner of the duel against *%s*! You have gained *%s* stat point(s) for your victory!' % (getName(opponent),winBoosts))
					# grant additional points if the favour bonus is in effect
					if duelResults[3]!=getPlayerID(trigger.nick) and favourPoints:
						cur.execute('UPDATE players SET boosts=boosts+%s WHERE name=\'%s\'' % (favourBoosts,trigger.nick))
						bot.reply('\00313As your opponent was favoured against you, you also gain an additional %s stat point(s)!' % favourBoosts)
					# grant the loser a reroll and set his HP to max
					cur.execute('UPDATE players SET rerolls=rerolls+%s,curhp=maxhp,currentduel=NULL,status=\'healthy\' WHERE id=%s' % (loseRerolls,opponent))
					bot.say('\00313%s: Better luck next time. You get %s stat reroll(s), tradable for %s stat point(s) each.' % (getName(opponent),loseRerolls,rollBoostRate))
					bot.say('\00313The duel between *%s* and *%s* has officially ended. The winner was *%s*! Both of them have been healed back to max. See you next time!' % (getName(duelResults[0]),getName(duelResults[1]),trigger.nick))
				# otherwise, just deal the damage
				else:
					if getStatus(opponent)=='stunned':
						cur.execute('UPDATE duels SET stage=1,dice=0,specialdice=0 WHERE duelid=%s', (getCurrentDuel(trigger.nick),))
						cur.execute('UPDATE players SET status=\'healthy\',curhp=curhp-%s WHERE id=%s' % (hits,opponent))
						bot.say('\00313%s: You have %s/%s HP remaining! Your stun wears off!' % (getName(opponent),getCurHP(opponent),getMaxHP(opponent)))
						bot.reply('\00313It is your chance to .attack again while %s is recovering!' % getName(opponent))
					elif getStatus(opponent)=='healthy':
						cur.execute('UPDATE duels SET turn=%s,dice=0,stage=1 WHERE duelid=%s', (opponent,getCurrentDuel(trigger.nick)))
						cur.execute('UPDATE players SET curhp=curhp-%s WHERE id=%s' % (hits,opponent))
						bot.say('\00313%s: You have %s/%s HP remaining! It is your turn to .attack!' % (getName(opponent),getCurHP(opponent),getMaxHP(opponent)))
					else:
						bot.reply('\00313Something is wrong with the Status column! :o')
			elif duelResults[8]==4:
				rolls = "Riposte roll: "
				hits = 0
				# changing the profile to do Riposte damage
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
				# change the profile back
				setProfile(curProfile)
				rolls = rolls + '!'
				rolls = re.sub(', !', '', rolls)
				bot.reply('\00313%s -- a grand total of *%s riposte damage*!' % (rolls,hits))
				# aw, zero damage!
				if hits < 1:
					cur.execute('UPDATE duels SET stage=1,dice=0 WHERE duelid=%s', (getCurrentDuel(trigger.nick),))
					bot.reply('\00313Unsuccessful riposte, but it\'s now your turn to .attack!')
				# if the opponent has less current HP than the damage done (or the same amount), they lose! process the final results
				elif getCurHP(opponent) < (hits + 1):
					# set winner to the player, set active duel to false
					cur.execute('UPDATE duels SET winner=%s,active=false WHERE duelid=%s', (getPlayerID(trigger.nick),getCurrentDuel(trigger.nick))) 
					# grant the winner their boost(s) and set HP to max
					cur.execute('UPDATE players SET boosts=boosts+%s,curhp=maxhp,currentduel=NULL,status=\'healthy\' WHERE name=\'%s\'' % (winBoosts,trigger.nick))
					bot.reply('\00313You are the winner of the duel against *%s*! You have gained *%s* stat point(s) for your victory!' % (getName(opponent),winBoosts))
					# grant additional points if the favour bonus is in effect
					if duelResults[3]!=getPlayerID(trigger.nick) and favourPoints:
						cur.execute('UPDATE players SET boosts=boosts+%s WHERE name=\'%s\'' % (favourBoosts,trigger.nick))
						bot.reply('\00313As your opponent was favoured against you, you also gain an additional %s stat point(s)!' % favourBoosts)
					# grant the loser a reroll and set his HP to max
					cur.execute('UPDATE players SET rerolls=rerolls+%s,curhp=maxhp,currentduel=NULL,status=\'healthy\' WHERE id=%s' % (loseRerolls,opponent))
					bot.say('\00313%s: Better luck next time. You get %s stat reroll(s), tradable for %s stat point(s) each.' % (getName(opponent),loseRerolls,rollBoostRate))
					bot.say('\00313The duel between *%s* and *%s* has officially ended. The winner was *%s*! Both of them have been healed back to max. See you next time!' % (getName(duelResults[0]),getName(duelResults[1]),trigger.nick))
				# otherwise, just deal the damage
				else:
					cur.execute('UPDATE duels SET stage=1,dice=0 WHERE duelid=%s', (getCurrentDuel(trigger.nick),))
					cur.execute('UPDATE players SET curhp=curhp-%s WHERE id=%s' % (hits,opponent))
					bot.say('\00313%s: You have %s/%s HP remaining!' % (getName(opponent),getCurHP(opponent),getMaxHP(opponent)))
					bot.reply('\00313Successful riposte! It is your turn to .attack!')

			else:
				bot.reply('\00313Not really sure how you got here....the Stage column must be messed up. Check it out!')
			db.commit()

# The defend command!
@module.commands('defend')
def defendDuel(bot, trigger):
	random.seed(time.time())
	#testDB(db,cur)
	if not doesExist(trigger.nick):
		bot.reply('\00313Your player needs to exist first! Say \'.createplayer\' to get started.')
	else:
		# determine if the player is actually in a duel or not
		cur.execute('SELECT * FROM duels WHERE (defender=%s OR challenger=%s) AND active=true' % (getPlayerID(trigger.nick),getPlayerID(trigger.nick)))
		duelResults = cur.fetchone()
		if not duelResults:
			cur.execute('SELECT challenger FROM duels WHERE defender=%s AND active=false AND accepted=false' % getPlayerID(trigger.nick))
			cha = cur.fetchone()
			if(cha):
				bot.reply('\00313You have a waiting request from %s! You have to .accept their challenge first!' % cha[0])
			else:
				bot.reply('\00313You are not currently in a duel! Go .challenge someone!')
		# test to see if it's the player's turn
		elif not (duelResults[6]==getPlayerID(trigger.nick)):
			bot.reply('\00313Wait your turn, it\'s %s\'s turn!' % getName(duelResults[6]))
		elif duelResults[8]==1 or duelResults[8]==3 or duelResults[8]==4:
			bot.reply('\00313It\'s your turn to .attack, not defend!')
		elif duelResults[8]==2:
			rolls = "\00313Defense roll: "
			hits = 0
			if duelResults[0]==getPlayerID(trigger.nick):
				opponent = duelResults[1]
			else:
				opponent = duelResults[0]
			# this loop rolls dice equal to the player's defense stat
			for x in range (0,getDef(getPlayerID(trigger.nick))):
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
			if DEBUG:
				bot.reply('These are the stats we are working with:')
				bot.reply('%s is dex of player, %s is dexDie, %s is DexThr, %s is dubDex, %s is duDxTh, %s is negDex, and %s is neDxTh' % (getDex(getPlayerID(trigger.nick)),dexDie,dexThr,dubDex,duDxTh,negDex,neDxTh))
			for x in range (0,getDex(getPlayerID(trigger.nick))):
				tRoll = random.randint(1,dexDie)
				spRolls = spRolls + str(tRoll) + ', '
				# do i really need to say it?
				if tRoll > (dexThr - 1):
					if dubDex and tRoll > (duDxTh - 1):
						spHits = spHits + 2
						if DEBUG:
							bot.say('%d: dub hit!' % tRoll)
					else:
						spHits = spHits + 1
						if DEBUG:
							bot.say('%d: hit!' % tRoll)
				elif negDex and tRoll < (neDxTh + 1):
					spHits = spHits - 1
					if DEBUG:
						bot.say('%d: negative hit!' % tRoll)
				elif DEBUG:
					bot.say('%d: no hit!' % tRoll)
				if DEBUG:
					bot.say('%d total so far!' % spHits)
			spRolls = spRolls + '!'
			spRolls = re.sub(', !', '', spRolls)
			bot.reply('%s -- a grand total of _%s hit(s)_!' % (rolls,hits))
			if showHiddenRolls:
				bot.reply(spRolls)
				bot.reply('You got a Dex roll of %s. Shhh....' % spHits)
			## duelResults[9] is the Hit roll from last time, and [10] is the Str roll
			isStun = False
			isRiposte = False
			
			if mayStun(duelResults[10],hits) and mayRiposte(spHits,duelResults[9],hits):
				if (duelResults[10] + duelResults[9]) > (hits + spHits):
					isStun = True
				elif (duelResults[10] + duelResults[9]) < (hits + spHits):
					isRiposte = True
			elif mayStun(duelResults[10],hits):
				isStun = True
			elif mayRiposte(spHits,duelResults[9],hits):
				isRiposte = True
			
	#		elif duelResults[10] > ((2 * hits) - 1) and duelResults[10] > 0:
	#			isStun = True
	#		elif spHits > ((2 * duelResults[9]) - 1) and spHits > 0:
	#			isRiposte = True
			# react according to the situation, ie stun, riposte, neither
			newDice = duelResults[9] - hits
			if isStun:
				if showWinningRolls:
					bot.say('\00313%s got a dex roll of %d, and %s got a str roll of %d.' % (trigger.nick,spHits,getName(opponent),duelResults[10]))
				if hits < 1:
					cur.execute('UPDATE duels SET turn=%s,stage=3,dice=%s,specialdice=0 WHERE duelid=%s', (opponent,newDice,getCurrentDuel(trigger.nick)))
					cur.execute('UPDATE players SET status=\'stunned\' WHERE id=%s' % getPlayerID(trigger.nick))
					bot.reply('\00313Too bad! Unfortunately, %s\'s blow manages to stun you! The turn passes to them for damage!' % getName(opponent))
				elif newDice < 1:
					cur.execute('UPDATE duels SET turn=%s,stage=1,dice=0,specialdice=0 WHERE duelid=%s', (opponent,getCurrentDuel(trigger.nick)))
					bot.reply('\00313Your armour holds, no damage for %s! Their strike winds you though, leaving you stunned! The turn passes back to them for a new .attack!' % getName(opponent))
				else:
					cur.execute('UPDATE duels SET turn=%s,stage=3,dice=%s,specialdice=0 WHERE duelid=%s', (opponent,newDice,getCurrentDuel(trigger.nick)))
					cur.execute('UPDATE players SET status=\'stunned\' WHERE name=\'%s\'' % trigger.nick)
					bot.reply('\00313Your armour blocks some of the attack, but %s\'s blow winds you!' % getName(opponent))
					bot.say('\00313%s: You have _%s_ remaining dice for damage, and you will have the opportunity to .attack again after due to your stun!' % (getName(opponent),newDice))
			elif isRiposte:
				if not fixedRiposte:
					riposteDice = int(((spHits + hits) / 2) - duelResults[9])
				if showWinningRolls:
					bot.say('\00313%s got a dex roll of %d, and %s got a str roll of %d.' % (trigger.nick,spHits,getName(opponent),duelResults[10]))
				if hits < 1: # currently we're determining riposte dice by whatever your dex roll was EDIT: now we're just giving you 6 EDITEDIT: now that depends if a variable is set, see above
					cur.execute('UPDATE duels SET stage=4,dice=%s,specialdice=0 WHERE duelid=%s', (riposteDice,getCurrentDuel(trigger.nick)))
					bot.reply('\00313Your....uh...armour sucks but...your weapon is fast! ...I guess.... Either way, you successfully riposte.')
				elif newDice < 1:
					cur.execute('UPDATE duels SET stage=4,dice=%s,specialdice=0 WHERE duelid=%s', (riposteDice,getCurrentDuel(trigger.nick)))
					bot.reply('\00313You are able to swiftly and deftly parry %s\'s attack away! You can now .attack with a riposte!' % getName(opponent))
				else:
					cur.execute('UPDATE duels SET stage=4,dice=%s,specialdice=0 WHERE duelid=%s', (riposteDice,getCurrentDuel(trigger.nick)))
					bot.reply('\00313%s\'s attack nearly strikes you, but you parry them away at the last second, catching them off guard! You can now .attack with a riposte!' % getName(opponent))
			else:
				if hits < 1:
					cur.execute('UPDATE duels SET turn=%s,stage=3 WHERE duelid=%s', (opponent,getCurrentDuel(trigger.nick)))
					bot.reply('\00313Too bad! The turn passes to *%s* for damage, with %s dice at their disposal!' % (opponent,duelResults[9]))
				elif newDice < 1:
					cur.execute('UPDATE duels SET stage=1,dice=0,specialdice=0 WHERE duelid=%s', (getCurrentDuel(trigger.nick),))
					bot.reply('\00313Your armour holds, no damage for %s! It is your turn to .attack!' % getName(opponent))
				else:
					cur.execute('UPDATE duels SET turn=%s,stage=3,dice=%s WHERE duelid=%s', (opponent,newDice,getCurrentDuel(trigger.nick)))
					bot.say('\00313%s: You have _%s_ dice remaining for damage. It is your turn to .attack!' % (getName(opponent),newDice))
			db.commit()

# The forfeit command!
@module.commands('forfeit')
def forfeitDuel(bot, trigger):
	#testDB(db,cur)
	if not doesExist(trigger.nick):
		bot.reply('\00313Your player needs to exist first! Say \'.createplayer\' to get started.')
	else:
		cur.execute('SELECT * FROM duels WHERE duelid=%s AND active=true', (getCurrentDuel(trigger.nick),))
		duelResults = cur.fetchone()
		if not duelResults:
			bot.reply('\00313You are not currently in a duel! Go .challenge someone before giving up!')
		else:
			if duelResults[0]==getPlayerID(trigger.nick):
				opponent = duelResults[1]
			else:
				opponent = duelResults[0]
			cur.execute('UPDATE duels SET winner=%s,active=false WHERE duelid=%s', (opponent,getCurrentDuel(trigger.nick)))
			# grant the winner their boost(s) and set HP to max
			cur.execute('UPDATE players SET boosts=boosts+%s,curhp=maxhp,currentduel=null WHERE id=%s' % (winBoosts,opponent))
			bot.say('\00313%s: You are the winner of the duel against %s! You have gained %s stat point(s) for your victory!' % (getName(opponent),trigger.nick,winBoosts))
		# grant the loser a reroll and set his HP to max
			cur.execute('UPDATE players SET rerolls=rerolls+%s,curhp=maxhp,currentduel=null WHERE name=\'%s\'' % (loseRerolls,trigger.nick))
			bot.reply('\00313Better luck next time. You get %s stat reroll(s), tradable for %s stat point(s) each.' % (loseRerolls,rollBoostRate))
			bot.say('\00313The duel between %s and %s has officially ended. The winner was %s! Both of them have been healed back to max. See you next time!' % (getName(duelResults[0]),getName(duelResults[1]),getName(opponent)))
			db.commit()

#######################
## EQUIPMENT FUNCTIONS
#######################
# Show equipped gear
@module.commands('equipped')
def getEquipped(bot, trigger):
	if not doesExist(trigger.nick):
		bot.reply('\00313You need to .createplayer first!')
	else:
		results = list(getInventory(getPlayerID(trigger.nick)))
		results.pop(0)
		results.pop(8)
		naked = True
		for x in results:
			if x:
				naked = False
		if naked:
			bot.reply('\00313You are naked!!!!')
		else:
			if results[0]:
				bot.reply('\00313Head: %s' % getExistName(results[0]))
			if results[1]:
				bot.reply('\00313Shoulders: %s' % getExistName(results[1]))
			if results[2]:
				bot.reply('\00313Hands: %s' % getExistName(results[2]))
			if results[3]:
				bot.reply('\00313Legs: %s' % getExistName(results[3]))
			if results[4]:
				bot.reply('\00313Feet: %s' % getExistName(results[4]))
			if results[5]:
				bot.reply('\00313Back: %s' % getExistName(results[5]))
			if results[6] and results[6]==results[7]:
				bot.reply('\00313Main and off hand: %s' % getExistName(results[6]))
			else:
				if results[6]:
					bot.reply('\00313Main Hand: %s' % getExistName(results[6]))
				if results[7]:
					bot.reply('\00313Off Hand: %s' % getExistName(results[7]))

# show held items, i.e. in the Other column in the inventory table
@module.commands('inventory')
def getMyInventory(bot, trigger):
	if not doesExist(trigger.nick):
		bot.reply('\00313You need to .createplayer first!')
	else:
		results = getInventory(getPlayerID(trigger.nick))[9]
		if not results:
			bot.reply('\00313You are not holding anything.')
		else:
			results = results.split()
			holding = ''
			for x in results:
				if holding:
					holding = holding + ', ' + str(x) + ' -- ' + getExistName(x)
				else:
					holding = str(x) + ' -- ' + getExistName(x)
			bot.reply('\00313You have, in your inventory, the following items:')
			bot.reply('\00313%s' % holding)

# TODO: THE BIG ONE TODO
# Equip an item from inventory
@module.commands('equip')
def equipItem(bot, trigger):
	if not doesExist(trigger.nick):
		bot.reply('\00313You need to .createplayer first.')
	else:
		PID = getPlayerID(trigger.nick)
		rest = trigger.group(2)
		if not rest:
			bot.reply('\00313You need to specify what you want to equip. Check your .inventory to see your item IDs.')
		else:
			rest = rest.split()
			if getItemType(getExistID(rest[0]))=='weapon' and not len(rest)==2 and getWeaponHand(getExistID(rest[0]))=='one':
				bot.reply('\00313You need to specify which hand the weapon is going to, as in \'.equip # HAND\', where # is the item ID and HAND is \'main\' or \'off\'.')
			else:
				inventory = getInventory(PID)
				if getItemType(getExistID(rest[0])) == 'weapon':
					hand = getWeaponHand(getExistID(rest[0]))
					if hand=='main' and inventory[7]:
						bot.reply('\00313Your main hand is occupied by your %s. You must .unequip it first!' % getExistName(inventory[7]))
						return
					elif hand=='main':
						cur.execute('UPDATE inventory SET MainHand=%s WHERE ID=%s', (rest[0],PID))
						bot.reply('\00313You are now wielding your %s in your main hand.' % getExistName(rest[0]))
					elif hand=='off' and inventory[8]:
						bot.reply('\00313Your off hand is occupied by your %s. You must .unequip it first!' % getExistName(inventory[8]))
						return
					elif hand=='off':
						cur.execute('UPDATE inventory SET OffHand=%s WHERE ID=%s', (rest[0],PID))
						bot.reply('\00313You are now wielding your %s in your off hand.' % getExistName(rest[0]))
					elif hand=='both' and (inventory[7] or inventory[8]):
						if inventory[7] and inventory[8]:
							bot.reply('\00313Your main hand is occupied by your %s, and your off hand is occupied by your %s. You must .unequip them first!' % (getExistName(inventory[7]),getExistName(inventory[8])))
						elif inventory[7]:
							bot.reply('\00313Your main hand is occupied by your %s. You must .unequip it first!' % getExistName(inventory[7]))
						else:
							bot.reply('\00313Your off hand is occupied by your %s. You must .unequip it first!' % getExistName(inventory[8]))
					elif hand=='both':
						cur.execute('UPDATE inventory SET MainHand=%s,OffHand=%s WHERE ID=%s', (rest[0],rest[0],PID))
						bot.reply('\00313You are now wielding your %s in both hands.' % getExistName(rest[0]))
					elif hand=='one':
						if rest[1]=='main' and inventory[7]:
							bot.reply('\00313Your main hand is occupied by your %s. You must .unequip it first!' % getExistName(inventory[7]))
							return
						elif rest[1]=='main':
							cur.execute('UPDATE inventory SET MainHand=%s WHERE ID=%s', (rest[0],PID))
							bot.reply('\00313You are now wielding your %s in your main hand.' % getExistName(rest[0]))
						elif rest[1]=='off' and inventory[8]:
							bot.reply('\00313Your off hand is occupied by your %s. You must .unequip it first!' % getExistName(inventory[8]))
							return
						elif rest[1]=='off':
							cur.execute('UPDATE inventory SET OffHand=%s WHERE ID=%s', (rest[0],PID))
							bot.reply('\00313You are now wielding your %s in your off hand.' % getExistName(rest[0]))
						else:
							bot.reply('\00313\'%s\' isn\'t a hand. You need to indicate \'main\' or \'off\'.')
							return
					else:
						bot.reply('\00313Uhh...You shouldn\'t be seeing this. There must be something messed up in this item\'s Hand column. Check it out!')
						return
				elif getItemType(getExistID(rest[0]))=='armour':
					slot = getArmourSlot(getExistID(rest[0]))
					if slot=='head' and inventory[1]:
						bot.reply('You are already wearing your %s on your head. You must .unequip it first!' % getExistName(inventory[1]))
						return
					elif slot=='head':
						cur.execute('UPDATE inventory SET Head=%s WHERE ID=%s', (rest[0],PID))
						bot.reply('\00313Your %s is now on your head.' % getExistName(rest[0]))
					elif slot=='shoulders' and inventory[2]:
						bot.reply('\00313You are already wearing your %s on your shoulders. You must .unequip them first!' % getExistName(inventory[2]))
						return
					elif slot=='shoulders':
						cur.execute('UPDATE inventory SET Shoulders=%s WHERE ID=%s', (rest[0],PID))
						bot.reply('\00313Your %s are now on your shoulders.' % getExistName(rest[0]))
					elif slot=='hands' and inventory[3]:
						bot.reply('\00313You are already wearing your %s on your hands. You must .unequip it first!' % getExistName(inventory[2]))
						return
					elif slot=='hands':
						cur.execute('UPDATE inventory SET Hands=%s WHERE ID=%s', (rest[0],PID))
						bot.reply('\00313Your %s are now on your hands.' % getExistName(rest[0]))
					elif slot=='legs' and inventory[4]:
						bot.reply('\00313You are already wearing your %s on your legs. You must .unequip them first!' % getExistName(inventory[2]))
						return
					elif slot=='legs':
						cur.execute('UPDATE inventory SET Legs=%s WHERE ID=%s', (rest[0],PID))
						bot.reply('\00313Your %s are now on your legs.' % getExistName(rest[0]))
					elif slot=='feet' and inventory[5]:
						bot.reply('\00313You are already wearing your %s on your feet. You must .unequip them first!' % getExistName(inventory[2]))
						return
					elif slot=='feet':
						cur.execute('UPDATE inventory SET Feet=%s WHERE ID=%s', (rest[0],PID))
						bot.reply('\00313Your %s are now on your feet.' % getExistName(rest[0]))
					elif slot=='back' and inventory[6]:
						bot.reply('\00313You are already wearing your %s on your back. You must .unequip it first!' % getExistName(inventory[2]))
						return
					elif slot=='back':
						cur.execute('UPDATE inventory SET Shoulders=%s WHERE ID=%s', (rest[0],PID))
						bot.reply('\00313Your %s is now on your back.' % getExistName(rest[0]))
					else:
						bot.reply('\00313Errr.....You really shouldn\'t be seeing this. There must be something messed up in this item\'s Slot column. Check it out!')
						return
				else:
					bot.reply('\00313This item is not equippable.')
					return
				removeFromInventory(PID,rest[0])

# Unequip a slot
@module.commands('unequip')
def unequipItem(bot, trigger):
	if not doesExist(trigger.nick):
		bot.reply('\00313You need to .createplayer first.')
	elif not trigger.group(2):
		bot.reply('\00313You need to specify which slot you want to unequip.')
	else:
		PID = getPlayerID(trigger.nick)
		inventory = list(getInventory(PID))
		inventory.pop(0)
		inventory.pop(8)
		naked = True
		for x in inventory:
			if x:
				naked = False
		if naked:
			bot.reply('\00313You\'re naked!')
		else:
			slot = trigger.group(2)
			if slot == 'head' and inventory[0]:
				thing = inventory[0]
				addToInventory(PID,inventory[0])
				cur.execute('UPDATE inventory SET Head=null WHERE ID=%d' % PID)
			elif slot == 'shoulders' and inventory[1]:
				thing = inventory[1]
				addToInventory(PID,inventory[1])
				cur.execute('UPDATE inventory SET Shoulders=null WHERE ID=%d' % PID)
			elif slot == 'hands' and inventory[2]:
				thing = inventory[2]
				addToInventory(PID,inventory[2])
				cur.execute('UPDATE inventory SET Hands=null WHERE ID=%d' % PID)
			elif slot == 'legs' and inventory[3]:
				thing = inventory[3]
				addToInventory(PID,inventory[3])
				cur.execute('UPDATE inventory SET Legs=null WHERE ID=%d' % PID)
			elif slot == 'feet' and inventory[4]:
				thing = inventory[4]
				addToInventory(PID,inventory[4])
				cur.execute('UPDATE inventory SET Feet=null WHERE ID=%d' % PID)
			elif slot == 'back' and inventory[5]:
				thing = inventory[5]
				addToInventory(PID,inventory[5])
				cur.execute('UPDATE inventory SET Back=null WHERE ID=%d' % PID)
			elif slot == 'main' and inventory[6] and inventory[6]==inventory[7]:
				thing = inventory[6]
				addToInventory(PID,inventory[6])
				cur.execute('UPDATE inventory SET MainHand=null,OffHand=null WHERE ID=%d' % PID)
			elif slot == 'main' and inventory[6]:
				thing = inventory[6]
				addToInventory(PID,inventory[6])
				cur.execute('UPDATE inventory SET MainHand=null WHERE ID=%d' % PID)
			elif slot == 'off' and inventory[7]:
				thing = inventory[7]
				addToInventory(PID,inventory[7])
				cur.execute('UPDATE inventory SET OffHand=null WHERE ID=%d' % PID)
			else:
				bot.reply('\00313You have nothing equipped in slot %s.' % slot)
				return
			bot.reply('\00313Your %s has been unequipped and returned to your inventory.' % getExistName(thing))
			db.commit()

####################################
#### DEBUGGING AND ADMIN FUNCTIONS
####################################
# override the help command
@module.commands('help')
def help(bot, trigger):
	bot.reply('\00313No help for you!')


# FOR DEBUG ONLY!!!!!!
@module.commands('debug')
def runDebug(bot, trigger):
	if DEBUG_CONTROL:
		canDebug = False
		for x in DEBUGGERS:
			if trigger.nick == x:
				canDebug = True
		if not canDebug:
			bot.reply('You aren\'t allowed to run this command.')
		elif trigger.group(2)=='commit':
			db.commit()
			bot.reply('Successful commit.')
		elif trigger.group(2)=='selftest':
			cur.execute('INSERT INTO duels (%s,%s,true,0,NULL,true,%s,%s,1,0,0)', (getPlayerID(trigger.nick),getPlayerID(trigger.nick),getPlayerID(trigger.nick),'loltesting'))
			bot.reply('Self-test duel created.')
		else:
			cur.execute(trigger.group(2))
			bot.reply('Query was successful.')

# FOR ADMIN ADDITIONS, NOT USING DEBUG. EASE OF USE?
@module.commands('admin')
def runAdmin(bot, trigger):
	if ADMIN_CONTROL:
		canAdmin = False
		for x in ADMINS:
			if trigger.nick == x:
				canAdmin = True
		if not canAdmin:
			bot.reply('You aren\'t allowed to run this command.')
		else:
			com = trigger.group(2).split()
			cSize = len(com)
			# the list command.
			if com[0].lower() == 'list':
				# make sure that something has actually been chosen
				if cSize > 1:
					# listing all defined items
					if com[1].lower() == 'items':
						cur.execute('SELECT Name FROM item_definitions')
						results = cur.fetchall()
						if results:
							for name in results:
								bot.reply('\00313%s' % name)
						else:
							bot.reply('No item definitions.')
					# listing all duel data
					elif com[1].lower() == 'duels':
						cur.execute('SELECT * FROM duels')
						results = cur.fetchall()
						if results:
							for duel in results:
								isActive = 'inactive'
								if results[2]:
									isActive = 'active'
								bot.reply('\00313%s vs %s, %s' % (getName(results[0]),getName(results[1]),isActive))
						else:
							bot.reply('No duel data.')
					else:
						bot.reply('No list called \'%s\'.' % com[1])
				else:
					bot.reply('Need to specify a target for command \'list\'.')
			elif com[0].lower() == 'give':
				# make sure that something has been chosen and a player has been selected
				if cSize > 2:
					# making sure the player exists
					if doesExist(com[1]):
						player = com.pop(1)
						com.pop(0)
						newItem = ' '.join(com)
						# making sure the item exists 
						if doesItemExist(newItem):
							cur.execute('INSERT INTO items VALUES(NULL,%d,%d,\'new\')' % (getItemID(newItem),getPlayerID(player)))
							cur.execute('SELECT LAST_INSERT_ID()')
							newID = cur.fetchone()[0]
							cur.execute('SELECT Inventory FROM inventory WHERE ID=%d' % getPlayerID(player))
							inventory = cur.fetchone()[0]
							if inventory:
								inventory = inventory + ' ' + str(newID)
							else:
								inventory = str(newID)
							cur.execute('UPDATE inventory SET Inventory=%s WHERE ID=%s', (inventory,getPlayerID(player)))
							bot.reply('\00313%s created and given to %s.' % (newItem,player))
							db.commit()
						else:
							bot.reply('\00313That is not an existing item.')
					else:
						bot.reply('\00313That is not an existing player.')
				else:
					bot.repl('\00313You need to specify what to give.')
			else:
				bot.reply('No command called \'%s\'.' % com[0])
