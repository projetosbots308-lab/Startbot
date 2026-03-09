from telegram import Update
from telegram.ext import ContextTypes
from services.mal_api import search_anime
from utils.formatters import format_anime


async def anime(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text("Use: /anime nome")
        return

    query = " ".join(context.args)

    data = search_anime(query)

    if not data["data"]:
        await update.message.reply_text("Anime não encontrado.")
        return

    anime = data["data"][0]

    caption = format_anime(anime)

    image = anime["images"]["jpg"]["large_image_url"]

    await update.message.reply_photo(
        photo=image,
        caption=caption,
        parse_mode="HTML"
    )
