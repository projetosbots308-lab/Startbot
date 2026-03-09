from telegram import Update
from telegram.ext import ContextTypes
from services.mal_api import search_manga
from deep_translator import GoogleTranslator


def traduzir(texto):
    try:
        return GoogleTranslator(source="auto", target="pt").translate(texto)
    except:
        return texto


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

    titulo = manga["title"]
    capitulos = manga["chapters"]
    score = manga["score"]

    synopsis = traduzir(manga["synopsis"])
    synopsis = synopsis[:300] + "..."

    generos = [g["name"] for g in manga["genres"]]
    generos = " | ".join([f"#{g}" for g in generos])

    image = manga["images"]["jpg"]["large_image_url"]

    texto = f"""
📖 {titulo}

📚 GÊNEROS: {generos}

📑 CAPÍTULOS: {capitulos}
⭐ NOTA: {score}

📝 SINOPSE:
{synopsis}
"""

    await update.message.reply_photo(
        photo=image,
        caption=texto
        )
