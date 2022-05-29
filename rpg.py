from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from random import randint
import random
import sqlite3
import rpg_db as db
import rpg_kb as kb
import equip 
import time
import datetime
import enemy
import schedule
from time import perf_counter
import rpg_str as rpgstr
import threading
import math
bot = Bot(token = '1838898111:AAEkKPly6ZFvUV2IPHKZrzEsBKFScA8NjeQ')
#bot = Bot(token = '1793720846:AAEt9Kv0p51_d8zwXLj5Vo7Vhgnt4SDjBNE')
dp = Dispatcher(bot)

connect = sqlite3.connect('rpg.db',check_same_thread=False, timeout = 10)
cursor = connect.cursor()

start_time = time.time()
update_gold = time.time()
bot_name = '@darkworldrpg_bot'
#bot_name = '@test_sexxxl_bot'
print("started")
report_admin = [793368809,498659074,334641189,599608959,907161629,747002915,614356822,819005408,475346109]


now = datetime.datetime.now()
def Update():
	while True:
		global start_time
		global update_gold
		if int(start_time) - int(time.time()) <= -20:
			cursor.execute("UPDATE rpg_users_stats SET energy = 0 WHERE energy < 0")
			connect.commit()
			cursor.execute("UPDATE rpg_users_stats SET energy = energy + 1 WHERE energy < max_energy")
			connect.commit()
			cursor.execute("UPDATE rpg_users_stats SET energy = 0 WHERE energy < 0")
			connect.commit()
			cursor.execute("UPDATE mine SET gold = max_gold WHERE gold > max_gold")
			connect.commit()
			start_time = time.time()
		if int(update_gold) - int(time.time()) <= -1200:
			cursor.execute("UPDATE mine SET gold = gold + (workers * mine_lvl) / 2 WHERE gold < max_gold")
			connect.commit()
			update_gold = time.time()
			now_day = int(now.day)
			cursor.execute("UPDATE bonus SET day_bonus = 0 WHERE bonus_day != ? ",(int(now_day),))
			connect.commit()
			cursor.execute("UPDATE bonus SET rulet_bonus = 0 WHERE rulet_day != ?",(int(now_day),))
			connect.commit()

