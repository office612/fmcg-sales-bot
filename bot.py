import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler

BOT_TOKEN = os.getenv("SALES_BOT_TOKEN", "")

logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

ROLES = {
    "\U0001f9d1 Торговый представитель": (
        "Добро пожаловать, коллега! \U0001f9d1\n\n"
        "Для торговых представителей я подготовил самое практичное из курса <b>\u00abРекорды продаж\u00bb</b>:\n\n"
        "\U0001f5fa ДПШМ-маршрут — как проходить точки и выжимать максимум\n"
        "\U0001f4ac Скрипты возражений — реальные фразы, которые работают\n"
        "\U0001f4ca KPI ТП — какие цифры важны и как их улучшить\n\n"
        "\U0001f511 <i>ТП, которые используют ДПШМ-систему, увеличивают продуктивность на 30% уже в первый месяц.</i>"
    ),
    "\U0001f465 Супервайзер / РОП": (
        "Добро пожаловать, лидер! \U0001f465\n\n"
        "Для супервайзеров и РОП-ов у меня приготовлено самое стратегическое из курса <b>\u00abРекорды продаж\u00bb</b>:\n\n"
        "\U0001f4cb Система контроля ТП — как видеть результат каждого в реальном времени\n"
        "\U0001f3af Постановка планов — формула, которая мотивирует, а не демотивирует\n"
        "\U0001f525 Топ-ошибки супервайзеров — кейсы из реальной дистрибуции\n\n"
        "\U0001f511 <i>Супервайзеры, внедрившие еженедельный разбор маршрутов, увеличили выполнение плана команды на 20\u201335%.</i>"
    ),
    "\U0001f3e2 Владелец / Дистрибьютор": (
        "Добро пожаловать, партнёр! \U0001f3e2\n\n"
        "Для владельцев и дистрибьюторов у меня приготовлено самое стратегическое из курса <b>\u00abРекорды продаж\u00bb</b>:\n\n"
        "\U0001f50d ДПШМ-система — аудит всей дистрибуции по 4 параметрам\n"
        "\U0001f4b0 Как построить прибыльный дистрибьюторский бизнес: цифры, структура, контроль\n"
        "\U0001f4c9 Топ-ошибки дистрибьюторов — разбор реальных кейсов\n\n"
        "\U0001f511 <i>Дистрибьюторы, которые внедряют ДПШМ-аудит, увеличивают охват на 25\u201335% уже в первые 90 дней.</i>"
    ),
}

ROLE_LIST = list(ROLES.keys())

def role_keyboard():
    buttons = [[KeyboardButton(r)] for r in ROLE_LIST]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)

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
        "\U0001f680 Скоро здесь появится доступ к полному курсу и материалам!\n\n"
        "А пока — подпишись на канал @fmcgsng, чтобы не пропустить обновления \U0001f447",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("\U0001f4e2 Канал FMCG SNG", url="https://t.me/fmcgsng")
        ]])
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
