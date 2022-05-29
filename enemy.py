class Enemy:
	name = 'default'
	damage = 1
	speed = 1
	hp = 1
	gold = 1
	xp = 1
	def GetEnemy(self,stats):	
		if stats == 'name':
			return self.name
		elif stats == 'damage':
			return self.damage
		elif stats == 'speed':
			return self.speed
		elif stats == 'hp':
			return self.hp
		elif stats == 'xp':
			return self.xp
		elif stats == 'gold':
			return self.gold

enemy_0 = Enemy()
enemy_0.name = 'Зомби'
enemy_0.damage = 2
enemy_0.speed = 1
enemy_0.hp = 30
enemy_0.xp = 5
enemy_0.gold = 3 

enemy_1 = Enemy()
enemy_1.name = "Дикая собака" 
enemy_1.damage = 3
enemy_1.speed = 1
enemy_1.hp = 20
enemy_1.xp = 5
enemy_1.gold = 3 


enemy_2 = Enemy()
enemy_2.name = "Медведь" 
enemy_2.damage = 5
enemy_2.speed = 1
enemy_2.hp = 30
enemy_2.xp = 5
enemy_2.gold = 5 


enemy_3 = Enemy()
enemy_3.name = "Скелет" 
enemy_3.damage = 4
enemy_3.speed = 1
enemy_3.hp = 25
enemy_3.xp = 5
enemy_3.gold = 3 


enemy_4 = Enemy()
enemy_4.name = "Огромный скорпион" 
enemy_4.damage = 7
enemy_4.speed = 1
enemy_4.hp = 25
enemy_4.xp = 6
enemy_4.gold = 5 


enemy_5 = Enemy()
enemy_5.name = "Троль" 
enemy_5.damage = 7
enemy_5.speed = 1
enemy_5.hp = 35
enemy_5.xp = 7
enemy_5.gold = 9


enemy_6 = Enemy()
enemy_6.name = "Йети" 
enemy_6.damage = 6 
enemy_6.speed = 1
enemy_6.hp = 35
enemy_6.xp = 6
enemy_6.gold = 9 


enemy_7 = Enemy()
enemy_7.name = "Агрессивная фея" 
enemy_7.damage = 6
enemy_7.speed = 2
enemy_7.hp = 15
enemy_7.xp = 5
enemy_7.gold = 13 


enemy_8 = Enemy()
enemy_8.name = "Эллементаль воды" 
enemy_8.damage = 5
enemy_8.speed = 1
enemy_8.hp = 40
enemy_8.xp = 5
enemy_8.gold = 8 


enemy_9 = Enemy()
enemy_9.name = "Эллементаль огня" 
enemy_9.damage = 9 
enemy_9.speed = 1
enemy_9.hp = 20
enemy_9.xp = 5
enemy_9.gold = 8


enemy_10 = Enemy()
enemy_10.name = "Эллементаль земли" 
enemy_10.damage = 4
enemy_10.speed = 1
enemy_10.hp = 50
enemy_10.xp = 5
enemy_10.gold = 8 


enemy_11 = Enemy()
enemy_11.name = "Эллементаль хаоса" 
enemy_11.damage = 10
enemy_11.speed = 2
enemy_11.hp = 30
enemy_11.xp = 5
enemy_11.gold = 8


enemy_12 = Enemy()
enemy_12.name = "Эллементаль воздуха" 
enemy_12.damage = 8
enemy_12.speed = 3
enemy_12.hp = 30
enemy_12.xp = 5
enemy_12.gold = 8


enemy_13 = Enemy()
enemy_13.name = "Молодой вампир" 
enemy_13.damage = 4
enemy_13.speed = 1
enemy_13.hp = 27
enemy_13.xp = 5
enemy_13.gold = 4 


enemy_14 = Enemy()
enemy_14.name = "Волк" 
enemy_14.damage = 5
enemy_14.speed = 1
enemy_14.hp = 25
enemy_14.xp = 3
enemy_14.gold = 4 


enemy_15 = Enemy()
enemy_15.name = "Оборотень" 
enemy_15.damage = 7
enemy_15.speed = 1
enemy_15.hp = 34
enemy_15.xp = 6
enemy_15.gold = 7 


enemy_16 = Enemy()
enemy_16.name = "Высший оборотень" 
enemy_16.damage = 10
enemy_16.speed = 2
enemy_16.hp = 40
enemy_16.xp = 10
enemy_16.gold = 10


enemy_17 = Enemy()
enemy_17.name = "Древний оборотень" 
enemy_17.damage = 14
enemy_17.speed = 2
enemy_17.hp = 43
enemy_17.xp = 15
enemy_17.gold = 15


