import telebot
from telebot import types

# Создаем бота с токеном, замените 'YOUR_BOT_TOKEN' на ваш токен
bot = telebot.TeleBot('YOUR_BOT_TOKEN')

# Пример категорий и подкатегорий товаров
categories = {
    "Электроника": ["Смартфоны", "Ноутбуки", "Телевизоры"],
    "Одежда": ["Мужская одежда", "Женская одежда", "Детская одежда"],
    "Еда": ["Фрукты", "Овощи", "Мясо"],
}

# Обработчик команды /select_category
@bot.message_handler(commands=['select_category'])
def send_category_buttons(message):
    markup = types.InlineKeyboardMarkup()
    for category in categories.keys():
        button = types.InlineKeyboardButton(text=category, callback_data=f"category_{category}")
        markup.add(button)
    bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=markup)

# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: call.data.startswith('category_'))
def callback_inline(call):
    category = call.data.split('_')[1]
    subcategories = categories.get(category, [])

    if subcategories:
        markup = types.InlineKeyboardMarkup()
        for subcategory in subcategories:
            button = types.InlineKeyboardButton(text=subcategory, callback_data=f"subcategory_{subcategory}")
            markup.add(button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Вы выбрали категорию: {category}. Выберите подкатегорию:", reply_markup=markup)
    else:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Подкатегории для категории {category} не найдены.")

# Обработчик нажатий на подкатегории
@bot.callback_query_handler(func=lambda call: call.data.startswith('subcategory_'))
def callback_subcategory_inline(call):
    subcategory = call.data.split('_')[1]
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Вы выбрали подкатегорию: {subcategory}")

# Запуск бота
bot.polling(none_stop=True)
