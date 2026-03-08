from telegram import Update
from telegram.ext import ContextTypes
from services.mal_api import search_manga

async def manga(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text("Use: /manga nome")
        return

    query = " ".join(context.args)

    data = search_manga(query)

    if not data["data"]:
        await update.message.reply_text("Mangá não encontrado.")
        return

    manga = data["data"][0]

    title = manga["title"]
    chapters = manga["chapters"]
    synopsis = manga["synopsis"]

    image = manga["images"]["jpg"]["large_image_url"]

    text = f"""
📖 {title}

📚 CAPÍTULOS: {chapters}

📝 SINOPSE:
{synopsis[:400]}...
"""

    await update.message.reply_photo(
        photo=image,
        caption=text
    )