enemy_18 = Enemy()
enemy_18.name = "Высший вампир" 
enemy_18.damage = 8
enemy_18.speed = 1
enemy_18.hp = 35
enemy_18.xp = 10
enemy_18.gold = 10


enemy_19 = Enemy()
enemy_19.name = "Древний вампир" 
enemy_19.damage = 15
enemy_19.speed = 3
enemy_19.hp = 45
enemy_19.xp = 20
enemy_19.gold = 20


enemy_20 = Enemy()
enemy_20.name = "Леший" 
enemy_20.damage = 6
enemy_20.speed = 2
enemy_20.hp = 30
enemy_20.xp = 10
enemy_20.gold = 10


enemy_21 = Enemy()
enemy_21.name = "Ведьма" 
enemy_21.damage = 10
enemy_21.speed = 1 
enemy_21.hp = 30
enemy_21.xp = 8
enemy_21.gold = 8 


enemy_22 = Enemy()
enemy_22.name = "Дух леса" 
enemy_22.damage = 7
enemy_22.speed = 1
enemy_22.hp = 34
enemy_22.xp = 6
enemy_22.gold = 7 


enemy_23 = Enemy()
enemy_23.name = "Бес" 
enemy_23.damage = 6
enemy_23.speed = 1
enemy_23.hp = 23
enemy_23.xp = 6
enemy_23.gold = 6 


enemy_24 = Enemy()
enemy_24.name = "Одержимый человек" 
enemy_24.damage = 5
enemy_24.speed = 1
enemy_24.hp = 30
enemy_24.xp = 6
enemy_24.gold = 10 


enemy_25 = Enemy()
enemy_25.name = "Адская гончая" 
enemy_25.damage = 5
enemy_25.speed = 2
enemy_25.hp = 30
enemy_25.xp = 8
enemy_25.gold = 9 


enemy_26 = Enemy()
enemy_26.name = "Падший ангел" 
enemy_26.damage = 10
enemy_26.speed = 2
enemy_26.hp = 40
enemy_26.xp = 15
enemy_26.gold = 15


enemy_27 = Enemy()
enemy_27.name = "Верховный демон" 
enemy_27.damage = 12
enemy_27.speed = 2
enemy_27.hp = 40
enemy_27.xp = 14
enemy_27.gold = 15


enemy_28 = Enemy()
enemy_28.name = "Адский цербер" 
enemy_28.damage = 8
enemy_28.speed = 2
enemy_28.hp = 40
enemy_28.xp = 10
enemy_28.gold = 12


enemy_29 = Enemy()
enemy_29.name = "Суккуб" 
enemy_29.damage = 7
enemy_29.speed = 1
enemy_29.hp = 30
enemy_29.xp = 14
enemy_29.gold = 11


enemy_30 = Enemy()
enemy_30.name = "Джин" 
enemy_30.damage = 15
enemy_30.speed = 1
enemy_30.hp = 40
enemy_30.xp = 15
enemy_30.gold = 15


enemy_31 = Enemy()
enemy_31.name = "Каменный голем" 
enemy_31.damage = 6
enemy_31.speed = 1
enemy_31.hp = 60
enemy_31.xp = 9
enemy_31.gold = 19 


enemy_32 = Enemy()
enemy_32.name = "Кристальный голем" 
enemy_32.damage = 8
enemy_32.speed = 1
enemy_32.hp = 100
enemy_32.xp = 20
enemy_32.gold = 40


enemy_33 = Enemy()
enemy_33.name = "Химера" 
enemy_33.damage = 10
enemy_33.speed = 2
enemy_33.hp = 40
enemy_33.xp = 10
enemy_33.gold = 10


enemy_34 = Enemy()
enemy_34.name = "Василиск" 
enemy_34.damage = 7
enemy_34.speed = 1
enemy_34.hp = 33
enemy_34.xp = 10
enemy_34.gold = 10


enemy_35 = Enemy()
enemy_35.name = "Гидра" 
enemy_35.damage = 12
enemy_35.speed = 2
enemy_35.hp = 50
enemy_35.xp = 15
enemy_35.gold = 16


enemy_36 = Enemy()
enemy_36.name = "Домовой" 
enemy_36.damage = 5
enemy_36.speed = 1
enemy_36.hp = 20
enemy_36.xp = 15
enemy_36.gold = 15


enemy_37 = Enemy()
enemy_37.name = "Кикимора" 
enemy_37.damage = 7
enemy_37.speed = 1
enemy_37.hp = 25
enemy_37.xp = 10
enemy_37.gold = 5


enemy_38 = Enemy()
enemy_38.name = "Минотавр" 
enemy_38.damage = 10
enemy_38.speed = 1
enemy_38.hp = 33
enemy_38.xp = 8
enemy_38.gold = 9 


