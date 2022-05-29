import sqlite3

conn = sqlite3.connect('rpg.db',check_same_thread=False,timeout = 10)
cur = conn.cursor()


cur.execute("""CREATE TABLE IF NOT EXISTS rpg_users(
	userid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	tgid INT,
	status INT,
	position INT,
	location INT,
	user_mark TEXT,
	last_status INT
	);
""")


cur.execute("""CREATE TABLE IF NOT EXISTS rpg_users_personage(
	userid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	tgid INT,
	race TEXT,
	name TEXT,
	clas TEXT,
	coins INT,
	gender TEXT,
	exp INT,
	partner INT,
	want_partner INT
	);
""")

cur.execute("""CREATE TABLE IF NOT EXISTS rpg_users_stats(
	userid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	tgid INT,
	hp INT,
	damage INT,
	speed INT,
	energy INT,
	max_energy INT,
	bash INT,
	heal INT,
	miss INT,
	critical INT,
	vampirise INT,
	armour INT,
	block INT,
	spikes INT,
	armour_theft INT,
	damage_theft INT,
	blindness INT,
	net_damage INT,
	poison INT,
	gold_rush INT
	);
""")

cur.execute("""CREATE TABLE IF NOT EXISTS rpg_users_inventory(
	userid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	tgid INT,
	armour INT,
	weapon INT,
	artifact INT,
	pet INT
	);
""")

cur.execute("""CREATE TABLE IF NOT EXISTS reports(
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	tgid INT,
	status INT,
	admin INT,
	question TEXT,
	answer TEXT
	);
""")

cur.execute("""CREATE TABLE IF NOT EXISTS chest(
	userid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	tgid INT,
	type INT,
	item_num INT
	);
""")


cur.execute("""CREATE TABLE IF NOT EXISTS statistic(
	userid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	tgid INT,
	amount_duels INT,
	win_duels INT,
	pve INT,
	color INT,
	chests INT,
	arena INT,
	colizey INT,
	bonus INT,
	rulet INT,
	bet INT,
	referals_gold INT
	);
""")

cur.execute("""CREATE TABLE IF NOT EXISTS bonus(
	userid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	tgid INT,
	rulet_bonus INT,
	day_bonus INT,
	rulet_day INT,
	rulet_hour INT,
	bonus_hour INT,
	bonus_day INT
	);
""")

cur.execute("""CREATE TABLE IF NOT EXISTS users_settings(
	userid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	tgid INT,
	duel_status INT,
	log_status INT,
	autosell_status INT
	);
""")

cur.execute("""CREATE TABLE IF NOT EXISTS users_fold(
	userid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	tgid INT,
	armour_fold TEXT,
	weapon_fold TEXT,
	pet_fold TEXT,
	artifact_fold TEXT,
	teg_fold TEXT
	);
""")

cur.execute("""CREATE TABLE IF NOT EXISTS referals(
	userid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	tgid INT,
	referals INT,
	inviter INT
	);
""")

cur.execute("""CREATE TABLE IF NOT EXISTS mine(
	userid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	tgid INT,
	workers INT,
	max_workers INT,
	gold INT,
	max_gold INT,
	mine_lvl INT
	);
""")



conn.commit()


def RegUser(tgid):
	cur.execute("""INSERT INTO rpg_users(tgid,status, position,user_mark,last_status)
	VALUES(?,0,0,"Пользователь👤",0);""",(tgid,))

	cur.execute("""INSERT INTO rpg_users_personage(tgid, race, name, gender,coins,exp,partner,want_partner,clas)
	VALUES(?,'0','0','0',200,0,0,0,'0');""",(tgid,))

	cur.execute("""INSERT INTO rpg_users_stats(tgid, hp, damage, speed,energy,max_energy,bash,heal,miss,critical,vampirise,armour,block,spikes,armour_theft,damage_theft,blindness,net_damage,poison,gold_rush)
	VALUES(?,25,2,1,100,100,0,0,0,0,0,0,0,0,0,0,0,0,0,0);""",(tgid,))

	cur.execute("""INSERT INTO rpg_users_inventory(tgid, armour, weapon, artifact,pet)
	VALUES(?,0,0,0,0);""",(tgid,))

	cur.execute("""INSERT INTO chest(tgid, type, item_num)
	VALUES(?,'0',0);""",(tgid,))

	cur.execute("""INSERT INTO statistic(tgid, amount_duels, win_duels,pve,color,chests,arena,colizey,bonus,rulet,bet,referals_gold)
	VALUES(?,0,0,0,0,0,0,0,0,0,0,0);""",(tgid,))

	cur.execute("""INSERT INTO bonus(tgid,rulet_bonus,day_bonus,rulet_hour,rulet_day,bonus_hour,bonus_day)
	VALUES(?,0,0,0,0,0,0);""",(tgid,))

	cur.execute("""INSERT INTO users_settings(tgid,duel_status,log_status,autosell_status)
	VALUES(?,1,0,0);""",(tgid,))

	cur.execute("""INSERT INTO users_fold(tgid,armour_fold,weapon_fold,pet_fold,artifact_fold,teg_fold)
	VALUES(?,'','','','','');""",(tgid,))

	cur.execute("""INSERT INTO referals(tgid,referals,inviter)
	VALUES(?,0,0);""",(tgid,))
	conn.commit()

async def MineReg(tgid):
	cur.execute("""INSERT INTO mine(tgid,workers,max_workers,gold,max_gold,mine_lvl)
	VALUES(?,0,25,0,1000,1);""",(tgid,))
	conn.commit()