@dp.message_handler()
async def Commands(msg: types.Message):
	#await msg.delete()
	if msg.text == '/start':
		if msg.chat.id == msg.from_user.id:
			try:
				cursor.execute("SELECT status FROM rpg_users WHERE tgid = ? ",(msg.from_user.id,))
				user_status = int(cursor.fetchone()[0]);
				await msg.reply('Вы уже зарегистрированы!😟')
			except Exception as ex:
				try:
					db.RegUser(msg.from_user.id)
					await bot.send_message(msg.from_user.id,"Здравствуй, путник😊.\nЯ помогу тебе скоротать время в нашем вирутальном мирке🌏.\nЧтобы начать играть тебе нужно создать своего персонажа, приступим?🤗",reply_markup = kb.add_personage_kb)
					cursor.execute("UPDATE rpg_users SET position = 1 WHERE tgid = ? ",(msg.from_user.id,))
					connect.commit()
				except Exception as ex:
					print(ex)
					await bot.send_message(msg.from_user.id,"Возникла ошибка, повторите попытку позже!")
		else:
			await msg.reply('Для регистрации необходимо перейти в личные сообщения!')

	try:		
		cursor.execute("SELECT status FROM rpg_users WHERE tgid = ? ",(msg.from_user.id,))
		user_status = int(cursor.fetchone()[0]);
	except Exception as ex:
		print(3)



	if user_status != 3:
		
		async def CheckMine():
			try:
				cursor.execute("SELECT userid FROM mine WHERE tgid = ? ",(msg.from_user.id,))
				check = int(cursor.fetchone()[0]);
				return True
			except:
				return False

		async def GetItemInfo(item_num,item_type):
			compl_info = ''
			if item_type == 'artifact':
				item_damage = equip.artifacts_arr[item_num].GetArtifact('damage')
				item_speed = equip.artifacts_arr[item_num].GetArtifact('speed')
				item_hp = equip.artifacts_arr[item_num].GetArtifact('hp')
				item_energy = equip.artifacts_arr[item_num].GetArtifact('energy')
				item_critical = equip.artifacts_arr[item_num].GetArtifact('critical')
				item_bash = equip.artifacts_arr[item_num].GetArtifact('bash')
				item_miss = equip.artifacts_arr[item_num].GetArtifact('miss')
				item_heal = equip.artifacts_arr[item_num].GetArtifact('heal')
				item_vampirise = equip.artifacts_arr[item_num].GetArtifact('vampirise')
				item_armour = equip.artifacts_arr[item_num].GetArtifact('armour')
				item_block = equip.artifacts_arr[item_num].GetArtifact('block')
				item_spikes = equip.artifacts_arr[item_num].GetArtifact('spikes')
				item_armour_theft = equip.artifacts_arr[item_num].GetArtifact('armour_theft')
				item_damage_theft = equip.artifacts_arr[item_num].GetArtifact('damage_theft')
				item_blindness = equip.artifacts_arr[item_num].GetArtifact('blindness')
				item_net_damage = equip.artifacts_arr[item_num].GetArtifact('net_damage')
				item_poison = equip.artifacts_arr[item_num].GetArtifact('poison')

				if item_damage > 0:
					compl_info += '\n🗡Бонус к атаке: ' + str(item_damage)
				if item_speed > 0:
					compl_info += '\n💨Бонус к скорости: ' + str(item_speed)
				if item_hp > 0:
					compl_info += '\n💟Бонус к здоровью: ' + str(item_hp)
				if item_energy > 0:
					compl_info += '\n⚡️Бонус к энергии: ' + str(item_energy)
				if item_critical > 0:
					compl_info += '\n🦾Шанс критического урона: ' + str(item_critical)
				if item_bash > 0:
					compl_info += '\n💫Шанс на оглушение: ' + str(item_bash)
				if item_miss > 0:
					compl_info += '\n🎭Шанс на уклонение: ' + str(item_miss)
				if item_heal > 0:
					compl_info += '\n💊Шанс на восстановление здоровья: ' + str(item_heal)
				if item_vampirise > 0:
					compl_info += '\n🩸Шанс эффекта вампиризма: ' + str(item_vampirise)
				if item_armour > 0:
					compl_info += '\n🛡Бонус к броне: ' + str(item_armour)
				if item_block > 0:
					compl_info += '\n🙌Шанс блокировать урон: ' + str(item_block)
				if item_spikes > 0:
					compl_info += '\n🧿Шанс отразить урон: ' + str(item_spikes)
				if item_armour_theft > 0:
					compl_info += '\n♻️Шанс своровать броню: ' + str(item_armour_theft)
				if item_damage_theft > 0:
					compl_info += '\n♻️Шанс своровать урон: ' + str(item_damage_theft)
				if item_blindness > 0:
					compl_info += '\n👁‍🗨Шанс ослепить противника: ' + str(item_blindness)
				if item_net_damage > 0:
					compl_info += '\n✨Шанс на чистый урон: ' + str(item_net_damage)
				if item_poison > 0:
					compl_info += '\n🧪Шанс отравить противника: ' + str(item_poison)



			elif item_type == 'armour':
				item_damage = equip.armour_arr[item_num].GetArmour('damage')
				item_speed = equip.armour_arr[item_num].GetArmour('speed')
				item_hp = equip.armour_arr[item_num].GetArmour('hp')
				item_energy = equip.armour_arr[item_num].GetArmour('energy')
				item_critical = equip.armour_arr[item_num].GetArmour('critical')
				item_bash = equip.armour_arr[item_num].GetArmour('bash')
				item_miss = equip.armour_arr[item_num].GetArmour('miss')
				item_heal = equip.armour_arr[item_num].GetArmour('heal')
				item_vampirise = equip.armour_arr[item_num].GetArmour('vampirise')
				item_armour = equip.armour_arr[item_num].GetArmour('armour')
				item_block = equip.armour_arr[item_num].GetArmour('block')
				item_spikes = equip.armour_arr[item_num].GetArmour('spikes')
				item_armour_theft = equip.armour_arr[item_num].GetArmour('armour_theft')
				item_damage_theft = equip.armour_arr[item_num].GetArmour('damage_theft')
				item_blindness = equip.armour_arr[item_num].GetArmour('blindness')
				item_net_damage = equip.armour_arr[item_num].GetArmour('net_damage')
				item_poison = equip.armour_arr[item_num].GetArmour('poison')

				if item_damage > 0:
					compl_info += '\n🗡Бонус к атаке: ' + str(item_damage)
				if item_speed > 0:
					compl_info += '\n💨Бонус к скорости: ' + str(item_speed)
				if item_hp > 0:
					compl_info += '\n💟Бонус к здоровью: ' + str(item_hp)
				if item_energy > 0:
					compl_info += '\n⚡️Бонус к энергии: ' + str(item_energy)
				if item_critical > 0:
					compl_info += '\n🦾Шанс критического урона: ' + str(item_critical)
				if item_bash > 0:
					compl_info += '\n💫Шанс на оглушение: ' + str(item_bash)
				if item_miss > 0:
					compl_info += '\n🎭Шанс на уклонение: ' + str(item_miss)
				if item_heal > 0:
					compl_info += '\n💊Шанс на восстановление здоровья: ' + str(item_heal)
				if item_vampirise > 0:
					compl_info += '\n🩸Шанс эффекта вампиризма: ' + str(item_vampirise)
				if item_armour > 0:
					compl_info += '\n🛡Бонус к броне: ' + str(item_armour)
				if item_block > 0:
					compl_info += '\n🙌Шанс блокировать урон: ' + str(item_block)
				if item_spikes > 0:
					compl_info += '\n🧿Шанс отразить урон: ' + str(item_spikes)
				if item_armour_theft > 0:
					compl_info += '\n♻️Шанс своровать броню: ' + str(item_armour_theft)
				if item_damage_theft > 0:
					compl_info += '\n♻️Шанс своровать урон: ' + str(item_damage_theft)
				if item_blindness > 0:
					compl_info += '\n👁‍🗨Шанс ослепить противника: ' + str(item_blindness)
				if item_net_damage > 0:
					compl_info += '\n✨Шанс на чистый урон: ' + str(item_net_damage)
				if item_poison > 0:
					compl_info += '\n🧪Шанс отравить противника: ' + str(item_poison)

			elif item_type == 'weapon':
				item_damage = equip.sword_arr[item_num].GetSword('damage')
				item_speed = equip.sword_arr[item_num].GetSword('speed')
				item_hp = equip.sword_arr[item_num].GetSword('hp')
				item_energy = equip.sword_arr[item_num].GetSword('energy')
				item_critical = equip.sword_arr[item_num].GetSword('critical')
				item_bash = equip.sword_arr[item_num].GetSword('bash')
				item_miss = equip.sword_arr[item_num].GetSword('miss')
				item_heal = equip.sword_arr[item_num].GetSword('heal')
				item_vampirise = equip.sword_arr[item_num].GetSword('vampirise')
				item_armour = equip.sword_arr[item_num].GetSword('armour')
				item_block = equip.sword_arr[item_num].GetSword('block')
				item_spikes = equip.sword_arr[item_num].GetSword('spikes')
				item_armour_theft = equip.sword_arr[item_num].GetSword('armour_theft')
				item_damage_theft = equip.sword_arr[item_num].GetSword('damage_theft')
				item_blindness = equip.sword_arr[item_num].GetSword('blindness')
				item_net_damage = equip.sword_arr[item_num].GetSword('net_damage')
				item_poison = equip.sword_arr[item_num].GetSword('poison')

				if item_damage > 0:
					compl_info += '\n🗡Бонус к атаке: ' + str(item_damage)
				if item_speed > 0:
					compl_info += '\n💨Бонус к скорости: ' + str(item_speed)
				if item_hp > 0:
					compl_info += '\n💟Бонус к здоровью: ' + str(item_hp)
				if item_energy > 0:
					compl_info += '\n⚡️Бонус к энергии: ' + str(item_energy)
				if item_critical > 0:
					compl_info += '\n🦾Шанс критического урона: ' + str(item_critical)
				if item_bash > 0:
					compl_info += '\n💫Шанс на оглушение: ' + str(item_bash)
				if item_miss > 0:
					compl_info += '\n🎭Шанс на уклонение: ' + str(item_miss)
				if item_heal > 0:
					compl_info += '\n💊Шанс на восстановление здоровья: ' + str(item_heal)
				if item_vampirise > 0:
					compl_info += '\n🩸Шанс эффекта вампиризма: ' + str(item_vampirise)
				if item_armour > 0:
					compl_info += '\n🛡Бонус к броне: ' + str(item_armour)
				if item_block > 0:
					compl_info += '\n🙌Шанс блокировать урон: ' + str(item_block)
				if item_spikes > 0:
					compl_info += '\n🧿Шанс отразить урон: ' + str(item_spikes)
				if item_armour_theft > 0:
					compl_info += '\n♻️Шанс своровать броню: ' + str(item_armour_theft)
				if item_damage_theft > 0:
					compl_info += '\n♻️Шанс своровать урон: ' + str(item_damage_theft)
				if item_blindness > 0:
					compl_info += '\n👁‍🗨Шанс ослепить противника: ' + str(item_blindness)
				if item_net_damage > 0:
					compl_info += '\n✨Шанс на чистый урон: ' + str(item_net_damage)
				if item_poison > 0:
					compl_info += '\n🧪Шанс отравить противника: ' + str(item_poison)
			elif item_type == 'pet':
				item_damage = equip.pets_arr[item_num].GetPet('damage')
				item_speed = equip.pets_arr[item_num].GetPet('speed')
				item_hp = equip.pets_arr[item_num].GetPet('hp')
				item_energy = equip.pets_arr[item_num].GetPet('energy')
				item_critical = equip.pets_arr[item_num].GetPet('critical')
				item_bash = equip.pets_arr[item_num].GetPet('bash')
				item_miss = equip.pets_arr[item_num].GetPet('miss')
				item_heal = equip.pets_arr[item_num].GetPet('heal')
				item_vampirise = equip.pets_arr[item_num].GetPet('vampirise')
				item_armour = equip.pets_arr[item_num].GetPet('armour')
				item_block = equip.pets_arr[item_num].GetPet('block')
				item_spikes = equip.pets_arr[item_num].GetPet('spikes')
				item_armour_theft = equip.pets_arr[item_num].GetPet('armour_theft')
				item_damage_theft = equip.pets_arr[item_num].GetPet('damage_theft')
				item_blindness = equip.pets_arr[item_num].GetPet('blindness')
				item_net_damage = equip.pets_arr[item_num].GetPet('net_damage')
				item_poison = equip.pets_arr[item_num].GetPet('poison')

				if item_damage > 0:
					compl_info += '\n🗡Бонус к атаке: ' + str(item_damage)
				if item_speed > 0:
					compl_info += '\n💨Бонус к скорости: ' + str(item_speed)
				if item_hp > 0:
					compl_info += '\n💟Бонус к здоровью: ' + str(item_hp)
				if item_energy > 0:
					compl_info += '\n⚡️Бонус к энергии: ' + str(item_energy)
				if item_critical > 0:
					compl_info += '\n🦾Шанс критического урона: ' + str(item_critical)
				if item_bash > 0:
					compl_info += '\n💫Шанс на оглушение: ' + str(item_bash)
				if item_miss > 0:
					compl_info += '\n🎭Шанс на уклонение: ' + str(item_miss)
				if item_heal > 0:
					compl_info += '\n💊Шанс на восстановление здоровья: ' + str(item_heal)
				if item_vampirise > 0:
					compl_info += '\n🩸Шанс эффекта вампиризма: ' + str(item_vampirise)
				if item_armour > 0:
					compl_info += '\n🛡Бонус к броне: ' + str(item_armour)
				if item_block > 0:
					compl_info += '\n🙌Шанс блокировать урон: ' + str(item_block)
				if item_spikes > 0:
					compl_info += '\n🧿Шанс отразить урон: ' + str(item_spikes)
				if item_armour_theft > 0:
					compl_info += '\n♻️Шанс своровать броню: ' + str(item_armour_theft)
				if item_damage_theft > 0:
					compl_info += '\n♻️Шанс своровать урон: ' + str(item_damage_theft)
				if item_blindness > 0:
					compl_info += '\n👁‍🗨Шанс ослепить противника: ' + str(item_blindness)
				if item_net_damage > 0:
					compl_info += '\n✨Шанс на чистый урон: ' + str(item_net_damage)
				if item_poison > 0:
					compl_info += '\n🧪Шанс отравить противника: ' + str(item_poison)

			return compl_info
		async def PlusStatistic(what,when):
			if when == 0:
				if what == 'amount_duels':
					cursor.execute("UPDATE statistic SET amount_duels = amount_duels + 1 WHERE tgid = ? ",(msg.from_user.id,))
					connect.commit()
				elif what == 'win_duels':
					cursor.execute("UPDATE statistic SET win_duels = win_duels + 1 WHERE tgid = ? ",(msg.from_user.id,))
					connect.commit()
				elif what == 'pve':
					cursor.execute("UPDATE statistic SET pve = pve + 1 WHERE tgid = ? ",(msg.from_user.id,))
					connect.commit()
				elif what == 'color':
					cursor.execute("UPDATE statistic SET color = color + 1 WHERE tgid = ? ",(msg.from_user.id,))
					connect.commit()
				elif what == 'chests':
					cursor.execute("UPDATE statistic SET chests = chests + 1 WHERE tgid = ? ",(msg.from_user.id,))
					connect.commit()
			else:
				if what == 'amount_duels':
					cursor.execute("UPDATE statistic SET amount_duels = amount_duels + 1 WHERE tgid = ? ",(when,))
					connect.commit()
				elif what == 'win_duels':
					cursor.execute("UPDATE statistic SET win_duels = win_duels + 1 WHERE tgid = ? ",(when,))
					connect.commit()
				elif what == 'pve':
					cursor.execute("UPDATE statistic SET pve = pve + 1 WHERE tgid = ? ",(when,))
					connect.commit()
				elif what == 'color':
					cursor.execute("UPDATE statistic SET color = color + 1 WHERE tgid = ? ",(when,))
					connect.commit()
				elif what == 'chests':
					cursor.execute("UPDATE statistic SET chests = chests + 1 WHERE tgid = ? ",(when,))
					connect.commit()
		

		async def GetRare(rare):#возвращает редкость предмета в тексте
			rare_text = ' '
			if rare == 0:
				rare_text = 'Обычная⬜️'
			elif rare == 1:
				rare_text = 'Редкая🟦'
			elif rare == 2:
				rare_text = 'Сверхредкая🟩'
			elif rare == 3:
				rare_text = 'Эпическая🟪'
			elif rare == 4:
				rare_text = 'Легендарная🟨'
			elif rare == 5:
				rare_text = 'Реликвия🟧'
			elif rare == 6:
				rare_text = 'Первозданный предмет🟥'
			elif rare == 7:
				rare_text = 'Божественная⬛️'
			else:
				rare_text = "Неизвестная✖️"
			return rare_text
		async def AddItem(item,item_type,who):
			try:
				cursor.execute("SELECT userid FROM rpg_users_inventory WHERE tgid = ? ",(msg.from_user.id,))
				my_userid = int(cursor.fetchone()[0]);
				need_id = my_userid
				if who != 0:
					need_id = who

				if item_type == 'artifact':
					item_text = str(item) + ' '
					cursor.execute("SELECT artifact_fold FROM users_fold WHERE userid = ? ",(need_id,))
					old_fold = cursor.fetchone()[0];
					new_fold = old_fold + item_text
					cursor.execute("UPDATE users_fold SET artifact_fold = ? WHERE userid = ? ",(new_fold,need_id))
					connect.commit()
				elif item_type == 'armour':
					item_text = str(item) + ' '
					cursor.execute("SELECT armour_fold FROM users_fold WHERE userid = ? ",(need_id,))
					old_fold = cursor.fetchone()[0];
					new_fold = old_fold + item_text
					cursor.execute("UPDATE users_fold SET armour_fold = ? WHERE userid = ? ",(new_fold,need_id))
					connect.commit()
				elif item_type == 'pet':
					item_text = str(item) + ' '
					cursor.execute("SELECT pet_fold FROM users_fold WHERE userid = ? ",(need_id,))
					old_fold = cursor.fetchone()[0];
					new_fold = old_fold + item_text
					cursor.execute("UPDATE users_fold SET pet_fold = ? WHERE userid = ? ",(new_fold,need_id))
					connect.commit()
				elif item_type == 'weapon':
					item_text = str(item) + ' '
					cursor.execute("SELECT weapon_fold FROM users_fold WHERE userid = ? ",(need_id,))
					old_fold = cursor.fetchone()[0];
					new_fold = old_fold + item_text
					cursor.execute("UPDATE users_fold SET weapon_fold = ? WHERE userid = ? ",(new_fold,need_id))
					connect.commit()
			except Exception as ex:
				print(ex)
				await msg.reply('Извините, произошла ошибка!🛑')
		async def RemoveItem(item,item_type):
			if item_type == 'artifact':
				cursor.execute("SELECT artifact_fold FROM users_fold WHERE tgid = ? ",(msg.from_user.id,))
				old_fold = cursor.fetchone()[0];
				replaced = str(item) + ' '
				new_fold = old_fold.replace(str(replaced),'',1)
				cursor.execute("UPDATE users_fold SET artifact_fold = ? WHERE tgid = ? ",(new_fold,msg.from_user.id))
				connect.commit()

			elif item_type == 'armour':
				cursor.execute("SELECT armour_fold FROM users_fold WHERE tgid = ? ",(msg.from_user.id,))
				old_fold = cursor.fetchone()[0];
				replaced = str(item) + ' '
				new_fold = old_fold.replace(replaced,'',1)
				cursor.execute("UPDATE users_fold SET armour_fold = ? WHERE tgid = ? ",(new_fold,msg.from_user.id))
				connect.commit()
			elif item_type == 'pet':
				cursor.execute("SELECT pet_fold FROM users_fold WHERE tgid = ? ",(msg.from_user.id,))
				old_fold = cursor.fetchone()[0];
				replaced = str(item) + ' '
				new_fold = old_fold.replace(replaced,'',1)
				cursor.execute("UPDATE users_fold SET pet_fold = ? WHERE tgid = ? ",(new_fold,msg.from_user.id))
				connect.commit()
			elif item_type == 'weapon':
				cursor.execute("SELECT weapon_fold FROM users_fold WHERE tgid = ? ",(msg.from_user.id,))
				old_fold = cursor.fetchone()[0];
				replaced = str(item) + ' '
				new_fold = old_fold.replace(replaced,'',1)
				cursor.execute("UPDATE users_fold SET weapon_fold = ? WHERE tgid = ? ",(new_fold,msg.from_user.id))
				connect.commit()


		async def PlusItem(item_type,userid,item_num):
			if item_type == 'artifact':
				item_damage = equip.artifacts_arr[item_num].GetArtifact('damage')
				item_speed = equip.artifacts_arr[item_num].GetArtifact('speed')
				item_hp = equip.artifacts_arr[item_num].GetArtifact('hp')
				item_energy = equip.artifacts_arr[item_num].GetArtifact('energy')
				item_critical = equip.artifacts_arr[item_num].GetArtifact('critical')
				item_bash = equip.artifacts_arr[item_num].GetArtifact('bash')
				item_miss = equip.artifacts_arr[item_num].GetArtifact('miss')
				item_heal = equip.artifacts_arr[item_num].GetArtifact('heal')
				item_vampirise = equip.artifacts_arr[item_num].GetArtifact('vampirise')
				item_armour = equip.artifacts_arr[item_num].GetArtifact('armour')
				item_block = equip.artifacts_arr[item_num].GetArtifact('block')
				item_spikes = equip.artifacts_arr[item_num].GetArtifact('spikes')
				item_armour_theft = equip.artifacts_arr[item_num].GetArtifact('armour_theft')
				item_damage_theft = equip.artifacts_arr[item_num].GetArtifact('damage_theft')
				item_blindness = equip.artifacts_arr[item_num].GetArtifact('blindness')
				item_net_damage = equip.artifacts_arr[item_num].GetArtifact('net_damage')
				item_poison = equip.artifacts_arr[item_num].GetArtifact('poison')

				cursor.execute("UPDATE rpg_users_inventory SET artifact = ? WHERE tgid = ? ",(item_num,msg.from_user.id))
				connect.commit()

				cursor.execute("UPDATE rpg_users_stats SET damage = damage + ? WHERE tgid = ? ",(item_damage,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET speed = speed + ? WHERE tgid = ? ",(item_speed,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET hp = hp + ? WHERE tgid = ? ",(item_hp,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET max_energy = max_energy + ? WHERE tgid = ? ",(item_energy,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET critical = critical + ? WHERE tgid = ? ",(item_critical,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET bash = bash + ? WHERE tgid = ? ",(item_bash,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET miss = miss + ? WHERE tgid = ? ",(item_miss,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET heal = heal + ? WHERE tgid = ? ",(item_heal,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET vampirise = vampirise + ? WHERE tgid = ? ",(item_vampirise,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET armour = armour + ? WHERE tgid = ? ",(item_armour,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET block = block + ? WHERE tgid = ? ",(item_block,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET spikes = spikes + ? WHERE tgid = ? ",(item_spikes,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET armour_theft = armour_theft + ? WHERE tgid = ? ",(item_armour_theft,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET damage_theft = damage_theft + ? WHERE tgid = ? ",(item_damage_theft,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET blindness = blindness + ? WHERE tgid = ? ",(item_blindness,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET net_damage = net_damage + ? WHERE tgid = ? ",(item_net_damage,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET poison = poison + ? WHERE tgid = ? ",(item_poison,msg.from_user.id))
				connect.commit()

			elif item_type == 'weapon':
				item_damage = equip.sword_arr[item_num].GetSword('damage')
				item_speed = equip.sword_arr[item_num].GetSword('speed')
				item_hp = equip.sword_arr[item_num].GetSword('hp')
				item_energy = equip.sword_arr[item_num].GetSword('energy')
				item_critical = equip.sword_arr[item_num].GetSword('critical')
				item_bash = equip.sword_arr[item_num].GetSword('bash')
				item_miss = equip.sword_arr[item_num].GetSword('miss')
				item_heal = equip.sword_arr[item_num].GetSword('heal')
				item_vampirise = equip.sword_arr[item_num].GetSword('vampirise')
				item_armour = equip.sword_arr[item_num].GetSword('armour')
				item_block = equip.sword_arr[item_num].GetSword('block')
				item_spikes = equip.sword_arr[item_num].GetSword('spikes')
				item_armour_theft = equip.sword_arr[item_num].GetSword('armour_theft')
				item_damage_theft = equip.sword_arr[item_num].GetSword('damage_theft')
				item_blindness = equip.sword_arr[item_num].GetSword('blindness')
				item_net_damage = equip.sword_arr[item_num].GetSword('net_damage')
				item_poison = equip.sword_arr[item_num].GetSword('poison')

				cursor.execute("UPDATE rpg_users_inventory SET weapon = ? WHERE tgid = ? ",(item_num,msg.from_user.id))
				connect.commit()

				cursor.execute("UPDATE rpg_users_stats SET damage = damage + ? WHERE tgid = ? ",(item_damage,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET speed = speed + ? WHERE tgid = ? ",(item_speed,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET hp = hp + ? WHERE tgid = ? ",(item_hp,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET max_energy = max_energy + ? WHERE tgid = ? ",(item_energy,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET critical = critical + ? WHERE tgid = ? ",(item_critical,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET bash = bash + ? WHERE tgid = ? ",(item_bash,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET miss = miss + ? WHERE tgid = ? ",(item_miss,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET heal = heal + ? WHERE tgid = ? ",(item_heal,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET vampirise = vampirise + ? WHERE tgid = ? ",(item_vampirise,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET armour = armour + ? WHERE tgid = ? ",(item_armour,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET block = block + ? WHERE tgid = ? ",(item_block,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET spikes = spikes + ? WHERE tgid = ? ",(item_spikes,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET armour_theft = armour_theft + ? WHERE tgid = ? ",(item_armour_theft,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET damage_theft = damage_theft + ? WHERE tgid = ? ",(item_damage_theft,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET blindness = blindness + ? WHERE tgid = ? ",(item_blindness,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET net_damage = net_damage + ? WHERE tgid = ? ",(item_net_damage,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET poison = poison + ? WHERE tgid = ? ",(item_poison,msg.from_user.id))
				connect.commit()


			elif item_type == 'armour':
				item_damage = equip.armour_arr[item_num].GetArmour('damage')
				item_speed = equip.armour_arr[item_num].GetArmour('speed')
				item_hp = equip.armour_arr[item_num].GetArmour('hp')
				item_energy = equip.armour_arr[item_num].GetArmour('energy')
				item_critical = equip.armour_arr[item_num].GetArmour('critical')
				item_bash = equip.armour_arr[item_num].GetArmour('bash')
				item_miss = equip.armour_arr[item_num].GetArmour('miss')
				item_heal = equip.armour_arr[item_num].GetArmour('heal')
				item_vampirise = equip.armour_arr[item_num].GetArmour('vampirise')
				item_armour = equip.armour_arr[item_num].GetArmour('armour')
				item_block = equip.armour_arr[item_num].GetArmour('block')
				item_spikes = equip.armour_arr[item_num].GetArmour('spikes')
				item_armour_theft = equip.armour_arr[item_num].GetArmour('armour_theft')
				item_damage_theft = equip.armour_arr[item_num].GetArmour('damage_theft')
				item_blindness = equip.armour_arr[item_num].GetArmour('blindness')
				item_net_damage = equip.armour_arr[item_num].GetArmour('net_damage')
				item_poison = equip.armour_arr[item_num].GetArmour('poison')

				cursor.execute("UPDATE rpg_users_inventory SET armour = ? WHERE tgid = ? ",(item_num,msg.from_user.id))
				connect.commit()

				cursor.execute("UPDATE rpg_users_stats SET damage = damage + ? WHERE tgid = ? ",(item_damage,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET speed = speed + ? WHERE tgid = ? ",(item_speed,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET hp = hp + ? WHERE tgid = ? ",(item_hp,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET max_energy = max_energy + ? WHERE tgid = ? ",(item_energy,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET critical = critical + ? WHERE tgid = ? ",(item_critical,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET bash = bash + ? WHERE tgid = ? ",(item_bash,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET miss = miss + ? WHERE tgid = ? ",(item_miss,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET heal = heal + ? WHERE tgid = ? ",(item_heal,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET vampirise = vampirise + ? WHERE tgid = ? ",(item_vampirise,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET armour = armour + ? WHERE tgid = ? ",(item_armour,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET block = block + ? WHERE tgid = ? ",(item_block,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET spikes = spikes + ? WHERE tgid = ? ",(item_spikes,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET armour_theft = armour_theft + ? WHERE tgid = ? ",(item_armour_theft,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET damage_theft = damage_theft + ? WHERE tgid = ? ",(item_damage_theft,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET blindness = blindness + ? WHERE tgid = ? ",(item_blindness,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET net_damage = net_damage + ? WHERE tgid = ? ",(item_net_damage,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET poison = poison + ? WHERE tgid = ? ",(item_poison,msg.from_user.id))
				connect.commit()


			elif item_type == 'pet':
				item_damage = equip.pets_arr[item_num].GetPet('damage')
				item_speed = equip.pets_arr[item_num].GetPet('speed')
				item_hp = equip.pets_arr[item_num].GetPet('hp')
				item_energy = equip.pets_arr[item_num].GetPet('energy')
				item_critical = equip.pets_arr[item_num].GetPet('critical')
				item_bash = equip.pets_arr[item_num].GetPet('bash')
				item_miss = equip.pets_arr[item_num].GetPet('miss')
				item_heal = equip.pets_arr[item_num].GetPet('heal')
				item_vampirise = equip.pets_arr[item_num].GetPet('vampirise')
				item_armour = equip.pets_arr[item_num].GetPet('armour')
				item_block = equip.pets_arr[item_num].GetPet('block')
				item_spikes = equip.pets_arr[item_num].GetPet('spikes')
				item_armour_theft = equip.pets_arr[item_num].GetPet('armour_theft')
				item_damage_theft = equip.pets_arr[item_num].GetPet('damage_theft')
				item_blindness = equip.pets_arr[item_num].GetPet('blindness')
				item_net_damage = equip.pets_arr[item_num].GetPet('net_damage')
				item_poison = equip.pets_arr[item_num].GetPet('poison')

				cursor.execute("UPDATE rpg_users_inventory SET pet = ? WHERE tgid = ? ",(item_num,msg.from_user.id))
				connect.commit()

				cursor.execute("UPDATE rpg_users_stats SET damage = damage + ? WHERE tgid = ? ",(item_damage,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET speed = speed + ? WHERE tgid = ? ",(item_speed,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET hp = hp + ? WHERE tgid = ? ",(item_hp,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET max_energy = max_energy + ? WHERE tgid = ? ",(item_energy,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET critical = critical + ? WHERE tgid = ? ",(item_critical,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET bash = bash + ? WHERE tgid = ? ",(item_bash,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET miss = miss + ? WHERE tgid = ? ",(item_miss,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET heal = heal + ? WHERE tgid = ? ",(item_heal,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET vampirise = vampirise + ? WHERE tgid = ? ",(item_vampirise,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET armour = armour + ? WHERE tgid = ? ",(item_armour,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET block = block + ? WHERE tgid = ? ",(item_block,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET spikes = spikes + ? WHERE tgid = ? ",(item_spikes,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET armour_theft = armour_theft + ? WHERE tgid = ? ",(item_armour_theft,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET damage_theft = damage_theft + ? WHERE tgid = ? ",(item_damage_theft,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET blindness = blindness + ? WHERE tgid = ? ",(item_blindness,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET net_damage = net_damage + ? WHERE tgid = ? ",(item_net_damage,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET poison = poison + ? WHERE tgid = ? ",(item_poison,msg.from_user.id))
				connect.commit()

		async def MinusITem(item_type,userid):
			if item_type == 'artifact':
				cursor.execute("SELECT artifact FROM rpg_users_inventory WHERE tgid = ? ",(msg.from_user.id,))
				item_num = int(cursor.fetchone()[0]);

				item_damage = equip.artifacts_arr[item_num].GetArtifact('damage')
				item_speed = equip.artifacts_arr[item_num].GetArtifact('speed')
				item_hp = equip.artifacts_arr[item_num].GetArtifact('hp')
				item_energy = equip.artifacts_arr[item_num].GetArtifact('energy')
				item_critical = equip.artifacts_arr[item_num].GetArtifact('critical')
				item_bash = equip.artifacts_arr[item_num].GetArtifact('bash')
				item_miss = equip.artifacts_arr[item_num].GetArtifact('miss')
				item_heal = equip.artifacts_arr[item_num].GetArtifact('heal')
				item_vampirise = equip.artifacts_arr[item_num].GetArtifact('vampirise')
				item_armour = equip.artifacts_arr[item_num].GetArtifact('armour')
				item_block = equip.artifacts_arr[item_num].GetArtifact('block')
				item_spikes = equip.artifacts_arr[item_num].GetArtifact('spikes')
				item_armour_theft = equip.artifacts_arr[item_num].GetArtifact('armour_theft')
				item_damage_theft = equip.artifacts_arr[item_num].GetArtifact('damage_theft')
				item_blindness = equip.artifacts_arr[item_num].GetArtifact('blindness')
				item_net_damage = equip.artifacts_arr[item_num].GetArtifact('net_damage')
				item_poison = equip.artifacts_arr[item_num].GetArtifact('poison')

				cursor.execute("UPDATE rpg_users_inventory SET artifact = 0 WHERE tgid = ? ",(msg.from_user.id,))
				connect.commit()

				cursor.execute("UPDATE rpg_users_stats SET damage = damage - ? WHERE tgid = ? ",(item_damage,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET speed = speed - ? WHERE tgid = ? ",(item_speed,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET hp = hp - ? WHERE tgid = ? ",(item_hp,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET max_energy = max_energy - ? WHERE tgid = ? ",(item_energy,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET critical = critical - ? WHERE tgid = ? ",(item_critical,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET bash = bash - ? WHERE tgid = ? ",(item_bash,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET miss = miss - ? WHERE tgid = ? ",(item_miss,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET heal = heal - ? WHERE tgid = ? ",(item_heal,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET vampirise = vampirise - ? WHERE tgid = ? ",(item_vampirise,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET armour = armour - ? WHERE tgid = ? ",(item_armour,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET block = block - ? WHERE tgid = ? ",(item_block,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET spikes = spikes - ? WHERE tgid = ? ",(item_spikes,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET armour_theft = armour_theft - ? WHERE tgid = ? ",(item_armour_theft,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET damage_theft = damage_theft - ? WHERE tgid = ? ",(item_damage_theft,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET blindness = blindness - ? WHERE tgid = ? ",(item_blindness,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET net_damage = net_damage - ? WHERE tgid = ? ",(item_net_damage,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET poison = poison - ? WHERE tgid = ? ",(item_poison,msg.from_user.id))
				connect.commit()

			elif item_type == 'weapon':
				cursor.execute("SELECT weapon FROM rpg_users_inventory WHERE tgid = ? ",(msg.from_user.id,))
				item_num = int(cursor.fetchone()[0]);

				item_damage = equip.sword_arr[item_num].GetSword('damage')
				item_speed = equip.sword_arr[item_num].GetSword('speed')
				item_hp = equip.sword_arr[item_num].GetSword('hp')
				item_energy = equip.sword_arr[item_num].GetSword('energy')
				item_critical = equip.sword_arr[item_num].GetSword('critical')
				item_bash = equip.sword_arr[item_num].GetSword('bash')
				item_miss = equip.sword_arr[item_num].GetSword('miss')
				item_heal = equip.sword_arr[item_num].GetSword('heal')
				item_vampirise = equip.sword_arr[item_num].GetSword('vampirise')
				item_armour = equip.sword_arr[item_num].GetSword('armour')
				item_block = equip.sword_arr[item_num].GetSword('block')
				item_spikes = equip.sword_arr[item_num].GetSword('spikes')
				item_armour_theft = equip.sword_arr[item_num].GetSword('armour_theft')
				item_damage_theft = equip.sword_arr[item_num].GetSword('damage_theft')
				item_blindness = equip.sword_arr[item_num].GetSword('blindness')
				item_net_damage = equip.sword_arr[item_num].GetSword('net_damage')
				item_poison = equip.sword_arr[item_num].GetSword('poison')

				cursor.execute("UPDATE rpg_users_inventory SET weapon = 0 WHERE tgid = ? ",(msg.from_user.id,))
				connect.commit()

				cursor.execute("UPDATE rpg_users_stats SET damage = damage - ? WHERE tgid = ? ",(item_damage,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET speed = speed - ? WHERE tgid = ? ",(item_speed,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET hp = hp - ? WHERE tgid = ? ",(item_hp,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET max_energy = max_energy - ? WHERE tgid = ? ",(item_energy,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET critical = critical - ? WHERE tgid = ? ",(item_critical,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET bash = bash - ? WHERE tgid = ? ",(item_bash,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET miss = miss - ? WHERE tgid = ? ",(item_miss,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET heal = heal - ? WHERE tgid = ? ",(item_heal,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET vampirise = vampirise - ? WHERE tgid = ? ",(item_vampirise,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET armour = armour - ? WHERE tgid = ? ",(item_armour,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET block = block - ? WHERE tgid = ? ",(item_block,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET spikes = spikes - ? WHERE tgid = ? ",(item_spikes,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET armour_theft = armour_theft - ? WHERE tgid = ? ",(item_armour_theft,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET damage_theft = damage_theft - ? WHERE tgid = ? ",(item_damage_theft,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET blindness = blindness - ? WHERE tgid = ? ",(item_blindness,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET net_damage = net_damage - ? WHERE tgid = ? ",(item_net_damage,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET poison = poison - ? WHERE tgid = ? ",(item_poison,msg.from_user.id))
				connect.commit()
			elif item_type == 'armour':
				cursor.execute("SELECT armour FROM rpg_users_inventory WHERE tgid = ? ",(msg.from_user.id,))
				item_num = int(cursor.fetchone()[0]);
				item_damage = equip.armour_arr[item_num].GetArmour('damage')
				item_speed = equip.armour_arr[item_num].GetArmour('speed')
				item_hp = equip.armour_arr[item_num].GetArmour('hp')
				item_energy = equip.armour_arr[item_num].GetArmour('energy')
				item_critical = equip.armour_arr[item_num].GetArmour('critical')
				item_bash = equip.armour_arr[item_num].GetArmour('bash')
				item_miss = equip.armour_arr[item_num].GetArmour('miss')
				item_heal = equip.armour_arr[item_num].GetArmour('heal')
				item_vampirise = equip.armour_arr[item_num].GetArmour('vampirise')
				item_armour = equip.armour_arr[item_num].GetArmour('armour')
				item_block = equip.armour_arr[item_num].GetArmour('block')
				item_spikes = equip.armour_arr[item_num].GetArmour('spikes')
				item_armour_theft = equip.armour_arr[item_num].GetArmour('armour_theft')
				item_damage_theft = equip.armour_arr[item_num].GetArmour('damage_theft')
				item_blindness = equip.armour_arr[item_num].GetArmour('blindness')
				item_net_damage = equip.armour_arr[item_num].GetArmour('net_damage')
				item_poison = equip.armour_arr[item_num].GetArmour('poison')

				cursor.execute("UPDATE rpg_users_inventory SET armour = 0 WHERE tgid = ? ",(msg.from_user.id,))
				connect.commit()

				cursor.execute("UPDATE rpg_users_stats SET damage = damage - ? WHERE tgid = ? ",(item_damage,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET speed = speed - ? WHERE tgid = ? ",(item_speed,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET hp = hp - ? WHERE tgid = ? ",(item_hp,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET max_energy = max_energy - ? WHERE tgid = ? ",(item_energy,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET critical = critical - ? WHERE tgid = ? ",(item_critical,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET bash = bash - ? WHERE tgid = ? ",(item_bash,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET miss = miss - ? WHERE tgid = ? ",(item_miss,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET heal = heal - ? WHERE tgid = ? ",(item_heal,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET vampirise = vampirise - ? WHERE tgid = ? ",(item_vampirise,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET armour = armour - ? WHERE tgid = ? ",(item_armour,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET block = block - ? WHERE tgid = ? ",(item_block,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET spikes = spikes - ? WHERE tgid = ? ",(item_spikes,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET armour_theft = armour_theft - ? WHERE tgid = ? ",(item_armour_theft,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET damage_theft = damage_theft - ? WHERE tgid = ? ",(item_damage_theft,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET blindness = blindness - ? WHERE tgid = ? ",(item_blindness,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET net_damage = net_damage - ? WHERE tgid = ? ",(item_net_damage,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET poison = poison - ? WHERE tgid = ? ",(item_poison,msg.from_user.id))
				connect.commit()
			elif item_type == 'pet':
				cursor.execute("SELECT pet FROM rpg_users_inventory WHERE tgid = ? ",(msg.from_user.id,))
				item_num = int(cursor.fetchone()[0]);

				item_damage = equip.pets_arr[item_num].GetPet('damage')
				item_speed = equip.pets_arr[item_num].GetPet('speed')
				item_hp = equip.pets_arr[item_num].GetPet('hp')
				item_energy = equip.pets_arr[item_num].GetPet('energy')
				item_critical = equip.pets_arr[item_num].GetPet('critical')
				item_bash = equip.pets_arr[item_num].GetPet('bash')
				item_miss = equip.pets_arr[item_num].GetPet('miss')
				item_heal = equip.pets_arr[item_num].GetPet('heal')
				item_vampirise = equip.pets_arr[item_num].GetPet('vampirise')
				item_armour = equip.pets_arr[item_num].GetPet('armour')
				item_block = equip.pets_arr[item_num].GetPet('block')
				item_spikes = equip.pets_arr[item_num].GetPet('spikes')
				item_armour_theft = equip.pets_arr[item_num].GetPet('armour_theft')
				item_damage_theft = equip.pets_arr[item_num].GetPet('damage_theft')
				item_blindness = equip.pets_arr[item_num].GetPet('blindness')
				item_net_damage = equip.pets_arr[item_num].GetPet('net_damage')
				item_poison = equip.pets_arr[item_num].GetPet('poison')

				cursor.execute("UPDATE rpg_users_inventory SET pet = 0 WHERE tgid = ? ",(msg.from_user.id,))
				connect.commit()

				cursor.execute("UPDATE rpg_users_stats SET damage = damage - ? WHERE tgid = ? ",(item_damage,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET speed = speed - ? WHERE tgid = ? ",(item_speed,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET hp = hp - ? WHERE tgid = ? ",(item_hp,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET max_energy = max_energy - ? WHERE tgid = ? ",(item_energy,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET critical = critical - ? WHERE tgid = ? ",(item_critical,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET bash = bash - ? WHERE tgid = ? ",(item_bash,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET miss = miss - ? WHERE tgid = ? ",(item_miss,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET heal = heal - ? WHERE tgid = ? ",(item_heal,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET vampirise = vampirise - ? WHERE tgid = ? ",(item_vampirise,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET armour = armour - ? WHERE tgid = ? ",(item_armour,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET block = block - ? WHERE tgid = ? ",(item_block,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET spikes = spikes - ? WHERE tgid = ? ",(item_spikes,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET armour_theft = armour_theft - ? WHERE tgid = ? ",(item_armour_theft,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET damage_theft = damage_theft - ? WHERE tgid = ? ",(item_damage_theft,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET blindness = blindness - ? WHERE tgid = ? ",(item_blindness,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET net_damage = net_damage - ? WHERE tgid = ? ",(item_net_damage,msg.from_user.id))
				cursor.execute("UPDATE rpg_users_stats SET poison = poison - ? WHERE tgid = ? ",(item_poison,msg.from_user.id))
				connect.commit()


		async def AddCoins(amount,true,message):#выдача золота
			cursor.execute("SELECT coins FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
			nowgold = int(cursor.fetchone()[0]);
			nowgold = nowgold + amount
			cursor.execute("UPDATE rpg_users_personage SET coins = ? WHERE tgid = ? ",(nowgold,msg.from_user.id,))
			connect.commit()
			if message == True:
				if true == True:	
					await bot.send_message(msg.from_user.id,"Вы получили " + str(amount) + " монет🤑")
				else:
					await bot.send_message(msg.from_user.id,"Вы получили " + str(amount) + " монет🤑",reply_markup = ReplyKeyboardRemove())

		async def AddExp(amount,type_of_xp):
			if type_of_xp == 'user':
				cursor.execute("UPDATE rpg_users_personage SET exp = exp + ? WHERE tgid = ? ",(amount,msg.from_user.id))
				connect.commit()


		async def MinusEnergy(amount):
			cursor.execute("UPDATE rpg_users_stats SET energy = energy - ? WHERE tgid = ? ",(amount,msg.from_user.id))
			connect.commit()
		async def PlusEnergy(amount):
			cursor.execute("UPDATE rpg_users_stats SET energy = energy + ? WHERE tgid = ? ",(amount,msg.from_user.id))
			connect.commit()

		cursor.execute("SELECT position FROM rpg_users WHERE tgid = ? ",(msg.from_user.id,))
		user_position = int(cursor.fetchone()[0]);

		if user_position == 1:
			if msg.chat.id == msg.from_user.id:
				if msg.text == 'Создать персонажа👶':
					await bot.send_message(msg.from_user.id,"🐱Отлично, выберите расу вашего персонажа.", reply_markup = kb.race_kb)
					cursor.execute("UPDATE rpg_users SET position = 2 WHERE tgid = ? ",(msg.from_user.id,))
					connect.commit()
			else: 
				await msg.reply('Регистрация только в личных сообщениях!')

		elif user_position == 2:
			if msg.chat.id == msg.from_user.id:
				if msg.text.lower() == 'орк' or  msg.text.lower() == 'человек' or  msg.text.lower() == 'эльф' or  msg.text.lower() == 'гоблин' or  msg.text.lower() == 'гном' or  msg.text.lower() == 'ящер':
					cursor.execute("UPDATE rpg_users_personage SET race = ? WHERE tgid = ? ",(msg.text,msg.from_user.id,))
					connect.commit()
					await bot.send_message(msg.from_user.id,"🚼Выберите, пожалуйста, пол вашего персонажа.",reply_markup = kb.gender_kb)
					cursor.execute("UPDATE rpg_users SET position = 999 WHERE tgid = ? ",(msg.from_user.id,))
					connect.commit()
				else:
					await msg.reply('Такой расы не существует!🤨')
			else: 
				await msg.reply('Регистрация только в личных сообщениях!')

		elif user_position == 999:
			if msg.chat.id == msg.from_user.id:
				await bot.send_message(msg.from_user.id,"🎫Отлично!Теперь введите имя вашего персонажа, другие жители мира смогут его видеть!(До 20 символов)",reply_markup = ReplyKeyboardRemove())
				cursor.execute("UPDATE rpg_users SET position = 4 WHERE tgid = ? ",(msg.from_user.id,))
				connect.commit()

				pers_gender = msg.text
				cursor.execute("UPDATE rpg_users_personage SET gender = ? WHERE tgid = ? ",(pers_gender,msg.from_user.id,))
				connect.commit()
			else: 
				await msg.reply('Регистрация только в личных сообщениях!')

		elif user_position == 4:
			if msg.chat.id == msg.from_user.id:
				if len(msg.text) > 20:
					pers_name = msg.text[:20]		
					cursor.execute("UPDATE rpg_users_personage SET name = ? WHERE tgid = ? ",(pers_name,msg.from_user.id,))
					connect.commit()
				else:
					pers_name = msg.text
					cursor.execute("UPDATE rpg_users_personage SET name = ? WHERE tgid = ? ",(pers_name,msg.from_user.id,))
					connect.commit()

				cursor.execute("UPDATE rpg_users SET position = 5 WHERE tgid = ? ",(msg.from_user.id,))
				connect.commit()

				await msg.reply('🕹Теперь давайте выберем класс вашего персонажа!\n\n⏺Маг - даёт 25 бонусных единиц энергии.\n\n⏺Ассасин - даёт 7% бонусного шанса к уклонению.\n\n⏺Воин - даёт 7 бонусных единиц к урону.\n\n⏺Берсерк - даёт бонусных 7% к шансу критического удара.\n\n⏺Паладин - бонусных 15 единиц здоровья.\n\n⏺Жрец - бонус 7% к шансу вампиризма.\n\n⏺Целитель - бонус 7% у шансу на исцеление.\n\n⏺Варвар - бонус 7% к шансу оглушить противника.',reply_markup = kb.clas_kb)
			else: 
				await msg.reply('Регистрация только в личных сообщениях!')
		elif user_position == 5:
			if msg.chat.id == msg.from_user.id:
				if msg.text == 'Варвар':
					cursor.execute("UPDATE rpg_users_personage SET clas = ? WHERE tgid = ? ",(msg.text,msg.from_user.id,))
					cursor.execute("UPDATE rpg_users_stats SET bash = 7 WHERE tgid = ? ",(msg.from_user.id,))
					connect.commit()
				elif msg.text == 'Маг':
					cursor.execute("UPDATE rpg_users_personage SET clas = ? WHERE tgid = ? ",(msg.text,msg.from_user.id,))
					cursor.execute("UPDATE rpg_users_stats SET max_energy = 125 WHERE tgid = ? ",(msg.from_user.id,))
					cursor.execute("UPDATE rpg_users_stats SET energy = 125 WHERE tgid = ? ",(msg.from_user.id,))
					connect.commit()
				elif msg.text == 'Ассасин':
					cursor.execute("UPDATE rpg_users_personage SET clas = ? WHERE tgid = ? ",(msg.text,msg.from_user.id,))
					cursor.execute("UPDATE rpg_users_stats SET miss = 7 WHERE tgid = ? ",(msg.from_user.id,))
					connect.commit()
				elif msg.text == 'Воин':
					cursor.execute("UPDATE rpg_users_stats SET damage = damage + 7 WHERE tgid = ? ",(msg.from_user.id,))
					cursor.execute("UPDATE rpg_users_personage SET clas = ? WHERE tgid = ? ",(msg.text,msg.from_user.id,))
					connect.commit()
				elif msg.text == 'Берсерк':
					cursor.execute("UPDATE rpg_users_stats SET critical = 7 WHERE tgid = ? ",(msg.from_user.id,))
					cursor.execute("UPDATE rpg_users_personage SET clas = ? WHERE tgid = ? ",(msg.text,msg.from_user.id,))
					connect.commit()
				elif msg.text == 'Паладин':
					cursor.execute("UPDATE rpg_users_stats SET hp = hp + 15 WHERE tgid = ? ",(msg.from_user.id,))
					cursor.execute("UPDATE rpg_users_personage SET clas = ? WHERE tgid = ? ",(msg.text,msg.from_user.id,))
					connect.commit()
				elif msg.text == 'Целитель':
					cursor.execute("UPDATE rpg_users_stats SET heal = 7 WHERE tgid = ? ",(msg.from_user.id,))
					cursor.execute("UPDATE rpg_users_personage SET clas = ? WHERE tgid = ? ",(msg.text,msg.from_user.id,))
					connect.commit()
				elif msg.text == 'Жрец':
					cursor.execute("UPDATE rpg_users_stats SET vampirise = 7 WHERE tgid = ? ",(msg.from_user.id,))
					cursor.execute("UPDATE rpg_users_personage SET clas = ? WHERE tgid = ? ",(msg.text,msg.from_user.id,))
					connect.commit()
				else:
					cursor.execute("UPDATE rpg_users_stats SET hp = hp + 15 WHERE tgid = ? ",(msg.from_user.id,))
					cursor.execute("UPDATE rpg_users_personage SET clas = 'Воин' WHERE tgid = ? ",(msg.from_user.id,))
					connect.commit()
				cursor.execute("UPDATE rpg_users SET position = 6 WHERE tgid = ? ",(msg.from_user.id,))
				await bot.send_message(msg.from_user.id, '💡Введите айди игрока, который вас пригласил и получите 100 бонусных монет при старте!',reply_markup = kb.ref_kb)
				#await bot.send_message(msg.from_user.id, "Отлично, ваша биография успешно заполнена!🥳\nВоспользуйтесь командой /help для знакомства с окружающим миром, а также введите /rules и прочтите правила.\n\n⚠️Наш канал - https://t.me/DarkWorldRPG\n⚠️Наш чат - https://t.me/DarkWorldRPG_chat",reply_markup = ReplyKeyboardRemove())
				connect.commit()
			else: 
				await msg.reply('Регистрация только в личных сообщениях!')
		elif user_position == 6:
			if msg.text == 'У меня нет реферального кода!🛑':
				cursor.execute("UPDATE rpg_users SET position = 0 WHERE tgid = ? ",(msg.from_user.id,))
				connect.commit()
				a = 'Отлично, ваша биография успешно заполнена!🥳\nСоветую вам открыть какой-то из сундуков, восползовавшись командой /chests или же пойти на работу: /work.\nВсе доступные команды: /help .'
				await bot.send_message(msg.from_user.id, a + "\n\n⚠️Наш канал - https://t.me/DarkWorldRPG\n⚠️Наш чат - https://t.me/DarkWorldRPG_chat",reply_markup = ReplyKeyboardRemove())
			else:
				try:
					a = int(msg.text) / 1
					try:

						cursor.execute("SELECT userid FROM rpg_users WHERE userid = ? ",(int(msg.text),))
						inviter = int(cursor.fetchone()[0]);

						cursor.execute("SELECT userid FROM rpg_users WHERE tgid= ? ",(msg.from_user.id,))
						my_id = int(cursor.fetchone()[0]);
						if int(msg.text) != my_id:
							cursor.execute("SELECT tgid FROM rpg_users WHERE userid = ? ",(int(msg.text),))
							inviter_tg = int(cursor.fetchone()[0]);

							cursor.execute("UPDATE referals SET inviter = ? WHERE tgid = ? ",(inviter,msg.from_user.id,))
							connect.commit()


							cursor.execute("SELECT userid FROM rpg_users WHERE tgid = ? ",(msg.from_user.id,))
							my_id = int(cursor.fetchone()[0]);

							cursor.execute("UPDATE referals SET referals = referals + 1 WHERE userid = ? ",(int(msg.text),))
							connect.commit()




							#next gold update

							await AddCoins(100,False,False)
							await msg.reply('Хорошо, также можете приглашать новых игроков и получать 20 золота за каждый сундук, который откроет реферал!')



							#next send message to inviter


							cursor.execute("SELECT name FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
							my_name = cursor.fetchone()[0];


							await bot.send_message(int(inviter_tg),'🥳По вашему приглашению зарегестрировался пользователь с ником ' + str(my_name) + ' !\nТеперь вы будете получать 20 монет за каждый сундук, который он откроет🤯.')
						else:
							await msg.reply('Вы что-то попутали, это ведь ваш айди!😳')

					except:
						await msg.reply('Извините, такого игрока не существует!🛑')
				except:
					await bot.send_message(msg.from_user.id, 'Извините, игрока с таким айди не существует!🛑')
				cursor.execute("UPDATE rpg_users SET position = 0 WHERE tgid = ? ",(msg.from_user.id,))
				connect.commit()
				await bot.send_message(msg.from_user.id, "Поздравляем, ваша биография успешно заполнена!🥳\nВоспользуйтесь командой /help для знакомства с окружающим миром, а также введите /rules и прочтите правила.\n\n⚠️Наш канал - https://t.me/DarkWorldRPG\n⚠️Наш чат - https://t.me/DarkWorldRPG_chat",reply_markup = ReplyKeyboardRemove())


		elif msg.text.lower() == 'снаряжение' or msg.text.lower() == '/equip' or msg.text.lower() == '/equip' + bot_name:
			cursor.execute("SELECT armour FROM rpg_users_inventory WHERE tgid = ? ",(msg.from_user.id,))
			your_armour = int(cursor.fetchone()[0]);

			cursor.execute("SELECT weapon FROM rpg_users_inventory WHERE tgid = ? ",(msg.from_user.id,))
			your_weapon = int(cursor.fetchone()[0]);

			cursor.execute("SELECT artifact FROM rpg_users_inventory WHERE tgid = ? ",(msg.from_user.id,))
			your_artifact = int(cursor.fetchone()[0]);

			cursor.execute("SELECT pet FROM rpg_users_inventory WHERE tgid = ? ",(msg.from_user.id,))
			your_pet = int(cursor.fetchone()[0]);

			armour_name = equip.armour_arr[your_armour].GetArmour('name')
			armour_rare = equip.armour_arr[your_armour].GetArmour('rare')
			armour_rare_text = await GetRare(armour_rare)

			weapon_name = equip.sword_arr[your_weapon].GetSword('name')
			weapon_rare = equip.sword_arr[your_weapon].GetSword('rare')
			weapon_rare_text = await GetRare(weapon_rare) 

			artifact_name = equip.artifacts_arr[your_artifact].GetArtifact('name')
			artifact_rare = equip.artifacts_arr[your_artifact].GetArtifact('rare') 
			artifact_rare_text = await GetRare(artifact_rare)

			pet_name = equip.pets_arr[your_pet].GetPet('name')
			pet_rare = equip.pets_arr[your_pet].GetPet('rare')
			pet_rare_text = await GetRare(pet_rare)



			armour_info = await GetItemInfo(your_armour,'armour')
			weapon_info = await GetItemInfo(your_weapon,'weapon')
			artifact_info = await GetItemInfo(your_artifact,'artifact')
			pet_info = await GetItemInfo(your_pet,'pet')

			await msg.reply('🎒Ваше снаряжение: \n\n👕Броня: ' + armour_name + '\n🌈Редкость: ' + armour_rare_text + armour_info + '\n\n🔫Оружие: ' + weapon_name + '\n🌈Редкость: ' + weapon_rare_text + weapon_info + '\n\n🔮Артефакт: ' + artifact_name + '\n🌈Редкость: ' + artifact_rare_text + artifact_info + '\n\n🧸Питомец: ' + pet_name + '\n🌈Редкость: ' + pet_rare_text + pet_info)

		elif msg.text.lower() == '\n/stats' + bot_name or msg.text.lower() == '/stats' or msg.text.lower() == 'характеристики' or msg.text.lower() == 'статы' or msg.text.lower() == 'стати':
			compl_str = 'ℹ️Характеристики вашего персонажа:  '

			cursor.execute("SELECT hp FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
			hp = cursor.fetchone()[0];

			cursor.execute("SELECT damage FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
			damage = cursor.fetchone()[0];

			cursor.execute("SELECT speed FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
			speed = cursor.fetchone()[0];

			cursor.execute("SELECT energy FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
			energy = cursor.fetchone()[0];

			cursor.execute("SELECT max_energy FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
			max_energy = cursor.fetchone()[0];

			cursor.execute("SELECT bash FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
			bash = cursor.fetchone()[0];

			cursor.execute("SELECT heal FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
			heal = cursor.fetchone()[0];

			cursor.execute("SELECT miss FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
			miss = cursor.fetchone()[0];

			cursor.execute("SELECT critical FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
			critical = cursor.fetchone()[0];

			cursor.execute("SELECT vampirise FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
			vampirise = cursor.fetchone()[0];

			cursor.execute("SELECT armour FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
			armour = cursor.fetchone()[0];

			cursor.execute("SELECT block FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
			block = cursor.fetchone()[0];

			cursor.execute("SELECT spikes FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
			spikes = cursor.fetchone()[0];

			cursor.execute("SELECT armour_theft FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
			armour_theft = cursor.fetchone()[0];

			cursor.execute("SELECT damage_theft FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
			damage_theft = cursor.fetchone()[0];

			cursor.execute("SELECT blindness FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
			blindness = cursor.fetchone()[0];

			cursor.execute("SELECT net_damage FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
			net_damage = cursor.fetchone()[0];

			cursor.execute("SELECT poison FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
			poison = cursor.fetchone()[0];


			compl_str += '\n💟Здоровье: ' + str(hp)
			compl_str += '\n🗡Урон: ' + str(damage)
			compl_str += '\n💨Скорость: ' + str(speed)
			compl_str += '\n⚡️Энергия: ' + str(energy) + '/' + str(max_energy)
			compl_str += '\n🛡Броня: ' + str(armour)
			compl_str += '\n💫Шанс оглушения: ' + str(bash) + '%'
			compl_str += '\n💊Шанс исцеления: ' + str(heal) + '%'
			compl_str += '\n🎭Шанс уклониться: ' + str(miss) + '%'
			compl_str += '\n🦾Шанс критического урона: ' + str(critical) + '%'
			compl_str += '\n🩸Шанс вампиризма: ' + str(vampirise) + '%'
			compl_str += '\n🧿Шипы: ' + str(spikes) + '%'
			compl_str += '\n♻️Шанс похитить урон: ' + str(damage_theft) + '%'
			compl_str += '\n♻️Шанс похитить броню: ' + str(armour_theft) + '%'
			compl_str += '\n👁‍🗨Шанс ослепить: ' + str(blindness) + '%'
			compl_str += '\n✨Шанс нанести чистый урон: ' + str(net_damage) + '%'
			compl_str += '\n🧪Шанс отравить: ' + str(poison) + '%'

			await msg.reply(compl_str)


		elif msg.text.lower() == '/bonus' or msg.text.lower() == 'бонус' or msg.text.lower() == '/bonus' + bot_name:
			cursor.execute("SELECT day_bonus FROM bonus WHERE tgid = ? ",(msg.from_user.id,))
			day_bonus = int(cursor.fetchone()[0]);
			if day_bonus == 0:
				cursor.execute("UPDATE statistic SET bonus = bonus + 1 WHERE tgid = ? ",(msg.from_user.id,))
				connect.commit()
				await AddCoins(200,False,False)
				await msg.reply('Вы получили бонус в размере 200 ' + 'монет💰')
				now_day = int(now.day)
				now_hour = int(now.hour)
				cursor.execute("UPDATE bonus SET bonus_day = ? WHERE tgid = ? ",(now_day,msg.from_user.id,))
				cursor.execute("UPDATE bonus SET bonus_hour = ? WHERE tgid = ? ",(now_hour,msg.from_user.id,))
				connect.commit()
				cursor.execute("UPDATE bonus SET day_bonus = 1 WHERE tgid = ? ",(msg.from_user.id,))
				connect.commit()
			else:
				await msg.reply('Сегодня вы уже получили ежедневный бонус!🙁')

		elif msg.text.lower() == '/roulette' or msg.text.lower() == 'рулетка' or msg.text.lower() == '/roulette' + bot_name: 
			cursor.execute("SELECT rulet_bonus FROM bonus WHERE tgid = ? ",(msg.from_user.id,))
			check_bonus = int(cursor.fetchone()[0]);
			if check_bonus == 0:
				text = ''
				cursor.execute("UPDATE statistic SET rulet = rulet + 1 WHERE tgid = ? ",(msg.from_user.id,))
				connect.commit()
				droped_bonus_num = random.randint(0,35)
				if droped_bonus_num == 0:
					text = 'Поздравляем, вы выиграли 25 монет!🥳'
					await AddCoins(25,False,False)
				elif droped_bonus_num == 1:
					text = 'Поздравляем, вы выиграли 50 монет!🥳'
					await AddCoins(50,False,False)
				elif droped_bonus_num == 2:
					text = 'Поздравляем, вы выиграли 100 монет!🥳'
					await AddCoins(100,False,False)
				elif droped_bonus_num == 3:
					text = 'Поздравляем, вы выиграли 200 монет!🎉'
					await AddCoins(200,False,False)
				elif droped_bonus_num == 4:
					text = 'Поздравляем, вы выиграли 100 опыта!🥳'
					await AddExp(100,'user')
				elif droped_bonus_num == 5:
					await AddExp(200,'user')
					text = 'Поздравляем, вы выиграли 200 опыта!🥳'
				elif droped_bonus_num == 6:
					await AddExp(500,'user')
					text = 'Поздравляем, вы выиграли 500 опыта!🎉'
				elif droped_bonus_num == 7:
					await AddExp(1000,'user')
					text = 'Поздравляем, вы выиграли 1000 опыта!🎉'
				elif droped_bonus_num == 8:
					await PlusEnergy(25)
					text = 'Поздравляем, вы выиграли 25 единиц энергии!🥳'
				elif droped_bonus_num == 9:
					await PlusEnergy(50)
					text = 'Поздравляем, вы выиграли 50 единиц энергии!🥳'
				elif droped_bonus_num == 10:
					await PlusEnergy(100)
					text = 'Поздравляем, вы выиграли 100 единиц энергии!🥳'
				elif droped_bonus_num == 11:
					await PlusEnergy(200)
					text = 'Поздравляем, вы выиграли 200 единиц энергии!🎉'
				elif droped_bonus_num == 12:
					text = 'Поздравляем, вы выиграли особый статус!🎉'
					new_status_num = random.randint(0,5)
					status = 'Default'
					if new_status_num == 0:
						status = 'Солнышко'
					elif new_status_num == 1:
						status = 'Рыбка'
					elif new_status_num == 2:
						status = 'Котёнок'
					elif new_status_num == 3:
						status = 'Полубог'
					elif new_status_num == 4:
						status = 'Архангел'
					elif new_status_num == 5:
						status = 'Зайка'
					cursor.execute("UPDATE rpg_users SET user_mark = ? WHERE tgid = ?",(str(status),msg.from_user.id,))
					connect.commit()
				elif droped_bonus_num == 13:
					await AddCoins(500,False,False)
					text = 'Поздравляем, вы выиграли 500 монет!🎉'
				elif droped_bonus_num == 14:
					text = 'Поздравляем, вы выиграли +1 к урону!🥳'
					cursor.execute("UPDATE rpg_users_stats SET damage = damage + 1 WHERE tgid = ? ",(msg.from_user.id,))
					connect.commit()
				elif droped_bonus_num == 15:
					text = 'Поздравляем, вы выиграли +1 к здоровью🥳'
					cursor.execute("UPDATE rpg_users_stats SET hp = hp + 1 WHERE tgid = ? ",(msg.from_user.id,))
					connect.commit()
				elif droped_bonus_num == 16:
					text = 'Поздравляем, вы выиграли 300 энергии, повеселитесь!🎉'
					await PlusEnergy(300)
				else:
					text = 'Извините,вы ничего не выиграли!☹️'
				await msg.reply(text)
				now_day = int(now.day)
				now_hour = int(now.hour)
				cursor.execute("UPDATE bonus SET rulet_day = ? WHERE tgid = ? ",(now_day,msg.from_user.id,))
				connect.commit()
				cursor.execute("UPDATE bonus SET rulet_hour = ? WHERE tgid = ? ",(now_hour,msg.from_user.id,))
				connect.commit()
				cursor.execute("UPDATE bonus SET rulet_bonus = 1 WHERE tgid = ? ",(msg.from_user.id,))
				connect.commit()
			else:
				await msg.reply('Сегодня вы уже играли в рулетку!🙁')

		elif msg.text == "Профиль" or msg.text.lower() == "профиль" or msg.text.lower() == "/profile" or msg.text.lower() == 'персонаж' or msg.text == 'Персонаж' or msg.text == '/profile@DarkWorldRPG_bot':
			cursor.execute("SELECT tgid FROM rpg_users WHERE tgid = ? ",(msg.from_user.id,))
			id_tg = str(cursor.fetchone()[0]);

			cursor.execute("SELECT userid FROM rpg_users WHERE tgid = ? ",(msg.from_user.id,))
			id_db = str(cursor.fetchone()[0]);

			cursor.execute("SELECT user_mark FROM rpg_users WHERE tgid = ? ",(msg.from_user.id,))
			user_mark = str(cursor.fetchone()[0]);

			cursor.execute("SELECT race FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
			pers_race = str(cursor.fetchone()[0]);

			cursor.execute("SELECT name FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
			pers_name  = str(cursor.fetchone()[0]);

			cursor.execute("SELECT clas FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
			pers_clas = str(cursor.fetchone()[0]);

			cursor.execute("SELECT coins FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
			pers_coins = str(cursor.fetchone()[0]);

			cursor.execute("SELECT gender FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
			pers_gender = str(cursor.fetchone()[0]);

			cursor.execute("SELECT partner FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
			partner_tg = str(cursor.fetchone()[0]);
			pers_partner = 'Отсутствует'
			if len(partner_tg) > 2:
				cursor.execute("SELECT name FROM rpg_users_personage WHERE tgid = ? ",(partner_tg,))
				partner_name  = str(cursor.fetchone()[0]);
				pers_partner = partner_name
			cursor.execute("SELECT exp FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
			user_exp = int(cursor.fetchone()[0]);
			pers_lvl = user_exp // 1000

			cursor.execute("SELECT duel_status FROM users_settings WHERE tgid = ? ",(msg.from_user.id,))
			your_duel_status = int(cursor.fetchone()[0]);
			your_duel_status_text = ''
			if your_duel_status == 0:
				your_duel_status_text = 'Включены✅'
			else:
				your_duel_status_text = 'Выключены🚫'


			cursor.execute("SELECT inviter FROM referals WHERE tgid = ? ",(msg.from_user.id,))
			my_inviter = int(cursor.fetchone()[0]);
			my_inviter_name = '🚷Отсутствует🚷'
			if my_inviter != 0:
				cursor.execute("SELECT name FROM rpg_users_personage WHERE userid = ? ",(my_inviter,))
				my_inviter_name = str(cursor.fetchone()[0]);




			cursor.execute("SELECT gender FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
			pers_gender = str(cursor.fetchone()[0]);

			await msg.reply("Ваш профиль: \n🔑ID в боте: " + id_db + '\n\n🌐Telegram ID: ' + id_tg + '\n\n📝Никнейм: ' + pers_name +'\n\n🗂Статус: '+ user_mark + '\n\n👶Раса персонажа: ' + pers_race + '\n\n🎎Класс персонажа: ' + pers_clas +'\n\n🚻Пол персонажа: ' + pers_gender + '\n\n💕Партнёр: ' + pers_partner + '\n\n👥Реферер: ' + str(my_inviter_name)+ '\n\n✳️Уровень персонажа: ' + str(pers_lvl) + '\n\n💰Золото: ' + str(pers_coins))

		
		
		elif msg.text.lower() == '/rarities' + bot_name or msg.text.lower() == '/rarities' or msg.text.lower() == 'редкости':
			await msg.reply('Иерархия редкости предметов: \n\n⬜️ - обычная \n🟦 - редкая \n🟩 - сверхредкая \n🟪 - эпическая \n🟨 - легендарная\n🟧 - реликвия \n🟥 - первозданный предмет \n⬛️ - божественная')
		elif msg.text.lower() == "бой" or msg.text.lower() == "/pve" or msg.text.lower() == '/pve' + bot_name:
			cursor.execute("SELECT energy FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
			energy = cursor.fetchone()[0];
			cursor.execute("UPDATE statistic SET pve = pve + 1 WHERE tgid = ? ",(msg.from_user.id,))
			connect.commit()
			if energy > 0:
				try:

					rand_enemy_num = random.randint(0,len(enemy.enemy_arr))
					

					enemy_hp = enemy.enemy_arr[rand_enemy_num].GetEnemy('hp')
					enemy_name = enemy.enemy_arr[rand_enemy_num].GetEnemy('name')
					enemy_speed = enemy.enemy_arr[rand_enemy_num].GetEnemy('speed')
					enemy_damage = enemy.enemy_arr[rand_enemy_num].GetEnemy('damage')
					enemy_xp = enemy.enemy_arr[rand_enemy_num].GetEnemy('xp')
					enemy_gold = enemy.enemy_arr[rand_enemy_num].GetEnemy('gold')
					enemy_bash = random.randint(0,40)
					enemy_heal = random.randint(0,40)
					enemy_miss = random.randint(0,40)
					enemy_critical = random.randint(0,40)
					enemy_vampirise = random.randint(0,40)
					enemy_armour = random.randint(0,50)
					enemy_block = random.randint(0,40)
					enemy_spikes = random.randint(0,40)
					enemy_armour_theft = random.randint(0,40)
					enemy_damage_theft = random.randint(0,40)
					enemy_blindness = random.randint(0,40)
					enemy_poison = random.randint(0,40)
					enemy_gold_rush = random.randint(0,40)
					enemy_net_damage = random.randint(0,40)



					cursor.execute("SELECT hp FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
					your_hp = int(cursor.fetchone()[0]);

					cursor.execute("SELECT damage FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
					your_damage = int(cursor.fetchone()[0]);

					cursor.execute("SELECT speed FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
					your_speed = int(cursor.fetchone()[0]);

					cursor.execute("SELECT bash FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
					your_bash = int(cursor.fetchone()[0]); ###

					cursor.execute("SELECT heal FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
					your_heal = int(cursor.fetchone()[0]); ###

					cursor.execute("SELECT miss FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
					your_miss = int(cursor.fetchone()[0]); #

					cursor.execute("SELECT critical FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
					your_critical = int(cursor.fetchone()[0]);

					cursor.execute("SELECT vampirise FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
					your_vampirise = int(cursor.fetchone()[0]);

					cursor.execute("SELECT armour FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
					your_armour = int(cursor.fetchone()[0]);

					cursor.execute("SELECT block FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
					your_block = int(cursor.fetchone()[0]); 

					cursor.execute("SELECT spikes FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
					your_spikes = int(cursor.fetchone()[0]);

					cursor.execute("SELECT armour_theft FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
					your_armour_theft = int(cursor.fetchone()[0]);

					cursor.execute("SELECT damage_theft FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
					your_damage_theft = int(cursor.fetchone()[0]);

					cursor.execute("SELECT blindness FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
					your_blindness = int(cursor.fetchone()[0]);

					cursor.execute("SELECT poison FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
					your_poison = int(cursor.fetchone()[0]);

					cursor.execute("SELECT gold_rush FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
					your_gold_rush = int(cursor.fetchone()[0]);

					cursor.execute("SELECT net_damage FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
					your_net_damage = int(cursor.fetchone()[0]);


					#состояния
					enemy_bashed = False
					you_bashed = False
					your_poisoned = 0
					enemy_poisoned = 0
					your_blinded = 0
					enemy_blinded = 0
					your_net_damaged = False
					enemy_net_damaged = False


					#log_counter
					#your
					amount_your_hit = 0
					amount_your_damage = 0
					amount_your_critical = 0
					amount_your_bashed = 0
					amount_your_blocked = 0
					amount_your_spikes = 0
					amount_your_gold_rush = 0
					amount_your_blindness = 0
					amount_your_poisoned = 0
					amount_your_net_damaged = 0
					amount_your_vampirise = 0
					amount_your_healed = 0
					amount_your_missed = 0
					amount_your_armour_theft = 0
					amount_your_damage_theft = 0


					#enemy
					amount_enemy_hit = 0
					amount_enemy_damage = 0
					amount_enemy_critical = 0
					amount_enemy_bashed = 0
					amount_enemy_blocked = 0
					amount_enemy_spikes = 0
					amount_enemy_gold_rush = 0
					amount_enemy_blindness = 0
					amount_enemy_poisoned = 0
					amount_enemy_net_damaged = 0
					amount_enemy_vampirise = 0
					amount_enemy_healed = 0
					amount_enemy_missed = 0
					amount_enemy_armour_theft = 0
					amount_enemy_damage_theft = 0


					num = random.randint(0,5)
					if num == 0:
						message = 'Вы встретили '
					elif num == 1:
						message = "Ваш враг - "
					elif num == 2:
						message = "Вы наткнулись на "
					elif num == 3:
						message = "Ваш противник - "
					elif num == 4:
						message = "Вам придётся сражаться с "
					elif num == 5:
						message = "На вашем пути встретился "
					fight_log = '0'
					cursor.execute("SELECT log_status FROM users_settings WHERE tgid = ? ",(msg.from_user.id,))
					log_status = int(cursor.fetchone()[0]);
					if log_status == 0:
						fight_log = message + enemy_name + "\n❤️Здоровье врага: " + str(enemy_hp) + '\n🛡Броня противника: ' + str(enemy_armour) + "\n🗡Атака врага: " + str(enemy_damage) + "\n⚡️Скорость врага: " + str(enemy_speed) + '\n🌪Шанс на уклонение: ' + str(enemy_miss) + "\n🩸Эффект вампиризма: " + str(enemy_critical) + "\n💫Шанс оглушения: " + str(enemy_bash) + '\n💉Шанс исцеления: ' + str(enemy_heal) + '\n💥Шанс критического урона: ' + str(enemy_critical)
						fight_log += '\n'
					else:
						fight_log = message + enemy_name + "\n❤️Здоровье врага: " + str(enemy_hp) + '\n🛡Броня противника: ' + str(enemy_armour) + "\n🗡Атака врага: " + str(enemy_damage) + "\n⚡️Скорость врага: " + str(enemy_speed) + '\n🌪Шанс на уклонение: ' + str(enemy_miss) + "\n🩸Эффект вампиризма: " + str(enemy_critical) + "\n💫Шанс оглушения: " + str(enemy_bash) + '\n💉Шанс исцеления: ' + str(enemy_heal) + '\n💥Шанс критического урона: ' + str(enemy_critical)
						fight_log += '\n💠Шанс на блок: ' + str(enemy_block) + '%\n🔅Шипы: ' + str(enemy_spikes) + '\n🔄Шанс своровать броню: ' + str(enemy_armour_theft) + '%\n🔁Шанс своровать урон: ' + str(enemy_damage_theft) +'%\n👁‍🗨Шанс ослепления: ' + str(enemy_blindness) + '%\n🧪Шанс отравления: ' + str(enemy_poison) + '%\n✳️Шанс на чистый урон: ' + str(enemy_net_damage) + '%' 
					await msg.reply(str(fight_log))

					while your_hp > 0 and enemy_hp > 0 :
						bash_chance = random.randint(30,100)
						heal_chance = random.randint(30,100)
						miss_chance = random.randint(30,100)
						critical_chance = random.randint(30,100)
						block_chance = random.randint(30,100)
						armour_theft_chance = random.randint(30,100)
						damage_theft_chance = random.randint(30,100)
						blindness_chance = random.randint(30,100)
						poison_chance = random.randint(30,100)
						gold_rush_chance = random.randint(30,100)
						vampirise_chance = random.randint(30,100)
						net_damage_chance = random.randint(30,100)
						spike_chance = random.randint(30,100)


						if you_bashed == False:
							if enemy_miss + your_blinded < miss_chance:
								if your_bash >= bash_chance:
									enemy_bashed = True
									amount_your_bashed += 1
								if your_heal >= heal_chance:

									one_percent = your_hp / 100
									your_hp += int(one_percent * 30)
									amount_your_healed += int(one_percent * 30)
									your_blinded = 0
									your_poisoned = 0
								if your_armour_theft >= armour_theft_chance and enemy_armour >= 2:
									enemy_armour = enemy_armour - 2
									your_armour += 2
									amount_your_armour_theft += 2
								if your_damage_theft >= armour_theft_chance and enemy_damage >= 2:
									enemy_damage = enemy_damage - 2
									your_damage += 2
									amount_your_damage_theft += 2
								if your_poison >= poison_chance:
									enemy_poisoned += 2
								if your_blindness >= blindness_chance:
									enemy_blinded += 2
									amount_your_blindness += 2 

								your_hit = 0
								#ataka
								if enemy_block < block_chance:
									double_damage = 1
									if your_critical >= critical_chance:
										double_damage = 2
									if your_net_damage >= net_damage_chance:
										your_hit = (your_damage * your_speed) * double_damage 
									else:
										your_hit = ((your_damage * your_speed) * double_damage)

										if enemy_armour >= int(your_hit):
											enemy_armour = enemy_armour - int(your_hit)
											your_hit = 0

									enemy_hp = enemy_hp - int(your_hit)
									amount_your_hit += 1
									amount_your_damage += int(your_hit)
									if your_vampirise >= vampirise_chance:
										your_hp += int(your_hit)
										amount_your_healed += int(your_hit)
									double_damage = 1
									if enemy_spikes >= spike_chance:
										your_hp = your_hp - int(your_hit / 2)
										amount_enemy_spikes += int(your_hit / 2)
								else:
									your_hit = your_damage * your_speed
									amount_your_hit += 1
									amount_your_damage += int(your_hit / 2)
									enemy_hp = enemy_hp - int(your_hit / 2)
									amount_enemy_blocked += int(your_hit /2)

								

								enemy_hp = enemy_hp - enemy_poisoned
								amount_enemy_poisoned += enemy_poisoned
							else:
								amount_your_missed += 1 

						else:
							you_bashed = False

						if enemy_hp <= 0 or your_hp <= 0:
							break
						
						if enemy_bashed == False:
							if your_miss + enemy_blinded < miss_chance:
								if enemy_bash >= bash_chance:
									your_bashed = True
									amount_enemy_bashed += 1
								if enemy_heal >= heal_chance:

									one_percent = enemy_hp / 100
									enemy_hp += int(one_percent * 30)
									amount_enemy_healed += int(one_percent * 30)
									enemy_blinded = 0
									enemy_poisoned = 0
								if enemy_armour_theft >= armour_theft_chance and your_armour >= 2:
									your_armour = your_armour - 2
									enemy_armour += 2
									amount_enemy_armour_theft += 2
								if enemy_damage_theft >= armour_theft_chance and your_damage >= 2:
									your_damage = your_damage - 2
									enemy_damage += 2
									amount_enemy_damage_theft += 2
								if enemy_poison >= poison_chance:
									your_poisoned += 2
								if enemy_blindness >= blindness_chance:
									your_blinded += 2
									amount_enemy_blindness += 2 

								enemy_hit = 0
								#ataka
								if your_block < block_chance:
									double_damage = 1
									if enemy_critical >= critical_chance:
										double_damage = 2
									if enemy_net_damage >= net_damage_chance:
										enemy_hit = (enemy_damage * enemy_speed) * double_damage 
									else:
										enemy_hit = ((enemy_damage * enemy_speed) * double_damage) 
										if your_armour >= int(enemy_hit):
											your_armour = your_armour - int(enemy_hit)
											enemy_hit = 0

									your_hp = your_hp - int(enemy_hit)
									amount_enemy_hit += 1
									amount_enemy_damage += int(enemy_hit)
									if enemy_vampirise >= vampirise_chance:
										enemy_hp += int(enemy_hit)
										amount_enemy_healed += int(enemy_hit)
									double_damage = 1
									if your_spikes >= spike_chance:
										enemy_hp = enemy_hp - int(enemy_hit / 2)
										amount_your_spikes += int(enemy_hit / 2)
								else:
									enemy_hit = enemy_damage * enemy_speed
									amount_enemy_hit += 1
									amount_enemy_damage += int(enemy_hit) / 2
									your_hp = your_hp - int(enemy_hit / 2)
									amount_your_blocked += int(enemy_hit / 2)
								
								your_hp = your_hp - your_poisoned
								amount_your_poisoned += your_poisoned

							else:
								amount_enemy_missed += 1 

						else:
							enemy_bashed = False

						if enemy_hp <= 0 or your_hp <= 0:
							break


					result = '0'
					result_message = '0'
					if your_hp <= 0:
						result = 'Вы проиграли!😢'
						cursor.execute("SELECT log_status FROM users_settings WHERE tgid = ? ",(msg.from_user.id,))
						log_status = int(cursor.fetchone()[0]);
						if log_status == 0:
							result_message = '\n\n🔹Вы нанесли урона: ' +str(amount_your_damage)+ '\n🔹Вы нанесли ударов: '+ str(amount_your_hit) + '\n🔹Вы восстановили здоровья: ' + str(amount_your_healed) 
							result_message += '\n\n\n🔸Противник нанёс урона: ' +str(amount_enemy_damage)+ '\n🔸Противник нанёс ударов: '+ str(amount_enemy_hit) + '\n🔸Противник восстановил здоровья: ' + str(amount_enemy_healed) 
						else:
							result_message = '\n\n🔹Вы нанесли урона: ' +str(amount_your_damage)+ '\n🔹Вы нанесли ударов: '+ str(amount_your_hit) + '\n🔹Вы восстановили здоровья: ' + str(amount_your_healed) 
							result_message += '\n🔹Вы заблокировали урона: ' +str(amount_your_blocked)+ '\n🔹Вы отразили урона шипами: ' + str(amount_your_spikes) + '\n🔹Вы своровали брони: ' +str(amount_your_armour_theft)+ '\n🔹Вы своровали урона: ' +str(amount_your_damage_theft)+ '\n🔹Урон противнику ядом: ' + str(amount_enemy_poisoned)+ '\n🔹Общее ослепление противника: ' +str(amount_your_blindness)+ '\n🔹Вы уклонились от ударов: ' +str(amount_your_missed)+ '\n🔹Вы оглушили противника: ' + str(amount_your_bashed)
							result_message += '\n\n\n🔸Противник нанёс урона: ' +str(amount_enemy_damage)+ '\n🔸Противник нанёс ударов: '+ str(amount_enemy_hit) + '\n🔸Противник восстановил здоровья: ' + str(amount_enemy_healed) 
							result_message += '\n🔸Противник заблокировал урона: ' +str(amount_enemy_blocked)+ '\n🔸Противник отразил урона шипами: ' + str(amount_enemy_spikes) + '\n🔸Противник своровал брони: ' +str(amount_enemy_armour_theft)+ '\n🔸Противник своровал урона: ' +str(amount_enemy_damage_theft)+ '\n🔸Урон по вам ядом: ' + str(amount_your_poisoned)+ '\n🔸Общее ослепление вас: ' +str(amount_enemy_blindness)+ '\n🔸Противник уклонился от ударов: ' +str(amount_enemy_missed)+ '\n🔸Противник оглушил вас: ' + str(amount_enemy_bashed)
						
						await MinusEnergy(5)
						await AddExp(int(enemy_gold / 2),'user')
						

					elif enemy_hp <= 0:
						result = 'Вы победили!🥳'
						cursor.execute("SELECT log_status FROM users_settings WHERE tgid = ? ",(msg.from_user.id,))
						log_status = int(cursor.fetchone()[0]);
						if log_status == 0:
							result_message = '\n\n🔹Вы нанесли урона: ' +str(amount_your_damage)+ '\n🔹Вы нанесли ударов: '+ str(amount_your_hit) + '\n🔹Вы восстановили здоровья: ' + str(amount_your_healed) 
							result_message += '\n\n\n🔸Противник нанёс урона: ' +str(amount_enemy_damage)+ '\n🔸Противник нанёс ударов: '+ str(amount_enemy_hit) + '\n🔸Противник восстановил здоровья: ' + str(amount_enemy_healed) 
						else:
							result_message = '\n\n🔹Вы нанесли урона: ' +str(amount_your_damage)+ '\n🔹Вы нанесли ударов: '+ str(amount_your_hit) + '\n🔹Вы восстановили здоровья: ' + str(amount_your_healed) 
							result_message += '\n🔹Вы заблокировали урона: ' +str(amount_your_blocked)+ '\n🔹Вы отразили урона шипами: ' + str(amount_enemy_spikes) + '\n🔹Вы своровали брони: ' +str(amount_your_armour_theft)+ '\n🔹Вы своровали урона: ' +str(amount_your_damage_theft)+ '\n🔹Урон противнику ядом: ' + str(amount_enemy_poisoned)+ '\n🔹Общее ослепление противника: ' +str(amount_your_blindness)+ '\n🔹Вы уклонились от ударов: ' +str(amount_your_missed)+ '\n🔹Вы оглушили противника: ' + str(amount_your_bashed)
							result_message += '\n\n\n🔸Противник нанёс урона: ' +str(amount_enemy_damage)+ '\n🔸Противник нанёс ударов: '+ str(amount_enemy_hit) + '\n🔸Противник восстановил здоровья: ' + str(amount_enemy_healed) 
							result_message += '\n🔸Противник заблокировал урона: ' +str(amount_enemy_blocked)+ '\n🔸Противник отразил урона шипами: ' + str(amount_your_spikes) + '\n🔸Противник своровал брони: ' +str(amount_enemy_armour_theft)+ '\n🔸Противник своровал урона: ' +str(amount_enemy_damage_theft)+ '\n🔸Урон по вам ядом: ' + str(amount_your_poisoned)+ '\n🔸Общее ослепление вас: ' +str(amount_enemy_blindness)+ '\n🔸Противник уклонился от ударов: ' +str(amount_enemy_missed)+ '\n🔸Противник оглушил вас: ' + str(amount_enemy_bashed)

						await MinusEnergy(5)
						await AddExp(enemy_gold,'user')
						await AddCoins(enemy_gold + random.randint(1,10),True,False)

					await msg.reply(result + result_message)
					
				except Exception as ex:
					print(4)
					print(ex)
					await bot.send_message(msg.from_user.id,'Противник сбежал с поля боя')
					await bot.send_message(793368809,str(ex))
			else:
				await msg.reply("У вас недостаточно энергии для этого действия!🛑")




		Splited_msg = msg.text.split(' ')

		if Splited_msg[0].lower() == 'дуэль' or Splited_msg[0].lower() == 'дуель' or Splited_msg[0].lower() == 'пвп' or Splited_msg[0].lower() == 'pvp':
			cursor.execute("SELECT energy FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
			energy = cursor.fetchone()[0];
			cursor.execute("SELECT userid FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
			your_id = int(cursor.fetchone()[0]);
			cursor.execute("SELECT duel_status FROM users_settings WHERE tgid = ? ",(msg.from_user.id,))
			your_duel = int(cursor.fetchone()[0]);
			if your_duel != 1:
				if energy > 0:
					try:
						enemy_id = 0
						if Splited_msg[1].lower() == 'random' or Splited_msg[1].lower() == 'рандом':
							cursor.execute("SELECT userid FROM rpg_users")
							enemy_arr = len(cursor.fetchall())
							enemy_duel = 1
							enemy_id = your_id
							while enemy_duel != 0:
								enemy_id = random.randint(1,enemy_arr - 1)
								if enemy_id == your_id:
									enemy_id = enemy_arr - your_id + 1
								cursor.execute("SELECT duel_status FROM users_settings WHERE userid = ? ",(enemy_id,))
								enemy_duel = int(cursor.fetchone()[0]);





						else:	
							enemy_id = int(Splited_msg[1])

						cursor.execute("SELECT tgid FROM rpg_users_stats WHERE userid = ? ",(enemy_id,))
						enemy_tg = int(cursor.fetchone()[0]);

						cursor.execute("SELECT duel_status FROM users_settings WHERE userid = ? ",(enemy_id,))
						enemy_status = int(cursor.fetchone()[0]);

						if enemy_status != 1:
							if enemy_tg != msg.from_user.id:
								cursor.execute("SELECT hp FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
								your_hp = int(cursor.fetchone()[0]);

								cursor.execute("SELECT damage FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
								your_damage = int(cursor.fetchone()[0]);

								cursor.execute("SELECT speed FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
								your_speed = int(cursor.fetchone()[0]);

								cursor.execute("SELECT bash FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
								your_bash = int(cursor.fetchone()[0]); ###

								cursor.execute("SELECT heal FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
								your_heal = int(cursor.fetchone()[0]); ###

								cursor.execute("SELECT miss FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
								your_miss = int(cursor.fetchone()[0]); #

								cursor.execute("SELECT critical FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
								your_critical = int(cursor.fetchone()[0]);

								cursor.execute("SELECT vampirise FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
								your_vampirise = int(cursor.fetchone()[0]);

								cursor.execute("SELECT armour FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
								your_armour = int(cursor.fetchone()[0]);

								cursor.execute("SELECT block FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
								your_block = int(cursor.fetchone()[0]); 

								cursor.execute("SELECT spikes FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
								your_spikes = int(cursor.fetchone()[0]);

								cursor.execute("SELECT armour_theft FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
								your_armour_theft = int(cursor.fetchone()[0]);

								cursor.execute("SELECT damage_theft FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
								your_damage_theft = int(cursor.fetchone()[0]);

								cursor.execute("SELECT blindness FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
								your_blindness = int(cursor.fetchone()[0]);

								cursor.execute("SELECT poison FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
								your_poison = int(cursor.fetchone()[0]);

								cursor.execute("SELECT gold_rush FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
								your_gold_rush = int(cursor.fetchone()[0]);

								cursor.execute("SELECT net_damage FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
								your_net_damage = int(cursor.fetchone()[0]);

								cursor.execute("SELECT name FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
								your_name = str(cursor.fetchone()[0]);

								cursor.execute("SELECT userid FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
								your_id = int(cursor.fetchone()[0]);



								cursor.execute("SELECT hp FROM rpg_users_stats WHERE tgid = ? ",(enemy_tg,))
								enemy_hp = int(cursor.fetchone()[0]);

								cursor.execute("SELECT damage FROM rpg_users_stats WHERE tgid = ? ",(enemy_tg,))
								enemy_damage = int(cursor.fetchone()[0]);

								cursor.execute("SELECT speed FROM rpg_users_stats WHERE tgid = ? ",(enemy_tg,))
								enemy_speed = int(cursor.fetchone()[0]);

								cursor.execute("SELECT bash FROM rpg_users_stats WHERE tgid = ? ",(enemy_tg,))
								enemy_bash = int(cursor.fetchone()[0]);

								cursor.execute("SELECT heal FROM rpg_users_stats WHERE tgid = ? ",(enemy_tg,))
								enemy_heal = int(cursor.fetchone()[0]);

								cursor.execute("SELECT miss FROM rpg_users_stats WHERE tgid = ? ",(enemy_tg,))
								enemy_miss = int(cursor.fetchone()[0]);

								cursor.execute("SELECT critical FROM rpg_users_stats WHERE tgid = ? ",(enemy_tg,))
								enemy_critical = int(cursor.fetchone()[0]);

								cursor.execute("SELECT vampirise FROM rpg_users_stats WHERE tgid = ? ",(enemy_tg,))
								enemy_vampirise = int(cursor.fetchone()[0]);

								cursor.execute("SELECT name FROM rpg_users_personage WHERE tgid = ? ",(enemy_tg,))
								enemy_name = cursor.fetchone()[0];

								cursor.execute("SELECT armour FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
								enemy_armour = int(cursor.fetchone()[0]);

								cursor.execute("SELECT block FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
								enemy_block = int(cursor.fetchone()[0]); 

								cursor.execute("SELECT spikes FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
								enemy_spikes = int(cursor.fetchone()[0]);

								cursor.execute("SELECT armour_theft FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
								enemy_armour_theft = int(cursor.fetchone()[0]);

								cursor.execute("SELECT damage_theft FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
								enemy_damage_theft = int(cursor.fetchone()[0]);

								cursor.execute("SELECT blindness FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
								enemy_blindness = int(cursor.fetchone()[0]);

								cursor.execute("SELECT poison FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
								enemy_poison = int(cursor.fetchone()[0]);

								cursor.execute("SELECT gold_rush FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
								enemy_gold_rush = int(cursor.fetchone()[0]);

								cursor.execute("SELECT net_damage FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
								enemy_net_damage = int(cursor.fetchone()[0]);

								enemy_bashed = False
								you_bashed = False
								your_poisoned = 0
								enemy_poisoned = 0
								your_blinded = 0
								enemy_blinded = 0
								your_net_damaged = False
								enemy_net_damaged = False


								#log_counter
								#your
								amount_your_hit = 0
								amount_your_damage = 0
								amount_your_critical = 0
								amount_your_bashed = 0
								amount_your_blocked = 0
								amount_your_spikes = 0
								amount_your_gold_rush = 0
								amount_your_blindness = 0
								amount_your_poisoned = 0
								amount_your_net_damaged = 0
								amount_your_vampirise = 0
								amount_your_healed = 0
								amount_your_missed = 0
								amount_your_armour_theft = 0
								amount_your_damage_theft = 0


								#enemy
								amount_enemy_hit = 0
								amount_enemy_damage = 0
								amount_enemy_critical = 0
								amount_enemy_bashed = 0
								amount_enemy_blocked = 0
								amount_enemy_spikes = 0
								amount_enemy_gold_rush = 0
								amount_enemy_blindness = 0
								amount_enemy_poisoned = 0
								amount_enemy_net_damaged = 0
								amount_enemy_vampirise = 0
								amount_enemy_healed = 0
								amount_enemy_missed = 0
								amount_enemy_armour_theft = 0
								amount_enemy_damage_theft = 0

								while your_hp > 0 and enemy_hp > 0 :
									bash_chance = random.randint(1,100)
									heal_chance = random.randint(1,100)
									miss_chance = random.randint(1,100)
									critical_chance = random.randint(1,100)
									block_chance = random.randint(1,100)
									armour_theft_chance = random.randint(1,100)
									damage_theft_chance = random.randint(1,100)
									blindness_chance = random.randint(1,100)
									poison_chance = random.randint(1,100)
									gold_rush_chance = random.randint(1,100)
									vampirise_chance = random.randint(1,100)
									net_damage_chance = random.randint(1,100)
									spike_chance = random.randint(1,100)


									if you_bashed == False:
										if enemy_miss + your_blinded < miss_chance:
											if your_bash >= bash_chance:
												enemy_bashed = True
												amount_your_bashed += 1
											if your_heal >= heal_chance:

												one_percent = your_hp / 100
												your_hp += int(one_percent * 30)
												amount_your_healed += int(one_percent * 30)
												your_blinded = 0
												your_poisoned = 0
											if your_armour_theft >= armour_theft_chance and enemy_armour >= 2:
												enemy_armour = enemy_armour - 2
												your_armour += 2
												amount_your_armour_theft += 2
											if your_damage_theft >= armour_theft_chance and enemy_damage >= 2:
												enemy_damage = enemy_damage - 2
												your_damage += 2
												amount_your_damage_theft += 2
											if your_poison >= poison_chance:
												enemy_poisoned += 2
											if your_blindness >= blindness_chance:
												enemy_blinded += 2
												amount_your_blindness += 2 

											your_hit = 0
											#ataka
											if enemy_block < block_chance:
												double_damage = 1
												if your_critical >= critical_chance:
													double_damage = 2
												if your_net_damage >= net_damage_chance:
													your_hit = (your_damage * your_speed) * double_damage 
												else:
													your_hit = ((your_damage * your_speed) * double_damage)

													if enemy_armour >= int(your_hit):
														enemy_armour = enemy_armour - int(your_hit)
														your_hit = 0

												enemy_hp = enemy_hp - int(your_hit)
												amount_your_hit += 1
												amount_your_damage += int(your_hit)
												if your_vampirise >= vampirise_chance:
													your_hp += int(your_hit)
													amount_your_healed += int(your_hit)
												double_damage = 1
												if enemy_spikes >= spike_chance:
													your_hp = your_hp - int(your_hit / 2)
													amount_enemy_spikes += int(your_hit / 2)
											else:
												your_hit = your_damage * your_speed
												amount_your_hit += 1
												amount_your_damage += int(your_hit / 2)
												enemy_hp = enemy_hp - int(your_hit / 2)
												amount_enemy_blocked += int(your_hit /2)

											

											enemy_hp = enemy_hp - enemy_poisoned
											amount_enemy_poisoned += enemy_poisoned
										else:
											amount_your_missed += 1 

									else:
										you_bashed = False

									if enemy_hp <= 0 or your_hp <= 0:
										break
									
									if enemy_bashed == False:
										if your_miss + enemy_blinded < miss_chance:
											if enemy_bash >= bash_chance:
												your_bashed = True
												amount_enemy_bashed += 1
											if enemy_heal >= heal_chance:

												one_percent = enemy_hp / 100
												enemy_hp += int(one_percent * 30)
												amount_enemy_healed += int(one_percent * 30)
												enemy_blinded = 0
												enemy_poisoned = 0
											if enemy_armour_theft >= armour_theft_chance and your_armour >= 2:
												your_armour = your_armour - 2
												enemy_armour += 2
												amount_enemy_armour_theft += 2
											if enemy_damage_theft >= armour_theft_chance and your_damage >= 2:
												your_damage = your_damage - 2
												enemy_damage += 2
												amount_enemy_damage_theft += 2
											if enemy_poison >= poison_chance:
												your_poisoned += 2
											if enemy_blindness >= blindness_chance:
												your_blinded += 2
												amount_enemy_blindness += 2 

											enemy_hit = 0
											#ataka
											if your_block < block_chance:
												double_damage = 1
												if enemy_critical >= critical_chance:
													double_damage = 2
												if enemy_net_damage >= net_damage_chance:
													enemy_hit = (enemy_damage * enemy_speed) * double_damage 
												else:
													enemy_hit = ((enemy_damage * enemy_speed) * double_damage) 
													if your_armour >= int(enemy_hit):
														your_armour = your_armour - int(enemy_hit)
														enemy_hit = 0

												your_hp = your_hp - int(enemy_hit)
												amount_enemy_hit += 1
												amount_enemy_damage += int(enemy_hit)
												if enemy_vampirise >= vampirise_chance:
													enemy_hp += int(enemy_hit)
													amount_enemy_healed += int(enemy_hit)
												double_damage = 1
												if your_spikes >= spike_chance:
													enemy_hp = enemy_hp - int(enemy_hit / 2)
													amount_your_spikes += int(enemy_hit / 2)
											else:
												enemy_hit = enemy_damage * enemy_speed
												amount_enemy_hit += 1
												amount_enemy_damage += int(enemy_hit) / 2
												your_hp = your_hp - int(enemy_hit / 2)
												amount_your_blocked += int(enemy_hit / 2)
											
											your_hp = your_hp - your_poisoned
											amount_your_poisoned += your_poisoned

										else:
											amount_enemy_missed += 1 

									else:
										enemy_bashed = False

									if enemy_hp <= 0 or your_hp <= 0:
										break
								cursor.execute("SELECT log_status FROM users_settings WHERE tgid = ? ",(msg.from_user.id,))
								log_status = int(cursor.fetchone()[0]);
								cursor.execute("SELECT log_status FROM users_settings WHERE tgid = ? ",(enemy_tg,))
								enemy_log_status = int(cursor.fetchone()[0]);

								your_result = '0'
								enemy_result = '0'
								result_message = '0'
								enemy_gold_msg = '0'
								your_gold_msg = '0'
								if your_hp <= 0:
									your_result = '❌Вы проиграли в дуэли с ' + enemy_name
									enemy_result = '✅Вы победили в дуэли с ' + your_name

									cursor.execute("UPDATE statistic SET win_duels = win_duels + 1 WHERE tgid = ? ",(msg.from_user.id,))
									connect.commit()

									if log_status == 0:
										result_message = '\n\n🔹Вы нанесли урона: ' +str(int(amount_your_damage))+ '\n🔹Вы нанесли ударов: '+ str(amount_your_hit) + '\n🔹Вы восстановили здоровья: ' + str(amount_your_healed) 
										result_message += '\n\n\n🔸Противник нанёс урона: ' +str(int(amount_enemy_damage))+ '\n🔸Противник нанёс ударов: '+ str(amount_enemy_hit) + '\n🔸Противник восстановил здоровья: ' + str(amount_enemy_healed) 
									else:
										result_message = '\n\n🔹Вы нанесли урона: ' +str(int(amount_your_damage))+ '\n🔹Вы нанесли ударов: '+ str(amount_your_hit) + '\n🔹Вы восстановили здоровья: ' + str(amount_your_healed) 
										result_message += '\n🔹Вы заблокировали урона: ' +str(amount_your_blocked)+ '\n🔹Вы отразили урона шипами: ' + str(amount_your_spikes) + '\n🔹Вы своровали брони: ' +str(your_armour_theft)+ '\n🔹Вы своровали урона: ' +str(your_damage_theft)+ '\n🔹Урон противнику ядом: ' + str(amount_enemy_poisoned)+ '\n🔹Общее ослепление противника: ' +str(amount_your_blindness)+ '\n🔹Вы уклонились от ударов: ' +str(amount_enemy_missed)+ '\n🔹Вы оглушили противника: ' + str(amount_your_bashed)
										result_message += '\n\n\n🔸Противник нанёс урона: ' +str(int(amount_enemy_damage))+ '\n🔸Противник нанёс ударов: '+ str(amount_enemy_hit) + '\n🔸Противник восстановил здоровья: ' + str(amount_enemy_healed) 
										result_message += '\n🔸Противник заблокировал урона: ' +str(amount_enemy_blocked)+ '\n🔸Противник отразил урона шипами: ' + str(amount_enemy_spikes) + '\n🔸Противник своровал брони: ' +str(amount_enemy_armour_theft)+ '\n🔸Противник своровал урона: ' +str(amount_enemy_damage_theft)+ '\n🔸Урон по вам ядом: ' + str(amount_your_poisoned)+ '\n🔸Общее ослепление вас: ' +str(amount_enemy_blindness)+ '\n🔸Противник уклонился от ударов: ' +str(amount_your_missed)+ '\n🔸Противник оглушил вас: ' + str(amount_enemy_bashed)
									
									if enemy_log_status == 0:
										enemy_result_message = '\n\n🔹Вы нанесли урона: ' +str(int(amount_enemy_damage))+ '\n🔹Вы нанесли ударов: '+ str(amount_enemy_hit) + '\n🔹Вы восстановили здоровья: ' + str(amount_enemy_healed) 
										enemy_result_message += '\n\n\n🔸Противник нанёс урона: ' +str(int(amount_your_damage))+ '\n🔸Противник нанёс ударов: '+ str(amount_your_hit) + '\n🔸Противник восстановил здоровья: ' + str(amount_your_healed) 
									else:
										enemy_result_message = '\n\n🔹Вы нанесли урона: ' +str(int(amount_enemy_damage))+ '\n🔹Вы нанесли ударов: '+ str(amount_enemy_hit) + '\n🔹Вы восстановили здоровья: ' + str(amount_enemy_healed) 
										enemy_result_message += '\n🔹Вы заблокировали урона: ' +str(amount_enemy_blocked)+ '\n🔹Вы отразили урона шипами: ' + str(amount_enemy_spikes) + '\n🔹Вы своровали брони: ' +str(amount_enemy_armour_theft)+ '\n🔹Вы своровали урона: ' +str(amount_enemy_damage_theft)+ '\n🔹Урон противнику ядом: ' + str(amount_your_poisoned)+ '\n🔹Общее ослепление противника: ' +str(amount_enemy_blindness)+ '\n🔹Вы уклонились от ударов: ' +str(amount_your_missed)+ '\n🔹Вы оглушили противника: ' + str(amount_enemy_bashed)
										enemy_result_message += '\n\n\n🔸Противник нанёс урона: ' +str(int(amount_your_damage))+ '\n🔸Противник нанёс ударов: '+ str(amount_your_hit) + '\n🔸Противник восстановил здоровья: ' + str(amount_your_healed) 
										enemy_result_message += '\n🔸Противник заблокировал урона: ' +str(amount_your_blocked)+ '\n🔸Противник отразил урона шипами: ' + str(amount_your_spikes) + '\n🔸Противник своровал брони: ' +str(amount_your_armour_theft)+ '\n🔸Противник своровал урона: ' +str(amount_your_damage_theft)+ '\n🔸Урон по вам ядом: ' + str(amount_enemy_poisoned)+ '\n🔸Общее ослепление вас: ' +str(amount_your_blindness)+ '\n🔸Противник уклонился от ударов: ' +str(amount_enemy_missed)+ '\n🔸Противник оглушил вас: ' + str(amount_your_bashed)
									cursor.execute("UPDATE rpg_users_personage SET coins = coins + 10 WHERE tgid = ? ",(enemy_tg,))
									connect.commit()
									enemy_gold_msg = 'Вы получили 10 монет💰'

									cursor.execute("SELECT coins FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
									your_coins = int(cursor.fetchone()[0]); 

									if your_coins > 5:
										cursor.execute("UPDATE rpg_users_personage SET coins = coins - 5 WHERE tgid = ? ",(msg.from_user.id,))
										connect.commit()

									else:
										cursor.execute("UPDATE rpg_users_personage SET coins = 0 WHERE tgid = ? ",(msg.from_user.id,))
										connect.commit()
									your_gold_msg = 'Вы потеряли 5 монет💰'
									


								elif enemy_hp <= 0:
									cursor.execute("UPDATE statistic SET win_duels = win_duels + 1 WHERE tgid = ? ",(msg.from_user.id,))
									connect.commit()
									enemy_result = '❌Вы проиграли в дуэли с ' + your_name
									your_result = '✅Вы победили в дуэли с ' + enemy_name
									if log_status == 0:
										result_message = '\n\n🔹Вы нанесли урона: ' +str(int(amount_your_damage))+ '\n🔹Вы нанесли ударов: '+ str(amount_your_hit) + '\n🔹Вы восстановили здоровья: ' + str(amount_your_healed) 
										result_message += '\n\n\n🔸Противник нанёс урона: ' +str(int(amount_enemy_damage))+ '\n🔸Противник нанёс ударов: '+ str(amount_enemy_hit) + '\n🔸Противник восстановил здоровья: ' + str(amount_enemy_healed) 
									else:
										result_message = '\n\n🔹Вы нанесли урона: ' +str(int(amount_your_damage))+ '\n🔹Вы нанесли ударов: '+ str(amount_your_hit) + '\n🔹Вы восстановили здоровья: ' + str(amount_your_healed) 
										result_message += '\n🔹Вы заблокировали урона: ' +str(amount_your_blocked)+ '\n🔹Вы отразили урона шипами: ' + str(amount_enemy_spikes) + '\n🔹Вы своровали брони: ' +str(your_armour_theft)+ '\n🔹Вы своровали урона: ' +str(your_damage_theft)+ '\n🔹Урон противнику ядом: ' + str(amount_enemy_poisoned)+ '\n🔹Общее ослепление противника: ' +str(amount_your_blindness)+ '\n🔹Вы уклонились от ударов: ' +str(amount_enemy_missed)+ '\n🔹Вы оглушили противника: ' + str(amount_your_bashed)
										result_message += '\n\n\n🔸Противник нанёс урона: ' +str(int(amount_enemy_damage))+ '\n🔸Противник нанёс ударов: '+ str(amount_enemy_hit) + '\n🔸Противник восстановил здоровья: ' + str(amount_enemy_healed) 
										result_message += '\n🔸Противник заблокировал урона: ' +str(amount_enemy_blocked)+ '\n🔸Противник отразил урона шипами: ' + str(amount_your_spikes) + '\n🔸Противник своровал брони: ' +str(amount_enemy_armour_theft)+ '\n🔸Противник своровал урона: ' +str(amount_enemy_damage_theft)+ '\n🔸Урон по вам ядом: ' + str(amount_your_poisoned)+ '\n🔸Общее ослепление вас: ' +str(amount_enemy_blindness)+ '\n🔸Противник уклонился от ударов: ' +str(amount_your_missed)+ '\n🔸Противник оглушил вас: ' + str(amount_enemy_bashed)
									
									if enemy_log_status == 0:
										enemy_result_message = '\n\n🔹Вы нанесли урона: ' +str(int(amount_enemy_damage))+ '\n🔹Вы нанесли ударов: '+ str(amount_enemy_hit) + '\n🔹Вы восстановили здоровья: ' + str(amount_enemy_healed) 
										enemy_result_message += '\n\n\n🔸Противник нанёс урона: ' +str(int(amount_your_damage))+ '\n🔸Противник нанёс ударов: '+ str(amount_your_hit) + '\n🔸Противник восстановил здоровья: ' + str(amount_your_healed) 
									else:
										enemy_result_message = '\n\n🔹Вы нанесли урона: ' +str(int(amount_enemy_damage))+ '\n🔹Вы нанесли ударов: '+ str(amount_enemy_hit) + '\n🔹Вы восстановили здоровья: ' + str(amount_enemy_healed) 
										enemy_result_message += '\n🔹Вы заблокировали урона: ' +str(amount_enemy_blocked)+ '\n🔹Вы отразили урона шипами: ' + str(amount_enemy_spikes) + '\n🔹Вы своровали брони: ' +str(amount_enemy_armour_theft)+ '\n🔹Вы своровали урона: ' +str(amount_enemy_damage_theft)+ '\n🔹Урон противнику ядом: ' + str(amount_your_poisoned)+ '\n🔹Общее ослепление противника: ' +str(amount_enemy_blindness)+ '\n🔹Вы уклонились от ударов: ' +str(amount_your_missed)+ '\n🔹Вы оглушили противника: ' + str(amount_enemy_bashed)
										enemy_result_message += '\n\n\n🔸Противник нанёс урона: ' +str(int(amount_your_damage))+ '\n🔸Противник нанёс ударов: '+ str(amount_your_hit) + '\n🔸Противник восстановил здоровья: ' + str(amount_your_healed) 
										enemy_result_message += '\n🔸Противник заблокировал урона: ' +str(amount_your_blocked)+ '\n🔸Противник отразил урона шипами: ' + str(amount_your_spikes) + '\n🔸Противник своровал брони: ' +str(amount_your_armour_theft)+ '\n🔸Противник своровал урона: ' +str(amount_your_damage_theft)+ '\n🔸Урон по вам ядом: ' + str(amount_enemy_poisoned)+ '\n🔸Общее ослепление вас: ' +str(amount_your_blindness)+ '\n🔸Противник уклонился от ударов: ' +str(amount_enemy_missed) + '\n🔸Противник оглушил вас: ' + str(amount_your_bashed)
									enemy_result_message += '\n\nДля реванша введите: пвп ' + str(your_id)

									cursor.execute("UPDATE rpg_users_personage SET coins = coins + 10 WHERE tgid = ? ",(msg.from_user.id,))
									connect.commit()
									your_gold_msg = 'Вы получили 10 монет💰'
									cursor.execute("SELECT coins FROM rpg_users_personage WHERE tgid = ? ",(enemy_tg,))
									your_coins = int(cursor.fetchone()[0]); 
									if your_coins > 5:
										cursor.execute("UPDATE rpg_users_personage SET coins = coins - 5 WHERE tgid = ? ",(enemy_tg,))
										connect.commit()
									else:
										cursor.execute("UPDATE rpg_users_personage SET coins = 0 WHERE tgid = ? ",(enemy_tg,))
										connect.commit()
									enemy_gold_msg = 'Вы потеряли 5 монет💰'
										
								cursor.execute("UPDATE rpg_users_stats SET energy = energy - ? WHERE tgid = ? ",(7,msg.from_user.id,))
								connect.commit()
								cursor.execute("UPDATE rpg_users_stats SET energy = energy - ? WHERE tgid = ? ",(5,enemy_tg,))
								connect.commit()
								cursor.execute("UPDATE statistic SET amount_duels = amount_duels + 1 WHERE tgid = ? ",(msg.from_user.id,))
								connect.commit()
								cursor.execute("UPDATE statistic SET amount_duels = amount_duels + 1 WHERE tgid = ? ",(enemy_tg,))
								connect.commit()
								await msg.reply(your_result + result_message + '\n\n' + your_gold_msg)
								try:
									await bot.send_message(enemy_tg,enemy_result + enemy_result_message + '\n\n' + enemy_gold_msg)
								except Exception as ex:
									return 0
							else:
								await msg.reply('Извините, вы не можете сражаться с собой!🛑')		
						else:
							await msg.reply('Соперник не принимает вызовы.🛑')

					except Exception as ex:
						print(ex)
						await msg.reply('Не удалось провести дуэль🛑')

				else:
					await msg.reply("У вас недостаточно энергии для этого действия!🛑")
			else:
				await msg.reply('Вы не можете сражаться пока ваши дуэли выключены!🚫')
		cursor.execute("SELECT position FROM rpg_users WHERE tgid = ? ",(msg.from_user.id,))
		partner_position = int(cursor.fetchone()[0]);

		if partner_position == 707:
			cursor.execute("SELECT name FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
			your_name = cursor.fetchone()[0];

			cursor.execute("SELECT want_partner FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
			want_partner = cursor.fetchone()[0];

			cursor.execute("SELECT name FROM rpg_users_personage WHERE tgid = ? ",(want_partner,))
			want_partner_name = cursor.fetchone()[0];


			if msg.text == 'Принять✅':
				cursor.execute("SELECT partner FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
				your_partner = cursor.fetchone()[0];
				cursor.execute("SELECT want_partner FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
				want_partner = cursor.fetchone()[0];
				cursor.execute("SELECT partner FROM rpg_users_personage WHERE tgid = ? ",(want_partner,))
				partner_partner = cursor.fetchone()[0];
				if partner_partner == 0:
					if your_partner == 0:


						cursor.execute("UPDATE rpg_users SET position = 0 WHERE tgid = ? ",(msg.from_user.id,))
						connect.commit()

						cursor.execute("UPDATE rpg_users_personage SET partner = ? WHERE tgid = ? ",(want_partner,msg.from_user.id,))
						connect.commit()

						cursor.execute("UPDATE rpg_users_personage SET partner = ? WHERE tgid = ? ",(msg.from_user.id, want_partner))
						connect.commit()

						cursor.execute("UPDATE rpg_users_personage SET want_partner = 0 WHERE tgid = ? ",(msg.from_user.id,))
						connect.commit()

						await msg.reply("🥳Поздравляем! Вы успешно заключили брак с " + want_partner_name + '.',reply_markup = ReplyKeyboardRemove())
						await bot.send_message(want_partner,'🥳Поздравляем! ' + your_name + " принял(а) ваше предложение вступить в брак.")
					else:
						await msg.reply('Вы уже состоите в браке🤨',reply_markup = ReplyKeyboardRemove())
				else:
					await msg.reply('Игрок, предложивший вам вступить в брак уже имеет партнёра!🤨',reply_markup = ReplyKeyboardRemove())
				cursor.execute("UPDATE rpg_users_personage SET want_partner = 0 WHERE tgid = ? ",(msg.from_user.id,))
				connect.commit()
				cursor.execute("UPDATE rpg_users SET position = 0 WHERE tgid = ? ",(msg.from_user.id,))
				connect.commit()

			elif msg.text == 'Отклонить❌':
				cursor.execute("UPDATE rpg_users SET position = 0 WHERE tgid = ? ",(msg.from_user.id,))
				connect.commit()

				cursor.execute("UPDATE rpg_users_personage SET want_partner = 0 WHERE tgid = ? ",(msg.from_user.id,))
				connect.commit()

				await msg.reply('Хорошо, предложение вступить в брак отклонено!🤪',reply_markup = ReplyKeyboardRemove())
				await bot.send_message(want_partner, your_name + " отклонил(а) ваше предложение вступить в брак😔.")
		elif Splited_msg[0].lower() == 'ставка' or Splited_msg[0].lower() == 'bet' or Splited_msg[0].lower == 'rate':
			try:
				cursor.execute("SELECT coins FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
				balance = int(cursor.fetchone()[0]);
				rate = Splited_msg[1]
				multipler = 1
				if rate == 'все' or rate == 'всё':
					rate = balance
				elif rate == 'половина' or rate == 'половину':
					rate = int(balance / 2)
				else:
					rate = int(rate)

				if rate > 0:
					if len(Splited_msg) == 2:
						if rate <= balance:
							cursor.execute("UPDATE statistic SET bet = bet + 1 WHERE tgid = ? ",(msg.from_user.id,))
							connect.commit()
							cursor.execute("UPDATE rpg_users_personage SET coins = coins - ? WHERE tgid = ? ",(int(rate),msg.from_user.id,))
							connect.commit()
							multipler_rnd = random.randint(0,10000) #0,0.25,0.50,0.75,1,1.5,2,5,30
							if multipler_rnd >= 9950 and multipler_rnd < 10000: #0.5%
								multipler = 30
							elif multipler_rnd < 9950 and multipler_rnd >= 8950: #10%
								multipler = 0
							elif multipler_rnd < 8950 and multipler_rnd >= 8600: #3.5%
								multipler = 5
							elif multipler_rnd < 8600 and multipler_rnd >= 7350: #12.5%
								multipler = 0.25
							elif multipler_rnd < 7350 and multipler_rnd >= 5350: #20%
								multipler = 1
							elif multipler_rnd < 5350 and multipler_rnd >= 3750: #16%
								multipler = 0.50
							elif multipler_rnd < 3750 and multipler_rnd >= 2300: #14.5
								multipler = 0.75
							elif multipler_rnd < 2300 and multipler_rnd >= 1000: #13%
								multipler = 1.5
							elif multipler_rnd < 1000 and multipler_rnd >= 0: #10%
								multipler = 2
							else:
								multipler = 1
							rate = int(rate * multipler)
							cursor.execute("UPDATE rpg_users_personage SET coins = coins + ? WHERE tgid = ? ",(int(rate),msg.from_user.id,))
							connect.commit()
							cursor.execute("SELECT coins FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
							balance = int(cursor.fetchone()[0]);
							await msg.reply('Ваша ставка умножена на x' + str(multipler) + '\nВаш баланс: ' + str(balance) + '💰')


						else:
							await msg.reply('Недостаточно денег на балансе!🛑')
					else:
						await msg.reply('Неправильное использование команды!🛑')
				else:	
					await msg.reply('Нельзя ставить на 0 или меньше!🛑')
			except Exception as ex:
				print(6)
				await msg.reply('Неправильное использование команды!🛑')
				print(ex)
		elif Splited_msg[0].lower() == 'брак' and len(Splited_msg) == 2:


			partner_id = int(Splited_msg[1])
			cursor.execute("SELECT tgid FROM rpg_users_stats WHERE userid = ? ",(partner_id,))
			partner_tg = int(cursor.fetchone()[0]);
			cursor.execute("SELECT name FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
			your_name = cursor.fetchone()[0];

			cursor.execute("SELECT name FROM rpg_users_personage WHERE tgid = ? ",(partner_tg,))
			partner_name = cursor.fetchone()[0];

			cursor.execute("SELECT partner FROM rpg_users_personage WHERE tgid = ? ",(partner_tg,))
			want_partner_partner = cursor.fetchone()[0];

			cursor.execute("SELECT partner FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
			your_partner = cursor.fetchone()[0];

			cursor.execute("SELECT want_partner FROM rpg_users_personage WHERE tgid = ? ",(partner_tg,))
			want_partner_check = cursor.fetchone()[0];

			if your_partner != partner_tg:
				if your_partner == 0:
					if want_partner_partner == 0:
						if int(partner_tg) != msg.from_user.id :
							if want_partner_check != msg.from_user.id:
								await bot.send_message(partner_tg, your_name + ' предлагает вам вступить в брак!💍',reply_markup = kb.partner_kb)
								cursor.execute("UPDATE rpg_users SET position = 707 WHERE tgid = ? ",(partner_tg,))
								connect.commit()

								cursor.execute("UPDATE rpg_users_personage SET want_partner = ? WHERE tgid = ? ",(msg.from_user.id,partner_tg,))
								connect.commit()

								await msg.reply('Предложение о браке отправлено, ожидайте результат.⏳')
							else:
								await msg.reply('Вы уже отправили предложение о браке этому человеку!❌')
						else:
							await msg.reply('Невозможно вступить в брак с самим собой!❌')
					else:
						await msg.reply(partner_name + ' уже состоит в браке!❌')
				else:
					await msg.reply('Для вступление в новый брак нужно разветись с текущим партнёром!❌')
			else:
				await msg.reply('Вы уже состоите в браке с ' + partner_name + '!❌')



		elif msg.text.lower() == 'шахта' or msg.text.lower() == '/mine' or msg.text.lower() == '/mine' + bot_name:
			if await CheckMine() == True:
				cursor.execute("SELECT workers FROM mine WHERE tgid = ? ",(msg.from_user.id,))
				workers = str(cursor.fetchone()[0]);
				cursor.execute("SELECT max_workers FROM mine WHERE tgid = ? ",(msg.from_user.id,))
				max_workers = str(cursor.fetchone()[0]);
				cursor.execute("SELECT gold FROM mine WHERE tgid = ? ",(msg.from_user.id,))
				gold = str(cursor.fetchone()[0]);
				cursor.execute("SELECT max_gold FROM mine WHERE tgid = ? ",(msg.from_user.id,))
				max_gold = str(cursor.fetchone()[0]);
				cursor.execute("SELECT mine_lvl FROM mine WHERE tgid = ? ",(msg.from_user.id,))
				mine_lvl = int(cursor.fetchone()[0]);

				resource = 'Уголь'
				if mine_lvl == 1:
					resource = 'Уголь'
				if mine_lvl == 2:
					resource = 'Медь'
				if mine_lvl == 3:
					resource = 'Свинец'
				if mine_lvl == 4:
					resource = 'Железо'
				if mine_lvl == 5:
					resource = 'Серебро'
				if mine_lvl == 6:
					resource = 'Золото'
				if mine_lvl == 7:
					resource = 'Изумруды'
				if mine_lvl == 8:
					resource = 'Рубины'
				if mine_lvl == 9:
					resource = 'Сапфиры'
				if mine_lvl == 10:
					resource = 'Лунная руда'
				if mine_lvl == 11:
					resource = 'Алмазы'
				if mine_lvl == 12:
					resource = 'Тёмные кристаллы'
				if mine_lvl == 13:
					resource = 'Святая руда'
				if mine_lvl == 14:
					resource = 'Адская руда'
				if mine_lvl >= 15:
					resource = 'Титанические кристаллы'

				await msg.reply('⛏Информация о вашей шахте:\n\n💎Добываемый ресурс: '+ resource +'\n👷Рабочие: '+ workers + '/'+ max_workers +'\n✳️Уровень шахты: '+str(mine_lvl)+'\n💹Добыча золота: ' + str(int((int(workers) * mine_lvl) / 2)) +'/30мин.\n💰Добытое золото: '+gold+'/'+max_gold+'\n\nℹ️Помощь: /mine_help')
			else:
				cursor.execute("SELECT coins FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
				coins = int(cursor.fetchone()[0]);
				if coins < 1500:
					await msg.reply('Извините, у вас не хватает денег на покупку шахты😟(Стоимость 1500 монет💰)')
				else:
					await bot.send_message(msg.from_user.id,'Желаете купить шахту?(Стоимость 1500 монет💰)',reply_markup = kb.YN_kb)
					cursor.execute("UPDATE rpg_users SET position = 21 WHERE tgid = ? ",(msg.from_user.id,))
					connect.commit()
		elif msg.text.lower() == '/mine_help' or msg.text.lower() == '/mine_help' + bot_name:
			await msg.reply('ℹ️Ваша задача прокачивать шахту (/mine_pump) и нанимать работников, всё это будет приносить вам золото, чем больше рабочих и чем выше уровень - тем выше ваш доход.\nДоступые команды для шахты: \n\n▪️Шахта - просмотр информации о шахте.\n▪️Шахта нанять кол-во - нанять кол-во работников на вашу шахту(1 работник = 50 монет).\n▪️Шахта продать кол-во - продать кол-во работников(1 работник = 25 монет)\n▪️Шахта забрать кол-во - забрать кол-во добытого на шахте золота.\n▪️Шахта улучшить - улучшить шахту.')
		elif msg.text == '/mine_pump' or msg.text == '/mine_pump' + bot_name or Splited_msg[0].lower() == 'шахта' or Splited_msg[0].lower() == 'mine':
			if await CheckMine() == True:
				if  msg.text == '/mine_pump' or msg.text == '/mine_pump' + bot_name or Splited_msg[1].lower() == 'улучшить' or Splited_msg[1].lower() == 'прокачать' or Splited_msg[1].lower() == 'pump' or Splited_msg[1].lower() == 'лвл':
					cursor.execute("SELECT mine_lvl FROM mine WHERE tgid = ? ",(msg.from_user.id,))
					mine_lvl = int(cursor.fetchone()[0]);
					if mine_lvl < 15:
						cursor.execute("SELECT coins FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
						coins = int(cursor.fetchone()[0]);
						if coins >= mine_lvl * 1000:
							minus = mine_lvl * 1000 * 4
							cursor.execute("UPDATE rpg_users_personage SET coins = coins - ? WHERE tgid = ? ",(minus,msg.from_user.id,))
							connect.commit()
							cursor.execute("UPDATE mine SET mine_lvl = mine_lvl + 1 WHERE tgid = ? ",(msg.from_user.id,))
							connect.commit()
							cursor.execute("UPDATE mine SET max_gold = max_gold + 1000 WHERE tgid = ? ",(msg.from_user.id,))
							connect.commit()
							cursor.execute("UPDATE mine SET max_workers = max_workers + 25 WHERE tgid = ? ",(msg.from_user.id,))
							connect.commit()
							await msg.reply('🥳Поздравляем, вы успешно прокачали шахту, потратив: ' + str(minus) + ' монет💰\n\nБонусы от повышения уровня: \n✅ +25 к максимальному кол-ву рабочих\n✅ +1000 к максимальному кол-ву золота\n✅ Новый добываемый ресурс')
						else:
							await msg.reply('Извините, у вас не хватает денег на улучшение шахты😟!(Стоимость улучшения: ' + str(minus) + ' золота)' + '\n\n💰Ваш баланс: ' + str(coins))
					else:
						await msg.reply('Вы не можете улучшить шахту, т.к ваша шахта имеет максимальный уровень!😉')


				elif Splited_msg[1].lower() == 'купить' or  Splited_msg[1].lower() == 'buy' or Splited_msg[1].lower() == 'нанять':
					try:
						buy_amount = int(Splited_msg[2])
						if buy_amount > 0:
							cursor.execute("SELECT workers FROM mine WHERE tgid = ? ",(msg.from_user.id,))
							workers = int(cursor.fetchone()[0]);
							cursor.execute("SELECT max_workers FROM mine WHERE tgid = ? ",(msg.from_user.id,))
							max_workers = int(cursor.fetchone()[0]);
							if max_workers - workers >= buy_amount:
								cursor.execute("SELECT coins FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
								coins = int(cursor.fetchone()[0]);
								if buy_amount * 100 <= coins:
									minus = buy_amount * 100
									cursor.execute("UPDATE rpg_users_personage SET coins = coins - ? WHERE tgid = ? ",(minus,msg.from_user.id,))
									connect.commit()
									cursor.execute("UPDATE mine SET workers = workers + ? WHERE tgid = ? ",(int(Splited_msg[2]),msg.from_user.id,))
									connect.commit()
									await msg.reply('Поздравляем, вы наняли ' + str(buy_amount) + ' рабочих!👷')
								else:
									await msg.reply('У вас не хватает денег на такое количество рабочих!😦')
							else:
								await msg.reply('Вы не можете купить столько рабочих из-за нехватки места для них!😦')
						else:
							await msg.reply('Нельзя купить 0 или меньше рабочих!😦')
					except:
						await msg.reply('Извините, произошла ошибка при обработке команды!😬')

				elif Splited_msg[1].lower() == 'sell' or Splited_msg[1].lower() == 'продать' or Splited_msg[1].lower() == 'уволить':
					try:
						sell_amount = int(Splited_msg[2])
						cursor.execute("SELECT workers FROM mine WHERE tgid = ? ",(msg.from_user.id,))
						workers = int(cursor.fetchone()[0]);
						if workers >= sell_amount:
							cursor.execute("UPDATE mine SET workers = workers - ? WHERE tgid = ? ",(int(Splited_msg[2]),msg.from_user.id,))
							connect.commit()
							await AddCoins(int(sell_amount * 25),False,False)
							await msg.reply('Вы успешно уволили ' + str(sell_amount) + ' рабочих и получили ' + str(int(sell_amount * 25)) +' монет!💰')

						else:
							await msg.reply('У вас нет столько рабочих!😦')	
					except:
						await msg.reply('Извините, произошла ошибка при обработке команды!😬')

				elif Splited_msg[1] == 'собрать' or Splited_msg[1].lower() == 'золото' or Splited_msg[1].lower() == 'голда' or Splited_msg[1].lower() == 'добыча' or Splited_msg[1].lower() == 'взять' or Splited_msg[1].lower() == 'забрать':
					try:
						get_amount = 1
						cursor.execute("SELECT gold FROM mine WHERE tgid = ? ",(msg.from_user.id,))
						gold = int(cursor.fetchone()[0]);
						if Splited_msg[2] == 'all' or Splited_msg[2] == 'всё' or Splited_msg[2] == 'все':
							get_amount = gold
						else:
							get_amount = int(Splited_msg[2])

						if get_amount <= gold:
							if get_amount > 0:
								cursor.execute("UPDATE mine SET gold = gold - ? WHERE tgid = ? ",(get_amount,msg.from_user.id,))
								connect.commit()
								await AddCoins(get_amount,False,False)

								cursor.execute("SELECT gold FROM mine WHERE tgid = ? ",(msg.from_user.id,))
								gold = int(cursor.fetchone()[0]);
								cursor.execute("SELECT coins FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
								balance = int(cursor.fetchone()[0]);
								await msg.reply('Поздравляем, вы собрали ' + str(get_amount) + ' монет!💰')
							else:
								await msg.reply('Неправильная сумма для вывода денег!😦')
						else:
							await msg.reply('У вас нет столько доступных денег для вывода!😦')
					except:
						await msg.reply('Извините, произошла ошибка при обработке команды!😬')

			else:
				await msg.reply('😳Извините, но у вас нет шахты, введите: /mine для покупки!')	 


		elif user_position == 21:
			if msg.text == 'Да✅':
				cursor.execute("SELECT coins FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
				coins = int(cursor.fetchone()[0]);
				if coins < 1500:
					await msg.reply('Извините, у вас не хватает денег на покупку шахты😟(Стоимость 1500 монет💰)')
				else:
					cursor.execute("UPDATE rpg_users_personage SET coins = coins - 1500 WHERE tgid = ? ",(msg.from_user.id,))
					connect.commit()
					await msg.reply('Поздравляем, вы купили собственную шахту🥳. Используйте /mine_help , чтобы узнать информацию о командах для шахты🧐.', reply_markup = ReplyKeyboardRemove())
					await db.MineReg(msg.from_user.id)
			else:
				await msg.reply('Хорошо, но я всё же советую вам приобрести щахту!😉', reply_markup = ReplyKeyboardRemove())


			cursor.execute("UPDATE rpg_users SET position = 0 WHERE tgid = ? ",(msg.from_user.id,))
			connect.commit()




			################await msg.reply(str(msg.reply_to_message.from_user.id))



		elif msg.text.lower() == 'настройки' or msg.text.lower() == '/settings' or msg.text.lower() == '/settings' + bot_name:
			cursor.execute("SELECT duel_status FROM users_settings WHERE tgid = ? ",(msg.from_user.id,))
			duel_status = cursor.fetchone()[0];

			cursor.execute("SELECT log_status FROM users_settings WHERE tgid = ? ",(msg.from_user.id,))
			log_status = cursor.fetchone()[0];
			cursor.execute("SELECT autosell_status FROM users_settings WHERE tgid = ? ",(msg.from_user.id,))
			autosell_status = cursor.fetchone()[0];
			duel_msg = ' '
			log_msg = ' '
			autosell_msg = ' '
			if duel_status == 0:
				duel_msg = 'Включены✅'
			else:
				duel_msg = 'Выключены🚫'
			if log_status == 0:
				log_msg = 'Выключен🚫'
			else:
				log_msg = 'Включён✅'
			if autosell_status == 0:
				autosell_msg = 'Выключена🚫'
			else:
				autosell_msg = 'Включена✅'
			turn_autosell = '/autosell_'
			turn_log = '/log_'
			turn_duels = '/duel_'
			if log_status == 0:
				turn_log += str(1)
			else:
				turn_log += str(0)

			if duel_status == 0:
				turn_duels += str(1)
			else:
				turn_duels += str(0)

			if autosell_status == 0:
				turn_autosell += str(1)
			else:
				turn_autosell += str(0)


			await msg.reply('⚙️Ваши настройки: \n\n' + '▫Дуэли: ' + duel_msg + ' \n' + turn_duels  + '_\n\n▫️Расширенный лог боёв: ' + log_msg + '\n' + turn_log + '_\n\n▫️Автоматическая продажа обычных предметов: ' + autosell_msg + '\n' + turn_autosell +'_\n\n\n❕Для переключения нажмите на текст под одним из пунктов настроек❕')
		split_settings = msg.text.split('_')

		if split_settings[0] == '/log':
			if int(split_settings[1]) == 0:
				cursor.execute("UPDATE users_settings SET log_status = 0 WHERE tgid = ? ",(msg.from_user.id,))
				connect.commit()

				await msg.reply('Вы перешли на стандартный вариант логов!❎')
			else:
				cursor.execute("UPDATE users_settings SET log_status = 1 WHERE tgid = ? ",(msg.from_user.id,))
				connect.commit()

				await msg.reply('Вы перешли на расширенный вариант логов!✅')
		elif split_settings[0] == '/duel': 
			if int(split_settings[1]) == 0:
				cursor.execute("UPDATE users_settings SET duel_status = 0 WHERE tgid = ? ",(msg.from_user.id,))
				connect.commit()

				await msg.reply('Теперь вы принимаете вызовы на дуэль!✅')
			else:
				cursor.execute("UPDATE users_settings SET duel_status = 1 WHERE tgid = ? ",(msg.from_user.id,))
				connect.commit()

				await msg.reply('Вы теперь не принимаете вызовы на дуэль!❎')
		elif split_settings[0] == '/autosell':
			if int(split_settings[1]) == 0:
				cursor.execute("UPDATE users_settings SET autosell_status = 0 WHERE tgid = ? ",(msg.from_user.id,))
				connect.commit()
				await msg.reply('Вы выключили автопродажу предметов обычной редкости!❎')
			else:
				cursor.execute("UPDATE users_settings SET autosell_status = 1 WHERE tgid = ? ",(msg.from_user.id,))
				connect.commit()
				await msg.reply('Вы включили автопродажу предметов обычной редкости!✅')

		elif msg.text.lower() == 'развод':
			cursor.execute("SELECT partner FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
			your_partner = cursor.fetchone()[0];

			if your_partner != 0:

				await msg.reply('Вы успешно развелись!💔')
				await bot.send_message(your_partner,'Ваш партнёр разорвал брак!💔')

				cursor.execute("UPDATE rpg_users_personage SET partner = 0 WHERE tgid = ? ",(your_partner,))
				connect.commit()

				cursor.execute("UPDATE rpg_users_personage SET partner = 0 WHERE tgid = ? ",(msg.from_user.id,))
				connect.commit()
			else:
				await msg.reply('Да ладно, вы и так не состояли в браке🤪...')	
		elif msg.text.lower() == '/referals' or msg.text.lower() == 'рефералы' or msg.text == '/referals' + bot_name:
			cursor.execute("SELECT referals FROM referals WHERE tgid = ? ",(msg.from_user.id,))
			amount_referals = str(cursor.fetchone()[0]);

			cursor.execute("SELECT referals_gold FROM statistic WHERE tgid = ? ",(msg.from_user.id,))
			geted_ref_gold = str(cursor.fetchone()[0]);

			cursor.execute("SELECT userid FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
			my_id = cursor.fetchone()[0];

			await msg.reply('ℹ️Информация о вашей реферальной деятельности: \n\n🆔Ваш реферальный код: '+ str(my_id)+'\n👨‍👩‍👧‍👦Кол-во рефералов: '+amount_referals+'\n🤑Полученное с рефералов золото: ' + geted_ref_gold)

		elif msg.text == '/ref_card' or msg.text == '/ref_card' + bot_name or msg.text.lower() == 'карта' or msg.text.lower() == 'реферальная карта' or msg.text.lower() == 'моя карта': 
			cursor.execute("SELECT referals FROM referals WHERE tgid = ? ",(msg.from_user.id,))
			amount_referals = str(cursor.fetchone()[0]);

			cursor.execute("SELECT referals_gold FROM statistic WHERE tgid = ? ",(msg.from_user.id,))
			geted_ref_gold = str(cursor.fetchone()[0]);

			cursor.execute("SELECT userid FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
			my_id = str(cursor.fetchone()[0]);

			await msg.reply('💬Скопируйте или перешлите следующее сообщение человеку, которого хотите пригласить: ')
			await msg.reply('Привет👋! \n😊Зарегестрируйся в боте @DarkWorldRPG_bot\nПри регистрации укажи реферальный код ' + my_id + ' и получи 100 бонусных монет!🤑\nБыстрее заходи, сразимся в дуэли⚔️')
		elif msg.text.lower() == '/arena' or msg.text.lower() == 'арена':
			cursor.execute("SELECT energy FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
			energy = cursor.fetchone()[0];
			if energy > 60:
				amount_your = 0
				amount_enemy = 0
				enemy_healed = 0
				your_healed = 0
				upd_bash = 0
				cursor.execute("SELECT hp FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
				your_full_hp = int(cursor.fetchone()[0]);
				circle = 1
				while circle < 12:
					try:
						
						enemy_hp = random.randint(1,15) * circle
						enemy_name = 'Враг №' + str(circle)
						enemy_speed = int(circle / 1.5) + 2
						enemy_damage = random.randint(1,10) * circle
						enemy_xp = random.randint(1,10) * circle
						enemy_gold = random.randint(1,10) * circle
						enemy_bash = random.randint(1,70)
						enemy_heal = random.randint(1,70)
						enemy_miss = random.randint(1,79)
						enemy_critical = random.randint(1,71)
						enemy_vampirise = random.randint(1,70)

						
						your_hp = your_full_hp

						cursor.execute("SELECT damage FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
						your_damage = int(cursor.fetchone()[0]);

						cursor.execute("SELECT speed FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
						your_speed = int(cursor.fetchone()[0]);

						cursor.execute("SELECT bash FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
						your_bash = int(cursor.fetchone()[0]);

						cursor.execute("SELECT heal FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
						your_heal = int(cursor.fetchone()[0]);

						cursor.execute("SELECT miss FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
						your_miss = int(cursor.fetchone()[0]);

						cursor.execute("SELECT critical FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
						your_critical = int(cursor.fetchone()[0]);

						cursor.execute("SELECT vampirise FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
						your_vampirise = int(cursor.fetchone()[0]);


						enemy_bashed = False
						you_bashed = False



						
						i = 0
						while True:
							bash_chance = random.randint(1,100)
							heal_chance = random.randint(1,100)
							miss_chance = random.randint(1,100)
							critical_chance = random.randint(1,100)
							vampirise_chance = random.randint(1,100)
							if you_bashed == False:
								if enemy_miss < miss_chance:
									if bash_chance <= your_bash:
										enemy_bashed = True
									if critical_chance <= your_critical:
										enemy_hp = int(enemy_hp - ((your_damage * (int(your_speed / 1.7))) * 2))
										amount_your += 1
									else:
										enemy_hp = enemy_hp - (int(your_speed / 1.7) * your_damage)
										amount_your += 1
									if vampirise_chance <= your_vampirise:
										your_hp += int(your_damage * your_speed / 1.7)
										your_healed += int(your_damage * your_speed / 1.7)
									if heal_chance <= your_heal:
										your_hp += int(your_hp / 3)
										your_healed += int(your_hp / 3)

							else:
								you_bashed = False

							if enemy_bashed == False:
								if your_miss < miss_chance:
									if enemy_bash >= bash_chance:
										you_bashed = True
									if critical_chance <= enemy_critical:
										enemy_hp = int(your_hp - ((enemy_damage * int(enemy_speed / 1.7)) * 2))
										amount_enemy += 1
									else:
										your_hp = your_hp - int(enemy_speed / 1.7) * enemy_damage
										amount_enemy += 1
									if vampirise_chance <= enemy_vampirise:
										enemy_hp += enemy_damage * int(enemy_speed / 1.7)
										enemy_healed += enemy_damage *int(enemy_speed / 1.7)
									if heal_chance <= enemy_heal:
										enemy_hp += int(enemy_hp / 3)
										enemy_healed += int(enemy_hp / 3)

							else:
								enemy_bashed = False 

							if your_healed < 0:
								your_healed = your_healed * -1
							if enemy_healed < 0:
								enemy_healed = enemy_healed * -1
								
							if enemy_hp <= 0:
								await AddCoins(enemy_gold,False,True)
								await AddExp(enemy_xp,'user')
								await PlusStatistic('pve',0)
								circle += 1	
								break
							if your_hp <= 0:
								await AddExp(random.randint(0,5),'user')
								await PlusStatistic('pve',0)
								break

							i += 1
						if your_hp <= 0:
							break
					except Exception as ex:
						print(7)
						print(ex)
						await bot.send_message(msg.from_user.id,'Противник сбежал с поля боя')
						await bot.send_message(793368809,str(ex))

				precompl_str = '\n💀Убито врагов: ' + str(circle) +'/12 \n\n❕Было нанесено урона: ' + str(amount_your * (int(your_speed / 1.7) * your_damage)) + "\n❕Было нанесено ударов: " + str(amount_your) + "\n❕Было восстановлено здоровья: " + str(your_healed) + "\n\n❗️Было получено урона: " + str(amount_enemy * (int(enemy_speed / 1.7) * enemy_damage)) + '\n❗️Было получено ударов: ' + str(amount_enemy) + '\n❗️Противники восстановил здоровья: ' + str(enemy_healed)
				await msg.reply("ℹ️Информация о сражении: " + '\n' + precompl_str)
				await MinusEnergy(60)
			else:
				await msg.reply("У вас недостаточно энергии для этого действия!🛑")

		elif Splited_msg[0].lower() == 'перевод':
			if len(Splited_msg) == 3:
				cursor.execute("SELECT coins FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
				first_balance = int(cursor.fetchone()[0]);
				if first_balance >= int(Splited_msg[2]) and first_balance > 0:
					if int(Splited_msg[2]) > 0:
						try:
							cursor.execute("SELECT tgid FROM rpg_users WHERE userid = ? ",(int(Splited_msg[1]),))
							second_balance = int(cursor.fetchone()[0]);
							if second_balance != msg.from_user.id:
								cursor.execute("UPDATE rpg_users_personage SET coins = coins - ? WHERE tgid = ? ",(int(Splited_msg[2]),msg.from_user.id,))
								cursor.execute("UPDATE rpg_users_personage SET coins = coins + ? WHERE userid = ? ",(int(Splited_msg[2]),int(Splited_msg[1]),))
								connect.commit()
								cursor.execute("SELECT name FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
								your_name = cursor.fetchone()[0];

								cursor.execute("SELECT userid FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
								your_id = cursor.fetchone()[0];
								
								await bot.send_message(second_balance,"Вы получили перевод в размере " + Splited_msg[2] + ' монет💰' + '\n👤Отправитель: ' + str(your_name) + "\n🌐Telegram ID: " + str(msg.from_user.id) + '\n🔑ID в боте: ' + str(your_id))
								await msg.reply('Перевод успешно отправлен!💸')
							else:
								await msg.reply('Нельзя переводить деньги самому себе!🛑')
						except Exception as ex:
							print(8)
							await msg.reply('Извините, возникла ошибка при переводе, возможно ошибочный айди пользователя!🛑')
							cursor.execute("UPDATE rpg_users_personage SET coins = coins + ? WHERE tgid = ? ",(int(Splited_msg[2]),msg.from_user.id,))
							print(ex)


					else:
						await msg.reply('Не возможно отправить 0 или меньше монет!🛑')
				else:
					await msg.reply('Перевод не успешен!На вашем балансе недостаточно монет!🛑')
			else:
				await msg.reply('Ошибочное использование команды!🛑')

		
		elif Splited_msg[0].lower() == "репорт":
			if len(Splited_msg) >=	 2:
				report_msg = msg.text[7:]
				cursor.execute("""INSERT INTO reports(tgid, status, admin, question, answer)
				VALUES(?,0,0,?,'0');""",(msg.from_user.id,report_msg,))
				connect.commit()
				cursor.execute("SELECT userid FROM rpg_users WHERE tgid = ?",(msg.from_user.id,))
				userid = cursor.fetchone()[0];

				cursor.execute("SELECT id FROM reports WHERE tgid = ? AND status = 0 ",(msg.from_user.id,))
				report_id = cursor.fetchone()[0];
				await msg.reply('Ваше обращение будет рассмотрено администраторами, ожидайте ответ!⏳')
				i = 0
				while i < len(report_admin):
					await bot.send_message(report_admin[i],'📣Поступил новый репорт: ' + '\n>' + report_msg + '\n\n🔑ID обращения: ' + str(report_id) + '\n🔑ID пользователя: ' + str(userid))
					cursor.execute("UPDATE reports SET status = 1 WHERE id = ? ",(report_id,))
					connect.commit()
					i += 1
			else:
				await msg.reply('Нельзя отправлять пустой репорт!🛑')

		elif msg.text.lower() == 'донат' or msg.text.lower() == '/donate' or msg.text.lower() == '/donate' + bot_name:
			
			await msg.reply('Ссылка на донат: https://www.donationalerts.com/r/darkworldbot \n\n♥️1 рубль = 20 игровых монет!♥️\n♥️ОБЯЗАТЕЛЬНО УКАЖИТЕ ВАШ АЙДИ ПРИ ДОНАТЕ♥️')

		elif msg.text.lower() == '/chests' or msg.text.lower() == '/chests' + bot_name or msg.text.lower() == 'сундуки' or msg.text.lower() == 'сундук':
			await bot.send_message(msg.from_user.id,'Какой сундук желаете открыть?\nСтоимость каждого сундука - 140 монет💰',reply_markup = kb.chest_kb)
			cursor.execute("UPDATE rpg_users SET position = 30 WHERE tgid = ? ",(msg.from_user.id,))
			connect.commit()

		elif user_position == 30:
			cursor.execute("SELECT coins FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
			balance = cursor.fetchone()[0];

			if balance >= 140:
				folder_length = 0 
				item_type = ''
				if msg.text == 'Сундук с питомцами🧸':
					#await PlusStatistic('chests',0)
					cursor.execute("SELECT pet_fold FROM users_fold WHERE tgid = ? ",(msg.from_user.id,))
					folder = cursor.fetchone()[0];
					splited_folder = folder.split(' ')
					folder_length = len(splited_folder)
					item_type = 'pet'
				elif msg.text == 'Сундук с бронёй👕':
					cursor.execute("SELECT armour_fold FROM users_fold WHERE tgid = ? ",(msg.from_user.id,))
					folder = cursor.fetchone()[0];
					splited_folder = folder.split(' ')
					folder_length = len(splited_folder)
					item_type = 'armour'
				elif msg.text == 'Сундук с оружием🔪':
					cursor.execute("SELECT weapon_fold FROM users_fold WHERE tgid = ? ",(msg.from_user.id,))
					folder = cursor.fetchone()[0];
					splited_folder = folder.split(' ')
					folder_length = len(splited_folder)
					item_type = 'weapon'
				elif msg.text == 'Сундук с артефактами🔮': 
					cursor.execute("SELECT artifact_fold FROM users_fold WHERE tgid = ? ",(msg.from_user.id,))
					folder = cursor.fetchone()[0];
					splited_folder = folder.split(' ')
					folder_length = len(splited_folder)
					item_type = 'artifact'
				else:
					item_type = '0'
					cursor.execute("UPDATE rpg_users SET position = 0 WHERE tgid = ? ",(msg.from_user.id,))
					connect.commit()
					await bot.send_message(msg.from_user.id,'Вы покинули магазин✅',reply_markup = kb.ReplyKeyboardRemove())
				if item_type != '0':
					if folder_length < 16: 
						need_rare = 0
						droped_rare = random.randint(0,10000)
						if droped_rare >= 0 and droped_rare <= 4500:#45%
							need_rare = 0
						elif droped_rare > 4500 and droped_rare <= 7500: #30%
							need_rare = 1
						elif droped_rare > 7500 and droped_rare <= 9000: #15%
							need_rare = 2
						elif droped_rare > 9000 and droped_rare <= 9700: #7%
							need_rare = 3
						elif droped_rare > 9700 and droped_rare <= 9900: #2%
							need_rare = 4
						elif droped_rare > 9900 and droped_rare <= 9990: #0.9%
							need_rare = 5
						elif droped_rare > 9900 and droped_rare <= 9997: #0.07%
							need_rare = 6
						elif droped_rare > 9997 and droped_rare <= 10000: #0.03%
							need_rare = 7

						str_drop = ''
						item_rare = 0
						item_num = random.randint(1,30)
						if item_type == 'artifact':
							item_num = random.randint(1,len(equip.artifacts_arr) - 1) 
							while True:
								now_rare = equip.artifacts_arr[item_num].GetArtifact('rare')
								if now_rare != need_rare:
									item_num = random.randint(1,len(equip.artifacts_arr) - 1) 
								else:
									break

							item_name = equip.artifacts_arr[int(item_num)].GetArtifact('name')
							item_rare = equip.artifacts_arr[int(item_num)].GetArtifact('rare')
							str_drop = '🥳Вам выпал новый артефакт: ' + str(item_name) + '\n🌈Редкость: ' + str(await GetRare(item_rare)) 
						elif item_type == 'weapon':
							item_num = random.randint(1,len(equip.sword_arr) - 1) 
							while True:
								now_rare = equip.sword_arr[item_num].GetSword('rare')
								if now_rare != need_rare:
									item_num = random.randint(1,len(equip.sword_arr) - 1) 
								else:
									break
							item_name = equip.sword_arr[int(item_num)].GetSword('name')
							item_rare = equip.sword_arr[int(item_num)].GetSword('rare')
							str_drop = '🥳Вам выпало новое оружие: ' + str(item_name) + '\n🌈Редкость: ' + str(await GetRare(item_rare)) 
						elif item_type == 'armour':
							item_num = random.randint(1,len(equip.armour_arr) - 1) 
							while True:
								now_rare = equip.armour_arr[item_num].GetArmour('rare')
								if now_rare != need_rare:
									item_num = random.randint(1,len(equip.armour_arr) - 1) 
								else:
									break
							item_name = equip.armour_arr[int(item_num)].GetArmour('name')
							item_rare = equip.armour_arr[int(item_num)].GetArmour('rare')
							str_drop = '🥳Вам выпал новый комплект брони: ' + str(item_name) + '\n🌈Редкость: ' + str(await GetRare(item_rare)) 	
						elif item_type == 'pet':
							now_rare = equip.pets_arr[item_num].GetPet('rare')
							while True:
								now_rare = equip.pets_arr[item_num].GetPet('rare')
								if now_rare != need_rare:
									item_num = random.randint(1,len(equip.pets_arr) - 1) 
								else:
									break 
							item_name = equip.pets_arr[int(item_num)].GetPet('name')
							item_rare = equip.pets_arr[int(item_num)].GetPet('rare')
							str_drop = '🥳Вам выпал новый питомец: ' + str(item_name) + '\n🌈Редкость: ' + str(await GetRare(item_rare)) 
						cursor.execute("SELECT autosell_status FROM users_settings WHERE tgid = ? ",(msg.from_user.id,))
						autosell_status = int(cursor.fetchone()[0]);
						if autosell_status == 1 and item_rare == 0:
							await bot.send_message(msg.from_user.id,str_drop + '\n\nЭтот предмет был автоматически продан(вы получили 50 монет)! Желаете открыть ещё один сундук?',reply_markup = kb.YN_kb)
							await AddCoins(50,False,False)
						else:
							await bot.send_message(msg.from_user.id,str_drop + '\n\nЭтот предмет добавлен в ваше хранилище! Желаете открыть ещё один сундук?',reply_markup = kb.YN_kb)
							await AddItem(str(item_num),item_type,0)
						cursor.execute("UPDATE rpg_users SET position = 31 WHERE tgid = ? ",(msg.from_user.id,))
						connect.commit()
						cursor.execute("UPDATE rpg_users_personage SET coins = coins - 140 WHERE tgid = ? ",(msg.from_user.id,))
						connect.commit()

						cursor.execute("SELECT inviter FROM referals WHERE tgid = ? ",(msg.from_user.id,))
						inviter = int(cursor.fetchone()[0]);

						cursor.execute("UPDATE rpg_users_personage SET coins = coins + 20 WHERE userid = ? ",(inviter,))
						connect.commit()

						cursor.execute("UPDATE statistic SET referals_gold = referals_gold + 20 WHERE userid = ? ",(inviter,))
						connect.commit()
						cursor.execute("UPDATE statistic SET chests = chests + 1 WHERE tgid = ? ",(msg.from_user.id,))
						connect.commit()
						

					else:
						await msg.reply('Извините, в вашем хранилище недостаточно места, чтобы открыть сундук. Продайте некоторые предметы и попробуйте ещё раз!',reply_markup = kb.ReplyKeyboardRemove())
						cursor.execute("UPDATE rpg_users SET position = 0 WHERE tgid = ? ",(msg.from_user.id,))
						connect.commit()
				else:
					cursor.execute("UPDATE rpg_users SET position = 0 WHERE tgid = ? ",(msg.from_user.id,))
					connect.commit()

			else:
				await msg.reply('На вашем балансе недостаточно монет!🛑',reply_markup = kb.ReplyKeyboardRemove())
				cursor.execute("UPDATE rpg_users SET position = 0 WHERE tgid = ? ",(msg.from_user.id,))
				connect.commit()



		elif user_position == 31:
			if msg.text == 'Да✅':
				cursor.execute("UPDATE rpg_users SET position = 30 WHERE tgid = ? ",(msg.from_user.id,))
				connect.commit()
				await msg.reply('Хорошо, какой сундук откроем?',reply_markup = kb.chest_kb)
			else:
				await msg.reply('Хорошо, вы покинули магазин сундуков!',reply_markup = ReplyKeyboardRemove())
				cursor.execute("UPDATE rpg_users SET position = 0 WHERE tgid = ? ",(msg.from_user.id,))
				connect.commit()

		elif msg.text.lower() == '/shop' or msg.text.lower() == 'магазин' or msg.text.lower() == '/shop' + bot_name:
			await bot.send_message(msg.from_user.id,'🛒Выберите товар, который хотите приобрести.',reply_markup = kb.shop_kb)
			cursor.execute("UPDATE rpg_users SET position = 10 WHERE tgid = ? ",(msg.from_user.id,))
			connect.commit()

		elif user_position == 10:
			if msg.text == 'Энергия⚡️':
				await bot.send_message(msg.from_user.id,'Какое количество энергии желаете купить?\n 25 энергии⚡️ = 45 монет💰\n 50 энергии⚡️ = 90 монет💰\n 100 энергии⚡️ = 180 монет💰',reply_markup = kb.energy_kb)
				cursor.execute("UPDATE rpg_users SET position = 11 WHERE tgid = ? ",(msg.from_user.id,))
				connect.commit()
			else:
				cursor.execute("UPDATE rpg_users SET position = 0 WHERE tgid = ? ",(msg.from_user.id,))
				connect.commit()
				await bot.send_message(msg.from_user.id,'Вы покинули магазин✅',reply_markup = kb.ReplyKeyboardRemove())

		elif user_position == 11:
			if msg.text == '25 энергии⚡️':
				cursor.execute("SELECT coins FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
				balance = cursor.fetchone()[0];

				if balance >= 45:
					cursor.execute("UPDATE rpg_users_personage SET coins = coins - 45 WHERE tgid = ? ",(msg.from_user.id,))
					connect.commit()
					cursor.execute("UPDATE rpg_users_stats SET energy = energy + 25 WHERE tgid = ? ",(msg.from_user.id,))
					connect.commit()

					await bot.send_message(msg.from_user.id,'Вы успешно приобрели 25 единиц энергии⚡️',reply_markup = kb.ReplyKeyboardRemove())	
				else:
					await bot.send_message(msg.from_user.id,'Недостаточно золота для покупки!🛑',reply_markup = kb.ReplyKeyboardRemove())	
			elif msg.text == '50 энергии⚡️':
				cursor.execute("SELECT coins FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
				balance = cursor.fetchone()[0];

				if balance >= 90:
					cursor.execute("UPDATE rpg_users_personage SET coins = coins - 90 WHERE tgid = ? ",(msg.from_user.id,))
					connect.commit()
					cursor.execute("UPDATE rpg_users_stats SET energy = energy + 50 WHERE tgid = ? ",(msg.from_user.id,))
					connect.commit()

					await bot.send_message(msg.from_user.id,'Вы успешно приобрели 50 единиц энергии⚡️',reply_markup = kb.ReplyKeyboardRemove())	
				else:
					await bot.send_message(msg.from_user.id,'Недостаточно золота для покупки!🛑',reply_markup = kb.ReplyKeyboardRemove())	

			elif msg.text == '100 энергии⚡️':
				cursor.execute("SELECT coins FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
				balance = cursor.fetchone()[0];

				if balance >= 180:
					cursor.execute("UPDATE rpg_users_personage SET coins = coins - 180 WHERE tgid = ? ",(msg.from_user.id,))
					connect.commit()
					cursor.execute("UPDATE rpg_users_stats SET energy = energy + 100 WHERE tgid = ? ",(msg.from_user.id,))
					connect.commit()

					await bot.send_message(msg.from_user.id,'Вы успешно приобрели 100 единиц энергии⚡️',reply_markup = kb.ReplyKeyboardRemove())	
				else:
					await bot.send_message(msg.from_user.id,'Недостаточно золота для покупки!🛑',reply_markup = kb.ReplyKeyboardRemove())	
			else:
				cursor.execute("UPDATE rpg_users SET position = 0 WHERE tgid = ? ",(msg.from_user.id,))
				connect.commit()
				await bot.send_message(msg.from_user.id,'Вы покинули магазин✅',reply_markup = kb.ReplyKeyboardRemove())
	
		elif msg.text.lower() == '/energy' or msg.text.lower() == 'энергия' or msg.text.lower() == '/energy' + bot_name:
			cursor.execute("SELECT energy FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
			energy = cursor.fetchone()[0];
			cursor.execute("SELECT max_energy FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
			max_energy = cursor.fetchone()[0];
			await msg.reply('Ваш запас энергии: ' + str(energy) + '/' + str(max_energy) + "⚡️")

		elif msg.text.lower() == '/rules' or msg.text.lower() == 'правила' or msg.text.lower() == '/rules' + bot_name:
			await msg.reply('Наши правила - https://telegra.ph/Pravila-bota-05-17')

		elif msg.text.lower() == '/balance' or msg.text.lower() == 'баланс' or msg.text.lower() == '/balance' + bot_name:
			cursor.execute("SELECT coins FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
			balance = cursor.fetchone()[0];
			await msg.reply('У вас на балансе ' + str(balance) + ' монет💰')
		elif Splited_msg[0].lower() == '/statistic' or Splited_msg[0].lower() == 'статистика' or Splited_msg[0] == '/statistic@DarkWorldRPG_bot':
			cursor.execute("SELECT win_duels FROM statistic WHERE tgid = ? ",(msg.from_user.id,))
			player_win_duels = cursor.fetchone()[0];

			cursor.execute("SELECT amount_duels FROM statistic WHERE tgid = ? ",(msg.from_user.id,))
			player_amount_duels = cursor.fetchone()[0];

			cursor.execute("SELECT color FROM statistic WHERE tgid = ? ",(msg.from_user.id,))
			player_color = cursor.fetchone()[0];

			cursor.execute("SELECT pve FROM statistic WHERE tgid = ? ",(msg.from_user.id,))
			player_pve = cursor.fetchone()[0];

			cursor.execute("SELECT chests FROM statistic WHERE tgid = ? ",(msg.from_user.id,))
			player_chests = cursor.fetchone()[0];

			cursor.execute("SELECT rulet FROM statistic WHERE tgid = ? ",(msg.from_user.id,))
			player_rulet = cursor.fetchone()[0];

			cursor.execute("SELECT bonus FROM statistic WHERE tgid = ? ",(msg.from_user.id,))
			player_bonus = cursor.fetchone()[0];

			cursor.execute("SELECT bet FROM statistic WHERE tgid = ? ",(msg.from_user.id,))
			player_bet = cursor.fetchone()[0];

			await msg.reply('📈Ваша статистика: \n🔹Сыграно дуэлей: ' +str(player_amount_duels)+ ' \n🔹Выиграно дуэлей: ' +str(player_win_duels) + ' \n🔹Сражений с монстрами: ' + str(player_pve) + ' \n🔹Открыто сундуков: ' +str(player_chests) +' \n🔹Игр в цвета: ' +str(player_color)  +' \n🔹Ставок в казино: ' +str(player_bet)+' \n🔹Сыграно раз в рулетку: ' +str(player_rulet) +' \n🔹Получено бонусов: ' + str(player_bonus))

		elif msg.text.lower() == 'работа' or msg.text.lower() == '/work':
			if msg.chat.id != msg.from_user.id:
				await msg.reply('Эта команда доступна только в личных сообщениях, давайте поговорим там😉.')
			await bot.send_message(msg.from_user.id,"Выберите подработку, которая вам по душе: ",reply_markup = kb.work_kb_1)
			cursor.execute("UPDATE rpg_users SET position = 15 WHERE tgid = ? ",(msg.from_user.id,))
			connect.commit()

		elif user_position == 15:
			cursor.execute("SELECT energy FROM rpg_users_stats WHERE tgid = ? ",(msg.from_user.id,))
			energy = cursor.fetchone()[0];
			if energy > 0:
				if msg.text == 'Доставка грузов📦':
					await bot.send_message(msg.from_user.id,'Заказ найден, вы приступили к работе!',reply_markup = ReplyKeyboardRemove())
					num = random.randint(0,20)
					coins = 1
					message = 'default message'
					if num == 0:
						message = "Вы доставили груз для союзной гильдии!"
						coins = random.randint(4,6)
					elif num == 1:
						message = "Вы доставили лист в другую часть города!"
						coins = random.randint(2,4)
					elif num == 2:
						message = "Вы доставили семейную реликвию в другую страну!"
						coins = random.randint(8,10)
					elif num == 3:
						message = "Вы доставили секретную посылку в какую-то пещеру!"
						coins = random.randint(6,8)
					elif num == 4:
						message = "Вы успешно доставили огромный ящик в соседний город!"
						coins = random.randint(8,10)
					elif num == 5:
						message = "Вы успешно доставили посылку на фронт!"
						coins = random.randint(7,10)
					elif num == 6:
						message = "Посылка для главы гильдии была успешно доставлена!"
						coins = random.randint(5,16)
					elif num == 7:
						message = "Вы успешно доставили небольшую коробку в другую часть города!"
						coins = random.randint(3,13)
					elif num == 8:
						message = "Вы успешно доставили артефакт в исследовательский центр!"
						coins = random.randint(5,11)
					elif num == 9:
						message = "Вы успешно доставили меч для члена вашей гильдии!"
						coins = random.randint(3,10)
					elif num == 10:
						message = "Вы успешно доставили посылку в другую часть страны!"
						coins = random.randint(1,6)
					elif num == 11:
						message = "Вы доставили посылку в посольство союзной расы!"
						coins = random.randint(5,20)
					elif num == 12:
						message = "Вы доставили ресурсы союзному клану!"
						coins = random.randint(4,13)
					elif num == 13:
						message = "Вы доставили коробку с питомцем союзнику!"
						coins = random.randint(1,9)
					elif num == 14:
						message = "Вы принесли странный кристалл для местного волшебника!"
						coins = random.randint(1,14)
					elif num == 15:
						message = "Вы случайно разбили груз и скрылись с места преступления!"
						coins = 0
					elif num == 16:
						message = "Груз был утерян в ходе доставки!"
						coins = 0
					elif num == 17:
						message = "Из-за погодных условий вы сильно опоздали!"
						coins = random.randint(1,14)
					elif num == 18:
						message = "Вы не смогли доставить груз из-за погодных условий!"
						coins = 0
					elif num == 19:
						message = "Вас обокрали по пути к точке назначения, груз доставить не удалось!"
						coins = 0
					elif num == 20:
						message = "Получатель отказался платить из-за вашего опоздания!"
						coins = 0
					await bot.send_message(msg.from_user.id,message,reply_markup = kb.work_kb_2)
					await AddCoins(int(coins / 1.2 ) ,True,True)
					await AddExp(coins,'user')
					await MinusEnergy(random.randint(3,5))
				
				elif msg.text == 'Рыбалка🐠':
					await bot.send_message(msg.from_user.id,'Вы начали рыбачить!',reply_markup = ReplyKeyboardRemove())
					num = random.randint(0,46)
					coins = 1
					message = 'default message'
					if num == 0:
						message = "Вы поймали рыбу-меч, после чего продали ее на рынке. "
						coins = 5
					elif num == 1:
						message = "Вы поймали особо крупную рыбу-меч и продали её коллекционеру. "
						coins = 10
					elif num == 2:
						message = "Вы поймали акулу и продали её на рынке. "
						coins = 7
					elif num == 3:
						message = "Вы поймали детёныша кракена, учёные заплатят приличную сумму."
						coins = 25
					elif num == 4:
						message = "Вы поймали камбалу и продали её на рынке."
						coins = 3
					elif num == 5:
						message = "Вы поймали морского окуня и продали его на рынке. "
						coins = 4
					elif num == 6:
						message = "Вы поймали окуня и продали его на рынке"
						coins = 2
					elif num == 7:
						message = "Вы поймали морского ската и продали его на рынке. "
						coins = 5
					elif num == 8:
						message = "Вы поймали электрического угря, после чего продали его на рынке"
						coins = 7
					elif num == 9:
						message = "Вы поймали неизвестную странную рыбу и отдали её учёным. "
						coins = 20
					elif num == 10:
						message = "Вы поймали сома, после чего продали его на рынке. "
						coins =  4
					elif num == 11:
						message = "Вы поймали рыбу-собаку и продали его на рынке. "
						coins = 3
					elif num == 12:
						message = "Вы поймали саблезубую рыбу и продали её на рынке."
						coins = 5
					elif num == 13:
						message = "Вы поймали сумеречную рыбу и продали её на рынке."
						coins = 9
					elif num == 14:
						message = "Вы поймали детёныша кита и продали его на рынке."
						coins = 15
					elif num == 15:
						message = "Вы поймали удильщика и продали его на рынке."
						coins = 9
					elif num == 16:
						message = "Вам не удалось поймать рыбу."
						coins = 0
					elif num == 17:
						message = "Вы выловили мешок с золотом."
						coins = 30
					elif num == 18:
						message = "Ваша удочка сломалась во время ловли."
						coins = 0
					elif num == 19:
						message = "Леска не выдержала и порвалась. Рыбу поймать не удалось."
						coins = 0
					elif num == 20:
						message = "Вам удалось поймать редкую золотую рыбу."
						coins = 30
					elif num == 21:
						message = "Вы смогли поймать морскую черепаху!"
						coins = 10
					elif num == 21:
						message = "Вы поймали омара и продали его на рынке!"
						coins = 10
					elif num == 23:
						message = "Вы поймали рыбу-иглу!"
						coins = 7
					elif num == 24:
						message = "Вы поймали осьминога и продали его на рынке!"
						coins = 10
					elif num == 25:
						message = "Вы поймали несколько королевских креветок и продали их на рынке!"
						coins = 8
					elif num == 26:
						message = "Вы поймали рыбу-каплю, коллекционеры хорошо за неё заплатят!"
						coins = 15
					elif num == 27:
						message = "Вы поймали старый сапог..."
						coins = 0
					elif num == 28:
						message = "Вы поймали медузу и продали её на рынке!"
						coins = 6
					elif num == 29:
						message = "Вы поймали светящуюся медузу и продали её на рынке!"
						coins = 9
					elif num == 30:
						message = "Вам улыбнулась удача и вы поймали крайне редкую медузу!"
						coins = 15
					elif num == 31:
						message = "Вы поймали кальмара!"
						coins = 7
					elif num >= 32:
						message = "Не удалось ничего поймать..."
						coins = 0

					await bot.send_message(msg.from_user.id,message,reply_markup = kb.work_kb_4)
					await AddCoins(int(coins / 1.2 ) ,True,True)
					await AddExp(coins,'user')
					await MinusEnergy(random.randint(3,5))

				elif msg.text == 'Закончить🔴':
					cursor.execute("UPDATE rpg_users SET position = 0 WHERE tgid = ? ",(msg.from_user.id,))
					connect.commit()
					await bot.send_message(msg.from_user.id, "Хорошо, время отдохнуть!",reply_markup = ReplyKeyboardRemove())

				elif msg.text == 'Работа в шахте⛏':
					await bot.send_message(msg.from_user.id,'Вы приступили к работе!',reply_markup = ReplyKeyboardRemove())
					num = random.randint(0,20)
					coins = 1
					message = 'default message'

					if num == 0:
						message = "Вам удалось добыть железную руду!"
						coins = 5
					elif num == 1:
						message = "Вам удалось добыть медь!"
						coins = 4
					elif num == 2:
						message = "Вам удалось добыть серебро!"
						coins = 10
					elif num == 3:
						message = "Вам удалось добыть золото!"
						coins = 13
					elif num == 4:
						message = "Вам удалось добыть алмазы!"
						coins = 15
					elif num == 5:
						message = "Вам удалось добыть уголь!"
						coins = 3
					elif num == 6:
						message = "Вы смогли добыть титан!"
						coins = 17
					elif num == 7:
						message = "Вы успешно добыли уран!"
						coins = 20
					elif num == 8:
						message = "Вы смогли добыть сапфир!"
						coins = 15
					elif num == 9:
						message = "Вам удалось добыть изумруд!"
						coins = 15
					elif num == 10:
						message = "Вы добыли сумеречную руду!"
						coins = 15
					elif num == 11:
						message = "Вы раскопали огромную неизвестную кость, которой заинтересовались ученые!"
						coins = 20
					elif num == 12:
						message = "Вы смогли добыть платину!"
						coins = 8
					elif num == 13:
						message = "Вы не смогли найти ничего ценного!"
						coins = 0
					elif num == 14:
						message = "Ваша кирка сломалась и вы не смогли добыть руду!"
						coins = 0
					elif num == 15:
						message = "Вы получили ранение в шахте, поэтому не смогли продолжить работу"
						coins = 0
					elif num == 16:
						message = "Вы прокопали большой тунель, но так и не смогли ничего найти!"
						coins = 0
					elif num >= 17:
						message = "Вам не удалось ничего найти!"
						coins = 0
					await bot.send_message(msg.from_user.id,message,reply_markup = kb.work_kb_5)
					await AddCoins(int(coins / 1.2 ) ,True,True)
					await AddExp(coins,'user')
					await MinusEnergy(random.randint(3,5))

				elif msg.text == 'Охота🏹':
					await bot.send_message(msg.from_user.id,'Лук и меч готов, приступаем к охоте!',reply_markup = ReplyKeyboardRemove())
					num = random.randint(0,40)
					coins = 1
					message = 'default message'
					if num == 0:
						message = "Вам удалось поймать фазана."
						coins = 4
					elif num == 1:
						message = "Вам удалось поймать тигра."
						coins = 9
					elif num == 2:
						message = "Вам удалось поймать лису."
						coins = 4
					elif num == 3:
						message = "Вам удалось поймать оленя."
						coins = 4
					elif num == 4:
						message = "Вам удалось поймать волка и отдать его в цирк!"
						coins = 10
					elif num == 5:
						message = "Вам удалось поймать кролика."
						coins = 3
					elif num == 6:
						message = "Вы смогли поймать орла."
						coins = 3
					elif num == 7:
						message = "Вы смогли поймать дикого козла!"
						coins = 4
					elif num == 8:
						message = "Вы смогли поймать дикую лошадь!"
						coins = 5
					elif num == 9:
						message = "Вы смогли поймать медведя!"
						coins = 6
					elif num == 10:
						message = "Отличная работа! Вам удалось поймать слона!"
						coins = 20
					elif num == 11:
						message = "Восхитительно!Вы поймали жирафа!"
						coins = 20
					elif num == 12:
						message = "Вы поймали крокодила!"
						coins = 15
					elif num == 13:
						message = "Вы поймали рысь!"
						coins = 12
					elif num == 14:
						message = "Вы поймали льва!"
						coins = 15
					elif num == 15:
						message = "Вы поймали пантеру!"
						coins = 15
					elif num == 16:
						message = "Вы поймали гиену!"
						coins = 11
					elif num == 17:
						message = "Вы смогли поймать фламинго!"
						coins = 4
					elif num == 18:
						message = "Вы поймали белочку🤗"
						coins = 20
					elif num == 19:
						message = "Вы поймали зебру!"
						coins = 7
					elif num == 20:
						message = "Вы смогли поймать енота!"
						coins =3
					elif num == 21:
						message = "Вы бродили в айти-джунглях и смогли поймать питона!"
						coins = 20
					elif num >= 22:
						message = "Вы упустили свою добычу😾"
						coins = 0


					await bot.send_message(msg.from_user.id,message,reply_markup = kb.work_kb_3)
					await AddCoins(int(coins / 1.2 ) ,True,True)
					await AddExp(coins,'user')
					await MinusEnergy(random.randint(3,5))
			else:
				await msg.reply('У вас недостаточно энергии для этого действия!🛑',reply_markup = ReplyKeyboardRemove())
				cursor.execute("UPDATE rpg_users SET position = 0 WHERE tgid = ? ",(msg.from_user.id,))
				connect.commit()
		elif msg.text == '/artifacts' or msg.text == '/artifacts' + bot_name or msg.text.lower() == 'артефакты' or msg.text == 'Артефакты🔮':
			cursor.execute("SELECT artifact_fold FROM users_fold WHERE tgid = ? ",(msg.from_user.id,))
			item_list = cursor.fetchone()[0];
			send_list = ''
			item_arr = item_list.split(' ')

			if item_arr[0] == '':
				await msg.reply('Извините, у вас нет таких предметов на складе!❌')
			else:

				send_list += '📦Ваши артефакты: '
				i = 0
				while i < len(item_arr) - 1:
					item_name = equip.artifacts_arr[int(item_arr[i])].GetArtifact('name')
					item_rare = equip.artifacts_arr[int(item_arr[i])].GetArtifact('rare')

					rare_text = await GetRare(item_rare)

					send_list += '\n' + str(i + 1) + ') ' + item_name + ' - ' + rare_text

					i+= 1

				send_list += '\n\n\nДля продажи предмета используйте: \n▪️артефакт продать <номер предмета>\nЧтобы надеть предмет используйте: \n▪️артефакт надеть <номер предмета>\nДля передачи предмета используйте: \n▪️артефакт передать <айди игрока> <номер предмета> '


				await msg.reply(send_list)

		elif msg.text == '/weapon' or msg.text == '/weapon' + bot_name or msg.text.lower() == 'оружие' or msg.text == 'Оружие🔫':
			cursor.execute("SELECT weapon_fold FROM users_fold WHERE tgid = ? ",(msg.from_user.id,))
			item_list = cursor.fetchone()[0];
			send_list = ''
			item_arr = item_list.split(' ')

			if item_arr[0] == '':
				await msg.reply('Извините, у вас нет таких предметов на складе!❌')
			else:

				send_list += '📦Ваше оружие: '
				i = 0
				while i < len(item_arr) - 1:
					item_name = equip.sword_arr[int(item_arr[i])].GetSword('name')
					item_rare = equip.sword_arr[int(item_arr[i])].GetSword('rare')

					rare_text = await GetRare(item_rare)

					send_list += '\n' + str(i + 1) + ') ' + item_name + ' - ' + rare_text

					i+= 1

				send_list += '\n\n\nДля продажи предмета используйте: \n▪️оружие продать <номер предмета>\nЧтобы надеть предмет используйте: \n▪️оружие надеть <номер предмета>\nДля передачи предмета используйте: \n▪️оружие передать <айди игрока> <номер предмета> '

				await msg.reply(send_list)

		elif msg.text == '/armour' or msg.text == '/armour' + bot_name or msg.text.lower() == 'броня' or msg.text == 'Броня👕':
			cursor.execute("SELECT armour_fold FROM users_fold WHERE tgid = ? ",(msg.from_user.id,))
			item_list = cursor.fetchone()[0];
			send_list = ''
			item_arr = item_list.split(' ')
			print(item_arr)
			if item_arr[0] == '':
				await msg.reply('Извините, у вас нет таких предметов на складе!❌')
			else:

				send_list += '📦Ваши комплекты брони: '
				i = 0
				while i < len(item_arr) - 1:
					item_name = equip.armour_arr[int(item_arr[i])].GetArmour('name')
					item_rare = equip.armour_arr[int(item_arr[i])].GetArmour('rare')

					rare_text = await GetRare(item_rare)

					send_list += '\n' + str(i + 1) + ') ' + item_name + ' - ' + rare_text

					i+= 1

				send_list += '\n\n\nДля продажи предмета используйте: \n▪️броня продать <номер предмета>\nЧтобы надеть предмет используйте: \n▪️броня надеть <номер предмета>\nДля передачи предмета используйте: \n▪️броня передать <айди игрока> <номер предмета> '


				await msg.reply(send_list)

		elif msg.text == '/pets' or msg.text == '/pets' + bot_name or msg.text.lower() == 'питомцы' or msg.text == 'Питомцы🧸':
			cursor.execute("SELECT pet_fold FROM users_fold WHERE tgid = ? ",(msg.from_user.id,))
			item_list = cursor.fetchone()[0];
			send_list = ''
			item_arr = item_list.split(' ')

			if item_arr[0] == '':
				await msg.reply('Извините, у вас нет таких предметов на складе!❌')
			else:

				send_list += '📦Ваши питомцы: '
				i = 0
				while i < len(item_arr) - 1:
					item_name = equip.pets_arr[int(item_arr[i])].GetPet('name')
					item_rare = equip.pets_arr[int(item_arr[i])].GetPet('rare')

					rare_text = await GetRare(item_rare)

					send_list += '\n' + str(i + 1) + ') ' + item_name + ' - ' + rare_text

					i+= 1

				send_list += '\n\n\nДля продажи предмета используйте: \n▪️питомец продать <номер предмета>\nЧтобы надеть предмет используйте: \n▪️питомец надеть <номер предмета>\nДля передачи предмета используйте: \n▪️питомец передать <айди игрока><номер предмета> '


				await msg.reply(send_list)

		elif msg.text == '/tegs' or msg.text == '/tegs' + bot_name or msg.text.lower() == 'теги' or msg.text.lower() == 'титулы':
			cursor.execute("SELECT teg_fold FROM users_fold WHERE tgid = ? ",(msg.from_user.id,))
			item_list = cursor.fetchone()[0];
			send_list = ''
			item_arr = item_list.split(',')
			if item_arr[0] == '':
				await msg.reply('Извините, у вас нет таких предметов на складе!❌')
			else:

				send_list += '📦Ваши титулы: '
				i = 0
				while i < len(item_arr):
					item_name = item_arr[0]

					send_list += '\n' + str(i + 1) + ') ' + item_name

					i+= 1

				send_list += '\n\n\nДля продажи предмета используйте: \n▪️тег продать <номер предмета>\nЧтобы надеть предмет используйте: \n▪️тег надеть <номер предмета>\nДля передачи предмета используйте: \n▪️тег <номер предмета> <айди игрока>'


				await msg.reply(send_list)


		elif Splited_msg[0].lower() == 'тег':
			if Splited_msg[1].lower == 'надеть':
				cursor.execute("SELECT teg_fold FROM users_fold WHERE tgid = ? ",(msg.from_user.id,))
				item_list = cursor.fetchone()[0];
				send_list = ''
				item_arr = item_list.split(',')
				if int(Splited_msg[2]) <= len(item_arr) and int(Splited_msg[2]) > 0:

					cursor.execute("UPDATE rpg_users SET user_mark = ? WHERE userid = ? ",(item_arr[int(Splited_msg[2])],msg.from_user.id,))
					connect.commit()
					await msg.reply('Вы успешно изменили титул на ' + '"' + item_arr[int(Splited_msg[2])]) + '"✅'
				else:
					await msg.reply('Извините, у вас нет такого предмета!❌')


		elif Splited_msg[0].lower() == '/help' or Splited_msg[0].lower() == 'помощь' or msg.text.lower() == '/help' + bot_name:
			if len(Splited_msg) == 1:
				first = 'Список доступных команд:\n💠Профиль👤\n💠Дуэль⚔️\n💠Рулетка🎰\n💠Бонус🎁\n💠Цвета❇️\n💠Ставка💰\n💠Бой🗡\n💠Магазин🛒\n💠Склад🧳\n💠Артефакты🔮\n💠Питомцы🧸\n💠Оружие🔫\n💠Броня👕\n💠Брак💍\n💠Сундуки📦\n💠Снаряжение👕\n💠Статы📊\n💠Баланс💰'
				await msg.reply(first + '\n💠Энергия⚡️\n💠Репорт📣\n💠Ник✍️\n💠Перевод💸\n💠Редкости📒\n💠Статистика📈\n💠Карта🏷\n💠Рефералы👨‍👩‍👧‍👦\n💠Настройки⚙️\n💠Донат💎\n\n\nДетальная информация о некоторых командах: https://telegra.ph/Instrukciya-k-komandam-Dark-World-Bot-07-13')


		if Splited_msg[0].lower() == 'ник':
			amount_split = len(Splited_msg)
			i = 1
			new_nick = ''
			while i < amount_split:
				new_nick = new_nick + Splited_msg[i] + ' '
				i = i + 1
			if len(new_nick) <= 20 and len(new_nick) > 0:
				if msg.text.find('.') == -1:
					if msg.text.find('/') == -1:
						if msg.text.find('@') == -1:
							cursor.execute("UPDATE rpg_users_personage SET name = ? WHERE tgid = ?",(str(new_nick), int(msg.from_user.id),))
							connect.commit()

							await msg.reply("Вы успешно сменили ник на '" + new_nick + "'✅")
						else:
							await msg.reply('Извините, никнейм не должен содержать "@".🛑')
					else:
						await msg.reply('Извините, никнейм не должен содержать "/".🛑')
				else:
					await msg.reply('Извините, никнейм не должен содержать точку.🛑')
			else:
				await msg.reply('Недопосутимый никнейм, максимальная длина 20 символов!🛑')
		elif msg.text == '/storage' or msg.text == '/storage' + bot_name or msg.text.lower() == 'склад':
			cursor.execute("SELECT artifact_fold FROM users_fold WHERE tgid = ? ",(msg.from_user.id,)) #
			art_fold = cursor.fetchone()[0];
			art_fold_len = len(art_fold.split(' ')) - 1

			cursor.execute("SELECT weapon_fold FROM users_fold WHERE tgid = ? ",(msg.from_user.id,)) #
			weapon_fold = cursor.fetchone()[0];
			weapon_fold_len = len(weapon_fold.split(' ')) - 1

			cursor.execute("SELECT armour_fold FROM users_fold WHERE tgid = ? ",(msg.from_user.id,)) #
			armour_fold = cursor.fetchone()[0];
			armour_fold_len = len(armour_fold.split(' ')) - 1

			cursor.execute("SELECT pet_fold FROM users_fold WHERE tgid = ? ",(msg.from_user.id,)) #
			pet_fold = cursor.fetchone()[0];
			pet_fold_len = len(pet_fold.split(' ')) - 1




			await bot.send_message(msg.from_user.id,'📦Информация о ваших хранилищах:\n\n👕Броня: ' + str(armour_fold_len) +'/15\n🔫Оружие: ' + str(weapon_fold_len) +'/15\n🔮Артефакты: ' + str(art_fold_len) + '/15\n🧸Питомцы: '+ str(pet_fold_len) +'/15\n\nКакое именно хранилище вас интересует?🤔',reply_markup = kb.fold_kb)
		elif msg.text == 'Покинуть склад🚷':
			await msg.reply('Хорошо, вы покинули склад!✅',reply_markup = ReplyKeyboardRemove())

		elif Splited_msg[0].lower() == 'артефакт':
			if Splited_msg[1].lower() == 'надеть':
				cursor.execute("SELECT artifact_fold FROM users_fold WHERE tgid = ? ",(msg.from_user.id,))
				old_fold = cursor.fetchone()[0];
				new_fold = old_fold.split(' ')

				if len(new_fold) >= int(Splited_msg[2]) and int(Splited_msg[2]) > 0:
					need_item = new_fold[int(Splited_msg[2]) - 1]
					cursor.execute("SELECT artifact FROM rpg_users_inventory WHERE tgid = ? ",(msg.from_user.id,))
					item = cursor.fetchone()[0];

					if item != 0:
						await MinusITem('artifact',msg.from_user.id)
						await AddItem(item,'artifact',0)
					await PlusItem('artifact',msg.from_user.id,int(need_item))
					await RemoveItem(need_item,'artifact')
					await msg.reply('Вы успешно надели новый предмет!✅')

				else:
					await msg.reply('У вас нет такого предмета!🧐')


			elif Splited_msg[1].lower() == 'передать':
				cursor.execute("SELECT artifact_fold FROM users_fold WHERE tgid = ? ",(msg.from_user.id,)) #
				old_fold = cursor.fetchone()[0];
				new_fold = old_fold.split(' ')

				if len(new_fold) >= int(Splited_msg[3]) and int(Splited_msg[3]) > 0:
					try:
						cursor.execute("SELECT artifact_fold FROM users_fold WHERE userid = ? ",(int(Splited_msg[2]),)) #
						old_second_fold = cursor.fetchone()[0];
						new_second_fold = old_second_fold.split(' ')	
						if len(new_second_fold) < 15:
							if Splited_msg[2] != 0:
								cursor.execute("SELECT userid FROM users_fold WHERE tgid = ? ",(msg.from_user.id,))
								your_id = cursor.fetchone()[0];
								if int(Splited_msg[2]) != int(your_id):
									item = new_fold[int(Splited_msg[3]) - 1]
									cursor.execute("SELECT tgid FROM users_fold WHERE userid = ? ",(int(Splited_msg[2]),))
									second_tg = int(cursor.fetchone()[0]);

									cursor.execute("SELECT name FROM rpg_users_personage WHERE userid = ? ",(int(Splited_msg[2]),))
									second_name = str(cursor.fetchone()[0]);
									cursor.execute("SELECT name FROM rpg_users_personage WHERE userid = ? ",(int(your_id),))
									your_name = str(cursor.fetchone()[0]);

									await AddItem(int(item),'artifact',int(Splited_msg[2]))#
									await RemoveItem(int(item),'artifact')#

									await msg.reply('Отлично вы успешно передали предмет игроку ' + second_name + ' ✅')
									await bot.send_message(second_tg,your_name + ' передал вам новый артефакт!🎁')
								else:
									await msg.reply('Нельзя передавать предметы самому себе!❌')
							else:
								await msg.reply('Нельзя передать предмет игроку с id 0!❌')
						else:
							await msg.reply('У игрока, которому вы хотите передать предмет, нет для него места!❌')
					except Exception as ex:
						print(ex)
						await msg.reply('Произошла неизвестная ошибка, возможно неправильное использование команды!🙁')
				else:
					await msg.reply('Невозможно передать предмет, которого у вас нет!❌')

			elif Splited_msg[1].lower() == 'продать':
				if Splited_msg[2].lower() == 'все' or Splited_msg[2].lower() == 'всё':
					i = 0
					cursor.execute("SELECT artifact_fold FROM users_fold WHERE tgid = ? ",(msg.from_user.id,))
					old_fold = cursor.fetchone()[0];
					new_fold = old_fold.split(' ')
					sell_list = Splited_msg[2:]
					sell_gold = 0
					sell_item = 0
					stop = len(new_fold) - 1
					while i < stop:
						item = int(new_fold[i])
						item_rare = equip.artifacts_arr[item].GetArtifact('rare')
						await RemoveItem(item,'artifact')
						sell_gold += (item_rare + 1) * 50
						sell_item += 1
						i += 1

					await msg.reply('🎉Вы успешно продали ' + str(sell_item) + ' предмет(ов) и получили ' + str(sell_gold) + ' монет💰' )
					await AddCoins(sell_gold,False,False)

				else:
					if rpgstr.FindDuplicate(msg.text + ' ') == False:
						i = 0
						stop = len(Splited_msg) - 2
						cursor.execute("SELECT artifact_fold FROM users_fold WHERE tgid = ? ",(msg.from_user.id,))
						old_fold = cursor.fetchone()[0];
						new_fold = old_fold.split(' ')
						sell_list = Splited_msg[2:]
						sell_gold = 0
						sell_item = 0
						while i < stop:
							item = int(new_fold[int(sell_list[i]) - 1])
							item_rare = equip.artifacts_arr[item].GetArtifact('rare')
							await RemoveItem(item,'artifact')
							sell_gold += (item_rare + 1) * 50
							sell_item += 1
							i += 1

						await msg.reply('🎉Вы успешно продали ' + str(sell_item) + ' предмет(ов) и получили ' + str(sell_gold) + ' монет💰' )
						await AddCoins(sell_gold,False,False)
					else:
						await msg.reply('Вы пытаетесь продать один и тот же предмет несколько раз, я не могу этого сделать🙁')


		elif Splited_msg[0].lower() == 'броня':
			if Splited_msg[1].lower() == 'надеть':
				cursor.execute("SELECT armour_fold FROM users_fold WHERE tgid = ? ",(msg.from_user.id,))
				old_fold = cursor.fetchone()[0];
				new_fold = old_fold.split(' ')

				if len(new_fold) >= int(Splited_msg[2]) and int(Splited_msg[2]) > 0:
					need_item = new_fold[int(Splited_msg[2]) - 1]
					cursor.execute("SELECT armour FROM rpg_users_inventory WHERE tgid = ? ",(msg.from_user.id,))
					item = cursor.fetchone()[0];

					if item != 0:
						await MinusITem('armour',msg.from_user.id)
						await AddItem(item,'armour',0)
					await PlusItem('armour',msg.from_user.id,int(need_item))
					await RemoveItem(need_item,'armour')
					await msg.reply('Вы успешно надели новый предмет!✅')

				else:
					await msg.reply('У вас нет такого предмета!🧐')

			elif Splited_msg[1].lower() == 'передать':
				cursor.execute("SELECT armour_fold FROM users_fold WHERE tgid = ? ",(msg.from_user.id,)) #
				old_fold = cursor.fetchone()[0];
				new_fold = old_fold.split(' ')

				if len(new_fold) >= int(Splited_msg[3]) and int(Splited_msg[3]) > 0:
					try:
						cursor.execute("SELECT armour_fold FROM users_fold WHERE userid = ? ",(int(Splited_msg[2]),)) #
						old_second_fold = cursor.fetchone()[0];
						new_second_fold = old_second_fold.split(' ')	
						if len(new_second_fold) < 15:
							if Splited_msg[2] != 0:
								cursor.execute("SELECT userid FROM users_fold WHERE tgid = ? ",(msg.from_user.id,))
								your_id = cursor.fetchone()[0];
								if int(Splited_msg[2]) != int(your_id):
									item = new_fold[int(Splited_msg[3]) - 1]
									cursor.execute("SELECT tgid FROM users_fold WHERE userid = ? ",(int(Splited_msg[2]),))
									second_tg = int(cursor.fetchone()[0]);

									cursor.execute("SELECT name FROM rpg_users_personage WHERE userid = ? ",(int(Splited_msg[2]),))
									second_name = str(cursor.fetchone()[0]);
									cursor.execute("SELECT name FROM rpg_users_personage WHERE userid = ? ",(int(your_id),))
									your_name = str(cursor.fetchone()[0]);

									await AddItem(int(item),'armour',int(Splited_msg[2]))#
									await RemoveItem(int(item),'armour')#

									await msg.reply('Отлично вы успешно передали предмет игроку ' + second_name + ' ✅')
									await bot.send_message(second_tg,your_name + ' передал вам новый комплект брони!🎁')#
								else:
									await msg.reply('Нельзя передавать предметы самому себе!❌')
							else:
								await msg.reply('Нельзя передать предмет игроку с id 0!❌')
						else:
							await msg.reply('У игрока, которому вы хотите передать предмет, нет для него места!❌')
					except Exception as ex:
						print(ex)
						await msg.reply('Произошла неизвестная ошибка, возможно неправильное использование команды!🙁')
				else:
					await msg.reply('Невозможно передать предмет, которого у вас нет!❌')
			elif Splited_msg[1].lower() == 'продать':
				if Splited_msg[2].lower() == 'все' or Splited_msg[2].lower() == 'всё':
					i = 0
					cursor.execute("SELECT armour_fold FROM users_fold WHERE tgid = ? ",(msg.from_user.id,))
					old_fold = cursor.fetchone()[0];
					new_fold = old_fold.split(' ')
					sell_list = Splited_msg[2:]
					sell_gold = 0
					sell_item = 0
					stop = len(new_fold) - 1
					while i < stop:
						item = int(new_fold[i])
						item_rare = equip.armour_arr[item].GetArmour('rare')
						await RemoveItem(item,'armour')
						sell_gold += (item_rare + 1) * 50
						sell_item += 1
						i += 1

					await msg.reply('🎉Вы успешно продали ' + str(sell_item) + ' предмет(ов) и получили ' + str(sell_gold) + ' монет💰' )
					await AddCoins(sell_gold,False,False)
					
				else:
					if rpgstr.FindDuplicate(msg.text + ' ') == False:
						i = 0
						stop = len(Splited_msg) - 2
						cursor.execute("SELECT armour_fold FROM users_fold WHERE tgid = ? ",(msg.from_user.id,))
						old_fold = cursor.fetchone()[0];
						new_fold = old_fold.split(' ')
						sell_list = Splited_msg[2:]
						sell_gold = 0
						sell_item = 0
						while i < stop:
							item = int(new_fold[int(sell_list[i]) - 1])
							item_rare = equip.armour_arr[item].GetArmour('rare')
							await RemoveItem(item,'armour')
							sell_gold += (item_rare + 1) * 50
							sell_item += 1
							i += 1

						await msg.reply('🎉Вы успешно продали ' + str(sell_item) + ' предмет(ов) и получили ' + str(sell_gold) + ' монет💰' )
						await AddCoins(sell_gold,False,False)
					else:
						await msg.reply('Вы пытаетесь продать один и тот же предмет несколько раз, я не могу этого сделать🙁')


		elif Splited_msg[0].lower() == 'питомец':
			if Splited_msg[1].lower() == 'надеть':
				cursor.execute("SELECT pet_fold FROM users_fold WHERE tgid = ? ",(msg.from_user.id,))
				old_fold = cursor.fetchone()[0];
				new_fold = old_fold.split(' ')

				if len(new_fold) >= int(Splited_msg[2]) and int(Splited_msg[2]) > 0:
					need_item = new_fold[int(Splited_msg[2]) - 1]
					cursor.execute("SELECT pet FROM rpg_users_inventory WHERE tgid = ? ",(msg.from_user.id,))
					item = cursor.fetchone()[0];

					if item != 0:
						await MinusITem('pet',msg.from_user.id)
						await AddItem(item,'pet',0)
					await PlusItem('pet',msg.from_user.id,int(need_item))
					await RemoveItem(need_item,'pet')
					await msg.reply('Вы успешно надели новый предмет!✅')
				else:
					await msg.reply('У вас нет такого предмета!🧐')
			elif Splited_msg[1].lower() == 'передать':
				cursor.execute("SELECT pet_fold FROM users_fold WHERE tgid = ? ",(msg.from_user.id,)) #
				old_fold = cursor.fetchone()[0];
				new_fold = old_fold.split(' ')

				if len(new_fold) >= int(Splited_msg[3]) and int(Splited_msg[3]) > 0:
					try:
						cursor.execute("SELECT pet_fold FROM users_fold WHERE userid = ? ",(int(Splited_msg[2]),)) #
						old_second_fold = cursor.fetchone()[0];
						new_second_fold = old_second_fold.split(' ')	
						if len(new_second_fold) < 15:
							if Splited_msg[2] != 0:
								cursor.execute("SELECT userid FROM users_fold WHERE tgid = ? ",(msg.from_user.id,))
								your_id = cursor.fetchone()[0];
								if int(Splited_msg[2]) != int(your_id):
									item = new_fold[int(Splited_msg[3]) - 1]
									cursor.execute("SELECT tgid FROM users_fold WHERE userid = ? ",(int(Splited_msg[2]),))
									second_tg = int(cursor.fetchone()[0]);

									cursor.execute("SELECT name FROM rpg_users_personage WHERE userid = ? ",(int(Splited_msg[2]),))
									second_name = str(cursor.fetchone()[0]);
									cursor.execute("SELECT name FROM rpg_users_personage WHERE userid = ? ",(int(your_id),))
									your_name = str(cursor.fetchone()[0]);

									await AddItem(int(item),'pet',int(Splited_msg[2]))#
									await RemoveItem(int(item),'pet')#

									await msg.reply('Отлично вы успешно передали предмет игроку ' + second_name + ' ✅')
									await bot.send_message(second_tg,your_name + ' передал вам нового питомца!🎁')
								else:
									await msg.reply('Нельзя передавать предметы самому себе!❌')
							else:
								await msg.reply('Нельзя передать предмет игроку с id 0!❌')
						else:
							await msg.reply('У игрока, которому вы хотите передать предмет, нет для него места!❌')
					except Exception as ex:
						print(ex)
						await msg.reply('Произошла неизвестная ошибка, возможно неправильное использование команды!🙁')
				else:
					await msg.reply('Невозможно передать предмет, которого у вас нет!❌')
			elif Splited_msg[1].lower() == 'продать':
				if Splited_msg[2].lower() == 'все' or Splited_msg[2].lower() == 'всё':
					i = 0
					cursor.execute("SELECT pet_fold FROM users_fold WHERE tgid = ? ",(msg.from_user.id,))
					old_fold = cursor.fetchone()[0];
					new_fold = old_fold.split(' ')
					sell_list = Splited_msg[2:]
					sell_gold = 0
					sell_item = 0
					stop = len(new_fold) - 1
					while i < stop:
						item = int(new_fold[i])
						item_rare = equip.pets_arr[item].GetPet('rare') 
						await RemoveItem(item,'pet')
						sell_gold += (item_rare + 1) * 50
						sell_item += 1
						i += 1

					await msg.reply('🎉Вы успешно продали ' + str(sell_item) + ' предмет(ов) и получили ' + str(sell_gold) + ' монет💰' )
					await AddCoins(sell_gold,False,False)

					
				else:
					if rpgstr.FindDuplicate(msg.text + ' ') == False:
						i = 0
						stop = len(Splited_msg) - 2
						cursor.execute("SELECT pet_fold FROM users_fold WHERE tgid = ? ",(msg.from_user.id,))
						old_fold = cursor.fetchone()[0];
						new_fold = old_fold.split(' ')
						sell_list = Splited_msg[2:]
						sell_gold = 0
						sell_item = 0
						while i < stop:
							item = int(new_fold[int(sell_list[i]) - 1])
							item_rare = equip.pets_arr[item].GetPet('rare')
							await RemoveItem(item,'pet')
							sell_gold += (item_rare + 1) * 50
							sell_item += 1
							i += 1

						await msg.reply('🎉Вы успешно продали ' + str(sell_item) + ' предмет(ов) и получили ' + str(sell_gold) + ' монет💰' )
						await AddCoins(sell_gold,False,False)
					else:
						await msg.reply('Вы пытаетесь продать один и тот же предмет несколько раз, я не могу этого сделать🙁')

		elif Splited_msg[0].lower() == 'оружие': 
			if Splited_msg[1].lower() == 'надеть':
				cursor.execute("SELECT weapon_fold FROM users_fold WHERE tgid = ? ",(msg.from_user.id,))
				old_fold = cursor.fetchone()[0];
				new_fold = old_fold.split(' ')

				if len(new_fold) >= int(Splited_msg[2]) and int(Splited_msg[2]) > 0:
					need_item = new_fold[int(Splited_msg[2]) - 1]
					cursor.execute("SELECT weapon FROM rpg_users_inventory WHERE tgid = ? ",(msg.from_user.id,))
					item = cursor.fetchone()[0];

					if item != 0:
						await MinusITem('weapon',msg.from_user.id)
						await AddItem(item,'weapon',0)
					await PlusItem('weapon',msg.from_user.id,int(need_item))
					await RemoveItem(need_item,'weapon')
					await msg.reply('Вы успешно надели новый предмет!✅')

				else:
					await msg.reply('У вас нет такого предмета!🧐')
			elif Splited_msg[1].lower() == 'передать':
				cursor.execute("SELECT weapon_fold FROM users_fold WHERE tgid = ? ",(msg.from_user.id,)) #
				old_fold = cursor.fetchone()[0];
				new_fold = old_fold.split(' ')

				if len(new_fold) >= int(Splited_msg[3]) and int(Splited_msg[3]) > 0:
					try:
						cursor.execute("SELECT weapon_fold FROM users_fold WHERE userid = ? ",(int(Splited_msg[2]),)) #
						old_second_fold = cursor.fetchone()[0];
						new_second_fold = old_second_fold.split(' ')	
						if len(new_second_fold) < 15:
							if Splited_msg[2] != 0:
								cursor.execute("SELECT userid FROM users_fold WHERE tgid = ? ",(msg.from_user.id,))
								your_id = cursor.fetchone()[0];
								if int(Splited_msg[2]) != int(your_id):
									item = new_fold[int(Splited_msg[3]) - 1]
									cursor.execute("SELECT tgid FROM users_fold WHERE userid = ? ",(int(Splited_msg[2]),))
									second_tg = int(cursor.fetchone()[0]);

									cursor.execute("SELECT name FROM rpg_users_personage WHERE userid = ? ",(int(Splited_msg[2]),))
									second_name = str(cursor.fetchone()[0]);
									cursor.execute("SELECT name FROM rpg_users_personage WHERE userid = ? ",(int(your_id),))
									your_name = str(cursor.fetchone()[0]);

									await AddItem(int(item),'weapon',int(Splited_msg[2]))#
									await RemoveItem(int(item),'weapon')#

									await msg.reply('Отлично вы успешно передали предмет игроку ' + second_name + ' ✅')
									await bot.send_message(second_tg,your_name + ' передал вам новое оружие!🎁')
								else:
									await msg.reply('Нельзя передавать предметы самому себе!❌')
							else:
								await msg.reply('Нельзя передать предмет игроку с id 0!❌')
						else:
							await msg.reply('У игрока, которому вы хотите передать предмет, нет для него места!❌')
					except Exception as ex:
						print(ex)
						await msg.reply('Произошла неизвестная ошибка, возможно неправильное использование команды!🙁')
				else:
					await msg.reply('Невозможно передать предмет, которого у вас нет!❌')
			elif Splited_msg[1].lower() == 'продать':
				if Splited_msg[2].lower() == 'все' or Splited_msg[2].lower() == 'всё':
					i = 0
					cursor.execute("SELECT weapon_fold FROM users_fold WHERE tgid = ? ",(msg.from_user.id,))
					old_fold = cursor.fetchone()[0];
					new_fold = old_fold.split(' ')
					sell_list = Splited_msg[2:]
					sell_gold = 0
					sell_item = 0
					stop = len(new_fold) - 1
					while i < stop:
						item = int(new_fold[i])
						item_rare = equip.sword_arr[item].GetSword('rare') 
						await RemoveItem(item,'weapon')
						sell_gold += (item_rare + 1) * 50
						sell_item += 1
						i += 1

					await msg.reply('🎉Вы успешно продали ' + str(sell_item) + ' предмет(ов) и получили ' + str(sell_gold) + ' монет💰' )
					await AddCoins(sell_gold,False,False)			
				else:
					if rpgstr.FindDuplicate(msg.text + ' ') == False:
						i = 0
						stop = len(Splited_msg) - 2
						cursor.execute("SELECT weapon_fold FROM users_fold WHERE tgid = ? ",(msg.from_user.id,))
						old_fold = cursor.fetchone()[0];
						new_fold = old_fold.split(' ')
						sell_list = Splited_msg[2:]
						sell_gold = 0
						sell_item = 0
						while i < stop:
							item = int(new_fold[int(sell_list[i]) - 1])
							item_rare = equip.sword_arr[item].GetSword('rare')
							await RemoveItem(item,'weapon')
							sell_gold += (item_rare + 1) * 50
							sell_item += 1
							i += 1

						await msg.reply('🎉Вы успешно продали ' + str(sell_item) + ' предмет(ов) и получили ' + str(sell_gold) + ' монет💰' )
						await AddCoins(sell_gold,False,False)
					else:
						await msg.reply('Вы пытаетесь продать один и тот же предмет несколько раз, я не могу этого сделать🙁')

		#	await msg.reply(msg.text)
		elif Splited_msg[0].lower() == 'цвета' or Splited_msg[0].lower() == 'цвет' or Splited_msg[0].lower() == 'color':
			if Splited_msg[1].lower() == 'красный' or Splited_msg[1].lower() == 'зеленый' or Splited_msg[1].lower() == 'зелёный' or  Splited_msg[1].lower() == 'черный' or Splited_msg[1].lower() == 'чёрный' or Splited_msg[1].lower() == 'синий':
				if len(Splited_msg) == 3:
					cursor.execute("SELECT coins FROM rpg_users_personage WHERE tgid = ? ",(msg.from_user.id,))
					balance = int(cursor.fetchone()[0]);
					if balance >= int(Splited_msg[2]) and balance > 0:
						if int(Splited_msg[2]) > 0:

							cursor.execute("UPDATE rpg_users_personage SET coins = coins - ? WHERE tgid = ? ",(int(Splited_msg[2]),msg.from_user.id,))
							connect.commit()

							color_num = random.randint(0,99)
							color = ''
							await PlusStatistic('color',0)
							if color_num <= 45:
								color = "чёрный"
								if Splited_msg[1].lower() == "черный" or Splited_msg[1].lower() == 'чёрный':
									win = int(Splited_msg[2]) * 2
									await msg.reply('Выпал ⚫️.\nВаша ставка удвоена, выигрыш составил: ' + str(win) + " монет!🎉")
									cursor.execute("UPDATE rpg_users_personage SET coins = coins + ? WHERE tgid = ? ",(win,msg.from_user.id,))
									connect.commit()
								else:
									await msg.reply('Выпал ⚫️.Вы проиграли.☹️')

							elif color_num > 45 and color_num <= 90:
								color = "красный"
								if Splited_msg[1].lower() == "красный":
									win = int(Splited_msg[2]) * 2
									await msg.reply('Выпал 🔴.\nВаша ставка удвоена, выигрыш составил: ' + str(win) + " монет!🎉")
									cursor.execute("UPDATE rpg_users_personage SET coins = coins + ? WHERE tgid = ? ",(win,msg.from_user.id,))
									connect.commit()
								else:
									await msg.reply('Выпал 🔴.Вы проиграли.☹️')
							elif color_num > 97:
								color = 'зелёный'
								if Splited_msg[1].lower() == 'зеленый' or Splited_msg[1].lower() == 'зелёный':
									win = int(Splited_msg[2]) * 10
									await msg.reply('Выпал 🟢.\nВаша ставка умножена на 10.Выигрыш составил: ' + str(win) + " монет!💎")
									cursor.execute("UPDATE rpg_users_personage SET coins = coins + ? WHERE tgid = ? ",(win,msg.from_user.id,))
									connect.commit()
								else:
									await msg.reply('Выпал 🟢.Вы проиграли.☹️')

							elif color_num > 90 and color_num <= 97:
								color = 'синий'
								if Splited_msg[1].lower() == 'синий':
									win = int(Splited_msg[2]) * 5
									await msg.reply('Выпал 🔵.\nВаша ставка умножена на 5.Выигрыш составил: ' + str(win) + " монет!🎉")
									cursor.execute("UPDATE rpg_users_personage SET coins = coins + ? WHERE tgid = ? ",(win,msg.from_user.id,))
									connect.commit()
								else:
									await msg.reply('Выпал 🔵.Вы проиграли.☹️')
						else:
							await msg.reply('Не возможно поставить 0 или меньше монет!🛑')
					else:
						await msg.reply('На вашем балансе недостаточно монет!🛑')
				else:
					await msg.reply('Ошибочное использование команды!🛑')
			else:
				await msg.reply('Нельзя ставить на ' + Splited_msg[1].lower() + '!🛑')


		if user_status == 2:
			if msg.text.find('/') != -1:

				cursor.execute("SELECT userid FROM rpg_users WHERE tgid = ?",(msg.from_user.id,))
				admin_id = cursor.fetchone()[0];
				cursor.execute("SELECT name FROM rpg_users_personage WHERE tgid = ?",(msg.from_user.id,))
				admin_name = cursor.fetchone()[0];

				geted = datetime.datetime.now()
				time_geted = str(geted.strftime("%d-%m-%Y %H:%M"))

				await bot.send_message(793368809,'Администратор использовал команду: ' + Splited_msg[0] + '\n🔅Полное сообщение: ' + msg.text + '\n🔅Имя администратора: ' + admin_name + '\n🔅Айди администратора: ' + str(admin_id) + '\n🔅Дата: ' + time_geted + '\n\n#Админ_' + str(admin_id))

			if Splited_msg[0] == '/get' or Splited_msg[0].lower() == "получить" or Splited_msg[0].lower() == "гет" or Splited_msg[0].lower() == "get":
				get_userid = 0
				get_tgid = 0
				if len(Splited_msg) == 1:
					get_tgid = msg.reply_to_message.from_user.id
					cursor.execute("SELECT userid FROM rpg_users WHERE tgid = ?",(int(get_tgid),))
					get_userid = cursor.fetchone()[0];
				else:
					get_userid = Splited_msg[1]
					cursor.execute("SELECT tgid FROM rpg_users WHERE userid = ?",(int(get_userid),))
					get_tgid = cursor.fetchone()[0];

				cursor.execute("SELECT user_mark FROM rpg_users WHERE userid = ?",(int(get_userid),))
				get_mark = cursor.fetchone()[0];


				cursor.execute("SELECT name FROM rpg_users_personage WHERE userid = ?",(int(get_userid),))
				get_name = cursor.fetchone()[0];

				cursor.execute("SELECT coins FROM rpg_users_personage WHERE userid = ?",(int(get_userid),))
				get_coins = cursor.fetchone()[0];
				
				cursor.execute("SELECT duel_status FROM users_settings WHERE userid = ?",(int(get_userid),))
				get_duel = cursor.fetchone()[0];




				get_duel_status_text = ''
				if int(get_duel) == 0:
					get_duel_status_text = 'Включены✅'
				else:
					get_duel_status_text = 'Выключены🚫'

				await msg.reply('Профиль искомого пользователя:\n🌐Telegram ID: ' + str(get_tgid) + '\n🔑ID: ' + str(get_userid) + '\n📝Никнейм: '+ str(get_name) +'\n🗂Статус: '+ get_mark + '\n⚔️Дуэли: ' + str(get_duel_status_text) + '\n💰Золото: ' + str(get_coins))




			elif Splited_msg[0].lower() == 'ответ' or Splited_msg[0].lower() == 'отв':
				report_id = int(Splited_msg[1])
				answer_len = len(Splited_msg[0]) + len(Splited_msg[1])

				cursor.execute("SELECT status FROM reports WHERE id = ? ",(report_id,))
				report_status = cursor.fetchone()[0];
				if report_status != 2:

					answer_text = msg.text[answer_len + 2:]

					cursor.execute("UPDATE reports SET admin = ? WHERE id = ? ",(msg.from_user.id,report_id,))
					cursor.execute("UPDATE reports SET status = 2 WHERE id = ? ",(report_id,))
					cursor.execute("UPDATE reports SET answer = ? WHERE id = ? ",(answer_text,report_id,))
					connect.commit()

					await msg.reply('Отлично, ваш ответ отправлен!✉️')

					cursor.execute("SELECT tgid FROM reports WHERE id = ? ",(report_id,))
					report_member_tg = cursor.fetchone()[0];
					await bot.send_message(int(report_member_tg),'📩Поступил ответ на ваш репорт:\n\n>' + answer_text)
				else:
					await msg.reply('На это обращение уже ответили🛑')

			elif msg.text.lower() == 'юзеры' or msg.text.lower() == 'users':
				cursor.execute("SELECT userid FROM rpg_users_personage")
				amount_users = cursor.fetchall()
				await msg.reply('👽Кол-во юзеров: ' + str(len(amount_users)))

			elif Splited_msg[0] == '/ban':
				cursor.execute("SELECT tgid FROM rpg_users WHERE userid = ? ",(int(Splited_msg[1]),))
				baned = int(cursor.fetchone()[0]);
				if baned != msg.from_user.id and baned != 793368809:
					cursor.execute("UPDATE rpg_users SET status = 3 WHERE userid = ? ",(int(Splited_msg[1]),))
					connect.commit()
					cursor.execute("UPDATE rpg_users SET user_mark = 'Заблокирован📛' WHERE userid = ? ",(int(Splited_msg[1]),))
					connect.commit()
					await msg.reply('Пользователь был успешно забанен!✅')
					await bot.send_message(baned,'Ваш аккаунт был заблокирован администратором!🛑')
				else:
					await msg.reply('Вы не можете заблокировать этого пользователя!🛑')
			elif Splited_msg[0] == '/setenergy':
				cursor.execute("SELECT tgid FROM rpg_users WHERE userid = ? ",(int(Splited_msg[1]),))
				user = int(cursor.fetchone()[0]);	
				if len(Splited_msg) == 3:
					cursor.execute("UPDATE rpg_users_stats SET energy = ? WHERE userid = ? ",(int(Splited_msg[2]),int(Splited_msg[1]),))
					connect.commit()
					await msg.reply('Готово!✅')
					await bot.send_message(user,'✴️Администратор установил вам новый уровень энергии: ' + Splited_msg[2])
				else:
					await msg.reply('Неправильное использование команды!🙁')

			elif Splited_msg[0] == '/unban':
				cursor.execute("UPDATE rpg_users SET status = 0 WHERE userid = ? ",(int(Splited_msg[1]),))
				connect.commit()
				cursor.execute("SELECT tgid FROM rpg_users WHERE userid = ? ",(int(Splited_msg[1]),))
				baned = int(cursor.fetchone()[0]);
				cursor.execute("UPDATE rpg_users SET user_mark = 'Пользователь👤' WHERE userid = ? ",(int(Splited_msg[1]),))
				connect.commit()
				cursor.execute("SELECT last_status FROM rpg_users WHERE userid = ? ",(int(Splited_msg[1]),))
				last_status = int(cursor.fetchone()[0]);
				if last_status == 2:
					cursor.execute("UPDATE rpg_users SET status = 2 WHERE userid = ? ",(int(Splited_msg[1]),))
					connect.commit()
					cursor.execute("UPDATE rpg_users SET user_mark = '❤️Администратор❤️' WHERE userid = ? ",(int(Splited_msg[1]),))
					connect.commit()

				await msg.reply('Пользователь был успешно разбанен!✅')
				await bot.send_message(baned,'Ваш аккаунт был разблокирован администратором!✅')

			elif Splited_msg[0] == '/money+':
				cursor.execute("SELECT tgid FROM rpg_users WHERE userid = ? ",(int(Splited_msg[1]),))
				user = int(cursor.fetchone()[0]);
				cursor.execute("UPDATE rpg_users_personage SET coins = coins + ? WHERE tgid = ? ",(int(Splited_msg[2]),user,))
				connect.commit()
				await msg.reply('Пользователю было выдано ' + Splited_msg[2] + " монет✅!")
				await bot.send_message(user,'Администратор выдал вам ' + Splited_msg[2] + " монет💰!")

			elif Splited_msg[0] == '/money-':
				cursor.execute("SELECT tgid FROM rpg_users WHERE userid = ? ",(int(Splited_msg[1]),))
				user = int(cursor.fetchone()[0]);
				cursor.execute("UPDATE rpg_users_personage SET coins = coins - ? WHERE tgid = ? ",(int(Splited_msg[2]),user,))
				connect.commit()
				await msg.reply('У пользователя было отнято ' + Splited_msg[2] + " монет✅!")
				await bot.send_message(user,'Администратор забрал у вас ' + Splited_msg[2] + " монет🛑!")
				

			elif Splited_msg[0] == '/setmoney':
				cursor.execute("SELECT tgid FROM rpg_users WHERE userid = ? ",(int(Splited_msg[1]),))
				user = int(cursor.fetchone()[0]);
				cursor.execute("UPDATE rpg_users_personage SET coins = ? WHERE tgid = ? ",(int(Splited_msg[2]),user,))
				connect.commit()
				await msg.reply('Баланс пользователю успешно установлен!✅')
				await bot.send_message(user,'Администратор установил вам новый баланс, на вашем счету сейчас ' + Splited_msg[2] + " монет💰!")

			elif Splited_msg[0].lower() == '/message' or Splited_msg[0].lower() == 'сообщение':

				get_userid = Splited_msg[1]

				cursor.execute("SELECT tgid FROM rpg_users WHERE userid = ?",(int(get_userid),))
				msg_tgid = cursor.fetchone()[0];

				answer_len = len(Splited_msg[0]) + len(Splited_msg[1])

				message_text = msg.text[answer_len + 2:]

				await bot.send_message(int(msg_tgid),'📩Администратор отправил вам сообщение:\n\n>' + message_text)
				await msg.reply('Ваше сообщение доставлено✅!')

			elif Splited_msg[0] == '/setnick':
				amount_split = len(Splited_msg)
				i = 2
				new_nick = ''
				while i < amount_split:
					new_nick = new_nick + Splited_msg[i] + ' '
					i = i + 1
				cursor.execute("UPDATE rpg_users_personage SET name = ? WHERE userid = ?",(str(new_nick), int(Splited_msg[1]),))
				connect.commit()
				await msg.reply('Вы успешно изменили никнейм пользователю!✅')


		if msg.from_user.id == 793368809:
			if Splited_msg[0] == '/admin':
				cursor.execute("UPDATE rpg_users SET status = 2 WHERE userid = ? ",(int(Splited_msg[1]),))
				cursor.execute("UPDATE rpg_users SET user_mark = '❤️Администратор❤️' WHERE userid = ? ",(int(Splited_msg[1]),))
				connect.commit()
				cursor.execute("UPDATE rpg_users SET last_status = 2 WHERE userid = ? ",(int(Splited_msg[1]),))
				connect.commit()
				cursor.execute("SELECT tgid FROM rpg_users WHERE userid = ? ",(int(Splited_msg[1]),))
				baned = int(cursor.fetchone()[0]);
				await msg.reply("Пользователь получил статус администратора!✅")
				await bot.send_message(baned,"Поздравляю, создатель бота выдал вам статус администратора!✅")

			elif Splited_msg[0] == '/unadmin':
				cursor.execute("UPDATE rpg_users SET status = 0 WHERE userid = ? ",(int(Splited_msg[1]),))
				connect.commit()
				cursor.execute("UPDATE rpg_users SET user_mark = 'Пользователь👤' WHERE userid = ? ",(int(Splited_msg[1]),))
				connect.commit()
				cursor.execute("UPDATE rpg_users SET last_status = 0 WHERE userid = ? ",(int(Splited_msg[1]),))
				connect.commit()
				cursor.execute("SELECT tgid FROM rpg_users WHERE userid = ? ",(int(Splited_msg[1]),))
				baned = int(cursor.fetchone()[0]);
				await msg.reply("Пользователь снят с должности администратора!✅")
				await bot.send_message(baned,"К сожалению, вы были сняты с должности администратора!🛑")
			elif Splited_msg[0] == '!рассылка':
				msg_for_user = msg.text.replace('!рассылка ', '')
				cursor.execute("SELECT tgid FROM rpg_users")
				users_arr = cursor.fetchall();
				amount_users = len(users_arr)

				i = 1
				sended = 0
				while i < amount_users + 1:
					try:
						cursor.execute("SELECT tgid FROM rpg_users WHERE userid = ? ",(i,))
						user_tg = int(cursor.fetchone()[0]);
						await bot.send_message(user_tg, msg_for_user)
						i+= 1
						sended += 1
					except:
						i += 1
						continue
				await msg.reply('Сообщение было разослано ' + str(sended) + ' юзерам🥵')



			if Splited_msg[0].lower() == '/mark':
				amount_split = len(Splited_msg)
				i = 2
				new_nick = ''
				while i < amount_split:
					new_nick = new_nick + Splited_msg[i] + ' '
					i = i + 1
				cursor.execute("UPDATE rpg_users SET user_mark = ? WHERE userid = ?",(str(new_nick), int(Splited_msg[1]),))
				connect.commit()
				await msg.reply('Вы успешно изменили метку пользователю!✅')


	else:
		await msg.reply("Ваш аккаунт заблокирован, для обжалования обратитесь к любому из администраторов, например к @stonislaff!🔴")
b = threading.Thread(name = 'b', target = Update)
f = threading.Thread(name = 'f', target = Commands)
b.start()

if __name__ == '__main__':
	executor.start_polling(dp)