enemy_39 = Enemy()
enemy_39.name = "Русалка" 
enemy_39.damage = 7
enemy_39.speed = 1
enemy_39.hp = 25
enemy_39.xp = 20
enemy_39.gold = 13


enemy_40 = Enemy()
enemy_40.name = "Циклоп" 
enemy_40.damage = 15
enemy_40.speed = 1 
enemy_40.hp = 55
enemy_40.xp = 30
enemy_40.gold = 30


enemy_41 = Enemy()
enemy_41.name = "Огненный дракон" 
enemy_41.damage = 20
enemy_41.speed = 1
enemy_41.hp = 50
enemy_41.xp = 20
enemy_41.gold = 20


enemy_42 = Enemy()
enemy_42.name = "Сумеречный дракон" 
enemy_42.damage = 30
enemy_42.speed = 2
enemy_42.hp = 70
enemy_42.xp = 100
enemy_42.gold = 100


enemy_43 = Enemy()
enemy_43.name = "Ледяной дракон" 
enemy_43.damage = 15
enemy_43.speed = 2
enemy_43.hp = 50
enemy_43.xp = 20
enemy_43.gold = 20


enemy_44 = Enemy()
enemy_44.name = "Костяной дракон" 
enemy_44.damage = 6
enemy_44.speed = 1
enemy_44.hp = 100
enemy_44.xp = 30
enemy_44.gold = 30


enemy_45 = Enemy()
enemy_45.name = "Виверна" 
enemy_45.damage = 7
enemy_45.speed = 1
enemy_45.hp = 34
enemy_45.xp = 15
enemy_45.gold = 15


enemy_46 = Enemy()
enemy_46.name = "Булаждающая душа" 
enemy_46.damage = 6
enemy_46.speed = 1
enemy_46.hp = 20
enemy_46.xp = 8
enemy_46.gold = 8 


enemy_47 = Enemy()
enemy_47.name = "Мумия" 
enemy_47.damage = 7
enemy_47.speed = 1 
enemy_47.hp = 25
enemy_47.xp = 8
enemy_47.gold = 8


enemy_48 = Enemy()
enemy_48.name = "Вендиго" 
enemy_48.damage = 12 
enemy_48.speed = 1
enemy_48.hp = 30
enemy_48.xp = 12
enemy_48.gold = 12


enemy_49 = Enemy()
enemy_49.name = "Сгусток слизи" 
enemy_49.damage = 1
enemy_49.speed = 1
enemy_49.hp = 50
enemy_49.xp = 7
enemy_49.gold = 3 


enemy_50 = Enemy()
enemy_50.name = "Гуль" 
enemy_50.damage = 8 
enemy_50.speed = 1
enemy_50.hp = 30
enemy_50.xp = 9
enemy_50.gold = 10


enemy_51 = Enemy()
enemy_51.name = "Сирена" 
enemy_51.damage = 9
enemy_51.speed = 1
enemy_51.hp = 30
enemy_51.xp = 12
enemy_51.gold = 15


enemy_52 = Enemy()
enemy_52.name = "Валькирия" 
enemy_52.damage = 13
enemy_52.speed = 1 
enemy_52.hp = 30
enemy_52.xp = 12
enemy_52.gold = 13


enemy_53 = Enemy()
enemy_53.name = "Банши" 
enemy_53.damage = 9
enemy_53.speed = 1
enemy_53.hp = 30
enemy_53.xp = 13
enemy_53.gold = 12


enemy_54 = Enemy()
enemy_54.name = "Гарпия" 
enemy_54.damage = 10
enemy_54.speed = 2
enemy_54.hp = 25
enemy_54.xp = 13
enemy_54.gold = 14


enemy_55 = Enemy()
enemy_55.name = "Грифон" 
enemy_55.damage = 15
enemy_55.speed = 2
enemy_55.hp = 50
enemy_55.xp = 40
enemy_55.gold = 40


enemy_56 = Enemy()
enemy_56.name = "Кентавр" 
enemy_56.damage = 7
enemy_56.speed = 1
enemy_56.hp = 35
enemy_56.xp = 12
enemy_56.gold = 7


enemy_57 = Enemy()
enemy_57.name = "Нимфа" 
enemy_57.damage = 7
enemy_57.speed = 1
enemy_57.hp = 25
enemy_57.xp = 6
enemy_57.gold = 16


enemy_58 = Enemy()
enemy_58.name = "Сатир" 
enemy_58.damage = 8
enemy_58.speed = 2
enemy_58.hp = 20
enemy_58.xp = 20
enemy_58.gold = 20


enemy_59 = Enemy()
enemy_59.name = "Гигантская саламандра" 
enemy_59.damage = 10
enemy_59.speed = 1
enemy_59.hp = 40
enemy_59.xp = 12
enemy_59.gold = 10


