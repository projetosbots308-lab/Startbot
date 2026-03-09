from telegram import Update
from telegram.ext import ContextTypes
from services.mal_api import search_manga
from deep_translator import GoogleTranslator

def traduzir(texto):
    try:
        return GoogleTranslator(source="auto", target="pt").translate(texto)
    except:
        return texto

# Função usada pelo comando /manga
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

    texto = format_manga(manga)

    await update.message.reply_text(texto)


# Função que formata mangá (para uso também no /ia)
def format_manga(manga):
    titulo = manga.get("title", "Desconhecido")
    capitulos = manga.get("chapters", "Desconhecido")
    score = manga.get("score", "Desconhecido")
    generos = [g["name"] for g in manga.get("genres", [])]
    generos = " | ".join([f"#{g}" for g in generos]) if generos else "Desconhecido"

    synopsis = traduzir(manga.get("synopsis", "Sem sinopse"))
    synopsis = synopsis[:300] + "..." if len(synopsis) > 300 else synopsis

    texto = f"""
📖 {titulo}

📚 Gêneros: {generos}
📑 Capítulos: {capitulos}
⭐ Nota: {score}

📝 Sinopse:
{synopsis}
"""
    return texto
