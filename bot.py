import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("SALES_BOT_TOKEN", "")

logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

ROLES = {
    "\U0001f9d1 Торговый представитель": (
        "Добро пожаловать, коллега! \U0001f9d1\n\n"
        "Для торговых представителей я подготовил самое практичное из курса <b>«Рекорды продаж»</b>:\n\n"
        "\U0001f5fa ДПШМ-маршрут — как проходить точки и выжимать максимум\n"
        "\U0001f4ac Скрипты возражений — реальные фразы, которые работают\n"
        "\U0001f4ca KPI ТП — какие цифры важны и как их улучшить\n\n"
        "\U0001f511 <i>ТП, которые используют ДПШМ-систему, увеличивают продуктивность на 30% уже в первый месяц.</i>\n\n"
        "Мырзахыт свяжется с тобой лично и поделится инструментами. \U0001f447"
    ),
    "\U0001f465 Супервайзер / РОП": (
        "Добро пожаловать, лидер! \U0001f465\n\n"
        "Для супервайзеров и РОП-ов у меня приготовлено самое стратегическое из курса <b>«Рекорды продаж»</b>:\n\n"
        "\U0001f4cb Система контроля ТП — как видеть результат каждого в реальном времени\n"
        "\U0001f3af Постановка планов — формула, которая мотивирует, а не демотивирует\n"
        "\U0001f525 Топ-ошибки супервайзеров — кейсы из реальной дистрибуции\n\n"
        "\U0001f511 <i>Супервайзеры, внедрившие еженедельный разбор маршрутов, увеличили выполнение плана команды на 20–35%.</i>\n\n"
        "Мырзахыт свяжется с тобой лично и предложит стратегию под твою команду. \U0001f447"
    ),
    "\U0001f3e2 Владелец / Дистрибьютор": (
        "Добро пожаловать, партнёр! \U0001f3e2\n\n"
        "Для владельцев и дистрибьюторов у меня приготовлено самое стратегическое из курса <b>«Рекорды продаж»</b>:\n\n"
        "\U0001f50d ДПШМ-система — аудит всей дистрибуции по 4 параметрам\n"
        "\U0001f4b0 Как построить прибыльный дистрибьюторский бизнес: цифры, структура, контроль\n"
        "\U0001f4c9 Топ-ошибки дистрибьюторов — разбор реальных кейсов\n\n"
        "\U0001f511 <i>Дистрибьюторы, которые внедряют ДПШМ-аудит, увеличивают охват на 25–35% уже в первые 90 дней.</i>\n\n"
        "Мырзахыт свяжется с тобой лично и предложит стратегию под твой бизнес. \U0001f447"
    ),
}

ROLE_LIST = list(ROLES.keys())

def role_keyboard():
    buttons = [[KeyboardButton(r)] for r in ROLE_LIST]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)

def details_keyboard():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("\U0001f4f2 Узнать подробнее", url="https://t.me/Mirzahit_Abdylakhatov")
    ]])

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! \U0001f44b\n\n"
        "Я бот канала @fmcgsng — Мырзахыт Абдылахатов, эксперт по дистрибуции и продажам.\n\n"
        "Чтобы я прислал тебе самое полезное — ответь на один вопрос:",
        reply_markup=role_keyboard()
    )

async def handle_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text not in ROLES:
        await update.message.reply_text("Выбери свою роль из кнопок ниже \U0001f447", reply_markup=role_keyboard())
        return
    await update.message.reply_text(ROLES[text], parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
    await update.message.reply_text(
        "Нажми кнопку ниже, чтобы узнать подробнее о курсе \U0001f447",
        reply_markup=details_keyboard()
    )

async def handle_unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Выбери свою роль \U0001f447", reply_markup=role_keyboard())

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    role_filter = filters.TEXT & ~filters.COMMAND & filters.Regex("^(" + "|".join(ROLE_LIST) + ")$")
    app.add_handler(MessageHandler(role_filter, handle_role))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_unknown))
    logger.info("Sales bot started.")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