enemy_60 = Enemy()
enemy_60.name = "Феникс" 
enemy_60.damage = 20
enemy_60.speed = 1
enemy_60.hp = 20
enemy_60.xp = 20
enemy_60.gold = 20


enemy_61 = Enemy()
enemy_61.name = "Пожиратель теней" 
enemy_61.damage = 9
enemy_61.speed = 2
enemy_61.hp = 30
enemy_61.xp = 12
enemy_61.gold = 12


enemy_62 = Enemy()
enemy_62.name = "Ловец снов" 
enemy_62.damage = 10
enemy_62.speed = 1
enemy_62.hp = 30
enemy_62.xp = 11
enemy_62.gold = 13


enemy_63 = Enemy()
enemy_63.name = "Собиратель душ" 
enemy_63.damage = 14
enemy_63.speed = 1
enemy_63.hp = 40
enemy_63.xp = 14
enemy_63.gold = 14


enemy_64 = Enemy()
enemy_64.name = "Морской змей" 
enemy_64.damage = 10
enemy_64.speed = 2
enemy_64.hp = 40
enemy_64.xp = 20
enemy_64.gold = 20


enemy_65 = Enemy()
enemy_65.name = "Сфинкс" 
enemy_65.damage = 10
enemy_65.speed = 1
enemy_65.hp = 32
enemy_65.xp = 15
enemy_65.gold = 11


enemy_66 = Enemy()
enemy_66.name = "Горгона" 
enemy_66.damage = 10
enemy_66.speed = 1
enemy_66.hp = 35
enemy_66.xp = 20
enemy_66.gold = 20


enemy_67 = Enemy()
enemy_67.name = "Келпи" 
enemy_67.damage = 7 
enemy_67.speed = 2
enemy_67.hp = 23
enemy_67.xp = 13
enemy_67.gold = 20


enemy_68 = Enemy()
enemy_68.name = "Драугр" 
enemy_68.damage = 13
enemy_68.speed = 1
enemy_68.hp = 30
enemy_68.xp = 5
enemy_68.gold = 5 


enemy_69 = Enemy()
enemy_69.name = "Гигансткий паук" 
enemy_69.damage = 15 
enemy_69.speed = 1
enemy_69.hp = 31
enemy_69.xp = 9
enemy_69.gold = 4 


enemy_70 = Enemy()
enemy_70.name = "Ехидна" 
enemy_70.damage = 7 
enemy_70.speed = 2
enemy_70.hp = 24
enemy_70.xp = 13
enemy_70.gold = 12


enemy_71 = Enemy()
enemy_71.name = "Кикимора" 
enemy_71.damage = 12
enemy_71.speed = 1
enemy_71.hp = 26
enemy_71.xp = 12
enemy_71.gold = 13


enemy_72 = Enemy()
enemy_72.name = "Водяной" 
enemy_72.damage = 14
enemy_72.speed = 1
enemy_72.hp = 30
enemy_72.xp = 14
enemy_72.gold = 15


enemy_73 = Enemy()
enemy_73.name = "Улитка из бара(минибос)" 
enemy_73.damage = 20 
enemy_73.speed = 1
enemy_73.hp = 100
enemy_73.xp = 50
enemy_73.gold = 50


enemy_74 = Enemy()
enemy_74.name = "Жнец" 
enemy_74.damage = 20
enemy_74.speed = 1 
enemy_74.hp = 20
enemy_74.xp = 20
enemy_74.gold = 20


enemy_75 = Enemy()
enemy_75.name = "Злая тень" 
enemy_75.damage = 5
enemy_75.speed = 2
enemy_75.hp = 50
enemy_75.xp = 1
enemy_75.gold = 1 




enemy_arr = [enemy_0,enemy_1,enemy_2,enemy_3,enemy_4,enemy_5,enemy_6,enemy_7,enemy_8,enemy_9,enemy_10,enemy_11,enemy_12,enemy_13,enemy_14,enemy_15,enemy_16,enemy_17,enemy_18,enemy_19,enemy_20,enemy_21,enemy_22,enemy_23,enemy_24,enemy_25,enemy_26,enemy_27,enemy_28,enemy_29,enemy_30,enemy_31,enemy_32,enemy_33,enemy_34,enemy_35,enemy_36,enemy_37,enemy_38,enemy_39,enemy_40,enemy_41,enemy_42,enemy_43,enemy_44,enemy_45,enemy_46,enemy_47,enemy_48,enemy_49,enemy_50,enemy_51,enemy_52,enemy_53,enemy_54,enemy_55,enemy_56,enemy_57,enemy_58,enemy_59,enemy_60,enemy_61,enemy_62,enemy_63,enemy_64,enemy_65,enemy_66,enemy_67,enemy_68,enemy_69,enemy_70,enemy_71,enemy_72,enemy_73,enemy_74,enemy_75]