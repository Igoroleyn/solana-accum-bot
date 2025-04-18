import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import os

# Установи свой Telegram user ID тут
OWNER_ID = 123456789  # заменишь на свой ID

# Токены по умолчанию
tracked_tokens = {"SOL", "BONK", "WIF", "JUP", "SHDW"}

# Языки
LANGUAGES = {"ru": "Русский", "en": "English"}
user_language = {}

# Логгирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("Access denied.")
        return
    lang = user_language.get(update.effective_user.id, 'ru')
    if lang == 'ru':
        await update.message.reply_text("Привет! Я бот для отслеживания накопления токенов Solana.")
    else:
        await update.message.reply_text("Hi! I am a bot that tracks token accumulation on Solana.")

# Команда /language
async def language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Русский", callback_data='lang_ru'),
                 InlineKeyboardButton("English", callback_data='lang_en')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose language / Выберите язык:", reply_markup=reply_markup)

# Обработка выбора языка
async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if query.data == 'lang_ru':
        user_language[user_id] = 'ru'
        await query.edit_message_text("Язык установлен: Русский")
    elif query.data == 'lang_en':
        user_language[user_id] = 'en'
        await query.edit_message_text("Language set to: English")

# Команда /accum
async def accum(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("Access denied.")
        return
    token = context.args[0].upper() if context.args else None
    if not token:
        await update.message.reply_text("Введите токен: /accum WIF")
        return
    await update.message.reply_text(f"[Demo] Накопление токена {token} — 2.3M за последние 7д")

# Команда /addtoken
async def add_token(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("Access denied.")
        return
    token = context.args[0].upper() if context.args else None
    if not token:
        await update.message.reply_text("Введите токен: /addtoken WIF")
        return
    tracked_tokens.add(token)
    await update.message.reply_text(f"Токен {token} добавлен в список отслеживаемых.")

# Команда /mytokens
async def my_tokens(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("Access denied.")
        return
    tokens = ", ".join(tracked_tokens)
    await update.message.reply_text(f"Отслеживаемые токены: {tokens}")

# Основной запуск бота
if __name__ == '__main__':
    token = os.getenv("BOT_TOKEN")
    if not token:
        print("Bot token is missing!")
        exit(1)

    # Выведем токен в консоль для проверки
    print(f"Bot Token: {token}")  # Это выведет токен в консоль

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("language", language))
    app.add_handler(CommandHandler("accum", accum))
    app.add_handler(CommandHandler("addtoken", add_token))
    app.add_handler(CommandHandler("mytokens", my_tokens))
    app.add_handler(CallbackQueryHandler(set_language))

    app.run_polling()

