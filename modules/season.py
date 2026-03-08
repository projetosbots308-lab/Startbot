from telegram import Update
from telegram.ext import ContextTypes
from services.mal_api import season_now

async def season(update: Update, context: ContextTypes.DEFAULT_TYPE):

    data = season_now()

    animes = data["data"][:10]

    text = "📅 ANIMES DA TEMPORADA:\n\n"

    for a in animes:
        text += f"• {a['title']}\n"

    await update.message.reply_text(text)
