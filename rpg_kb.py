from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


btn_add_personage = KeyboardButton('Создать персонажа👶')
add_personage_kb = ReplyKeyboardMarkup(resize_keyboard = True).add(btn_add_personage)


btn_race_1 = KeyboardButton('Эльф')
btn_race_2 = KeyboardButton('Орк')
btn_race_3 = KeyboardButton('Человек')
btn_race_4 = KeyboardButton('Гном')
btn_race_5 = KeyboardButton('Гоблин')
btn_race_6 = KeyboardButton('Ящер')

race_kb = ReplyKeyboardMarkup(resize_keyboard = True).add(btn_race_1).add(btn_race_2).add(btn_race_3).add(btn_race_4).add(btn_race_5).add(btn_race_6)



gender_btn_1 = KeyboardButton('Мужской🙎‍♂️')
gender_btn_2 = KeyboardButton('Женский🙍‍♀️')
gender_kb = ReplyKeyboardMarkup(resize_keyboard = True).add(gender_btn_1).add(gender_btn_2)

work_btn_1 = KeyboardButton('Доставка грузов📦')
work_btn_2 = KeyboardButton('Охота🏹')
work_btn_3 = KeyboardButton('Рыбалка🐠')
work_btn_4 = KeyboardButton('Работа в шахте⛏')

work_kb_1 = ReplyKeyboardMarkup(resize_keyboard = True).add(work_btn_1).add(work_btn_2).add(work_btn_3).add(work_btn_4)
work_btn_false = KeyboardButton("Закончить🔴")
work_kb_2 = ReplyKeyboardMarkup(resize_keyboard = True).add(work_btn_1).add(work_btn_false)
work_kb_3 = ReplyKeyboardMarkup(resize_keyboard = True).add(work_btn_2).add(work_btn_false)
work_kb_4 = ReplyKeyboardMarkup(resize_keyboard = True).add(work_btn_3).add(work_btn_false)
work_kb_5 = ReplyKeyboardMarkup(resize_keyboard = True).add(work_btn_4).add(work_btn_false)



clas_btn_1 = KeyboardButton('Маг')#energy
clas_btn_2 = KeyboardButton('Ассасин')#miss
clas_btn_3 = KeyboardButton('Воин')#damage
clas_btn_4 = KeyboardButton('Берсерк')#critical
clas_btn_5 = KeyboardButton('Паладин')#hp
clas_btn_6 = KeyboardButton('Целитель')#heal
clas_btn_7 = KeyboardButton('Жрец')#vampirise
clas_btn_8 = KeyboardButton('Варвар')#bash

clas_kb = ReplyKeyboardMarkup(resize_keyboard = True).add(clas_btn_1).add(clas_btn_2).add(clas_btn_3).add(clas_btn_4).add(clas_btn_5).add(clas_btn_6).add(clas_btn_7).add(clas_btn_8)

partner_btn_true = KeyboardButton('Принять✅')
partner_btn_false = KeyboardButton('Отклонить❌')

partner_kb = ReplyKeyboardMarkup(resize_keyboard = True).add(partner_btn_true).add(partner_btn_false)

closed_btn = KeyboardButton('Выйти❌') 

shop_btn_1 = KeyboardButton('Энергия⚡️')
shop_kb = ReplyKeyboardMarkup(resize_keyboard = True).add(shop_btn_1).add(closed_btn)

energy_btn_1 = KeyboardButton('25 энергии⚡️')
energy_btn_2 = KeyboardButton('50 энергии⚡️')
energy_btn_3 = KeyboardButton('100 энергии⚡️')

energy_kb = ReplyKeyboardMarkup(resize_keyboard = True).add(energy_btn_1).add(energy_btn_2).add(energy_btn_3).add(closed_btn)


chest_btn_1 = KeyboardButton('Сундук с бронёй👕')
chest_btn_2 = KeyboardButton('Сундук с оружием🔪')
chest_btn_3 = KeyboardButton('Сундук с артефактами🔮')
chest_btn_4 = KeyboardButton('Сундук с питомцами🧸')

chest_kb = ReplyKeyboardMarkup(resize_keyboard = True).add(chest_btn_1).add(chest_btn_2).add(chest_btn_3).add(chest_btn_4).add(closed_btn)


chest_true = KeyboardButton('Да✅')
chest_false = KeyboardButton('Нет❌')

YN_kb = ReplyKeyboardMarkup(resize_keyboard = True).add(chest_true).add(chest_false)

fold_btn_3 = KeyboardButton('Артефакты🔮')
fold_btn_4 = KeyboardButton('Питомцы🧸 ')
fold_btn_1 = KeyboardButton('Броня👕')
fold_btn_2 = KeyboardButton('Оружие🔫')
fold_btn_5 = KeyboardButton('Покинуть склад🚷')

fold_kb = ReplyKeyboardMarkup(resize_keyboard = True).add(fold_btn_1).add(fold_btn_2).add(fold_btn_3).add(fold_btn_4).add(fold_btn_5)


referals = KeyboardButton('У меня нет реферального кода!🛑')
ref_kb = ReplyKeyboardMarkup(resize_keyboard = True).add(referals)
