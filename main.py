from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

import config

from modules.start import start
from modules.welcome import welcome
from modules.anime import anime
from modules.manga import manga
from modules.season import season
from modules.moderation import ban


app = ApplicationBuilder().token(config.TOKEN).build()


app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("anime", anime))
app.add_handler(CommandHandler("manga", manga))
app.add_handler(CommandHandler("season", season))
app.add_handler(CommandHandler("ban", ban))


app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))


app.run_polling()
